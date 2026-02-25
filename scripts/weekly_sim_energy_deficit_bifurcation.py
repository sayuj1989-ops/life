import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure src is in path to import spinalmodes
sys.path.append("src")

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    # Fallback if running from a different directory structure
    sys.path.append(str(Path(__file__).parent.parent / "src"))
    from spinalmodes.iec import solve_beam_static

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

def run_experiment():
    print("Starting Energy Deficit Bifurcation Sweep...")

    # Ensure output directories exist
    Path("outputs/thermodynamic_cost").mkdir(parents=True, exist_ok=True)
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)

    # Parameters for Sweep
    L_values = np.linspace(0.25, 0.55, 31) # 0.25 to 0.55 m (adolescent growth)
    chi_values = np.linspace(0.0, 0.15, 16) # active curvature coupling strength

    # Standard IEC Parameters
    E0 = 1.0e9  # Pa (1.0 GPa)
    rho = 1100.0  # kg/m^3

    # Reference for Isometric Growth: A ~ L^2
    A_ref = 0.001
    L_ref = 0.4

    g = 9.81  # m/s^2
    eta_a = 1.0

    # Information field parameters (Bimodal Gaussian)
    # Cervical
    A_c = 0.5; s_c = 0.80; sigma_c = 0.08
    # Lumbar
    A_l = 0.7; s_l = 0.25; sigma_l = 0.10

    # Proprioceptive supply reference
    L0 = 0.35

    # We need a reference S0 (Supply at L0) to scale Supply
    # We'll calculate P_counter for a "nominal" chi_kappa at L0 to set S0
    chi_nominal = 0.05

    # --- Helper to compute P_counter for given L, chi ---
    def compute_p_counter(L, chi_k):
        A_cross = A_ref * (L / L_ref)**2
        I_moment = (A_cross**2) / (4 * np.pi)

        n_nodes = 100
        s = np.linspace(0, L, n_nodes)
        s_norm = s / L

        # Information Field Gradient
        grad_I_c = gaussian_grad(s_norm, A_c, s_c, sigma_c, L)
        grad_I_l = gaussian_grad(s_norm, A_l, s_l, sigma_l, L)
        grad_I = grad_I_c + grad_I_l

        # Loads
        q = rho * A_cross * g
        P_load = 0.0

        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        # Active State (IEC)
        kappa_target_IEC = chi_k * grad_I
        theta_IEC, kappa_IEC = solve_beam_static(
            s, kappa_target_IEC, E_field, M_active,
            I_moment=I_moment, P_load=P_load, distributed_load=q
        )

        # Passive State (Gravity only, chi=0 implicit)
        kappa_target_passive = np.zeros_like(s)
        theta_passive, kappa_passive = solve_beam_static(
            s, kappa_target_passive, E_field, M_active,
            I_moment=I_moment, P_load=P_load, distributed_load=q
        )

        # P_counter
        kappa_diff_sq = (kappa_IEC - kappa_passive)**2
        mean_kappa_diff_sq = np.mean(kappa_diff_sq)
        P_counter = eta_a * rho * A_cross * g * (L**2) * mean_kappa_diff_sq

        return P_counter

    # Calculate Reference Supply S0
    print(f"Calibrating Supply S0 at L={L0}m, chi={chi_nominal}...")
    S0 = compute_p_counter(L0, chi_nominal)
    print(f"Reference Supply S0 = {S0:.6f}")

    results = []

    print("Running 2D Parameter Sweep...")
    for chi in chi_values:
        for L in L_values:
            P_dem = compute_p_counter(L, chi)

            # Supply Model: S ~ L^0.5
            S_supp = S0 * (L / L0)**0.5

            deficit = P_dem - S_supp
            deficit_ratio = deficit / S_supp if S_supp > 0 else 0

            is_vulnerable = 1 if deficit > 0 else 0

            results.append({
                "chi_kappa": chi,
                "L": L,
                "P_demand": P_dem,
                "S_supply": S_supp,
                "Deficit": deficit,
                "Deficit_Ratio": deficit_ratio,
                "Is_Vulnerable": is_vulnerable
            })

    df = pd.DataFrame(results)

    # Save Raw Data
    csv_path = Path("outputs/thermodynamic_cost/energy_phase_diagram.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

    # --- Analysis: Critical Length L_crit ---
    # For each chi, find the first L where Deficit > 0
    l_crit_data = []
    for chi in chi_values:
        subset = df[df['chi_kappa'] == chi]
        # Interpolate to find zero crossing
        # We look for sign change in Deficit
        L_crit = np.nan

        # Check if it ever becomes positive
        if subset['Deficit'].max() > 0:
            # Find index where it crosses
            # We iterate through the sorted L values
            subset = subset.sort_values('L')
            deficits = subset['Deficit'].values
            lengths = subset['L'].values

            for i in range(len(deficits)-1):
                if deficits[i] <= 0 and deficits[i+1] > 0:
                    # Linear interpolation
                    y1, y2 = deficits[i], deficits[i+1]
                    x1, x2 = lengths[i], lengths[i+1]
                    # 0 = y1 + (x - x1) * (y2-y1)/(x2-x1)
                    # -(y1) * (x2-x1)/(y2-y1) + x1 = x
                    L_crit = x1 - y1 * (x2 - x1) / (y2 - y1)
                    break

            # If it starts positive (at L_min)
            if deficits[0] > 0:
                 L_crit = lengths[0] # Or technically < L_min

        l_crit_data.append({'chi_kappa': chi, 'L_crit': L_crit})

    df_crit = pd.DataFrame(l_crit_data)

    # --- Plotting ---

    # 1. Heatmap of Deficit Ratio
    pivot_table = df.pivot(index='chi_kappa', columns='L', values='Deficit_Ratio')

    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table, cmap='RdBu_r', center=0, cbar_kws={'label': 'Deficit Ratio (Demand-Supply)/Supply'})
    plt.gca().invert_yaxis() # Put 0 at bottom
    plt.title('Energy Deficit Phase Diagram: Bifurcation')
    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Active Curvature Strength $\chi_{\kappa}$')
    plt.tight_layout()
    plt.savefig('outputs/figures/energy_deficit_heatmap.png', dpi=300)
    plt.close()

    # 2. Phase Boundary (L_crit vs chi)
    plt.figure(figsize=(8, 6))
    plt.plot(df_crit['chi_kappa'], df_crit['L_crit'], 'k-o', linewidth=2, label='Onset of Instability ($L_{crit}$)')

    # Shade the "Vulnerable Region" (Above/Right of curve)
    # Since L > L_crit is vulnerable
    plt.fill_between(df_crit['chi_kappa'], df_crit['L_crit'], 0.6, alpha=0.2, color='red', label='Energy Deficit Window')
    plt.fill_between(df_crit['chi_kappa'], 0.2, df_crit['L_crit'], alpha=0.2, color='green', label='Metabolic Safety')

    plt.ylim(0.25, 0.55)
    plt.xlim(0, 0.15)
    plt.xlabel('Active Curvature Strength $\chi_{\kappa}$')
    plt.ylabel('Critical Length $L_{crit}$ (m)')
    plt.title('H_2026_02_08: Early Onset of Vulnerability with High $\chi_{\kappa}$')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig('outputs/figures/energy_phase_boundary.png', dpi=300)
    plt.close()

    print("Plots saved to outputs/figures/")
    print("\n--- Phase Boundary Data ---")
    print(df_crit)

if __name__ == "__main__":
    run_experiment()
