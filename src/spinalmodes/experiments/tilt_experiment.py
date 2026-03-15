import csv
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(".")

from src.spinalmodes.countercurvature.coupling import CounterCurvatureParams
from src.spinalmodes.countercurvature.info_fields import InfoField1D
from src.spinalmodes.countercurvature.pyelastica_bridge import CounterCurvatureRodSystem
from src.spinalmodes.countercurvature.scoliosis_metrics import compute_lateral_scoliosis_index


def generate_sine_field(s: np.ndarray, L: float) -> InfoField1D:
    I = np.sin(2 * np.pi * s / L)
    dIds = np.gradient(I, s)
    return InfoField1D(s=s, I=I, dIds=dIds)

def run_experiment():
    print("Starting Load Vector Tilt Sweep Experiment...")

    L = 1.0
    n_points = 200
    date_str = time.strftime("%Y-%m-%d")

    output_dir = Path(f"outputs/sim/{date_str}_tilt_sweep")
    output_dir.mkdir(parents=True, exist_ok=True)

    s = np.linspace(0, L, n_points)
    info = generate_sine_field(s, L)

    # Simulation params
    n_elements = 50
    final_time = 3.0
    dt = 5e-5

    tilt_values_deg = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0]

    # Base params for countercurvature that normally creates an S-shape
    # chi_kappa drives preferred curvature, chi_M drives active moment
    chi_kappa = 10.0

    results = []

    tracemalloc.start()
    start_time_total = time.time()

    for tilt_deg in tilt_values_deg:
        tilt_rad = np.radians(tilt_deg)

        print(f"Running Tilt: {tilt_deg} degrees")

        params = CounterCurvatureParams(
            chi_E=0.0,
            chi_kappa=chi_kappa,
            chi_M=0.0,
            chi_tau=0.0,
            scale_length=L
        )

        # PyElastica setup
        # Vertical rod initialization
        # Let's initialize the rod pointing up the Z axis: base_direction=(0,0,1)
        # Normal pointing along X: normal=(1,0,0)
        # Then, gravity acts in a tilted direction.
        # By default run_simulation applies gravity along the direction (0,0,-1)
        # We can simulate tilt by keeping gravity vertical and tilting the base_direction of the rod!
        # A rod tilted by `tilt_deg` from the vertical Z-axis towards the X-axis:
        # Direction: (sin(tilt), 0, cos(tilt))
        # Normal: (cos(tilt), 0, -sin(tilt))  (perpendicular to direction)

        base_dir = (np.sin(tilt_rad), 0.0, np.cos(tilt_rad))
        normal_dir = (np.cos(tilt_rad), 0.0, -np.sin(tilt_rad))

        system = CounterCurvatureRodSystem.from_iec(
            info=info,
            params=params,
            length=L,
            n_elements=n_elements,
            E0=1e6,
            radius=0.02,
            rho=1000,
            gravity=9.81,
            base_direction=base_dir,
            normal=normal_dir
        )

        result = system.run_simulation(final_time=final_time, dt=dt, save_every=200)

        # Analysis
        final_centerline = result.centerline[-1] # Shape (n_nodes, 3)
        # We want to measure the deviation from the straight tilted line.
        # Or more simply, the lateral deviation (Y-axis), since the bend is in X-Z plane by default.
        # If it buckles out of plane, Y will be non-zero.
        # Let's rotate the centerline back to the local frame where Z is longitudinal and X is sagittal.

        # Local Z (longitudinal) is base_dir
        # Local X (sagittal) is normal_dir
        # Local Y (lateral) is cross(base_dir, normal_dir)

        local_z_axis = np.array(base_dir)
        local_x_axis = np.array(normal_dir)
        local_y_axis = np.cross(local_z_axis, local_x_axis)

        # Project centerline coordinates onto local axes
        # Shift so base is at 0,0,0
        shifted_centerline = final_centerline - final_centerline[0]

        local_x = shifted_centerline @ local_x_axis
        local_y = shifted_centerline @ local_y_axis
        local_z = shifted_centerline @ local_z_axis

        # Compute lateral scoliosis index (using local Z and Y)
        sagittal_index, _, max_dev_y = compute_lateral_scoliosis_index(local_z, local_y)

        # Compute Cobb angle from lateral (Y) vs longitudinal (Z)
        # Note: compute_lateral_scoliosis_index returns sagittal_index which is a bit of a misnomer in this context,
        # but it gives a metric of lateral deviation. Let's use max_dev_y as a primary metric.

        # We can also compute max sagittal deviation (X)
        max_dev_x = np.max(np.abs(local_x))

        tip_deflection_z_local = local_z[-1]

        results.append({
            "tilt_deg": tilt_deg,
            "max_dev_sagittal_x": max_dev_x,
            "max_dev_lateral_y": max_dev_y,
            "sagittal_index_y": sagittal_index,
            "tip_z_local": tip_deflection_z_local
        })

    end_time_total = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTotal Runtime: {end_time_total - start_time_total:.2f}s")
    print(f"Peak Memory: {peak_mem / 1024 / 1024:.2f} MB")

    # Save Results
    csv_path = output_dir / "results.csv"
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["tilt_deg", "max_dev_sagittal_x", "max_dev_lateral_y", "sagittal_index_y", "tip_z_local"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {csv_path}")

    # Save params
    with open(output_dir / "params.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["chi_kappa", "chi_M", "L", "n_elements"])
        writer.writerow([chi_kappa, 0.0, L, n_elements])

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot([r["tilt_deg"] for r in results], [r["max_dev_sagittal_x"] for r in results], 'o-', label="Sagittal (In-plane)")
    ax1.plot([r["tilt_deg"] for r in results], [r["max_dev_lateral_y"] for r in results], 's-', label="Lateral (Out-of-plane)")
    ax1.set_xlabel("Load Vector Tilt (degrees)")
    ax1.set_ylabel("Maximum Deviation (m)")
    ax1.set_title("Sagittal vs Lateral Deviation vs Tilt")
    ax1.grid(True)
    ax1.legend()

    ax2.plot([r["tilt_deg"] for r in results], [r["tip_z_local"] for r in results], '^-', color='green')
    ax2.set_xlabel("Load Vector Tilt (degrees)")
    ax2.set_ylabel("Local Tip Z (m)")
    ax2.set_title("Longitudinal Compression vs Tilt")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(output_dir / "plot_tilt_effect.png")
    print(f"Plot saved to {output_dir / 'plot_tilt_effect.png'}")

if __name__ == "__main__":
    run_experiment()
