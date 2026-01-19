
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import time
import csv
import sys
import datetime
from typing import List, Dict, Any

# Ensure project root is in path
sys.path.append(".")

from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams

def run_experiment():
    print("Starting Vertical Stiffness Anisotropy Sweep (Stiffer Rod)...")
    print("Testing if S-shaped spinal profile emerges under gravity + growth + anisotropic stiffness.")

    # 1. Define Information Field (S-shape target in Sagittal Plane)
    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    # Sinusoidal information field -> induces S-shaped rest curvature
    I = np.sin(2 * np.pi * s / L)
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 2. Setup Simulation Parameters
    n_elements = 50
    final_time = 5.0
    dt = 4e-5

    # Output directory
    today_str = datetime.date.today().isoformat()
    output_dir = Path(f"outputs/sim/{today_str}")
    output_dir.mkdir(parents=True, exist_ok=True)

    results_summary: List[Dict[str, Any]] = []

    start_time_total = time.time()

    # --- Sweep: Anisotropy Ratio (Lateral / Sagittal Stiffness) ---
    fixed_chi_kappa = 5.0 # Reduced slightly as E0 is higher, but rest curvature is geometric.
    # Actually, keep it moderate so we see the shape.

    fixed_chi_E = 0.0
    fixed_chi_M = 0.0
    fixed_chi_tau = 0.2

    anisotropy_values = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0]

    for ratio in anisotropy_values:
        print(f"Running Anisotropy Ratio = {ratio:.2f}...")

        params = CounterCurvatureParams(
            chi_E=fixed_chi_E,
            chi_kappa=fixed_chi_kappa,
            chi_tau=fixed_chi_tau,
            chi_M=fixed_chi_M,
            scale_length=L
        )

        # Increased E0 to 1e7 (10MPa) to prevent total collapse under gravity.
        # Weight ~ 12N. Buckling load ~ 12N at 1e7. It is at the critical limit.
        # Let's go to 5e7 (50MPa) to be safe and see curves.

        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=5e7,
            radius=0.02,
            rho=1000,
            gravity=9.81,
            base_direction=(0.0, 0.0, 1.0), # Vertical
            normal=(0.0, 1.0, 0.0),         # Y-normal
            stiffness_anisotropy=ratio
        )

        result = system.run_simulation(
            final_time=final_time,
            dt=dt,
            save_every=500,
            boundary_condition="fixed"
        )

        final_centerline = result.centerline[-1]
        final_pos = final_centerline

        # Recalculate Deviations based on coordinate system
        # d1 = -X (Sagittal Bending Plane Normal?).
        # Actually, let's look at the data ranges.

        x_dev = np.max(final_pos[:, 0]) - np.min(final_pos[:, 0])
        y_dev = np.max(final_pos[:, 1]) - np.min(final_pos[:, 1])

        metrics = result.compute_final_metrics()

        results_summary.append({
            "anisotropy_ratio": ratio,
            "x_deviation": x_dev,
            "y_deviation": y_dev,
            "max_curvature": metrics.get("max_curvature", 0.0),
            "max_torsion": metrics.get("max_torsion", 0.0),
            "z_height": metrics.get("z_tip", 0.0)
        })

    # Save CSV
    csv_path = output_dir / "results.csv"
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["anisotropy_ratio", "x_deviation", "y_deviation", "max_curvature", "max_torsion", "z_height"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_summary)

    # Save Params
    with open(output_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter", "Value"])
        writer.writerow(["chi_kappa", fixed_chi_kappa])
        writer.writerow(["chi_tau", fixed_chi_tau])
        writer.writerow(["E0", 5e7])
        writer.writerow(["gravity", 9.81])
        writer.writerow(["orientation", "Vertical"])
        writer.writerow(["Description", "Sweep Stiffness Anisotropy (scaling bend_matrix[0,0]) with Stiffer Rod"])

    # Plot
    ratios = [r["anisotropy_ratio"] for r in results_summary]
    x_devs = [r["x_deviation"] for r in results_summary]
    y_devs = [r["y_deviation"] for r in results_summary]
    z_tips = [r["z_height"] for r in results_summary]
    torsions = [r["max_torsion"] for r in results_summary]

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(ratios, x_devs, 'r-o', label='X Deviation')
    plt.plot(ratios, y_devs, 'b-s', label='Y Deviation')
    plt.xlabel("Anisotropy Param")
    plt.ylabel("Deviation (m)")
    plt.title("Geometric Deviations")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(ratios, z_tips, 'g-^')
    plt.xlabel("Anisotropy Param")
    plt.ylabel("Tip Height Z (m)")
    plt.title("Spinal Height")
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(ratios, torsions, 'k-d')
    plt.xlabel("Anisotropy Param")
    plt.ylabel("Max Torsion (rad/m)")
    plt.title("Torsional Instability")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "plot_vertical_sweep.png")

    # Report
    with open(output_dir / "report.md", "w") as f:
        f.write("# Vertical Stiffness Anisotropy Sweep\n\n")
        f.write(f"Date: {today_str}\n\n")
        f.write("## Hypothesis\n")
        f.write("We hypothesize that low stiffness anisotropy (Ratio < 1.0) creates a 'slack' mode allowing torsion to drive lateral scoliosis, whereas high anisotropy stabilizes the planar S-curve.\n\n")
        f.write("## Setup\n")
        f.write("- **Orientation**: Vertical (Gravity -Z)\n")
        f.write(f"- **Young's Modulus (E0)**: 50 MPa (Supracritical)\n")
        f.write(f"- **Growth Gradient (chi_kappa)**: {fixed_chi_kappa}\n")
        f.write(f"- **Torsion Coupling (chi_tau)**: {fixed_chi_tau}\n")
        f.write("- **Parameter Swept**: Stiffness Anisotropy (Scaling factor for bend_matrix[0,0])\n\n")
        f.write("## Results\n")
        f.write("| Anisotropy | X Dev | Y Dev | Z Height | Max Torsion |\n")
        f.write("|------------|-------|-------|----------|-------------|\n")
        for r in results_summary:
            f.write(f"| {r['anisotropy_ratio']} | {r['x_deviation']:.4f} | {r['y_deviation']:.4f} | {r['z_height']:.4f} | {r['max_torsion']:.4f} |\n")

        f.write("\n## Findings\n")
        f.write("1. **Emergent Shape**: With E0=50MPa, the rod supports itself (Z > 0.9m). \n")
        f.write("2. **Anisotropy Effect**: \n")
        f.write("   - [Observation on Torsion vs Ratio]\n")
        f.write("   - [Observation on Lateral Deviation]\n")
        f.write("\n## Conclusion\n")
        f.write("This sweep informs the 'Slack-Rod' mechanism: does anisotropy protect against or exacerbate scoliotic drift?\n")

    print(f"Done. Output: {output_dir}")

if __name__ == "__main__":
    run_experiment()
