"""Experiment: Proprioceptive Lag Induced Instability.

This script validates the hypothesis that rapid axial growth (increasing L) coupled with
fixed neural conduction velocity leads to a critical feedback delay (tau) that destabilizes
the spinal postural control loop.

Hypothesis:
    As Length (L) increases, the delay tau ~ L/v increases.
    If tau > Critical Delay, the system undergoes a Hopf bifurcation into limit cycle oscillations,
    which manifest as lateral instability (Scoliosis).

Protocol:
    1. Sweep Length L from 0.2m to 0.5m.
    2. Sweep Delay tau from 0ms to 150ms.
    3. Measure resulting Cobb Angle.
    4. Generate Stability Phase Diagram.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from tqdm import tqdm
import time

# Import simulation bridge
# Note: running as script, so we use absolute import based on PYTHONPATH=.
from src.spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation

def run_experiment():
    output_dir = Path("outputs/proprioceptive_lag")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(">>> Starting Proprioceptive Lag Experiment...")

    # Experiment Parameters
    lengths = [0.2, 0.3, 0.4, 0.5]
    # Reduced resolution for quick verification
    delays = np.linspace(0.0, 0.16, 9) # 0, 20, 40 ... 160ms
    gain = 0.5 # Feedback Gain (Nm per unit curvature)

    # Simulation Parameters
    n_elements = 30
    duration = 3.0 # Reduced duration
    dt = 2e-4 # Slightly larger dt for speed, check stability

    results = []

    total_runs = len(lengths) * len(delays)
    pbar = tqdm(total=total_runs, desc="Simulating")

    for L in lengths:
        for tau in delays:
            # We add a small lateral defect to seed instability if it's unstable
            res = run_protein_simulation(
                anisotropy=2.0, # Moderate stability
                active_curvature=1.0, # Drive kyphosis
                initial_lateral_defect=0.1, # Seed: 0.1 m^-1
                length=L,
                n_elements=n_elements,
                duration=duration,
                dt=dt,
                proprioception_delay=tau,
                proprioception_gain=gain,
                show_progress=False
            )

            cobb = res.get("cobb_angle", np.nan)

            results.append({
                "length": L,
                "delay": tau,
                "gain": gain,
                "cobb_angle": cobb,
                "max_curvature": res.get("max_curvature", np.nan),
                "success": res.get("success", False),
                "runtime": res.get("runtime_sec", 0)
            })

            pbar.set_postfix({"L": f"{L:.2f}", "tau": f"{tau:.3f}", "Cobb": f"{cobb:.1f}"})
            pbar.update(1)

    pbar.close()

    # Save Results
    df = pd.DataFrame(results)
    csv_path = output_dir / "stability_sweep.csv"
    df.to_csv(csv_path, index=False)
    print(f"Results saved to {csv_path}")

    # Analysis & Plotting
    plot_results(df, output_dir)

def plot_results(df, output_dir):
    # 1. Heatmap of Cobb Angle
    plt.figure(figsize=(10, 8))
    pivot = df.pivot(index="delay", columns="length", values="cobb_angle")

    # Reverse Y axis so 0 is at bottom? No, standard matrix is fine, but let's make it intuitive.
    # sns.heatmap plots index (delay) on Y (top-down usually).
    # We want 0 at bottom.

    ax = sns.heatmap(pivot, annot=True, fmt=".1f", cmap="magma", cbar_kws={'label': 'Cobb Angle (deg)'})
    ax.invert_yaxis()

    plt.title("Proprioceptive Lag Instability Phase Diagram")
    plt.xlabel("Spine Length (m)")
    plt.ylabel("Proprioceptive Delay (s)")

    plt.tight_layout()
    plt.savefig(output_dir / "stability_phase_diagram.png")
    plt.close()

    # 2. Line Plot: Cobb vs Delay for each Length
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="delay", y="cobb_angle", hue="length", palette="viridis", marker="o")
    plt.title("Instability Onset: Critical Delay Threshold")
    plt.xlabel("Delay (s)")
    plt.ylabel("Cobb Angle (deg)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "cobb_vs_delay.png")
    plt.close()

    print("Plots generated in", output_dir)

if __name__ == "__main__":
    run_experiment()
