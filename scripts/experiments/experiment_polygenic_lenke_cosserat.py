#!/usr/bin/env python3
import os
import sys

# Append the src directory to sys.path to allow importing from spinalmodes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from spinalmodes.countercurvature.multi_segment import solve_multi_segment_cosserat_buckling

def calculate_polygenic_multiplier(b, tau, K_d, mgL):
    """
    Simplified stability margin -> polygenic multiplier logic.
    A lower margin (negative) increases the instability drive Q.
    """
    base_margin = 5.3

    b_effect = (1.0 - b) * 20.0
    tau_effect = (tau - 70.0) * -0.5
    kd_effect = (K_d - 10.0) * -2.0
    mgl_effect = (mgL - 73.6) * -0.5

    margin = base_margin - b_effect + tau_effect + kd_effect + mgl_effect

    # Map margin to a multiplier. If margin is positive, multiplier is small.
    # If margin is highly negative, multiplier is large.
    multiplier = np.exp(-margin / 10.0)
    return max(0.1, multiplier)

def main():
    os.makedirs('outputs/experiments', exist_ok=True)
    os.makedirs('outputs/figures', exist_ok=True)

    # Scenarios from polygenic_stacking
    scenarios = [
        {'Scenario': 'Baseline', 'b': 1.0, 'tau_ms': 70.0, 'K_d': 10.0, 'mgL': 73.6},
        {'Scenario': 'Combined (Polygenic Trap)', 'b': 0.71, 'tau_ms': 96.4, 'K_d': 12.96, 'mgL': 93.7}
    ]

    # Generate results for lenke types using polygenic multiplier
    all_data = []

    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=True)
    axes = axes.flatten()

    for l_type in range(1, 7):
        # We will use the 'Combined' scenario multiplier for the visualization to show clear buckling
        combined_scenario = scenarios[1]
        multiplier = calculate_polygenic_multiplier(
            combined_scenario['b'], combined_scenario['tau_ms'],
            combined_scenario['K_d'], combined_scenario['mgL']
        )

        z, eval, evec, B, Q = solve_multi_segment_cosserat_buckling(N=100, lenke_type=l_type, polygenic_multiplier=multiplier)

        full_mode = np.zeros(100)
        full_mode[2:-2] = evec
        full_mode = full_mode / (np.max(np.abs(full_mode)) + 1e-9) # Normalize amplitude

        if np.sum(full_mode) < 0:
             full_mode = -full_mode

        # Add to data list
        for i, z_val in enumerate(z):
            all_data.append({
                'Lenke_Type': l_type,
                'Normalized_Position': z_val,
                'Lateral_Deviation': full_mode[i],
                'Instability_Drive_Q': Q[i],
                'Stiffness_B': B[i]
            })

        # Plot
        ax = axes[l_type-1]
        ax.plot(full_mode, z, linewidth=3, label=f'Eigenmode (Mode 1)')
        ax.plot(Q/np.max(Q), z, 'r--', alpha=0.5, label='Instability Drive Q')
        ax.axvline(0, color='k', linestyle=':', alpha=0.5)

        ax.set_title(f'Lenke Type {l_type}')
        if l_type % 3 == 1:
            ax.set_ylabel('Normalized Position (0=Sacrum, 1=T1)')
        if l_type > 3:
            ax.set_xlabel('Lateral Deviation')
        ax.grid(True, alpha=0.3)

    axes[0].legend(loc='upper left', fontsize='small')
    plt.suptitle('Multi-segment Cosserat Rod: Polygenic Lenke Curve Morphologies', fontsize=16)
    plt.tight_layout()
    plt.savefig('outputs/experiments/polygenic_lenke_cosserat_plot.png')
    print("Saved outputs/experiments/polygenic_lenke_cosserat_plot.png")

    df = pd.DataFrame(all_data)
    df.to_csv('outputs/experiments/polygenic_lenke_cosserat_results.csv', index=False)
    print("Saved outputs/experiments/polygenic_lenke_cosserat_results.csv")

if __name__ == '__main__':
    main()
