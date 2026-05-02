import numpy as np
from scipy.linalg import eigh

def solve_multi_segment_cosserat_buckling(N=100, lenke_type=1):
    """
    Solves the generalized 1D buckling eigenvalue problem for a multi-segment Cosserat rod:
    (B y'')'' = lambda Q y

    This maps polygenic-driven global instability (the generalized Energy Deficit Window)
    into specific structural manifestations (Lenke Types 1-6) based on regional parameters.

    Parameters:
    -----------
    N : int
        Number of spatial discretization points along the rod.
    lenke_type : int
        Lenke curve type (1-6) to simulate.

    Returns:
    --------
    z : np.ndarray
        Normalized spatial position array (0 to 1).
    evals : float
        The lowest eigenvalue (critical buckling load).
    evec : np.ndarray
        The dominant buckling eigenmode (structural shape).
    B : np.ndarray
        Regional stiffness profile.
    Q : np.ndarray
        Regional instability drive profile.
    """
    # Normalized spine length (0 = sacrum, 1 = T1/C7)
    z = np.linspace(0, 1, N)
    dz = z[1] - z[0]

    # Baseline parameters
    B = np.ones(N) * 1.0  # Regional stiffness (EI)
    Q = np.ones(N) * 0.1  # Regional instability drive (from time delay, damping, etc.)

    # Regionalization masks
    lumbar_idx = (z >= 0.0) & (z < 0.3)
    tl_junction_idx = (z >= 0.3) & (z < 0.4)
    thoracic_idx = (z >= 0.4) & (z < 0.8)
    proximal_t_idx = (z >= 0.8) & (z <= 1.0)

    # Apply structural stiffness modifiers (rib cage buttressing, lumbar bulk)
    B[thoracic_idx] *= 1.5
    B[tl_junction_idx] *= 0.689
    B[lumbar_idx] *= 1.2

    # Modulate instability drive Q based on the specified Lenke type
    # Q maps to parameter-driven instability (increased delay tau, reduced damping b)
    if lenke_type == 1:
        # Main Thoracic
        Q[thoracic_idx] *= 5.0
    elif lenke_type == 2:
        # Double Thoracic
        Q[thoracic_idx] *= 4.0
        Q[proximal_t_idx] *= 4.0
    elif lenke_type == 3:
        # Double Major
        Q[thoracic_idx] *= 4.0
        Q[lumbar_idx] *= 4.0
    elif lenke_type == 4:
        # Triple Major
        Q[proximal_t_idx] *= 3.0
        Q[thoracic_idx] *= 3.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 5:
        # Thoracolumbar/Lumbar
        Q[tl_junction_idx] *= 6.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 6:
        # Thoracolumbar/Lumbar - Main Thoracic
        Q[thoracic_idx] *= 2.5
        Q[tl_junction_idx] *= 5.0
        Q[lumbar_idx] *= 5.0

    # Smooth the regional transitions
    B = np.convolve(B, np.ones(5)/5, mode='same')
    Q = np.convolve(Q, np.ones(5)/5, mode='same')

    # Construct finite difference matrices for the clamped-free buckling problem
    # D2 is the second derivative operator
    D2 = np.diag(-2 * np.ones(N)) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    D2 = D2 / (dz**2)

    B_matrix = np.diag(B)

    # L = D^2(B D^2 y)
    L_matrix = np.dot(D2, np.dot(B_matrix, D2))

    # Apply Boundary Conditions (Clamped at z=0: y(0)=0, y'(0)=0)
    # Remove the first two rows and columns to enforce these conditions
    L_matrix_int = L_matrix[2:-2, 2:-2]
    Q_matrix_int = np.diag(Q)[2:-2, 2:-2]

    # Solve generalized eigenvalue problem: L y = lambda Q y
    eigenvalues, eigenvectors = eigh(L_matrix_int, Q_matrix_int)

    # Sort and extract the lowest buckling mode (fundamental eigenmode)
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    evec_full = np.zeros(N)
    evec_full[2:-2] = eigenvectors[:, 0]

    # Normalize structural deviation
    evec_full = evec_full / np.max(np.abs(evec_full))

    # Ensure consistent sign convention for visual alignment
    if np.sum(evec_full) < 0:
        evec_full = -evec_full

    return z, eigenvalues[0], evec_full, B, Q
