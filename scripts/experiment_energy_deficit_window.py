#!/usr/bin/env python3
"""
Simulates the "Thermodynamic Cost of Countercurvature" (P_counter) as a function of spinal length L.
Identifies the critical L where the Energy Deficit Window opens.

Parameters:
- L: 0.25 to 0.55 m (30 steps)
- IEC parameters: chi_kappa=0.05, E0=1.0 GPa, rho=1100 kg/m^3
- A scales isometrically (A ~ L^2) with A=0.001 m^2 at L=0.35 m
- Information field: Bimodal Gaussian
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
E0 = 1.0e9       # Pa
rho = 1100.0     # kg/m^3
g = 9.81         # m/s^2
chi_kappa = 0.05
eta_a = 1.0      # Normalized units

# Isometric Growth Reference
L_ref = 0.35     # m
A_ref = 0.001    # m^2 at L_ref

# Information field parameters (Bimodal Gaussian)
# Cervical
A_c = 0.5; s_c = 0.80; sigma_c = 0.08
# Lumbar
A_l = 0.7; s_l = 0.25; sigma_l = 0.10
I_0 = 0.3 # Baseline

# Proprioceptive Supply parameters
L_0 = 0.35 # m (pre-adolescent reference, same as L_ref)

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

def solve_system(L):
    """
    Solves the system for a given L.
    Returns: P_counter, Cobb_angle
    """
    # Isometric Growth: A scales with L^2
    A = A_ref * (L / L_ref)**2

    # Moment of Inertia (Circular approx)
    I_moment = (A**2) / (4 * np.pi)

    # Spatial grid
    n_nodes = 100
    s = np.linspace(0, L, n_nodes)

    # 1. Compute Gradient
    grad_I = get_bimodal_field_gradient(s, L)

    # 2. Loads
    q = rho * A * g  # N/m
    P_load = 0.0     # N (assuming gravity only as per methods)

    # 3. Beam Properties
    E_field = np.full_like(s, E0)
    M_active = np.zeros_like(s)

    # 4. IEC Equilibrium (Active)
    # kappa_target = chi_kappa * grad_I
    kappa_target_IEC = chi_kappa * grad_I
    theta_IEC, kappa_IEC = solve_beam_static(
        s, kappa_target_IEC, E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # 5. Passive Equilibrium (Gravity only)
    # kappa_target = 0
    kappa_target_passive = np.zeros_like(s)
    theta_passive, kappa_passive = solve_beam_static(
        s, kappa_target_passive, E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # 6. Thermodynamic Cost
    # P_counter ~ eta_a * rho * A * g * L^2 * <|kappa_IEC - kappa_passive|^2>
    kappa_diff_sq = (kappa_IEC - kappa_passive)**2
    mean_kappa_diff_sq = np.mean(kappa_diff_sq)
    P_counter = eta_a * rho * A * g * (L**2) * mean_kappa_diff_sq

    # 7. Cobb Angle (just for reference)
    cobb_angle = np.degrees(np.max(theta_IEC) - np.min(theta_IEC))
    d_geo = np.mean(np.abs(theta_IEC - theta_passive)) # Geodesic deviation proxy

    return P_counter, cobb_angle, d_geo

def main():
    print("Starting Energy Deficit Window Simulation (Isometric Scaling)...")

    output_dir = Path("outputs/thermodynamic_cost")
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = Path("outputs/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Parameter Sweep L
    L_vals = np.linspace(0.25, 0.55, 30)

    # First pass: Calculate P_counter for all L
    results_pre = []
    for L in L_vals:
        P_cnt, cobb, d_geo = solve_system(L)
        results_pre.append({
            "L": L,
            "P_counter": P_cnt,
            "Cobb_angle": cobb,
            "D_geo": d_geo
        })

    df_pre = pd.DataFrame(results_pre)

    # Calculate S0 at L_0 = 0.35
    # Interpolate or use closest value
    # We can assume S0 = P_counter at L_0 (if we calculate it exactly)
    P_0, _, _ = solve_system(L_0)
    S_0 = P_0
    print(f"Calibrated Supply S0 = {S_0:.6f} at L0={L_0}m")

    # Second pass: Compute S_proprio and find L_crit
    results_final = []

    for idx, row in df_pre.iterrows():
        L = row["L"]
        P_cnt = row["P_counter"]

        # S_proprio(L) = S_0 * (L / L_0)^alpha
        S_proprio_05 = S_0 * (L / L_0)**0.5
        S_proprio_10 = S_0 * (L / L_0)**1.0

        results_final.append({
            "L": L,
            "P_counter": P_cnt,
            "S_proprio_alpha05": S_proprio_05,
            "S_proprio_alpha10": S_proprio_10,
            "Cobb_angle": row["Cobb_angle"],
            "D_geo": row["D_geo"]
        })

    df = pd.DataFrame(results_final)
    csv_path = output_dir / "energy_deficit_window.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(df["L"], df["P_counter"], 'r-', linewidth=2, label=r'$P_{counter}$ (Demand ~ $L^2$)')
    plt.plot(df["L"], df["S_proprio_alpha05"], 'b--', linewidth=2, label=r'$S_{proprio}$ ($\alpha=0.5$)')
    plt.plot(df["L"], df["S_proprio_alpha10"], 'g--', linewidth=2, label=r'$S_{proprio}$ ($\alpha=1.0$)')

    # Shaded region between P_counter and S_proprio_alpha05 (assuming alpha=0.5 is main case)
    # Only shade where P > S
    plt.fill_between(df["L"], df["P_counter"], df["S_proprio_alpha05"],
                     where=(df["P_counter"] > df["S_proprio_alpha05"]),
                     color='red', alpha=0.2, label='Energy Deficit Window')

    # Mark L0
    plt.axvline(x=L_0, color='k', linestyle=':', label=r'$L_{crit} \approx L_0$')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Thermodynamic Cost / Supply (Normalized)')
    plt.title('Energy Deficit Window: Demand vs Supply')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plot_path = figures_dir / "energy_deficit_window.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"Saved figure to {plot_path}")

if __name__ == "__main__":
    main()
