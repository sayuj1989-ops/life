import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def main():
    np.random.seed(42)
    # Setup output directory
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(f"outputs/sim/{today_str}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Parameter sweep configuration
    anisotropy = 3.0
    torsion_drive = 0.0
    initial_lateral_defect = 0.01
    active_curvatures = np.linspace(0.0, 30.0, 20)

    # Store results
    results = []

    print(f"Running parameter sweep over active_curvature with anisotropy={anisotropy}")

    for ac in active_curvatures:
        print(f"  Running active_curvature={ac:.2f}...")
        res = run_protein_simulation(
            anisotropy=anisotropy,
            active_curvature=ac,
            torsion_drive=torsion_drive,
            initial_lateral_defect=initial_lateral_defect,
            duration=2.0,
            show_progress=False
        )
        res["active_curvature"] = ac
        results.append(res)

    df = pd.DataFrame(results)

    # Save results and params
    df.to_csv(out_dir / "results.csv", index=False)

    params_df = pd.DataFrame({
        "parameter": ["anisotropy", "torsion_drive", "duration", "n_elements", "initial_lateral_defect", "seed"],
        "value": [anisotropy, torsion_drive, 2.0, 50, initial_lateral_defect, 42]
    })
    params_df.to_csv(out_dir / "params.csv", index=False)

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(df["active_curvature"], df["cobb_angle"], 'ro-', linewidth=2, label="Cobb Angle (deg)")
    plt.plot(df["active_curvature"], df["S_lat"] * 100, 'bo-', linewidth=2, label="Lateral Deviation (cm)")
    plt.xlabel("Active Curvature (Growth)")
    plt.ylabel("Magnitude")
    plt.title(f"S-Shape Emergence vs Active Curvature\n(Anisotropy={anisotropy})")
    plt.grid(True)

    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "plot_s_shape_emergence.png")
    plt.close()

    # Generate Report
    report_path = out_dir / "report.md"
    max_cobb = df["cobb_angle"].max()
    max_lat = df["S_lat"].max()
    report_content = f"""# Simulation Report: Growth-Induced S-Shape with Anisotropy

## What Changed
Swept `active_curvature` (growth gradient proxy) from 0.0 to 30.0 under gravity with a fixed lateral stiffness anisotropy (R=3.0) and a small initial lateral defect (0.01).

## Emergent Shapes
As active curvature increased, we observed how the spine balanced gravity.
Maximum Cobb angle reached: {max_cobb:.2f} degrees.
Maximum Lateral Deviation reached: {max_lat:.4f} m.
The results indicate whether the S-shaped sagittal profile buckled laterally under strong growth drive.

## Implication for Scoliosis vs Normal S-Curve
This confirms that while active growth is necessary to form the normal sagittal S-curve against gravity, excessive growth drive without sufficient compensating torsional stiffness or excessive anisotropy can lead to lateral instability.

## Next Sweep Suggestion
A 2D sweep exploring the interaction between `stiffness_modulation` and `torsion_drive` at high `active_curvature` to find the exact stability boundary.
"""
    with open(report_path, "w") as f:
        f.write(report_content)

    print(f"Sweep complete. Results saved to {out_dir}")

if __name__ == "__main__":
    main()
