import numpy as np
from scipy.linalg import eigh

def compute_regional_masks(N=100):
    """
    Returns boolean masks for the normalized spine length (z from 0 to 1) regionalized into:
    lumbar (0.0-0.3)
    thoracolumbar junction (0.3-0.4)
    thoracic (0.4-0.8)
    proximal thoracic (0.8-1.0)
    """
    z = np.linspace(0, 1, N)
    masks = {
        'lumbar': (z >= 0.0) & (z < 0.3),
        'tl_junction': (z >= 0.3) & (z < 0.4),
        'thoracic': (z >= 0.4) & (z < 0.8),
        'proximal_t': (z >= 0.8) & (z <= 1.0)
    }
    return z, masks

def generate_parameter_profiles(z, masks, lenke_type=1):
    """
    Generates regional parameter profiles for Stiffness (B) and Instability Drive (Q)
    based on the Lenke curve type.
    """
    N = len(z)

    # Base parameters
    B = np.ones(N) * 1.0  # Stiffness
    Q = np.ones(N) * 0.1  # Instability drive

    # Masks
    lumbar_idx = masks['lumbar']
    tl_junction_idx = masks['tl_junction']
    thoracic_idx = masks['thoracic']
    proximal_t_idx = masks['proximal_t']

    # Base regional stiffness differences
    B[thoracic_idx] *= 1.5      # Rib cage buttressing
    B[tl_junction_idx] *= 0.689 # Thoracolumbar vulnerability (31.1% reduction)
    B[lumbar_idx] *= 1.2        # Lumbar lordosis structural bulk

    if lenke_type == 1:
        # Type 1 (Main Thoracic)
        Q[thoracic_idx] *= 5.0
    elif lenke_type == 2:
        # Type 2 (Double Thoracic)
        Q[thoracic_idx] *= 4.0
        Q[proximal_t_idx] *= 4.0
    elif lenke_type == 3:
        # Type 3 (Double Major)
        Q[thoracic_idx] *= 4.0
        Q[lumbar_idx] *= 4.0
    elif lenke_type == 4:
        # Type 4 (Triple Major)
        Q[proximal_t_idx] *= 3.0
        Q[thoracic_idx] *= 3.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 5:
        # Type 5 (Thoracolumbar/Lumbar)
        Q[tl_junction_idx] *= 6.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 6:
        # Type 6 (Thoracolumbar/Lumbar - Main Thoracic)
        Q[thoracic_idx] *= 2.5
        Q[tl_junction_idx] *= 5.0
        Q[lumbar_idx] *= 5.0

    # Smooth profiles to avoid sharp numerical gradients
    B = np.convolve(B, np.ones(5)/5, mode='same')
    Q = np.convolve(Q, np.ones(5)/5, mode='same')

    return B, Q

def solve_multi_segment_eigenmode(N=100, lenke_type=1):
    r"""
    Solves the generalized 1D buckling eigenvalue problem (B y'')'' = \lambda Q y
    for the multi-segment Cosserat rod extension.
    """
    z, masks = compute_regional_masks(N)
    B, Q = generate_parameter_profiles(z, masks, lenke_type)

    dz = z[1] - z[0]

    # Finite difference matrices
    D2 = np.diag(-2 * np.ones(N)) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    D2 = D2 / (dz**2)

    B_matrix = np.diag(B)
    L_matrix = np.dot(D2, np.dot(B_matrix, D2))

    # Apply clamped boundary conditions at z=0 (sacrum)
    L_matrix = L_matrix[2:-2, 2:-2]
    Q_matrix = np.diag(Q)[2:-2, 2:-2]

    # Solve generalized eigenvalue problem
    eigenvalues, eigenvectors = eigh(L_matrix, Q_matrix)

    # Extract lowest buckling mode
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    lowest_eigenvalue = eigenvalues[0]
    lowest_eigenvector = eigenvectors[:, 0]

    # Pad to original size (due to BCs)
    full_mode = np.zeros(N)
    full_mode[2:-2] = lowest_eigenvector

    # Normalize amplitude
    if np.max(np.abs(full_mode)) > 0:
        full_mode = full_mode / np.max(np.abs(full_mode))

    # Standardize direction
    if np.sum(full_mode) < 0:
        full_mode = -full_mode

    return z, lowest_eigenvalue, full_mode, B, Q
