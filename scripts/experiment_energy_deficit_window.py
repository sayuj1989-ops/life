
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Add source directory to path
sys.path.append(os.path.abspath("src"))

try:
    from spinalmodes.iec import solve_beam_static, IECParameters
except ImportError:
    # If src is not in pythonpath, try to add it relatively
    sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
    from spinalmodes.iec import solve_beam_static, IECParameters

def generate_bimodal_gaussian_field(s, L, params):
    """
    Generate bimodal gaussian field I(s) and its gradient.
    params: dict with A_c, s_c, sigma_c, A_l, s_l, sigma_l, I_0
    """
    xi = s / L

    # Cervical bump
    term_c = params['A_c'] * np.exp(-((xi - params['s_c'])**2) / (2 * params['sigma_c']**2))
    grad_c = term_c * (- (xi - params['s_c']) / (params['sigma_c']**2)) * (1/L)

    # Lumbar bump
    term_l = params['A_l'] * np.exp(-((xi - params['s_l'])**2) / (2 * params['sigma_l']**2))
    grad_l = term_l * (- (xi - params['s_l']) / (params['sigma_l']**2)) * (1/L)

    I_field = term_c + term_l + params['I_0']
    grad_I = grad_c + grad_l

    return I_field, grad_I

def run_experiment():
    # Parameters
    # Standard IEC parameters from methods
    chi_kappa_iec = 0.05
    E0 = 1.0e9 # 1 GPa
    rho = 1100.0 # kg/m^3
    g = 9.81 # m/s^2
    eta_a = 1.0 # normalized units

    # Isometric Growth Parameters
    # Assume A=0.001 at L=0.4m (standard adult/adolescent length)
    L_ref = 0.4
    A_ref = 0.001

    # Field parameters
    field_params = {
        'A_c': 0.5, 's_c': 0.80, 'sigma_c': 0.08,
        'A_l': 0.7, 's_l': 0.25, 'sigma_l': 0.10,
        'I_0': 0.3
    }

    # Parameter sweep L
    L_values = np.linspace(0.25, 0.55, 30)

    results = []

    for L in L_values:
        s = np.linspace(0, L, 100)

        # Isometric Scaling of Cross-Section
        # A(L) ~ L^2
        A_L = A_ref * (L / L_ref)**2

        # Moment of Inertia for circular cross-section
        # I = pi * r^4 / 4
        # A = pi * r^2 => r^2 = A/pi => r^4 = A^2/pi^2
        # I = pi * (A^2/pi^2) / 4 = A^2 / (4*pi)
        I_moment_L = (A_L**2) / (4 * np.pi)

        # Distributed load (weight per unit length)
        # Note: solve_beam_static uses distributed_load (N/m).
        distributed_load = rho * A_L * g

        # 1. Compute IEC state (chi_kappa = 0.05)
        I_field, grad_I = generate_bimodal_gaussian_field(s, L, field_params)
        kappa_target_iec = chi_kappa_iec * grad_I

        # Assume E_field is constant E0
        E_field = np.full_like(s, E0)
        M_active = np.zeros_like(s) # No active moment specified

        theta_iec, kappa_iec = solve_beam_static(
            s, kappa_target_iec, E_field, M_active,
            I_moment=I_moment_L, P_load=0, distributed_load=distributed_load
        )

        # 2. Compute Passive state (chi_kappa = 0.0 -> kappa_target = 0)
        kappa_target_passive = np.zeros_like(s)

        theta_passive, kappa_passive = solve_beam_static(
            s, kappa_target_passive, E_field, M_active,
            I_moment=I_moment_L, P_load=0, distributed_load=distributed_load
        )

        # 3. Compute P_counter
        # P_counter ~ eta_a * rho * A * g * L^2 * <|kappa_IEC - kappa_passive|^2>
        # mean over s
        kappa_diff_sq = (kappa_iec - kappa_passive)**2
        mean_kappa_diff_sq = np.mean(kappa_diff_sq)

        P_counter = eta_a * rho * A_L * g * (L**2) * mean_kappa_diff_sq

        # Compute Cobb angle (amplitude of theta_iec in degrees)
        cobb_angle = np.rad2deg(np.max(theta_iec) - np.min(theta_iec))

        d_geo = np.sqrt(np.mean((theta_iec - theta_passive)**2))

        results.append({
            'L': L,
            'P_counter': P_counter,
            'Cobb_angle': cobb_angle,
            'D_geo': d_geo
        })

    df = pd.DataFrame(results)

    # 4. Compute Proprioceptive Supply S_proprio(L)
    # S_proprio(L) = S_0 * (L / L_0)^alpha
    # L_0 = 0.35 m (pre-adolescent reference)
    # S_0 = P_counter(L_0)

    # Interpolate P_counter at L_0
    L0 = 0.35
    P_at_L0 = np.interp(L0, df['L'], df['P_counter'])

    df['S_proprio_alpha05'] = P_at_L0 * (df['L'] / L0)**0.5
    df['S_proprio_alpha10'] = P_at_L0 * (df['L'] / L0)**1.0

    # Check scaling of P_counter
    # Fit P = k * L^beta
    log_L = np.log(df['L'])
    log_P = np.log(df['P_counter'])
    coeffs = np.polyfit(log_L, log_P, 1)
    scaling_exponent = coeffs[0]
    print(f"P_counter scaling exponent (isometric): {scaling_exponent:.4f}")

    # Check deficit at L=0.45
    P_45 = np.interp(0.45, df['L'], df['P_counter'])
    S_45 = np.interp(0.45, df['L'], df['S_proprio_alpha05'])
    deficit_pct = (P_45 - S_45) / S_45 * 100
    print(f"At L=0.45 m: P={P_45:.4f}, S={S_45:.4f}, Deficit={deficit_pct:.2f}%")

    # Find intersection L_crit
    # We expect P < S at small L, and P > S at large L
    # Find where P crosses S
    # Since we calibrated S at L0, they cross at L0.
    # If P grows faster than S, then for L > L0, P > S (Deficit).

    # Save CSV
    os.makedirs("outputs/thermodynamic_cost", exist_ok=True)
    df.to_csv("outputs/thermodynamic_cost/energy_deficit_window.csv", index=False)
    print("Saved CSV to outputs/thermodynamic_cost/energy_deficit_window.csv")

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label=r'$P_{counter}$ (Isometric Growth)')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label=r'$S_{proprio} (\alpha=0.5)$')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'g:', linewidth=1.5, label=r'$S_{proprio} (\alpha=1.0)$')

    # Fill between P and S (alpha=0.5) for L > L0
    # Assuming P > S for L > L0
    idx = df['L'] >= L0
    plt.fill_between(df['L'][idx], df['P_counter'][idx], df['S_proprio_alpha05'][idx],
                     color='red', alpha=0.1, label='Energy Deficit Window')

    plt.axvline(x=L0, color='k', linestyle=':', label=f'$L_{{crit}} = {L0} m$')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Thermodynamic Cost (normalized)')
    plt.title('Energy Deficit Window (Isometric Scaling)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    os.makedirs("outputs/figures", exist_ok=True)
    plt.savefig("outputs/figures/energy_deficit_window.png", dpi=300)
    print("Saved plot to outputs/figures/energy_deficit_window.png")

if __name__ == "__main__":
    run_experiment()
