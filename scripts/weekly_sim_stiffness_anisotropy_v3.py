import csv
import random
import sys
import time
import tracemalloc
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

# Ensure project root is in path
sys.path.append(".")

from src.spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def run_experiment():
    print("Starting Stiffness Anisotropy Sweep Experiment...")

    seed_value = 42
    np.random.seed(seed_value)
    random.seed(seed_value)

    active_curvature_val = 15.0
    torsion_drive_val = 0.1
    duration = 2.0
    dt = 1e-4

    anisotropies = np.linspace(1.0, 10.0, 19)

    today_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"outputs/sim/{today_str}_anisotropy_v3")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["parameter", "value"])
        writer.writerow(["random_seed", seed_value])
        writer.writerow(["active_curvature", active_curvature_val])
        writer.writerow(["torsion_drive", torsion_drive_val])
        writer.writerow(["duration", duration])

    results = []

    start_time_total = time.time()

    for aniso in anisotropies:
        print(f"Running Anisotropy: {aniso:.2f}")
        res = run_protein_simulation(
            anisotropy=aniso,
            active_curvature=active_curvature_val,
            torsion_drive=torsion_drive_val,
            duration=duration,
            dt=dt,
            show_progress=False
        )

        if res["success"]:
            s_lat = res.get("S_lat", 0.0)
            cobb = res.get("cobb_angle", 0.0)
            results.append({
                "anisotropy": aniso,
                "S_lat": s_lat,
                "cobb_angle": cobb,
                "max_curvature": res.get("max_curvature", 0.0),
                "z_tip": res.get("z_tip", 0.0)
            })
            print(f"  Success. S_lat: {s_lat:.4f}, Cobb: {cobb:.2f}")
        else:
            print(f"  Failed: {res['error']}")

    csv_path = output_dir / "results.csv"
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["anisotropy", "S_lat", "cobb_angle", "max_curvature", "z_tip"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    fig, ax1 = plt.subplots(figsize=(8, 6))
    x_vals = [r["anisotropy"] for r in results]
    cobb_angles = [r["cobb_angle"] for r in results]

    color = 'tab:red'
    ax1.set_xlabel("Stiffness Anisotropy Ratio")
    ax1.set_ylabel("Cobb Angle (degrees)", color=color)
    ax1.plot(x_vals, cobb_angles, 'o-', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    s_lats = [r["S_lat"] for r in results]
    ax2.set_ylabel("Lateral Scoliosis Index (S_lat)", color=color)
    ax2.plot(x_vals, s_lats, 's--', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("Spinal Stability vs Stiffness Anisotropy")
    fig.tight_layout()
    plt.savefig(output_dir / "plot_anisotropy_sweep.png")

if __name__ == "__main__":
    run_experiment()
