import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path

# Use Agg backend for matplotlib
plt.switch_backend('Agg')

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation, verify_pyelastica_installation

def run_sweep():
    # Verify PyElastica is installed
    verify_pyelastica_installation(exit_on_fail=True)

    # Output directory
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(f"outputs/sim/{date_str}_kyphosis_emergence")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Parameters
    seed = 42
    np.random.seed(seed)

    natural_kyphosis_vals = np.linspace(0.0, 5.0, 20)
    anisotropy_val = 3.0
    active_curvature_val = 10.0 # Some growth to make the system sensitive

    results = []

    # Run the sweep
    for nk in natural_kyphosis_vals:
        print(f"Running simulation with natural_kyphosis = {nk:.2f}...")

        # Save exact config used for reproducibility
        config = {
            "seed": seed,
            "anisotropy": anisotropy_val,
            "active_curvature": active_curvature_val,
            "torsion_drive": 0.0,
            "stiffness_modulation": 0.0,
            "initial_lateral_defect": 0.0,
            "natural_kyphosis": nk,
            "length": 0.4,
            "n_elements": 50,
            "duration": 2.0,
        }

        # Call the simulation engine
        res = run_protein_simulation(
            anisotropy=config["anisotropy"],
            active_curvature=config["active_curvature"],
            torsion_drive=config["torsion_drive"],
            stiffness_modulation=config["stiffness_modulation"],
            initial_lateral_defect=config["initial_lateral_defect"],
            natural_kyphosis=config["natural_kyphosis"],
            length=config["length"],
            n_elements=config["n_elements"],
            duration=config["duration"],
            show_progress=False
        )

        if res.get("success"):
            # Include input parameters alongside results for clarity
            row = config.copy()
            row.update({
                "max_curvature": res.get("max_curvature"),
                "max_torsion": res.get("max_torsion"),
                "end_to_end_distance": res.get("end_to_end_distance"),
                "S_lat": res.get("S_lat"),
                "cobb_angle": res.get("cobb_angle"),
                "z_tip": res.get("z_tip"),
                "x_tip": res.get("x_tip"),
                "y_tip": res.get("y_tip"),
                "U_CC": res.get("U_CC"),
                "info_gain_ratio": res.get("info_gain_ratio")
            })
            results.append(row)
        else:
            print(f"  Simulation failed: {res.get('error')}")
            # Append empty/NaN data
            row = config.copy()
            row.update({k: np.nan for k in ["max_curvature", "max_torsion", "end_to_end_distance", "S_lat", "cobb_angle", "z_tip", "x_tip", "y_tip", "U_CC", "info_gain_ratio"]})
            results.append(row)

    # Save params.csv (what was swept)
    params_df = pd.DataFrame({"natural_kyphosis": natural_kyphosis_vals, "active_curvature": [active_curvature_val]*len(natural_kyphosis_vals), "anisotropy": [anisotropy_val]*len(natural_kyphosis_vals), "seed": [seed]*len(natural_kyphosis_vals)})
    params_df.to_csv(out_dir / "params.csv", index=False)

    # Save results.csv
    results_df = pd.DataFrame(results)
    results_df.to_csv(out_dir / "results.csv", index=False)

    # Generate and save plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: S_lat and Cobb Angle vs natural_kyphosis
    ax1 = axes[0]
    ax1.plot(results_df["natural_kyphosis"], results_df["S_lat"], 'bo-', label="S_lat (Lateral Deviation)")
    ax1.set_xlabel("Natural Kyphosis")
    ax1.set_ylabel("Lateral Scoliosis Index (S_lat)", color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    ax2.plot(results_df["natural_kyphosis"], results_df["cobb_angle"], 'ro--', label="Cobb Angle")
    ax2.set_ylabel("Cobb Angle (degrees)", color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    ax1.set_title("Emergent S-Shape Geometry vs Kyphosis")
    ax1.grid(True, alpha=0.3)

    # Plot 2: Max Curvature and Tip Z Deflection
    ax3 = axes[1]
    ax3.plot(results_df["natural_kyphosis"], results_df["max_curvature"], 'go-', label="Max Curvature (1/m)")
    ax3.set_xlabel("Natural Kyphosis")
    ax3.set_ylabel("Max Curvature (1/m)", color='g')
    ax3.tick_params(axis='y', labelcolor='g')

    ax4 = ax3.twinx()
    # Normalize z_tip roughly
    ax4.plot(results_df["natural_kyphosis"], results_df["z_tip"], 'mo--', label="Z Tip Position (m)")
    ax4.set_ylabel("Z Tip Position (m)", color='m')
    ax4.tick_params(axis='y', labelcolor='m')

    ax3.set_title("Sagittal and Longitudinal Metrics")
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_dir / "plot_metrics.png", dpi=300)
    plt.close()

    print(f"Sweep complete! Results saved to {out_dir}")

if __name__ == "__main__":
    run_sweep()
