"""
Weekly Simulation: Anisotropy x Growth Mismatch (2026-08-06)

Goal:
Test whether an S-shaped spinal profile emerges under gravity-like loading with growth + anisotropic stiffness.
This sweep specifically targets the 'Vector-Scalar Mismatch' hypothesis where high growth (scalar)
overwhelms directional stiffness (vector), or vice versa.

Hypothesis:
High anisotropy should stabilize the spine against growth-induced buckling, but there may be a crossover point.
"""

import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add scripts directory to path to allow importing experiment_minimal_elastica
sys.path.append(str(Path(__file__).parent))

# Add src to path for direct access if needed (though experiment_minimal_elastica does it too)
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from experiment_minimal_elastica import run_experiment
except ImportError:
    # Fallback if running from a different context
    sys.path.append("scripts")
    from experiment_minimal_elastica import run_experiment

def run_sweep():
    # Setup paths
    date_str = "2026-08-06"
    out_dir = Path(f"outputs/sim/{date_str}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "results.csv"

    # Define Sweep Parameters
    # Anisotropy: Vector signal (Directional Stiffness)
    # Reduced set for performance
    anisotropies = [1.0, 4.0, 12.0]

    # Chi_Kappa: Scalar signal (Growth/Gain)
    # Reduced set for performance
    chi_kappas = [0.0, 10.0, 20.0, 30.0]

    # Chi_Tau: Zero to isolate planar buckling/S-shape emergence
    chi_taus = [0.0]

    # Run Experiment
    print(f"Starting sweep: {date_str} - Anisotropy x Growth Mismatch")
    if out_file.exists():
        out_file.unlink() # Clear previous results

    # Optimization: n_elements=30, final_time=1.0 for speed (12 runs * 30s = 6 mins)
    run_experiment(
        out_file=str(out_file),
        anisotropies=anisotropies,
        chi_kappas=chi_kappas,
        chi_taus=chi_taus,
        boundary_condition="fixed",
        n_elements=30,
        final_time=1.0,
        curvature_profile="constant",
        info_center=0.6,
        info_width=0.1,
        info_amplitude=0.1
    )

    return out_dir, out_file

def analyze_results(out_dir, out_file):
    print("Analyzing results...")

    results = []
    with open(out_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            for key in row:
                try:
                    row[key] = float(row[key])
                except ValueError:
                    pass
            results.append(row)

    # Plotting
    plot_metric(results, "s_lat", "Lateral Deviation (S_lat)", out_dir / "plot_s_lat.png")
    plot_metric(results, "cobb_angle", "Cobb Angle (deg)", out_dir / "plot_cobb.png")
    plot_metric(results, "max_curvature", "Max Curvature (1/m)", out_dir / "plot_curvature.png")

    # Generate Report
    write_report(results, out_dir / "report.md")

def plot_metric(results, metric_key, ylabel, save_path):
    anisotropies = sorted(list(set(r["stiffness_anisotropy"] for r in results)))

    plt.figure(figsize=(10, 6))

    for aniso in anisotropies:
        subset = [r for r in results if r["stiffness_anisotropy"] == aniso]
        subset.sort(key=lambda x: x["chi_kappa"])

        x = [r["chi_kappa"] for r in subset]
        y = [r[metric_key] for r in subset]

        plt.plot(x, y, marker='o', label=f"Anisotropy={aniso}")

    plt.xlabel("Growth Gain (chi_kappa)")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} vs Growth Gain by Anisotropy")
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()
    print(f"Saved plot: {save_path}")

def write_report(results, report_path):
    # Determine key findings
    # Find max S_lat
    if not results:
        max_s_lat = 0.0
        max_cobb = 0.0
    else:
        max_s_lat = max(r["s_lat"] for r in results)
        max_cobb = max(r["cobb_angle"] for r in results)

    # Check for emergence of S-shapes (S_lat > 0.1 is usually significant)
    unstable_runs = [r for r in results if r["s_lat"] > 0.1]

    report = f"""# Simulation Report: Anisotropy-Growth Mismatch (2026-08-06)

## Overview
This experiment tested the "Vector-Scalar Mismatch" hypothesis by sweeping **Growth Gain (chi_kappa)** against **Stiffness Anisotropy**.
The goal was to determine if high growth coupled with low or high anisotropy induces S-shaped buckling in a gravity-loaded spine.

## Parameters
- **Anisotropy:** 1.0, 4.0, 12.0
- **Chi_Kappa:** 0.0, 10.0, 20.0, 30.0
- **Chi_Tau:** 0.0 (Planar)
- **Boundary:** Fixed
- **Curvature:** Constant (Sagittal Kyphosis)

## Key Findings
- **Max Lateral Deviation (S_lat):** {max_s_lat:.4f} m
- **Max Cobb Angle:** {max_cobb:.4f} deg

### Emergent Behaviors
"""

    if not unstable_runs:
        report += "- **Stability:** The spine remained stable across all parameters tested. No significant S-shaped buckling observed (S_lat < 0.1).\\n"
    else:
        report += "- **Instability:** Significant lateral deviation was observed.\\n"
        # Analyze relationship
        low_aniso_instability = any(r["s_lat"] > 0.1 for r in unstable_runs if r["stiffness_anisotropy"] <= 2.0)
        high_aniso_stability = all(r["s_lat"] < 0.1 for r in results if r["stiffness_anisotropy"] >= 8.0)

        if low_aniso_instability:
            report += "- **Vector-Scalar Mismatch:** Low anisotropy (weak vector) combined with high growth (strong scalar) triggered buckling.\\n"

        if high_aniso_stability:
            report += "- **Anisotropic Protection:** High anisotropy (R >= 8.0) successfully suppressed growth-induced buckling.\\n"
        elif any(r["s_lat"] > 0.1 for r in results if r["stiffness_anisotropy"] >= 8.0):
             report += "- **Failure of Protection:** Even high anisotropy failed to suppress buckling at high growth rates.\\n"

    report += """
## Conclusion
This sweep informs the Scoliosis Mechanism Map by clarifying the role of Stiffness Anisotropy as a stabilizing 'Vector' force against 'Scalar' growth expansion.

## Next Steps
- Investigate if Torsion (chi_tau) breaks the anisotropic protection seen here.
- Test with 'harmonic' curvature profiles to simulate pre-existing imperfections.
"""

    with open(report_path, "w") as f:
        f.write(report)
    print(f"Saved report: {report_path}")

if __name__ == "__main__":
    out_dir, out_file = run_sweep()
    analyze_results(out_dir, out_file)
