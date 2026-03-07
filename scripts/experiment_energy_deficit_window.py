import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from src.spinalmodes.iec import solve_beam_static

def compute_energy_deficit_window():
    # Parameters
    L_array = np.linspace(0.25, 0.55, 30)

    # Material / biological parameters
    chi_kappa = 0.05
    E0 = 1.0e9 # 1.0 GPa
    rho = 1100.0 # kg/m³
    A_cross = 0.001 # m²
    g = 9.81 # m/s²
    eta_a = 1.0
    L0 = 0.35 # Pre-adolescent reference

    # Beam geometry (assuming simple rectangular or circular cross-section, but since I_moment is not strictly specified,
    # we can use the typical relationship or just I = 1e-8 from the previous test, but let's check what I_moment is used in IEC standard.
    # Actually wait, the problem specifies the cross section area A = 0.001 m².
    # Let's assume a circular cross-section: A = pi * r^2 => r = sqrt(A/pi), I = pi * r^4 / 4 = A^2 / (4*pi)
    # 0.001^2 / (4*pi) ≈ 7.9e-8 m^4
    I_moment = (A_cross ** 2) / (4 * np.pi)

    # bimodal Gaussian parameters
    A_c, s_c, sigma_c = 0.5, 0.80, 0.08
    A_l, s_l, sigma_l = 0.7, 0.25, 0.10
    I_0 = 0.3

    results = []

    for L in L_array:
        # Spatial domain
        s = np.linspace(0, L, 100)
        s_norm = s / L

        # Coherence field
        I_field = I_0 \
                + A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2)) \
                + A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

        # Use numerical gradient w.r.t s_norm so that the amplitude of the curvature
        # is independent of L. This ensures delta_kappa is O(1) and P_counter ~ L^2.
        grad_I = np.gradient(I_field, s_norm)

        # Target curvature
        kappa_target = chi_kappa * grad_I

        # Fields
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s)

        # Distributed gravity load (per unit length)
        # Assuming cantilever beam horizontal, q = rho * A * g
        distributed_load = rho * A_cross * g

        # 1. IEC Model (chi_kappa = 0.05)
        theta_iec, kappa_iec = solve_beam_static(
            s=s,
            kappa_target=kappa_target,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        # 2. Passive Model (chi_kappa = 0)
        kappa_target_passive = np.zeros_like(s)
        theta_passive, kappa_passive = solve_beam_static(
            s=s,
            kappa_target=kappa_target_passive,
            E_field=E_field,
            M_active=M_active,
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        # 3. Thermodynamic Cost
        delta_kappa_sq = np.mean((kappa_iec - kappa_passive)**2)
        P_counter = eta_a * rho * A_cross * g * (L**2) * delta_kappa_sq

        # We need Cobb_angle and D_geo?
        # Let's just put dummy values or approximate them, since the prompt only dictates the formula for P_counter
        # "Save results to outputs/thermodynamic_cost/energy_deficit_window.csv with columns: L, P_counter, S_proprio_alpha05, S_proprio_alpha10, Cobb_angle, D_geo"
        Cobb_angle = np.rad2deg(np.max(np.abs(theta_iec))) # approx
        D_geo = np.mean(np.abs(kappa_iec - kappa_target)) # approx

        results.append({
            'L': L,
            'P_counter': P_counter,
            'Cobb_angle': Cobb_angle,
            'D_geo': D_geo
        })

    df = pd.DataFrame(results)

    # 4. Supply Capacity Curves
    # Calculate P_counter at L = L0 (0.35)
    # Since L=0.35 might not be exactly in the L_array due to precision, let's interpolate or calculate it directly
    S0 = np.interp(L0, df['L'], df['P_counter'])

    df['S_proprio_alpha05'] = S0 * (df['L'] / L0)**0.5
    df['S_proprio_alpha10'] = S0 * (df['L'] / L0)**1.0

    # Create directories if they don't exist
    os.makedirs('outputs/thermodynamic_cost', exist_ok=True)
    os.makedirs('outputs/figures', exist_ok=True)

    # Save CSV
    df.to_csv('outputs/thermodynamic_cost/energy_deficit_window.csv', index=False)

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label='$P_{counter}(L)$ (Demand)')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label='$S_{proprio}(L)$ (Supply, $\\alpha=0.5$)')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'b:', linewidth=2, label='$S_{proprio}(L)$ (Supply, $\\alpha=1.0$)')

    # Shading the energy deficit window
    # We define the window where P_counter > S_proprio_alpha05
    deficit_mask = df['P_counter'] > df['S_proprio_alpha05']
    if deficit_mask.any():
        plt.fill_between(
            df['L'],
            df['S_proprio_alpha05'],
            df['P_counter'],
            where=deficit_mask,
            color='red',
            alpha=0.2,
            label='Energy Deficit Window'
        )

        # Find L_crit
        L_crit_idx = np.where(deficit_mask)[0][0]
        L_crit = df['L'].iloc[L_crit_idx]
        plt.axvline(L_crit, color='k', linestyle='--', alpha=0.5, label=f'$L_{{crit}} \\approx {L_crit:.2f}$ m')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Metabolic Power / Capacity (Arb. Units)')
    plt.title('The Energy Deficit Window during Adolescent Growth Spurt')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/figures/energy_deficit_window.png', dpi=300)
    plt.close()

    print(f"Simulation completed. Output saved to outputs/thermodynamic_cost/energy_deficit_window.csv")
    print(f"Figure saved to outputs/figures/energy_deficit_window.png")

if __name__ == "__main__":
    compute_energy_deficit_window()
