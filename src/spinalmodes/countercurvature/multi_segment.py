import numpy as np
from scipy.linalg import eigh

def solve_multi_segment_cosserat_buckling(N=100, lenke_type=1):
    """
    Solves the generalized 1D buckling eigenvalue problem for a multi-segment Cosserat rod.
    (B y'')'' = lambda Q y

    Regionalized to predict Lenke curve types 1-6.
    z from 0 (sacrum) to 1 (T1)
    - Lumbar: 0.0 - 0.3
    - Thoracolumbar junction: 0.3 - 0.4
    - Thoracic: 0.4 - 0.8
    - Proximal Thoracic: 0.8 - 1.0
    """
    z = np.linspace(0, 1, N)
    dz = z[1] - z[0]

    # Base parameters
    B = np.ones(N) * 1.0  # Stiffness
    Q = np.ones(N) * 0.1  # Instability drive

    # Regional masks
    lumbar_idx = (z >= 0.0) & (z < 0.3)
    tl_junction_idx = (z >= 0.3) & (z < 0.4)
    thoracic_idx = (z >= 0.4) & (z < 0.8)
    proximal_t_idx = (z >= 0.8) & (z <= 1.0)

    # Base regional stiffness differences
    B[thoracic_idx] *= 1.5      # Rib cage buttressing
    B[tl_junction_idx] *= 0.689 # Thoracolumbar vulnerability
    B[lumbar_idx] *= 1.2        # Lumbar lordosis structural bulk

    # Modulate Q to trigger specific Lenke patterns
    if lenke_type == 1:
        Q[thoracic_idx] *= 5.0
    elif lenke_type == 2:
        Q[thoracic_idx] *= 4.0
        Q[proximal_t_idx] *= 4.0
    elif lenke_type == 3:
        Q[thoracic_idx] *= 4.0
        Q[lumbar_idx] *= 4.0
    elif lenke_type == 4:
        Q[proximal_t_idx] *= 3.0
        Q[thoracic_idx] *= 3.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 5:
        Q[tl_junction_idx] *= 6.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 6:
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
