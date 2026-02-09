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

    # Parameters
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

def calculate_p_counter(L, chi_kappa, eta_a=1.0, E0=1.0e9, rho=1100.0, A_cross=0.001, g=9.81, I_moment=1.0e-8, chi_E=0.10):
    n_nodes = 100
    s = np.linspace(0, L, n_nodes)

    # Information field
    I_field = generate_bimodal_gaussian_field(s, L)
    grad_I = np.gradient(I_field, s)

    # Stiffness field
    E_field = E0 * (1.0 + chi_E * I_field)

    # Distributed load (gravity transverse)
    distributed_load = rho * A_cross * g

    # 1. IEC Case: Active target curvature
    kappa_target_iec = chi_kappa * grad_I
    theta_iec, kappa_iec = solve_beam_static(
        s=s,
        kappa_target=kappa_target_iec,
        E_field=E_field,
        M_active=np.zeros_like(s),
        I_moment=I_moment,
        P_load=0.0,
        distributed_load=distributed_load
    )

    # 2. Passive Case: Gravity only (chi_kappa = 0)
    # Target curvature is 0
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

    P_counter = eta_a * rho * A_cross * g * (L**2) * mean_diff_sq
    return P_counter

def run_simulation():
    print("Starting Energy Phase Diagram simulation...")

    # Parameters
    L_start = 0.1
    L_end = 0.6
    n_L = 30
    L_values = np.linspace(L_start, L_end, n_L)

    chi_start = 0.0
    chi_end = 0.20
    n_chi = 30
    chi_values = np.linspace(chi_start, chi_end, n_chi)

    # Calibration parameters
    L_ref = 0.35
    chi_ref = 0.05

    # 1. Calibrate S_0
    print(f"Calibrating S_proprio at L={L_ref}, chi_kappa={chi_ref}...")
    P_ref = calculate_p_counter(L_ref, chi_ref)
    S_0 = P_ref
    print(f"S_0 calibrated to: {S_0:.6e}")

    # 2. Parameter Sweep
    print("Running parameter sweep...")
    results = []

    # Pre-calculate S_proprio for each L (independent of chi_kappa)
    # S_proprio(L) = S_0 * (L / L_ref)^alpha
    alpha = 0.5
    S_proprio_map = {L: S_0 * (L / L_ref)**alpha for L in L_values}

    for i, chi in enumerate(chi_values):
        print(f"Processing chi_kappa={chi:.3f} ({i+1}/{n_chi})")
        for L in L_values:
            P = calculate_p_counter(L, chi)
            S = S_proprio_map[L]
            deficit = P - S

            results.append({
                'chi_kappa': chi,
                'L': L,
                'P_counter': P,
                'S_proprio': S,
                'Deficit': deficit,
                'In_Deficit': 1 if deficit > 0 else 0
            })

    df = pd.DataFrame(results)

    # Save CSV
    output_dir = 'outputs/thermodynamic_cost'
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'energy_phase_data.csv')
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Plotting Heatmap
    print("Generating Heatmap...")

    # Use matplotlib directly for pcolormesh
    fig, ax = plt.subplots(figsize=(10, 8))

    # Pivot data for plotting
    Z = df.pivot(index='chi_kappa', columns='L', values='Deficit').values
    X, Y = np.meshgrid(L_values, chi_values)

    max_abs = max(abs(df['Deficit'].min()), abs(df['Deficit'].max()))

    c = ax.pcolormesh(X, Y, Z, cmap='RdBu_r', vmin=-max_abs, vmax=max_abs, shading='auto')
    fig.colorbar(c, ax=ax, label='Energy Deficit (P - S)')

    # Contour line at 0
    contour = ax.contour(X, Y, Z, levels=[0], colors='black', linewidths=2)
    ax.clabel(contour, inline=True, fontsize=10, fmt='Boundary')

    ax.set_title('Energy Deficit Phase Diagram\nDeficit = P_counter - S_proprio')
    ax.set_xlabel('Spinal Length L (m)')
    ax.set_ylabel('Intrinsic Curvature Drive (chi_kappa)')
    ax.grid(True, alpha=0.3)

    # Mark the reference point
    ax.plot(L_ref, chi_ref, 'ko', label='Calibration Point (Critical)')
    ax.legend()

    # Save Figure
    fig_dir = 'manuscript/figures'
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, 'energy_phase_diagram.png')
    plt.savefig(fig_path, dpi=300)
    print(f"Saved figure to {fig_path}")

if __name__ == "__main__":
    run_simulation()
