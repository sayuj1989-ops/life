#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Ensure spinalmodes is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from spinalmodes.countercurvature.multi_segment import solve_multi_segment_cosserat_buckling

def compute_stability_margin(tau, b, Kd, mgL):
    """
    Simplified stability margin calculation for the inverted pendulum with delayed feedback.
    margin < 0 implies instability (Hopf bifurcation crossed).
    """
    # Baseline Hopf threshold approximations
    # In a real dynamic model, this requires solving the roots of the characteristic quasi-polynomial.
    # Here we use a surrogate empirical formulation capturing the trade-offs:
    # Margin = Damping + Control - Delay_penalty - Load_penalty

    # Normalizing around baseline (tau=70, b=1.0, Kd=12.0, mgL=73.6 -> Margin ~ +5.3)
    # This is a phenomenological map to demonstrate the polygenic stacking.
    base_margin = 5.3

    delta_tau = tau - 70.0
    delta_b = b - 1.0
    delta_Kd = Kd - 12.0
    delta_mgL = mgL - 73.6

    # Penalties
    # Higher delay decreases margin
    # Lower damping decreases margin
    # Shifted Kd (towards peak) decreases margin
    # Higher load decreases margin

    margin = base_margin - 0.2 * delta_tau + 15.0 * delta_b - 1.5 * np.abs(delta_Kd) - 0.1 * delta_mgL
    return margin

def assign_lenke_type(tau, b, Kd, mgL):
    """
    Heuristic mapping from molecular parameter stack to regional structural vulnerability (Lenke Type).
    This simulates how systemic delays or structural weaknesses manifest in specific eigenmodes.
    """
    # Lenke 1 (Main Thoracic): Driven heavily by delay (tau) and low damping (b) in thoracic region.
    # Lenke 5 (TL/L): Driven heavily by load (mgL) on the vulnerable TL junction.
    # Lenke 2/3/4/6 are intermediate mixed states.

    if mgL > 85.0 and tau < 85.0:
        return 5 # Load dominated -> TL junction buckles
    elif tau > 85.0 and mgL < 80.0:
        return 1 # Delay dominated -> Thoracic (longest moment arm) buckles
    elif tau > 85.0 and mgL >= 80.0:
        return 3 # Combined severe -> Double major
    elif b < 0.8:
        return 2 # Severe structural laxity -> Double thoracic
    elif Kd > 12.5:
        return 4 # Control gain mismatch -> Triple
    else:
        return 6 # Default mixed

def run_polygenic_simulation():
    print("Running Polygenic Lenke Cosserat Simulation...")
    np.random.seed(42)
    N_pop = 10000

    # 1. Generate Polygenic Population
    # Parameters distributed normally around the baseline
    tau_dist = np.random.normal(loc=70.0, scale=10.0, size=N_pop)
    b_dist = np.random.normal(loc=1.0, scale=0.15, size=N_pop)
    Kd_dist = np.random.normal(loc=12.0, scale=0.5, size=N_pop)
    mgL_dist = np.random.normal(loc=73.6, scale=8.0, size=N_pop)

    margins = np.zeros(N_pop)
    lenke_assignments = np.zeros(N_pop, dtype=int)

    unstable_indices = []

    for i in range(N_pop):
        margin = compute_stability_margin(tau_dist[i], b_dist[i], Kd_dist[i], mgL_dist[i])
        margins[i] = margin
        if margin < 0:
            unstable_indices.append(i)
            lenke_assignments[i] = assign_lenke_type(tau_dist[i], b_dist[i], Kd_dist[i], mgL_dist[i])

    prevalence = len(unstable_indices) / N_pop * 100
    print(f"Population Size: {N_pop}")
    print(f"Unstable Individuals (AIS Prevalence): {len(unstable_indices)} ({prevalence:.2f}%)")

    os.makedirs('outputs/experiments', exist_ok=True)

    # 2. Simulate Lenke Curve Types for Unstable Individuals
    # We will simulate all 6 Lenke types using the multi-segment Cosserat model.
    print("Simulating Multi-segment Cosserat Eigenmodes for Lenke Types 1-6...")

    z_array = None
    lenke_modes = {}

    for l_type in range(1, 7):
        z, evals, evec, B, Q = solve_multi_segment_cosserat_buckling(N=100, lenke_type=l_type)
        if z_array is None:
            z_array = z
        lenke_modes[f'Lenke_Type_{l_type}'] = evec

    # Save CSV with curve shapes
    df_curves = pd.DataFrame({'Normalized_Position': z_array})
    for l_type in range(1, 7):
        df_curves[f'Lenke_Type_{l_type}'] = lenke_modes[f'Lenke_Type_{l_type}']

    csv_path = 'outputs/experiments/polygenic_lenke_cosserat_results.csv'
    df_curves.to_csv(csv_path, index=False)
    print(f"Saved structural curves to {csv_path}")

    # 3. Generate Visual Artifacts
    import matplotlib
    matplotlib.use('Agg') # Handle headless environments
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(16, 8))

    # Subplot 1: Polygenic Threshold Distribution
    ax1 = plt.subplot(1, 2, 1)
    ax1.hist(margins, bins=50, color='lightgray', edgecolor='gray', alpha=0.7)

    # Highlight unstable tail
    unstable_margins = [margins[i] for i in unstable_indices]
    ax1.hist(unstable_margins, bins=20, color='red', edgecolor='darkred', alpha=0.8, label=f'Unstable (Margin < 0)\nPrevalence: {prevalence:.1f}%')
    ax1.axvline(x=0, color='black', linestyle='--', linewidth=2, label='Hopf Bifurcation Threshold')
    ax1.set_title("Polygenic Stacking: Universal Trap vs Individual Vulnerability", fontsize=12)
    ax1.set_xlabel("Stability Margin (ms) - Distance to Bifurcation")
    ax1.set_ylabel("Frequency (Simulated Population)")
    ax1.legend()

    # Subplot 2: Multi-segment Lenke Curve Expressions
    ax2 = plt.subplot(1, 2, 2)
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown']

    # Spread them out horizontally for clarity
    offsets = np.linspace(-0.5, 0.5, 6)

    for l_type in range(1, 7):
        # Count frequency in the unstable sub-population
        freq = np.sum(lenke_assignments == l_type) / len(unstable_indices) * 100 if len(unstable_indices) > 0 else 0

        mode = lenke_modes[f'Lenke_Type_{l_type}']
        ax2.plot(mode + offsets[l_type-1], z_array, color=colors[l_type-1], linewidth=2.5,
                 label=f'Lenke {l_type} ({freq:.1f}%)')
        ax2.axvline(offsets[l_type-1], color='gray', linestyle=':', alpha=0.3)

    ax2.set_title("Multi-segment Cosserat Model: Lenke Morphologies", fontsize=12)
    ax2.set_ylabel("Normalized Spinal Position (0=Sacrum, 1=T1)")
    ax2.set_xlabel("Lateral Deviation (Offset for clarity)")
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.2)

    plt.suptitle("Polygenic Trigger & Structural Morphogenesis of Adolescent Idiopathic Scoliosis", fontsize=16)
    plt.tight_layout()

    plot_path = 'outputs/experiments/polygenic_lenke_cosserat_plot.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Saved simulation plot to {plot_path}")

if __name__ == '__main__':
    run_polygenic_simulation()
