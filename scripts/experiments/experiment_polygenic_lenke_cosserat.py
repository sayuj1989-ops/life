#!/usr/bin/env python3
"""
Experiment: Multi-Segment Cosserat Rod Modeling of Lenke Classes.

This script extends the single-link inverted pendulum DDE approach to a continuous
multi-segment Cosserat rod model. By combining the global Polygenic Threshold instability
with regional parameter profiles (stiffness and energy deficit drives), it explicitly
solves for the eigenmodes corresponding to Lenke Curve Types 1-6.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.linalg import eigh

from experiment_utils import StandardExperimentParser, setup_experiment
from spinalmodes.countercurvature.multi_segment import (
    build_regional_stiffness_multiplier,
    build_lenke_instability_drive
)

def solve_lenke_eigenmode(N: int, lenke_type: int):
    """Solves (B y'')'' = lambda Q y for the dominant buckling mode."""
    z = np.linspace(0, 1, N)
    dz = z[1] - z[0]

    # Generate multi-segment spatial parameter profiles
    B = build_regional_stiffness_multiplier(z)
    Q = build_lenke_instability_drive(z, lenke_type)

    # Construct finite difference matrices
    D2 = np.diag(-2 * np.ones(N)) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    D2 = D2 / (dz**2)

    B_matrix = np.diag(B)
    L_matrix = np.dot(D2, np.dot(B_matrix, D2))

    # Apply Boundary conditions (Clamped at z=0: y(0)=0, y'(0)=0)
    # Removing first two and last two nodes
    L_matrix = L_matrix[2:-2, 2:-2]
    Q_matrix = np.diag(Q)[2:-2, 2:-2]

    # Solve generalized eigenvalue problem: L y = lambda Q y
    eigenvalues, eigenvectors = eigh(L_matrix, Q_matrix)

    # Get lowest buckling mode
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    evec = eigenvectors[:, 0]
    full_mode = np.zeros(N)
    full_mode[2:-2] = evec
    full_mode = full_mode / np.max(np.abs(full_mode)) # Normalize

    if np.sum(full_mode) < 0:
         full_mode = -full_mode

    return z, full_mode, B, Q

def main():
    parser = StandardExperimentParser(
        description="Multi-Segment Cosserat Rod Modeling of Polygenic Lenke Curve Types"
    )
    args = parser.parse_args()
    out_dir = setup_experiment(args)

    N = 50 if args.quick else 100

    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=True)
    axes = axes.flatten()

    all_modes = []

    for l_type in range(1, 7):
        z, mode, B, Q = solve_lenke_eigenmode(N, l_type)
        all_modes.append(mode)

        ax = axes[l_type-1]
        ax.plot(mode, z, linewidth=3, label=f'Eigenmode (Mode 1)')
        ax.plot(Q/np.max(Q), z, 'r--', alpha=0.5, label='Instability Drive Q(z)')
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

    fig_path = os.path.join(out_dir, "lenke_multi_segment_cosserat.png")
    plt.savefig(fig_path, dpi=300)
    print(f"Saved figure to {fig_path}")

    # Save to standard outputs/figures/ folder as well for quick access
    os.makedirs('outputs/figures', exist_ok=True)
    std_fig_path = 'outputs/figures/lenke_multi_segment_cosserat.png'
    plt.savefig(std_fig_path, dpi=300)

    # Save Data
    df = pd.DataFrame({'Normalized_Position': np.linspace(0, 1, N)})
    for l_type in range(1, 7):
        df[f'Lenke_Type_{l_type}'] = all_modes[l_type-1]

    csv_path = os.path.join(out_dir, "lenke_multi_segment_cosserat.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved data to {csv_path}")

if __name__ == '__main__':
    main()
