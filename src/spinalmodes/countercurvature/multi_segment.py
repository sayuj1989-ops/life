import numpy as np
from scipy.linalg import eigh

def solve_multi_segment_cosserat_buckling(N=100, lenke_type=1):
    """
    Generalized 1D buckling eigenvalue problem for multi-segment Cosserat rod
    (B y'')'' = lambda Q y

    Models Lenke 1-6 explicitly by modulating regional parameters.
    """
    # z from 0 (sacrum) to 1 (T1)
    z = np.linspace(0, 1, N)
    dz = z[1] - z[0]

    # Base parameters
    B = np.ones(N) * 1.0  # Stiffness
    Q = np.ones(N) * 0.1  # Instability drive

    # Regional masks (approximate normalized spine locations)
    lumbar_idx = (z >= 0.0) & (z < 0.3)      # L5-L1
    tl_junction_idx = (z >= 0.3) & (z < 0.4) # T12-T11
    thoracic_idx = (z >= 0.4) & (z < 0.8)    # T10-T2
    proximal_t_idx = (z >= 0.8) & (z <= 1.0) # T1-C

    # Base regional stiffness differences
    B[thoracic_idx] *= 1.5 # Rib cage buttressing
    B[tl_junction_idx] *= 0.689 # Thoracolumbar vulnerability (31.1% reduction)
    B[lumbar_idx] *= 1.2 # Lumbar lordosis structural bulk

    # We modulate Q based on regional variations in tau, damping b, and asymmetric loading
    # to trigger specific Lenke patterns.
    # Q represents the effective destabilizing drive (Energy Deficit window overlap).

    if lenke_type == 1:
        # Type 1 (Main Thoracic): Minimal paraspinal muscle mass + max moment arm
        Q[thoracic_idx] *= 5.0
    elif lenke_type == 2:
        # Type 2 (Double Thoracic): Proximal thoracic and main thoracic destabilize
        Q[thoracic_idx] *= 4.0
        Q[proximal_t_idx] *= 4.0
    elif lenke_type == 3:
        # Type 3 (Double Major): Thoracic and lumbar simultaneously buckle
        Q[thoracic_idx] *= 4.0
        Q[lumbar_idx] *= 4.0
    elif lenke_type == 4:
        # Type 4 (Triple Major): Proximal thoracic, main thoracic, and lumbar
        Q[proximal_t_idx] *= 3.0
        Q[thoracic_idx] *= 3.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 5:
        # Type 5 (Thoracolumbar/Lumbar): T-L junction vulnerability dominates
        Q[tl_junction_idx] *= 6.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 6:
        # Type 6 (Thoracolumbar/Lumbar-Main Thoracic): Lumbar > Thoracic drive
        Q[thoracic_idx] *= 2.5
        Q[tl_junction_idx] *= 5.0
        Q[lumbar_idx] *= 5.0

    # Smooth the profiles
    B = np.convolve(B, np.ones(5)/5, mode='same')
    Q = np.convolve(Q, np.ones(5)/5, mode='same')

    # Construct finite difference matrices
    D2 = np.diag(-2 * np.ones(N)) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    D2 = D2 / (dz**2)

    B_matrix = np.diag(B)
    L_matrix = np.dot(D2, np.dot(B_matrix, D2))

    # Apply Boundary conditions (Clamped at z=0: y(0)=0, y'(0)=0)
    L_matrix = L_matrix[2:-2, 2:-2]
    Q_matrix = np.diag(Q)[2:-2, 2:-2]

    # Solve generalized eigenvalue problem: L y = lambda Q y
    eigenvalues, eigenvectors = eigh(L_matrix, Q_matrix)

    # Get lowest buckling mode (first eigenvector)
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    return z, eigenvalues[0], eigenvectors[:, 0], B, Q
