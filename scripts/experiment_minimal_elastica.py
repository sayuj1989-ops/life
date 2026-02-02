"""
Reproducible experiment for PyElastica rod simulation mapping protein/ECM parameters.

This script maps protein/ECM-inspired parameters (stiffness anisotropy,
preferred curvature) to emergent curvature/torsion outputs using a vertical
rod model (spine-like).

Biological mappings:
- Stiffness Anisotropy: Represents ECM fiber alignment or vertebral geometry.
- Preferred Curvature (chi_kappa): Represents active growth/sensing.
- Torsion Coupling (chi_tau): Represents anisotropic tissue organization.
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


def _get_curvature_profile(profile_type: str, n_elements: int, length: float) -> np.ndarray:
    """
    Generate a geometric curvature profile :math:`\\kappa_{\\text{gen}}` along the rod.

    This helper constructs an intrinsic curvature field defined on the
    material coordinates of the rod, discretized into ``n_elements + 1``
    points along its length.

    Parameters
    ----------
    profile_type :
        String specifying the type of curvature profile to generate.
        Supported options are:

        * ``"constant"``:
            Uniform curvature of magnitude ``2.0`` (1/m) along the entire rod.
        * ``"harmonic"``:
            Sinusoidal modulation around a baseline of ``2.0`` (1/m),
            i.e. ``2.0 + 1.0 * sin(2*pi*s/length)``.
        * ``"kink"``:
            Localized Gaussian bump of additional curvature (amplitude ``5.0``)
            centered at ``0.6 * length`` with width ``0.05 * length``,
            added to a baseline of ``2.0`` (1/m).

    n_elements :
        Number of discretization elements used to represent the rod. The
        generated profile is sampled at ``n_elements + 1`` material points.

    length :
        Total physical length of the rod (in meters) over which the curvature
        profile is defined.

    Returns
    -------
    numpy.ndarray
        Array of shape ``(3, n_elements + 1)`` containing the intrinsic
        curvature components in the rod's material frame:

        * index ``0``: sagittal-plane curvature (e.g., intrinsic
          kyphosis/lordosis or protein-induced bend), populated according
          to ``profile_type``;
        * indices ``1`` and ``2``: set to zero, reserved for out-of-plane
          or torsional curvature components.
    """
    # Initialize kappa_gen (3, n_elements + 1)
    # Index 0: Sagittal curvature (intrinsic kyphosis/lordosis or protein bend)
    kappa_gen = np.zeros((3, n_elements + 1))
    s = np.linspace(0, length, n_elements + 1)

    if profile_type == "constant":
        kappa_gen[0, :] = 2.0  # 1/m (Constant intrinsic curvature)
    elif profile_type == "harmonic":
        # Sinusoidal curvature: 2.0 + 1.0 * sin(2*pi*s/L)
        kappa_gen[0, :] = 2.0 + 1.0 * np.sin(2 * np.pi * s / length)
    elif profile_type == "kink":
        # Localized high curvature: 2.0 + 5.0 * Gaussian
        sigma = 0.05 * length
        center = 0.6 * length
        kappa_gen[0, :] = 2.0 + 5.0 * np.exp(-0.5 * ((s - center) / sigma)**2)
    else:
        raise ValueError(f"Unknown curvature_profile: {profile_type}")

    return kappa_gen


def run_experiment(
    out_file: str,
    anisotropies: list[float],
    chi_kappas: list[float],
    chi_taus: list[float],
    boundary_condition: str,
    n_elements: int = 50,
    final_time: float = 2.0,
    save_every: int = 5000,
    info_center: float = 0.6,
    info_width: float = 0.1,
    info_amplitude: float = 0.1,
    curvature_profile: str = "constant",
):
    """Run the parameter sweep and save results."""
    if not PYELASTICA_AVAILABLE:
        print("Warning: PyElastica is not installed. Using mock objects for testing.")

    print("Running PyElastica experiment...")
    print(
        "Goal: Map stiffness anisotropy & chi_kappa/chi_tau to emergent curvature."
    )
    print(f"Boundary Condition: {boundary_condition}")
    print(f"Results will be saved to: {out_file}")

    # Ensure output directory exists
    out_dir = os.path.dirname(out_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Rod parameters (approximate spine scale)
    # Coordinate system:
    #   d1 (Normal): X-axis. Rotation about d1 = Sagittal bending (Y-Z plane).
    #   d2 (Binormal): Y-axis. Rotation about d2 = Lateral bending (X-Z plane).
    #   d3 (Tangent): Z-axis. Rotation about d3 = Torsion (X-Y plane).
    #
    # Stiffness Anisotropy (R):
    #   Scales bend_matrix[0,0] (Stiffness about d1/Sagittal).
    #   R > 1.0 implies Sagittal Stiffness > Lateral Stiffness.
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
        "chi_tau",
        "boundary_condition",
        "info_center",
        "info_width",
        "info_amplitude",
        "max_curvature",
        "max_torsion",
        "y_tip",
        "s_lat",
        "cobb_angle",
        "runtime_sec",
        "peak_memory_mb",
        "end_to_end_distance",
        "curvature_profile"
    ]

    # Check if file exists to write header
    file_exists = os.path.isfile(out_file)

    with open(out_file, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        print("-" * 120)
        print(
            f"{'Anisotropy':<12} | {'chi_kappa':<10} | {'chi_tau':<10} | {'Max Curv':<10} | "
            f"{'Max Tor':<10} | {'Y Tip':<10} | {'S_lat':<8} | {'Cobb':<8} | "
            f"{'Time (s)':<10} | {'Mem (MB)':<8}"
        )
        print("-" * 120)

        for chi_kappa in chi_kappas:
            for chi_tau in chi_taus:
                for anisotropy in anisotropies:
                    # Start tracking memory and time
                    tracemalloc.start()
                    t0 = time.time()

                    # 1. Setup Information Field (Simulating a protein gradient)
                    s = np.linspace(0, length, n_elements + 1)
                    # Gaussian bump in information density
                    info_density = 0.5 + info_amplitude * np.exp(
                        -0.5 * ((s - info_center * length) / (info_width * length))**2
                    )
                    dIds = np.gradient(info_density, s)
                    info = InfoField1D(s=s, I=info_density, dIds=dIds)

                    # 2. Setup Coupling Parameters
                    # chi_kappa drives curvature correction (Lateral/d2)
                    # chi_tau drives torsion correction (Twist/d3)
                    params = CounterCurvatureParams(
                        chi_kappa=chi_kappa,
                        chi_tau=chi_tau,
                        chi_E=0.0,
                        chi_M=0.0,
                        scale_length=length
                    )

                    # 3. Setup Geometric Curvature (kappa_gen)
                    # Note: chi_kappa couples to index 1 (Lateral Plane/Scoliosis)
                    kappa_gen = _get_curvature_profile(curvature_profile, n_elements, length)

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
                        "chi_tau": chi_tau,
                        "boundary_condition": boundary_condition,
                        "info_center": info_center,
                        "info_width": info_width,
                        "info_amplitude": info_amplitude,
                        "max_curvature": metrics.get('max_curvature', 0.0),
                        "max_torsion": metrics.get('max_torsion', 0.0),
                        "y_tip": metrics.get('y_tip', 0.0),
                        "s_lat": metrics.get('S_lat', 0.0),
                        "cobb_angle": metrics.get('cobb_angle', 0.0),
                        "end_to_end_distance": metrics.get(
                            'end_to_end_distance', 0.0
                        ),
                        "runtime_sec": round(runtime, 4),
                        "peak_memory_mb": round(peak_mb, 2),
                        "curvature_profile": curvature_profile
                    }

                    writer.writerow(row_data)
                    csvfile.flush()  # Ensure write

                    print(
                        f"{anisotropy:<12.2f} | {chi_kappa:<10.2f} | {chi_tau:<10.2f} | "
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
        default="outputs/minimal_experiment_results_v2.csv",
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
        "--chi-tau-list",
        type=float,
        nargs="+",
        default=[0.0],
        help="List of preferred torsion coupling (chi_tau) values to sweep"
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

    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="Run a fast smoke test (short duration, few elements)."
    )

    parser.add_argument(
        "--scenario",
        type=str,
        default="default",
        choices=["default", "intermediate_anisotropy", "high_growth", "vector_scalar_mismatch", "protein_profile"],
        help="Pre-configured scenarios."
    )

    parser.add_argument(
        "--info-center",
        type=float,
        default=0.6,
        help="Center of information field bump (fraction of length)."
    )

    parser.add_argument(
        "--info-width",
        type=float,
        default=0.1,
        help="Width of information field bump (fraction of length)."
    )

    parser.add_argument(
        "--info-amplitude",
        type=float,
        default=0.1,
        help="Amplitude of information field bump."
    )

    parser.add_argument(
        "--curvature-profile",
        type=str,
        default="constant",
        choices=["constant", "harmonic", "kink"],
        help="Type of intrinsic curvature profile."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Handle presets
    anisotropies = args.anisotropy_list
    chi_kappas = args.chi_kappa_list
    chi_taus = args.chi_tau_list
    final_time = args.final_time
    n_elements = args.n_elements

    if args.quick_test:
        print(">>> Quick Test Mode Activated")
        anisotropies = [1.0]
        chi_kappas = [0.0]
        chi_taus = [0.0]
        final_time = 0.1
        n_elements = 20

    elif args.scenario == "intermediate_anisotropy":
        print(">>> Scenario: Intermediate Anisotropy")
        anisotropies = [0.5, 1.0, 2.0, 4.0]
        chi_kappas = [5.0]
        chi_taus = [0.0]

    elif args.scenario == "high_growth":
         print(">>> Scenario: High Growth Drive")
         anisotropies = [1.0, 5.0]
         chi_kappas = [10.0, 15.0]
         chi_taus = [0.0]

    elif args.scenario == "vector_scalar_mismatch":
         print(">>> Scenario: Vector-Scalar Mismatch (Microgravity Simulation)")
         # Vector: Anisotropy (Structural Alignment) - Decreasing implies loss of directional cue
         # Scalar: Chi_Kappa (Growth/Sensing Gain) - Increasing implies compensatory gain increase (Senescence)
         # High Anisotropy (10.0) ~ Healthy Fibrillin/Collagen
         # Low Anisotropy (1.0) ~ Isotropic/Degraded Matrix
         anisotropies = [10.0, 5.0, 2.0, 1.0]
         chi_kappas = [0.0, 5.0, 10.0, 20.0]
         chi_taus = [0.0]

    elif args.scenario == "protein_profile":
         print(">>> Scenario: Protein Profile (Harmonic Curvature)")
         # Simulating a protein with varying intrinsic curvature and high stiffness
         anisotropies = [5.0]
         chi_kappas = [5.0]
         chi_taus = [0.0]
         args.curvature_profile = "harmonic"

    run_experiment(
        out_file=args.out_file,
        anisotropies=anisotropies,
        chi_kappas=chi_kappas,
        chi_taus=chi_taus,
        boundary_condition=args.boundary_condition,
        n_elements=n_elements,
        final_time=final_time,
        info_center=args.info_center,
        info_width=args.info_width,
        info_amplitude=args.info_amplitude,
        curvature_profile=args.curvature_profile,
    )
