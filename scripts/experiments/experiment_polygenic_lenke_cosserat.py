#!/usr/bin/env python3
import os
import sys
import pandas as pd
import numpy as np

# Ensure matplotlib uses the Agg backend for headless environments
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add src to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from spinalmodes.countercurvature.multi_segment import get_lenke_profiles, solve_buckling_eigenmodes

def main():
    os.makedirs('outputs/experiments', exist_ok=True)

    N = 100
    z, profiles = get_lenke_profiles(N=N)

    df = pd.DataFrame({'Normalized_Position': z})

    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=True)
    axes = axes.flatten()

    for l_type in range(1, 7):
        lenke_name = f'Lenke_Type_{l_type}'
        B, Q = profiles[lenke_name]

        eigval, evec = solve_buckling_eigenmodes(B, Q, N=N)

        full_mode = np.zeros(N)
        full_mode[2:-2] = evec
        full_mode = full_mode / np.max(np.abs(full_mode)) # Normalize

        if np.sum(full_mode) < 0:
             full_mode = -full_mode

        df[lenke_name] = full_mode

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

    plot_path = 'outputs/experiments/polygenic_lenke_cosserat_plot.png'
    csv_path = 'outputs/experiments/polygenic_lenke_cosserat_results.csv'

    plt.savefig(plot_path, dpi=300)
    df.to_csv(csv_path, index=False)

    print(f"Saved plot to {plot_path}")
    print(f"Saved results to {csv_path}")

if __name__ == '__main__':
    main()
