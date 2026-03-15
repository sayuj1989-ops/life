import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from spinalmodes.countercurvature.api import (
        InfoField1D,
        CounterCurvatureParams,
        compute_effective_stiffness,
        compute_rest_curvature,
        geodesic_curvature_deviation
    )
    from spinalmodes.iec import solve_beam_static
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

def compute_P_counter(s, kappa_info, E_field, I_moment):
    """
    Compute P_counter, the metabolic power required for countercurvature.
    """
    EI = E_field * I_moment
    energy_density = 0.5 * EI * (kappa_info ** 2)
    return np.trapz(energy_density, s)

def run_sweep():
    # 2D Parameter sweep ranges
    chi_kappa_vals = np.linspace(0.01, 0.10, 20)
    L_vals = np.linspace(0.25, 0.55, 20)

    # Fixed parameters
    rho = 1100
    A = 0.001
    g = 9.81
    E0 = 1.0e9 # 1.0 GPa

    # Geometric and other assumptions
    radius = np.sqrt(A / np.pi)
    I_moment = (np.pi * radius**4) / 4.0

    # Information field params
    I_amplitude = 1.0

    # Base metabolic capacity
    S_0 = 0.05 # Tuning parameter to make R_deficit ~ 1 in the middle
    L_0 = 0.35 # Reference length (m)

    results = []

    for chi_kappa in chi_kappa_vals:
        for L in L_vals:
            # 1. Setup spatial domain
            n_nodes = 100
            s = np.linspace(0, L, n_nodes)
            s_norm = s / L # Normalized arc length

            # 2. Setup Information Field (Gaussian bump)
            I_center = 0.5
            I_width = 0.1
            I = I_amplitude * np.exp(-0.5 * ((s_norm - I_center) / I_width)**2)
            dIds = np.gradient(I, s_norm) # Gradient with respect to normalized length s_norm
            info = InfoField1D(s=s, I=I, dIds=dIds)

            # 3. Setup IEC Parameters
            params = CounterCurvatureParams(
                chi_kappa=chi_kappa,
                chi_E=0.0,
                chi_M=0.0,
                chi_tau=0.0,
                scale_length=1.0
            )

            # 4. IEC Couplings
            E_field = compute_effective_stiffness(info, params, E0)

            # Active target curvature (kappa_target = chi_kappa * dIds)
            kappa_target_3d = compute_rest_curvature(info, params, kappa_gen=0.0)
            # Take the relevant bending component (index 1)
            kappa_target = kappa_target_3d[1, :]

            # M_active
            M_active = np.zeros_like(s) # Not used in this particular simplified setup

            # 5. Solve Beam Mechanics (Static)
            # Linear density: rho * A
            w_dist = rho * A * g # Distributed load N/m

            # 5a. Passive state (no information)
            theta_passive, kappa_passive = solve_beam_static(
                s=s,
                kappa_target=np.zeros_like(s),
                E_field=E_field,
                M_active=M_active,
                I_moment=I_moment,
                P_load=0.0,
                distributed_load=w_dist
            )

            # 5b. Info-driven state
            theta_info, kappa_info = solve_beam_static(
                s=s,
                kappa_target=kappa_target,
                E_field=E_field,
                M_active=M_active,
                I_moment=I_moment,
                P_load=0.0,
                distributed_load=w_dist
            )

            # 6. Compute Metrics
            P_counter = compute_P_counter(s, kappa_info, E_field, I_moment)

            # Energy Deficit Ratio
            S_proprio = S_0 * (L / L_0)**0.7
            R_deficit = P_counter / S_proprio

            # Cobb angle proxy from a lateral asymmetry perturbation
            eps_asym = 0.03

            if R_deficit > 1.0:
                # If in deficit, simulate lateral asymmetry perturbation explicitly
                # where the target curvature is asymmetric
                kappa_target_lat = eps_asym * np.ones_like(s)
                # Reduced effective stiffness in lateral due to energy deficit (loss of active control)
                E_field_lat = E_field / (R_deficit ** 2)
            else:
                kappa_target_lat = np.zeros_like(s)
                E_field_lat = E_field

            theta_lat, kappa_lat = solve_beam_static(
                s=s,
                kappa_target=kappa_target_lat,
                E_field=E_field_lat,
                M_active=np.zeros_like(s),
                I_moment=I_moment,
                P_load=0.0,
                distributed_load=w_dist # Still under gravity
            )

            # Cobb Angle
            cobb_angle = np.abs(theta_lat[-1] - theta_lat[0]) * 180 / np.pi

            # Geodesic Deviation
            # Assuming g_eff = 1 for simplicity here
            g_eff = np.ones_like(s)
            geo_dev = geodesic_curvature_deviation(s, kappa_passive, kappa_info, g_eff)
            D_geo = geo_dev["D_geo"]


            results.append({
                "chi_kappa": chi_kappa,
                "L": L,
                "P_counter": float(P_counter),
                "cobb_angle": float(cobb_angle),
                "D_geo": float(D_geo),
                "R_deficit": float(R_deficit)
            })

    df = pd.DataFrame(results)

    # Save outputs
    out_dir_data = Path("outputs/thermodynamic_cost")
    out_dir_data.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir_data / "phase_diagram_energy_deficit.csv"
    df.to_csv(out_csv, index=False)

    out_dir_fig = Path("outputs/figures")
    out_dir_fig.mkdir(parents=True, exist_ok=True)

    # Heatmap 1: R_deficit
    R_grid = df.pivot(index="L", columns="chi_kappa", values="R_deficit").values
    X, Y = np.meshgrid(chi_kappa_vals, L_vals)

    plt.figure(figsize=(8, 6))
    cp = plt.contourf(X, Y, R_grid, levels=50, cmap="viridis")
    plt.colorbar(cp, label="Energy Deficit Ratio (R_deficit)")
    # Add contour for R_deficit = 1

    # Check if R_deficit=1 is within the range to plot contour safely
    if R_grid.min() <= 1.0 <= R_grid.max():
        plt.contour(X, Y, R_grid, levels=[1.0], colors='red', linewidths=2, linestyles='dashed')

    plt.title("Energy Deficit Window Phase Diagram")
    plt.xlabel(r"Information Coupling Strength ($\chi_\kappa$)")
    plt.ylabel("Spinal Length L (m)")

    plt.savefig(out_dir_fig / "phase_diagram_energy_deficit.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Heatmap 2: Cobb angle
    Cobb_grid = df.pivot(index="L", columns="chi_kappa", values="cobb_angle").values

    plt.figure(figsize=(8, 6))
    cp2 = plt.contourf(X, Y, Cobb_grid, levels=50, cmap="magma")
    plt.colorbar(cp2, label="Cobb Angle (degrees)")
    if R_grid.min() <= 1.0 <= R_grid.max():
        plt.contour(X, Y, R_grid, levels=[1.0], colors='white', linewidths=2, linestyles='dashed')

    plt.title("Scoliosis Emergence (Cobb Angle)")
    plt.xlabel(r"Information Coupling Strength ($\chi_\kappa$)")
    plt.ylabel("Spinal Length L (m)")

    plt.savefig(out_dir_fig / "phase_diagram_energy_deficit_cobb.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("Simulation completed successfully.")

if __name__ == "__main__":
    run_sweep()
