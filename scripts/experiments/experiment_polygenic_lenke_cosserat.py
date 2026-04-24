#!/usr/bin/env python3
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.spinalmodes.countercurvature.multi_segment import solve_buckling_eigenmodes

def main():
    os.makedirs('outputs/experiments', exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=True)
    axes = axes.flatten()

    all_modes = []

    for l_type in range(1, 7):
        z, eval_, evec, B, Q = solve_buckling_eigenmodes(N=100, lenke_type=l_type)

        full_mode = np.zeros(100)
        full_mode[2:-2] = evec
        full_mode = full_mode / (np.max(np.abs(full_mode)) + 1e-10)

        if np.sum(full_mode) < 0:
            full_mode = -full_mode

        all_modes.append(full_mode)

        ax = axes[l_type-1]
        ax.plot(full_mode, z, linewidth=3, label=r'Eigenmode (Mode 1)')
        ax.plot(Q/np.max(Q), z, 'r--', alpha=0.5, label='Instability Drive Q')
        ax.axvline(0, color='k', linestyle=':', alpha=0.5)

        ax.set_title(f'Lenke Type {l_type}')
        if l_type % 3 == 1:
            ax.set_ylabel('Normalized Position (0=Sacrum, 1=T1)')
        if l_type > 3:
            ax.set_xlabel('Lateral Deviation')
        ax.grid(True, alpha=0.3)

    axes[0].legend(loc='upper left', fontsize='small')
    plt.suptitle('Multi-segment Cosserat Rod: Lenke Curve Morphologies', fontsize=16)
    plt.tight_layout()
    plot_path = 'outputs/experiments/polygenic_lenke_cosserat_plot.png'
    plt.savefig(plot_path)
    print(f"Saved {plot_path}")

    z = np.linspace(0, 1, 100)
    df = pd.DataFrame({'Normalized_Position': z})
    for l_type in range(1, 7):
        df[f'Lenke_Type_{l_type}'] = all_modes[l_type-1]

    csv_path = 'outputs/experiments/polygenic_lenke_cosserat_results.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved {csv_path}")

if __name__ == '__main__':
    main()
