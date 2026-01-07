
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import tracemalloc
import csv
import sys

# Ensure src is in path for imports
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.scoliosis_metrics import (
    compute_scoliosis_metrics,
    build_lateral_curvature_bump,
    ScoliosisMetrics
)

def run_experiment_improved():
    print("Starting improved PyElastica rod experiment with Scoliosis Metrics...")
    print("Mapping protein/ECM parameters to emergent curvature and scoliosis.")

    # 1. Define Information Field (e.g., sinusoidal modulation)
    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    # Sinusoidal information field
    I = np.sin(2 * np.pi * s / L)**2
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 2. Setup Simulation Parameters
    n_elements = 50
    final_time = 2.0
    dt = 1e-4

    # Sweep parameters: chi_kappa (geometric countercurvature)
    chi_kappa_values = [0.0, 1.0, 2.0, 3.0]
    results_summary = []

    # Output directory
    output_dir = Path("outputs/experiments/minimal_rod_sweep_improved")
    output_dir.mkdir(parents=True, exist_ok=True)

    tracemalloc.start()
    start_time_total = time.time()

    # Create a lateral bump to seed potential scoliosis
    # This represents a biological imperfection or asymmetry
    # Reduced epsilon_lat just in case, though 0.05 should be fine.
    kappa_lat = build_lateral_curvature_bump(s, epsilon_lat=0.05, center_hat=0.6, width_hat=0.12)

    for chi_k in chi_kappa_values:
        # Define Parameters (Protein/ECM-inspired)
        # chi_E: stiffness modulation (ECM densification)
        # chi_kappa: rest curvature modulation (Developmental shape programming)
        # chi_M: active moments (Muscle tone / Active stresses)
        params = CounterCurvatureParams(
            chi_E=0.5,
            chi_kappa=chi_k,
            chi_M=0.0,
            scale_length=L
        )

        print(f"\nRunning simulation for chi_kappa={chi_k}...")

        # Horizontal rod to see gravity sag vs countercurvature
        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=1e6,
            radius=0.02,
            rho=1000,
            gravity=9.81,
            base_direction=(1.0, 0.0, 0.0), # Rod along X
            normal=(0.0, 1.0, 0.0),       # Normal along Y -> d1=Y
            kappa_lat=kappa_lat           # Lateral curvature (about Z)
        )

        result = system.run_simulation(final_time=final_time, dt=dt, save_every=100)

        # Metrics
        # 1. Sagittal (Z) Metrics
        # centerline is (time, n_nodes, 3), so final_centerline is (n_nodes, 3)
        final_centerline = result.centerline[-1]
        tip_deflection_z = final_centerline[-1, 2] # Sagittal vertical (Tip Z)

        # 2. Lateral (Y) Metrics (Scoliosis)
        # x is longitudinal (dim 0), y is lateral (dim 1)
        x_coords = final_centerline[:, 0]
        y_coords = final_centerline[:, 1]

        # Debugging
        print(f"  Debug: x_coords range: {x_coords.min():.4f} to {x_coords.max():.4f}")
        print(f"  Debug: y_coords range: {y_coords.min():.4f} to {y_coords.max():.4f}")

        scol_metrics = compute_scoliosis_metrics(z=x_coords, y=y_coords)

        # Store
        results_summary.append({
            "chi_kappa": chi_k,
            "tip_deflection_z": tip_deflection_z,
            "S_lat": scol_metrics.S_lat,
            "cobb_angle": scol_metrics.cobb_like_deg,
            "lat_dev_max": scol_metrics.lat_dev_max
        })

        print(f"  Tip Deflection Z: {tip_deflection_z:.4f} m")
        print(f"  S_lat: {scol_metrics.S_lat:.4f}")
        print(f"  Cobb Angle: {scol_metrics.cobb_like_deg:.2f} deg")

    end_time_total = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTotal Sweep Runtime: {end_time_total - start_time_total:.2f}s")
    print(f"Peak Memory: {peak_mem / 1024 / 1024:.2f} MB")

    # Save summary using CSV module
    csv_path = output_dir / "sweep_results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["chi_kappa", "tip_deflection_z", "S_lat", "cobb_angle", "lat_dev_max"])
        writer.writeheader()
        writer.writerows(results_summary)
    print(f"Sweep results saved to {csv_path}")

    # Plot
    chi_k_list = [r["chi_kappa"] for r in results_summary]
    tip_z_list = [r["tip_deflection_z"] for r in results_summary]
    s_lat_list = [r["S_lat"] for r in results_summary]
    cobb_list = [r["cobb_angle"] for r in results_summary]

    plt.figure(figsize=(15, 5))

    # Plot 1: Chi_kappa vs Sagittal Deflection
    plt.subplot(1, 3, 1)
    plt.plot(chi_k_list, tip_z_list, 'o-', label="Tip Z")
    plt.xlabel("Coupling Gain $\chi_\kappa$")
    plt.ylabel("Sagittal Deflection Z (m)")
    plt.title("Counter-Curvature Effect (Sagittal)")
    plt.grid(True)

    # Plot 2: Chi_kappa vs S_lat
    plt.subplot(1, 3, 2)
    plt.plot(chi_k_list, s_lat_list, 's-', color='orange', label="S_lat")
    plt.xlabel("Coupling Gain $\chi_\kappa$")
    plt.ylabel("Lateral Scoliosis Index ($S_{lat}$)")
    plt.title("Lateral Asymmetry (Scoliosis)")
    plt.grid(True)

    # Plot 3: Chi_kappa vs Cobb Angle
    plt.subplot(1, 3, 3)
    plt.plot(chi_k_list, cobb_list, '^-', color='green', label="Cobb Angle")
    plt.xlabel("Coupling Gain $\chi_\kappa$")
    plt.ylabel("Cobb Angle (deg)")
    plt.title("Cobb Angle")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "sweep_plot.png")
    print(f"Sweep plot saved to {output_dir / 'sweep_plot.png'}")

    # Report using Markdown table
    with open(output_dir / "report.md", "w") as f:
        f.write("# Improved Rod Experiment Report\n\n")
        f.write(f"- **Runtime**: {end_time_total - start_time_total:.2f}s\n")
        f.write(f"- **Peak Memory**: {peak_mem / 1024 / 1024:.2f} MB\n\n")
        f.write("## Parameter Sweep (Chi_Kappa)\n\n")
        f.write("| chi_kappa | tip_deflection_z | S_lat | cobb_angle |\n")
        f.write("|-----------|------------------|-------|------------|\n")
        for r in results_summary:
            f.write(f"| {r['chi_kappa']} | {r['tip_deflection_z']:.4f} | {r['S_lat']:.4f} | {r['cobb_angle']:.2f} |\n")

    print(f"Report saved to {output_dir / 'report.md'}")

if __name__ == "__main__":
    run_experiment_improved()
