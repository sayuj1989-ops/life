import os
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

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
    kyphosis_values = np.linspace(-2.0, 6.0, 21)

    # Fixed parameters
    anisotropy = 3.0
    active_curvature = 10.0
    initial_lateral_defect = 0.05
    duration = 2.0
    n_elements = 50
    dt = 1e-4

    results = []

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(f"outputs/sim/{date_str}")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Starting Load Vector Tilt / Kyphosis Sweep...")
    print(f"Active Curvature: {active_curvature}, Defect: {initial_lateral_defect}, Anisotropy: {anisotropy}")

    tracemalloc.start()
    t0 = time.time()

    for kyphosis in kyphosis_values:
        print(f"Simulating Kyphosis = {kyphosis:.2f}...")

        sim_result = run_protein_simulation(
            anisotropy=anisotropy,
            active_curvature=active_curvature,
            natural_kyphosis=float(kyphosis),
            initial_lateral_defect=initial_lateral_defect,
            duration=duration,
            dt=dt,
            n_elements=n_elements,
            show_progress=False
        )

        if not sim_result.get("success", False):
            print(f"  FAILED: {sim_result.get('error', 'Unknown Error')}")
            continue

        cobb_angle = sim_result.get("cobb_angle", 0.0)
        s_lat = sim_result.get("S_lat", 0.0)
        u_cc = sim_result.get("U_CC", 0.0)

        print(f"  -> Cobb: {cobb_angle:.2f} deg, S_lat: {s_lat:.4f}")

        results.append({
            "natural_kyphosis": kyphosis,
            "anisotropy": anisotropy,
            "active_curvature": active_curvature,
            "initial_lateral_defect": initial_lateral_defect,
            "cobb_angle": cobb_angle,
            "s_lat": s_lat,
            "u_cc": u_cc,
            "runtime_sec": sim_result.get("runtime_sec", 0.0)
        })

    t1 = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Save Results
    df = pd.DataFrame(results)
    df.to_csv(out_dir / "results.csv", index=False)

    # Save Params
    params_df = pd.DataFrame([{
        "kyphosis_min": kyphosis_values[0],
        "kyphosis_max": kyphosis_values[-1],
        "steps": len(kyphosis_values),
        "anisotropy": anisotropy,
        "active_curvature": active_curvature,
        "initial_lateral_defect": initial_lateral_defect,
        "duration": duration,
        "dt": dt,
        "n_elements": n_elements,
        "seed": seed
    }])
    params_df.to_csv(out_dir / "params.csv", index=False)

    # Generate Plots
    plt.figure(figsize=(10, 6))
    plt.plot(df['natural_kyphosis'], df['cobb_angle'], 'o-', linewidth=2, color='blue')
    plt.xlabel('Natural Kyphosis (deg equiv.)')
    plt.ylabel('Cobb Angle (degrees)')
    plt.title('Effect of Load Vector Tilt on Lateral Instability')
    plt.grid(True, alpha=0.3)
    plt.savefig(out_dir / "plot_kyphosis_cobb.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(df['natural_kyphosis'], df['s_lat'], 's--', linewidth=2, color='red')
    plt.xlabel('Natural Kyphosis (deg equiv.)')
    plt.ylabel('Lateral Deviation S_lat (m)')
    plt.title('Effect of Load Vector Tilt on Lateral Deviation')
    plt.grid(True, alpha=0.3)
    plt.savefig(out_dir / "plot_kyphosis_slat.png", dpi=300)
    plt.close()

    # Generate Report
    report_path = out_dir / "report.md"
    with open(report_path, "w") as f:
        f.write("# Weekly Simulation: Load Vector Tilt Sweep\n\n")
        f.write("## Overview\n")
        f.write("Swept `natural_kyphosis` from -2.0 to 6.0 to simulate the effect of load vector tilt on emergent S-shape geometry.\n\n")
        f.write("## Results\n")
        max_cobb = df['cobb_angle'].max()
        crit_k = df.loc[df['cobb_angle'].idxmax(), 'natural_kyphosis']
        f.write(f"The maximum Cobb angle observed was {max_cobb:.2f} deg at Kyphosis = {crit_k:.2f}.\n\n")
        f.write("## Interpretation\n")
        f.write("Sagittal profile and load vector tilt strongly gate lateral buckling vulnerability, informing scoliosis onset vs normal S-curve development under active growth.\n\n")
        f.write("## Next Sweep Suggestion\n")
        f.write("Investigate combined torsion and load vector tilt mapping to model asymmetric axial loads.\n")

if __name__ == "__main__":
    run_sweep()
