import csv
import sys
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Ensure project root is in path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from scripts.experiments.experiment_utils import StandardExperimentParser, setup_experiment
from src.spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation


def main():
    parser = StandardExperimentParser(
        description="Sweep active_curvature to test S-shape emergence under gravity and anisotropy."
    )
    args = parser.parse_args()
    out_dir = setup_experiment(args)

    print("Starting Growth S-Shape Emergence Sweep...")

    # Set fixed seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    if args.quick:
        active_curvatures = np.linspace(0.0, 10.0, 3)
    else:
        # Run a sweep of 10 points
        active_curvatures = np.linspace(0.0, 15.0, 10)

    # Fixed Parameters
    fixed_anisotropy = 3.0  # High lateral stiffness
    gravity = 9.81
    duration = 2.0
    dt = 1e-4
    n_elements = 50

    results_summary = []

    # Save Params
    with open(out_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter", "Value"])
        writer.writerow(["anisotropy", fixed_anisotropy])
        writer.writerow(["gravity", gravity])
        writer.writerow(["duration", duration])
        writer.writerow(["dt", dt])
        writer.writerow(["n_elements", n_elements])
        writer.writerow(["seed", 42])
        writer.writerow(["Description", "Sweep active_curvature from 0 to 15 under gravity and fixed anisotropy=3.0"])

    for active_curv in active_curvatures:
        print(f"Running active_curvature={active_curv:.2f}...")

        # Run simulation using PyElastica Bridge function
        res = run_protein_simulation(
            anisotropy=fixed_anisotropy,
            active_curvature=active_curv,
            torsion_drive=0.0,
            stiffness_modulation=0.0,
            initial_lateral_defect=0.0,
            natural_kyphosis=2.0,  # Baseline
            n_elements=n_elements,
            duration=duration,
            dt=dt,
            gravity=gravity,
            show_progress=False
        )

        if not res.get("success", False):
            print(f"Simulation failed for active_curvature={active_curv:.2f}: {res.get('error')}")
            continue

        results_summary.append({
            "active_curvature": active_curv,
            "cobb_angle": res.get("cobb_angle", 0.0),
            "max_curvature": res.get("max_curvature", 0.0),
            "end_to_end_distance": res.get("end_to_end_distance", 0.0),
            "z_tip": res.get("z_tip", 0.0),
            "U_CC": res.get("U_CC", 0.0)
        })

    if not results_summary:
        print("All simulations failed.")
        sys.exit(1)

    # Save CSV
    csv_path = out_dir / "results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "active_curvature", "cobb_angle", "max_curvature",
            "end_to_end_distance", "z_tip", "U_CC"
        ])
        writer.writeheader()
        writer.writerows(results_summary)

    # Plot
    plt.figure(figsize=(15, 5))

    # Plot 1: Cobb Angle vs Growth
    plt.subplot(1, 3, 1)
    plt.plot([r["active_curvature"] for r in results_summary], [r["cobb_angle"] for r in results_summary], 'm-d')
    plt.xlabel("Active Curvature")
    plt.ylabel("Cobb Angle (deg)")
    plt.title("Scoliosis Measure")
    plt.grid(True)

    # Plot 2: Z Tip (Sagittal range proxy) vs Growth
    plt.subplot(1, 3, 2)
    plt.plot([r["active_curvature"] for r in results_summary], [r["z_tip"] for r in results_summary], 'b-o')
    plt.xlabel("Active Curvature")
    plt.ylabel("Z Tip Height (m)")
    plt.title("Vertical Deflection")
    plt.grid(True)

    # Plot 3: End-to-end Distance vs Growth
    plt.subplot(1, 3, 3)
    plt.plot([r["active_curvature"] for r in results_summary], [r["end_to_end_distance"] for r in results_summary], 'r-^')
    plt.xlabel("Active Curvature")
    plt.ylabel("End-to-End Distance (m)")
    plt.title("Compression / Buckling")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(out_dir / "plot_s_shape.png")

    print(f"Done. Output: {out_dir}")

if __name__ == "__main__":
    main()
