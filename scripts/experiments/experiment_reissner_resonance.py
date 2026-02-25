"""
Reissner Resonance Experiment Script.

This script investigates the hypothesis (H_2026_03_10_RF_Resonance) that the Reissner Fiber
acts as a tuned mechanical resonator, and that specific frequencies (e.g., 1-2 Hz) of
cyclic loading or active curvature modulation can lead to resonant amplification or damping
of spinal curvature.

It uses the PyElastica bridge to simulate a rod under gravity with time-varying
'active curvature' (chi_kappa) modulation.

Usage:
    python scripts/experiments/experiment_reissner_resonance.py --frequencies 0.5 1.0 2.0 4.0
"""

import argparse
import csv
import math
import os
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np

# Ensure src is in python path
current_file = Path(__file__).resolve()
src_path = current_file.parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

try:
    from spinalmodes.countercurvature.pyelastica_bridge import (
        CounterCurvatureRodSystem,
        CounterCurvatureParams,
        InfoField1D,
        CircadianParams,
        PYELASTICA_AVAILABLE,
        SimulationResult
    )
except ImportError as e:
    # If imports fail (e.g., missing dependencies), we handle it gracefully in main
    PYELASTICA_AVAILABLE = False
    print(f"Import Warning: {e}")


def run_resonance_experiment(
    out_dir: str = "outputs/reissner_resonance",
    frequencies: List[float] = None,
    amplitude: float = 0.5,
    base_chi_kappa: float = 5.0,
    duration: float = 2.0,
    n_elements: int = 50,
    dt: float = 1e-4,
    quick_test: bool = False
) -> List[Dict[str, Any]]:
    """
    Run the resonance frequency sweep.

    Args:
        out_dir: Directory to save results.
        frequencies: List of frequencies (Hz) to sweep.
        amplitude: Modulation amplitude (relative to base_chi_kappa).
        base_chi_kappa: Baseline active curvature coupling strength.
        duration: Simulation duration (s).
        n_elements: Number of rod elements.
        dt: Time step (s).
        quick_test: If True, override parameters for a fast run.

    Returns:
        List of result dictionaries.
    """
    if not PYELASTICA_AVAILABLE:
        print("Error: PyElastica not available. Cannot run experiment.")
        return []

    if frequencies is None:
        frequencies = [0.5, 1.0, 2.0, 4.0]

    if quick_test:
        frequencies = [1.0]
        duration = 0.1
        n_elements = 20

    # Ensure output directory exists
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    csv_file = out_path / "resonance_results.csv"
    md_file = out_path / "resonance_report.md"

    print(f"Starting Reissner Resonance Experiment...")
    print(f"  Output Dir: {out_dir}")
    print(f"  Frequencies: {frequencies} Hz")
    print(f"  Amplitude: {amplitude}")
    print(f"  Base Chi_Kappa: {base_chi_kappa}")

    results = []

    # Fixed parameters
    length = 0.5  # meters
    radius = 0.01
    E0 = 1e6
    rho = 1000.0
    gravity = 9.81

    # Header for console output
    print("-" * 100)
    print(f"{'Freq(Hz)':<10} | {'Period(s)':<10} | {'Max Cobb':<10} | {'Max K':<10} | {'Energy(J)':<10} | {'Time(s)':<10}")
    print("-" * 100)

    for freq in frequencies:
        tracemalloc.start()
        t0 = time.time()

        period = 1.0 / freq if freq > 0 else 0.0

        # 1. Setup Information Field (Uniform for simplicity, or gradient)
        s = np.linspace(0, length, n_elements + 1)
        # Gradient field to induce base curvature
        I = 0.5 + 0.5 * (s / length)
        dIds = np.gradient(I, s)
        info = InfoField1D(s=s, I=I, dIds=dIds)

        # 2. Setup Params
        # We start with base_chi_kappa. The modulation will oscillate around this.
        params = CounterCurvatureParams(
            chi_kappa=base_chi_kappa,
            chi_tau=0.0,
            chi_E=0.0,
            chi_M=0.0,
            scale_length=length
        )

        # 3. Setup Circadian (Resonant) Modulation
        # We reuse CircadianParams but with short periods (Hz range)
        modulation_params = CircadianParams(
            period=period,
            amplitude=amplitude,
            phase=0.0
        )

        # 4. Create System
        # Initial slight kyphosis to break symmetry
        kappa_gen = np.zeros((3, n_elements + 1))
        kappa_gen[1, :] = 2.0 # Natural kyphosis

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
            base_direction=(0.0, 0.0, 1.0), # Vertical
            normal=(1.0, 0.0, 0.0)
        )

        # 5. Run Simulation
        result = rod_system.run_simulation(
            final_time=duration,
            dt=dt,
            save_every=int(duration / dt / 50), # 50 snapshots
            gravity=gravity,
            boundary_condition="fixed",
            circadian_params=modulation_params,
            progress_bar=False
        )

        t1 = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # 6. Compute Metrics
        metrics = result.compute_final_metrics()

        # Analyze Oscillation Amplitude (Standard Deviation of Tip Position)
        # result.centerline is (time, nodes, 3)
        # tip pos is (time, -1, 3)
        tip_traj = result.centerline[:, -1, :]
        tip_x_std = np.std(tip_traj[:, 0]) # Lateral sway
        tip_y_std = np.std(tip_traj[:, 1]) # Sagittal sway

        row = {
            "frequency_hz": freq,
            "period_s": period,
            "amplitude": amplitude,
            "base_chi_kappa": base_chi_kappa,
            "max_cobb_angle": metrics.get("cobb_angle", 0.0),
            "max_curvature": metrics.get("max_curvature", 0.0),
            "total_energy": metrics.get("bending_energy", 0.0) + metrics.get("gravitational_energy", 0.0),
            "tip_sway_lateral": tip_x_std,
            "tip_sway_sagittal": tip_y_std,
            "runtime_sec": t1 - t0,
            "peak_memory_mb": peak / (1024 * 1024)
        }
        results.append(row)

        print(
            f"{freq:<10.2f} | {period:<10.4f} | "
            f"{row['max_cobb_angle']:<10.2f} | {row['max_curvature']:<10.2f} | "
            f"{row['total_energy']:<10.2e} | {row['runtime_sec']:<10.2f}"
        )

    # Save to CSV
    if results:
        keys = list(results[0].keys())
        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        print(f"\nResults saved to {csv_file}")

        _generate_markdown_report(md_file, results)
        print(f"Report saved to {md_file}")

    return results


def _generate_markdown_report(filepath: Path, results: List[Dict[str, Any]]):
    """Generate a Markdown report from results."""
    with open(filepath, "w") as f:
        f.write("# Reissner Resonance Experiment Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Hypothesis\n")
        f.write("Exploring if specific modulation frequencies amplify curvature (Resonance).\n\n")

        f.write("## Results Summary\n")
        f.write("| Freq (Hz) | Cobb Angle (deg) | Max Curvature | Tip Sway (Lat) | Energy (J) |\n")
        f.write("|---|---|---|---|---|\n")

        for r in results:
            f.write(
                f"| {r['frequency_hz']:.2f} | {r['max_cobb_angle']:.2f} | "
                f"{r['max_curvature']:.2f} | {r['tip_sway_lateral']:.4e} | "
                f"{r['total_energy']:.2e} |\n"
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reissner Resonance Experiment")
    parser.add_argument("--frequencies", type=float, nargs="+", help="List of frequencies (Hz)")
    parser.add_argument("--amplitude", type=float, default=0.5, help="Modulation amplitude")
    parser.add_argument("--duration", type=float, default=2.0, help="Simulation duration (s)")
    parser.add_argument("--quick", action="store_true", help="Run quick test")

    args = parser.parse_args()

    run_resonance_experiment(
        frequencies=args.frequencies,
        amplitude=args.amplitude,
        duration=args.duration,
        quick_test=args.quick
    )
