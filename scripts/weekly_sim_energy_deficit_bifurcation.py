"""
Weekly Simulation: Energy Deficit Bifurcation Phase Diagram.

Investigates the "Energy Deficit Window" in the 2D parameter space of (chi_kappa, L).
Maps the ratio of metabolic demand (P_counter) to proprioceptive supply (S_proprio)
to identify regions of vulnerability (R > 1).

Also computes the emergent Cobb angle to correlate energy deficit with scoliosis onset.

Scaling:
- P_counter scales as L^2 (Isometric growth: A ~ L^2).
- S_proprio scales as L^0.5 (Supply constraint).
"""

import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Ensure src is in python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.countercurvature.pyelastica_bridge import (
    CounterCurvatureRodSystem,
    PYELASTICA_AVAILABLE,
)
from spinalmodes.countercurvature.coupling import CounterCurvatureParams
from spinalmodes.countercurvature.info_fields import InfoField1D

def generate_bimodal_gaussian_field(s, L):
    """
    Generate the bimodal Gaussian information field I(s).
    Formula from manuscript/sections/methods.tex (and experiment_energy_deficit_window.py):
    I(s) = A_c * exp(-((s/L - s_c)^2)/(2*sigma_c^2)) +
           A_l * exp(-((s/L - s_l)^2)/(2*sigma_l^2)) + I_0
    """
    if L <= 0:
        return np.zeros_like(s)

    s_norm = s / L

    # Parameters
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08

    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10

    I_0 = 0.3

    term_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    term_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return term_c + term_l + I_0

def run_experiment():
    output_dir = Path("outputs/thermodynamic_cost")
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = Path("outputs/figures")
    fig_dir.mkdir(parents=True, exist_ok=True)

    print(f"Running Weekly Sim: Energy Deficit Bifurcation -> {output_dir}")

    if not PYELASTICA_AVAILABLE:
        print("Error: PyElastica not found. Cannot run simulation.")
        return

    # Sweep Parameters
    chi_values = np.linspace(0.01, 0.10, 20)
    L_values = np.linspace(0.25, 0.55, 20)

    # Fixed Parameters
    rho = 1100.0
    g = 9.81
    E0 = 1.0e9

    # Isometric Scaling Reference (L_ref=0.5m -> A_ref=0.001 m^2)
    L_ref_iso = 0.5
    A_ref_iso = 0.001
    radius_ref_iso = np.sqrt(A_ref_iso / np.pi)

    # Simulation settings (optimized for speed)
    n_elements = 50
    final_time = 1.0 # Reduced duration for speed
    dt = 2e-4        # Increased time step for speed (quasi-static)
    initial_lateral_defect = 0.03 # Perturbation for symmetry breaking

    results = []

    print(f"{'chi_kappa':<10} | {'L (m)':<6} | {'P_counter':<10} | {'Cobb':<6} | {'Time':<6}")
    print("-" * 55)

    # Pre-calculate baseline for calibration later
    # We store raw P_counter values, then calibrate S0 after the loop.

    for chi in chi_values:
        for L in L_values:
            t0 = time.time()

            # 1. Scaling (Isometric)
            # Radius scales linearly with L to maintain slenderness ratio (geometric similarity)
            # But here we scale Area as L^2, which implies Radius ~ L.
            radius = radius_ref_iso * (L / L_ref_iso)
            A = np.pi * radius**2

            # 2. Info Field
            s = np.linspace(0, L, n_elements + 1)
            I_field = generate_bimodal_gaussian_field(s, L)
            dIds = np.gradient(I_field, s)
            info = InfoField1D(s=s, I=I_field, dIds=dIds)

            # 3. Passive Simulation (chi_kappa = 0)
            # Used as the reference "gravity-only" state
            params_pass = CounterCurvatureParams(
                chi_kappa=0.0, # Passive
                chi_tau=0.0,
                chi_E=0.10,    # Material property (stiffness modulation) remains
                chi_M=0.0,
                scale_length=L
            )

            # Initial defect is geometric, so it applies to both passive and active?
            # Yes, defect is intrinsic.
            kappa_gen = np.zeros((3, n_elements + 1))
            kappa_gen[0, :] = initial_lateral_defect # Lateral

            sys_pass = CounterCurvatureRodSystem.from_iec(
                info=info,
                params=params_pass,
                length=L,
                n_elements=n_elements,
                E0=E0,
                radius=radius,
                rho=rho,
                kappa_gen=kappa_gen, # Apply defect
                gravity=g
            )

            # Run Passive
            res_pass = sys_pass.run_simulation(final_time=final_time, dt=dt, progress_bar=False)

            # Extract Passive Curvature (Sagittal component, index 1)
            # kappa is (time, n_nodes, 3). Take last time step.
            if len(res_pass.kappa) > 0:
                kappa_pass_sagittal = res_pass.kappa[-1, :, 1]
            else:
                kappa_pass_sagittal = np.zeros(n_elements + 1)

            # 4. Active Simulation (Target chi_kappa)
            params_act = CounterCurvatureParams(
                chi_kappa=chi,
                chi_tau=0.0, # No torsion drive in this specific sweep
                chi_E=0.10,
                chi_M=0.0,
                scale_length=L
            )

            sys_act = CounterCurvatureRodSystem.from_iec(
                info=info,
                params=params_act,
                length=L,
                n_elements=n_elements,
                E0=E0,
                radius=radius,
                rho=rho,
                kappa_gen=kappa_gen,
                gravity=g
            )

            res_act = sys_act.run_simulation(final_time=final_time, dt=dt, progress_bar=False)
            metrics_act = res_act.compute_final_metrics()

            # Extract Active Curvature
            if len(res_act.kappa) > 0:
                kappa_act_sagittal = res_act.kappa[-1, :, 1]
            else:
                kappa_act_sagittal = np.zeros(n_elements + 1)

            # 5. Compute P_counter
            # P ~ L^2 * mean((k_act - k_pass)^2)
            # P_counter factor: eta_a * rho * A * g
            # eta_a = 1.0 (from experiment_energy_deficit_window.py)
            # Note: A scales as L^2 here, so P_counter ~ L^2 * L^2 * (1/L^2) ~ L^2.
            eta_a = 1.0
            sq_diff = (kappa_act_sagittal - kappa_pass_sagittal)**2
            mean_sq_diff = np.mean(sq_diff)

            P_counter = eta_a * rho * A * g * (L**2) * mean_sq_diff

            # 6. Compute D_geo (Geodesic Deviation)
            D_geo = L * np.sqrt(mean_sq_diff)

            runtime = time.time() - t0

            results.append({
                "chi_kappa": chi,
                "L": L,
                "P_counter": P_counter,
                "Cobb_angle": metrics_act.get("cobb_angle", 0.0),
                "S_lat": metrics_act.get("S_lat", 0.0),
                "D_geo": D_geo,
                "runtime": runtime
            })

            # Minimal logging to avoid spam
            if (abs(chi - 0.05) < 0.005) and (abs(L - 0.4) < 0.01):
                 print(f"{chi:<10.3f} | {L:<6.3f} | {P_counter:<10.2e} | {metrics_act.get('cobb_angle',0):<6.2f} | {runtime:<6.2f}")

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # 7. Post-Processing: Compute R_deficit
    # Supply: S_proprio = S_0 * (L/L_0)^0.5  (Updated to 0.5 based on memory/hypothesis)
    # L_0 = 0.35 (Pre-adolescent reference)
    # Calibrate S_0 such that R=1 at chi=0.05, L=0.35

    target_chi = 0.05
    target_L = 0.35
    L_0 = 0.35

    # Find closest point
    # Normalize for distance calculation
    chi_norm = (df['chi_kappa'] - df['chi_kappa'].min()) / (df['chi_kappa'].max() - df['chi_kappa'].min())
    L_norm = (df['L'] - df['L'].min()) / (df['L'].max() - df['L'].min())

    target_chi_norm = (target_chi - df['chi_kappa'].min()) / (df['chi_kappa'].max() - df['chi_kappa'].min())
    target_L_norm = (target_L - df['L'].min()) / (df['L'].max() - df['L'].min())

    dist = (chi_norm - target_chi_norm)**2 + (L_norm - target_L_norm)**2
    closest_idx = dist.idxmin()

    ref_row = df.loc[closest_idx]
    S_0 = ref_row['P_counter']
    found_chi = ref_row['chi_kappa']
    found_L = ref_row['L']

    print(f"Calibrated S_0 = {S_0:.4e} at closest point chi={found_chi:.3f}, L={found_L:.3f}")

    # Compute S_proprio and R_deficit
    # Using exponent 0.5
    df['S_proprio'] = S_0 * (df['L'] / L_0)**0.5
    df['R_deficit'] = df['P_counter'] / df['S_proprio']

    # Save Results
    csv_path = output_dir / "phase_diagram_energy_deficit.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved data to {csv_path}")

    # 8. Plotting
    # Pivot for Heatmap
    pivot_R = df.pivot(index='chi_kappa', columns='L', values='R_deficit')
    pivot_Cobb = df.pivot(index='chi_kappa', columns='L', values='Cobb_angle')

    X_L = pivot_R.columns.values
    Y_chi = pivot_R.index.values
    Z_R = pivot_R.values
    Z_Cobb = pivot_Cobb.values

    # Plot 1: Energy Deficit Ratio
    plt.figure(figsize=(10, 8))
    # Filled contour
    cp = plt.contourf(X_L, Y_chi, Z_R, levels=20, cmap='RdYlBu_r') # Red=High Deficit, Blue=Safe
    plt.colorbar(cp, label='Energy Deficit Ratio (R_deficit)')

    # Critical Boundary R=1
    cs = plt.contour(X_L, Y_chi, Z_R, levels=[1.0], colors='k', linewidths=2, linestyles='--')
    plt.clabel(cs, inline=1, fmt='R=1.0', fontsize=12)

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_\kappa$')
    plt.title('Energy Deficit Phase Diagram: Vulnerability Window')

    plt.text(0.3, 0.08, "Safe Region (R < 1)", color='blue', fontweight='bold')
    plt.text(0.45, 0.08, "Deficit Region (R > 1)", color='red', fontweight='bold')

    plt.savefig(fig_dir / "phase_diagram_energy_deficit.png", dpi=150)
    plt.close()

    # Plot 2: Cobb Angle
    plt.figure(figsize=(10, 8))
    cp2 = plt.contourf(X_L, Y_chi, Z_Cobb, levels=20, cmap='viridis')
    plt.colorbar(cp2, label='Cobb Angle (deg)')

    # Overlay R=1 contour for correlation
    cs2 = plt.contour(X_L, Y_chi, Z_R, levels=[1.0], colors='white', linewidths=2, linestyles='--')
    plt.clabel(cs2, inline=1, fmt='R=1.0', fontsize=10)

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_\kappa$')
    plt.title('Emergent Scoliosis Phase Diagram')

    plt.savefig(fig_dir / "phase_diagram_energy_deficit_cobb.png", dpi=150)
    plt.close()

    print("Plots saved.")

if __name__ == "__main__":
    run_experiment()
