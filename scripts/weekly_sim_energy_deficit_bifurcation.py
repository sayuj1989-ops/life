"""
Weekly Simulation: Energy Deficit Bifurcation Phase Diagram

Performs a 2D parameter sweep of the Energy Deficit Window across (chi_kappa, L) space.
Generates a phase diagram showing where AIS vulnerability is highest (R_deficit > 1).

Hypothesis: H_2026_02_08_EnergyPhase
The Energy Deficit Window forms a wedge-shaped instability region.

Outputs:
- outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv
- outputs/figures/phase_diagram_energy_deficit.png
- outputs/figures/phase_diagram_energy_deficit_cobb.png
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Ensure src is in python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.iec import solve_beam_static
from spinalmodes.countercurvature.scoliosis_metrics import (
    build_lateral_curvature_bump,
    compute_scoliosis_metrics
)

def generate_bimodal_gaussian_field(s, L):
    """
    Generate the bimodal Gaussian information field I(s).
    Formula from manuscript/sections/methods.tex:
    I(s) = A_c * exp(-((s/L - s_c)^2)/(2*sigma_c^2)) +
           A_l * exp(-((s/L - s_l)^2)/(2*sigma_l^2)) + I_0
    """
    if L == 0:
        return np.full_like(s, 0.3)

    s_norm = s / L

    # Parameters from prompt/manuscript
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

def compute_lateral_displacement(theta, s):
    """
    Compute lateral (y) and longitudinal (z) coordinates from angle theta.
    Assumes beam starts at (0, 0) and theta is angle with z-axis.

    In the lateral plane (coronal):
    dz = cos(theta) * ds
    dy = sin(theta) * ds
    """
    ds = np.diff(s)
    ds = np.insert(ds, 0, ds[0]) # Approximation for first element or use 0 start

    # Better integration: trapezoidal
    z = np.zeros_like(s)
    y = np.zeros_like(s)

    # Simple cumulative sum for small deflections is fine, but let's be reasonably precise
    # z[i] = sum(cos(theta) * ds)
    # y[i] = sum(sin(theta) * ds)

    # We use cumulative trapezoidal rule if possible, or just cumsum of midpoints
    # For weekly sim speed, cumsum is fine.

    # Midpoint approximation
    # dz_i = cos((theta_i + theta_{i-1})/2) * ds_i

    # Simplified:
    z = np.cumsum(np.cos(theta) * ds)
    y = np.cumsum(np.sin(theta) * ds)

    # Adjust start to 0,0
    z = z - z[0]
    y = y - y[0]

    return y, z

def run_simulation():
    print("Running Weekly Sim: Energy Deficit Bifurcation Phase Diagram...")

    # Output directories
    output_data_dir = Path("outputs/thermodynamic_cost")
    output_fig_dir = Path("outputs/figures")
    output_data_dir.mkdir(parents=True, exist_ok=True)
    output_fig_dir.mkdir(parents=True, exist_ok=True)

    # Sweep Parameters
    chi_kappa_vals = np.linspace(0.01, 0.10, 20)
    L_vals = np.linspace(0.25, 0.55, 20)

    # Fixed Parameters
    rho = 1100.0
    A = 0.001
    g = 9.81
    E0 = 1.0e9 # 1.0 GPa
    I_moment = A**2 / (4 * np.pi) # m^4
    chi_E = 0.10

    # Reference for Calibration
    # We want R_deficit = 1 at (chi_kappa=0.05, L=0.35)
    # So we compute P_counter for this point, and set S_0 = P_counter.
    # Then S_proprio(0.35) = S_0 * 1 = P_counter, so R = 1.
    ref_chi_kappa = 0.05
    ref_L = 0.35

    print("Calibrating S_0 at reference point (chi=0.05, L=0.35)...")

    def compute_p_counter(L, chi_kappa):
        n_nodes = 100
        s = np.linspace(0, L, n_nodes)
        I_field = generate_bimodal_gaussian_field(s, L)
        grad_I = np.gradient(I_field, s)
        E_field = E0 * (1.0 + chi_E * I_field)
        distributed_load = rho * A * g

        # Active
        kappa_target_iec = chi_kappa * grad_I
        theta_iec, kappa_iec = solve_beam_static(
            s=s, kappa_target=kappa_target_iec, E_field=E_field,
            M_active=np.zeros_like(s), I_moment=I_moment,
            P_load=0.0, distributed_load=distributed_load
        )

        # Passive
        kappa_target_pass = np.zeros_like(s)
        theta_pass, kappa_pass = solve_beam_static(
            s=s, kappa_target=kappa_target_pass, E_field=E_field,
            M_active=np.zeros_like(s), I_moment=I_moment,
            P_load=0.0, distributed_load=distributed_load
        )

        # P_counter
        # P ~ L^2 * mean(delta_kappa^2)
        curvature_diff_sq = (kappa_iec - kappa_pass)**2
        mean_diff_sq = np.mean(curvature_diff_sq)
        p_counter = rho * A * g * (L**2) * mean_diff_sq

        # D_geo
        d_geo = np.sqrt(np.mean((theta_iec - theta_pass)**2))

        return p_counter, d_geo, s, I_field

    S_0, _, _, _ = compute_p_counter(ref_L, ref_chi_kappa)
    print(f"Calibration Complete: S_0 = {S_0:.4e} W (normalized)")

    results = []

    print(f"Starting Sweep: {len(chi_kappa_vals)}x{len(L_vals)} = {len(chi_kappa_vals)*len(L_vals)} points")

    for chi_k in chi_kappa_vals:
        for L in L_vals:
            # 1. Compute P_counter (Sagittal)
            p_counter, d_geo, s, I_field = compute_p_counter(L, chi_k)

            # 2. Compute Supply and Deficit
            s_proprio = S_0 * (L / 0.35)**0.7
            r_deficit = p_counter / s_proprio

            # 3. Lateral Instability Simulation
            # E_lat drops if R_deficit > 1
            stiffness_scale = 1.0 / max(1.0, r_deficit)
            E_lat_field = E0 * stiffness_scale * (1.0 + chi_E * I_field)

            # Lateral perturbation
            epsilon_asym = 0.03
            kappa_target_lat = build_lateral_curvature_bump(s, epsilon_lat=epsilon_asym)

            # Solve Lateral Beam (No gravity load, just perturbation)
            # We assume lateral plane is orthogonal to gravity, so distributed_load=0
            # Unless we model the "falling over" effect, but beam theory usually handles this via P_load if needed.
            # Here we just check stiffness vs curvature perturbation.
            # However, if R_deficit is high, stiffness is low, so the same kappa_target might result in large theta?
            # Wait, kappa_target is the REST curvature. If we apply kappa_target, the beam tries to curve.
            # If stiffness is low, it curves EASIER? No.
            # In the beam equation: EI * (kappa - kappa_target) = M_ext.
            # If M_ext = 0 (no load), then kappa = kappa_target. Stiffness cancels out!
            # So just reducing stiffness won't change the shape if there is no load.
            # We need a LOAD to see the effect of stiffness reduction.
            # The prompt says: "A lateral load (w_lat) is included to ensure this softening results in Cobb angle amplification."
            # So I must add a lateral distributed load.
            # Let's say w_lat = 0.1 * rho * A * g (10% of weight acting laterally due to slight tilt?)
            w_lat = 0.1 * rho * A * g

            theta_lat, kappa_lat = solve_beam_static(
                s=s,
                kappa_target=kappa_target_lat, # The perturbation seeds the shape
                E_field=E_lat_field,
                M_active=np.zeros_like(s),
                I_moment=I_moment,
                P_load=0.0,
                distributed_load=w_lat # The load amplifies it if stiffness is low
            )

            # Compute Cobb
            y_lat, z_lat = compute_lateral_displacement(theta_lat, s)
            metrics = compute_scoliosis_metrics(z=z_lat, y=y_lat)
            cobb = metrics.cobb_like_deg

            results.append({
                "chi_kappa": chi_k,
                "L": L,
                "P_counter": p_counter,
                "S_proprio": s_proprio,
                "R_deficit": r_deficit,
                "Cobb_angle": cobb,
                "D_geo": d_geo,
                "In_Deficit": r_deficit > 1.0
            })

    # Save Results
    df = pd.DataFrame(results)
    csv_path = output_data_dir / "phase_diagram_energy_deficit.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved sweep data to {csv_path}")

    # Plotting
    # 1. R_deficit Heatmap
    pivot_R = df.pivot(index="chi_kappa", columns="L", values="R_deficit")

    plt.figure(figsize=(10, 8))
    # Using imshow correctly with extent
    extent = [L_vals[0], L_vals[-1], chi_kappa_vals[0], chi_kappa_vals[-1]]
    plt.imshow(pivot_R, origin='lower', extent=extent, aspect='auto', cmap='viridis')
    plt.colorbar(label='Energy Deficit Ratio (R_deficit)')

    # Contour at R=1
    # We need meshgrid for contour
    X, Y = np.meshgrid(L_vals, chi_kappa_vals)
    # pivot_R is (n_chi, n_L), perfect for contour(X, Y, Z)
    CS = plt.contour(X, Y, pivot_R, levels=[1.0], colors='red', linewidths=2)
    plt.clabel(CS, inline=True, fontsize=10, fmt='R=1')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'IEC Coupling Strength $\chi_\kappa$')
    plt.title('Phase Diagram: Energy Deficit Window')

    fig_path_R = output_fig_dir / "phase_diagram_energy_deficit.png"
    plt.savefig(fig_path_R, dpi=300)
    plt.close()

    # 2. Cobb Angle Heatmap
    pivot_Cobb = df.pivot(index="chi_kappa", columns="L", values="Cobb_angle")

    plt.figure(figsize=(10, 8))
    plt.imshow(pivot_Cobb, origin='lower', extent=extent, aspect='auto', cmap='plasma')
    plt.colorbar(label='Cobb Angle (degrees)')

    # Overlay R=1 contour for reference
    CS = plt.contour(X, Y, pivot_R, levels=[1.0], colors='white', linestyles='dashed', linewidths=1)

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'IEC Coupling Strength $\chi_\kappa$')
    plt.title('Phase Diagram: Emergent Scoliosis (Cobb Angle)')

    fig_path_Cobb = output_fig_dir / "phase_diagram_energy_deficit_cobb.png"
    plt.savefig(fig_path_Cobb, dpi=300)
    plt.close()

    print(f"Saved figures to {fig_path_R} and {fig_path_Cobb}")

if __name__ == "__main__":
    run_simulation()
