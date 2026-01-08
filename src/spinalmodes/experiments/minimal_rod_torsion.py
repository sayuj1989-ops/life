
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import tracemalloc
import csv

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams

def run_experiment():
    print("Starting minimal PyElastica rod torsion experiment...")
    print("Mapping protein/ECM parameters (chi_tau) to emergent torsion.")

    # 1. Define Information Field (e.g., sinusoidal modulation)
    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    # A simple sinusoidal info field
    I = np.sin(2 * np.pi * s / L)**2
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 2. Setup Simulation Parameters
    n_elements = 50
    final_time = 2.0
    dt = 1e-4

    # Sweep parameters: chi_tau (torsion coupling)
    # This represents PCP gene disruption or off-axis alignment
    chi_tau_values = [0.0, 1.0, 3.0, 5.0]
    results_summary = []

    # Output directory
    output_dir = Path("outputs/experiments/minimal_rod_torsion")
    output_dir.mkdir(parents=True, exist_ok=True)

    tracemalloc.start()
    start_time_total = time.time()

    for chi_t in chi_tau_values:
        # Define Parameters (Protein/ECM-inspired)
        params = CounterCurvatureParams(
            chi_E=0.5,
            chi_kappa=2.0, # Maintain some sagittal curvature
            chi_tau=chi_t, # Sweep torsion
            chi_M=0.0,
            scale_length=L
        )

        print(f"\nRunning simulation for chi_tau={chi_t}...")

        # Horizontal rod
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
        # Torsion is index 2 of kappa
        final_torsion = result.torsion[-1]
        avg_torsion = np.mean(np.abs(final_torsion))

        # Curvature is norm of first two components (bending)
        final_curvature = result.curvature[-1]
        avg_curvature = np.mean(final_curvature)

        # Store
        results_summary.append({
            "chi_tau": chi_t,
            "avg_torsion": avg_torsion,
            "avg_curvature": avg_curvature
        })

        print(f"  Avg Torsion: {avg_torsion:.4f}")
        print(f"  Avg Curvature: {avg_curvature:.4f}")

    end_time_total = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTotal Sweep Runtime: {end_time_total - start_time_total:.2f}s")
    print(f"Peak Memory: {peak_mem / 1024 / 1024:.2f} MB")

    # Save summary using CSV module
    csv_path = output_dir / "torsion_results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["chi_tau", "avg_torsion", "avg_curvature"])
        writer.writeheader()
        writer.writerows(results_summary)
    print(f"Results saved to {csv_path}")

    # Plot
    chi_t_list = [r["chi_tau"] for r in results_summary]
    avg_t_list = [r["avg_torsion"] for r in results_summary]
    avg_k_list = [r["avg_curvature"] for r in results_summary]

    plt.figure(figsize=(10, 5))

    # Plot 1: Chi_tau vs Avg Torsion
    plt.subplot(1, 2, 1)
    plt.plot(chi_t_list, avg_t_list, 'o-', color='purple', label="Avg Torsion")
    plt.xlabel("Torsion Coupling $\chi_\\tau$")
    plt.ylabel("Average Torsion ($m^{-1}$)")
    plt.title("Emergent Torsion from PCP Disruption")
    plt.grid(True)

    # Plot 2: Chi_tau vs Avg Curvature (Cross-talk check)
    plt.subplot(1, 2, 2)
    plt.plot(chi_t_list, avg_k_list, 's-', color='orange', label="Avg Curvature")
    plt.xlabel("Torsion Coupling $\chi_\\tau$")
    plt.ylabel("Average Curvature ($m^{-1}$)")
    plt.title("Impact on Sagittal Curvature")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "torsion_plot.png")
    print(f"Plot saved to {output_dir / 'torsion_plot.png'}")

    # Report
    with open(output_dir / "report.md", "w") as f:
        f.write("# Minimal Rod Torsion Experiment Report\n\n")
        f.write(f"- **Runtime**: {end_time_total - start_time_total:.2f}s\n")
        f.write(f"- **Peak Memory**: {peak_mem / 1024 / 1024:.2f} MB\n\n")
        f.write("## Parameter Sweep (Chi_Tau)\n\n")
        f.write("| chi_tau | avg_torsion | avg_curvature |\n")
        f.write("|---------|-------------|---------------|\n")
        for r in results_summary:
            f.write(f"| {r['chi_tau']} | {r['avg_torsion']:.4f} | {r['avg_curvature']:.4f} |\n")

    print(f"Report saved to {output_dir / 'report.md'}")

if __name__ == "__main__":
    run_experiment()
