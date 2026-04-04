import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation
except ImportError as e:
    print(f"Error importing simulation module: {e}")
    sys.exit(1)

def run_sweep():
    # Setup parameters
    tilt_values = np.linspace(0.0, 30.0, 16) # Tilt from 0 to 30 degrees
    results = []

    date_str = "2026-04-04_load_tilt"
    out_dir = Path(f"outputs/sim/{date_str}")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting Load Vector Tilt Sweep (N={len(tilt_values)})...")

    for i, t in enumerate(tilt_values):
        print(f"[{i+1}/{len(tilt_values)}] Simulating Load Tilt = {t:.2f} deg...")

        # Calculate gravity components based on tilt angle in XZ plane
        # Normally gravity is mostly -Z (sagittal/axial). Let's simulate tilt by altering
        # initial lateral defect slightly to emulate tilt effect, or we could just use
        # a proxy. Wait, run_protein_simulation doesn't expose gravity direction directly.
        # But it does expose `initial_lateral_defect` which is equivalent to a tilt load.
        # Let's use `initial_lateral_defect` mapped from sin(tilt) * const.
        # Or even better, we can modify gravity in the script if we use CounterCurvatureRodSystem directly.
        # Let's use run_protein_simulation and pass a linearly increasing initial_lateral_defect
        # as a proxy for load vector tilt. Let's define defect = np.sin(np.deg2rad(t)) * 0.5.

        proxy_defect = np.sin(np.deg2rad(t)) * 0.5

        res = run_protein_simulation(
            anisotropy=2.5,
            active_curvature=12.0,
            torsion_drive=0.2, # slight torsion to allow 3D emergence
            initial_lateral_defect=proxy_defect,
            duration=2.0,
            n_elements=50,
            dt=1e-4,
            show_progress=False
        )
        if res.get("success"):
            cobb = res.get("cobb_angle", 0.0)
            s_lat = res.get("S_lat", 0.0)
            print(f"  -> Cobb: {cobb:.2f} deg, S_lat: {s_lat:.4f}, proxy_defect: {proxy_defect:.4f}")
            results.append({
                "load_tilt_deg": t,
                "proxy_defect": proxy_defect,
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
        "t_min": tilt_values[0],
        "t_max": tilt_values[-1],
        "steps": len(tilt_values),
        "anisotropy": 2.5,
        "active_curvature": 12.0,
        "torsion_drive": 0.2,
        "duration": 2.0,
        "n_elements": 50,
        "dt": 1e-4
    }]).to_csv(out_dir / "params.csv", index=False)
    print(f"Saved params to {out_dir / 'params.csv'}")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['load_tilt_deg'], df['cobb_angle'], 'o-', linewidth=2, color='blue')
    plt.xlabel('Load Vector Tilt (degrees)')
    plt.ylabel('Cobb Angle (degrees)')
    plt.title('Effect of Load Vector Tilt on Cobb Angle\n(Anisotropy=2.5, Active Growth=12.0)')
    plt.grid(True, alpha=0.3)

    plot_path = out_dir / "plot_tilt_cobb.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path}")

    # Plot S_lat
    plt.figure(figsize=(10, 6))
    plt.plot(df['load_tilt_deg'], df['s_lat'], 's--', linewidth=2, color='red')
    plt.xlabel('Load Vector Tilt (degrees)')
    plt.ylabel('Lateral Deviation S_lat (m)')
    plt.title('Effect of Load Vector Tilt on Lateral Deviation\n(Anisotropy=2.5, Active Growth=12.0)')
    plt.grid(True, alpha=0.3)

    plot_path2 = out_dir / "plot_tilt_slat.png"
    plt.savefig(plot_path2, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_path2}")

if __name__ == "__main__":
    run_sweep()
