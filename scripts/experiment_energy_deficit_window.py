import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from spinalmodes.iec import compute_gradient, solve_beam_static

def generate_bimodal_coherence_field(s: np.ndarray, L: float) -> np.ndarray:
    """Generate bimodal Gaussian information field as specified in methods.tex."""
    s_norm = s / L

    A_c, s_c, sigma_c = 0.5, 0.80, 0.08
    A_l, s_l, sigma_l = 0.7, 0.25, 0.10
    I_0 = 0.3

    I_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    I_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return I_c + I_l + I_0

def get_coupled_fields(s: np.ndarray, L: float, chi_kappa: float, E0: float):
    I_field = generate_bimodal_coherence_field(s, L)
    s_norm = s / L
    grad_I = np.gradient(I_field, s_norm)

    # IEC-1: Target curvature bias
    kappa_target = chi_kappa * grad_I

    # IEC-2: Constitutive bias
    E_field = np.full_like(s, E0)

    # IEC-3: Active moment
    M_active = np.zeros_like(s)

    return kappa_target, E_field, M_active

def generate_figure(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 6))

    L = df['L']
    P_counter = df['P_counter']
    S_alpha05 = df['S_proprio_alpha05']
    S_alpha10 = df['S_proprio_alpha10']

    ax.plot(L, P_counter, 'r-', linewidth=2.5, label=r'Metabolic Demand $P_{counter} \sim L^2$')
    ax.plot(L, S_alpha05, 'b--', linewidth=2.0, label=r'Supply $S_{proprio} \sim L^{0.5}$ (Sublinear)')
    ax.plot(L, S_alpha10, 'g:', linewidth=2.0, label=r'Supply $S_{proprio} \sim L^{1.0}$ (Linear)')

    deficit_mask = P_counter > S_alpha05
    if deficit_mask.any():
        ax.fill_between(L, S_alpha05, P_counter, where=deficit_mask,
                        color='red', alpha=0.2, hatch='//', label='Energy Deficit Window')

        L_crit_idx = np.where(deficit_mask)[0][0]
        idx_before = L_crit_idx - 1

        if idx_before >= 0:
            L1, L2 = L.iloc[idx_before], L.iloc[L_crit_idx]
            P1, P2 = P_counter.iloc[idx_before], P_counter.iloc[L_crit_idx]
            S1, S2 = S_alpha05.iloc[idx_before], S_alpha05.iloc[L_crit_idx]

            dP = P2 - P1
            dS = S2 - S1
            L_crit = L1 + (S1 - P1) * (L2 - L1) / (dP - dS)
        else:
            L_crit = L.iloc[L_crit_idx]

        ax.axvline(x=L_crit, color='k', linestyle='-.', alpha=0.6, label=f"$L_{{crit}} \\approx {L_crit:.2f}$ m")

    ax.set_xlabel('Spinal Length $L$ (m)', fontsize=12)
    ax.set_ylabel('Normalized Metabolic Power', fontsize=12)
    ax.set_title('Thermodynamic Collapse: The Energy Deficit Window', fontsize=14)
    ax.legend(fontsize=10, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.6)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    os.makedirs('outputs/figures', exist_ok=True)
    plt.tight_layout()
    fig.savefig('outputs/figures/energy_deficit_window.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Figure saved to outputs/figures/energy_deficit_window.png")

def main():
    L_vals = np.linspace(0.25, 0.55, 30)

    chi_kappa = 0.05
    E0 = 1.0e9      # Pa
    rho = 1100.0    # kg/m^3
    A = 0.001       # m^2
    eta_a = 1.0
    g = 9.81

    L_0 = 0.35

    # 1. First pass to find P_counter for all L to find S_0 = P_counter(L_0)
    P_counter_vals = []

    for L in L_vals:
        n_nodes = 100
        s = np.linspace(0, L, n_nodes)

        kappa_target_iec, E_field_iec, M_active_iec = get_coupled_fields(s, L, chi_kappa, E0)

        w = rho * A * g
        I_moment = 1e-8

        theta_iec, kappa_iec = solve_beam_static(
            s=s, kappa_target=kappa_target_iec, E_field=E_field_iec,
            M_active=M_active_iec, I_moment=I_moment, P_load=0.0, distributed_load=w
        )

        kappa_target_passive = np.zeros_like(s)
        theta_passive, kappa_passive = solve_beam_static(
            s=s, kappa_target=kappa_target_passive, E_field=E_field_iec,
            M_active=np.zeros_like(s), I_moment=I_moment, P_load=0.0, distributed_load=w
        )

        mean_sq_diff = np.mean((kappa_iec - kappa_passive)**2)
        P_counter = eta_a * rho * A * g * (L**2) * mean_sq_diff
        P_counter_vals.append(P_counter)

    P_counter_vals = np.array(P_counter_vals)
    S_0 = np.interp(L_0, L_vals, P_counter_vals)

    # 2. Second pass to save all stats to df
    results = []
    for i, L in enumerate(L_vals):
        P_counter = P_counter_vals[i]

        S_proprio_alpha05 = S_0 * (L / L_0)**0.5
        S_proprio_alpha10 = S_0 * (L / L_0)**1.0

        s = np.linspace(0, L, 100)
        kappa_target_iec, E_field_iec, M_active_iec = get_coupled_fields(s, L, chi_kappa, E0)
        w = rho * A * g
        theta_iec, kappa_iec = solve_beam_static(s, kappa_target_iec, E_field_iec, M_active_iec, I_moment=1e-8, P_load=0.0, distributed_load=w)
        kappa_target_passive = np.zeros_like(s)
        theta_passive, kappa_passive = solve_beam_static(s, kappa_target_passive, E_field_iec, M_active_iec, I_moment=1e-8, P_load=0.0, distributed_load=w)

        cobb_angle = np.degrees(np.max(theta_iec) - np.min(theta_iec))
        D_geo = np.sqrt(np.mean((theta_iec - theta_passive)**2))

        results.append({
            'L': L,
            'P_counter': P_counter,
            'S_proprio_alpha05': S_proprio_alpha05,
            'S_proprio_alpha10': S_proprio_alpha10,
            'Cobb_angle': cobb_angle,
            'D_geo': D_geo
        })

    df = pd.DataFrame(results)

    os.makedirs('outputs/thermodynamic_cost', exist_ok=True)
    df.to_csv('outputs/thermodynamic_cost/energy_deficit_window.csv', index=False)
    print("CSV saved to outputs/thermodynamic_cost/energy_deficit_window.csv")

    generate_figure(df)

if __name__ == "__main__":
    main()
