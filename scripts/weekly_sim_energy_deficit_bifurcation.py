"""
Weekly Simulation: Energy Deficit Bifurcation Phase Diagram.

Performs a 2D parameter sweep of the Energy Deficit Window across (chi_kappa, L) space.
Generates a phase diagram showing where AIS vulnerability is highest (R_deficit > 1).

Phase Diagram:
- X-axis: Spinal Length L (0.25 - 0.55 m)
- Y-axis: IEC Coupling Strength chi_kappa (0.01 - 0.10)
- Color: R_deficit ratio and Cobb angle magnitude.

Outputs:
- outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv
- outputs/figures/phase_diagram_energy_deficit.png
- outputs/figures/phase_diagram_energy_deficit_cobb.png

Reference: Manuscript Section 4.6, H_2026_02_08_EnergyPhase
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    sys.path.append('src')
    from spinalmodes.iec import solve_beam_static

def generate_bimodal_gaussian_field(s, L):
    """
    Generate the bimodal Gaussian information field I(s).
    Formula from manuscript/sections/methods.tex.
    """
    if L == 0:
        return np.full_like(s, 0.3)

    s_norm = s / L

    # Parameters from prompt/manuscript
    A_c = 0.5; s_c = 0.80; sigma_c = 0.08
    A_l = 0.7; s_l = 0.25; sigma_l = 0.10
    I_0 = 0.3

    term_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    term_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return term_c + term_l + I_0

def run_simulation():
    print("Starting Energy Deficit Bifurcation Simulation (2D Sweep)...")

    # 1. Setup Parameters
    chi_kappa_range = np.linspace(0.01, 0.10, 20)
    L_range = np.linspace(0.25, 0.55, 20)

    # Fixed Parameters
    rho = 1100.0
    A_cross = 0.001
    g = 9.81
    E0 = 1.0e9
    chi_E = 0.10
    I_moment = A_cross**2 / (4 * np.pi)

    # Lateral Asymmetry Perturbation
    epsilon_asym = 0.03

    # 2. Determine Reference S_0
    # Reference condition: chi_kappa = 0.05, L = 0.35
    print("Calibrating Proprioceptive Supply S_0...")
    L_ref = 0.35
    chi_kappa_ref = 0.05

    def calculate_p_counter(L_val, chi_kappa_val):
        n_nodes = 100
        s = np.linspace(0, L_val, n_nodes)
        I_field = generate_bimodal_gaussian_field(s, L_val)
        grad_I = np.gradient(I_field, s)
        E_field = E0 * (1.0 + chi_E * I_field)

        # IEC Case
        kappa_target_iec = chi_kappa_val * grad_I
        theta_iec, kappa_iec = solve_beam_static(
            s=s, kappa_target=kappa_target_iec, E_field=E_field,
            M_active=np.zeros_like(s), I_moment=I_moment,
            P_load=0.0, distributed_load=rho * A_cross * g
        )

        # Passive Case
        theta_pass, kappa_pass = solve_beam_static(
            s=s, kappa_target=np.zeros_like(s), E_field=E_field,
            M_active=np.zeros_like(s), I_moment=I_moment,
            P_load=0.0, distributed_load=rho * A_cross * g
        )

        # P_counter
        curvature_diff_sq = (kappa_iec - kappa_pass)**2
        P_val = rho * A_cross * g * (L_val**2) * np.mean(curvature_diff_sq)

        # D_geo
        D_geo_val = np.sqrt(np.mean((theta_iec - theta_pass)**2))

        return P_val, D_geo_val

    P_ref, _ = calculate_p_counter(L_ref, chi_kappa_ref)
    S_0 = P_ref
    print(f"Calibration complete. S_0 = {S_0:.6e} (at L={L_ref}, chi_k={chi_kappa_ref})")

    # 3. Parameter Sweep
    results = []

    print(f"Sweeping {len(chi_kappa_range)}x{len(L_range)} grid...")

    for chi_kappa in chi_kappa_range:
        for L in L_range:
            # Step 1: Sagittal Analysis (Thermodynamic Cost)
            P_counter, D_geo = calculate_p_counter(L, chi_kappa)

            # Proprioceptive Supply
            S_proprio = S_0 * (L / 0.35)**0.7
            R_deficit = P_counter / S_proprio

            # Step 2: Lateral Analysis (Cobb Angle)
            # Lateral Stiffness Reduction
            if R_deficit > 1.0:
                E_lat_val = E0 / R_deficit
            else:
                E_lat_val = E0

            # Lateral Asymmetry
            # kappa_lat(s) = (epsilon_asym / L) * sin(pi * s / L)
            n_nodes = 100
            s = np.linspace(0, L, n_nodes)
            kappa_lat_target = (epsilon_asym / L) * np.sin(np.pi * s / L)

            # Solve Lateral Beam (Constant Stiffness E_lat_val)
            # We include a lateral load component (10% of gravity) to represent a
            # "tilted" perturbation or P-delta effect. This ensures that the
            # stiffness reduction (E_lat_val) actually amplifies the deformation.
            # Without this external moment, theta depends only on kappa_target.
            w_lat = 0.1 * rho * A_cross * g

            theta_lat, _ = solve_beam_static(
                s=s, kappa_target=kappa_lat_target,
                E_field=np.full_like(s, E_lat_val),
                M_active=np.zeros_like(s), I_moment=I_moment,
                P_load=0.0, distributed_load=w_lat
            )

            cobb_angle = np.rad2deg(np.max(theta_lat) - np.min(theta_lat))

            results.append({
                'chi_kappa': chi_kappa,
                'L': L,
                'P_counter': P_counter,
                'S_proprio': S_proprio,
                'R_deficit': R_deficit,
                'D_geo': D_geo,
                'Cobb_angle': cobb_angle
            })

    df = pd.DataFrame(results)

    # 4. Save Results
    output_dir = Path('outputs/thermodynamic_cost')
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / 'phase_diagram_energy_deficit.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved sweep data to {csv_path}")

    # 5. Generate Plots
    fig_dir = Path('outputs/figures')
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Prepare Pivot Tables for Heatmaps
    pivot_R = df.pivot(index='chi_kappa', columns='L', values='R_deficit')
    pivot_Cobb = df.pivot(index='chi_kappa', columns='L', values='Cobb_angle')

    X, Y = np.meshgrid(L_range, chi_kappa_range)

    # Plot 1: R_deficit Phase Diagram
    plt.figure(figsize=(10, 8))
    # Note: imshow logic requires careful orientation. pcolormesh is safer with X, Y.
    # pivot index is Y (chi_kappa), columns is X (L).
    # pivot values need to be passed correctly.
    Z_R = pivot_R.values

    cp = plt.contourf(X, Y, Z_R, levels=20, cmap='RdYlBu_r')
    plt.colorbar(cp, label='Energy Deficit Ratio ($R_{deficit}$)')

    # Contour line at R=1
    cs = plt.contour(X, Y, Z_R, levels=[1.0], colors='k', linewidths=2, linestyles='--')
    plt.clabel(cs, inline=1, fmt='R=1.0')

    plt.title('Energy Deficit Phase Diagram\n($R_{deficit} = P_{counter} / S_{proprio}$)')
    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Coupling Strength $\chi_{\kappa}$')
    plt.grid(True, alpha=0.3)

    fig_path_R = fig_dir / 'phase_diagram_energy_deficit.png'
    plt.savefig(fig_path_R, dpi=300)
    plt.close()
    print(f"Saved R_deficit phase diagram to {fig_path_R}")

    # Plot 2: Cobb Angle Phase Diagram
    plt.figure(figsize=(10, 8))
    Z_Cobb = pivot_Cobb.values

    cp = plt.contourf(X, Y, Z_Cobb, levels=20, cmap='magma')
    plt.colorbar(cp, label='Cobb Angle (deg)')

    # Overlay R=1 boundary
    cs = plt.contour(X, Y, Z_R, levels=[1.0], colors='w', linewidths=2, linestyles='--')
    plt.clabel(cs, inline=1, fmt='R=1.0')

    plt.title('Emergent Scoliosis Magnitude\n(Lateral Asymmetry $\epsilon_{asym}=0.03$)')
    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Coupling Strength $\chi_{\kappa}$')
    plt.grid(True, alpha=0.3)

    fig_path_Cobb = fig_dir / 'phase_diagram_energy_deficit_cobb.png'
    plt.savefig(fig_path_Cobb, dpi=300)
    plt.close()
    print(f"Saved Cobb angle phase diagram to {fig_path_Cobb}")

if __name__ == "__main__":
    run_simulation()
