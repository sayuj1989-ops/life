"""
Experiment: Optimization Failure — Exploding Gradient Map.

This script implements Phase 1, Week 3 of the Gravity Optimization research schedule.
It maps the "Exploding Gradient" region where high information-to-curvature coupling
(chi_kappa) combined with low stiffness anisotropy leads to instability (scoliosis).

Key innovation: Sensory noise injection into the information gradient.
    grad_I_noisy = grad_I + eta, where eta ~ N(0, sigma_noise)

This models imprecise mechanosensing (e.g. PIEZO2 dysfunction, proprioceptive
error) that degrades the quality of the shape-maintenance gradient signal.

Hypothesis:
    Scoliosis emerges as an "Exploding Gradient" when:
    1. The Learning Rate (chi_kappa) exceeds structural damping (anisotropy)
    2. Sensory noise (sigma) degrades gradient fidelity below a critical threshold
    3. The combination creates a wedge-shaped instability region in
       (chi_kappa, sigma_noise) space

Measurable outputs:
    - Phase diagram of Cobb Angle in (chi_kappa, sigma_noise) space
    - Critical noise threshold sigma_c(chi_kappa) for scoliosis onset
    - Torsion emergence as a secondary instability marker
    - Comparison: noisy vs noise-free gradient descent convergence

References:
    - Research Schedule Phase 1, Week 3: "Optimization Failure"
    - Hypothesis Register: H_2026_02_08_EnergyPhase
"""

import argparse
import csv
import os
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path
from typing import List

import numpy as np

sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from spinalmodes.countercurvature.coupling import CounterCurvatureParams
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.pyelastica_bridge import (
    CounterCurvatureRodSystem,
    compute_U_CC,
    verify_pyelastica_installation,
)


def create_noisy_info_field(
    s: np.ndarray,
    info_center_frac: float = 0.5,
    info_width_frac: float = 0.1,
    info_amplitude: float = 0.5,
    sigma_noise: float = 0.0,
    rng: np.random.Generator = None,
) -> InfoField1D:
    """Create an information field with optional gradient noise.

    The base field is a Gaussian bump (representing HOX-encoded shape programme).
    Noise is injected into the gradient dI/ds to model imprecise mechanosensing.

    Parameters
    ----------
    s : np.ndarray
        Arc-length grid.
    info_center_frac : float
        Center of Gaussian bump as fraction of length.
    info_width_frac : float
        Width of Gaussian bump as fraction of length.
    info_amplitude : float
        Amplitude of the information bump.
    sigma_noise : float
        Standard deviation of additive Gaussian noise on dI/ds.
    rng : np.random.Generator
        Random number generator for reproducibility.

    Returns
    -------
    InfoField1D
        Information field with noisy gradient.
    """
    length = s[-1] - s[0]
    center = info_center_frac * length
    width = info_width_frac * length

    # Base information field (clean signal)
    I = 0.5 + info_amplitude * np.exp(-0.5 * ((s - center) / width) ** 2)
    dIds_clean = np.gradient(I, s)

    # Inject sensory noise into the gradient
    if sigma_noise > 0.0 and rng is not None:
        noise = rng.normal(0.0, sigma_noise, size=dIds_clean.shape)
        dIds = dIds_clean + noise
    else:
        dIds = dIds_clean

    return InfoField1D(s=s, I=I, dIds=dIds)


def run_optimization_failure_sweep(
    out_file: str,
    chi_kappas: List[float],
    sigma_noises: List[float],
    n_trials: int = 3,
    n_elements: int = 50,
    final_time: float = 2.0,
    seed: int = 42,
):
    """Run the optimization failure parameter sweep.

    For each (chi_kappa, sigma_noise) pair, runs n_trials stochastic realisations
    and records the mean and std of scoliosis metrics.

    Parameters
    ----------
    out_file : str
        Path to output CSV file.
    chi_kappas : list of float
        Information-curvature coupling strengths to sweep.
    sigma_noises : list of float
        Noise levels for gradient corruption.
    n_trials : int
        Number of stochastic trials per parameter pair.
    n_elements : int
        Number of rod elements.
    final_time : float
        Simulation duration (seconds).
    seed : int
        Base random seed for reproducibility.
    """
    verify_pyelastica_installation(exit_on_fail=True)

    print("=" * 100)
    print("EXPERIMENT: Optimization Failure — Exploding Gradient Map")
    print("=" * 100)
    print(f"Sweeping chi_kappa: {chi_kappas}")
    print(f"Sweeping sigma_noise: {sigma_noises}")
    print(f"Trials per point: {n_trials}")
    print(f"Output: {out_file}")
    print("=" * 100)

    # Rod parameters
    length = 0.5      # metres
    radius = 0.01     # metres
    E0 = 1e6          # Pa
    rho = 1000.0      # kg/m^3
    gravity = 9.81
    dt = 1e-5
    anisotropy = 1.5  # Moderate anisotropy (between low=1.0 and high=5.0)

    # Prepare output
    out_dir = os.path.dirname(out_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    fieldnames = [
        "timestamp", "chi_kappa", "sigma_noise", "trial",
        "cobb_angle", "max_torsion", "S_lat", "max_curvature",
        "U_CC", "U_gravity", "U_elastic", "U_info", "info_gain_ratio",
        "runtime_sec", "peak_memory_mb",
    ]

    file_exists = os.path.isfile(out_file)
    with open(out_file, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        print(
            f"{'chi_k':<8} | {'sigma':<8} | {'trial':<6} | "
            f"{'Cobb':<8} | {'Torsion':<9} | {'S_lat':<8} | "
            f"{'U_CC':<12} | {'Time':<8}"
        )
        print("-" * 90)

        total = len(chi_kappas) * len(sigma_noises) * n_trials
        count = 0

        for chi_kappa in chi_kappas:
            for sigma_noise in sigma_noises:
                for trial in range(n_trials):
                    count += 1
                    rng = np.random.default_rng(seed + trial * 1000 + hash(
                        (chi_kappa, sigma_noise)
                    ) % 10000)

                    tracemalloc.start()
                    t0 = time.time()

                    # Create noisy information field
                    s = np.linspace(0, length, n_elements + 1)
                    info = create_noisy_info_field(
                        s, sigma_noise=sigma_noise, rng=rng
                    )

                    # Coupling: pure curvature drive (no active moments)
                    params = CounterCurvatureParams(
                        chi_kappa=chi_kappa,
                        chi_tau=0.0,
                        chi_E=0.0,
                        chi_M=0.0,
                        scale_length=length,
                    )

                    # Baseline sagittal curvature
                    kappa_gen = np.zeros((3, n_elements + 1))
                    kappa_gen[0, :] = 2.0  # Sagittal kyphosis

                    # Create and run
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
                        stiffness_anisotropy=anisotropy,
                    )

                    result = rod_system.run_simulation(
                        final_time=final_time,
                        dt=dt,
                        save_every=5000,
                        gravity=gravity,
                        boundary_condition="fixed",
                        progress_bar=False,
                    )

                    t1 = time.time()
                    _, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    # Compute metrics
                    sim_metrics = result.compute_final_metrics()
                    cost = compute_U_CC(result, info, params, gravity, rho, E0)

                    row = {
                        "timestamp": datetime.now().isoformat(),
                        "chi_kappa": chi_kappa,
                        "sigma_noise": sigma_noise,
                        "trial": trial,
                        "cobb_angle": sim_metrics.get("cobb_angle", 0.0),
                        "max_torsion": sim_metrics.get("max_torsion", 0.0),
                        "S_lat": sim_metrics.get("S_lat", 0.0),
                        "max_curvature": sim_metrics.get("max_curvature", 0.0),
                        "U_CC": cost["U_CC"],
                        "U_gravity": cost["U_gravity"],
                        "U_elastic": cost["U_elastic"],
                        "U_info": cost["U_info"],
                        "info_gain_ratio": cost["info_gain_ratio"],
                        "runtime_sec": round(t1 - t0, 4),
                        "peak_memory_mb": round(peak / (1024 * 1024), 2),
                    }
                    writer.writerow(row)
                    csvfile.flush()

                    print(
                        f"{chi_kappa:<8.2f} | {sigma_noise:<8.3f} | {trial:<6d} | "
                        f"{row['cobb_angle']:<8.2f} | {row['max_torsion']:<9.4f} | "
                        f"{row['S_lat']:<8.4f} | {row['U_CC']:<12.4f} | "
                        f"{row['runtime_sec']:<8.3f}"
                    )

    print("=" * 100)
    print(f"Experiment complete. {count}/{total} simulations finished.")
    generate_report(out_file)


def generate_report(csv_file: str):
    """Generate a Markdown report from the sweep results."""
    md_file = str(Path(csv_file).with_suffix(".md"))

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No data to report.")
        return

    with open(md_file, "w") as f:
        f.write("# Optimization Failure: Exploding Gradient Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Source:** `{os.path.basename(csv_file)}`\n\n")

        f.write("## Hypothesis\n\n")
        f.write("Scoliosis emerges as an 'Exploding Gradient' when the learning rate\n")
        f.write("(chi_kappa) exceeds structural damping AND sensory noise degrades\n")
        f.write("gradient fidelity below a critical threshold.\n\n")

        # Aggregate by (chi_kappa, sigma_noise)
        from collections import defaultdict
        groups = defaultdict(list)
        for r in rows:
            key = (float(r["chi_kappa"]), float(r["sigma_noise"]))
            groups[key].append(float(r["cobb_angle"]))

        f.write("## Mean Cobb Angle by (chi_kappa, sigma_noise)\n\n")
        f.write("| chi_kappa | sigma_noise | mean_Cobb | std_Cobb | n_scoliotic |\n")
        f.write("|-----------|-------------|-----------|----------|-------------|\n")

        for (ck, sn), cobbs in sorted(groups.items()):
            mean_c = np.mean(cobbs)
            std_c = np.std(cobbs)
            n_scol = sum(1 for c in cobbs if c > 10.0)
            f.write(f"| {ck:.2f} | {sn:.3f} | {mean_c:.2f} | {std_c:.2f} | {n_scol}/{len(cobbs)} |\n")

        # Identify critical noise threshold
        f.write("\n## Critical Noise Threshold\n\n")
        f.write("sigma_c is the noise level at which mean Cobb angle first exceeds 10 degrees.\n\n")

        chi_vals = sorted(set(float(r["chi_kappa"]) for r in rows))
        for ck in chi_vals:
            sigma_c = None
            sigma_vals = sorted(set(sn for (c, sn) in groups.keys() if c == ck))
            for sn in sigma_vals:
                if np.mean(groups[(ck, sn)]) > 10.0:
                    sigma_c = sn
                    break
            if sigma_c is not None:
                f.write(f"- chi_kappa = {ck:.2f}: sigma_c ≈ {sigma_c:.3f}\n")
            else:
                f.write(f"- chi_kappa = {ck:.2f}: no scoliosis onset detected\n")

        # Cost function analysis
        f.write("\n## Cost Function U_CC Analysis\n\n")
        f.write("| chi_kappa | sigma_noise | U_CC (mean) | U_info (mean) | info_gain_ratio |\n")
        f.write("|-----------|-------------|-------------|---------------|------------------|\n")

        cost_groups = defaultdict(list)
        for r in rows:
            key = (float(r["chi_kappa"]), float(r["sigma_noise"]))
            cost_groups[key].append({
                "U_CC": float(r["U_CC"]),
                "U_info": float(r["U_info"]),
                "info_gain_ratio": float(r["info_gain_ratio"]),
            })

        for (ck, sn), costs in sorted(cost_groups.items()):
            mean_ucc = np.mean([c["U_CC"] for c in costs])
            mean_ui = np.mean([c["U_info"] for c in costs])
            mean_igr = np.mean([c["info_gain_ratio"] for c in costs])
            f.write(f"| {ck:.2f} | {sn:.3f} | {mean_ucc:.4f} | {mean_ui:.4f} | {mean_igr:.4f} |\n")

    print(f"Report generated: {md_file}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Optimization Failure: Exploding Gradient Experiment"
    )
    parser.add_argument(
        "--out-file", type=str,
        default="outputs/optimization_failure/exploding_gradient.csv",
    )
    parser.add_argument("--quick-test", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.quick_test:
        chi_kappas = [0.0, 10.0, 20.0]
        sigma_noises = [0.0, 0.5, 1.0]
        n_trials = 2
        n_elements = 20
        final_time = 0.1
    else:
        chi_kappas = [0.0, 2.0, 5.0, 10.0, 15.0, 20.0]
        sigma_noises = [0.0, 0.1, 0.2, 0.5, 1.0, 2.0]
        n_trials = 5
        n_elements = 50
        final_time = 2.0

    run_optimization_failure_sweep(
        out_file=args.out_file,
        chi_kappas=chi_kappas,
        sigma_noises=sigma_noises,
        n_trials=n_trials,
        n_elements=n_elements,
        final_time=final_time,
        seed=args.seed,
    )
