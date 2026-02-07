"""
Reproducible experiment mapping specific Protein/ECM biological scenarios to
physical parameters in a PyElastica rod simulation.

This script explicitly connects biological entities (e.g., Fibrillin-1, Piezo2)
to their hypothesized mechanical effects (Anisotropy, Stiffness Modulation,
Curvature Gain).

Scenarios:
- Control: Baseline healthy spine.
- Fibrillin_Loss (Marfan-like): Reduced stiffness anisotropy.
- Piezo2_Gain (Proprioceptive enhancement): High active curvature correction.
- Microgravity_Mismatch: High Anisotropy but High Gain (conflicting signals).
- Stiffness_Modulated: Stiffness varies with information density (chi_E).
"""

import argparse
import csv
import os
import sys
import time
import tracemalloc
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

# Ensure src is in python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.countercurvature.coupling import CounterCurvatureParams
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.pyelastica_bridge import (
    PYELASTICA_AVAILABLE,
    CounterCurvatureRodSystem,
)


@dataclass
class ProteinScenario:
    """Defines the mapping from a biological condition to physical parameters."""
    name: str
    description: str
    anisotropy: float      # Stiffness Anisotropy (Sagittal/Lateral)
    chi_kappa: float       # Active curvature gain (Growth)
    chi_tau: float         # Active torsion gain (Twist)
    chi_E: float           # Stiffness modulation by info density
    boundary_condition: str = "fixed"


# Define the Biological Scenarios
SCENARIOS: Dict[str, ProteinScenario] = {
    "Control": ProteinScenario(
        name="Control",
        description="Baseline healthy parameters.",
        anisotropy=2.0,
        chi_kappa=5.0,
        chi_tau=0.0,
        chi_E=0.0
    ),
    "Fibrillin_Loss": ProteinScenario(
        name="Fibrillin_Loss",
        description="Reduced anisotropy due to ECM degradation (e.g. Marfan).",
        anisotropy=1.0,  # Isotropic
        chi_kappa=5.0,
        chi_tau=0.0,
        chi_E=0.0
    ),
    "Piezo2_Gain": ProteinScenario(
        name="Piezo2_Gain",
        description="Enhanced mechanosensation driving active correction.",
        anisotropy=2.0,
        chi_kappa=15.0,  # Strong active correction
        chi_tau=0.0,
        chi_E=0.0
    ),
    "Vector_Scalar_Mismatch": ProteinScenario(
        name="Vector_Scalar_Mismatch",
        description="High structural anisotropy but conflicting scalar gain (e.g. Microgravity).",
        anisotropy=5.0,  # Very stiff/aligned
        chi_kappa=20.0,  # Excessive gain
        chi_tau=0.0,
        chi_E=0.0
    ),
    "Torsional_Instability": ProteinScenario(
        name="Torsional_Instability",
        description="Presence of torsional coupling (e.g. Planar Cell Polarity defect).",
        anisotropy=2.0,
        chi_kappa=5.0,
        chi_tau=5.0,     # Torsion active
        chi_E=0.0
    ),
    "Stiffening_Response": ProteinScenario(
        name="Stiffening_Response",
        description="Tissue stiffens in response to information density.",
        anisotropy=2.0,
        chi_kappa=5.0,
        chi_tau=0.0,
        chi_E=1.0        # Stiffens where info is high
    )
}


def run_protein_experiment(
    out_file: str,
    selected_scenarios: Optional[List[str]] = None,
    n_elements: int = 50,
    final_time: float = 2.0,
    save_every: int = 5000,
    info_center: float = 0.6,
    info_width: float = 0.1,
    info_amplitude: float = 0.1,
):
    """Run the experiment for selected protein scenarios."""
    if not PYELASTICA_AVAILABLE:
        print("Warning: PyElastica is not installed. Using mock objects for testing.")

    print("Running Protein Physics Experiment...")
    print(f"Results will be saved to: {out_file}")

    # Ensure output directory exists
    out_dir = os.path.dirname(out_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Filter scenarios if list provided
    scenarios_to_run = []
    if selected_scenarios:
        for name in selected_scenarios:
            if name in SCENARIOS:
                scenarios_to_run.append(SCENARIOS[name])
            else:
                print(f"Warning: Scenario '{name}' not found. Skipping.")
    else:
        scenarios_to_run = list(SCENARIOS.values())

    if not scenarios_to_run:
        print("No valid scenarios to run.")
        return

    # Simulation constants
    length = 0.5
    radius = 0.01
    E0 = 1e6
    rho = 1000.0
    gravity = 9.81
    dt = 1e-5

    # Prepare CSV
    fieldnames = [
        "timestamp",
        "scenario_name",
        "description",
        "stiffness_anisotropy",
        "chi_kappa",
        "chi_tau",
        "chi_E",
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

    file_exists = os.path.isfile(out_file)
    with open(out_file, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        print("-" * 140)
        print(
            f"{'Scenario':<25} | {'Aniso':<5} | {'chi_k':<5} | {'chi_t':<5} | {'chi_E':<5} | "
            f"{'Max Curv':<8} | {'Max Tor':<8} | {'S_lat':<8} | {'Time (s)':<8} | {'Mem (MB)':<8}"
        )
        print("-" * 140)

        for scenario in scenarios_to_run:
            tracemalloc.start()
            t0 = time.time()

            # 1. Setup Info Field
            s = np.linspace(0, length, n_elements + 1)
            info_density = 0.5 + info_amplitude * np.exp(
                -0.5 * ((s - info_center * length) / (info_width * length))**2
            )
            dIds = np.gradient(info_density, s)
            info = InfoField1D(s=s, I=info_density, dIds=dIds)

            # 2. Setup Params
            params = CounterCurvatureParams(
                chi_kappa=scenario.chi_kappa,
                chi_tau=scenario.chi_tau,
                chi_E=scenario.chi_E,
                chi_M=0.0,
                scale_length=length
            )

            # 3. Create Rod
            # Constant intrinsic curvature (Kyphosis/Lordosis equivalent)
            kappa_gen = np.zeros((3, n_elements + 1))
            kappa_gen[0, :] = 2.0

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
                base_direction=(0.0, 0.0, 1.0),
                normal=(1.0, 0.0, 0.0),
                stiffness_anisotropy=scenario.anisotropy
            )

            # 4. Run Sim
            result = rod_system.run_simulation(
                final_time=final_time,
                dt=dt,
                save_every=save_every,
                gravity=gravity,
                boundary_condition=scenario.boundary_condition
            )

            t1 = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            runtime = t1 - t0
            peak_mb = peak / (1024 * 1024)

            metrics = result.compute_final_metrics()

            row_data = {
                "timestamp": datetime.now().isoformat(),
                "scenario_name": scenario.name,
                "description": scenario.description,
                "stiffness_anisotropy": scenario.anisotropy,
                "chi_kappa": scenario.chi_kappa,
                "chi_tau": scenario.chi_tau,
                "chi_E": scenario.chi_E,
                "boundary_condition": scenario.boundary_condition,
                "max_curvature": metrics.get('max_curvature', 0.0),
                "max_torsion": metrics.get('max_torsion', 0.0),
                "y_tip": metrics.get('y_tip', 0.0),
                "s_lat": metrics.get('S_lat', 0.0),
                "cobb_angle": metrics.get('cobb_angle', 0.0),
                "end_to_end_distance": metrics.get('end_to_end_distance', 0.0),
                "runtime_sec": round(runtime, 4),
                "peak_memory_mb": round(peak_mb, 2)
            }

            writer.writerow(row_data)
            csvfile.flush()

            print(
                f"{scenario.name:<25} | {scenario.anisotropy:<5.1f} | {scenario.chi_kappa:<5.1f} | "
                f"{scenario.chi_tau:<5.1f} | {scenario.chi_E:<5.1f} | "
                f"{row_data['max_curvature']:<8.4f} | "
                f"{row_data['max_torsion']:<8.4f} | "
                f"{row_data['s_lat']:<8.4f} | {runtime:<8.4f} | "
                f"{peak_mb:<8.2f}"
            )

    print("-" * 140)
    print("Experiment complete.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Protein/ECM Physics Experiment"
    )
    parser.add_argument(
        "--out-file",
        type=str,
        default="outputs/protein_physics_results.csv",
        help="Path to output CSV file"
    )
    parser.add_argument(
        "--scenarios",
        type=str,
        nargs="+",
        help="List of specific scenarios to run (names). If empty, runs all."
    )
    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="Run a fast smoke test (short duration, few elements)."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    final_time = 2.0
    n_elements = 50

    if args.quick_test:
        print(">>> Quick Test Mode Activated")
        final_time = 0.1
        n_elements = 20

    run_protein_experiment(
        out_file=args.out_file,
        selected_scenarios=args.scenarios,
        n_elements=n_elements,
        final_time=final_time
    )
