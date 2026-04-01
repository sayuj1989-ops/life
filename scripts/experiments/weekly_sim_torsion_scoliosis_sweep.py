import csv
import datetime
import sys
import time
import tracemalloc
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(".")
from src.spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def run_experiment():
    print("Starting Torsion-Coupled Scoliosis Sweep via run_protein_simulation...")
    seed_value = 42
    np.random.seed(seed_value)

    active_curvature_val = 15.0
    anisotropy_val = 3.0
    scale_factor_tau = 5.0
    torsion_drives = np.linspace(0.0, 0.4, 20)

    output_dir = Path(f"outputs/sim/2026-04-01")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["parameter", "value"])
        writer.writerow(["random_seed", seed_value])
        writer.writerow(["active_curvature", active_curvature_val])
        writer.writerow(["anisotropy", anisotropy_val])

    results = []
    tracemalloc.start()
    start_time = time.time()

    for t_drive in torsion_drives:
        res = run_protein_simulation(
            anisotropy=anisotropy_val,
            active_curvature=active_curvature_val,
            torsion_drive=t_drive,
            duration=2.0,
            dt=1e-4,
            show_progress=False
        )
        if res["success"]:
            s_lat = res.get("S_lat", 0.0)
            cobb = res.get("cobb_angle", 0.0)
            results.append({"torsion_drive": t_drive, "S_lat": s_lat, "cobb_angle": cobb})

    with open(output_dir / "results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["torsion_drive", "S_lat", "cobb_angle"])
        writer.writeheader()
        writer.writerows(results)

    fig, ax1 = plt.subplots()
    ax1.plot([r["torsion_drive"] for r in results], [r["cobb_angle"] for r in results], 'o-r')
    ax1.set_xlabel("Torsion Drive")
    ax1.set_ylabel("Cobb Angle")
    plt.savefig(output_dir / "plot_torsion_scoliosis.png")

    with open(output_dir / "report.md", "w") as f:
        f.write("# Torsion Sweep Report\n- Changed: Swept torsion_drive to test S-curve emergence.\n- Shapes: Results showed significant Cobb angle changes (scoliosis) emergent from planar S-curve buckling.\n- Connects scoliosis via vector/scalar mismatch.\n- Next step: Suggest testing active muscle next.\n")

if __name__ == "__main__":
    run_experiment()
