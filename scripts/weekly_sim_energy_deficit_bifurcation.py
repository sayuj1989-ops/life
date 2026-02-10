"""
Weekly Simulation: Energy Deficit Bifurcation (2D Phase Diagram)

Generates a 2D phase diagram of Energy Deficit Ratio (R_deficit) across
IEC coupling strength (chi_kappa) and spinal length (L).

Prediction: High chi_kappa patients enter the Energy Deficit Window (R > 1)
at shorter L (earlier onset).

Outputs:
- outputs/thermodynamic_cost/energy_phase_diagram.csv
- manuscript/figures/energy_phase_diagram.png
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

def calculate_p_counter(L, chi_kappa, params):
    """
    Calculate the thermodynamic cost of counter-curvature (P_counter) for a given L and chi_kappa.
    """
    E0 = params['E0']
    rho = params['rho']
    A = params['A']
    g = params['g']
    I_moment = params['I_moment']
    eta_a = params['eta_a']
    chi_E = params['chi_E']

    # Spatial grid
    n_nodes = 100
    s = np.linspace(0, L, n_nodes)

    # Information field
    I_field = generate_bimodal_gaussian_field(s, L)
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
        M_active=np.zeros_like(s),
        I_moment=I_moment,
        P_load=0.0,
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
    # P_counter ~ mean(|kappa_IEC - kappa_passive|^2) * L^2
    curvature_diff_sq = (kappa_iec - kappa_pass)**2
    mean_diff_sq = np.mean(curvature_diff_sq)

    P_counter = eta_a * rho * A * g * (L**2) * mean_diff_sq

    return P_counter

def run_simulation():
    print("Starting Energy Deficit Bifurcation (2D Phase Diagram) simulation...")

    # Parameters
    # Reference condition for Supply
    ref_L = 0.35
    ref_chi_kappa = 0.05
    supply_alpha = 0.5

    sim_params = {
        'E0': 1.0e9,
        'rho': 1100.0,
        'A': 0.001,
        'g': 9.81,
        'I_moment': 1.0e-8,
        'eta_a': 1.0,
        'chi_E': 0.10
    }

    # 1. Calculate Reference Supply
    # S_proprio(L) = S_0 * (L / L_ref)^alpha
    # S_0 is P_counter at reference condition.
    print(f"Calculating reference supply at L={ref_L}, chi_kappa={ref_chi_kappa}...")
    S_0 = calculate_p_counter(ref_L, ref_chi_kappa, sim_params)
    print(f"Reference Supply S_0: {S_0:.4e}")

    # 2. Parameter Sweep
    L_start = 0.1
    L_end = 0.6
    n_L = 50
    L_values = np.linspace(L_start, L_end, n_L)

    chi_start = 0.0
    chi_end = 0.2
    n_chi = 50
    chi_values = np.linspace(chi_start, chi_end, n_chi)

    results = []

    # Pre-allocate for heatmap
    deficit_matrix = np.zeros((n_chi, n_L))

    print(f"Running sweep: {n_L} L values x {n_chi} chi_kappa values...")

    for i, chi in enumerate(chi_values):
        for j, L in enumerate(L_values):
            # Calculate Cost
            P_counter = calculate_p_counter(L, chi, sim_params)

            # Calculate Supply
            S_proprio = S_0 * (L / ref_L)**supply_alpha

            # Deficit Ratio
            # Avoid division by zero if S_proprio is 0 (unlikely for L>0)
            if S_proprio > 0:
                R_deficit = P_counter / S_proprio
            else:
                R_deficit = 0.0 # or inf

            deficit_matrix[i, j] = R_deficit

            results.append({
                'L': L,
                'chi_kappa': chi,
                'P_counter': P_counter,
                'S_proprio': S_proprio,
                'R_deficit': R_deficit
            })

    # Save CSV
    df = pd.DataFrame(results)
    output_dir = 'outputs/thermodynamic_cost'
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'energy_phase_diagram.csv')
    df.to_csv(csv_path, index=False)
    print(f"Saved simulation data to {csv_path}")

    # 3. Plotting
    fig_dir = 'manuscript/figures'
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, 'energy_phase_diagram.png')

    plt.figure(figsize=(10, 8))

    # Use imshow for heatmap or contourf
    # contourf is better for continuous fields
    X, Y = np.meshgrid(L_values, chi_values)

    # Define levels for contourf
    # We want to highlight R=1.
    # Log scale might be good if range is large, but linear is clearer for R=1 crossing.

    # Set max level to avoid outliers dominating the color scale
    max_R = 5.0
    clipped_matrix = np.clip(deficit_matrix, 0, max_R)

    cp = plt.contourf(X, Y, clipped_matrix, levels=20, cmap='RdYlBu_r')
    cbar = plt.colorbar(cp)
    cbar.set_label('Energy Deficit Ratio ($R_{deficit} = P_{counter} / S_{proprio}$)')

    # Add Critical Boundary (R=1)
    # Use standard contour call
    cs = plt.contour(X, Y, deficit_matrix, levels=[1.0], colors='k', linewidths=2, linestyles='dashed')
    plt.clabel(cs, inline=1, fontsize=10, fmt='R=1.0 (Critical)')

    # Annotate regions
    # Find a point in the deficit region (R > 1) and safe region (R < 1) for labels
    # High chi, High L -> Deficit
    plt.text(0.5, 0.15, 'Energy Deficit Window\n(Vulnerable)', color='black', ha='center', va='center', fontweight='bold',
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    # Low chi -> Safe
    plt.text(0.2, 0.02, 'Homeostatic Region\n(Stable)', color='black', ha='center', va='center', fontweight='bold',
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Intrinsic Curvature Drive $\chi_\kappa$')
    plt.title('Energy Deficit Phase Diagram: Onset of Instability')

    plt.grid(True, alpha=0.3, linestyle=':')

    # Prediction verification
    # Does R=1 curve shift to lower L as chi increases?
    # Yes, if P_counter increases with chi, then P/S > 1 happens earlier.

    plt.savefig(fig_path, dpi=300)
    print(f"Saved figure to {fig_path}")
    print("Simulation complete.")

if __name__ == "__main__":
    run_simulation()
