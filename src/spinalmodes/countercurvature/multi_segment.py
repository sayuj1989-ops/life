import numpy as np
from scipy.linalg import eigh

def get_lenke_profiles(N=100):
    """
    Returns regional parameter profiles B (stiffness) and Q (instability drive)
    for different Lenke curve types (1-6) along the spine z from 0 (sacrum) to 1 (T1).
    """
    z = np.linspace(0, 1, N)

    # Regional masks
    lumbar_idx = (z >= 0.0) & (z < 0.3)      # L5-L1
    tl_junction_idx = (z >= 0.3) & (z < 0.4) # T12-T11
    thoracic_idx = (z >= 0.4) & (z < 0.8)    # T10-T2
    proximal_t_idx = (z >= 0.8) & (z <= 1.0) # T1-C

    profiles = {}

    for l_type in range(1, 7):
        B = np.ones(N) * 1.0
        Q = np.ones(N) * 0.1

        # Base regional stiffness differences
        B[thoracic_idx] *= 1.5
        B[tl_junction_idx] *= 0.689
        B[lumbar_idx] *= 1.2

        if l_type == 1:
            Q[thoracic_idx] *= 5.0
        elif l_type == 2:
            Q[thoracic_idx] *= 4.0
            Q[proximal_t_idx] *= 4.0
        elif l_type == 3:
            Q[thoracic_idx] *= 4.0
            Q[lumbar_idx] *= 4.0
        elif l_type == 4:
            Q[proximal_t_idx] *= 3.0
            Q[thoracic_idx] *= 3.0
            Q[lumbar_idx] *= 3.0
        elif l_type == 5:
            Q[tl_junction_idx] *= 6.0
            Q[lumbar_idx] *= 3.0
        elif l_type == 6:
            Q[thoracic_idx] *= 2.5
            Q[tl_junction_idx] *= 5.0
            Q[lumbar_idx] *= 5.0

        # Smooth profiles
        B = np.convolve(B, np.ones(5)/5, mode='same')
        Q = np.convolve(Q, np.ones(5)/5, mode='same')

        profiles[f'Lenke_Type_{l_type}'] = (B, Q)

    return z, profiles

def solve_buckling_eigenmodes(B, Q, N=100):
    """
    Solves generalized eigenvalue problem for multi-segment Cosserat rod
    (B y'')'' = lambda Q y
    """
    z = np.linspace(0, 1, N)
    dz = z[1] - z[0]

    D2 = np.diag(-2 * np.ones(N)) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    D2 = D2 / (dz**2)

    B_matrix = np.diag(B)
    L_matrix = np.dot(D2, np.dot(B_matrix, D2))

    L_matrix = L_matrix[2:-2, 2:-2]
    Q_matrix = np.diag(Q)[2:-2, 2:-2]

    eigenvalues, eigenvectors = eigh(L_matrix, Q_matrix)

    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    return eigenvalues[0], eigenvectors[:, 0]
