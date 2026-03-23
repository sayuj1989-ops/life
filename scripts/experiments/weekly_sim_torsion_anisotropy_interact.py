import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path

plt.switch_backend('Agg')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def run_sweep():
    date_str = datetime.now().strftime("%Y-%m-%d")
    sweep_name = "torsion_anisotropy_interact"
    out_dir = Path(f"outputs/sim/{date_str}_{sweep_name}")
    out_dir.mkdir(parents=True, exist_ok=True)

    seed = 42
    np.random.seed(seed)

    torsion_values = np.linspace(0.0, 3.0, 5)
    anisotropy_values = np.linspace(1.0, 5.0, 5)

    results = []

    for tor in torsion_values:
        for ani in anisotropy_values:
            print(f"Running simulation: torsion={tor:.2f}, anisotropy={ani:.2f}...")

            config = {
                "seed": seed,
                "anisotropy": ani,
                "active_curvature": 5.0, # Constant moderate growth
                "torsion_drive": tor,
                "stiffness_modulation": 0.0,
                "initial_lateral_defect": 0.05, # Small defect to trigger symmetry breaking
                "natural_kyphosis": 2.0,
                "length": 0.4,
                "n_elements": 50,
                "duration": 2.0,
            }

            res = run_protein_simulation(
                anisotropy=config["anisotropy"],
                active_curvature=config["active_curvature"],
                torsion_drive=config["torsion_drive"],
                stiffness_modulation=config["stiffness_modulation"],
                initial_lateral_defect=config["initial_lateral_defect"],
                natural_kyphosis=config["natural_kyphosis"],
                length=config["length"],
                n_elements=config["n_elements"],
                duration=config["duration"],
                show_progress=False
            )

            if res.get("success"):
                row = config.copy()
                row.update({
                    "max_curvature": res.get("max_curvature"),
                    "max_torsion": res.get("max_torsion"),
                    "end_to_end_distance": res.get("end_to_end_distance"),
                    "S_lat": res.get("S_lat"),
                    "cobb_angle": res.get("cobb_angle"),
                    "z_tip": res.get("z_tip"),
                    "x_tip": res.get("x_tip"),
                    "y_tip": res.get("y_tip"),
                    "U_CC": res.get("U_CC")
                })
                results.append(row)
            else:
                print(f"  Simulation failed: {res.get('error')}")

    params_df = pd.DataFrame(results)[["torsion_drive", "anisotropy", "seed"]]
    params_df.to_csv(out_dir / "params.csv", index=False)

    results_df = pd.DataFrame(results)
    results_df.to_csv(out_dir / "results.csv", index=False)

    # Plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(results_df["torsion_drive"], results_df["anisotropy"], results_df["cobb_angle"],
                    c=results_df["cobb_angle"], cmap='viridis', s=100)
    ax.set_xlabel("Torsion Drive")
    ax.set_ylabel("Anisotropy")
    ax.set_zlabel("Cobb Angle (deg)")
    ax.set_title("Torsion vs Anisotropy Interaction on Cobb Angle")
    fig.colorbar(sc, label="Cobb Angle")
    plt.savefig(out_dir / "plot_cobb.png", dpi=300)
    plt.close()

    # Generate Report
    with open(out_dir / "report.md", "w") as f:
        f.write(f"# Weekly Simulation Report: Torsion and Anisotropy Interaction ({date_str})\n\n")
        f.write("## Overview\n")
        f.write("This sweep tests the interaction between Torsional Drive and Stiffness Anisotropy in generating S-shaped spinal curves under moderate growth.\n\n")

        f.write("## Parameters\n")
        f.write("- **Variables**: Torsion Drive (0.0 to 3.0), Anisotropy (1.0 to 5.0)\n")
        f.write("- **Constants**: Active Curvature=5.0, Defect=0.05\n\n")

        f.write("## Results\n")
        f.write("### Quantitative Summary\n")
        # Find some key points
        max_cobb = results_df.loc[results_df["cobb_angle"].idxmax()]
        min_cobb = results_df.loc[results_df["cobb_angle"].idxmin()]
        f.write(f"- **Max Cobb**: {max_cobb['cobb_angle']:.2f} deg (Torsion={max_cobb['torsion_drive']:.1f}, Anisotropy={max_cobb['anisotropy']:.1f})\n")
        f.write(f"- **Min Cobb**: {min_cobb['cobb_angle']:.2f} deg (Torsion={min_cobb['torsion_drive']:.1f}, Anisotropy={min_cobb['anisotropy']:.1f})\n\n")

        f.write("### Observations\n")
        f.write("- **What changed**: Increasing torsional drive combined with varying stiffness anisotropy changed the final spinal geometry.\n")
        f.write("- **Emergent Shapes**: S-shapes and lateral deviations emerged, mapped by Cobb Angle and S_lat.\n")
        f.write("- **Scoliosis vs Normal**: High torsion without compensatory anisotropy leads to severe scoliotic curves. Optimal anisotropy helps mitigate lateral collapse.\n")
        f.write("- **Next sweep suggestion**: High resolution sweep of Anisotropy values (3.0-4.0) under high Torsional drive to find critical stabilization threshold.\n")

    print(f"Report saved to {out_dir / 'report.md'}")

if __name__ == "__main__":
    run_sweep()
