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

    # Proprioceptive supply reference (calibrated to cross at 0.35m)
    L_crit_target = 0.35

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
        ds = s[1] - s[0]

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

        # 6. Compute Thermodynamic Cost (Demand)
        # The Cost is proportional to the Active Moment required to maintain the difference
        # between the Passive (Gravity-Sagged) state and the Active (Target) state.
        # M_active_required = EI * (kappa_IEC - kappa_passive)
        # Cost ~ Integral |M_active_required| ds

        M_active_required = E_field * I_moment * (kappa_IEC - kappa_passive)

        # Integrated Moment (Total Active Work Capacity Required)
        # Units: Nm * m = J (Energy-like) or just Integrated Moment (Nm^2?) No.
        # Moment (Nm) integrated over length (m) = Nm^2? No.
        # Let's normalize by a reference length or just use the raw value.
        # Scaling Analysis:
        # EI ~ L^4
        # kappa ~ L^-1 (geometric similarity) or L^-2 (gravity sag)?
        # If simulation is correct, we can observe the scaling directly.

        Demand_IntegratedMoment = np.sum(np.abs(M_active_required)) * ds

        # Alternatively, calculate Power ~ Moment * Rate.
        # But we assume Rate is constant. So Cost ~ Moment.

        # 7. Additional Metrics
        # Cobb Angle
        cobb_angle = np.degrees(np.max(theta_IEC) - np.min(theta_IEC))

        results.append({
            "L": L,
            "Demand_IntegratedMoment": Demand_IntegratedMoment,
            "Cobb_angle": cobb_angle,
            "EI": E0 * I_moment,
            "Mass": rho * A_cross * L
        })

    df = pd.DataFrame(results)

    # --- Supply Curve Calibration ---
    # We calibrate Supply to equal Demand at L_crit_target (0.35m)
    # Supply S ~ L^2 (Surface Limited) or L^3 (Volume Limited)

    # Interpolate Demand at L_crit
    Demand_at_crit = np.interp(L_crit_target, df['L'], df['Demand_IntegratedMoment'])

    # Calculate Supply Curves
    # S = S0 * (L / L_crit)^alpha
    # S0 = Demand_at_crit (to force crossover)

    # Case 1: Surface Limited (L^2) - e.g. Mitochondrial Surface Area
    df['Supply_L2'] = Demand_at_crit * (df['L'] / L_crit_target)**2.0

    # Case 2: Volume Limited (L^3) - e.g. ATP Pool (Optimistic)
    # But usually Supply < Demand is the problem.
    # If Demand scales as L^4, both L^2 and L^3 will cross.
    # We focus on L^2 as the conservative biological limit (West et al.)

    # Case 3: Optimistic Supply (L^3)
    df['Supply_L3'] = Demand_at_crit * (df['L'] / L_crit_target)**3.0

    # Check scaling of Demand
    # Fit log-log to get exponent
    log_L = np.log(df['L'])
    log_D = np.log(df['Demand_IntegratedMoment'])
    coeffs = np.polyfit(log_L, log_D, 1)
    demand_exponent = coeffs[0]

    print(f"Demand Scaling Exponent: {demand_exponent:.4f} (Expected ~4.0)")

    # Save CSV
    out_dir = Path("outputs/thermodynamic_cost")
    csv_path = out_dir / "energy_deficit_window_v2.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

    # Generate Figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Demand
    ax.plot(df['L'], df['Demand_IntegratedMoment'], 'r-', linewidth=2, label=f'Demand (Moment) $\\propto L^{{{demand_exponent:.1f}}}$')

    # Plot Supply
    ax.plot(df['L'], df['Supply_L2'], 'b--', linewidth=2, label=r'Supply (Surface) $\propto L^{2.0}$')
    # ax.plot(df['L'], df['Supply_L3'], 'g:', label=r'Supply (Volume) $\propto L^{3.0}$')

    # Fill Deficit Window
    ax.fill_between(df['L'], df['Demand_IntegratedMoment'], df['Supply_L2'],
                    where=(df['Demand_IntegratedMoment'] > df['Supply_L2']),
                    color='red', alpha=0.1, interpolate=True, label='Energy Deficit Window')

    ax.set_xlabel('Spinal Length L (m)')
    ax.set_ylabel('Thermodynamic Cost (Integrated Moment, Nm·m)')
    ax.set_title('Metabolic Buckling: The Allometric Trap')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Annotate Crossover
    ax.axvline(L_crit_target, color='k', linestyle='--', alpha=0.5)
    ax.text(L_crit_target, ax.get_ylim()[1]*0.8, f' $L_{{crit}} = {L_crit_target}m$', rotation=90)

    # Highlight Growth Spurt Zone (0.35 - 0.45)
    # ax.axvspan(0.35, 0.45, color='orange', alpha=0.05)

    fig_path = Path("outputs/figures/energy_deficit_window.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved Figure to {fig_path}")

    # --- Analysis for Manuscript ---
    target_L = 0.45
    D_target = np.interp(target_L, df['L'], df['Demand_IntegratedMoment'])
    S_target = np.interp(target_L, df['L'], df['Supply_L2'])
    deficit_pct = ((D_target - S_target) / S_target) * 100

    print("\n--- Manuscript Statistics ---")
    print(f"Critical Length L_crit: {L_crit_target} m")
    print(f"At L = {target_L} m (Peak Growth):")
    print(f"  Demand  = {D_target:.4f}")
    print(f"  Supply  = {S_target:.4f}")
    print(f"  Deficit = {deficit_pct:.1f}%")

if __name__ == "__main__":
    run_experiment()
