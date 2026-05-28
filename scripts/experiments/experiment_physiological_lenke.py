import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.spinalmodes.countercurvature.physiological_lenke import solve_physiological_lenke_buckling

def main():
    os.makedirs('outputs/experiments', exist_ok=True)

    # Plot for Baseline vs Polygenic
    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=True)
    axes = axes.flatten()

    all_modes_base = []
    all_modes_poly = []

    for l_type in range(1, 7):
        # Baseline solve
        zb, eval_b, evec_b, EI_b, Q_b = solve_physiological_lenke_buckling(N=100, lenke_type=l_type, baseline=True)
        mode_b = np.zeros(100)
        mode_b[2:-2] = evec_b
        mode_b = mode_b / np.max(np.abs(mode_b))
        if np.sum(mode_b) < 0: mode_b = -mode_b
        all_modes_base.append(mode_b)

        # Polygenic solve
        zp, eval_p, evec_p, EI_p, Q_p = solve_physiological_lenke_buckling(N=100, lenke_type=l_type, baseline=False)
        mode_p = np.zeros(100)
        mode_p[2:-2] = evec_p
        mode_p = mode_p / np.max(np.abs(mode_p))
        if np.sum(mode_p) < 0: mode_p = -mode_p
        all_modes_poly.append(mode_p)

        ax = axes[l_type-1]
        ax.plot(mode_b, zb, 'b-', linewidth=2, label='Baseline Mode')
        ax.plot(mode_p, zp, 'r--', linewidth=2, label='Polygenic Mode')
        ax.axvline(0, color='k', linestyle=':', alpha=0.5)

        ax.set_title(f'Lenke Type {l_type}')
        if l_type % 3 == 1: ax.set_ylabel('Normalized Position (0=Sacrum, 1=T1)')
        if l_type > 3: ax.set_xlabel('Lateral Deviation')
        ax.grid(True, alpha=0.3)

    axes[0].legend(loc='upper left', fontsize='small')
    plt.suptitle('Physiological Cosserat Rod: Lenke Morphologies (Baseline vs Polygenic Stack)', fontsize=16)
    plt.tight_layout()
    plt.savefig('outputs/experiments/physiological_lenke_plot.png')

    # Save to CSV
    df = pd.DataFrame({'Normalized_Position': zb})
    for l_type in range(1, 7):
        df[f'Lenke_Type_{l_type}_Base'] = all_modes_base[l_type-1]
        df[f'Lenke_Type_{l_type}_Poly'] = all_modes_poly[l_type-1]

    df.to_csv('outputs/experiments/physiological_lenke_results.csv', index=False)

if __name__ == '__main__':
    main()
