import os
import sys

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import run_protein_simulation
try:
    from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation
    from plot_style import apply_nature_style
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

def run_sweep():
    # Reproducibility
    seed = 42
    np.random.seed(seed)

    # Setup parameters
    active_curvature_values = np.linspace(0.0, 20.0, 21)
    anisotropy = 5.0
    initial_lateral_defect = 0.05
    natural_kyphosis = 2.0
    duration = 2.0
    n_elements = 50
    dt = 1e-4

    results = []

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(f"outputs/sim/{date_str}")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Active Curvature Sweep (N={len(active_curvature_values)})...")
    print(f"Anisotropy: {anisotropy}, Defect: {initial_lateral_defect}, Kyphosis: {natural_kyphosis}")

    for i, active_curv in enumerate(active_curvature_values):
        print(f"[{i+1}/{len(active_curvature_values)}] Simulating Active Curvature = {active_curv:.2f}...")

        sim_result = run_protein_simulation(
            anisotropy=float(anisotropy),
            active_curvature=float(active_curv),
            initial_lateral_defect=initial_lateral_defect,
            natural_kyphosis=natural_kyphosis,
            duration=duration,
            dt=dt,
            n_elements=n_elements,
            show_progress=False
        )

        if not sim_result.get("success", False):
            print(f"  FAILED: {sim_result.get('error', 'Unknown Error')}")
            continue

        # Extract metrics
        cobb_angle = sim_result.get("cobb_angle", 0.0)
        max_curvature = sim_result.get("max_curvature", 0.0)
        s_lat = sim_result.get("S_lat", 0.0)
        u_cc = sim_result.get("U_CC", 0.0)
        max_torsion = sim_result.get("max_torsion", 0.0)

        print(f"  -> Cobb: {cobb_angle:.2f} deg, MaxCurv: {max_curvature:.2f}, S_lat: {s_lat:.4f}")

        results.append({
            "active_curvature": active_curv,
            "anisotropy": anisotropy,
            "initial_lateral_defect": initial_lateral_defect,
            "natural_kyphosis": natural_kyphosis,
            "cobb_angle": cobb_angle,
            "max_curvature": max_curvature,
            "s_lat": s_lat,
            "max_torsion": max_torsion,
            "u_cc": u_cc,
            "runtime_sec": sim_result.get("runtime_sec", 0.0)
        })

    # Save Results
    df = pd.DataFrame(results)
    csv_path = out_dir / "results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved results to {csv_path}")

    # Save Params (for reproducibility)
    params_path = out_dir / "params.csv"
    params_df = pd.DataFrame([{
        "active_curvature_min": active_curvature_values[0],
        "active_curvature_max": active_curvature_values[-1],
        "steps": len(active_curvature_values),
        "anisotropy": anisotropy,
        "initial_lateral_defect": initial_lateral_defect,
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
    apply_nature_style()
    # Plot 1: Active Curvature vs Cobb Angle
    plt.figure(figsize=(10, 6))
    plt.plot(df['active_curvature'], df['cobb_angle'], 'o-', linewidth=2, color='blue')
    plt.xlabel('Active Curvature (Growth Drive)')
    plt.ylabel('Cobb Angle (degrees)')
    plt.title('Effect of Active Curvature on Cobb Angle\n(Anisotropy = 5.0)')
    plt.grid(True, alpha=0.3)

    plot_path = out_dir / "plot_curvature_cobb.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path}")

    # Plot 2: Active Curvature vs Lateral Deviation (S_lat)
    plt.figure(figsize=(10, 6))
    plt.plot(df['active_curvature'], df['s_lat'], 's--', linewidth=2, color='red')
    plt.xlabel('Active Curvature (Growth Drive)')
    plt.ylabel('Lateral Deviation S_lat (m)')
    plt.title('Effect of Active Curvature on Lateral Deviation\n(Anisotropy = 5.0)')
    plt.grid(True, alpha=0.3)

    plot_path2 = out_dir / "plot_curvature_slat.png"
    plt.savefig(plot_path2, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path2}")

    # Plot 3: Active Curvature vs Max Curvature
    plt.figure(figsize=(10, 6))
    plt.plot(df['active_curvature'], df['max_curvature'], '^-', linewidth=2, color='green')
    plt.xlabel('Active Curvature (Growth Drive)')
    plt.ylabel('Max Curvature (1/m)')
    plt.title('Effect of Active Curvature on Max Curvature\n(Anisotropy = 5.0)')
    plt.grid(True, alpha=0.3)

    plot_path3 = out_dir / "plot_curvature_maxcurv.png"
    plt.savefig(plot_path3, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path3}")

if __name__ == "__main__":
    run_sweep()
