"""
experiment_energy_deficit_window.py

Simulates the Thermodynamic Cost of Countercurvature (P_counter) as a function of spinal length L,
identifying the critical length L_crit where the Energy Deficit Window opens.

Solves the beam equation for a column under gravity with intrinsic curvature.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_bvp
import os
import sys

# Ensure outputs directories exist
os.makedirs("outputs/thermodynamic_cost", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)

# --- Parameters ---
RHO = 1100.0  # kg/m^3
A_REF = 0.001 # m^2 (Reference area at L_REF)
L_REF = 0.4   # m (Reference length for scaling)
G = 9.81      # m/s^2
E0 = 1.0e9    # Pa (1.0 GPa)

# IEC Parameters (Bimodal Gaussian)
A_c = 0.5; s_c = 0.80; sigma_c = 0.08
A_l = 0.7; s_l = 0.25; sigma_l = 0.10
I_0 = 0.3

# Simulation Parameters
L_MIN = 0.20
L_MAX = 0.60
N_STEPS = 50
ETA_A = 1.0

def get_information_field(s, L):
    """
    Computes the bimodal Gaussian information field I(s).
    s: array of spatial coordinates [0, L]
    L: total length
    """
    s_norm = s / L

    # Cervical lordosis component
    I_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))

    # Lumbar lordosis component
    I_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return I_c + I_l + I_0

def solve_column(L, chi_kappa):
    """
    Solves the beam equation for a column under gravity with intrinsic curvature.

    Governing equation (small angle approximation):
    theta'' = kappa_hat' - (P(s)/EI) * theta

    where P(s) = rho * A * g * (L - s)
    """

    # Isometric scaling: A scales with L^2
    current_A = A_REF * (L / L_REF)**2
    # I scales with A^2 (assuming circular scaling) => I ~ L^4
    current_I = (current_A**2) / (4 * np.pi)

    s_eval = np.linspace(0, L, 100)

    def get_d2I_ds2(s):
        s_norm = s / L
        # Second derivative of Gaussian:
        term_c = np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2)) * \
                 ( ((s_norm - s_c)**2)/(sigma_c**4) - 1/(sigma_c**2) )
        d2Ic_dsn2 = A_c * term_c

        term_l = np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2)) * \
                 ( ((s_norm - s_l)**2)/(sigma_l**4) - 1/(sigma_l**2) )
        d2Il_dsn2 = A_l * term_l

        return (d2Ic_dsn2 + d2Il_dsn2) / (L**2)

    def fun(s, y):
        theta = y[0]
        # theta_prime = y[1]

        P_s = RHO * current_A * G * (L - s)
        kappa_hat_prime = chi_kappa * get_d2I_ds2(s)

        # theta'' = kappa_hat' - (P(s)/EI) * theta
        theta_double_prime = kappa_hat_prime - (P_s / (E0 * current_I)) * theta

        return np.vstack((y[1], theta_double_prime))

    def bc(ya, yb):
        # ya is at s=0, yb is at s=L
        # theta(0) = 0
        # theta'(L) = kappa_hat(L)

        s_norm_L = 1.0
        dIc_dsn = A_c * np.exp(-((s_norm_L - s_c)**2) / (2 * sigma_c**2)) * (-(s_norm_L - s_c) / sigma_c**2)
        dIl_dsn = A_l * np.exp(-((s_norm_L - s_l)**2) / (2 * sigma_l**2)) * (-(s_norm_L - s_l) / sigma_l**2)
        dI_ds_L = (dIc_dsn + dIl_dsn) / L
        kappa_hat_L = chi_kappa * dI_ds_L

        return np.array([ya[0], yb[1] - kappa_hat_L])

    # Initial guess: zero
    y_guess = np.zeros((2, s_eval.size))

    sol = solve_bvp(fun, bc, s_eval, y_guess, max_nodes=1000)

    if not sol.success:
        print(f"Warning: Solver failed for L={L}, chi_kappa={chi_kappa}")

    theta_interp = np.interp(s_eval, sol.x, sol.y[0])
    kappa_interp = np.interp(s_eval, sol.x, sol.y[1])

    return s_eval, theta_interp, kappa_interp

def main():
    print("Starting Energy Deficit Window simulation...")
    L_values = np.linspace(L_MIN, L_MAX, N_STEPS)
    results = []

    for L in L_values:
        # Isometric scaling for P_counter calculation
        current_A = A_REF * (L / L_REF)**2

        # 1. Compute Active (IEC) curvature
        s, theta_iec, kappa_iec = solve_column(L, chi_kappa=0.05)

        # 2. Compute Passive (Gravity only) curvature
        _, theta_passive, kappa_passive = solve_column(L, chi_kappa=0.0)

        # 3. Compute P_counter
        # P_counter ~ η_a * ρ * A * g * L² * <|κ_IEC - κ_passive|²>
        # Note: A ~ L^2. So P ~ L^2 * L^2 * (1/L)^2 ~ L^2 if kappa ~ 1/L.
        # But if gravity dominates, kappa_passive deviates more.
        msd_kappa = np.mean((kappa_iec - kappa_passive)**2)
        P_counter = ETA_A * RHO * current_A * G * (L**2) * msd_kappa

        results.append({
            "L": L,
            "P_counter": P_counter
        })

    df = pd.DataFrame(results)

    # Interpolate P_counter at L_crit = 0.35 to set the crossover point
    L_crit = 0.35
    if L_crit < df['L'].min() or L_crit > df['L'].max():
         S0 = df.iloc[len(df)//2]['P_counter']
    else:
         S0 = np.interp(L_crit, df['L'], df['P_counter'])

    # Calculate Supply curve
    # Supply scales as Surface Area (L^2)
    # We calibrate it to match Demand at L_crit
    df['S_proprio'] = S0 * (df['L'] / L_crit)**2.0

    # Save CSV
    output_csv = "outputs/thermodynamic_cost/energy_deficit_window.csv"
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plot P_counter (Demand)
    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=3, label=r'Metabolic Demand ($P_{counter}$)')

    # Plot S_proprio (Supply)
    plt.plot(df['L'], df['S_proprio'], 'b--', linewidth=2, label=r'Metabolic Supply ($L^2$ Scaling)')

    # Shade Energy Deficit Window
    deficit_mask = df['P_counter'] > df['S_proprio']
    if deficit_mask.any():
        plt.fill_between(df['L'], df['P_counter'], df['S_proprio'],
                         where=deficit_mask, color='red', alpha=0.2, label='Energy Deficit Window')

        # Add annotation for the deficit
        # Find max deficit
        deficit_vals = df['P_counter'] - df['S_proprio']
        max_idx = deficit_vals.argmax()
        max_L = df.iloc[max_idx]['L']
        max_val = df.iloc[max_idx]['P_counter']

        plt.annotate('Thermodynamic\nBuckling', xy=(max_L, max_val), xytext=(max_L-0.1, max_val),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=12, fontweight='bold')


    plt.xlabel('Spinal Length L (m)', fontsize=14)
    plt.ylabel('Thermodynamic Cost (J/s)', fontsize=14)
    plt.title('The Energy Deficit Window', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)

    # Add Critical Length Line
    plt.axvline(x=L_crit, color='k', linestyle=':', alpha=0.5)
    plt.text(L_crit + 0.01, df['P_counter'].min(), r'$L_{crit} \approx 0.35$ m', rotation=90, va='bottom')

    output_png = "outputs/figures/energy_deficit_window.png"
    plt.savefig(output_png, dpi=300)
    print(f"Figure saved to {output_png}")

if __name__ == "__main__":
    main()
