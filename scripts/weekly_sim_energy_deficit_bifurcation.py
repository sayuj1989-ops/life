#!/usr/bin/env python3
"""
Weekly Simulation: Energy Deficit Bifurcation.

Performs a 2D parameter sweep of the Energy Deficit Window across (χ_κ, L) space,
generating a phase diagram showing where AIS vulnerability is highest.

Hypothesis ID: H_2026_02_08_EnergyPhase
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from spinalmodes.iec import solve_beam_static, compute_amplitude

# Constants
RHO = 1100.0  # kg/m^3
G_GRAVITY = 9.81  # m/s^2
E0 = 1.0e9    # Pa (1.0 GPa)
A_VAL = 0.001 # m^2 (Fixed as per prompt)

# Information Field Parameters (Bimodal Gaussian)
# I(s) = A_c exp(...) + A_l exp(...) + I_0
A_C = 0.5
S_C_REL = 0.80
SIGMA_C_REL = 0.08
A_L = 0.7
S_L_REL = 0.25
SIGMA_L_REL = 0.10
I_0 = 0.3

# Supply Calibration
# S_proprio = S_0 * (L/L_0)^0.7
# Using values from previous script context as defaults since prompt didn't specify S_0, L_0
L_0_SUPPLY = 0.353
S_0_SUPPLY = 0.0867

def generate_bimodal_I(s, L):
    """Generate bimodal Gaussian information field I(s)."""
    s_norm = s / L

    term_c = A_C * np.exp(-((s_norm - S_C_REL)**2) / (2 * SIGMA_C_REL**2))
    term_l = A_L * np.exp(-((s_norm - S_L_REL)**2) / (2 * SIGMA_L_REL**2))

    return term_c + term_l + I_0

def run_simulation():
    # Prepare output directory
    output_dir = Path("outputs/thermodynamic_cost")
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = Path("outputs/figures")
    figure_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "phase_diagram_energy_deficit.csv"

    # Check if data already exists to avoid duplication
    if csv_path.exists():
        print(f"Loading existing data from {csv_path}...")
        df = pd.read_csv(csv_path)
    else:
        # Parameter Sweep
        # χ_κ: 0.01 to 0.10 in 20 steps
        chi_kappa_values = np.linspace(0.01, 0.10, 20)
        # L: 0.25 to 0.55 m in 20 steps
        L_values = np.linspace(0.25, 0.55, 20)

        results = []

        print(f"Starting 2D sweep: {len(chi_kappa_values)}x{len(L_values)} = {len(chi_kappa_values)*len(L_values)} points")

        for chi_kappa in chi_kappa_values:
            for L in L_values:
                # Derived geometric props
                I_moment = (A_VAL**2) / (4 * np.pi)  # m^4 (cylindrical approx)

                # Distributed load (Gravity acting transversely in 1D beam model approximation)
                distributed_load = RHO * A_VAL * G_GRAVITY  # N/m

                # Spatial grid
                s = np.linspace(0, L, 100)

                # --- 1. Compute P_counter (Sagittal) ---

                # Generate Information Field
                I_field = generate_bimodal_I(s, L)
                grad_I = np.gradient(I_field, s)

                # Active Curvature (Sagittal)
                kappa_target_active = 0.0 + chi_kappa * grad_I

                # Passive Curvature (Gravity Only, chi_kappa=0)
                kappa_target_passive = np.zeros_like(s)

                # Constant E field (chi_E = 0 for this sweep)
                E_field = np.full_like(s, E0)
                M_active = np.zeros_like(s) # chi_f = 0

                # Solve Active
                theta_active, kappa_active = solve_beam_static(
                    s=s,
                    kappa_target=kappa_target_active,
                    E_field=E_field,
                    M_active=M_active,
                    I_moment=I_moment,
                    P_load=0.0,
                    distributed_load=distributed_load
                )

                # Solve Passive
                theta_passive, kappa_passive = solve_beam_static(
                    s=s,
                    kappa_target=kappa_target_passive,
                    E_field=E_field,
                    M_active=M_active,
                    I_moment=I_moment,
                    P_load=0.0,
                    distributed_load=distributed_load
                )

                # Compute P_counter
                # P_counter ~ eta_a * rho * A * g * L^2 * <|kappa_active - kappa_passive|^2>
                # Assuming eta_a = 1.0
                mse_kappa = np.mean((kappa_active - kappa_passive)**2)
                P_counter = 1.0 * RHO * A_VAL * G_GRAVITY * (L**2) * mse_kappa

                # D_geo
                d_geo = np.sqrt(mse_kappa)

                # --- 2. Compute Cobb Angle (Lateral) ---

                # Lateral Asymmetry Perturbation (ε_asym = 0.03)
                epsilon_asym = 0.03
                kappa_target_lat = np.full_like(s, epsilon_asym)

                # Solve Lateral (assuming same mechanics, orthogonal plane)
                theta_lat, kappa_lat = solve_beam_static(
                    s=s,
                    kappa_target=kappa_target_lat,
                    E_field=E_field,
                    M_active=M_active,
                    I_moment=I_moment,
                    P_load=0.0,
                    distributed_load=distributed_load
                )

                cobb_angle = compute_amplitude(theta_lat)

                # --- 3. Compute R_deficit ---
                S_proprio = S_0_SUPPLY * (L / L_0_SUPPLY)**0.7
                R_deficit = P_counter / S_proprio
                in_deficit = R_deficit > 1.0

                results.append({
                    "chi_kappa": chi_kappa,
                    "L": L,
                    "P_counter": P_counter,
                    "Cobb_angle": cobb_angle,
                    "D_geo": d_geo,
                    "S_proprio": S_proprio,
                    "R_deficit": R_deficit,
                    "In_Deficit": in_deficit
                })

        # Convert to DataFrame
        df = pd.DataFrame(results)

        # Save CSV
        df.to_csv(csv_path, index=False)
        print(f"Saved results to {csv_path}")

    # Generate Plots
    generate_plots(df, figure_dir)

def generate_plots(df, figure_dir):
    # Pivot data for heatmap
    pivot_R = df.pivot(index="chi_kappa", columns="L", values="R_deficit")
    pivot_Cobb = df.pivot(index="chi_kappa", columns="L", values="Cobb_angle")

    X = pivot_R.columns.values
    Y = pivot_R.index.values

    # 1. R_deficit Heatmap
    plt.figure(figsize=(10, 8))
    # Use meshgrid for contourf
    X_grid, Y_grid = np.meshgrid(X, Y)

    plt.contourf(X_grid, Y_grid, pivot_R.values, levels=20, cmap="RdYlBu_r")
    plt.colorbar(label="Energy Deficit Ratio $R_{deficit}$")

    # Contour line at R=1.0
    cs = plt.contour(X_grid, Y_grid, pivot_R.values, levels=[1.0], colors='k', linewidths=2, linestyles='--')
    plt.clabel(cs, inline=1, fontsize=10, fmt='R=1.0')

    plt.title("Energy Deficit Phase Diagram")
    plt.xlabel("Spinal Length L (m)")
    plt.ylabel(r"Coupling Strength $\chi_\kappa$")
    plt.grid(True, alpha=0.3)

    plt.savefig(figure_dir / "phase_diagram_energy_deficit.png", dpi=300)
    plt.close()
    print(f"Saved plot to {figure_dir / 'phase_diagram_energy_deficit.png'}")

    # 2. Cobb Angle Heatmap
    plt.figure(figsize=(10, 8))
    plt.contourf(X_grid, Y_grid, pivot_Cobb.values, levels=20, cmap="viridis")
    plt.colorbar(label="Cobb Angle (degrees)")

    plt.title("Lateral Instability (Cobb Angle)")
    plt.xlabel("Spinal Length L (m)")
    plt.ylabel(r"Coupling Strength $\chi_\kappa$")
    plt.grid(True, alpha=0.3)

    plt.savefig(figure_dir / "phase_diagram_energy_deficit_cobb.png", dpi=300)
    plt.close()
    print(f"Saved plot to {figure_dir / 'phase_diagram_energy_deficit_cobb.png'}")

if __name__ == "__main__":
    run_simulation()
