import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def main():
    out_dir = Path("outputs/sim/2026-03-17")
    out_dir.mkdir(parents=True, exist_ok=True)

    active_curvature = 15.0
    torsion_drive = 0.5
    anisotropies = np.linspace(1.0, 10.0, 20)

    results = []

    for a in anisotropies:
        res = run_protein_simulation(
            anisotropy=a,
            active_curvature=active_curvature,
            torsion_drive=torsion_drive,
            duration=2.0,
            show_progress=False
        )
        res["anisotropy"] = a
        results.append(res)

    df = pd.DataFrame(results)
    df.to_csv(out_dir / "results.csv", index=False)

    params_df = pd.DataFrame({
        "parameter": ["active_curvature", "torsion_drive", "duration", "n_elements"],
        "value": [active_curvature, torsion_drive, 2.0, 50]
    })
    params_df.to_csv(out_dir / "params.csv", index=False)

    plt.figure(figsize=(10, 6))
    plt.plot(df["anisotropy"], df["cobb_angle"], 'bo-', linewidth=2, label="Cobb Angle (deg)")
    plt.xlabel("Anisotropy")
    plt.ylabel("Cobb Angle (deg)")
    plt.title(f"Scoliosis vs Anisotropy (AC={active_curvature}, Torsion={torsion_drive})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "plot_stiffness_anisotropy.png")
    plt.close()

if __name__ == "__main__":
    main()