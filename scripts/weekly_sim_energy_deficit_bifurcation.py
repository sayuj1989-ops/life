#!/usr/bin/env python3
"""
Weekly Simulation: Energy Deficit Bifurcation (2D Phase Diagram).
# Executed for H_2026_02_08_EnergyPhase

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
    from spinalmodes.countercurvature.api import (
        geodesic_curvature_deviation,
        InfoField1D,
        compute_countercurvature_metric
    )
except ImportError:
    # Fallback if running from a different directory structure
    sys.path.append(str(Path(__file__).parent.parent / "src"))
    from spinalmodes.iec import solve_beam_static
    from spinalmodes.countercurvature.api import (
        geodesic_curvature_deviation,
        InfoField1D,
        compute_countercurvature_metric
    )

# --- Parameters ---
# Fixed parameters
E0 = 1.0e9  # Pa (1.0 GPa)
rho = 1100.0  # kg/m^3
g = 9.81  # m/s^2
A_cross = 0.001 # m^2 (Fixed as per instructions)
eta_a = 1.0

# Information field parameters (Bimodal Gaussian)
# Cervical
A_c = 0.5; s_c = 0.80; sigma_c = 0.08
# Lumbar
A_l = 0.7; s_l = 0.25; sigma_l = 0.10
I_0 = 0.3 # Baseline

# Lateral Perturbation
epsilon_asym = 0.03 # 3% lateral curvature defect

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

def get_bimodal_field(s, L):
    """
    Compute bimodal information field I(s).
    """
    s_norm = s / L
    I_c = gaussian(s_norm, A_c, s_c, sigma_c)
    I_l = gaussian(s_norm, A_l, s_l, sigma_l)
    return I_c + I_l + I_0

def solve_system(L, chi_kappa, S0, L_calib):
    """
    Solves the system for a given L and chi_kappa.
    Returns dict of metrics.
    """
    # Moment of Inertia (Circular approx)
    I_moment = (A_cross**2) / (4 * np.pi)

    # Spatial grid
    n_nodes = 100
    s = np.linspace(0, L, n_nodes)

    # 1. Construct InfoField
    I_vals = get_bimodal_field(s, L)
    grad_I = get_bimodal_field_gradient(s, L)

    # Need to create InfoField object for api calls
    # Note: InfoField1D expects dIds
    info_field = InfoField1D(s=s, I=I_vals, dIds=grad_I)

    # 2. Compute g_eff
    g_eff = compute_countercurvature_metric(info_field)

    # 3. Loads
    q = rho * A_cross * g
    P_load = 0.0

    # 4. Beam Properties
    E_field = np.full_like(s, E0)
    M_active = np.zeros_like(s) # We use kappa_target instead of M_active for IEC-1

    # --- Sagittal Solve (Counter-Curvature) ---
    # kappa_target = chi_kappa * grad_I
    kappa_target_sag = chi_kappa * grad_I
    theta_sag, kappa_sag = solve_beam_static(
        s, kappa_target_sag, E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # Passive Equilibrium (Gravity only)
    theta_passive, kappa_passive = solve_beam_static(
        s, np.zeros_like(s), E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # 5. Thermodynamic Cost P_counter
    # P_counter ~ eta_a * rho * A * g * L^2 * <|kappa_IEC - kappa_passive|^2>
    kappa_diff_sq = (kappa_sag - kappa_passive)**2
    mean_kappa_diff_sq = np.mean(kappa_diff_sq)
    P_counter = eta_a * rho * A_cross * g * (L**2) * mean_kappa_diff_sq

    # 6. Supply and R_deficit
    # S(L) = S0 * (L / L_calib)^0.7
    if L_calib > 0:
        S_proprio = S0 * (L / L_calib)**0.7
    else:
        S_proprio = S0

    R_deficit = P_counter / S_proprio if S_proprio > 1e-12 else 0.0

    # 7. Geodesic Deviation D_geo
    d_geo_res = geodesic_curvature_deviation(s, kappa_passive, kappa_sag, g_eff)
    D_geo = d_geo_res["D_geo"]

    # --- Lateral Solve (Cobb Angle) ---
    # Perturbation: constant lateral curvature bias or mode shape
    # We use a constant bias for simplicity as "asymmetry perturbation"
    kappa_target_lat = np.full_like(s, epsilon_asym)

    # Elastic Lateral Solve
    theta_lat, kappa_lat = solve_beam_static(
        s, kappa_target_lat, E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # Calculate Cobb (Elastic)
    # Cobb is max difference in angle (radians -> degrees)
    # Usually sum of max tilts. Here theta is absolute angle.
    # Cobb approx = range of theta
    cobb_elastic = np.degrees(np.max(theta_lat) - np.min(theta_lat))

    # Instability Model for Cobb
    # If R_deficit > 1, the "gain" of the error correction loop flips or fails.
    # We model this as an amplification factor.
    # Gain G = 1 / (1 - R) is standard for feedback limit.
    # We clamp R to avoid division by zero and limit amplification.

    if R_deficit >= 1.0:
        amplification = 10.0 # High value for instability
    else:
        amplification = 1.0 / max(0.1, 1.0 - R_deficit)

    cobb_final = cobb_elastic * amplification

    # Clamp to physical limits (e.g. 90 degrees)
    cobb_final = min(cobb_final, 90.0)

    return {
        "P_counter": P_counter,
        "S_proprio": S_proprio,
        "R_deficit": R_deficit,
        "D_geo": D_geo,
        "Cobb_elastic": cobb_elastic,
        "Cobb_angle": cobb_final
    }

def calibrate_supply():
    """
    Calibrate Supply S0 such that R=1 at a reference point.
    Reference: L=0.35m, chi_kappa=0.04 (Healthy-ish/At-Risk boundary)
    """
    L_ref = 0.35
    chi_ref = 0.04

    # Temporary solve to get P_counter at reference
    # Pass dummy S0, L_calib
    res = solve_system(L_ref, chi_ref, S0=1.0, L_calib=1.0)
    P_ref = res["P_counter"]

    print(f"Calibration: P_counter={P_ref:.6e} at L={L_ref}, chi={chi_ref}")
    return P_ref, L_ref

def run_sweep():
    print("Starting 2D Energy Deficit Bifurcation Sweep...")

    output_dir = Path("outputs/thermodynamic_cost")
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = Path("outputs/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Parameter Ranges
    # chi_kappa: 0.01 to 0.10 in 20 steps
    chi_vals = np.linspace(0.01, 0.10, 20)

    # L: 0.25 to 0.55 m in 20 steps
    L_vals = np.linspace(0.25, 0.55, 20)

    # Calibrate Supply
    S0, L_calib = calibrate_supply()
    print(f"Calibrated Supply S0 = {S0:.6e} at L={L_calib}m")

    results = []

    for chi in chi_vals:
        for L in L_vals:
            metrics = solve_system(L, chi, S0, L_calib)

            entry = {
                "chi_kappa": chi,
                "L": L
            }
            entry.update(metrics)
            results.append(entry)

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
    # Use log scale or levels centered around 1? Linear is fine.
    # Set levels to highlight R=1
    levels = np.linspace(0, max(2.0, pivot_R.values.max()), 21)
    cp = plt.contourf(X, Y, pivot_R.values, levels=levels, cmap='RdYlBu_r')
    cbar = plt.colorbar(cp)
    cbar.set_label(r'Energy Deficit Ratio $R_{deficit} = P_{counter}/S_{proprio}$')

    # Contour at R=1 (Bifurcation Boundary)
    if pivot_R.values.min() < 1.0 < pivot_R.values.max():
        cs = plt.contour(X, Y, pivot_R.values, levels=[1.0], colors='k', linewidths=2, linestyles='--')
        plt.clabel(cs, fmt='R=1.0', inline=True, fontsize=10)

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_\kappa$')
    plt.title('Phase Diagram: Energy Deficit Bifurcation')
    plt.tight_layout()
    plt.savefig(output_dir / "phase_diagram_energy_deficit.png", dpi=150)
    plt.close()

    # Plot 2: Cobb Angle
    plt.figure(figsize=(10, 8))
    cp2 = plt.contourf(X, Y, pivot_Cobb.values, levels=20, cmap='viridis')
    cbar2 = plt.colorbar(cp2)
    cbar2.set_label('Cobb Angle (degrees)')

    # Overlay R=1 contour for reference
    if pivot_R.values.min() < 1.0 < pivot_R.values.max():
        cs = plt.contour(X, Y, pivot_R.values, levels=[1.0], colors='white', linewidths=2, linestyles='--')
        plt.clabel(cs, fmt='Instability Limit', inline=True, fontsize=10, colors='white')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_\kappa$')
    plt.title('Phase Diagram: Cobb Angle Emergence')
    plt.tight_layout()
    plt.savefig(output_dir / "phase_diagram_energy_deficit_cobb.png", dpi=150)
    plt.close()
    print("Saved heatmaps to outputs/figures/")

if __name__ == "__main__":
    run_sweep()
