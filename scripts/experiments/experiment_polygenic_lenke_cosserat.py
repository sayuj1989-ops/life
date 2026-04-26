import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from spinalmodes.countercurvature.multi_segment import solve_multi_segment_eigenmode

def main():
    os.makedirs('outputs/experiments', exist_ok=True)
    os.makedirs('outputs/figures', exist_ok=True)

    print("Simulating Polygenic Thresholds mapping to Lenke Curve Types via Multi-Segment Cosserat Rod...")

    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=True)
    axes = axes.flatten()

    all_modes = []

    for l_type in range(1, 7):
        z, eval, full_mode, B, Q = solve_multi_segment_eigenmode(N=100, lenke_type=l_type)
        all_modes.append(full_mode)

        ax = axes[l_type-1]
        ax.plot(full_mode, z, linewidth=3, label='Eigenmode (Mode 1)')
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
    plt.savefig('outputs/experiments/polygenic_lenke_cosserat_plot.png')
    print("Saved outputs/experiments/polygenic_lenke_cosserat_plot.png")

    # Save data
    z = np.linspace(0, 1, 100)
    df = pd.DataFrame({'Normalized_Position': z})
    for l_type in range(1, 7):
        df[f'Lenke_Type_{l_type}'] = all_modes[l_type-1]

    df.to_csv('outputs/experiments/polygenic_lenke_cosserat_results.csv', index=False)
    print("Saved outputs/experiments/polygenic_lenke_cosserat_results.csv")

if __name__ == '__main__':
    main()
