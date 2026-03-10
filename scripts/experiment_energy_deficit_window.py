import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from spinalmodes.iec import solve_beam_static

def main():
    # Setup directories
    os.makedirs('outputs/thermodynamic_cost', exist_ok=True)
    os.makedirs('outputs/figures', exist_ok=True)
    os.makedirs('figures/main', exist_ok=True)

    # Parameters
    L_vals = np.linspace(0.25, 0.55, 30)
    chi_kappa = 0.05
    E0 = 1.0e9
    rho = 1100.0
    A_cross = 0.001
    g = 9.81
    I_moment = 1e-8
    eta_a = 1.0

    # Information field parameters
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08
    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10
    I_0 = 0.3

    results = []

    # Function to compute P_counter for a given L
    def compute_P_counter(L):
        s = np.linspace(0, L, 100)
        s_norm = s / L

        # Bimodal Gaussian
        I_field = (A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2)) +
                   A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2)) + I_0)

        grad_I_s = np.gradient(I_field, s)
        # IEC-1 coupling with L factor to maintain fixed-curvature assumption
        kappa_target = chi_kappa * grad_I_s * L

        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        distributed_load = rho * A_cross * g

        # IEC model
        theta_IEC, kappa_IEC = solve_beam_static(
            s=s, kappa_target=kappa_target, E_field=E_field, M_active=M_active,
            I_moment=I_moment, P_load=0.0, distributed_load=distributed_load
        )

        # Passive model
        theta_passive, kappa_passive = solve_beam_static(
            s=s, kappa_target=np.zeros_like(s), E_field=E_field, M_active=M_active,
            I_moment=I_moment, P_load=0.0, distributed_load=distributed_load
        )

        P_counter = eta_a * rho * A_cross * g * (L**2) * np.mean((kappa_IEC - kappa_passive)**2)

        # Approximations for placeholders
        Cobb_angle = np.rad2deg(np.max(theta_IEC) - np.min(theta_IEC))
        D_geo = float(np.sqrt(np.mean((kappa_IEC - kappa_passive)**2))) * L

        return P_counter, Cobb_angle, D_geo

    # First compute S_0 at L_0 = 0.35
    L_0 = 0.35
    S_0, _, _ = compute_P_counter(L_0)

    for L in L_vals:
        P_counter, Cobb_angle, D_geo = compute_P_counter(L)

        # Proprioceptive supply
        S_proprio_alpha05 = S_0 * (L / L_0)**0.5
        S_proprio_alpha10 = S_0 * (L / L_0)**1.0

        results.append({
            'L': L,
            'P_counter': P_counter,
            'S_proprio_alpha05': S_proprio_alpha05,
            'S_proprio_alpha10': S_proprio_alpha10,
            'Cobb_angle': Cobb_angle,
            'D_geo': D_geo
        })

    df = pd.DataFrame(results)
    df.to_csv('outputs/thermodynamic_cost/energy_deficit_window.csv', index=False)

    # Generate Figure
    plt.figure(figsize=(8, 6))
    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label='$P_{\\mathrm{counter}}$ ($L^2$ scaling)')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label='$S_{\\mathrm{proprio}}$ ($\\alpha=0.5$)')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'c--', linewidth=2, label='$S_{\\mathrm{proprio}}$ ($\\alpha=1.0$)')

    # Shade Energy Deficit Window for alpha=0.5
    # Find intersection index
    deficit_mask = df['P_counter'] > df['S_proprio_alpha05']
    if deficit_mask.any():
        L_crit_idx = deficit_mask.idxmax()
        L_crit = df.loc[L_crit_idx, 'L']
        plt.fill_between(df['L'], df['S_proprio_alpha05'], df['P_counter'], where=deficit_mask,
                         color='red', alpha=0.2, label=f'Energy Deficit Window ($L > {L_crit:.2f}$ m)')

    plt.axvline(L_0, color='gray', linestyle=':', label='$L_0 = 0.35$ m')
    plt.xlabel('Spinal Length $L$ (m)')
    plt.ylabel('Metabolic Power / Supply (normalized)')
    plt.title('The Energy Deficit Window')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/figures/energy_deficit_window.png', dpi=300)
    plt.savefig('figures/main/energy_deficit_window.png', dpi=300)
    print("Results saved to outputs/thermodynamic_cost/energy_deficit_window.csv")
    print("Figures saved to outputs/figures/energy_deficit_window.png and figures/main/energy_deficit_window.png")

if __name__ == "__main__":
    main()
