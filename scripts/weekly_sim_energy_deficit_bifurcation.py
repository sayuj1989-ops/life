#!/usr/bin/env python3
"""
Weekly Simulation: Energy Deficit Bifurcation.

Performs a 2D parameter sweep of the Energy Deficit Window across (χ_κ, L) space.
Generates a phase diagram showing where AIS vulnerability is highest (Energy Deficit > Supply).

Hypothesis ID: H_2026_02_08_EnergyPhase
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path if needed (though usually not needed if running from root)
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from spinalmodes.countercurvature.api import (
        CounterCurvatureRodSystem,
        CounterCurvatureParams,
        InfoField1D,
        geodesic_curvature_deviation
    )
except ImportError:
    # Fallback to local import if structure is different
    sys.path.append("src")
    from spinalmodes.countercurvature.api import (
        CounterCurvatureRodSystem,
        CounterCurvatureParams,
        InfoField1D,
        geodesic_curvature_deviation
    )

# Constants
RHO = 1100.0       # kg/m^3
A_REF = 0.001      # m^2 (Fixed area)
L_REF = 0.4        # m (Reference length for scaling, though not used here)
G = 9.81           # m/s^2
E0 = 1.0e9         # Pa (1.0 GPa)
ANISOTROPY = 2.0   # Moderate protection
ETA_A = 1.0        # Scaling factor for P_counter

# IEC Bimodal Gaussian Parameters
A_c = 0.5; s_c = 0.80; sigma_c = 0.08
A_l = 0.7; s_l = 0.25; sigma_l = 0.10
I_0 = 0.3

def get_bimodal_gaussian_field(s, L):
    """
    Computes the bimodal Gaussian information field I(s) and its gradient dI/ds.
    s: array of spatial coordinates [0, L]
    L: total length
    """
    s_norm = s / L

    # Field I(s)
    I_c = A_c * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    I_l = A_l * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))
    I = I_c + I_l + I_0

    # Gradient dI/ds
    # d/ds = (d/ds_norm) * (ds_norm/ds) = (d/ds_norm) * (1/L)
    dIc_dsn = I_c * (-(s_norm - s_c) / sigma_c**2) * np.exp(-((s_norm - s_c)**2) / (2 * sigma_c**2))
    dIl_dsn = I_l * (-(s_norm - s_l) / sigma_l**2) * np.exp(-((s_norm - s_l)**2) / (2 * sigma_l**2))
    # Corrected gradient calculation above (multiplying by exp term)

    dIds = (dIc_dsn + dIl_dsn) / L

    return I, dIds

def run_single_simulation(L, chi_kappa, anisotropy, initial_lateral_defect=0.03):
    """
    Runs a single simulation for a given length L and coupling strength chi_kappa.
    Returns the final curvature state (kappa) and metrics.
    """
    # 1. Geometry Scaling
    current_A = A_REF
    radius = np.sqrt(current_A / np.pi)
    n_elements = 20

    # 2. Setup Information Field
    s = np.linspace(0, L, n_elements + 1)
    I, dIds = get_bimodal_gaussian_field(s, L)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 3. Setup Parameters
    params = CounterCurvatureParams(
        chi_kappa=chi_kappa,
        chi_tau=0.0,
        chi_E=0.0,
        chi_M=0.0,
        scale_length=L
    )

    # 4. Create System with intrinsic curvature
    kappa_gen = np.zeros((3, n_elements + 1))
    kappa_gen[1, :] = 2.0  # Natural Kyphosis (Sagittal)
    if initial_lateral_defect > 0:
        kappa_gen[0, :] = initial_lateral_defect # Lateral Defect

    try:
        rod_system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=E0,
            rho=RHO,
            radius=radius,
            kappa_gen=kappa_gen,
            gravity=G,
            stiffness_anisotropy=anisotropy
        )

        # 5. Run Simulation
        duration = 0.5 # Fast settle
        dt = 2e-4

        result = rod_system.run_simulation(
            final_time=duration,
            dt=dt,
            save_every=max(1, int(duration/dt/5)),
            boundary_condition="fixed",
            progress_bar=False,
            damping_constant=2.0
        )

        # Return final kappa (n_nodes, 3) and simulation metrics
        metrics = result.compute_final_metrics()
        final_kappa = result.kappa[-1] # (n_nodes, 3)

        return final_kappa, metrics

    except Exception as e:
        print(f"Simulation failed for L={L}, chi={chi_kappa}: {e}")
        return None, {}

def run_sweep():
    # Parameters
    chi_vals = np.linspace(0.01, 0.10, 20)
    L_vals = np.linspace(0.25, 0.55, 20)

    results = []

    # Create output directory
    output_dir = Path("outputs/thermodynamic_cost")
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = Path("outputs/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Energy Deficit Sweep: {len(chi_vals)}x{len(L_vals)} runs")

    for i, chi in enumerate(chi_vals):
        print(f"Row {i+1}/{len(chi_vals)} (chi={chi:.3f})...", end="", flush=True)
        for L in L_vals:
            current_A = A_REF

            # 1. Active Run (chi_kappa = chi)
            kappa_active, metrics_active = run_single_simulation(L, chi, ANISOTROPY, initial_lateral_defect=0.03)

            # 2. Passive Run (chi_kappa = 0.0)
            kappa_passive, _ = run_single_simulation(L, 0.0, ANISOTROPY, initial_lateral_defect=0.03)

            if kappa_active is not None and kappa_passive is not None:
                # 3. Compute P_counter
                # Mean Squared Difference of curvature vectors
                diff = kappa_active - kappa_passive # (N, 3)
                msd_kappa = np.mean(np.sum(diff**2, axis=1)) # Sum over components, mean over nodes

                # P_counter definition based on energy functional approximation
                # Scales with Volume * E * Curvature^2 ~ A*L * E * (1/L^2) ~ A/L if A fixed?
                # Using the user provided scaling L^2 in the task description for P_counter?
                # User task step 1 says: P_counter(χ_κ, L) — metabolic power required for countercurvature
                # Step 2 says: P_counter scaling (L^{2-3})
                # The formula used in existing script was: ETA_A * RHO * current_A * G * (L**2) * msd_kappa
                # Let's stick to this formula as it seems to be the intended one for this sweep.
                P_counter = ETA_A * RHO * current_A * G * (L**2) * msd_kappa

                # 4. Metrics
                cobb_angle = metrics_active.get("cobb_angle", 0.0)
                D_geo = np.sqrt(msd_kappa)

                results.append({
                    "chi_kappa": chi,
                    "L": L,
                    "P_counter": P_counter,
                    "Cobb": cobb_angle,
                    "D_geo": D_geo
                })
        print(" Done.")

    df = pd.DataFrame(results)

    # Compute Supply S_proprio
    # Reference point: L=0.35, chi=0.05
    # Find closest point in results
    ref_idx = ((df['L']-0.35).abs() + (df['chi_kappa']-0.05).abs()).idxmin()
    S0_ref = df.loc[ref_idx, 'P_counter']

    print(f"\nReference S0 (at L=0.35, chi=0.05): {S0_ref:.6e}")

    # Calculate Supply and R_deficit
    # S_proprio = S0 * (L/0.35)^0.7
    # Note: Use L_0 = 0.35 as reference length for supply normalization
    L0_supply = 0.35
    df['S_proprio'] = S0_ref * (df['L'] / L0_supply)**0.7
    df['R_deficit'] = df['P_counter'] / df['S_proprio']

    # Save CSV
    csv_path = output_dir / "phase_diagram_energy_deficit.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    generate_plots(df, figures_dir)

def generate_plots(df, output_dir):
    # Pivot for heatmaps
    # Ensure index/columns are sorted
    pivot_R = df.pivot(index="chi_kappa", columns="L", values="R_deficit")
    pivot_Cobb = df.pivot(index="chi_kappa", columns="L", values="Cobb")

    # The pivot might return unsorted axes if data wasn't sorted, but linspace is sorted.
    # Just to be safe, sort index/columns
    pivot_R = pivot_R.sort_index(axis=0).sort_index(axis=1)
    pivot_Cobb = pivot_Cobb.sort_index(axis=0).sort_index(axis=1)

    chi_axis = pivot_R.index
    L_axis = pivot_R.columns
    X, Y = np.meshgrid(L_axis, chi_axis)

    # Plot 1: R_deficit
    plt.figure(figsize=(10, 8))
    # Use 'RdYlBu_r' so Red is high (Deficit), Blue is low (Surplus)
    # R > 1 is Deficit (Red)
    cp = plt.contourf(X, Y, pivot_R.values, levels=20, cmap='RdYlBu_r')
    plt.colorbar(cp, label=r'Energy Deficit Ratio $R_{deficit}$')

    # Contour line at R=1
    # Check if we have values crossing 1.0
    if pivot_R.values.min() < 1.0 < pivot_R.values.max():
        plt.contour(X, Y, pivot_R.values, levels=[1.0], colors='k', linewidths=2, linestyles='--')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_\kappa$')
    plt.title('Energy Deficit Phase Diagram')

    # Add annotation for R>1 region
    plt.text(0.3, 0.08, 'Deficit Window (R > 1)', color='black', fontweight='bold',
             bbox=dict(facecolor='white', alpha=0.5))

    plt.savefig(output_dir / "phase_diagram_energy_deficit.png", dpi=150)
    plt.close()

    # Plot 2: Cobb Angle
    plt.figure(figsize=(10, 8))
    cp2 = plt.contourf(X, Y, pivot_Cobb.values, levels=20, cmap='viridis')
    plt.colorbar(cp2, label='Cobb Angle (degrees)')

    plt.xlabel('Spinal Length L (m)')
    plt.ylabel(r'Coupling Strength $\chi_\kappa$')
    plt.title('Scoliosis Emergence Phase Diagram')

    plt.savefig(output_dir / "phase_diagram_energy_deficit_cobb.png", dpi=150)
    plt.close()
    print("Plots saved.")

if __name__ == "__main__":
    run_sweep()
