import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

def run_sweep():
    # Setup parameters
    seed = 42
    np.random.seed(seed)
    anisotropy_values = np.linspace(1.0, 5.0, 17) # 17 points for 0.25 steps
    results = []

    date_str = "2026-04-02"
    out_dir = Path(f"outputs/sim/{date_str}")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Stiffness Anisotropy Sweep (N={len(anisotropy_values)})...")

    active_curvature = 12.0
    torsion_drive = 0.5

    for i, a in enumerate(anisotropy_values):
        print(f"[{i+1}/{len(anisotropy_values)}] Simulating Anisotropy = {a:.2f}...")
        res = run_protein_simulation(
            anisotropy=float(a),
            active_curvature=active_curvature,
            torsion_drive=torsion_drive,
            initial_lateral_defect=0.05,
            duration=2.0,
            n_elements=50,
            dt=1e-4,
            show_progress=False
        )
        if res.get("success"):
            cobb = res.get("cobb_angle", 0.0)
            s_lat = res.get("S_lat", 0.0)
            print(f"  -> Cobb: {cobb:.2f} deg, S_lat: {s_lat:.4f}")
            results.append({
                "stiffness_anisotropy": a,
                "cobb_angle": cobb,
                "s_lat": s_lat,
                "max_curvature": res.get("max_curvature", 0.0),
                "max_torsion": res.get("max_torsion", 0.0)
            })
        else:
            print(f"  -> Failed: {res.get('error')}")

    # Save Results
    df = pd.DataFrame(results)
    df.to_csv(out_dir / "results.csv", index=False)
    print(f"Saved results to {out_dir / 'results.csv'}")

    # Save Params
    pd.DataFrame([{
        "a_min": anisotropy_values[0],
        "a_max": anisotropy_values[-1],
        "steps": len(anisotropy_values),
        "active_curvature": active_curvature,
        "torsion_drive": torsion_drive,
        "initial_lateral_defect": 0.05,
        "duration": 2.0,
        "n_elements": 50,
        "dt": 1e-4,
        "seed": seed
    }]).to_csv(out_dir / "params.csv", index=False)
    print(f"Saved params to {out_dir / 'params.csv'}")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['stiffness_anisotropy'], df['cobb_angle'], 'o-', linewidth=2, color='blue')
    plt.xlabel('Stiffness Anisotropy')
    plt.ylabel('Cobb Angle (degrees)')
    plt.title(f'Effect of Stiffness Anisotropy on Cobb Angle\n(Active Growth={active_curvature}, Torsion={torsion_drive})')
    plt.grid(True, alpha=0.3)

    plot_path = out_dir / "plot_anisotropy_cobb.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path}")

if __name__ == "__main__":
    run_sweep()
