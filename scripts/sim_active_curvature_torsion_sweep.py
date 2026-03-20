import os
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import from spinalmodes
try:
    from spinalmodes.countercurvature.pyelastica_bridge import (
        PYELASTICA_AVAILABLE,
        run_protein_simulation,
    )
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

def run_sweep():
    if not PYELASTICA_AVAILABLE:
        print("PyElastica not available. Exiting.")
        sys.exit(1)

    # Reproducibility
    seed = 42
    np.random.seed(seed)

    # Setup parameters
    active_curvatures = np.linspace(0.0, 15.0, 16)
    anisotropy = 3.0 # Moderate anisotropy
    torsion_drive = 0.5 # Small symmetry breaking
    initial_lateral_defect = 0.0
    natural_kyphosis = 2.0
    duration = 2.0
    dt = 1e-4
    n_elements = 50

    results = []

    out_dir = Path("outputs/sim/2026-03-20_active_curvature_torsion")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Active Curvature Sweep w/ Torsion (N={len(active_curvatures)})...")
    print(f"Active Curvature Range: [{active_curvatures[0]:.1f}, {active_curvatures[-1]:.1f}]")
    print(f"Anisotropy: {anisotropy}, Torsion Drive: {torsion_drive}")

    for i, ac in enumerate(active_curvatures):
        print(f"[{i+1}/{len(active_curvatures)}] Simulating Active Curvature = {ac:.1f}...")

        tracemalloc.start()
        t0 = time.time()

        try:
            # 4. Run Simulation via the bridge API
            sim_result = run_protein_simulation(
                anisotropy=anisotropy,
                active_curvature=ac,
                torsion_drive=torsion_drive,
                initial_lateral_defect=initial_lateral_defect,
                natural_kyphosis=natural_kyphosis,
                duration=duration,
                dt=dt,
                n_elements=n_elements,
                show_progress=False
            )

            success = sim_result.get("success", False)
            error_msg = sim_result.get("error", "")

        except Exception as e:
            success = False
            error_msg = str(e)
            sim_result = {}
            print(f"  FAILED: {error_msg}")

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        t1 = time.time()

        if success:
            cobb_angle = sim_result.get("cobb_angle", 0.0)
            max_curvature = sim_result.get("max_curvature", 0.0)
            s_lat = sim_result.get("S_lat", 0.0)
            u_cc = sim_result.get("U_CC", 0.0)
            z_tip = sim_result.get("z_tip", 0.0)
            end_to_end = sim_result.get("end_to_end_distance", 0.0)

            print(f"  -> Cobb: {cobb_angle:.2f} deg, MaxCurv: {max_curvature:.2f}, S_lat: {s_lat:.4f}, Z_tip: {z_tip:.4f}")

            results.append({
                "active_curvature": ac,
                "anisotropy": anisotropy,
                "torsion_drive": torsion_drive,
                "cobb_angle": cobb_angle,
                "max_curvature": max_curvature,
                "s_lat": s_lat,
                "z_tip": z_tip,
                "end_to_end": end_to_end,
                "u_cc": u_cc,
                "runtime_sec": t1 - t0,
                "peak_memory_mb": peak / (1024 * 1024),
                "success": success,
                "error": error_msg
            })
        else:
             results.append({
                "active_curvature": ac,
                "anisotropy": anisotropy,
                "torsion_drive": torsion_drive,
                "cobb_angle": np.nan,
                "max_curvature": np.nan,
                "s_lat": np.nan,
                "z_tip": np.nan,
                "end_to_end": np.nan,
                "u_cc": np.nan,
                "runtime_sec": t1 - t0,
                "peak_memory_mb": peak / (1024 * 1024),
                "success": success,
                "error": error_msg
            })


    # Save Results
    df = pd.DataFrame(results)
    csv_path = out_dir / "results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Save Params (for reproducibility)
    params_path = out_dir / "params.csv"
    params_df = pd.DataFrame([{
        "active_curvature_min": active_curvatures[0],
        "active_curvature_max": active_curvatures[-1],
        "steps": len(active_curvatures),
        "anisotropy": anisotropy,
        "torsion_drive": torsion_drive,
        "natural_kyphosis": natural_kyphosis,
        "duration": duration,
        "dt": dt,
        "n_elements": n_elements,
        "seed": seed
    }])
    params_df.to_csv(params_path, index=False)
    print(f"Saved params to {params_path}")

    # Generate Plots
    generate_plots(df, out_dir)

def generate_plots(df, out_dir):
    df_valid = df.dropna(subset=['cobb_angle'])

    if df_valid.empty:
        print("No valid results to plot.")
        return

    # Plot 1: Active Curvature vs Cobb Angle
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df_valid['active_curvature'], df_valid['cobb_angle'], 'o-', linewidth=2, color='tab:blue')
    ax1.set_xlabel('Active Curvature (1/m)')
    ax1.set_ylabel('Cobb Angle (degrees)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.plot(df_valid['active_curvature'], df_valid['s_lat'], 's--', linewidth=2, color='tab:red')
    ax2.set_ylabel('Lateral Deviation S_lat (m)', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title('Effect of Active Curvature on Lateral Instability w/ Torsion\n(Anisotropy=3.0, Torsion Drive=0.5)')
    ax1.grid(True, alpha=0.3)

    plot_path = out_dir / "plot_active_curvature_torsion_cobb.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path}")

    # Plot 2: Active Curvature vs Sagittal Metrics
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df_valid['active_curvature'], df_valid['max_curvature'], 'o-', linewidth=2, color='tab:green')
    ax1.set_xlabel('Active Curvature (1/m)')
    ax1.set_ylabel('Max Curvature (1/m)', color='tab:green')
    ax1.tick_params(axis='y', labelcolor='tab:green')

    ax2 = ax1.twinx()
    ax2.plot(df_valid['active_curvature'], df_valid['z_tip'], 'd--', linewidth=2, color='tab:purple')
    ax2.set_ylabel('Tip Z Position (m)', color='tab:purple')
    ax2.tick_params(axis='y', labelcolor='tab:purple')

    plt.title('Sagittal Metrics vs Active Curvature\n(Anisotropy=3.0, Torsion Drive=0.5)')
    ax1.grid(True, alpha=0.3)

    plot_path2 = out_dir / "plot_active_curvature_torsion_sagittal.png"
    plt.savefig(plot_path2, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path2}")

if __name__ == "__main__":
    run_sweep()
