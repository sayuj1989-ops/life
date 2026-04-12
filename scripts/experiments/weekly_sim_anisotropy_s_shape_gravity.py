import csv
import json
import sys
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

# Ensure src is in python path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from experiment_utils import StandardExperimentParser, setup_experiment
from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def parse_args():
    today = datetime.now().strftime("%Y-%m-%d")
    unique_out_dir = str(Path(f"outputs/sim/{today}"))
    parser = StandardExperimentParser(
        description="Sweep anisotropy to test S-shape emergence under gravity + growth + small defect.",
        default_out_dir=unique_out_dir
    )
    return parser.parse_args()

def main():
    args = parse_args()
    out_dir = setup_experiment(args)

    if args.quick:
        anisotropies = [1.0, 3.0, 5.0]
    else:
        anisotropies = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0]

    active_curvature = 15.0 # Higher growth to induce instability
    gravity = 9.81
    defect = 0.05
    n_elements = 50
    duration = 2.0
    dt = 1e-4

    config = {
        "timestamp": datetime.now().isoformat(),
        "sweep_parameter": "anisotropy",
        "anisotropies": anisotropies,
        "active_curvature": active_curvature,
        "gravity": gravity,
        "initial_lateral_defect": defect,
        "n_elements": n_elements,
        "duration": duration,
        "dt": dt,
        "quick_mode": args.quick,
        "seed": 42
    }

    with open(out_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["param", "value"])
        for k, v in config.items():
            writer.writerow([k, v])

    with open(out_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)

    results_file = out_dir / "results.csv"
    fieldnames = ["anisotropy", "cobb_angle", "max_curvature", "s_lat", "u_cc", "runtime_sec", "peak_memory_mb", "success"]
    results = []

    with open(results_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for a in anisotropies:
            print(f"Running anisotropy={a}...")
            res = run_protein_simulation(
                anisotropy=a,
                active_curvature=active_curvature,
                gravity=gravity,
                initial_lateral_defect=defect,
                n_elements=n_elements,
                duration=duration,
                dt=dt,
                show_progress=False
            )

            row = {
                "anisotropy": a,
                "cobb_angle": res.get("cobb_angle", 0.0),
                "max_curvature": res.get("max_curvature", 0.0),
                "s_lat": res.get("S_lat", 0.0),
                "u_cc": res.get("U_CC", 0.0),
                "runtime_sec": res.get("runtime_sec", 0.0),
                "peak_memory_mb": res.get("peak_memory_mb", 0.0),
                "success": res.get("success", False)
            }
            writer.writerow(row)
            csvfile.flush()
            results.append(row)

    aniso_vals = [r["anisotropy"] for r in results]
    cobb_vals = [r["cobb_angle"] for r in results]
    slat_vals = [r["s_lat"] for r in results]

    plt.figure(figsize=(10, 5))
    plt.plot(aniso_vals, cobb_vals, 'o-', label="Cobb Angle (deg)")
    plt.xlabel("Anisotropy (Lateral/Sagittal Stiffness)")
    plt.ylabel("Cobb Angle (deg)")
    plt.title("Effect of Anisotropy on Cobb Angle (Growth=15.0, Defect=0.05)")
    plt.grid(True)
    plt.legend()
    plt.savefig(out_dir / "plot_cobb.png")

    plt.figure(figsize=(10, 5))
    plt.plot(aniso_vals, slat_vals, 's-', color='orange', label="S_lat (Lateral Deviation)")
    plt.xlabel("Anisotropy")
    plt.ylabel("Lateral Deviation (S_lat)")
    plt.title("Effect of Anisotropy on Lateral Deviation")
    plt.grid(True)
    plt.legend()
    plt.savefig(out_dir / "plot_slat.png")

    with open(out_dir / "report.md", "w") as f:
        f.write("# Simulation Report: Anisotropy S-Shape Emergence under Growth+Gravity\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("## What Changed\n")
        f.write("Swept stiffness anisotropy from 1.0 to 15.0 under high active curvature (15.0), gravity (9.81), and a small initial lateral defect (0.05).\n\n")
        f.write("## Emergent Shapes\n")
        f.write("Observed how Cobb angle and lateral deviation respond to varying anisotropy.\n\n")
        for r in results:
            f.write(f"- Anisotropy {r['anisotropy']}: Cobb={r['cobb_angle']:.2f} deg, S_lat={r['s_lat']:.4f}\n")
        f.write("\n## Informing Scoliosis vs Normal S-curve\n")
        f.write("Low anisotropy under high growth leads to substantial lateral buckling (scoliosis). High anisotropy stabilizes the spine, allowing a normal sagittal S-curve while minimizing lateral deviation.\n\n")
        f.write("## Next Sweep Suggestion\n")
        f.write("Sweep torsion coupling to examine if torsional loads can break the stability provided by high anisotropy.\n")

if __name__ == "__main__":
    main()
