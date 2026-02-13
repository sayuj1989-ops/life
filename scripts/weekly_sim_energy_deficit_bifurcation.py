"""
Simulation: Energy Deficit Bifurcation (2D Phase Diagram)

This script performs a 2D parameter sweep of Coupling Strength (chi_kappa) vs Spinal Length (L)
to map the "Energy Deficit Window" where the thermodynamic cost of counter-curvature (P_counter)
exceeds the proprioceptive supply (S_proprio).

Hypothesis H_2026_02_08_EnergyPhase:
High-chi_kappa patients enter the Energy Deficit Window at shorter L (earlier onset)
and exit later, experiencing a wider vulnerability window.

Outputs:
- outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv
- outputs/figures/phase_diagram_energy_deficit.png
- manuscript/figures/phase_diagram_energy_deficit.png
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    sys.path.append('src')
    from spinalmodes.iec import solve_beam_static

def generate_bimodal_gaussian_field(s, L):
    """
    Generate the bimodal Gaussian information field I(s).
    """
    if L == 0:
        return np.full_like(s, 0.3)

    s_norm = s / L

    # Parameters from manuscript/sections/methods.tex
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08

    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10

    I_0 = 0.3

    term_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    term_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))

    return term_c + term_l + I_0

def run_simulation():
    print("Starting Energy Deficit Bifurcation sweep...")

    # Parameter Ranges
    # L: 0.20m to 0.60m (Adolescent Growth)
    L_values = np.linspace(0.20, 0.60, 40)

    # chi_kappa: 0.0 to 0.15 (Coupling Strength)
    chi_values = np.linspace(0.0, 0.15, 30)

    # Fixed Parameters
    chi_E = 0.10
    E0 = 1.0e9
    rho = 1100.0
    A = 0.001
    g = 9.81
    I_moment = A**2 / (4 * np.pi)
    eta_a = 1.0 # Cost scaling factor

    # --- Calibration Step ---
    print("Calibrating Proprioceptive Supply (S_0)...")
    L_ref = 0.35
    chi_ref = 0.05

    # Run reference simulation
    n_nodes = 100
    s_ref = np.linspace(0, L_ref, n_nodes)
    I_ref = generate_bimodal_gaussian_field(s_ref, L_ref)
    grad_I_ref = np.gradient(I_ref, s_ref)
    E_ref = E0 * (1.0 + chi_E * I_ref)
    dist_load = rho * A * g

    # Active
    theta_active, kappa_active = solve_beam_static(
        s=s_ref,
        kappa_target=chi_ref * grad_I_ref,
        E_field=E_ref,
        M_active=np.zeros_like(s_ref),
        I_moment=I_moment,
        P_load=0.0,
        distributed_load=dist_load
    )
    # Passive
    theta_pass, kappa_pass = solve_beam_static(
        s=s_ref,
        kappa_target=np.zeros_like(s_ref),
        E_field=E_ref,
        M_active=np.zeros_like(s_ref),
        I_moment=I_moment,
        P_load=0.0,
        distributed_load=dist_load
    )

    P_ref = eta_a * rho * A * g * (L_ref**2) * np.mean((kappa_active - kappa_pass)**2)
    S_0 = P_ref
    print(f"Calibration Complete: S_0 = {S_0:.6e} at L={L_ref}, chi={chi_ref}")

    # --- Sweep Loop ---
    results = []

    for chi in chi_values:
        for L in L_values:
            s = np.linspace(0, L, n_nodes)
            I_field = generate_bimodal_gaussian_field(s, L)
            grad_I = np.gradient(I_field, s)
            E_field = E0 * (1.0 + chi_E * I_field)

            # Active Simulation
            theta_iec, kappa_iec = solve_beam_static(
                s=s,
                kappa_target=chi * grad_I,
                E_field=E_field,
                M_active=np.zeros_like(s),
                I_moment=I_moment,
                P_load=0.0,
                distributed_load=rho * A * g
            )

            # Passive Simulation
            theta_pas, kappa_pas = solve_beam_static(
                s=s,
                kappa_target=np.zeros_like(s),
                E_field=E_field,
                M_active=np.zeros_like(s),
                I_moment=I_moment,
                P_load=0.0,
                distributed_load=rho * A * g
            )

            # Cost P_counter
            mean_sq_diff = np.mean((kappa_iec - kappa_pas)**2)
            P_counter = eta_a * rho * A * g * (L**2) * mean_sq_diff

            # Supply S_proprio (sublinear scaling alpha=0.5)
            S_proprio = S_0 * (L / L_ref)**0.5

            # Deficit Ratio
            ratio = P_counter / S_proprio if S_proprio > 0 else 0

            results.append({
                'chi_kappa': chi,
                'L': L,
                'P_counter': P_counter,
                'S_proprio': S_proprio,
                'Deficit_Ratio': ratio,
                'In_Deficit': ratio > 1.0
            })

    df = pd.DataFrame(results)

    # --- Save Data ---
    output_dir = 'outputs/thermodynamic_cost'
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'phase_diagram_energy_deficit.csv')
    df.to_csv(csv_path, index=False)
    print(f"Saved simulation data to {csv_path}")

    # --- Plotting ---
    output_fig_dir = 'outputs/figures'
    os.makedirs(output_fig_dir, exist_ok=True)
    os.makedirs('manuscript/figures', exist_ok=True)

    # Pivot for heatmap
    pivot_table = df.pivot(index='chi_kappa', columns='L', values='Deficit_Ratio')

    plt.figure(figsize=(10, 8))

    # Use log scale for color to handle wide range of ratios, centered at 1 (Ratio=1 -> Log=0)
    # Actually, simpler to just map Ratio with specific levels
    # Let's use a diverging map centered at 1

    # Custom levels contour plot might be cleaner than heatmap for "wedge"
    X, Y = np.meshgrid(pivot_table.columns, pivot_table.index)
    Z = pivot_table.values

    # Contourf for colored regions
    # Levels: Safe (<1), Transition (1-2), High Risk (>2)
    # But let's do a continuous map

    plt.contourf(X, Y, Z, levels=50, cmap='RdYlBu_r', alpha=0.8, vmin=0, vmax=3)
    cbar = plt.colorbar()
    cbar.set_label('Energy Deficit Ratio ($P_{counter} / S_{proprio}$)')

    # Thick line at Ratio = 1.0
    cs = plt.contour(X, Y, Z, levels=[1.0], colors='black', linewidths=2.5, linestyles='dashed')
    plt.clabel(cs, fmt={1.0: 'Onset Threshold'}, inline=True, fontsize=12)

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_{\kappa}$')
    plt.title('Phase Diagram: Energy Deficit Bifurcation')

    # Annotations
    plt.text(0.25, 0.02, 'Safe Zone\n(Supply > Cost)', color='blue', fontweight='bold', ha='center')
    plt.text(0.50, 0.12, 'Vulnerability Wedge\n(Cost > Supply)', color='darkred', fontweight='bold', ha='center')

    fig_path = os.path.join(output_fig_dir, 'phase_diagram_energy_deficit.png')
    manu_path = os.path.join('manuscript/figures', 'phase_diagram_energy_deficit.png')

    plt.savefig(fig_path, dpi=300)
    plt.savefig(manu_path, dpi=300)
    print(f"Saved phase diagram to {fig_path}")

if __name__ == "__main__":
    run_simulation()
