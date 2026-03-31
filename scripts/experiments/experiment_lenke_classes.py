#!/usr/bin/env python3
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.linalg import eigh

def get_lenke_parameters(lenke_type, N=100):
    z = np.linspace(0, 1, N)

    # B: Regional stiffness.
    B = np.ones(N)
    # Q: Instability drive.
    Q = np.ones(N) * 0.1

    # Regions
    thoracic_idx = (z > 0.4) & (z < 0.8) # T5-T12 approx
    tl_junction_idx = (z >= 0.3) & (z <= 0.4) # T11-L1
    lumbar_idx = (z > 0.1) & (z < 0.3) # L1-L5
    upper_thoracic_idx = (z >= 0.8) & (z < 0.95) # T1-T4

    # Default parameters for baseline spine
    # Stiffness EI
    B[thoracic_idx] *= 1.5 # rib cage buttressing
    B[tl_junction_idx] *= 0.8 # Thoracolumbar vulnerability (31.1% reduction context)

    # Structural modifiers
    tau_profile = np.ones(N)  # Proprioceptive delay tau
    b_profile = np.ones(N)    # Local damping b

    # Asymmetric loading (cardiac offset, aortic pulsation, handedness)
    load_profile = np.sin(np.pi * z) + 0.5 * np.sin(2 * np.pi * z)
    load_profile = np.maximum(load_profile, 0.1)

    if lenke_type == 1:
        # Type 1: Main Thoracic
        load_profile[thoracic_idx] *= 1.2
        b_profile[thoracic_idx] *= 0.8
    elif lenke_type == 2:
        # Type 2: Double Thoracic
        load_profile[upper_thoracic_idx] *= 1.5
        load_profile[thoracic_idx] *= 1.2
        B[upper_thoracic_idx] *= 0.7
    elif lenke_type == 3:
        # Type 3: Double Major (Thoracic + Lumbar)
        load_profile[thoracic_idx] *= 1.2
        load_profile[lumbar_idx] *= 1.3
        tau_profile[lumbar_idx] *= 1.2
    elif lenke_type == 4:
        # Type 4: Triple Major
        load_profile[upper_thoracic_idx] *= 1.3
        load_profile[thoracic_idx] *= 1.2
        load_profile[lumbar_idx] *= 1.2
        B[upper_thoracic_idx] *= 0.8
    elif lenke_type == 5:
        # Type 5: Thoracolumbar/Lumbar
        load_profile[tl_junction_idx] *= 1.5
        b_profile[tl_junction_idx] *= 0.7
        tau_profile[tl_junction_idx] *= 1.3
    elif lenke_type == 6:
        # Type 6: Thoracolumbar/Lumbar - Main Thoracic
        load_profile[tl_junction_idx] *= 1.4
        load_profile[thoracic_idx] *= 1.1
        b_profile[tl_junction_idx] *= 0.75
        tau_profile[thoracic_idx] *= 1.2

    # Combine structural modifiers into instability drive Q
    # Higher load, higher delay (tau), lower damping (b) -> higher Q
    Q = load_profile * tau_profile / b_profile
    Q = np.maximum(Q, 0.1)

    return B, Q


def solve_buckling_eigenmodes(B, Q, N=100):
    """
    Simplified generalized eigenvalue problem for multi-segment Cosserat rod
    (B y'')'' = lambda Q y
    """
    z = np.linspace(0, 1, N)
    dz = z[1] - z[0]

    # Construct finite difference matrices (simplified)
    # 2nd derivative matrix D2 for y''
    D2 = np.diag(-2 * np.ones(N)) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    D2 = D2 / (dz**2)

    # Apply B to D4 (approximate)
    B_matrix = np.diag(B)
    L_matrix = np.dot(D2, np.dot(B_matrix, D2))

    # Apply Boundary conditions (Clamped at z=0: y(0)=0, y'(0)=0)
    # For a realistic spine, boundaries are clamped at sacrum, free at head
    L_matrix = L_matrix[2:-2, 2:-2]
    Q_matrix = np.diag(Q)[2:-2, 2:-2]

    # Solve generalized eigenvalue problem: L y = lambda Q y
    eigenvalues, eigenvectors = eigh(L_matrix, Q_matrix)

    # Sort by eigenvalue (lowest buckling load)
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    return z, eigenvalues, eigenvectors


def main():
    os.makedirs('outputs/experiments', exist_ok=True)
    os.makedirs('research/figures', exist_ok=True)

    N = 100
    z = np.linspace(0, 1, N)
    all_modes = {'Normalized_Position': z}

    plt.figure(figsize=(12, 8))

    for lenke_type in range(1, 7):
        B, Q = get_lenke_parameters(lenke_type, N)
        _, evals, evecs = solve_buckling_eigenmodes(B, Q, N)

        # Take the dominant mode (lowest eigenvalue)
        dominant_mode = np.zeros(N)
        dominant_mode[2:-2] = evecs[:, 0]
        # Normalize
        if np.max(np.abs(dominant_mode)) > 0:
            dominant_mode = dominant_mode / np.max(np.abs(dominant_mode))

        # Ensure consistent sign (e.g., maximum deflection is positive)
        if np.abs(np.min(dominant_mode)) > np.max(dominant_mode):
            dominant_mode = -dominant_mode

        all_modes[f'Type_{lenke_type}'] = dominant_mode
        all_modes[f'Type_{lenke_type}_B'] = B
        all_modes[f'Type_{lenke_type}_Q'] = Q

        plt.plot(z, dominant_mode, label=f'Lenke Type {lenke_type}')

    modes_df = pd.DataFrame(all_modes)
    modes_df.to_csv('outputs/experiments/lenke_six_types.csv', index=False)
    print("Saved outputs/experiments/lenke_six_types.csv")

    plt.title('Multi-segment Cosserat Rod Dominant Buckling Modes (Lenke Types 1-6)')
    plt.xlabel('Normalized Position (Sacrum to T1)')
    plt.ylabel('Amplitude / Normalized Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('research/figures/lenke_six_types.png')
    print("Saved research/figures/lenke_six_types.png")

if __name__ == '__main__':
    main()
