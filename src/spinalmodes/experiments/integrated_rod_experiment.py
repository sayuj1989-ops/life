"""
Integrated PyElastica experiment for Biological Counter-Curvature.

This module implements a reproducible, minimal experiment that maps protein/ECM-inspired
parameters (stiffness, preferred curvature, active moments) to emergent curvature
and torsion outputs. It unifies previous experiments into a single pedagogical
sweep, connecting directly to `scoliosis_metrics` for standardized reporting.

Biological Mappings:
- chi_kappa: Geometric Counter-Curvature (e.g. from pre-strained ECM/Collagen alignment).
- chi_M:     Active Muscle Torque (e.g. from YAP/TAZ-mediated myogenesis).
- chi_tau:   Torsional Coupling (e.g. from Cilia/PCP defects like PTK7/Vangl2).

The simulation sets up a Cosserat rod under gravity and applies these biological
biases via an 'Information Field' (spatial gene expression gradient).
"""

import sys
import time
import csv
import tracemalloc
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import asdict

# Ensure project root is in path
sys.path.append(".")

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem, PYELASTICA_AVAILABLE
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics

def run_experiment():
    # -------------------------------------------------------------------------
    # 0. Environment Check
    # -------------------------------------------------------------------------
    if not PYELASTICA_AVAILABLE:
        print("ERROR: PyElastica is not installed in the environment.")
        print("This experiment requires the PyElastica Cosserat rod solver.")
        print("\nTo install:")
        print("  pip install pyelastica")
        print("  # or")
        print("  pip install -r requirements.txt")
        print("\nReference: https://github.com/GazzolaLab/PyElastica")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # 1. Setup & Configuration
    # -------------------------------------------------------------------------
    print("Starting Integrated PyElastica Counter-Curvature Experiment...")
    output_dir = Path("outputs/experiments/integrated_rod_sweep")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Physical Parameters
    L = 1.0                 # Length (m)
    n_elements = 50         # Discrete elements
    radius = 0.02           # Radius (m)
    E0 = 1e6                # Young's Modulus (Pa)
    rho = 1000              # Density (kg/m^3)
    gravity = 9.81          # Gravity (m/s^2)
    final_time = 3.0        # Simulation time (s) - enough to settle
    dt = 5e-5               # Timestep (s)

    # Information Field: Sinusoidal (representing segmented HOX expression)
    n_points = 200
    s_grid = np.linspace(0, L, n_points)
    # I(s) = sin^2(2*pi*s/L) creates a periodic signal with positive peaks
    # dI/ds = (4*pi/L)*sin*cos -> Alternating gradients
    I = np.sin(2 * np.pi * s_grid / L)**2
    dIds = np.gradient(I, s_grid)
    info_field = InfoField1D(s=s_grid, I=I, dIds=dIds)

    # -------------------------------------------------------------------------
    # 2. Parameter Sweeps
    # -------------------------------------------------------------------------
    # We define three regimes to test the "Triple Theory":
    # A. Passive Geometric Support (chi_kappa)
    # B. Active Muscular Correction (chi_M)
    # C. Torsional Instability (chi_tau)

    sweeps = [
        # (Name, Param_Key, Range)
        ("Geometric_Support", "chi_kappa", [0.0, 1.0, 2.0, 3.0]),
        ("Active_Correction", "chi_M",     [0.0, 5.0, 10.0, 15.0]),
        ("Torsional_Defect",  "chi_tau",   [0.0, 0.5, 1.0, 1.5])
    ]

    results_data = []

    # Start Resource Monitoring
    tracemalloc.start()
    start_time_total = time.time()

    for sweep_name, param_key, values in sweeps:
        print(f"\n--- Running Sweep: {sweep_name} ({param_key}) ---")

        for val in values:
            # Base parameters (everything zero)
            # chi_E is fixed at 0.5 (stiffness modulation enabled)
            params_dict = {
                "chi_E": 0.5,
                "chi_kappa": 0.0,
                "chi_M": 0.0,
                "chi_tau": 0.0,
                "scale_length": L
            }
            # Update the sweep variable
            params_dict[param_key] = val

            params = CounterCurvatureParams(**params_dict)

            # Initialize System
            # Rod oriented along X, Gravity in -Z.
            # Sagittal plane is X-Z. Coronal plane is X-Y.
            system = CounterCurvatureRodSystem.from_iec(
                info=info_field,
                params=params,
                length=L,
                n_elements=n_elements,
                E0=E0,
                radius=radius,
                rho=rho,
                gravity=gravity,
                base_direction=(1.0, 0.0, 0.0), # Along X
                normal=(0.0, 1.0, 0.0)          # Normal Y
            )

            # Run Simulation
            sim_result = system.run_simulation(
                final_time=final_time,
                dt=dt,
                save_every=500 # Sparse saving
            )

            # -----------------------------------------------------------------
            # 3. Analysis & Metrics
            # -----------------------------------------------------------------
            # Extract final configuration
            final_centerline = sim_result.centerline[-1] # (n_nodes, 3)
            x = final_centerline[:, 0]
            y = final_centerline[:, 1]
            z = final_centerline[:, 2]

            # Sagittal Metrics (Counter-Curvature Plane X-Z)
            # We treat 'z' as the lateral deviation from the x-axis for metric calc
            sagittal_metrics = compute_scoliosis_metrics(z=x, y=z)

            # Coronal Metrics (Scoliosis Plane X-Y)
            coronal_metrics = compute_scoliosis_metrics(z=x, y=y)

            # Emergent Curvature/Torsion
            avg_curvature = np.mean(sim_result.curvature[-1])
            avg_torsion = np.mean(np.abs(sim_result.torsion[-1]))

            # Store Result
            entry = {
                "sweep": sweep_name,
                "param": param_key,
                "value": val,
                "tip_deflection_z": z[-1],
                "sagittal_index": sagittal_metrics.S_lat, # "Counter-Curvature Index"
                "sagittal_cobb": sagittal_metrics.cobb_like_deg,
                "coronal_index": coronal_metrics.S_lat,   # "Scoliosis Index"
                "avg_curvature": avg_curvature,
                "avg_torsion": avg_torsion
            }
            results_data.append(entry)

            print(f"[{param_key}={val}] Tip Z: {z[-1]:.3f} m | Sagittal Index: {sagittal_metrics.S_lat:.3f} | Torsion: {avg_torsion:.2f}")

    # End Resource Monitoring
    end_time_total = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    runtime = end_time_total - start_time_total
    peak_mem_mb = peak_mem / 1024 / 1024

    print(f"\nTotal Runtime: {runtime:.2f}s")
    print(f"Peak Memory: {peak_mem_mb:.2f} MB")

    # -------------------------------------------------------------------------
    # 4. Reporting
    # -------------------------------------------------------------------------

    # Save CSV
    csv_path = output_dir / "integrated_sweep_results.csv"
    keys = results_data[0].keys()
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results_data)
    print(f"Saved CSV to {csv_path}")

    # Generate Markdown Report
    report_path = output_dir / "report.md"
    with open(report_path, "w") as f:
        f.write("# Integrated Biological Counter-Curvature Experiment\n\n")
        f.write("A minimal reproducible experiment mapping biological parameters to spinal geometry.\n\n")
        f.write(f"- **Date**: {time.strftime('%Y-%m-%d')}\n")
        f.write(f"- **Runtime**: {runtime:.2f} s\n")
        f.write(f"- **Peak Memory**: {peak_mem_mb:.2f} MB\n\n")

        f.write("## 1. Geometric Support (chi_kappa)\n")
        f.write("Simulates pre-strained ECM or collagen alignment resisting gravity.\n\n")
        write_table(f, [r for r in results_data if r["sweep"] == "Geometric_Support"])

        f.write("\n## 2. Active Correction (chi_M)\n")
        f.write("Simulates YAP/TAZ-mediated muscle tension generation.\n\n")
        write_table(f, [r for r in results_data if r["sweep"] == "Active_Correction"])

        f.write("\n## 3. Torsional Defect (chi_tau)\n")
        f.write("Simulates PCP/Ciliary defects introducing twist.\n\n")
        write_table(f, [r for r in results_data if r["sweep"] == "Torsional_Defect"])

    print(f"Saved Report to {report_path}")

    # Generate Plot
    generate_plots(results_data, output_dir)

def write_table(f, rows):
    if not rows: return
    headers = ["value", "tip_deflection_z", "sagittal_index", "avg_torsion"]
    f.write("| " + " | ".join(headers) + " |\n")
    f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
    for r in rows:
        f.write(f"| {r['value']} | {r['tip_deflection_z']:.4f} | {r['sagittal_index']:.4f} | {r['avg_torsion']:.4f} |\n")

def generate_plots(results, output_dir):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Plot 1: Geometric Support (Sagittal Index vs chi_kappa)
    data = [r for r in results if r["sweep"] == "Geometric_Support"]
    axes[0].plot([r["value"] for r in data], [r["sagittal_index"] for r in data], 'o-')
    axes[0].set_xlabel(r"$\chi_\kappa$ (Geometry)")
    axes[0].set_ylabel("Sagittal Index (S-Shape)")
    axes[0].set_title("Geometric Counter-Curvature")
    axes[0].grid(True)

    # Plot 2: Active Correction (Tip Deflection vs chi_M)
    data = [r for r in results if r["sweep"] == "Active_Correction"]
    axes[1].plot([r["value"] for r in data], [r["tip_deflection_z"] for r in data], 's-', color='green')
    axes[1].set_xlabel(r"$\chi_M$ (Muscle)")
    axes[1].set_ylabel("Tip Deflection Z (m)")
    axes[1].set_title("Active Gravity Resistance")
    axes[1].grid(True)

    # Plot 3: Torsional Defect (Torsion vs chi_tau)
    data = [r for r in results if r["sweep"] == "Torsional_Defect"]
    axes[2].plot([r["value"] for r in data], [r["avg_torsion"] for r in data], '^-', color='red')
    axes[2].set_xlabel(r"$\chi_\tau$ (PCP/Cilia)")
    axes[2].set_ylabel("Average Torsion ($m^{-1}$)")
    axes[2].set_title("Emergent Torsion")
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "integrated_sweep_plot.png")
    print(f"Saved Plot to {output_dir / 'integrated_sweep_plot.png'}")

if __name__ == "__main__":
    run_experiment()
