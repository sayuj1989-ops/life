
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import tracemalloc
import csv

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics

def run_experiment():
    print("Starting minimal PyElastica rod parameter sweep...")
    print("Mapping protein/ECM parameters (chi_kappa, chi_M) to rod curvature.")

    # 1. Define Information Field (e.g., sinusoidal modulation)
    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    # A simple sinusoidal info field: high information -> stiffer or more curved
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
    output_dir = Path("outputs/experiments/minimal_rod_sweep")
    output_dir.mkdir(parents=True, exist_ok=True)

    tracemalloc.start()
    start_time_total = time.time()

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
            base_direction=(1.0, 0.0, 0.0),
            normal=(0.0, 1.0, 0.0)
        )

        result = system.run_simulation(final_time=final_time, dt=dt, save_every=100)

        # Metrics
        final_curvature = result.curvature[-1]
        avg_curvature = np.mean(final_curvature)

        # Sagittal deflection (z-coordinate)
        final_centerline = result.centerline[-1]
        tip_deflection_z = final_centerline[2, -1] # Sagittal vertical

        # Store
        results_summary.append({
            "chi_kappa": chi_k,
            "avg_curvature": avg_curvature,
            "tip_deflection_z": tip_deflection_z
        })

        print(f"  Avg Curvature: {avg_curvature:.4f}")
        print(f"  Tip Deflection Z: {tip_deflection_z:.4f} m")

    end_time_total = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTotal Sweep Runtime: {end_time_total - start_time_total:.2f}s")
    print(f"Peak Memory: {peak_mem / 1024 / 1024:.2f} MB")

    # Save summary using CSV module
    csv_path = output_dir / "sweep_results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["chi_kappa", "avg_curvature", "tip_deflection_z"])
        writer.writeheader()
        writer.writerows(results_summary)
    print(f"Sweep results saved to {csv_path}")

    # Plot
    chi_k_list = [r["chi_kappa"] for r in results_summary]
    tip_z_list = [r["tip_deflection_z"] for r in results_summary]
    avg_k_list = [r["avg_curvature"] for r in results_summary]

    plt.figure(figsize=(10, 5))

    # Plot 1: Chi_kappa vs Tip Deflection
    plt.subplot(1, 2, 1)
    plt.plot(chi_k_list, tip_z_list, 'o-', label="Tip Z")
    plt.xlabel("Coupling Gain $\chi_\kappa$")
    plt.ylabel("Tip Deflection Z (m)")
    plt.title("Effect of Geometric Countercurvature")
    plt.grid(True)

    # Plot 2: Chi_kappa vs Avg Curvature
    plt.subplot(1, 2, 2)
    plt.plot(chi_k_list, avg_k_list, 's-', color='orange', label="Avg Curvature")
    plt.xlabel("Coupling Gain $\chi_\kappa$")
    plt.ylabel("Average Curvature ($m^{-1}$)")
    plt.title("Emergent Curvature")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "sweep_plot.png")
    print(f"Sweep plot saved to {output_dir / 'sweep_plot.png'}")

    # 3. Demonstration of Active Moments (Chi_M)
    print("\nDemonstrating Active Moments (Chi_M)...")
    params_active = CounterCurvatureParams(
        chi_E=0.0,
        chi_kappa=0.0,
        chi_M=5.0, # Active torque
        scale_length=L
    )

    system_active = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params_active,
            length=L,
            n_elements=n_elements,
            E0=1e6,
            radius=0.02,
            rho=1000,
            gravity=9.81, # With gravity
            base_direction=(1.0, 0.0, 0.0),
            normal=(0.0, 1.0, 0.0)
    )
    result_active = system_active.run_simulation(final_time=final_time, dt=dt, save_every=100)
    tip_active = result_active.centerline[-1, 2, -1]
    print(f"  Tip Deflection Z (Active Moments): {tip_active:.4f} m")

    # Save active moment result
    np.save(output_dir / "active_centerline.npy", result_active.centerline)

    # Report using Markdown table
    with open(output_dir / "report.md", "w") as f:
        f.write("# Minimal Rod Experiment Report\n\n")
        f.write(f"- **Runtime**: {end_time_total - start_time_total:.2f}s\n")
        f.write(f"- **Peak Memory**: {peak_mem / 1024 / 1024:.2f} MB\n\n")
        f.write("## Parameter Sweep (Chi_Kappa)\n\n")
        f.write("| chi_kappa | avg_curvature | tip_deflection_z |\n")
        f.write("|-----------|---------------|------------------|\n")
        for r in results_summary:
            f.write(f"| {r['chi_kappa']} | {r['avg_curvature']:.4f} | {r['tip_deflection_z']:.4f} |\n")

        f.write("\n\n## Active Moments Demonstration\n")
        f.write(f"- Chi_M: 5.0\n")
        f.write(f"- Tip Deflection Z: {tip_active:.4f} m\n")

    print(f"Report saved to {output_dir / 'report.md'}")

if __name__ == "__main__":
    run_experiment()
