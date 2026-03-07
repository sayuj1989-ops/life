#!/usr/bin/env python3
"""
Weekly Simulation: Torsion Drive Sweep under Moderate Growth/Anisotropy.

Tests how the torsional coupling parameter (torsion_drive) impacts spinal
metrics (Cobb angle, Lateral deviation) under a baseline of moderate active
sagittal growth (active_curvature=10.0) and moderate lateral stiffness
protection (anisotropy=2.0).

Hypothesis: Symmetry-breaking torsion triggers scoliotic deformation only when
a baseline energy deficit (growth) exists, but intermediate anisotropy might
modulate the response.
"""

import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation


def run_sweep():
    # Reproducibility
    np.random.seed(42)

    # Fixed Parameters
    active_curvature = 10.0  # Moderate growth
    anisotropy = 2.0         # Moderate lateral stiffness protection
    initial_lateral_defect = 0.01 # Tiny imperfection
    natural_kyphosis = 2.0
    duration = 3.0           # 3 seconds to let instabilities manifest
    n_elements = 50
    length = 1.0

    # Sweep range: torsion_drive
    # From 0.0 (perfect planar) to 2.0 (strong torsion)
    torsion_values = np.linspace(0.0, 2.0, 15)

    results = []

    # Create output directory
    today = time.strftime("%Y-%m-%d")
    output_dir = Path(f"outputs/sim/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Torsion Drive Sweep: {len(torsion_values)} runs")
    print(f"Fixed Params: Active={active_curvature}, Anisotropy={anisotropy}, Seed=42")

    for torsion in torsion_values:
        print(f"  Running torsion_drive={torsion:.4f}...", end="", flush=True)

        try:
            res = run_protein_simulation(
                anisotropy=anisotropy,
                active_curvature=active_curvature,
                torsion_drive=torsion,
                initial_lateral_defect=initial_lateral_defect,
                natural_kyphosis=natural_kyphosis,
                length=length,
                n_elements=n_elements,
                duration=duration,
                show_progress=False
            )

            if res.get("success"):
                results.append({
                    "torsion_drive": torsion,
                    "cobb_angle": res.get("cobb_angle", 0.0),
                    "max_curvature": res.get("max_curvature", 0.0),
                    "S_lat": res.get("S_lat", 0.0),
                    "z_tip": res.get("z_tip", 0.0),
                    "U_CC": res.get("U_CC", 0.0),
                    "runtime": res.get("runtime_sec", 0.0)
                })
                print(f" Done. Cobb={res.get('cobb_angle', 0.0):.2f} S_lat={res.get('S_lat', 0.0):.4f}")
            else:
                print(f" Failed: {res.get('error')}")

        except Exception as e:
            print(f" Error: {e}")

    # Save results
    df = pd.DataFrame(results)
    csv_path = output_dir / "results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Generate Plots
    generate_plots(df, output_dir)

    # Save parameters
    params_df = pd.DataFrame([{
        "active_curvature": active_curvature,
        "anisotropy": anisotropy,
        "initial_lateral_defect": initial_lateral_defect,
        "natural_kyphosis": natural_kyphosis,
        "duration": duration,
        "n_elements": n_elements,
        "length": length,
        "seed": 42
    }])
    params_df.to_csv(output_dir / "params.csv", index=False)
    print(f"Saved parameters to {output_dir / 'params.csv'}")


def generate_plots(df, output_dir):
    # Plot 1: Torsion vs Cobb Angle
    plt.figure(figsize=(10, 6))
    plt.plot(df["torsion_drive"], df["cobb_angle"], 'o-', linewidth=2, label="Cobb Angle")
    plt.xlabel("Torsion Drive")
    plt.ylabel("Cobb Angle (degrees)")
    plt.title("Torsion Sensitivity: Cobb Angle vs Torsion Drive\n(Active Curvature=10.0, Anisotropy=2.0)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(output_dir / "plot_torsion_cobb.png", dpi=150)
    plt.close()

    # Plot 2: Torsion vs Lateral Deviation (S_lat)
    plt.figure(figsize=(10, 6))
    plt.plot(df["torsion_drive"], df["S_lat"], 's-', color='orange', linewidth=2, label="Lateral Deviation")
    plt.xlabel("Torsion Drive")
    plt.ylabel("Lateral Deviation S_lat (m)")
    plt.title("Torsion Sensitivity: Lateral Deviation vs Torsion Drive\n(Active Curvature=10.0, Anisotropy=2.0)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(output_dir / "plot_torsion_slat.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    run_sweep()
