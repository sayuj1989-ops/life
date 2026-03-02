import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

if script_dir not in sys.path:
    sys.path.append(script_dir)

from spinalmodes.iec import solve_beam_static
from experiment_utils import StandardExperimentParser, setup_experiment

def get_species_data():
    data_path = os.path.join(project_root, 'data', 'species_parameters.csv')
    df = pd.read_csv(data_path)
    # Ensure Gravity_G exists
    if 'Gravity_G' not in df.columns:
        df['Gravity_G'] = 1.0
    return df

def simulate_species(row):
    # Retrieve parameters
    L = row['Length_m']
    mass = row['Mass_kg']
    EI = row['EI_Nm2']
    g = 9.81 * row['Gravity_G']
    posture = row['Posture']

    # Assumptions for Cross-Sectional Area
    rho = 1100.0
    # Approximate volume
    vol = mass / rho
    # Approximate A = vol / L (ignoring appendages for simplicity)
    A = vol / L

    # Calculate target chi_kappa
    # We assume humans and facultative bipeds have higher chi_kappa (0.05)
    # Quadrupeds have lower (0.01)
    # Extinct Brachiosaurus has huge length, let's keep it 0.01
    if 'Biped' in posture:
        chi_kappa = 0.05
    else:
        chi_kappa = 0.01

    n_nodes = 100
    s = np.linspace(0, L, n_nodes)
    s_norm = s / L

    # Information field parameters (bimodal Gaussian)
    A_c = 0.5
    s_c = 0.80
    sigma_c = 0.08
    A_l = 0.7
    s_l = 0.25
    sigma_l = 0.10
    I_0 = 0.3

    I_field = (A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2)) +
               A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2)) +
               I_0)

    grad_I = np.gradient(I_field, s)
    kappa_target_IEC = chi_kappa * grad_I

    E_field = np.full_like(s, EI)
    M_active = np.zeros_like(s)
    I_moment = 1.0  # Since we are passing E_field as EI, I_moment=1.0 is fine

    # Distributed load logic
    # Bipeds have axial load, quadrupeds have transverse load mostly.
    # To simplify, we apply gravity as a distributed transverse load
    # scaled by a posture factor (bipeds = 0.1, quadrupeds = 1.0)
    if 'Biped' in posture:
        posture_factor = 0.1
    else:
        posture_factor = 1.0

    distributed_load = rho * A * g * posture_factor

    theta_IEC, kappa_IEC = solve_beam_static(
        s=s,
        kappa_target=kappa_target_IEC,
        E_field=E_field,
        M_active=M_active,
        I_moment=I_moment,
        P_load=0.0,
        distributed_load=distributed_load
    )

    # Passive configuration (gravity only, chi_kappa=0)
    theta_passive, kappa_passive = solve_beam_static(
        s=s,
        kappa_target=np.zeros_like(s),
        E_field=E_field,
        M_active=M_active,
        I_moment=I_moment,
        P_load=0.0,
        distributed_load=distributed_load
    )

    # Metrics
    cobb_angle = np.rad2deg(np.max(theta_IEC) - np.min(theta_IEC))
    D_geo = np.mean(np.abs(kappa_IEC - kappa_passive))

    mse_kappa = np.mean((kappa_IEC - kappa_passive)**2)
    eta_a = 1.0
    P_counter = eta_a * rho * A * g * (L**2) * mse_kappa

    # Cost per unit length for fairer scaling
    P_counter_norm = P_counter / L

    return {
        "Species": row['Species'],
        "L": L,
        "Mass": mass,
        "Posture": posture,
        "Gravity_G": row['Gravity_G'],
        "Cobb_angle": cobb_angle,
        "D_geo": D_geo,
        "P_counter": P_counter,
        "P_counter_norm": P_counter_norm,
        "log_L": np.log10(L),
        "log_P": np.log10(P_counter) if P_counter > 0 else 0
    }

def run_experiment():
    parser = StandardExperimentParser(
        description="Experiment: Cross Species Scaling & Gravity Phase Diagram"
    )
    args = parser.parse_args()

    # Add a custom experiment directory to output_dir
    args.out_dir = str(Path(args.out_dir) / "cross_species_scaling")
    output_dir = setup_experiment(args)

    df_params = get_species_data()
    print(f"Loaded {len(df_params)} species configurations.")

    results = []
    for _, row in df_params.iterrows():
        try:
            res = simulate_species(row)
            results.append(res)
            print(f"Simulated {row['Species']}: L={row['Length_m']}m, Cobb={res['Cobb_angle']:.1f}°, P_counter={res['P_counter']:.2e}")
        except Exception as e:
            print(f"Failed to simulate {row['Species']}: {e}")

    df_results = pd.DataFrame(results)

    csv_path = output_dir / "cross_species_results.csv"
    df_results.to_csv(csv_path, index=False)
    print(f"\nResults saved to {csv_path}")

    # Generating Plots
    fig_dir = output_dir / "figures"
    fig_dir.mkdir(exist_ok=True)

    # Plot 1: L vs P_counter (log-log)
    plt.figure(figsize=(10, 6))
    for posture in df_results['Posture'].unique():
        subset = df_results[df_results['Posture'] == posture]
        plt.scatter(subset['L'], subset['P_counter'], label=posture, s=100, alpha=0.7)

    for i, row in df_results.iterrows():
        plt.annotate(row['Species'], (row['L'], row['P_counter']),
                     xytext=(5, 5), textcoords='offset points', fontsize=8)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Thermodynamic Cost P_counter (W)')
    plt.title('Cross-Species Scaling of Energy Deficit')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add theoretical scaling lines
    # For quadrupeds: P ~ L^4
    # For bipeds: P ~ L^2
    L_range = np.linspace(df_results['L'].min(), df_results['L'].max(), 100)
    plt.plot(L_range, L_range**4 * 1e-3, 'k--', alpha=0.5, label='L^4 scaling (Quadruped)')
    plt.plot(L_range, L_range**2 * 1e-1, 'r--', alpha=0.5, label='L^2 scaling (Biped)')

    plt.legend()

    p1_path = fig_dir / "scaling_cost_vs_length.png"
    plt.savefig(p1_path, dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 2: Gravity-Length Phase Diagram
    plt.figure(figsize=(10, 6))

    # Separate core dataset from extra-terrestrial
    core_df = df_results[df_results['Gravity_G'] == 1.0]
    extra_df = df_results[df_results['Gravity_G'] != 1.0]

    # Color mapping by cost
    scatter = plt.scatter(df_results['L'], df_results['Gravity_G'],
                          c=df_results['log_P'], cmap='viridis', s=100)

    plt.colorbar(scatter, label='Log10(Thermodynamic Cost P_counter)')

    for i, row in df_results.iterrows():
        plt.annotate(row['Species'], (row['L'], row['Gravity_G']),
                     xytext=(5, 5), textcoords='offset points', fontsize=8)

    plt.xscale('log')
    plt.xlabel('Spinal Length L (m)')
    plt.ylabel('Gravity (G)')
    plt.title('Gravity-Length Phase Diagram')
    plt.grid(True, alpha=0.3)

    p2_path = fig_dir / "gravity_length_phase_diagram.png"
    plt.savefig(p2_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figures saved to {fig_dir}")

if __name__ == "__main__":
    run_experiment()
