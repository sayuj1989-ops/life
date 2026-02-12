"""
Weekly Simulation: Energy Deficit Bifurcation.

Performs a 2D parameter sweep of the Energy Deficit Window across (chi_kappa, L) space.
Generates a phase diagram showing where AIS vulnerability is highest (R_deficit > 1).
"""

import sys
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    # Fallback if running from script dir
    sys.path.append(str(Path(__file__).parent.parent / "src"))
    from spinalmodes.iec import solve_beam_static

def generate_bimodal_gaussian_field(s, L):
    """
    Generate the bimodal Gaussian information field I(s).
    Formula from manuscript/sections/methods.tex:
    I(s) = A_c * exp(-((s/L - s_c)^2)/(2*sigma_c^2)) +
           A_l * exp(-((s/L - s_l)^2)/(2*sigma_l^2)) + I_0
    """
    if L <= 0:
        return np.full_like(s, 0.3)

    s_norm = s / L

    # Parameters
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08

    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10

    I_0 = 0.3

    # Calculate components
    term_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    term_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return term_c + term_l + I_0

def compute_p_counter(L, chi_kappa, chi_E=0.10, E0=1.0e9, rho=1100, A=0.001, g=9.81):
    """
    Computes P_counter for a given configuration.
    """
    n_nodes = 100
    s = np.linspace(0, L, n_nodes)

    # Material properties
    I_moment = A**2 / (4 * np.pi)
    distributed_load = rho * A * g # Gravity load

    # 1. Generate Fields
    I_field = generate_bimodal_gaussian_field(s, L)
    grad_I = np.gradient(I_field, s)
    E_field = E0 * (1.0 + chi_E * I_field)

    # 2. Sagittal IEC Solution (Active)
    kappa_target_iec = chi_kappa * grad_I
    theta_iec, kappa_iec = solve_beam_static(
        s=s,
        kappa_target=kappa_target_iec,
        E_field=E_field,
        M_active=np.zeros_like(s),
        I_moment=I_moment,
        P_load=0.0,
        distributed_load=distributed_load
    )

    # 3. Passive Solution (No Information)
    kappa_target_pass = np.zeros_like(s)
    theta_pass, kappa_pass = solve_beam_static(
        s=s,
        kappa_target=kappa_target_pass,
        E_field=E_field,
        M_active=np.zeros_like(s),
        I_moment=I_moment,
        P_load=0.0,
        distributed_load=distributed_load
    )

    # 4. Compute P_counter
    # P ~ rho*A*g * L^2 * <(kappa_iec - kappa_pass)^2>
    curvature_diff_sq = (kappa_iec - kappa_pass)**2
    mean_diff_sq = np.mean(curvature_diff_sq)
    P_counter = 1.0 * rho * A * g * (L**2) * mean_diff_sq

    # 5. Geodesic Deviation
    D_geo = np.sqrt(np.mean((theta_iec - theta_pass)**2))

    return P_counter, D_geo

def run_simulation():
    print("Running Weekly Sim: Energy Deficit Bifurcation Phase Diagram...")

    # 1. Setup Parameters
    chi_kappa_vals = np.linspace(0.01, 0.10, 20)
    L_vals = np.linspace(0.25, 0.55, 20)

    # Fixed Params
    rho = 1100
    A = 0.001
    g = 9.81
    E0 = 1.0e9
    chi_E = 0.10

    # 2. Reference Proprioceptive Supply S0
    # S_proprio(L) = S_0 * (L/L0)^0.7
    # S_0 is P_counter at L=0.35, chi_kappa=0.05
    ref_L = 0.35
    ref_chi = 0.05
    S0, _ = compute_p_counter(ref_L, ref_chi, chi_E, E0, rho, A, g)
    print(f"Reference S0 (P_counter at L={ref_L}, chi={ref_chi}): {S0:.4e} N/m")

    results = []

    # 3. Parameter Sweep
    total_steps = len(chi_kappa_vals) * len(L_vals)
    step_count = 0

    for chi in chi_kappa_vals:
        for L in L_vals:
            step_count += 1
            if step_count % 50 == 0:
                print(f"Progress: {step_count}/{total_steps}")

            # A. Compute Thermodynamics
            P_counter, D_geo = compute_p_counter(L, chi, chi_E, E0, rho, A, g)

            # S_proprio
            S_proprio = S0 * (L / ref_L)**0.7

            # R_deficit
            R_deficit = P_counter / S_proprio

            # B. Compute Lateral Stability (Cobb Angle)
            # Lateral Simulation with perturbation epsilon
            epsilon_asym = 0.03
            w_lat = 0.1 * rho * A * g # 10% gravity sideways

            # Softening Model: If Deficit, stiffness drops
            # E_eff = E0 / max(1, R_deficit)
            softening_factor = max(1.0, R_deficit)
            E_lat_base = E0 # Assuming isotropic base stiffness for simplicity
            E_lat_field = (E_lat_base / softening_factor) * np.ones_like(np.linspace(0, L, 100))

            # Solve Lateral Beam
            # kappa_target_lat = epsilon_asym (constant)
            s_lat = np.linspace(0, L, 100)
            kappa_target_lat = np.full_like(s_lat, epsilon_asym)
            I_moment = A**2 / (4 * np.pi)

            theta_lat, _ = solve_beam_static(
                s=s_lat,
                kappa_target=kappa_target_lat,
                E_field=E_lat_field,
                M_active=np.zeros_like(s_lat),
                I_moment=I_moment,
                P_load=0.0,
                distributed_load=w_lat
            )

            cobb_angle = np.rad2deg(np.max(theta_lat) - np.min(theta_lat))

            results.append({
                'chi_kappa': chi,
                'L': L,
                'P_counter': P_counter,
                'S_proprio': S_proprio,
                'R_deficit': R_deficit,
                'D_geo': D_geo,
                'Cobb_angle': cobb_angle
            })

    # 4. Save Results
    output_dir = Path('outputs/thermodynamic_cost')
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(results)
    csv_path = output_dir / 'phase_diagram_energy_deficit.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved data to {csv_path}")

    # 5. Generate Plots
    fig_dir = Path('outputs/figures')
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Pivot for heatmap
    pivot_R = df.pivot(index='chi_kappa', columns='L', values='R_deficit')
    pivot_Cobb = df.pivot(index='chi_kappa', columns='L', values='Cobb_angle')

    X_L = pivot_R.columns.values
    Y_chi = pivot_R.index.values

    # Plot 1: R_deficit Phase Diagram
    plt.figure(figsize=(10, 8))
    # Use pcolormesh
    # Note: pcolormesh X, Y defines corners, or centers. Using simple imshow or contourf is easier.
    X, Y = np.meshgrid(X_L, Y_chi)

    # Contourf
    levels = np.linspace(0, 3.0, 31) # Cap at 3 for visibility
    cp = plt.contourf(X, Y, pivot_R.values, levels=levels, cmap='RdYlBu_r', extend='max')
    cbar = plt.colorbar(cp, label='Energy Deficit Ratio ($R_{deficit}$)')

    # Critical Boundary R=1
    plt.contour(X, Y, pivot_R.values, levels=[1.0], colors='k', linewidths=2, linestyles='--')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Coupling Strength $\chi_\kappa$')
    plt.title('Phase Diagram: Energy Deficit Window ($P_{counter} / S_{proprio}$)')

    # Annotate regions
    plt.text(0.30, 0.02, 'Stable Region\n($R < 1$)', color='blue', fontweight='bold')
    plt.text(0.45, 0.08, 'Instability Wedge\n($R > 1$)', color='red', fontweight='bold')

    plt.savefig(fig_dir / 'phase_diagram_energy_deficit.png', dpi=300)
    plt.close()

    # Plot 2: Cobb Angle Phase Diagram
    plt.figure(figsize=(10, 8))
    levels_cobb = np.linspace(0, 90, 31)
    cp2 = plt.contourf(X, Y, pivot_Cobb.values, levels=levels_cobb, cmap='magma', extend='max')
    cbar2 = plt.colorbar(cp2, label='Lateral Cobb Angle (deg)')

    # Overlay R=1 contour for reference
    plt.contour(X, Y, pivot_R.values, levels=[1.0], colors='white', linewidths=1.5, linestyles='--')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Coupling Strength $\chi_\kappa$')
    plt.title('Phase Diagram: Scoliosis Emergence (Lateral Cobb Angle)')

    plt.savefig(fig_dir / 'phase_diagram_energy_deficit_cobb.png', dpi=300)
    plt.close()

    print(f"Saved plots to {fig_dir}")

if __name__ == "__main__":
    run_simulation()
