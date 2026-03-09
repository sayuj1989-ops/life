#!/usr/bin/env python3
import sys; import os; sys.path.insert(0, os.path.abspath('.'))
"""
Simulate P_counter(L) scaling and identify the Energy Deficit Window.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.spinalmodes.iec import IECParameters, solve_beam_static, apply_iec_coupling

def run_simulation():
    # Length sweep
    L_steps = 30
    L_array = np.linspace(0.25, 0.55, L_steps)

    # Parameters
    E0 = 1.0e9  # 1.0 GPa
    rho = 1100.0  # kg/m^3
    A = 0.001  # m^2
    g = 9.81  # m/s^2
    eta_a = 1.0  # normalized units

    # Baseline information field parameters
    I_amplitude = 1.0

    # Storage
    results = []

    # Reference L0 for proprioceptive supply
    L0 = 0.35
    S0 = None

    # First pass: find S0 at L0
    # To do this cleanly, we just find the P_counter at L0 directly.
    # We will interpolate or compute it exactly.
    def compute_P_counter(L):
        # Setup parameters
        params = IECParameters(
            chi_kappa=0.05,
            E0=E0,
            C0=1e6, # default
            length=L,
            n_nodes=100
        )

        # We need a custom bimodal gaussian I(s) as per methods.tex
        # I(s) = A_c exp(...) + A_l exp(...) + I_0
        s = params.s_array
        s_norm = s / L
        A_c, s_c, sigma_c = 0.5, 0.80, 0.08
        A_l, s_l, sigma_l = 0.7, 0.25, 0.10
        I_0 = 0.3

        I_field = (A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2)) +
                   A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2)) + I_0)

        # IEC-1: grad_I
        # To maintain the "fixed-curvature assumption" where target curvature
        # is independent of L, we multiply by L to cancel out the 1/L factor from the spatial gradient of s_norm.
        grad_I = np.gradient(I_field, s)
        kappa_target = params.chi_kappa * grad_I * L

        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        I_moment = A**2 / 12.0 # approx for square
        # wait, the methods say: EI / MgL^2. E0=1GPa, A=0.001. Let's use I_moment = 1e-8
        I_moment = 1e-8

        # distributed load = rho * A * g
        w = rho * A * g

        # Active case: chi_kappa = 0.05
        theta_iec, kappa_iec = solve_beam_static(
            s=s,
            kappa_target=kappa_target,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=w
        )

        # Passive case: chi_kappa = 0.0
        theta_pas, kappa_pas = solve_beam_static(
            s=s,
            kappa_target=np.zeros_like(s),
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=w
        )

        # P_counter
        mean_sq_diff = np.mean((kappa_iec - kappa_pas)**2)
        P_count = eta_a * rho * A * g * (L**2) * mean_sq_diff

        # Cobb angle approx
        cobb = np.degrees(np.max(theta_iec) - np.min(theta_iec))

        # D_geo approx: normalized area between curves
        d_geo = np.mean(np.abs(theta_iec - theta_pas))

        return P_count, cobb, d_geo

    # Compute P_counter for all L
    P_counters = []
    cobbs = []
    d_geos = []

    for L in L_array:
        P_count, cobb, d_geo = compute_P_counter(L)
        P_counters.append(P_count)
        cobbs.append(cobb)
        d_geos.append(d_geo)

        if np.isclose(L, L0, atol=1e-3) or (L > L0 and S0 is None):
            S0 = P_count
            if S0 == 0:
                S0 = 1e-6 # prevent div by zero

    # If S0 is still None, interpolate
    if S0 is None:
        S0 = np.interp(L0, L_array, P_counters)

    for L, P_count, cobb, d_geo in zip(L_array, P_counters, cobbs, d_geos):
        S_proprio_alpha05 = S0 * (L / L0)**0.5
        S_proprio_alpha10 = S0 * (L / L0)**1.0

        results.append({
            'L': L,
            'P_counter': P_count,
            'S_proprio_alpha05': S_proprio_alpha05,
            'S_proprio_alpha10': S_proprio_alpha10,
            'Cobb_angle': cobb,
            'D_geo': d_geo
        })

    df = pd.DataFrame(results)

    # Save CSV
    os.makedirs('outputs/thermodynamic_cost', exist_ok=True)
    df.to_csv('outputs/thermodynamic_cost/energy_deficit_window.csv', index=False)
    print("Saved outputs/thermodynamic_cost/energy_deficit_window.csv")

    # Plot
    os.makedirs('outputs/figures', exist_ok=True)
    plt.figure(figsize=(8, 6))

    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label='$P_{counter}$ (Demand)')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label='$S_{proprio}$ (Supply, $\\alpha=0.5$)')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'b:', linewidth=2, label='$S_{proprio}$ (Supply, $\\alpha=1.0$)')

    # Shaded region for alpha=0.5
    # Find crossings
    diff = df['P_counter'] - df['S_proprio_alpha05']
    crossings = np.where(np.diff(np.sign(diff)))[0]

    # Fill between crossings (or after first crossing)
    if len(crossings) > 0:
        idx_start = crossings[0]
        idx_end = len(df) - 1
        plt.fill_between(df['L'][idx_start:idx_end+1],
                         df['S_proprio_alpha05'][idx_start:idx_end+1],
                         df['P_counter'][idx_start:idx_end+1],
                         color='red', alpha=0.2, label='Energy Deficit Window')

        plt.axvline(df['L'].iloc[idx_start], color='k', linestyle='--', alpha=0.5)
        plt.text(df['L'].iloc[idx_start] + 0.01, df['P_counter'].iloc[idx_start],
                 f'$L_{{crit}} \\approx {df["L"].iloc[idx_start]:.2f}$ m',
                 verticalalignment='bottom')

    plt.xlabel('Spinal Length $L$ (m)', fontsize=12)
    plt.ylabel('Metabolic Power (Normalized)', fontsize=12)
    plt.title('The Energy Deficit Window', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig('outputs/figures/energy_deficit_window.png', dpi=300)
    print("Saved outputs/figures/energy_deficit_window.png")

if __name__ == '__main__':
    run_simulation()
