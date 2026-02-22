import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    print("Starting Energy Deficit Window Experiment...")

    # Ensure output directories exist
    Path("outputs/thermodynamic_cost").mkdir(parents=True, exist_ok=True)
    Path("outputs/figures").mkdir(parents=True, exist_ok=True)

    # Parameters
    L_min, L_max = 0.25, 0.55
    n_steps = 30
    L_values = np.linspace(L_min, L_max, n_steps)

    # Standard IEC Parameters
    E0 = 1.0e9  # Pa (1.0 GPa)
    rho = 1100.0  # kg/m^3
    # A=0.001 m^2 is the reference area at standard length L=0.4m
    # We implement Isometric Growth: A ~ L^2 to match manuscript logic.
    A_ref = 0.001
    L_ref = 0.4

    g = 9.81  # m/s^2
    chi_kappa = 0.05
    eta_a = 1.0

    # Information field parameters (Bimodal Gaussian)
    # Cervical
    A_c = 0.5; s_c = 0.80; sigma_c = 0.08
    # Lumbar
    A_l = 0.7; s_l = 0.25; sigma_l = 0.10
    I_0 = 0.3 # Baseline

    # Proprioceptive supply reference
    L0 = 0.35

    results = []

    for L in L_values:
        # Isometric Growth: A scales with L^2
        A_cross = A_ref * (L / L_ref)**2

        # Moment of Inertia (Circular approx)
        # I = A^2 / (4*pi)
        I_moment = (A_cross**2) / (4 * np.pi)

        # Spatial grid
        n_nodes = 100
        s = np.linspace(0, L, n_nodes)
        s_norm = s / L

        # 1. Compute Information Field Gradient (nabla I)
        # I(s) = I_c(s) + I_l(s) + I_0
        grad_I_c = gaussian_grad(s_norm, A_c, s_c, sigma_c, L)
        grad_I_l = gaussian_grad(s_norm, A_l, s_l, sigma_l, L)
        grad_I = grad_I_c + grad_I_l

        # 2. Define Loads
        # Distributed load q = rho * A * g
        q = rho * A_cross * g
        P_load = 0.0

        # 3. Beam Properties
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s) # chi_f = 0

        # 4. Compute IEC Equilibrium (Active)
        # kappa_target = chi_kappa * grad_I
        kappa_target_IEC = chi_kappa * grad_I

        theta_IEC, kappa_IEC = solve_beam_static(
            s, kappa_target_IEC, E_field, M_active,
            I_moment=I_moment, P_load=P_load, distributed_load=q
        )

        # 5. Compute Passive Equilibrium (Gravity only)
        # kappa_target = 0
        kappa_target_passive = np.zeros_like(s)

        theta_passive, kappa_passive = solve_beam_static(
            s, kappa_target_passive, E_field, M_active,
            I_moment=I_moment, P_load=P_load, distributed_load=q
        )

        # 6. Compute Thermodynamic Cost P_counter
        # P_counter ~ eta_a * rho * A * g * L^2 * <|kappa_IEC - kappa_passive|^2>
        kappa_diff_sq = (kappa_IEC - kappa_passive)**2
        mean_kappa_diff_sq = np.mean(kappa_diff_sq) # Average (1/m^2)

        P_counter = eta_a * rho * A_cross * g * (L**2) * mean_kappa_diff_sq

        # 7. Additional Metrics
        # Cobb Angle
        cobb_angle = np.degrees(np.max(theta_IEC) - np.min(theta_IEC))

        # Geodesic Deviation D_geo
        D_geo = np.sqrt(mean_kappa_diff_sq) * L

        results.append({
            "L": L,
            "P_counter": P_counter,
            "Cobb_angle": cobb_angle,
            "D_geo": D_geo,
            "mean_kappa_diff_sq": mean_kappa_diff_sq
        })

    df = pd.DataFrame(results)

    # Calculate Proprioceptive Supply Curves
    # Reference P_counter at L0.
    S0 = np.interp(L0, df['L'], df['P_counter'])

    # Supply scaling models:
    df['S_proprio_alpha05'] = S0 * (df['L'] / L0)**0.5
    df['S_proprio_alpha10'] = S0 * (df['L'] / L0)**1.0

    print("\nResults Summary:")
    print(df[['L', 'P_counter', 'S_proprio_alpha05', 'Cobb_angle']].head())
    print(df[['L', 'P_counter', 'S_proprio_alpha05', 'Cobb_angle']].tail())

    # Save CSV
    out_dir = Path("outputs/thermodynamic_cost")
    csv_path = out_dir / "energy_deficit_window.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

    # Generate Figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Demand
    ax.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label=r'Demand $P_{counter} \propto L^2$ (Isometric)')

    # Plot Supply
    ax.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label=r'Supply $S_{proprio} \propto L^{0.5}$')
    ax.plot(df['L'], df['S_proprio_alpha10'], 'b:', label=r'Supply $S_{proprio} \propto L^{1.0}$')

    # Fill Deficit Window
    ax.fill_between(df['L'], df['P_counter'], df['S_proprio_alpha05'],
                    where=(df['P_counter'] > df['S_proprio_alpha05']),
                    color='red', alpha=0.1, interpolate=True, label='Energy Deficit Window')

    ax.set_xlabel('Spinal Length L (m)')
    ax.set_ylabel('Thermodynamic Cost (Normalized)')
    ax.set_title('Thermodynamic Buckling: Cost vs Supply Capacity')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add annotation for Critical Length
    deficit_mask = df['P_counter'] > df['S_proprio_alpha05']
    if deficit_mask.any():
        idx = deficit_mask.idxmax()
        # Find intersection properly
        diff = df['P_counter'] - df['S_proprio_alpha05']
        roots = []
        for i in range(len(diff)-1):
            if diff.iloc[i] * diff.iloc[i+1] < 0:
                x1, y1 = df.iloc[i]['L'], diff.iloc[i]
                x2, y2 = df.iloc[i+1]['L'], diff.iloc[i+1]
                root = x1 - y1 * (x2 - x1) / (y2 - y1)
                roots.append(root)

        if roots:
            L_crit_val = roots[0]
            ax.axvline(L_crit_val, color='k', linestyle='--', alpha=0.5)
            ax.text(L_crit_val, ax.get_ylim()[1]*0.8, f' $L_{{crit}} \\approx {L_crit_val:.2f}$ m', rotation=90)

    fig_dir = Path("outputs/figures")
    fig_path = fig_dir / "energy_deficit_window.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved Figure to {fig_path}")

    # --- Analysis for Manuscript ---
    target_L = 0.45
    P_target = np.interp(target_L, df['L'], df['P_counter'])
    S_target = np.interp(target_L, df['L'], df['S_proprio_alpha05'])
    deficit_pct = ((P_target - S_target) / S_target) * 100

    print("\n--- Manuscript Statistics ---")
    print(f"Reference Length L0: {L0} m")
    print(f"At L = {target_L} m:")
    print(f"  P_counter = {P_target:.4f}")
    print(f"  S_proprio = {S_target:.4f}")
    print(f"  Deficit   = {deficit_pct:.1f}%")

if __name__ == "__main__":
    run_experiment()
