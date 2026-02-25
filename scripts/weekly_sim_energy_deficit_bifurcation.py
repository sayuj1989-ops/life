#!/usr/bin/env python3
"""
Weekly Simulation: Energy Deficit Bifurcation Phase Diagram.

Performs a 2D parameter sweep of the Energy Deficit Window across (chi_kappa, L) space.
Generates a phase diagram showing where AIS vulnerability is highest.

Hypothesis ID: H_2026_02_08_EnergyPhase
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure src is in path to import spinalmodes
script_dir = Path(__file__).parent.resolve()
src_dir = script_dir.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    print("Error: Could not import spinalmodes.iec. Check PYTHONPATH.")
    sys.exit(1)

def gaussian(s_norm, A, center, width):
    """Compute Gaussian function."""
    return A * np.exp(-((s_norm - center)**2) / (2 * width**2))

def gaussian_grad(s_norm, A, center, width, L):
    """
    Compute spatial gradient of Gaussian function d/ds.
    """
    term = -(s_norm - center) / (width**2)
    val = gaussian(s_norm, A, center, width)
    return val * term / L

def run_experiment():
    print("Starting Energy Deficit Window 2D Sweep...")

    # Ensure output directories exist
    Path("outputs/thermodynamic_cost").mkdir(parents=True, exist_ok=True)
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)

    # 1. Parameter Sweep Definition
    n_steps = 20
    chi_kappa_vals = np.linspace(0.01, 0.10, n_steps)
    L_vals = np.linspace(0.25, 0.55, n_steps)

    # Fixed Parameters
    rho = 1100.0
    A = 0.001 # Fixed Area (m^2)
    g = 9.81
    E0 = 1.0e9 # 1.0 GPa
    eta_a = 1.0 # Metabolic efficiency factor

    # Perturbation
    epsilon_asym = 0.03

    # Information field parameters (Bimodal Gaussian)
    # Cervical
    A_c = 0.5; s_c = 0.80; sigma_c = 0.08
    # Lumbar
    A_l = 0.7; s_l = 0.25; sigma_l = 0.10

    # Reference for Supply
    L0 = 0.35
    chi_kappa_ref = 0.05

    # Prepare I_moment (Fixed A means Fixed I_moment)
    # Circular approx: I = A^2 / (4*pi)
    I_moment = (A**2) / (4 * np.pi)

    # Distributed load q = rho * A * g
    q = rho * A * g
    P_load = 0.0

    def simulate(L, chi_kappa):
        """
        Simulate beam mechanics.
        Returns:
            P_counter: Metabolic cost of maintaining sagittal profile (J/s)
            cobb_baseline: Cobb angle from purely elastic lateral perturbation (degrees)
            D_geo: Geodesic deviation metric (m)
        """
        n_nodes = 100
        s = np.linspace(0, L, n_nodes)
        s_norm = s / L

        # --- 1. Sagittal Plane (Metabolic Cost) ---
        # Driven by Information Field Gradient
        grad_I_c = gaussian_grad(s_norm, A_c, s_c, sigma_c, L)
        grad_I_l = gaussian_grad(s_norm, A_l, s_l, sigma_l, L)
        grad_I = grad_I_c + grad_I_l

        # Target curvature (Sagittal)
        kappa_sag_target = chi_kappa * grad_I

        # Beam Properties
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s) # chi_f = 0

        # Solve Active (IEC) Sagittal
        theta_sag_IEC, kappa_sag_IEC = solve_beam_static(
            s, kappa_sag_target, E_field, M_active,
            I_moment=I_moment, P_load=P_load, distributed_load=q
        )

        # Solve Passive Sagittal (Gravity only, target=0)
        theta_sag_passive, kappa_sag_passive = solve_beam_static(
            s, np.zeros_like(s), E_field, M_active,
            I_moment=I_moment, P_load=P_load, distributed_load=q
        )

        # Compute Cost P_counter
        # Cost is proportional to difference between Active and Passive curvature states
        kappa_diff_sq = (kappa_sag_IEC - kappa_sag_passive)**2
        mean_kappa_diff_sq = np.mean(kappa_diff_sq)

        P_counter = eta_a * rho * A * g * (L**2) * mean_kappa_diff_sq
        D_geo = np.sqrt(mean_kappa_diff_sq) * L

        # --- 2. Lateral Plane (Instability Probe) ---
        # Driven by Perturbation only
        # We assume isotropic material properties for simplicity
        kappa_lat_target = np.full_like(s, epsilon_asym)

        # Solve Lateral Elastic Response
        theta_lat, kappa_lat = solve_beam_static(
            s, kappa_lat_target, E_field, M_active,
            I_moment=I_moment, P_load=P_load, distributed_load=q
        )

        # Calculate Baseline Cobb Angle (Elastic Response)
        cobb_baseline = np.degrees(np.max(theta_lat) - np.min(theta_lat))

        return P_counter, cobb_baseline, D_geo

    # Pre-calculate S0 (Reference P_counter)
    # We need to run one simulation at L0, chi_kappa_ref to get S0
    print(f"Calculating reference supply S0 at L={L0}, chi_kappa={chi_kappa_ref}...")
    S0, _, _ = simulate(L0, chi_kappa_ref)
    print(f"Reference S0 = {S0:.6f}")

    results = []

    # Run Sweep
    total_steps = len(L_vals) * len(chi_kappa_vals)
    step = 0
    print(f"Running sweep ({total_steps} steps)...")

    for L in L_vals:
        for chi_kappa in chi_kappa_vals:
            step += 1
            if step % 50 == 0:
                print(f"  Step {step}/{total_steps}")

            P_counter, cobb_base, D_geo = simulate(L, chi_kappa)

            # S_proprio
            # Supply scales as (L/L0)^0.7
            S_proprio = S0 * ((L / L0)**0.7)
            R_deficit = P_counter / S_proprio

            # Calculate Final Cobb Angle with Instability Amplification
            # If R_deficit > 1, the gain control fails, amplifying the perturbation.
            # We model this phenomenologically as a multiplier.
            amplification = 1.0
            if R_deficit > 1.0:
                # Linear amplification beyond threshold
                amplification = 1.0 + 5.0 * (R_deficit - 1.0)

            cobb_final = cobb_base * amplification

            results.append({
                "chi_kappa": chi_kappa,
                "L": L,
                "P_counter": P_counter,
                "Cobb_baseline": cobb_base,
                "Cobb_angle": cobb_final, # Use the amplified one for plotting
                "D_geo": D_geo,
                "S_proprio": S_proprio,
                "R_deficit": R_deficit
            })

    df = pd.DataFrame(results)

    # Save CSV
    out_dir = Path("outputs/thermodynamic_cost")
    csv_path = out_dir / "phase_diagram_energy_deficit.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

    # Generate Heatmaps
    fig_dir = Path("outputs/figures")

    # Pivot for heatmap
    pivot_R = df.pivot(index="chi_kappa", columns="L", values="R_deficit")
    pivot_Cobb = df.pivot(index="chi_kappa", columns="L", values="Cobb_angle")

    # Prepare Meshgrid
    X, Y = np.meshgrid(L_vals, chi_kappa_vals)

    # Plot R_deficit
    plt.figure(figsize=(10, 8))
    Z_R = pivot_R.values

    # Use RdYlBu_r (Red is high, Blue is low). High R_deficit is bad (Red).
    pcm = plt.pcolormesh(X, Y, Z_R, shading='auto', cmap='RdYlBu_r')
    plt.colorbar(pcm, label='R_deficit (P_counter / S_proprio)')

    # Add contour for R=1 (Energy Deficit Boundary)
    CS = plt.contour(X, Y, Z_R, levels=[1.0], colors='k', linewidths=2)
    plt.clabel(CS, inline=1, fontsize=10, fmt='R=1.0')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'IEC Coupling $\chi_\kappa$')
    plt.title('Energy Deficit Phase Diagram: Instability Region')

    fig_path = fig_dir / "phase_diagram_energy_deficit.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved Figure to {fig_path}")

    # Plot Cobb Angle
    plt.figure(figsize=(10, 8))
    Z_Cobb = pivot_Cobb.values
    # Viridis: Yellow is high Cobb, Purple is low
    pcm_cobb = plt.pcolormesh(X, Y, Z_Cobb, shading='auto', cmap='viridis')
    plt.colorbar(pcm_cobb, label='Cobb Angle (degrees)')

    # Add contour for Cobb=10 (Scoliosis threshold)
    CS_cobb = plt.contour(X, Y, Z_Cobb, levels=[10.0], colors='r', linestyles='dashed', linewidths=2)
    plt.clabel(CS_cobb, inline=1, fontsize=10, fmt='10 deg')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'IEC Coupling $\chi_\kappa$')
    plt.title('Scoliosis Emergence: Cobb Angle Phase Diagram')

    fig_path_cobb = fig_dir / "phase_diagram_energy_deficit_cobb.png"
    plt.savefig(fig_path_cobb, dpi=300)
    plt.close()
    print(f"Saved Figure to {fig_path_cobb}")

if __name__ == "__main__":
    run_experiment()
