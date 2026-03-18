import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def main():
    # Setup output directory
    out_dir = Path("outputs/sim/2026-03-18")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Parameter sweep configuration
    active_curvature = 12.0
    torsion_drive = 0.0
    anisotropies = np.linspace(0.5, 5.0, 20)

    # Store results
    results = []

    print(f"Running parameter sweep over stiffness_anisotropy with active_curvature={active_curvature}, torsion_drive={torsion_drive}")

    for aniso in anisotropies:
        print(f"  Running stiffness_anisotropy={aniso:.2f}...")
        res = run_protein_simulation(
            anisotropy=aniso,
            active_curvature=active_curvature,
            torsion_drive=torsion_drive,
            duration=2.0,
            show_progress=False
        )
        res["stiffness_anisotropy"] = aniso
        results.append(res)

    df = pd.DataFrame(results)

    # Save results and params
    df.to_csv(out_dir / "results.csv", index=False)

    params_df = pd.DataFrame({
        "parameter": ["active_curvature", "torsion_drive", "duration", "n_elements"],
        "value": [active_curvature, torsion_drive, 2.0, 50]
    })
    params_df.to_csv(out_dir / "params.csv", index=False)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plot Cobb Angle vs Stiffness Anisotropy
    plt.plot(df["stiffness_anisotropy"], df["cobb_angle"], 'bo-', linewidth=2, label="Cobb Angle (deg)")
    plt.xlabel("Stiffness Anisotropy")
    plt.ylabel("Cobb Angle (deg)")
    plt.title(f"Scoliosis Emergence vs Stiffness Anisotropy\n(Active Curvature={active_curvature}, Torsion Drive={torsion_drive})")
    plt.grid(True)

    # Highlight critical threshold if exists
    max_cobb = df["cobb_angle"].max()
    if max_cobb > 10:
        critical_idx = df["cobb_angle"] > 10
        if critical_idx.any():
            crit_aniso = df.loc[critical_idx, "stiffness_anisotropy"].iloc[-1]
            plt.axvline(x=crit_aniso, color='r', linestyle='--', label=f"Critical Threshold (~{crit_aniso:.1f})")

    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "plot_stiffness_anisotropy.png")
    plt.close()

    print(f"Sweep complete. Results saved to {out_dir}")

if __name__ == "__main__":
    main()
