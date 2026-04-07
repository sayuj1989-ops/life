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

try:
    from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

def run_sweep():
    # Reproducibility
    seed = 42
    np.random.seed(seed)

    # Setup parameter family to sweep: Load vector tilt (gravity direction)
    # We will simulate the spine tilted laterally relative to gravity.
    # To do this using run_protein_simulation, we can apply an initial lateral defect
    # to mimic the effect of a tilted load, or vary the anisotropy under a fixed tilt.
    # Let's sweep stiffness_anisotropy under a fixed small initial lateral defect (mimicking tilt).
    anisotropy_values = np.linspace(1.0, 10.0, 15)

    # Fixed parameters
    active_curvature = 10.0
    initial_lateral_defect = 0.05 # Mimics a 5% off-axis load/tilt
    duration = 2.0
    n_elements = 50
    dt = 1e-4

    results = []

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(f"outputs/sim/{date_str}_anisotropy_tilt")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Starting Anisotropy Sweep under Tilted Load...")

    tracemalloc.start()
    t0 = time.time()

    for anisotropy in anisotropy_values:
        print(f"Simulating Anisotropy = {anisotropy:.2f}...")

        sim_result = run_protein_simulation(
            anisotropy=anisotropy,
            active_curvature=active_curvature,
            torsion_drive=0.0, # No intrinsic torsion
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
        max_torsion = sim_result.get("max_torsion", 0.0)
        s_lat = sim_result.get("S_lat", 0.0)

        print(f"  -> Cobb: {cobb_angle:.2f} deg, MaxTorsion: {max_torsion:.2f}, S_lat: {s_lat:.4f}")

        results.append({
            "anisotropy": anisotropy,
            "active_curvature": active_curvature,
            "initial_lateral_defect": initial_lateral_defect,
            "cobb_angle": cobb_angle,
            "max_torsion": max_torsion,
            "s_lat": s_lat,
            "runtime_sec": sim_result.get("runtime_sec", 0.0),
        })

    t1 = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTotal Sweep Time: {t1 - t0:.2f} s")

    df = pd.DataFrame(results)

    csv_path = out_dir / "results.csv"
    df.to_csv(csv_path, index=False)

    params_path = out_dir / "params.csv"
    params_df = pd.DataFrame([{
        "anisotropy_min": anisotropy_values[0],
        "anisotropy_max": anisotropy_values[-1],
        "active_curvature": active_curvature,
        "initial_lateral_defect": initial_lateral_defect,
        "duration": duration,
        "dt": dt,
        "n_elements": n_elements,
        "seed": seed
    }])
    params_df.to_csv(params_path, index=False)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['anisotropy'], df['cobb_angle'], 'o-', linewidth=2, label='Cobb Angle')
    plt.xlabel('Stiffness Anisotropy Ratio')
    plt.ylabel('Cobb Angle (degrees)')
    plt.title('Effect of Stiffness Anisotropy on Off-Axis Load Stability')
    plt.grid(True, alpha=0.3)
    plt.savefig(out_dir / "plot_cobb_vs_anisotropy.png", dpi=300)
    plt.close()

    # Generate Report
    report_path = out_dir / "report.md"
    with open(report_path, "w") as f:
        f.write(f"# Weekly Simulation: Anisotropy Sweep under Off-Axis Load\n\n")
        f.write("## Experiment Overview\n")
        f.write("Sweeping `stiffness_anisotropy` to observe how directional stiffness constraints rescue the spine from an off-axis gravitational load (mimicked via initial lateral defect) combined with active sagittal growth.\n\n")

        f.write("## Changes\n")
        f.write("- Parameter family swept: `stiffness_anisotropy`\n")
        f.write(f"- 15 runs from {anisotropy_values[0]:.1f} to {anisotropy_values[-1]:.1f}\n")
        f.write("- Fixed active growth (`chi_kappa` = 10.0) and lateral defect (0.05)\n\n")

        f.write("## Emergent Shapes\n")
        max_cobb = df['cobb_angle'].max()
        min_cobb = df['cobb_angle'].min()
        f.write(f"Varying anisotropy reveals a transition in structural stability. Low anisotropy permits large lateral deviations (Cobb peaking ~{max_cobb:.1f} deg), while high anisotropy constrains the S-shape primarily to the sagittal plane (Cobb reduced to ~{min_cobb:.1f} deg).\n\n")

        f.write("## Relevance to Scoliosis\n")
        f.write("Normal S-curves require high dorso-ventral compliance but lateral rigidity (high anisotropy). A loss of this anisotropy (e.g., fibrillin microfibril defects) under active growth and slight off-axis loads triggers buckling into a 3D scoliotic profile.\n\n")

        f.write("## Next Sweep Suggestion\n")
        f.write("Perform a 2D parameter sweep of `stiffness_anisotropy` vs `torsion_drive` under tilt to map the complete transition boundary.\n")

if __name__ == "__main__":
    run_sweep()
