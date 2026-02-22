import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    import seaborn as sns
except ImportError:
    sns = None

# Ensure src is in path to import spinalmodes
sys.path.append("src")

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    # Fallback if running from a different directory structure
    repo_root = Path(__file__).parent.parent
    sys.path.append(str(repo_root / "src"))
    from spinalmodes.iec import solve_beam_static

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------
# Standard IEC Parameters (Physical Constants)
E0 = 1.0e9  # Pa (1.0 GPa)
RHO = 1100.0  # kg/m^3
G = 9.81  # m/s^2
ETA_A = 1.0 # Efficiency factor for cost

# Geometric scaling
A_REF = 0.001  # m^2 at L=0.4m
L_REF = 0.4

# Information field parameters (Bimodal Gaussian)
A_C = 0.5; S_C = 0.80; SIGMA_C = 0.08
A_L = 0.7; S_L = 0.25; SIGMA_L = 0.10

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

def compute_energy_cost(L, chi):
    """
    Compute the thermodynamic cost P_counter for a given length L and coupling chi.
    """
    # Isometric Growth: A scales with L^2
    A_cross = A_REF * (L / L_REF)**2
    # Moment of Inertia I ~ A^2
    I_moment = (A_cross**2) / (4 * np.pi)

    # Spatial grid
    n_nodes = 100
    s = np.linspace(0, L, n_nodes)
    s_norm = s / L

    # Information Field Gradient (nabla I)
    grad_I_c = gaussian_grad(s_norm, A_C, S_C, SIGMA_C, L)
    grad_I_l = gaussian_grad(s_norm, A_L, S_L, SIGMA_L, L)
    grad_I = grad_I_c + grad_I_l

    # Loads
    q = RHO * A_cross * G
    P_load = 0.0

    # Beam Properties
    E_field = np.full_like(s, E0)
    M_active = np.zeros_like(s)

    # IEC Equilibrium (Active)
    kappa_target_IEC = chi * grad_I
    theta_IEC, kappa_IEC = solve_beam_static(
        s, kappa_target_IEC, E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # Passive Equilibrium (Gravity only, chi=0 implicit for kappa_target)
    kappa_target_passive = np.zeros_like(s)
    theta_passive, kappa_passive = solve_beam_static(
        s, kappa_target_passive, E_field, M_active,
        I_moment=I_moment, P_load=P_load, distributed_load=q
    )

    # Thermodynamic Cost P_counter
    # P_counter ~ eta_a * rho * A * g * L^2 * <|kappa_IEC - kappa_passive|^2>
    kappa_diff_sq = (kappa_IEC - kappa_passive)**2
    mean_kappa_diff_sq = np.mean(kappa_diff_sq)
    P_counter = ETA_A * RHO * A_cross * G * (L**2) * mean_kappa_diff_sq

    return P_counter

def compute_supply(L, S0, L0):
    """Compute supply based on scaling law."""
    return S0 * (L / L0)**0.5

def run_experiment():
    print("Starting Energy Phase Diagram Experiment (H_2026_02_08)...")

    # Ensure output directories exist
    Path("outputs/thermodynamic_cost").mkdir(parents=True, exist_ok=True)
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)

    # Ranges for sweep
    L_values = np.linspace(0.2, 0.6, 40)
    chi_values = np.linspace(0.0, 0.2, 21)

    # ---------------------------------------------------------
    # 2. Compute Baseline Supply Curve
    # ---------------------------------------------------------
    chi_baseline = 0.05
    L0 = 0.35

    print(f"Computing Baseline Supply Curve (chi={chi_baseline}, L0={L0})...")

    # Calculate S0 (Cost at L0 for baseline chi)
    S0 = compute_energy_cost(L0, chi_baseline)
    print(f"Baseline Cost S0 at L={L0}m: {S0:.6f} Watts (normalized)")

    # ---------------------------------------------------------
    # 3. Perform 2D Parameter Sweep
    # ---------------------------------------------------------
    print(f"Starting Sweep: {len(chi_values)} chi x {len(L_values)} L = {len(chi_values)*len(L_values)} points.")

    results = []

    for chi in chi_values:
        for L in L_values:
            P_counter = compute_energy_cost(L, chi)
            S_proprio = compute_supply(L, S0, L0)
            deficit = P_counter - S_proprio

            results.append({
                "chi_kappa": chi,
                "L": L,
                "P_counter": P_counter,
                "S_proprio": S_proprio,
                "Deficit": deficit,
                "Is_Deficit": deficit > 0
            })

    df = pd.DataFrame(results)

    # Save Data
    csv_path = Path("outputs/thermodynamic_cost/energy_phase_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved Data to {csv_path}")

    # ---------------------------------------------------------
    # 4. Visualization (Phase Diagram)
    # ---------------------------------------------------------
    # Pivot for Heatmap
    pivot_table = df.pivot(index="chi_kappa", columns="L", values="Deficit")

    # Flip y-axis so high chi is at top
    pivot_table = pivot_table.sort_index(ascending=False)

    plt.figure(figsize=(10, 8))

    if sns:
        ax = sns.heatmap(
            pivot_table,
            cmap="RdBu_r",
            center=0,
            cbar_kws={'label': r'Energy Deficit ($P_{counter} - S_{proprio}$)'}
        )

        xticks = ax.get_xticks()

        n_ticks_x = 10
        x_indices = np.linspace(0, len(pivot_table.columns)-1, n_ticks_x, dtype=int)
        ax.set_xticks(x_indices + 0.5)
        ax.set_xticklabels([f"{pivot_table.columns[i]:.2f}" for i in x_indices], rotation=0)

        n_ticks_y = 10
        y_indices = np.linspace(0, len(pivot_table.index)-1, n_ticks_y, dtype=int)
        ax.set_yticks(y_indices + 0.5)
        ax.set_yticklabels([f"{pivot_table.index[i]:.2f}" for i in y_indices], rotation=0)

    else:
        pivot_imshow = df.pivot(index="chi_kappa", columns="L", values="Deficit")
        plt.imshow(
            pivot_imshow,
            aspect='auto',
            extent=[L_values.min(), L_values.max(), chi_values.min(), chi_values.max()],
            cmap="RdBu_r",
            origin='lower'
        )
        plt.colorbar(label=r'Energy Deficit ($P_{counter} - S_{proprio}$)')

    plt.title("Energy Deficit Phase Diagram")
    plt.xlabel("Spine Length L (m)")
    plt.ylabel(r"Coupling Strength $\chi_\kappa$")

    fig_path = Path("outputs/figures/energy_phase_diagram.png")
    plt.savefig(fig_path, dpi=300)
    print(f"Saved Figure to {fig_path}")

if __name__ == "__main__":
    run_experiment()
