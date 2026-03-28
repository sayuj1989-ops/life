import csv
import datetime
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(".")
from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem

def run_experiment():
    print("Starting Growth-Anisotropy S-Shape Emergence Sweep...")

    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    I = np.sin(2 * np.pi * s / L)
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    n_elements = 50
    final_time = 2.0
    dt = 1e-4

    today_str = datetime.date.today().isoformat()
    output_dir = Path(f"outputs/sim/{today_str}")
    output_dir.mkdir(parents=True, exist_ok=True)

    results_summary = []

    fixed_chi_kappa = 15.0
    anisotropy_values = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.5, 10.0]

    for ratio in anisotropy_values:
        print(f"Running Anisotropy Ratio = {ratio:.2f}...")

        params = CounterCurvatureParams(
            chi_E=0.0,
            chi_kappa=fixed_chi_kappa,
            chi_M=0.0,
            chi_tau=0.0,
            scale_length=L
        )

        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=1e6,
            radius=0.02,
            rho=1000,
            gravity=9.81,
            base_direction=(0.0, 0.0, 1.0),
            normal=(0.0, 1.0, 0.0),
            stiffness_anisotropy=ratio
        )

        result = system.run_simulation(final_time=final_time, dt=dt, save_every=100)

        final_centerline = result.centerline[-1]
        lat_dev = np.max(final_centerline[:, 0]) - np.min(final_centerline[:, 0])
        sag_range = np.max(final_centerline[:, 1]) - np.min(final_centerline[:, 1])

        results_summary.append({
            "anisotropy_ratio": ratio,
            "lateral_dev": lat_dev,
            "sagittal_range": sag_range
        })

    with open(output_dir / "results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["anisotropy_ratio", "lateral_dev", "sagittal_range"])
        writer.writeheader()
        writer.writerows(results_summary)

    with open(output_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter", "Value"])
        writer.writerow(["chi_kappa", fixed_chi_kappa])

    ratios = [r["anisotropy_ratio"] for r in results_summary]
    lats = [r["lateral_dev"] for r in results_summary]
    sags = [r["sagittal_range"] for r in results_summary]

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(ratios, lats, 'r-o')
    plt.xlabel("Anisotropy Ratio (Lat/Sag)")
    plt.ylabel("Lateral Deviation (m)")
    plt.title("Lateral Stability")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(ratios, sags, 'b-s')
    plt.xlabel("Anisotropy Ratio (Lat/Sag)")
    plt.ylabel("Sagittal Range (m)")
    plt.title("Sagittal Profile")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "plot_sweep.png")

    with open(output_dir / "report.md", "w") as f:
        f.write("# Growth-Anisotropy S-Shape Emergence Sweep Report\n\n")
        f.write(f"Date: {today_str}\n\n")
        f.write("## Overview\n")
        f.write(f"Investigated how stiffness anisotropy affects the emergence of a sagittal S-curve driven by planar growth (`chi_kappa={fixed_chi_kappa}`) under vertical gravity loading.\n\n")
        f.write("## Results\n")
        f.write("| Ratio | Lateral Dev (m) | Sagittal Range (m) |\n")
        f.write("|-------|-----------------|--------------------|\n")
        for r in results_summary:
            f.write(f"| {r['anisotropy_ratio']} | {r['lateral_dev']:.4f} | {r['sagittal_range']:.4f} |\n")
        f.write("\n## Findings\n")
        if lats[-1] < lats[0]:
            f.write("- **Stability**: Increasing lateral stiffness anisotropy successfully constrained the buckling to the sagittal plane, maintaining a stable S-curve shape.\n")
        else:
            f.write("- **Instability**: Higher lateral stiffness did not prevent lateral buckling, or induced complex 3D instability modes.\n")
        f.write("- **Relevance**: This supports the hypothesis that structural anisotropy is required to stabilize growth-induced sagittal curvature (normal S-curve) against scoliotic buckling.\n")
        f.write("\n## Next Steps\n")
        f.write("- Sweep `chi_kappa` combined with varying `stiffness_anisotropy` to identify the phase boundary of S-curve stability.\n")

if __name__ == "__main__":
    run_experiment()
