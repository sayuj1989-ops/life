import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from src.spinalmodes.iec import solve_beam_static

def run_experiment():
    # Parameters
    chi_kappa = 0.05
    E0 = 1.0e9
    rho = 1100.0
    A = 0.001
    g = 9.81
    eta_a = 1.0
    I_moment = 1e-8

    # Information field parameters
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08
    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10
    I_0 = 0.3

    L_vals = np.linspace(0.25, 0.55, 30)
    results = []

    for L in L_vals:
        s = np.linspace(0, L, 100)
        s_norm = s / L

        # Information field
        I_field = (A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2)) +
                   A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2)) +
                   I_0)

        grad_I = np.gradient(I_field, s)
        kappa_target = chi_kappa * grad_I * L

        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        dist_load = rho * A * g

        # Using exact arguments of solve_beam_static:
        # solve_beam_static(s, kappa_target, E_field, M_active, I_moment=1e-8, P_load=100.0, distributed_load=0.0)
        theta_IEC, kappa_IEC = solve_beam_static(s, kappa_target, E_field, M_active, I_moment=I_moment, P_load=0.0, distributed_load=dist_load)
        theta_pass, kappa_pass = solve_beam_static(s, np.zeros_like(s), E_field, M_active, I_moment=I_moment, P_load=0.0, distributed_load=dist_load)

        # P_counter
        mean_diff_sq = np.mean((kappa_IEC - kappa_pass)**2)
        P_counter = eta_a * rho * A * g * (L**2) * mean_diff_sq

        # D_geo (geodesic deviation proxy)
        D_geo = np.sqrt(mean_diff_sq)

        # Cobb angle approx
        cobb = np.rad2deg(np.max(np.abs(theta_IEC)) - np.min(np.abs(theta_IEC)))

        results.append({
            'L': L,
            'P_counter': P_counter,
            'Cobb_angle': cobb,
            'D_geo': D_geo
        })

    df = pd.DataFrame(results)

    # Proprioceptive supply capacity
    L_0 = 0.35
    S_0 = df.loc[np.abs(df['L'] - L_0).idxmin(), 'P_counter']

    df['S_proprio_alpha05'] = S_0 * (df['L'] / L_0)**0.5
    df['S_proprio_alpha10'] = S_0 * (df['L'] / L_0)**1.0

    os.makedirs('outputs/thermodynamic_cost', exist_ok=True)
    df.to_csv('outputs/thermodynamic_cost/energy_deficit_window.csv', index=False)

    # Plot
    os.makedirs('outputs/figures', exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label='$P_{counter}$ (Demand)')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label='$S_{proprio}$ (Supply, $\\alpha=0.5$)')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'c--', linewidth=2, label='$S_{proprio}$ (Supply, $\\alpha=1.0$)')

    from scipy.interpolate import interp1d
    f_diff = interp1d(df['L'], df['P_counter'] - df['S_proprio_alpha05'])
    L_dense = np.linspace(0.25, 0.55, 1000)
    diffs = f_diff(L_dense)
    crossings = L_dense[np.where(np.diff(np.sign(diffs)))[0]]
    if len(crossings) > 0:
        L_crit = crossings[0]
        plt.axvline(L_crit, color='k', linestyle=':', label=f'$L_{{crit}}$ $\\approx$ {L_crit:.2f} m')
        plt.fill_between(df['L'], df['S_proprio_alpha05'], df['P_counter'],
                         where=(df['L'] > L_crit), color='red', alpha=0.2, label='Energy Deficit Window')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Metabolic Power (normalized)')
    plt.title('The Energy Deficit Window')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('outputs/figures/energy_deficit_window.png')
    plt.close()

if __name__ == '__main__':
    run_experiment()
