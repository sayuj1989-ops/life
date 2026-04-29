import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from spinalmodes.countercurvature.multi_segment import solve_multi_segment_cosserat_buckling

def main():
    # Setup output dir
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'outputs', 'experiments'))
    os.makedirs(out_dir, exist_ok=True)

    def get_stiffness_B(z, lenke_type):
        """Returns stiffness B(z) for a given Lenke type scenario."""
        B = np.ones_like(z)

        # Base stiffness: Thoracic is stiffer due to rib cage
        B[(z >= 0.4) & (z < 0.8)] *= 2.0
        # Proximal thoracic is also stiffer
        B[z >= 0.8] *= 1.5

        if lenke_type == 1:
            # Type 1: Main Thoracic. Thoracic stiffness is reduced (e.g., rib cage anomaly)
            B[(z >= 0.4) & (z < 0.8)] *= 0.5
        elif lenke_type == 5:
            # Type 5: Thoracolumbar/Lumbar. Lumbar stiffness is reduced
            B[(z >= 0.0) & (z < 0.4)] *= 0.5
        elif lenke_type == 6:
            # Type 6: Thoracolumbar/Lumbar - Main Thoracic. Both reduced
            B[(z >= 0.4) & (z < 0.8)] *= 0.6
            B[(z >= 0.0) & (z < 0.4)] *= 0.6

        return B

    def get_instability_Q(z, lenke_type):
        """Returns instability drive Q(z) for a given Lenke type scenario."""
        Q = np.ones_like(z)

        # Base instability: higher in lumbar due to gravity/loading
        Q[(z >= 0.0) & (z < 0.4)] *= 1.5

        if lenke_type == 1:
            # Type 1: High instability drive in thoracic (e.g., mechanoreceptor deficit localized here)
            Q[(z >= 0.4) & (z < 0.8)] *= 2.0
        elif lenke_type == 5:
            # Type 5: High instability drive in thoracolumbar
            Q[(z >= 0.3) & (z < 0.5)] *= 2.0
        elif lenke_type == 6:
            # Type 6: Widespread instability drive
            Q *= 1.5

        return Q

    results = []

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i, lenke_type in enumerate([1, 5, 6]):
        B_func = lambda z: get_stiffness_B(z, lenke_type)
        Q_func = lambda z: get_instability_Q(z, lenke_type)

        vals, vecs, z = solve_multi_segment_cosserat_buckling(B_func, Q_func, n_points=100)

        # Primary mode is the one with smallest eigenvalue
        primary_mode = vecs[:, 0]
        critical_lambda = vals[0]

        # Determine dominant region based on max amplitude
        max_amp_idx = np.argmax(np.abs(primary_mode))
        z_max = z[max_amp_idx]

        if z_max < 0.3:
            region = 'Lumbar'
        elif z_max < 0.4:
            region = 'Thoracolumbar'
        elif z_max < 0.8:
            region = 'Thoracic'
        else:
            region = 'Proximal Thoracic'

        results.append({
            'Lenke_Type': lenke_type,
            'Critical_Lambda': critical_lambda,
            'Dominant_Region': region,
            'Z_Max_Amplitude': z_max
        })

        # Plot
        ax = axes[i]
        # Spine from bottom (z=0) to top (z=1), so plot z on y-axis, y on x-axis
        ax.plot(primary_mode, z, linewidth=2)
        ax.axhline(0.3, color='k', linestyle='--', alpha=0.3)
        ax.axhline(0.4, color='k', linestyle='--', alpha=0.3)
        ax.axhline(0.8, color='k', linestyle='--', alpha=0.3)

        ax.text(0, 0.15, 'Lumbar', ha='center', alpha=0.5)
        ax.text(0, 0.35, 'TL', ha='center', alpha=0.5)
        ax.text(0, 0.6, 'Thoracic', ha='center', alpha=0.5)
        ax.text(0, 0.9, 'Prox. Thoracic', ha='center', alpha=0.5)

        ax.set_title(f'Lenke Type {lenke_type} Mode')
        ax.set_ylabel('Spine Height (z)')
        ax.set_xlabel('Deflection')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'polygenic_lenke_cosserat_plot.png'))

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(out_dir, 'polygenic_lenke_cosserat_results.csv'), index=False)

if __name__ == "__main__":
    main()
