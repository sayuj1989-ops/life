import sys
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import run_protein_simulation
try:
    from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

def run_sweep():
    # Reproducibility
    seed = 42
    np.random.seed(seed)

    # Setup parameters
    natural_kyphosis_values = np.linspace(0.0, 10.0, 21)
    # Fixed parameters from previous successful instability
    active_curvature = 12.0 # Proven unstable at anisotropy=5.0
    anisotropy = 5.0
    initial_lateral_defect = 0.05
    duration = 2.0
    n_elements = 50
    dt = 1e-4

    results = []

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(f"outputs/sim/{date_str}")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Natural Kyphosis Sweep (N={len(natural_kyphosis_values)})...")
    print(f"Active Curvature: {active_curvature}, Anisotropy: {anisotropy}, Defect: {initial_lateral_defect}")

    for i, kyphosis in enumerate(natural_kyphosis_values):
        print(f"[{i+1}/{len(natural_kyphosis_values)}] Simulating Natural Kyphosis = {kyphosis:.2f}...")

        sim_result = run_protein_simulation(
            anisotropy=float(anisotropy),
            active_curvature=active_curvature,
            initial_lateral_defect=initial_lateral_defect,
            natural_kyphosis=float(kyphosis),
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
            "natural_kyphosis": kyphosis,
            "active_curvature": active_curvature,
            "anisotropy": anisotropy,
            "initial_lateral_defect": initial_lateral_defect,
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
        "natural_kyphosis_min": natural_kyphosis_values[0],
        "natural_kyphosis_max": natural_kyphosis_values[-1],
        "steps": len(natural_kyphosis_values),
        "active_curvature": active_curvature,
        "anisotropy": anisotropy,
        "initial_lateral_defect": initial_lateral_defect,
        "duration": duration,
        "dt": dt,
        "n_elements": n_elements,
        "seed": seed
    }])
    params_df.to_csv(params_path, index=False)
    print(f"Saved params to {params_path}")

    # Generate Plots
    generate_plots(df, out_dir, active_curvature, anisotropy)

def generate_plots(df, out_dir, active_curv, anisotropy):
    # Plot 1: Natural Kyphosis vs Cobb Angle
    plt.figure(figsize=(10, 6))
    plt.plot(df['natural_kyphosis'], df['cobb_angle'], 'o-', linewidth=2, color='blue')
    plt.xlabel('Natural Kyphosis (1/m)')
    plt.ylabel('Cobb Angle (degrees)')
    plt.title(f'Effect of Natural Kyphosis on Cobb Angle\n(Active Curvature = {active_curv}, Anisotropy = {anisotropy})')
    plt.grid(True, alpha=0.3)

    plot_path = out_dir / "plot_kyphosis_cobb.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path}")

    # Plot 2: Natural Kyphosis vs Lateral Deviation (S_lat)
    plt.figure(figsize=(10, 6))
    plt.plot(df['natural_kyphosis'], df['s_lat'], 's--', linewidth=2, color='red')
    plt.xlabel('Natural Kyphosis (1/m)')
    plt.ylabel('Lateral Deviation S_lat (m)')
    plt.title(f'Effect of Natural Kyphosis on Lateral Deviation\n(Active Curvature = {active_curv}, Anisotropy = {anisotropy})')
    plt.grid(True, alpha=0.3)

    plot_path2 = out_dir / "plot_kyphosis_slat.png"
    plt.savefig(plot_path2, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path2}")

    # Plot 3: Natural Kyphosis vs Max Curvature
    plt.figure(figsize=(10, 6))
    plt.plot(df['natural_kyphosis'], df['max_curvature'], '^-', linewidth=2, color='green')
    plt.xlabel('Natural Kyphosis (1/m)')
    plt.ylabel('Max Curvature (1/m)')
    plt.title(f'Effect of Natural Kyphosis on Max Curvature\n(Active Curvature = {active_curv}, Anisotropy = {anisotropy})')
    plt.grid(True, alpha=0.3)

    plot_path3 = out_dir / "plot_kyphosis_maxcurv.png"
    plt.savefig(plot_path3, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path3}")

if __name__ == "__main__":
    run_sweep()
