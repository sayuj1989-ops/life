#!/usr/bin/env python3
"""
Weekly Simulation: Energy Deficit Bifurcation (2D Phase Diagram).

Performs a 2D parameter sweep of the Energy Deficit Window across (χ_κ, L) space.
Generates a phase diagram showing where AIS vulnerability is highest (Energy Deficit > Supply).

Hypothesis ID: H_2026_02_08_EnergyPhase
Solver: spinalmodes.iec.solve_beam_static (Fast Static Equilibrium)
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Ensure src is in path to import spinalmodes
sys.path.append("src")

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    # Fallback if running from a different directory structure
    sys.path.append(str(Path(__file__).parent.parent / "src"))
    from spinalmodes.iec import solve_beam_static

# --- Parameters ---
E0 = 1.0e9  # Pa (1.0 GPa)
rho = 1100.0  # kg/m^3
g = 9.81  # m/s^2

# Isometric Growth: A ~ L^2
# Reference: A=0.001 m^2 at L=0.4m
A_ref = 0.001
L_ref = 0.4
eta_a = 1.0

# Information field parameters (Bimodal Gaussian)
# Cervical
A_c = 0.5; s_c = 0.80; sigma_c = 0.08
# Lumbar
A_l = 0.7; s_l = 0.25; sigma_l = 0.10
I_0 = 0.3 # Baseline

def gaussian(s_norm, A, center, width):
    """Compute Gaussian function."""
    return A * np.exp(-((s_norm - center)**2) / (2 * width**2))

def gaussian_grad(s_norm, A, center, width, L):
    """
    Compute spatial gradient of Gaussian function d/ds.
    I(s) = A * exp(-(s/L - c)^2 / 2w^2)
    dI/ds = A * exp(...) * -(s/L - c)/w^2 * (1/L)
    """
    term = -(s_norm - center) / (width**2)
    val = gaussian(s_norm, A, center, width)
    return val * term / L

def get_bimodal_field_gradient(s, L):
    """
    Compute total gradient of bimodal information field.
    I(s) = I_c(s) + I_l(s) + I_0
    Returns: grad_I (array)
    """
    s_norm = s / L
    grad_I_c = gaussian_grad(s_norm, A_c, s_c, sigma_c, L)
    grad_I_l = gaussian_grad(s_norm, A_l, s_l, sigma_l, L)
    return grad_I_c + grad_I_l

def solve_system(L, chi_kappa):
    """
    Solves the system for a given L and chi_kappa.
    Returns: P_counter, Cobb_angle
    """
    # Isometric Growth: A scales with L^2
    A_cross = A_ref * (L / L_ref)**2

    # Moment of Inertia (Circular approx)
    I_moment = (A_cross**2) / (4 * np.pi)

    # Spatial grid
    n_nodes = 100
    s = np.linspace(0, L, n_nodes)

    # 1. Compute Gradient
    grad_I = get_bimodal_field_gradient(s, L)

    # 2. Loads
    q = rho * A_cross * g
    P_load = 0.0

    # 3. Beam Properties
    E_field = np.full_like(s, E0)
    M_active = np.zeros_like(s)

    # 4. IEC Equilibrium (Active)
    kappa_target_IEC = chi_kappa * grad_I
    theta_IEC, kappa_IEC = solve_beam_static(
        s, kappa_target_IEC, E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # 5. Passive Equilibrium (Gravity only)
    kappa_target_passive = np.zeros_like(s)
    theta_passive, kappa_passive = solve_beam_static(
        s, kappa_target_passive, E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # 6. Thermodynamic Cost
    # P_counter ~ eta_a * rho * A * g * L^2 * <|kappa_IEC - kappa_passive|^2>
    kappa_diff_sq = (kappa_IEC - kappa_passive)**2
    mean_kappa_diff_sq = np.mean(kappa_diff_sq)
    P_counter = eta_a * rho * A_cross * g * (L**2) * mean_kappa_diff_sq

    # 7. Cobb Angle
    cobb_angle = np.degrees(np.max(theta_IEC) - np.min(theta_IEC))

    return P_counter, cobb_angle

def run_sweep():
    print("Starting 2D Energy Deficit Bifurcation Sweep...")

    output_dir = Path("outputs/thermodynamic_cost")
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = Path("outputs/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Parameter Ranges
    # L from 0.15m to 0.85m (covering pre-adolescent to adult)
    L_vals = np.linspace(0.15, 0.85, 30)

    # chi_kappa from 0.0 to 0.15 (covering healthy to pathological)
    chi_vals = np.linspace(0.0, 0.15, 30)

    # Reference Supply Calibration
    # Calibrate Supply S(L) based on a "Healthy/Reference" trajectory
    # Reference condition: L=0.35m, chi_kappa=0.05
    L_calib = 0.35
    chi_calib = 0.05
    P_calib, _ = solve_system(L_calib, chi_calib)
    S0 = P_calib
    print(f"Calibrated Supply S0 = {S0:.6f} at L={L_calib}m, chi={chi_calib}")

    results = []

    for chi in chi_vals:
        for L in L_vals:
            P_counter, cobb = solve_system(L, chi)

            # Supply Model: S(L) = S0 * (L / L_calib)^1.0
            # Assuming linear scaling of proprioceptive supply capacity with length
            S_proprio = S0 * (L / L_calib)**1.0

            R_deficit = P_counter / S_proprio if S_proprio > 1e-9 else 0.0

            results.append({
                "chi_kappa": chi,
                "L": L,
                "P_counter": P_counter,
                "S_proprio": S_proprio,
                "R_deficit": R_deficit,
                "Cobb_angle": cobb
            })

    df = pd.DataFrame(results)
    csv_path = output_dir / "phase_diagram_energy_deficit.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved sweep data to {csv_path}")

    # Generate Heatmaps
    generate_heatmaps(df, figures_dir)

def generate_heatmaps(df, output_dir):
    pivot_R = df.pivot(index="chi_kappa", columns="L", values="R_deficit")
    pivot_Cobb = df.pivot(index="chi_kappa", columns="L", values="Cobb_angle")

    # Ensure sorted axes
    pivot_R = pivot_R.sort_index(axis=0).sort_index(axis=1)
    chi_axis = pivot_R.index
    L_axis = pivot_R.columns
    X, Y = np.meshgrid(L_axis, chi_axis)

    # Plot 1: Energy Deficit Ratio
    plt.figure(figsize=(10, 8))
    # RdYlBu_r: Red (High Deficit), Blue (Low Deficit)
    cp = plt.contourf(X, Y, pivot_R.values, levels=20, cmap='RdYlBu_r')
    cbar = plt.colorbar(cp)
    cbar.set_label(r'Energy Deficit Ratio $R_{deficit} = P_{counter}/S_{proprio}$')

    # Contour at R=1 (Bifurcation Boundary)
    if pivot_R.values.min() < 1.0 < pivot_R.values.max():
        cs = plt.contour(X, Y, pivot_R.values, levels=[1.0], colors='k', linewidths=2, linestyles='--')
        plt.clabel(cs, fmt='R=1.0', inline=True, fontsize=10)

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_\kappa$')
    plt.title('Phase Diagram: Energy Deficit Bifurcation')
    plt.savefig(output_dir / "phase_diagram_energy_deficit.png", dpi=150)
    plt.close()

    # Plot 2: Cobb Angle
    plt.figure(figsize=(10, 8))
    cp2 = plt.contourf(X, Y, pivot_Cobb.values, levels=20, cmap='viridis')
    cbar2 = plt.colorbar(cp2)
    cbar2.set_label('Cobb Angle (degrees)')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_\kappa$')
    plt.title('Phase Diagram: Cobb Angle Severity')
    plt.savefig(output_dir / "phase_diagram_cobb.png", dpi=150)
    plt.close()
    print("Saved heatmaps to outputs/figures/")

if __name__ == "__main__":
    run_sweep()
