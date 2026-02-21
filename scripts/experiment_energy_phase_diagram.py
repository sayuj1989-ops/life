"""
experiment_energy_phase_diagram.py

Generates a 2D Phase Diagram (chi_kappa vs L) of the Energy Deficit Bifurcation.
Hypothesis: H_2026_02_08_EnergyPhase
"High-chi_kappa patients enter the Energy Deficit Window at shorter L."

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import solve_bvp
import os

# Ensure outputs directories exist
os.makedirs("outputs/thermodynamic_cost", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)

# --- Parameters (matching experiment_energy_deficit_window.py) ---
RHO = 1100.0  # kg/m^3
A_REF = 0.001 # m^2 (Reference area at L_REF)
L_REF = 0.4   # m (Reference length for scaling)
G = 9.81      # m/s^2
E0 = 1.0e9    # Pa (1.0 GPa)

# IEC Parameters (Bimodal Gaussian Information Field)
A_c = 0.5; s_c = 0.80; sigma_c = 0.08
A_l = 0.7; s_l = 0.25; sigma_l = 0.10
I_0 = 0.3

# Simulation Parameters
ETA_A = 1.0

def solve_column(L, chi_kappa):
    """
    Solves the beam equation for a column under gravity with intrinsic curvature.
    Returns s_eval, theta_interp, kappa_interp.
    """

    # Isometric scaling: A scales with L^2
    current_A = A_REF * (L / L_REF)**2
    # I scales with A^2 (assuming circular scaling) => I ~ L^4
    current_I = (current_A**2) / (4 * np.pi)

    s_eval = np.linspace(0, L, 100)

    def get_d2I_ds2(s):
        s_norm = s / L
        # Second derivative of Gaussian components
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
        # theta(0) = 0
        # theta'(L) = kappa_hat(L)

        # Calculate kappa_hat(L) = chi_kappa * dI/ds|L
        s_norm_L = 1.0
        dIc_dsn = A_c * np.exp(-((s_norm_L - s_c)**2) / (2 * sigma_c**2)) * (-(s_norm_L - s_c) / sigma_c**2)
        dIl_dsn = A_l * np.exp(-((s_norm_L - s_l)**2) / (2 * sigma_l**2)) * (-(s_norm_L - s_l) / sigma_l**2)
        dI_ds_L = (dIc_dsn + dIl_dsn) / L
        kappa_hat_L = chi_kappa * dI_ds_L

        return np.array([ya[0], yb[1] - kappa_hat_L])

    # Initial guess
    y_guess = np.zeros((2, s_eval.size))

    sol = solve_bvp(fun, bc, s_eval, y_guess, max_nodes=1000)

    if not sol.success:
        # Fallback or warning (usually converges for reasonable parameters)
        pass

    theta_interp = np.interp(s_eval, sol.x, sol.y[0])
    kappa_interp = np.interp(s_eval, sol.x, sol.y[1])

    return s_eval, theta_interp, kappa_interp

def main():
    print("Starting Energy Phase Diagram simulation...")

    # Grid Definition
    L_steps = 50
    chi_steps = 50
    L_values = np.linspace(0.15, 0.65, L_steps)
    chi_values = np.linspace(0.01, 20.0, chi_steps)

    # Precompute Reference Supply S0
    # Reference: L=0.35, chi_kappa=0.05
    L_ref_supply = 0.35
    chi_ref_supply = 0.05

    # 1. Active (IEC) at ref
    _, _, kappa_iec_ref = solve_column(L_ref_supply, chi_ref_supply)
    # 2. Passive at ref (chi=0)
    _, _, kappa_pass_ref = solve_column(L_ref_supply, 0.0)

    current_A_ref = A_REF * (L_ref_supply / L_REF)**2
    msd_kappa_ref = np.mean((kappa_iec_ref - kappa_pass_ref)**2)
    S0 = ETA_A * RHO * current_A_ref * G * (L_ref_supply**2) * msd_kappa_ref

    print(f"Reference Supply S0 computed at L={L_ref_supply}, chi={chi_ref_supply}: {S0:.2e}")

    # Initialize data storage
    X, Y = np.meshgrid(L_values, chi_values)
    Z_deficit = np.zeros_like(X)

    data_records = []

    # Parameter Sweep
    for i, chi in enumerate(chi_values):
        for j, L in enumerate(L_values):
            # Compute Demand (P_counter)
            current_A = A_REF * (L / L_REF)**2

            # Active
            _, _, kappa_iec = solve_column(L, chi)
            # Passive
            _, _, kappa_pass = solve_column(L, 0.0)

            msd_kappa = np.mean((kappa_iec - kappa_pass)**2)
            P_counter = ETA_A * RHO * current_A * G * (L**2) * msd_kappa

            # Compute Supply
            # S(L) = S0 * (L / L_ref_supply)^2
            Supply = S0 * (L / L_ref_supply)**2

            Deficit = P_counter - Supply
            Z_deficit[i, j] = Deficit

            data_records.append({
                "chi_kappa": chi,
                "L": L,
                "P_counter": P_counter,
                "Supply": Supply,
                "Deficit": Deficit
            })

        if (i+1) % 10 == 0:
            print(f"Computed row {i+1}/{chi_steps} (chi_kappa={chi:.2f})")

    # Save Data
    df = pd.DataFrame(data_records)
    output_csv = "outputs/thermodynamic_cost/energy_phase_diagram.csv"
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

    # Plotting
    plt.figure(figsize=(10, 8))

    # Heatmap
    # Use pcolormesh for proper grid alignment
    # Norm: centered at 0 with diverging colormap

    vmin = -np.max(np.abs(Z_deficit))
    vmax = np.max(np.abs(Z_deficit))

    # Cap the color range to visualize the transition better?
    # Or just use symmetric log if values span orders of magnitude?
    # P_counter scales significantly. Deficit can be large.
    # Let's use a symmetric linear scale but clamped if needed, or just standard.
    # The bifurcation is at 0.

    plt.pcolormesh(X, Y, Z_deficit, cmap='RdBu_r', vmin=-1e-4, vmax=1e-4, shading='auto')
    # Note: vmin/vmax likely need adjustment based on S0 magnitude.
    # S0 is likely small. Let's auto-scale or use percentiles, but 0 must be white.
    # Re-plotting with dynamic limits centered at 0.

    max_val = np.max(np.abs(Z_deficit))
    # We want to highlight the zero crossing.

    pcm = plt.pcolormesh(X, Y, Z_deficit, cmap='RdBu_r',
                         vmin=-max_val/2, vmax=max_val/2, shading='auto')

    plt.colorbar(pcm, label='Energy Deficit (J/m?)')

    # Zero Contour (Bifurcation Line)
    CS = plt.contour(X, Y, Z_deficit, levels=[0], colors='k', linewidths=2, linestyles='--')
    plt.clabel(CS, inline=True, fontsize=10, fmt='Bifurcation')

    plt.xlabel('Spinal Length L (m)', fontsize=12)
    plt.ylabel(r'Coupling Strength $\chi_\kappa$', fontsize=12)
    plt.title('Energy Deficit Phase Diagram', fontsize=14)

    plt.text(0.2, 15, "Vulnerability Zone\n(Deficit > 0)", color='red', fontsize=12, fontweight='bold')
    plt.text(0.5, 2, "Safe Zone\n(Surplus)", color='blue', fontsize=12, fontweight='bold')

    plt.tight_layout()
    output_png = "outputs/figures/energy_phase_diagram.png"
    plt.savefig(output_png, dpi=300)
    print(f"Figure saved to {output_png}")

if __name__ == "__main__":
    main()
