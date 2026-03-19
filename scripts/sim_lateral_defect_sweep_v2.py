import csv
import random
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Ensure project root is in path
sys.path.append(".")

from src.spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def run_experiment():
    print("Starting Lateral Defect Sweep...")

    # Set and save a random seed for reproducibility
    seed_value = 42
    np.random.seed(seed_value)
    random.seed(seed_value)

    # Base parameters
    L = 1.0
    n_elements = 50
    duration = 3.0
    dt = 1e-4

    # Keep other parameters fixed
    anisotropy_val = 3.0
    active_curvature = 12.0  # High growth drive to sensitize to defects
    natural_kyphosis = 2.0
    torsion_drive = 0.0
    scale_factor_kappa = 5.0

    # Sweep initial lateral defect
    # 20 points from 0 to 0.15
    defect_vals = np.linspace(0.0, 0.15, 20)

    # Output directory
    date_str = datetime.now().strftime("%Y-%m-%d")
    # Add _v2 to distinguish from previous if it exists
    output_dir = Path(f"outputs/sim/{date_str}_defect_sweep_v2")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save params
    with open(output_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["parameter", "value"])
        writer.writerow(["random_seed", seed_value])
        writer.writerow(["L", L])
        writer.writerow(["n_elements", n_elements])
        writer.writerow(["duration", duration])
        writer.writerow(["anisotropy", anisotropy_val])
        writer.writerow(["active_curvature", active_curvature])
        writer.writerow(["natural_kyphosis", natural_kyphosis])
        writer.writerow(["torsion_drive", torsion_drive])
        writer.writerow(["scale_factor_kappa", scale_factor_kappa])

    results = []

    tracemalloc.start()
    start_time_total = time.time()

    for defect in defect_vals:
        print(f"\n--- Running Lateral Defect: {defect:.4f} ---")

        res = run_protein_simulation(
            anisotropy=anisotropy_val,
            active_curvature=active_curvature,
            torsion_drive=torsion_drive,
            initial_lateral_defect=defect,
            natural_kyphosis=natural_kyphosis,
            length=L,
            n_elements=n_elements,
            duration=duration,
            dt=dt,
            scale_factor_kappa=scale_factor_kappa,
            show_progress=False
        )

        if res["success"]:
            s_lat = res.get("S_lat", 0.0)
            cobb = res.get("cobb_angle", 0.0)
            print(f"Success. S_lat: {s_lat:.4f}, Cobb: {cobb:.2f} deg")

            results.append({
                "initial_lateral_defect": defect,
                "S_lat": s_lat,
                "cobb_angle": cobb,
                "max_curvature": res.get("max_curvature", 0.0),
                "z_tip": res.get("z_tip", 0.0)
            })
        else:
            print(f"Failed: {res['error']}")

    end_time_total = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTotal Runtime: {end_time_total - start_time_total:.2f}s")

    # Save Results
    csv_path = output_dir / "results.csv"
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["initial_lateral_defect", "S_lat", "cobb_angle", "max_curvature", "z_tip"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {csv_path}")

    # Plot Comparison
    fig, ax1 = plt.subplots(figsize=(8, 6))

    defs = [r["initial_lateral_defect"] for r in results]
    cobb_angles = [r["cobb_angle"] for r in results]

    color = 'tab:red'
    ax1.set_xlabel("Initial Lateral Defect (1/m)")
    ax1.set_ylabel("Cobb Angle (degrees)", color=color)
    ax1.plot(defs, cobb_angles, 'o-', color=color, label="Cobb Angle")
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    s_lats = [r["S_lat"] for r in results]
    ax2.set_ylabel("Lateral Scoliosis Index ($S_{lat}$)", color=color)
    ax2.plot(defs, s_lats, 's--', color=color, label="S_lat")
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f"Sensitivity to Initial Lateral Defect (Growth={active_curvature}, Anisotropy={anisotropy_val})")
    fig.tight_layout()
    plt.savefig(output_dir / "plot_defect_sweep.png")
    print(f"Plot saved to {output_dir / 'plot_defect_sweep.png'}")

if __name__ == "__main__":
    run_experiment()
