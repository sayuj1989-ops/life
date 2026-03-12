import os
import sys
# Ensure src is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from typing import Tuple
from numpy.typing import NDArray

from src.spinalmodes.iec import solve_beam_static, compute_amplitude

def generate_bimodal_gaussian_field(s_norm: NDArray[np.float64]) -> NDArray[np.float64]:
    """Generate bimodal Gaussian coherence field based on manuscript parameters."""
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08
    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10
    I_0 = 0.3

    # Cervical/Thoracic bump
    c_bump = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    # Lumbar bump
    l_bump = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return I_0 + c_bump + l_bump

def compute_energy_deficit_window():
    # Setup directories
    os.makedirs('outputs/thermodynamic_cost', exist_ok=True)
    os.makedirs('outputs/figures', exist_ok=True)

    # Standard IEC parameters from methods
    chi_kappa = 0.05
    E0 = 1.0e9  # 1.0 GPa
    rho = 1100.0  # kg/m^3
    A_area = 0.001  # m^2
    g = 9.81
    eta_a = 1.0

    # Inertia approximation for a circular cross section
    r = np.sqrt(A_area / np.pi)
    I_moment = (np.pi / 4) * (r**4)

    # Distributed load from gravity
    q_gravity = rho * A_area * g

    # Length sweep
    L_array = np.linspace(0.25, 0.55, 30)

    # Proprioceptive supply calibration
    L_0 = 0.35

    results = []

    for L in L_array:
        n_nodes = max(100, int(L * 1000))
        s = np.linspace(0, L, n_nodes)
        s_norm = s / L

        # Coherence field and gradient
        I_field = generate_bimodal_gaussian_field(s_norm)
        grad_I = np.gradient(I_field, s)

        # IEC-1 target curvature (maintain fixed-curvature scaling: kappa_target = chi_kappa * grad_I * L)
        kappa_target = chi_kappa * grad_I * L

        # E_field is constant E0 (as per chi_E=0 by default)
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        # Solve full IEC model
        theta_iec, kappa_iec = solve_beam_static(
            s=s,
            kappa_target=kappa_target,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=q_gravity
        )

        # Solve passive model (chi_kappa = 0)
        kappa_target_passive = np.zeros_like(s)
        theta_pass, kappa_pass = solve_beam_static(
            s=s,
            kappa_target=kappa_target_passive,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=q_gravity
        )

        # Calculate P_counter
        # P_counter = eta_a * rho * A * g * L^2 * mean(|kappa_IEC - kappa_passive|^2)
        mean_diff_sq = np.mean((np.abs(kappa_iec - kappa_pass))**2)
        P_counter = eta_a * rho * A_area * g * (L**2) * mean_diff_sq

        # Calculate true geometry metrics
        cobb_angle = compute_amplitude(theta_iec)
        d_geo = np.mean((kappa_iec - kappa_target)**2)

        results.append({
            'L': L,
            'P_counter': P_counter,
            'Cobb_angle': cobb_angle,
            'D_geo': d_geo
        })

    df = pd.DataFrame(results)

    # Find P_counter at L_0 by interpolation
    S_0 = np.interp(L_0, df['L'], df['P_counter'])

    df['S_proprio_alpha05'] = S_0 * (df['L'] / L_0)**0.5
    df['S_proprio_alpha10'] = S_0 * (df['L'] / L_0)**1.0

    # Determine exact L_crit for alpha=0.5
    # First drop lengths below L_0 to ensure we catch the crossing in the adolescent range
    df_upper = df[df['L'] >= L_0].copy()
    idx_crit = np.where(df_upper['P_counter'] > df_upper['S_proprio_alpha05'])[0]

    if len(idx_crit) > 0:
        L_crit = df_upper['L'].iloc[idx_crit[0]]
    else:
        L_crit = np.nan

    print(f"L_crit (alpha=0.5): {L_crit:.3f} m")

    # Save CSV
    df.to_csv('outputs/thermodynamic_cost/energy_deficit_window.csv', index=False)

    # Plotting
    plt.figure(figsize=(8, 6))

    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label=r'$P_{\mathrm{counter}}$ (Demand, $\propto L^2$)')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label=r'$S_{\mathrm{proprio}}$ (Supply, $\propto L^{0.5}$)')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'b:', linewidth=1.5, label=r'$S_{\mathrm{proprio}}$ (Supply, $\propto L^{1.0}$)')

    # Shaded region for energy deficit (P_counter > S_proprio_alpha05)
    plt.fill_between(df['L'], df['S_proprio_alpha05'], df['P_counter'],
                     where=(df['P_counter'] > df['S_proprio_alpha05']),
                     color='red', alpha=0.2, label='Energy Deficit Window')

    plt.axvline(x=L_0, color='gray', linestyle='-.', alpha=0.7, label=rf'$L_{{\mathrm{{crit}}}} = {L_0:.2f}$ m')

    plt.title('The Energy Deficit Window', fontsize=14)
    plt.xlabel('Spinal Length $L$ (m)', fontsize=12)
    plt.ylabel('Metabolic Power / Supply Capacity (a.u.)', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig('outputs/figures/energy_deficit_window.png', dpi=300)
    plt.close()

    print(f"Results saved to outputs/thermodynamic_cost/energy_deficit_window.csv")
    print(f"Figure saved to outputs/figures/energy_deficit_window.png")

if __name__ == "__main__":
    compute_energy_deficit_window()
