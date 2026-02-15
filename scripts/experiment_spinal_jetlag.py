"""
Experiment: Spinal Jetlag — Circadian Desynchronization.

This script implements Phase 2, Weeks 5-7 of the Gravity Optimization research schedule.
It models time-varying information-curvature coupling modulated by a circadian clock
and simulates desynchronization ("jetlag") effects on spinal alignment.

Experimental Conditions:
1. Entrained (phi=0): Clock and gravity in phase.
2. Free-running: Clock drifts relative to gravity (period mismatch).
3. Jetlagged (phi=pi): Anti-phase, destructive interference.
4. Microgravity: Gravity amplitude removed.

Coupling Model:
    chi_kappa(t) = chi_0 * (1 + A * cos(omega * t + phi))
    g(t) = g_0 * 0.5 * (1 + cos(omega_g * t))  [Simulates daily activity cycle]

Hypothesis:
    Spinal alignment relies on synchronization between the internal clock (sensitivity)
    and external loading (gravity). Desynchronization (Jetlag) or loss of signal (Microgravity)
    leads to optimization failure (Scoliosis).
"""

import argparse
import csv
import os
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np

# Ensure src is in python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.countercurvature.coupling import CounterCurvatureParams
from spinalmodes.countercurvature.info_fields import InfoField1D
from spinalmodes.countercurvature.pyelastica_bridge import (
    CounterCurvatureRodSystem,
    compute_U_CC,
    verify_pyelastica_installation,
    CircadianParams,
    SimulationResult,
)
from spinalmodes.countercurvature.scoliosis_metrics import compute_scoliosis_metrics


def create_info_field(length: float, n_elements: int) -> InfoField1D:
    s = np.linspace(0, length, n_elements + 1)
    # Gaussian bump
    info_center = 0.5 * length
    info_width = 0.1 * length
    I = 0.5 + 0.5 * np.exp(-0.5 * ((s - info_center) / info_width) ** 2)
    dIds = np.gradient(I, s)
    return InfoField1D(s=s, I=I, dIds=dIds)


def analyze_cycles(result: SimulationResult, period: float) -> List[Dict[str, float]]:
    """Compute metrics for each cycle in the simulation."""
    cycle_metrics = []

    # Identify cycle boundaries
    times = result.time
    if len(times) == 0:
        return []

    max_time = times[-1]
    # Use round to handle floating point noise near the boundary
    n_cycles = int(np.round(max_time / period))

    # If round down to 0 but we have data, try to extract at least one cycle if reasonable
    if n_cycles == 0 and max_time > 0.8 * period:
        n_cycles = 1

    for i in range(n_cycles):
        t_start = i * period
        t_end = (i + 1) * period

        # Filter indices
        indices = np.where((times >= t_start) & (times < t_end))[0]
        if len(indices) == 0:
            continue

        # Get data for this cycle
        cycle_kappas = result.kappa[indices]  # (n_steps, n_nodes, 3)
        cycle_centerlines = result.centerline[indices] # (n_steps, 3, n_nodes)

        # Compute Cobb angle history for this cycle
        cobbs = []
        for j in range(len(indices)):
            pos = cycle_centerlines[j].T # (n_nodes, 3)

            if np.any(np.isnan(pos)):
                # print(f"WARNING: NaNs detected in cycle {i+1}, step {j}")
                continue

            # Z is longitudinal (2), X is Lateral (0)
            try:
                met = compute_scoliosis_metrics(pos[:, 2], pos[:, 0])
                cobbs.append(met.cobb_like_deg)
            except np.linalg.LinAlgError:
                # print(f"WARNING: SVD failed in Cobb calc, cycle {i+1}, step {j}")
                continue
            except Exception as e:
                # print(f"WARNING: Error in Cobb calc: {e}")
                continue

        if not cobbs:
            continue

        # Metrics
        mean_cobb = np.mean(cobbs)
        max_cobb = np.max(cobbs)
        std_cobb = np.std(cobbs)

        cycle_metrics.append({
            "cycle": i + 1,
            "mean_cobb": float(mean_cobb),
            "max_cobb": float(max_cobb),
            "std_cobb": float(std_cobb),
        })

    return cycle_metrics


def run_jetlag_experiment(
    out_file: str,
    n_cycles: int = 3,
    period: float = 5.0,
    quick_test: bool = False,
):
    verify_pyelastica_installation(exit_on_fail=True)

    print("=" * 100)
    print("EXPERIMENT: Spinal Jetlag — Circadian Desynchronization")
    print("=" * 100)

    # Rod Parameters
    length = 0.5
    radius = 0.01
    E0 = 1e6
    rho = 1000.0
    gravity_base = 9.81
    n_elements = 20 if quick_test else 50
    dt = 5e-5

    # Simulation Settings
    final_time = n_cycles * period
    save_every = 1000 if quick_test else 2000

    # Base Parameters
    chi_0 = 5.0  # Base coupling strength
    amplitude = 0.5  # 50% modulation
    anisotropy = 2.0

    # Conditions
    conditions = [
        {
            "name": "Entrained",
            "circadian_period": period,
            "gravity_period": period,
            "circadian_phase": 0.0,
            "gravity_dynamic": True,
            "gravity_amp": gravity_base,
            "description": "Clock and Gravity in phase (phi=0)"
        },
        {
            "name": "Jetlagged",
            "circadian_period": period,
            "gravity_period": period,
            "circadian_phase": np.pi,
            "gravity_dynamic": True,
            "gravity_amp": gravity_base,
            "description": "Clock and Gravity anti-phase (phi=pi)"
        },
        {
            "name": "Free-running",
            "circadian_period": period * 1.1, # 10% mismatch (Drift)
            "gravity_period": period,         # External gravity is 24h
            "circadian_phase": 0.0,
            "gravity_dynamic": True,
            "gravity_amp": gravity_base,
            "description": "Clock period mismatched (Drift)"
        },
        {
            "name": "Microgravity",
            "circadian_period": period,
            "gravity_period": period,
            "circadian_phase": 0.0,
            "gravity_dynamic": False,
            "gravity_amp": 0.001, # Microgravity
            "description": "Gravity signal removed"
        }
    ]

    if quick_test:
        conditions = [conditions[0], conditions[1]] # Just Entrained and Jetlagged
        n_cycles = 1
        final_time = period

    # Prepare CSV
    out_dir = os.path.dirname(out_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    fieldnames = [
        "timestamp", "condition", "cycle",
        "mean_cobb", "max_cobb", "std_cobb",
        "final_U_CC", "final_info_gain_ratio",
        "runtime_sec", "peak_memory_mb"
    ]

    with open(out_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        print(f"{'Condition':<15} | {'Cycle':<5} | {'Mean Cobb':<10} | {'Max Cobb':<10} | {'U_CC':<10}")
        print("-" * 80)

        info = create_info_field(length, n_elements)

        for cond in conditions:
            tracemalloc.start()
            t0 = time.time()

            # Setup Params
            circadian = CircadianParams(
                chi_0=chi_0,
                amplitude=amplitude,
                period=cond["circadian_period"],
                phase=cond["circadian_phase"]
            )

            params = CounterCurvatureParams(
                chi_kappa=chi_0, # Initial value, modulated later
                chi_tau=0.0,
                chi_E=0.0,
                scale_length=length
            )

            # Base Geometric Curvature (Kyphosis + Slight Lateral Defect to break symmetry)
            kappa_gen = np.zeros((3, n_elements + 1))
            kappa_gen[1, :] = 2.0 # Kyphosis
            kappa_gen[0, :] = 0.2 # Increased lateral defect to ensure measurable Cobb in stable cases

            # Create System
            rod_system = CounterCurvatureRodSystem.from_iec(
                info=info,
                params=params,
                length=length,
                n_elements=n_elements,
                E0=E0,
                rho=rho,
                radius=radius,
                kappa_gen=kappa_gen,
                gravity=cond["gravity_amp"],
                stiffness_anisotropy=anisotropy
            )

            # Run
            result = rod_system.run_simulation(
                final_time=final_time,
                dt=dt,
                save_every=save_every,
                gravity=cond["gravity_amp"],
                boundary_condition="fixed",
                circadian_params=circadian,
                gravity_dynamic=cond["gravity_dynamic"],
                gravity_period=cond["gravity_period"],
                progress_bar=False
            )

            t1 = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Analyze
            cycle_stats = analyze_cycles(result, period)

            # Final Cost
            cost = compute_U_CC(result, info, params, gravity=cond["gravity_amp"], rho=rho, E0=E0)

            if not cycle_stats:
                # Handle instability case where analyze_cycles returned empty due to NaNs
                row = {
                    "timestamp": datetime.now().isoformat(),
                    "condition": cond["name"],
                    "cycle": 1,
                    "mean_cobb": float("nan"),
                    "max_cobb": float("nan"),
                    "std_cobb": float("nan"),
                    "final_U_CC": cost["U_CC"],
                    "final_info_gain_ratio": cost["info_gain_ratio"],
                    "runtime_sec": round(t1 - t0, 4),
                    "peak_memory_mb": round(peak / (1024 * 1024), 2),
                }
                writer.writerow(row)
                csvfile.flush()
                print(f"{row['condition']:<15} | {'FAIL':<5} | {'Instability detected':<20}")

            for stat in cycle_stats:
                row = {
                    "timestamp": datetime.now().isoformat(),
                    "condition": cond["name"],
                    "cycle": stat["cycle"],
                    "mean_cobb": stat["mean_cobb"],
                    "max_cobb": stat["max_cobb"],
                    "std_cobb": stat["std_cobb"],
                    "final_U_CC": cost["U_CC"],
                    "final_info_gain_ratio": cost["info_gain_ratio"],
                    "runtime_sec": round(t1 - t0, 4),
                    "peak_memory_mb": round(peak / (1024 * 1024), 2),
                }
                writer.writerow(row)
                csvfile.flush()

                print(
                    f"{row['condition']:<15} | {row['cycle']:<5} | "
                    f"{row['mean_cobb']:<10.2f} | {row['max_cobb']:<10.2f} | "
                    f"{row['final_U_CC']:<10.2f}"
                )

    print("=" * 100)
    generate_report(out_file)


def generate_report(csv_file: str):
    """Generate Markdown report."""
    md_file = str(Path(csv_file).with_suffix(".md"))

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return

    with open(md_file, "w") as f:
        f.write("# Spinal Jetlag Experiment Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Hypothesis\n")
        f.write("Spinal alignment requires synchronization between circadian-modulated sensitivity "
                "(chi_kappa) and external gravity loading. Desynchronization (Jetlag) or signal loss "
                "(Microgravity) leads to instability.\n\n")

        f.write("## Summary of Results\n\n")
        f.write("| Condition | Cycle | Mean Cobb (deg) | Max Cobb (deg) | U_CC (J) |\n")
        f.write("|-----------|-------|-----------------|----------------|----------|\n")

        for r in rows:
            mean_c = float(r['mean_cobb']) if r['mean_cobb'] and r['mean_cobb'] != 'nan' else None
            max_c = float(r['max_cobb']) if r['max_cobb'] and r['max_cobb'] != 'nan' else None
            ucc = float(r['final_U_CC'])

            mean_str = f"{mean_c:.2f}" if mean_c is not None else "INSTABILITY"
            max_str = f"{max_c:.2f}" if max_c is not None else "INSTABILITY"

            f.write(f"| {r['condition']} | {r['cycle']} | {mean_str} | "
                    f"{max_str} | {ucc:.4f} |\n")

        f.write("\n## Analysis\n\n")

        # Analyze Jetlag vs Entrained
        entrained = [r for r in rows if r['condition'] == "Entrained"]
        jetlagged = [r for r in rows if r['condition'] == "Jetlagged"]

        def get_max_cobb(rows_list):
            valid_cobbs = [float(r['max_cobb']) for r in rows_list if r['max_cobb'] and r['max_cobb'] != 'nan']
            if not valid_cobbs:
                return float('inf') # Instability is worse than any Cobb
            return max(valid_cobbs)

        if entrained and jetlagged:
            e_max = get_max_cobb(entrained)
            j_max = get_max_cobb(jetlagged)

            e_str = f"{e_max:.2f}°" if e_max != float('inf') else "Unstable"
            j_str = f"{j_max:.2f}°" if j_max != float('inf') else "Unstable"

            f.write(f"- **Entrained Max Cobb:** {e_str}\n")
            f.write(f"- **Jetlagged Max Cobb:** {j_str}\n")

            if j_max > e_max:
                f.write("**Result:** Jetlagged condition shows higher spinal deformity (or instability), supporting the hypothesis.\n")
            else:
                f.write("**Result:** No significant deformity increase in Jetlagged condition.\n")

    print(f"Report generated: {md_file}")


def parse_args():
    parser = argparse.ArgumentParser(description="Spinal Jetlag Experiment")
    parser.add_argument("--out-file", type=str, default="outputs/spinal_jetlag/results.csv")
    parser.add_argument("--cycles", type=int, default=3)
    parser.add_argument("--period", type=float, default=5.0)
    parser.add_argument("--quick-test", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_jetlag_experiment(
        out_file=args.out_file,
        n_cycles=args.cycles,
        period=args.period,
        quick_test=args.quick_test
    )
