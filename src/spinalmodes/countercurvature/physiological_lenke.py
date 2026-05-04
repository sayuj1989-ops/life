import numpy as np
from scipy.linalg import eigh

def solve_physiological_lenke_buckling(N=100, lenke_type=1, baseline=True):
    z = np.linspace(0, 1, N)
    dz = z[1] - z[0]

    # Baseline vs Polygenic Stacking parameters
    b_base = 1.0 if baseline else 0.71
    tau_base = 70.0 if baseline else 96.4
    Kd_base = 10.0 if baseline else 12.96
    mgL_base = 73.6 if baseline else 93.7

    # Regional structural stiffness variations (EI)
    EI = np.ones(N) * 1.0
    lumbar_idx = (z >= 0.0) & (z < 0.3)
    tl_junction_idx = (z >= 0.3) & (z < 0.4)
    thoracic_idx = (z >= 0.4) & (z < 0.8)
    proximal_t_idx = (z >= 0.8) & (z <= 1.0)

    EI[thoracic_idx] *= 1.5
    EI[tl_junction_idx] *= 0.689
    EI[lumbar_idx] *= 1.2

    # Regional physiological variations for Q(z) = f(tau, b, mgL, Kd)
    tau_z = np.ones(N) * tau_base
    b_z = np.ones(N) * b_base
    F_asym = np.ones(N) * 1.0

    # Pattern specific modulations to trigger Lenke morphologies
    if lenke_type == 1:
        b_z[thoracic_idx] *= 0.5
        F_asym[thoracic_idx] *= 2.0
    elif lenke_type == 2:
        b_z[thoracic_idx] *= 0.6
        b_z[proximal_t_idx] *= 0.6
        F_asym[thoracic_idx] *= 1.5
        F_asym[proximal_t_idx] *= 1.5
    elif lenke_type == 3:
        b_z[thoracic_idx] *= 0.6
        b_z[lumbar_idx] *= 0.6
        F_asym[thoracic_idx] *= 1.5
        F_asym[lumbar_idx] *= 1.5
    elif lenke_type == 4:
        b_z[proximal_t_idx] *= 0.7
        b_z[thoracic_idx] *= 0.7
        b_z[lumbar_idx] *= 0.7
        F_asym[proximal_t_idx] *= 1.3
        F_asym[thoracic_idx] *= 1.3
        F_asym[lumbar_idx] *= 1.3
    elif lenke_type == 5:
        b_z[tl_junction_idx] *= 0.4
        b_z[lumbar_idx] *= 0.6
        F_asym[tl_junction_idx] *= 2.5
    elif lenke_type == 6:
        b_z[thoracic_idx] *= 0.8
        b_z[tl_junction_idx] *= 0.5
        b_z[lumbar_idx] *= 0.5
        F_asym[tl_junction_idx] *= 2.0
        F_asym[lumbar_idx] *= 2.0

    # Formulate effective destabilizing drive Q(z)
    # Q combines the effects of delay, damping, and load in a unified framework
    Q_z = (tau_z / 70.0) * (1.0 / b_z) * (mgL_base / 73.6) * (Kd_base / 10.0) * F_asym

    # Smooth the profiles
    EI = np.convolve(EI, np.ones(5)/5, mode='same')
    Q_z = np.convolve(Q_z, np.ones(5)/5, mode='same')

    # Construct finite difference matrices
    D2 = np.diag(-2 * np.ones(N)) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    D2 = D2 / (dz**2)

    EI_matrix = np.diag(EI)
    L_matrix = np.dot(D2, np.dot(EI_matrix, D2))

    # Apply Boundary conditions (Clamped at z=0)
    L_matrix = L_matrix[2:-2, 2:-2]
    Q_matrix = np.diag(Q_z)[2:-2, 2:-2]

    eigenvalues, eigenvectors = eigh(L_matrix, Q_matrix)

    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    return z, eigenvalues[0], eigenvectors[:, 0], EI, Q_z
