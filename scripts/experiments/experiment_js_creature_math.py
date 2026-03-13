"""
Experiment: JS Creature Math Translation
----------------------------------------
This script is a Python translation of the provided p5.js "creature" mathematical
algorithm. It generates and saves a visualization at two different time points (t=0, t=PI).
The structure of this math shares similarities with the Information-Elasticity Coupling
(IEC) and Biological Counter-Curvature models present in the repository, combining
spatial periodic modes (akin to an information field `k`) and a linear positional gradient (`e`)
into an emergent structural metric (`d`) that drives a dynamic structural response (`wave`).

Usage:
    python scripts/experiments/experiment_js_creature_math.py
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def generate_organism(x: float, y: float, t: float) -> tuple[float, float]:
    """
    Computes a single coordinate for the 'creature' shape based on the
    p5.js algorithm.
    """
    # k acts as a spatial periodic mode or information field
    k = 5 * np.cos(x / 14) * np.cos(y / 30)

    # e acts as a linear/gravity-like gradient along y
    e = y / 8 - 13

    # d is the emergent structural metric combining k and e
    d = (k**2 + e**2) / 59 + 4

    # Angle processing
    angleTerm = np.arctan2(k, e)
    q = 60 - 3 * np.sin(angleTerm * e)

    # Dynamic active wave component
    wave = k * (3 + 4 / d * np.sin(d * d - t * 2))

    # Helical/rotational deformation variable
    c = d / 2 + e / 99 - t / 18

    # Final geometric transformation
    xCoord = (q + wave) * np.sin(c) + 200
    yCoord = (q + d * 9) * np.cos(c) + 200

    return xCoord, yCoord

def run_simulation(t: float, output_path: Path) -> None:
    """
    Generates 10000 points and plots the organism for a given time step.
    """
    x_vals = []
    y_vals = []

    for i in range(10000):
        x = i % 80
        y = i / 43
        xc, yc = generate_organism(x, y, t)
        x_vals.append(xc)
        y_vals.append(yc)

    plt.figure(figsize=(6, 6), facecolor='#090909')
    plt.scatter(x_vals, y_vals, s=0.15, color='white', alpha=0.5)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#090909')
    plt.close()

    print(f"Saved: {output_path}")

def main():
    # Setup output directory
    output_dir = Path('outputs/experiments/js_creature')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate visualization for two time points
    print("Generating JS creature visualization (t=0)...")
    run_simulation(0, output_dir / 'creature_t0.png')

    print("Generating JS creature visualization (t=pi)...")
    run_simulation(np.pi, output_dir / 'creature_tPI.png')

    print("Generation complete.")

if __name__ == "__main__":
    main()
