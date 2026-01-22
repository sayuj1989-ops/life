"""
Reproducible experiment for PyElastica rod simulation mapping protein/ECM parameters.

This script maps protein/ECM-inspired parameters (stiffness anisotropy,
preferred curvature) to emergent curvature/torsion outputs using a vertical
rod model (spine-like).

Biological mappings:
- Stiffness Anisotropy: Represents ECM fiber alignment or vertebral geometry.
- Preferred Curvature (chi_kappa): Represents active growth/sensing.
- Boundary Conditions: Represents pelvic anchoring (fixed vs pinned).
"""

import argparse
import csv
import os
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path

import numpy as np

# Ensure src is in python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.countercurvature.coupling import CounterCurvatureParams
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.pyelastica_bridge import (
    PYELASTICA_AVAILABLE,
    CounterCurvatureRodSystem,
)


def run_experiment(
    out_file: str,
    anisotropies: list[float],
    chi_kappas: list[float],
    boundary_condition: str,
    n_elements: int = 50,
    final_time: float = 2.0,
    save_every: int = 5000,
):
    """Run the parameter sweep and save results."""
    if not PYELASTICA_AVAILABLE:
        print("Error: PyElastica is not installed.")
        print("To install, run: pip install pyelastica")
        print("Or refer to https://github.com/GazzolaLab/PyElastica")
        sys.exit(1)

    print("Running PyElastica experiment...")
    print(
        "Goal: Map stiffness anisotropy & chi_kappa to emergent curvature."
    )
    print(f"Boundary Condition: {boundary_condition}")
    print(f"Results will be saved to: {out_file}")

    # Ensure output directory exists
    out_dir = os.path.dirname(out_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Rod parameters (approximate spine scale)
    length = 0.5  # meters
    radius = 0.01  # meters
    E0 = 1e6      # Pa (soft tissue/cartilage range)
    rho = 1000.0  # kg/m^3
    gravity = 9.81
    dt = 1e-5  # Stable time step for these parameters

    # Prepare CSV
    fieldnames = [
        "timestamp",
        "stiffness_anisotropy",
        "chi_kappa",
        "boundary_condition",
        "max_curvature",
        "max_torsion",
        "y_tip",
        "s_lat",
        "cobb_angle",
        "runtime_sec",
        "peak_memory_mb",
        "end_to_end_distance"
    ]

    # Check if file exists to write header
    file_exists = os.path.isfile(out_file)

    with open(out_file, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        print("-" * 120)
        print(
            f"{'Anisotropy':<12} | {'chi_kappa':<10} | {'Max Curv':<10} | "
            f"{'Max Tor':<10} | {'Y Tip':<10} | {'S_lat':<8} | {'Cobb':<8} | "
            f"{'Time (s)':<10} | {'Mem (MB)':<8}"
        )
        print("-" * 120)

        for chi_kappa in chi_kappas:
            for anisotropy in anisotropies:
                # Start tracking memory and time
                tracemalloc.start()
                t0 = time.time()

                # 1. Setup Information Field (Simulating a protein gradient)
                s = np.linspace(0, length, n_elements + 1)
                # Gaussian bump in information density
                info_density = 0.5 + 0.1 * np.exp(
                    -0.5 * ((s - 0.6 * length) / (0.1 * length))**2
                )
                dIds = np.gradient(info_density, s)
                info = InfoField1D(s=s, I=info_density, dIds=dIds)

                # 2. Setup Coupling Parameters
                # chi_kappa drives curvature correction
                params = CounterCurvatureParams(
                    chi_kappa=chi_kappa,
                    chi_E=0.0,
                    chi_M=0.0,
                    scale_length=length
                )

                # 3. Setup Geometric Curvature (kappa_gen)
                # Constant intrinsic curvature about d1 (index 0)
                kappa_gen = np.zeros((3, n_elements + 1))
                kappa_gen[0, :] = 2.0  # 1/m

                # 4. Create Rod System
                rod_system = CounterCurvatureRodSystem.from_iec(
                    info=info,
                    params=params,
                    length=length,
                    n_elements=n_elements,
                    E0=E0,
                    rho=rho,
                    radius=radius,
                    kappa_gen=kappa_gen,
                    gravity=gravity,
                    base_position=(0.0, 0.0, 0.0),
                    base_direction=(0.0, 0.0, 1.0),  # Vertical
                    normal=(1.0, 0.0, 0.0),         # Normal in X
                    stiffness_anisotropy=anisotropy
                )

                # 5. Run Simulation
                result = rod_system.run_simulation(
                    final_time=final_time,
                    dt=dt,
                    save_every=save_every,
                    gravity=gravity,
                    boundary_condition=boundary_condition
                )

                t1 = time.time()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                runtime = t1 - t0
                peak_mb = peak / (1024 * 1024)

                # 6. Compute Metrics
                metrics = result.compute_final_metrics()

                # 7. Store and Print
                row_data = {
                    "timestamp": datetime.now().isoformat(),
                    "stiffness_anisotropy": anisotropy,
                    "chi_kappa": chi_kappa,
                    "boundary_condition": boundary_condition,
                    "max_curvature": metrics.get('max_curvature', 0.0),
                    "max_torsion": metrics.get('max_torsion', 0.0),
                    "y_tip": metrics.get('y_tip', 0.0),
                    "s_lat": metrics.get('S_lat', 0.0),
                    "cobb_angle": metrics.get('cobb_angle', 0.0),
                    "end_to_end_distance": metrics.get(
                        'end_to_end_distance', 0.0
                    ),
                    "runtime_sec": round(runtime, 4),
                    "peak_memory_mb": round(peak_mb, 2)
                }

                writer.writerow(row_data)
                csvfile.flush()  # Ensure write

                print(
                    f"{anisotropy:<12.2f} | {chi_kappa:<10.2f} | "
                    f"{row_data['max_curvature']:<10.4f} | "
                    f"{row_data['max_torsion']:<10.4f} | "
                    f"{row_data['y_tip']:<10.4f} | "
                    f"{row_data['s_lat']:<8.4f} | "
                    f"{row_data['cobb_angle']:<8.4f} | {runtime:<10.4f} | "
                    f"{peak_mb:<8.2f}"
                )

    print("-" * 120)
    print("Experiment complete.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="PyElastica Spinal Rod Experiment"
    )

    parser.add_argument(
        "--out-file",
        type=str,
        default="outputs/minimal_experiment_results.csv",
        help="Path to output CSV file"
    )

    parser.add_argument(
        "--anisotropy-list",
        type=float,
        nargs="+",
        default=[0.1, 0.5, 1.0, 2.0, 5.0],
        help="List of stiffness anisotropy values to sweep"
    )

    parser.add_argument(
        "--chi-kappa-list",
        type=float,
        nargs="+",
        default=[0.0, 5.0, 10.0],
        help="List of preferred curvature coupling (chi_kappa) values to sweep"
    )

    parser.add_argument(
        "--boundary-condition",
        type=str,
        default="fixed",
        choices=["fixed", "pinned"],
        help="Boundary condition at the base"
    )

    parser.add_argument(
        "--final-time", type=float, default=2.0, help="Simulation duration (s)"
    )

    parser.add_argument(
        "--n-elements", type=int, default=50, help="Number of rod elements"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    run_experiment(
        out_file=args.out_file,
        anisotropies=args.anisotropy_list,
        chi_kappas=args.chi_kappa_list,
        boundary_condition=args.boundary_condition,
        n_elements=args.n_elements,
        final_time=args.final_time
    )
