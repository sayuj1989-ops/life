import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.spinalmodes.iec import (
    compute_amplitude,
    solve_beam_static,
)

def bimodal_gaussian(s, L, Ac=0.5, sc=0.80, sigmac=0.08, Al=0.7, sl=0.25, sigmal=0.10, I0=0.3):
    s_norm = s / L
    bump_c = Ac * np.exp(-((s_norm - sc)**2) / (2 * sigmac**2))
    bump_l = Al * np.exp(-((s_norm - sl)**2) / (2 * sigmal**2))
    return bump_c + bump_l + I0

def compute_gradient(field, s):
    return np.gradient(field, s)

def main():
    # Setup parameters
    L_range = np.linspace(0.25, 0.55, 30)
    chi_kappa = 0.05
    E0 = 1.0e9
    rho = 1100.0
    A_cross = 0.001
    g = 9.81
    eta_a = 1.0

    # Store results
    results = []

    for L in L_range:
        s = np.linspace(0, L, 100)
        s_norm = s / L

        # Information field
        I_field = bimodal_gaussian(s, L)

        # In order to maintain the fixed-curvature assumption mentioned in the manuscript,
        # we compute gradient with respect to normalized arc length s_norm.
        # This aligns with the instruction:
        # "When simulating length-varying information fields in IEC models, compute spatial gradients with respect to normalized arc length (s/L) to satisfy the fixed-curvature assumption."
        grad_I = compute_gradient(I_field, s_norm)

        # IEC parameters
        kappa_target = chi_kappa * grad_I
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        # Note: manuscript says "g = 9.81 m/s^2", uniform body force = rho * A * g
        distributed_load = rho * A_cross * g

        # Solve full IEC model
        theta_iec, kappa_iec = solve_beam_static(
            s, kappa_target, E_field, M_active,
            I_moment=1e-8, P_load=0.0, distributed_load=distributed_load
        )

        # Solve passive model (chi_kappa = 0)
        theta_pas, kappa_pas = solve_beam_static(
            s, np.zeros_like(s), E_field, M_active,
            I_moment=1e-8, P_load=0.0, distributed_load=distributed_load
        )

        # Calculate P_counter
        # P_counter(L) = eta_a * rho * A * g * L^2 * mean(|kappa_IEC - kappa_passive|^2)
        mean_sq_diff = np.mean((kappa_iec - kappa_pas)**2)
        P_counter = eta_a * rho * A_cross * g * (L**2) * mean_sq_diff

        # Calculate Cobb angle (using amplitude of theta_iec)
        cobb_angle = compute_amplitude(theta_iec)

        # Calculate geodesic deviation D_geo
        D_geo = np.mean(np.abs(theta_iec - theta_pas))

        results.append({
            'L': L,
            'P_counter': P_counter,
            'mean_sq_diff': mean_sq_diff,
            'Cobb_angle': cobb_angle,
            'D_geo': D_geo
        })

    df = pd.DataFrame(results)

    # Calculate S_proprio
    # S0 is P_counter at L0 = 0.35
    row0 = df.iloc[(df['L'] - 0.35).abs().argsort()[:1]]
    S0 = row0['P_counter'].values[0]
    L0 = 0.35

    df['S_proprio_alpha05'] = S0 * ((df['L'] / L0) ** 0.5)
    df['S_proprio_alpha10'] = S0 * ((df['L'] / L0) ** 1.0)

    # Save CSV
    os.makedirs('outputs/thermodynamic_cost', exist_ok=True)
    df.to_csv('outputs/thermodynamic_cost/energy_deficit_window.csv', index=False)
    print("Saved outputs/thermodynamic_cost/energy_deficit_window.csv")

    # Generate Figure
    plt.figure(figsize=(8, 6), dpi=300)

    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label=r'$P_{counter}(L)$ (Demand)')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label=r'$S_{proprio}$ ($\alpha=0.5$)')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'b:', linewidth=2, label=r'$S_{proprio}$ ($\alpha=1.0$)')

    # Find intersection for alpha=0.5
    # Since P_counter scales as L^2 and S_proprio scales as L^0.5, they intersect at L0=0.35.
    # The deficit is for L > 0.35.
    L_crit = 0.35
    plt.axvline(L_crit, color='k', linestyle='--', alpha=0.5, label=f'$L_{{crit}} \\approx {L_crit:.2f}$ m')

    mask = df['L'] >= L_crit
    plt.fill_between(df.loc[mask, 'L'],
                     df.loc[mask, 'S_proprio_alpha05'],
                     df.loc[mask, 'P_counter'],
                     color='red', alpha=0.2, label='Energy Deficit Window')

    plt.xlabel('Spinal Length $L$ (m)', fontsize=12)
    plt.ylabel('Metabolic Power / Supply (normalized units)', fontsize=12)
    plt.title('Thermodynamic Cost of Countercurvature', fontsize=14)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)

    # Save figures
    os.makedirs('outputs/figures', exist_ok=True)
    plt.savefig('outputs/figures/energy_deficit_window.png', dpi=300, bbox_inches='tight')
    print("Saved outputs/figures/energy_deficit_window.png")

if __name__ == '__main__':
    main()
