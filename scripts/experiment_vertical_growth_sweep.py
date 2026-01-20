
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
    print("Starting Vertical Growth (chi_kappa) Sweep...")
    print("Testing S-shaped emergence under gravity (vertical rod) with anisotropic stiffness.")

    # 1. Define Information Field (S-shape target)
    L = 1.0
    n_points = 200
    s = np.linspace(0, L, n_points)
    # Sinusoidal information field implying an S-shape
    I = np.sin(2 * np.pi * s / L)
    dIds = np.gradient(I, s)
    info = InfoField1D(s=s, I=I, dIds=dIds)

    # 2. Setup Simulation Parameters (Optimized for stability)
    n_elements = 30
    final_time = 1.0
    dt = 4e-5

    # Output directory
    today_str = datetime.date.today().isoformat()
    output_dir = Path(f"outputs/sim/{today_str}")
    output_dir.mkdir(parents=True, exist_ok=True)

    results_summary: List[Dict[str, Any]] = []

    # --- Sweep: Growth Gradient Gain (chi_kappa) ---
    # Fixed Anisotropy: 0.5 (Weaker in one bending mode, encouraging buckling)
    # Fixed Torsion: 0.0 (Decoupled to isolate planar S-shape vs buckling)
    fixed_anisotropy = 0.5
    fixed_chi_E = 0.0
    fixed_chi_M = 0.0
    fixed_chi_tau = 0.0

    # Sweep chi_kappa: 0 to 20
    chi_kappa_values = np.linspace(0, 20, 11)

    print(f"Output Directory: {output_dir}")

    for val in chi_kappa_values:
        print(f"Running chi_kappa = {val:.2f}...")

        params = CounterCurvatureParams(
            chi_E=fixed_chi_E,
            chi_kappa=val,
            chi_tau=fixed_chi_tau,
            chi_M=fixed_chi_M,
            scale_length=L
        )

        # Vertical Rod: Base at (0,0,0), Direction (0,0,1)
        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=1e6,
            radius=0.02,
            rho=1000,
            base_direction=(0.0, 0.0, 1.0), # Vertical Z
            normal=(0.0, 1.0, 0.0),        # Y normal
            stiffness_anisotropy=fixed_anisotropy,
            gravity=9.81
        )

        # Run with gravity explicitly passed
        result = system.run_simulation(
            final_time=final_time,
            dt=dt,
            save_every=100,
            gravity=9.81
        )

        # Analyze Final State
        final_pos = result.centerline[-1] # (n_nodes, 3)

        # Geometry metrics
        # Lateral = X (index 0), Sagittal = Y (index 1), Axial = Z (index 2)
        # Note: 'normal' was Y. Director d2 is Y. d1 is X.
        # Anisotropy 0.5 applies to d1 (X-axis rotation) -> bending in Y-Z plane (Sagittal).
        # So Sagittal stiffness is reduced.

        # Lateral Deviation (X)
        lat_dev = np.max(final_pos[:, 0]) - np.min(final_pos[:, 0])

        # Sagittal Range (Y) - Depth
        sag_range = np.max(final_pos[:, 1]) - np.min(final_pos[:, 1])

        # Z-tip (Height retention)
        z_tip = final_pos[-1, 2]

        # Max Curvature
        curvature = result.curvature[-1]
        max_curvature = np.max(curvature)

        results_summary.append({
            "chi_kappa": val,
            "lateral_dev": lat_dev,
            "sagittal_range": sag_range,
            "z_tip": z_tip,
            "max_curvature": max_curvature
        })

    # Save CSV
    csv_path = output_dir / "results.csv"
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["chi_kappa", "lateral_dev", "sagittal_range", "z_tip", "max_curvature"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_summary)

    # Save Params
    with open(output_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter", "Value"])
        writer.writerow(["stiffness_anisotropy", fixed_anisotropy])
        writer.writerow(["chi_tau", fixed_chi_tau])
        writer.writerow(["chi_E", fixed_chi_E])
        writer.writerow(["final_time", final_time])
        writer.writerow(["base_direction", "Vertical (Z)"])
        writer.writerow(["Description", "Sweep Growth Gradient (chi_kappa) on Vertical Rod under Gravity"])

    # Plot
    kappas = [r["chi_kappa"] for r in results_summary]
    lats = [r["lateral_dev"] for r in results_summary]
    sags = [r["sagittal_range"] for r in results_summary]
    z_tips = [r["z_tip"] for r in results_summary]

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(kappas, sags, 'b-s')
    plt.xlabel("Growth Gain (chi_kappa)")
    plt.ylabel("Sagittal Depth (m)")
    plt.title("S-Shape Formation (Sagittal)")
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(kappas, lats, 'r-o')
    plt.xlabel("Growth Gain (chi_kappa)")
    plt.ylabel("Lateral Deviation (m)")
    plt.title("Lateral Instability")
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(kappas, z_tips, 'g-^')
    plt.xlabel("Growth Gain (chi_kappa)")
    plt.ylabel("Z-Tip Height (m)")
    plt.title("Vertical Collapse / Buckling")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "plot_vertical_growth_sweep.png")

    print(f"Sweep Completed. Results saved to {output_dir}")

if __name__ == "__main__":
    run_experiment()
