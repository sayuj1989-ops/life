"""
Experiment: Energy Deficit Window Simulation

This script simulates the thermodynamic cost of counter-curvature (P_counter)
as a function of spinal length (L) using the IEC beam solver.

It compares P_counter against a hypothetical proprioceptive supply capacity (S_proprio)
that scales sublinearly with length. The crossover point defines the "Energy Deficit Window"
during early development.

Outputs:
- outputs/thermodynamic_cost/energy_deficit_window.csv: Simulation data
- outputs/figures/energy_deficit_window.png: Figure visualizing the deficit window

Reference: Manuscript Section 4.6
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Add src to python path to import spinalmodes
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    # If not found, try adding just 'src' assuming run from root
    sys.path.append('src')
    from spinalmodes.iec import solve_beam_static

def generate_bimodal_gaussian_field(s, L):
    """
    Generate the bimodal Gaussian information field I(s).
    Formula from manuscript/sections/methods.tex:
    I(s) = A_c * exp(-((s/L - s_c)^2)/(2*sigma_c^2)) +
           A_l * exp(-((s/L - s_l)^2)/(2*sigma_l^2)) + I_0
    """
    # Avoid division by zero
    if L == 0:
        return np.full_like(s, 0.3)

    s_norm = s / L

    # Parameters from prompt
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08

    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10

    I_0 = 0.3

    # Calculate components
    term_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    term_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return term_c + term_l + I_0

def run_simulation():
    print("Starting Energy Deficit Window simulation...")

    # Parameters
    L_start = 0.25
    L_end = 0.55
    n_steps = 30
    L_values = np.linspace(L_start, L_end, n_steps)

    # IEC parameters
    chi_kappa = 0.05
    chi_E = 0.10 # Standard parameter mentioned in table
    # chi_f = 0.0 # Active moment implicitly 0 in solve_beam_static if M_active=0

    # Material / Geometric parameters
    E0 = 1.0e9 # Pa
    rho = 1100.0 # kg/m^3
    A_ref = 0.001 # m^2 at L_ref
    L_ref_geom = 0.4 # Reference length for geometric scaling
    g = 9.81 # m/s^2

    eta_a = 1.0 # Scaling factor for P_counter

    results = []

    for L in L_values:
        # Isometric scaling: Cross-sectional area scales as L^2
        # This implies geometric similarity (thickness proportional to length)
        A = A_ref * (L / L_ref_geom)**2
        I_moment = A**2 / (4 * np.pi) # m^4 (circular approx from A)
        # Spatial grid
        n_nodes = 100
        s = np.linspace(0, L, n_nodes)

        # Information field
        I_field = generate_bimodal_gaussian_field(s, L)

        # Gradient of I (finite difference)
        grad_I = np.gradient(I_field, s)

        # Stiffness field
        E_field = E0 * (1.0 + chi_E * I_field)

        # Distributed load (gravity transverse)
        distributed_load = rho * A * g

        # 1. IEC Case: Active target curvature
        kappa_target_iec = chi_kappa * grad_I
        theta_iec, kappa_iec = solve_beam_static(
            s=s,
            kappa_target=kappa_target_iec,
            E_field=E_field,
            M_active=np.zeros_like(s), # Assuming no active moment for this simplified model
            I_moment=I_moment,
            P_load=0.0, # No tip load
            distributed_load=distributed_load
        )

        # 2. Passive Case: Gravity only (chi_kappa = 0)
        # We keep chi_E non-zero as it's a material property, but target curvature is 0.
        kappa_target_pass = np.zeros_like(s)
        theta_pass, kappa_pass = solve_beam_static(
            s=s,
            kappa_target=kappa_target_pass,
            E_field=E_field,
            M_active=np.zeros_like(s),
            I_moment=I_moment,
            P_load=0.0,
            distributed_load=distributed_load
        )

        # Calculate P_counter
        # P_counter ~ mean(|kappa_IEC - kappa_passive|^2) * L^2 * ...
        curvature_diff_sq = (kappa_iec - kappa_pass)**2
        mean_diff_sq = np.mean(curvature_diff_sq)

        P_counter = eta_a * rho * A * g * (L**2) * mean_diff_sq

        # Also store Cobb angle proxy (max deflection angle range)
        cobb_angle = np.rad2deg(np.max(theta_iec) - np.min(theta_iec))

        # Geodesic deviation D_geo: difference between IEC shape and passive shape
        # We approximate using L2 norm of angle difference (dimensionless)
        D_geo = np.sqrt(np.mean((theta_iec - theta_pass)**2))

        results.append({
            'L': L,
            'P_counter': P_counter,
            'Cobb_angle': cobb_angle,
            'D_geo': D_geo
        })

    df = pd.DataFrame(results)

    # Compute Proprioceptive Supply Capacity
    # S_proprio(L) = S_0 * (L / L_0)^alpha
    # L_0 = 0.35
    # S_0 = P_counter(L_0)

    L_ref = 0.35
    # Interpolate P_counter at L_ref
    S_0 = np.interp(L_ref, df['L'], df['P_counter'])

    df['S_proprio_alpha05'] = S_0 * (df['L'] / L_ref)**0.5
    df['S_proprio_alpha10'] = S_0 * (df['L'] / L_ref)**1.0

    # Find critical length L_crit where P_counter > S_proprio_alpha05
    # We look for the crossing point. Since S_0 is defined at L_ref, they cross there.
    # The "window" is where P > S.
    # If P is constant (L^0) and S increases (L^0.5), P > S for L < L_ref.
    # So L_crit is L_ref (0.35).
    L_crit = L_ref

    # Save CSV with explicit column order
    output_dir = 'outputs/thermodynamic_cost'
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'energy_deficit_window.csv')
    df_out = df[['L', 'P_counter', 'S_proprio_alpha05', 'S_proprio_alpha10', 'Cobb_angle', 'D_geo']]
    df_out.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Plotting
    output_fig_dir = 'outputs/figures'
    os.makedirs(output_fig_dir, exist_ok=True)
    fig_path = os.path.join(output_fig_dir, 'energy_deficit_window.png')

    # Also save to manuscript figures just in case latex expects it there.
    manuscript_fig_path = os.path.join('manuscript/figures', 'energy_deficit_window.png')
    os.makedirs('manuscript/figures', exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(df['L'], df['P_counter'], 'r-', linewidth=2, label=r'$P_{counter} \sim L^2 \langle \Delta \kappa^2 \rangle$')
    plt.plot(df['L'], df['S_proprio_alpha05'], 'b--', linewidth=2, label=r'$S_{proprio} (\alpha=0.5)$')
    plt.plot(df['L'], df['S_proprio_alpha10'], 'g:', linewidth=2, label=r'$S_{proprio} (\alpha=1.0)$')

    # Shade Energy Deficit Window (where P_counter > S_proprio_alpha05)
    plt.fill_between(df['L'], df['P_counter'], df['S_proprio_alpha05'],
                     where=(df['P_counter'] > df['S_proprio_alpha05']),
                     color='red', alpha=0.1, label='Energy Deficit Window')

    plt.axvline(x=L_crit, color='k', linestyle=':', alpha=0.5)
    plt.text(L_crit, plt.ylim()[1]*0.1, f' $L_{{crit}}={L_crit}$ m', rotation=90)

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Thermodynamic Cost (normalized)')
    plt.title('Energy Deficit Window: Cost vs. Proprioceptive Supply')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.savefig(fig_path, dpi=300)
    plt.savefig(manuscript_fig_path, dpi=300) # Save both places
    print(f"Saved figure to {fig_path} and {manuscript_fig_path}")

    # Analyze scaling
    # Fit P_counter = k * L^beta
    log_L = np.log(df['L'])
    log_P = np.log(df['P_counter'])
    slope, intercept = np.polyfit(log_L, log_P, 1)
    print(f"P_counter scaling exponent: {slope:.2f}")
    print(f"L_crit: {L_crit:.2f} m")

if __name__ == "__main__":
    run_simulation()
