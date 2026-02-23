#!/usr/bin/env python3
"""
Minimal reproducible experiment: Protein-Driven Countercurvature Physics.

This script maps protein-inspired parameters (ECM Stiffness Anisotropy, Piezo2 Active Curvature)
to emergent spinal geometry (Cobb Angle, Kyphosis, Torsion) using the PyElastica Cosserat rod solver.

It performs a parameter sweep and saves metrics to 'outputs/protein_physics/experiment_results.csv'.
"""

import sys
import os
import time
import pandas as pd
import numpy as np
from pathlib import Path

# Ensure src is in python path
current_dir = Path(__file__).resolve().parent
src_path = current_dir.parent / "src"
sys.path.append(str(src_path))

try:
    from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation, PYELASTICA_AVAILABLE
except ImportError as e:
    print(f"Error importing simulation bridge: {e}")
    print("Ensure you are running from the repo root or have installed the package.")
    sys.exit(1)

def main():
    if not PYELASTICA_AVAILABLE:
        print("ERROR: PyElastica is not installed but is required for this experiment.")
        print("To install, run:")
        print("    pip install pyelastica")
        print("Or visit: https://github.com/GazzolaLab/PyElastica")
        sys.exit(1)

    print(">>> Starting Protein Physics Experiment (PyElastica)")
    output_dir = Path("outputs/protein_physics")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / "experiment_results.csv"

    # --- Parameter Sweep Definition ---
    # 1. Anisotropy (A): Ratio of Lateral/Sagittal Stiffness.
    #    Biological proxy: Collagen fiber alignment (Vimentin/Col1a1 organization).
    #    Range: 1.0 (Isotropic/Disordered) to 4.0 (Highly Aligned).
    anisotropy_levels = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]

    # 2. Active Curvature (C): Magnitude of active bending drive.
    #    Biological proxy: Piezo2-mediated ion flux / Proprioceptive drive.
    #    Range: 0.0 (Passive) to 2.0 (Strong Active Drive).
    active_curvature_levels = [0.0, 0.5, 1.0, 1.5, 2.0]

    # Fixed Parameters
    torsion_drive = 0.0          # Assume no intrinsic twist for this baseline
    stiffness_modulation = 0.0   # Uniform stiffness for now
    initial_lateral_defect = 0.05 # Small perturbation to seed symmetry breaking (5% curvature)

    results = []

    total_runs = len(anisotropy_levels) * len(active_curvature_levels)
    count = 0

    start_time_global = time.time()

    print(f"Running {total_runs} simulations...")
    print(f"{'Anisotropy':<12} | {'ActiveCurv':<12} | {'Cobb (deg)':<12} | {'Energy (J)':<12} | {'Time (s)':<10}")
    print("-" * 70)

    for A in anisotropy_levels:
        for C in active_curvature_levels:
            count += 1

            # Run Simulation
            # using default duration=2.0s, dt=1e-4, n_elements=50
            sim_output = run_protein_simulation(
                anisotropy=A,
                active_curvature=C,
                torsion_drive=torsion_drive,
                stiffness_modulation=stiffness_modulation,
                initial_lateral_defect=initial_lateral_defect,
                show_progress=False  # Keep stdout clean
            )

            # Collect Metrics
            if sim_output.get("success"):
                cobb = sim_output.get("cobb_angle", 0.0)
                energy = sim_output.get("U_CC", 0.0)
                runtime = sim_output.get("runtime_sec", 0.0)

                print(f"{A:<12.1f} | {C:<12.1f} | {cobb:<12.2f} | {energy:<12.4f} | {runtime:<10.2f}")

                results.append({
                    "anisotropy": A,
                    "active_curvature": C,
                    "cobb_angle": cobb,
                    "max_curvature": sim_output.get("max_curvature"),
                    "U_CC": energy,
                    "U_elastic": sim_output.get("U_elastic"),
                    "U_info": sim_output.get("U_info"),
                    "runtime_sec": runtime,
                    "peak_memory_mb": sim_output.get("peak_memory_mb")
                })
            else:
                print(f"{A:<12.1f} | {C:<12.1f} | {'FAILED':<12} | {'N/A':<12} | {'N/A':<10}")
                results.append({
                    "anisotropy": A,
                    "active_curvature": C,
                    "error": sim_output.get("error")
                })

    # Save Results
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    end_time_global = time.time()
    total_time = end_time_global - start_time_global

    print("-" * 70)
    print(f"Experiment completed in {total_time:.2f} seconds.")
    print(f"Results saved to: {output_csv}")

if __name__ == "__main__":
    main()
