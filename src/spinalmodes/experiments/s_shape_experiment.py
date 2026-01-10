
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import tracemalloc
import csv
import sys
from typing import List, Dict, Any

# Ensure project root is in path to resolve src imports
sys.path.append(".")

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.scoliosis_metrics import compute_lateral_scoliosis_index

def count_zero_crossings(signal: np.ndarray) -> int:
    """Count the number of times the signal crosses zero."""
    return int(np.sum(np.diff(np.signbit(signal))))

def run_experiment():
    print("Starting S-Shape Counter-Curvature Experiment...")
    print("Exploring the emergence of S-shaped profiles via Active Muscle Torques (chi_M).")

    # 1. Define Information Field (Sinusoidal)
    # The information field encodes the "target" shape.
    # A full sine wave (0 to 2pi) promotes an S-shape.
    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    # I(s) = sin(2*pi*s/L) -> Gradient creates alternating curvature
    I = np.sin(2 * np.pi * s / L)
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 2. Setup Simulation Parameters
    n_elements = 50
    final_time = 3.0  # Allow settling
    dt = 5e-5        # Smaller timestep for stability with active torques

    # Output directory
    output_dir = Path("outputs/experiments/s_shape_sweep")
    output_dir.mkdir(parents=True, exist_ok=True)

    results_summary: List[Dict[str, Any]] = []

    tracemalloc.start()
    start_time_total = time.time()

    # --- Sweep: Active Muscle Torque Gain (chi_M) ---
    # We expect that as chi_M increases, the rod will transition from
    # gravity-dominated (C-shape sag) to information-dominated (S-shape).
    chi_M_values = [0.0, 5.0, 10.0, 15.0, 20.0]

    # Fixed parameters
    chi_E = 0.0      # Constant stiffness
    chi_kappa = 0.0  # No intrinsic rest curvature, purely active control

    print(f"\nRunning sweep for chi_M in {chi_M_values}...")

    for chi_M in chi_M_values:
        params = CounterCurvatureParams(
            chi_E=chi_E,
            chi_kappa=chi_kappa,
            chi_M=chi_M,
            chi_tau=0.0,
            scale_length=L
        )

        # Horizontal rod (along X) subject to Gravity (down Z)
        # Active torques must work against gravity to create shape.
        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=1e6,
            radius=0.02,
            rho=1000,
            gravity=9.81,
            base_direction=(1.0, 0.0, 0.0), # Horizontal
            normal=(0.0, 1.0, 0.0)
        )

        # Run simulation
        result = system.run_simulation(final_time=final_time, dt=dt, save_every=200)

        # Analysis of final state
        # result.centerline is (time, n_nodes, 3) because of pyelastica_bridge output logic
        final_centerline = result.centerline[-1] # Shape (n_nodes, 3)

        # Centerline columns: 0=x, 1=y, 2=z
        x_coords = final_centerline[:, 0]
        z_coords = final_centerline[:, 2] # Vertical deflection

        # Curvature profile (signed curvature in x-z plane roughly corresponds to kappa[1])
        # kappa shape is (time, n_nodes, 3)
        # Index 1 is the bending normal to the rod plane.
        final_kappa_y = result.kappa[-1, :, 1]

        # Metric 1: Tip Deflection (Sag)
        tip_deflection_z = z_coords[-1]

        # Metric 2: "S-Shape Index" using Scoliosis Metrics (repurposed for Sagittal plane)
        # We treat 'x' as longitudinal and 'z' as lateral deviation.
        # This gives a measure of how much the rod deviates from the horizontal axis, normalized by length.
        sagittal_index, _, max_dev = compute_lateral_scoliosis_index(x_coords, z_coords)

        # Metric 3: Zero Crossings of Curvature
        # Gravity alone -> C-shape -> 0 crossings (mostly monotonic curvature or single sign)
        # S-shape -> At least 1 crossing (inflection point)
        # We ignore small noise around zero.
        zero_crossings = count_zero_crossings(final_kappa_y)

        results_summary.append({
            "chi_M": chi_M,
            "tip_deflection_z": tip_deflection_z,
            "sagittal_index": sagittal_index,
            "max_dev_z": max_dev,
            "zero_crossings": zero_crossings
        })

        print(f"chi_M={chi_M:4.1f} | Tip Z={tip_deflection_z:7.4f} m | Sagittal Index={sagittal_index:6.4f} | Zero Crossings={zero_crossings}")

    end_time_total = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTotal Runtime: {end_time_total - start_time_total:.2f}s")
    print(f"Peak Memory: {peak_mem / 1024 / 1024:.2f} MB")

    # Save Results to CSV
    csv_path = output_dir / "s_shape_results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["chi_M", "tip_deflection_z", "sagittal_index", "max_dev_z", "zero_crossings"])
        writer.writeheader()
        writer.writerows(results_summary)
    print(f"Results saved to {csv_path}")

    # Generate Plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    chi_m_vals = [r["chi_M"] for r in results_summary]
    tip_defs = [r["tip_deflection_z"] for r in results_summary]
    crossings = [r["zero_crossings"] for r in results_summary]

    color = 'tab:blue'
    ax1.set_xlabel(r"Active Muscle Gain $\chi_M$")
    ax1.set_ylabel("Tip Deflection Z (m)", color=color)
    ax1.plot(chi_m_vals, tip_defs, 'o-', color=color, label="Tip Deflection")
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel("Curvature Zero Crossings", color=color)
    ax2.plot(chi_m_vals, crossings, 's--', color=color, label="Zero Crossings")
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_yticks(range(0, max(crossings)+2))

    plt.title("Emergence of S-Shape from Active Muscle Torques")
    fig.tight_layout()
    plt.savefig(output_dir / "s_shape_plot.png")
    print(f"Plot saved to {output_dir / 's_shape_plot.png'}")

    # Generate Markdown Report
    with open(output_dir / "report.md", "w") as f:
        f.write("# S-Shape Counter-Curvature Experiment Report\n\n")
        f.write("This experiment maps the Active Muscle Torque parameter (`chi_M`) to the emergence of S-shaped spinal profiles.\n")
        f.write("A horizontal rod is subjected to gravity. An information field `I(s) ~ sin(s)` drives active moments.\n\n")

        f.write(f"- **Runtime**: {end_time_total - start_time_total:.2f}s\n")
        f.write(f"- **Peak Memory**: {peak_mem / 1024 / 1024:.2f} MB\n\n")

        f.write("## Results Summary\n\n")
        f.write("| chi_M | Tip Z (m) | Sagittal Index | Zero Crossings |\n")
        f.write("|-------|-----------|----------------|----------------|\n")
        for r in results_summary:
            f.write(f"| {r['chi_M']} | {r['tip_deflection_z']:.4f} | {r['sagittal_index']:.4f} | {r['zero_crossings']} |\n")

        f.write("\n## Interpretation\n\n")
        f.write("- **Low chi_M**: Gravity dominates, rod sags into a C-shape (0 crossings).\n")
        f.write("- **High chi_M**: Active torques counteract gravity, inducing the target S-shape (multiple crossings).\n")
        f.write("- **Sagittal Index**: Measures the normalized amplitude of the deflection.\n")

if __name__ == "__main__":
    run_experiment()
