"""
Simulation: Energy Deficit Bifurcation (2D Phase Diagram)

This script performs a full parameter sweep of Curvature Sensitivity (chi_kappa) vs. Spinal Length (L)
to map the "Energy Deficit Window" where thermodynamic cost exceeds proprioceptive supply.

Hypothesis: H_2026_02_08_EnergyPhase
Prediction: High-chi_kappa patients enter the Energy Deficit Window at shorter L (earlier onset).

Outputs:
- outputs/thermodynamic_cost/energy_deficit_bifurcation.csv: Phase diagram data
- manuscript/figures/energy_deficit_bifurcation.png: Heatmap of Energy Deficit Ratio
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
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
    Matches definition in scripts/experiment_energy_deficit_window.py
    """
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

def compute_p_counter(L, chi_kappa, chi_E=0.10):
    """
    Compute Thermodynamic Cost P_counter for a given length and sensitivity.
    """
    # Parameters
    E0 = 1.0e9 # Pa
    rho = 1100.0 # kg/m^3
    A = 0.001 # m^2
    g = 9.81 # m/s^2
    I_moment = 1.0e-8 # m^4
    eta_a = 1.0 # Scaling factor

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
    # We keep chi_E non-zero as it's a material property
    theta_pass, kappa_pass = solve_beam_static(
        s=s,
        kappa_target=np.zeros_like(s),
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

    return P_counter

def run_simulation():
    print("Starting Energy Deficit Bifurcation simulation...")

    # Reference Calculation for S_proprio normalization
    # We calibrate S_proprio such that at L=0.35m and chi_kappa=0.05, Supply = Cost (R=1.0)
    # This defines the "Edge of Chaos" for a standard patient.
    L_ref = 0.35
    chi_kappa_ref = 0.05
    P_ref = compute_p_counter(L_ref, chi_kappa_ref)
    S_0 = P_ref
    print(f"Reference P_counter (S_0) at L={L_ref}, chi={chi_kappa_ref}: {S_0:.4e}")

    # Parameter Sweep Grid
    # High resolution for smooth heatmap
    n_L = 20
    n_chi = 20

    L_values = np.linspace(0.10, 0.60, n_L)
    chi_values = np.linspace(0.01, 0.20, n_chi)

    results = []

    # Pre-compute P_counter for grid
    print(f"Running sweep: {n_L}x{n_chi} = {n_L*n_chi} points...")

    for chi in chi_values:
        for L in L_values:
            P_cost = compute_p_counter(L, chi)

            # Proprioceptive Supply: S(L) ~ L^0.7
            # S_proprio(L) = S_0 * (L / L_ref)^0.7
            S_supply = S_0 * (L / L_ref)**0.7

            # Energy Deficit Ratio R = Cost / Supply
            # R > 1 implies Deficit
            R_deficit = P_cost / S_supply

            results.append({
                'chi_kappa': chi,
                'L': L,
                'P_cost': P_cost,
                'S_supply': S_supply,
                'R_deficit': R_deficit,
                'In_Deficit': R_deficit > 1.0
            })

    df = pd.DataFrame(results)

    # Save Results
    output_dir = 'outputs/thermodynamic_cost'
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'energy_deficit_bifurcation.csv')
    df.to_csv(csv_path, index=False)
    print(f"Saved simulation data to {csv_path}")

    # Plotting Phase Diagram
    # Pivot for heatmap
    pivot_table = df.pivot(index='chi_kappa', columns='L', values='R_deficit')

    # Setup figure
    fig_dir = 'manuscript/figures'
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, 'energy_deficit_bifurcation.png')

    plt.figure(figsize=(10, 8))

    # Create Heatmap using imshow
    # We use log scale for color since R can vary widely? Maybe just linear with robust max.
    # Let's cap R at 3.0 for visualization

    # Check orientation: pivot index is chi (rows), columns is L
    # pivot_table index is ascending chi_kappa (0.01..0.20) -> Rows
    # pivot_table columns is ascending L (0.1..0.6) -> Columns
    Z = pivot_table.values

    # Plot extent [L_min, L_max, chi_min, chi_max]
    extent = [L_values[0], L_values[-1], chi_values[0], chi_values[-1]]

    plt.imshow(Z, cmap='RdYlBu_r', vmin=0.0, vmax=3.0, origin='lower',
               extent=extent, aspect='auto')

    plt.colorbar(label='Energy Deficit Ratio (Cost/Supply)')

    # Draw Contour line at R=1.0
    # Need meshgrid for contour matching extent
    # X corresponds to columns (L), Y to rows (chi)
    cnt = plt.contour(L_values, chi_values, Z, levels=[1.0],
                      colors='black', linewidths=2, linestyles='--')
    plt.clabel(cnt, inline=True, fontsize=10, fmt='R=1.0')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Curvature Sensitivity $\chi_\kappa$')
    plt.title('Phase Diagram: Energy Deficit Window\n(Red = Deficit, Blue = Stable)')

    # Annotate regions
    # Find a point in deficit and stable using data coordinates
    # Deficit is at High chi, Low L (R > 1)
    # Stability is at Low chi, High L (R < 1)

    # Coordinates: L (x), chi (y)
    x_def = L_values[int(n_L*0.2)]
    y_def = chi_values[int(n_chi*0.8)]

    x_stab = L_values[int(n_L*0.8)]
    y_stab = chi_values[int(n_chi*0.2)]

    plt.text(x_def, y_def, 'Energy Deficit\n(Vulnerable)', color='maroon',
             fontweight='bold', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    plt.text(x_stab, y_stab, 'Metabolic Stability\n(Safe)', color='navy',
             fontweight='bold', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    print(f"Saved phase diagram to {fig_path}")

if __name__ == "__main__":
    run_simulation()
