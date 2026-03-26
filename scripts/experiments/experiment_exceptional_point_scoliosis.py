"""
Experiment: Non-Hermitian Exceptional Points in Spinal Biomechanics.

This script implements a 2-DOF non-Hermitian eigenvalue model coupling lateral
bending and axial torsion, simulating the active, proprioceptively controlled spine.
It computes the complex eigenvalues across a 2D parameter sweep (Active Feedback
Gain vs. Bending Stiffness) to identify the Exceptional Point (EP) where
eigenvalues and eigenvectors coalesce.

At the EP, the system's sensitivity to perturbations (like minor collagen
anisotropy or metabolic delay) scales non-linearly (as sqrt(epsilon) instead
of epsilon), positing that scoliosis is an emergent topological phase transition
caused by the spine lingering near a biomechanical EP during the adolescent
growth spurt.
"""

import os
import sys
import time
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Ensure src is in python path
current_file = Path(__file__).resolve()
src_path = current_file.parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))


def run_ep_simulation():
    print("Running Non-Hermitian Exceptional Point Simulation...")
    t0 = time.time()

    out_dir = Path("outputs/exceptional_points")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Parameter Sweep Grid
    # G: Active feedback gain (proprioceptive sensitivity)
    # K: Bending stiffness
    N = 100
    G_vals = np.linspace(0.5, 3.0, N)
    K_vals = np.linspace(0.5, 3.0, N)

    # Grid matrices for results
    eig1_real = np.zeros((N, N))
    eig2_real = np.zeros((N, N))
    eig1_imag = np.zeros((N, N))
    eig2_imag = np.zeros((N, N))
    sensitivity = np.zeros((N, N))

    results = []

    # System Parameters
    # Modeling the spine as a 2x2 non-Hermitian matrix H:
    # H = [ K - i*gamma,     G       ]
    #     [    -G,       K + i*gamma ]
    # Where:
    # K is base stiffness
    # gamma is intrinsic damping/loss
    # G represents the active, non-reciprocal coupling (sensorimotor feedback)
    gamma = 1.0

    # Perturbation magnitude to measure sensitivity near EP
    epsilon = 1e-4

    for i, K in enumerate(K_vals):
        for j, G in enumerate(G_vals):
            # Construct Non-Hermitian Matrix
            H = np.array([
                [K - 1j * gamma, G],
                [-G, K + 1j * gamma]
            ])

            # Compute eigenvalues
            vals, vecs = np.linalg.eig(H)

            # Sort eigenvalues by real part, then imaginary
            idx = np.argsort(np.real(vals))
            vals = vals[idx]

            eig1_real[i, j] = np.real(vals[0])
            eig2_real[i, j] = np.real(vals[1])
            eig1_imag[i, j] = np.imag(vals[0])
            eig2_imag[i, j] = np.imag(vals[1])

            # Calculate Sensitivity (Spectral Gap)
            # Near an EP, the spectral gap closes. The response to a perturbation
            # delta_H scales as sqrt(epsilon).
            gap = np.abs(vals[0] - vals[1])

            # Perturbed system
            H_pert = H + np.array([[epsilon, 0], [0, 0]])
            vals_pert, _ = np.linalg.eig(H_pert)
            gap_pert = np.abs(vals_pert[0] - vals_pert[1])

            # Ratio of eigenvalue shift to perturbation magnitude
            # High near EP
            shift = max(np.abs(vals_pert[0] - vals[0]), np.abs(vals_pert[1] - vals[1]))
            sens = shift / epsilon
            sensitivity[i, j] = sens

            # Determine if this point is near the EP (where gap ~ 0)
            is_ep = gap < 1e-2

            if i % 10 == 0 and j == N//2:
                results.append({
                    "K_stiffness": K,
                    "G_gain": G,
                    "eig1_real": np.real(vals[0]),
                    "eig1_imag": np.imag(vals[0]),
                    "eig2_real": np.real(vals[1]),
                    "eig2_imag": np.imag(vals[1]),
                    "spectral_gap": gap,
                    "sensitivity": sens,
                    "is_ep": is_ep
                })

    # Save CSV Results
    df = pd.DataFrame(results)
    csv_path = out_dir / "ep_metrics.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved metrics to {csv_path}")

    # Plot 1: Riemann Surfaces of Eigenvalues (Real Part)
    G_grid, K_grid = np.meshgrid(G_vals, K_vals)

    fig = plt.figure(figsize=(12, 5))

    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(G_grid, K_grid, eig1_real, cmap='viridis', alpha=0.8)
    ax1.plot_surface(G_grid, K_grid, eig2_real, cmap='plasma', alpha=0.8)
    ax1.set_xlabel('Active Gain (G)')
    ax1.set_ylabel('Stiffness (K)')
    ax1.set_zlabel('Re(Eigenvalues)')
    ax1.set_title('Riemann Surface: Real Part')

    # Plot 2: Imaginary Part showing coalescence
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(G_grid, K_grid, eig1_imag, cmap='viridis', alpha=0.8)
    ax2.plot_surface(G_grid, K_grid, eig2_imag, cmap='plasma', alpha=0.8)
    ax2.set_xlabel('Active Gain (G)')
    ax2.set_ylabel('Stiffness (K)')
    ax2.set_zlabel('Im(Eigenvalues)')
    ax2.set_title('Riemann Surface: Imaginary Part (Coalescence at EP)')

    plt.tight_layout()
    plot_path1 = out_dir / "ep_riemann_surfaces.png"
    plt.savefig(plot_path1, dpi=300)
    plt.close()
    print(f"Saved Riemann surfaces plot to {plot_path1}")

    # Plot 3: Non-linear Sensitivity Map
    plt.figure(figsize=(8, 6))
    plt.pcolormesh(G_grid, K_grid, np.log10(sensitivity), shading='auto', cmap='inferno')
    plt.colorbar(label='Log10(Sensitivity)')
    plt.xlabel('Active Gain (G)')
    plt.ylabel('Stiffness (K)')
    plt.title('Topological Sensitivity near Exceptional Point')

    # Highlight EP region
    ep_indices = np.where(sensitivity > np.percentile(sensitivity, 99))
    if len(ep_indices[0]) > 0:
        plt.scatter(G_vals[ep_indices[1]], K_vals[ep_indices[0]],
                    color='cyan', s=10, label='Exceptional Point Region')
        plt.legend()

    plot_path2 = out_dir / "ep_sensitivity_map.png"
    plt.savefig(plot_path2, dpi=300)
    plt.close()
    print(f"Saved sensitivity map to {plot_path2}")

    t1 = time.time()
    print(f"Simulation completed in {t1 - t0:.2f} seconds.")


if __name__ == "__main__":
    run_ep_simulation()
