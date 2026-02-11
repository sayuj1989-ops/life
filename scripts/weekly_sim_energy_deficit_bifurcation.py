"""
Weekly Simulation: Energy Deficit Bifurcation (2D Phase Diagram)

Generates a 2D phase diagram of Energy Deficit Ratio (R_deficit) across
IEC coupling strength (chi_kappa) and spinal length (L).

Outputs:
- outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv
- outputs/figures/phase_diagram_energy_deficit.png
- outputs/figures/phase_diagram_energy_deficit_cobb.png
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Add src to python path to import spinalmodes
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from spinalmodes.iec import solve_beam_static
except ImportError:
    # If not found, try adding just 'src' assuming run from root
    sys.path.append('src')
    from spinalmodes.iec import solve_beam_static

from spinalmodes.countercurvature.validation_and_metrics import geodesic_curvature_deviation, compute_countercurvature_metric
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.scoliosis_metrics import build_lateral_curvature_bump

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

def calculate_p_counter(L, chi_kappa, params, compute_cobb=False):
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
    dIds = grad_I # For InfoField1D

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

    # Calculate D_geo
    info = InfoField1D(s=s, I=I_field, dIds=dIds)
    g_eff = compute_countercurvature_metric(info)
    d_geo_metrics = geodesic_curvature_deviation(s, kappa_pass, kappa_iec, g_eff)
    D_geo = d_geo_metrics['D_geo']

    cobb_angle = 0.0
    if compute_cobb:
        # Lateral Plane Simulation
        epsilon_asym = 0.03
        kappa_lat_target = build_lateral_curvature_bump(s, epsilon_lat=epsilon_asym)

        # Apply small lateral test load to probe stiffness
        # Load = 10% of axial load due to gravity (approx)
        P_lat_test = 0.1 * (rho * A * g * L)

        theta_lat, _ = solve_beam_static(
            s=s,
            kappa_target=kappa_lat_target,
            E_field=E_field, # Same stiffness profile
            M_active=np.zeros_like(s),
            I_moment=I_moment,
            P_load=P_lat_test, # Lateral test load
            distributed_load=0.0 # No lateral gravity
        )

        cobb_angle = np.degrees(np.max(theta_lat) - np.min(theta_lat))

    return P_counter, D_geo, cobb_angle

def run_simulation():
    print("Starting Energy Deficit Bifurcation (2D Phase Diagram) simulation...")

    # Parameters
    # Reference condition for Supply
    ref_L = 0.35
    ref_chi_kappa = 0.05
    supply_alpha = 0.7 # Updated from 0.5 to 0.7 as per prompt

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
    S_0, _, _ = calculate_p_counter(ref_L, ref_chi_kappa, sim_params, compute_cobb=False)
    print(f"Reference Supply S_0: {S_0:.4e}")

    # 2. Parameter Sweep
    L_start = 0.25
    L_end = 0.55
    n_L = 20
    L_values = np.linspace(L_start, L_end, n_L)

    chi_start = 0.01
    chi_end = 0.10
    n_chi = 20
    chi_values = np.linspace(chi_start, chi_end, n_chi)

    results = []

    # Pre-allocate for heatmaps
    deficit_matrix = np.zeros((n_chi, n_L))
    cobb_matrix = np.zeros((n_chi, n_L))

    print(f"Running sweep: {n_L} L values x {n_chi} chi_kappa values...")

    for i, chi in enumerate(chi_values):
        for j, L in enumerate(L_values):
            # Calculate Cost and Cobb
            P_counter, D_geo, cobb = calculate_p_counter(L, chi, sim_params, compute_cobb=True)

            # Calculate Supply
            S_proprio = S_0 * (L / ref_L)**supply_alpha

            # Deficit Ratio
            if S_proprio > 0:
                R_deficit = P_counter / S_proprio
            else:
                R_deficit = 0.0

            deficit_matrix[i, j] = R_deficit
            cobb_matrix[i, j] = cobb

            results.append({
                'L': L,
                'chi_kappa': chi,
                'P_counter': P_counter,
                'S_proprio': S_proprio,
                'R_deficit': R_deficit,
                'D_geo': D_geo,
                'Cobb_angle': cobb
            })

    # Save CSV
    df = pd.DataFrame(results)
    output_dir = Path('outputs/thermodynamic_cost')
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / 'phase_diagram_energy_deficit.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved simulation data to {csv_path}")

    # 3. Plotting
    fig_dir = Path('outputs/figures')
    fig_dir.mkdir(parents=True, exist_ok=True)

    # 3a. Energy Deficit Phase Diagram
    fig_path = fig_dir / 'phase_diagram_energy_deficit.png'
    plt.figure(figsize=(10, 8))
    X, Y = np.meshgrid(L_values, chi_values)

    # Clip for visualization
    max_R = 5.0
    clipped_matrix = np.clip(deficit_matrix, 0, max_R)

    cp = plt.contourf(X, Y, clipped_matrix, levels=20, cmap='RdYlBu_r')
    cbar = plt.colorbar(cp)
    cbar.set_label(r'Energy Deficit Ratio ($R_{deficit} = P_{counter} / S_{proprio}$)')

    # Add Critical Boundary (R=1)
    cs = plt.contour(X, Y, deficit_matrix, levels=[1.0], colors='k', linewidths=2, linestyles='dashed')
    plt.clabel(cs, inline=1, fontsize=10, fmt='R=1.0 (Critical)')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Intrinsic Curvature Drive $\chi_\kappa$')
    plt.title('Energy Deficit Phase Diagram: Onset of Instability')
    plt.grid(True, alpha=0.3, linestyle=':')
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved figure to {fig_path}")

    # 3b. Cobb Angle Phase Diagram
    fig_cobb_path = fig_dir / 'phase_diagram_energy_deficit_cobb.png'
    plt.figure(figsize=(10, 8))

    cp_cobb = plt.contourf(X, Y, cobb_matrix, levels=20, cmap='viridis')
    cbar_cobb = plt.colorbar(cp_cobb)
    cbar_cobb.set_label('Predicted Cobb Angle (deg)')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Intrinsic Curvature Drive $\chi_\kappa$')
    plt.title('Lateral Instability Map (Cobb Angle)')
    plt.grid(True, alpha=0.3, linestyle=':')
    plt.savefig(fig_cobb_path, dpi=300)
    plt.close()
    print(f"Saved figure to {fig_cobb_path}")

    print("Simulation complete.")

if __name__ == "__main__":
    run_simulation()
