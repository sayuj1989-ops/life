import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigs

def solve_multi_segment_cosserat_buckling(B_func, Q_func, n_points=100):
    """
    Solves the 1D buckling eigenvalue problem (B y'')'' = \\lambda Q y
    for a multi-segment Cosserat rod model of the spine.
    """
    z = np.linspace(0, 1, n_points)
    dz = z[1] - z[0]

    B = B_func(z)
    Q = Q_func(z)

    # Finite difference matrix for D2 = d^2/dz^2
    diagonals = [np.ones(n_points-1), -2*np.ones(n_points), np.ones(n_points-1)]
    D2 = sp.diags(diagonals, [-1, 0, 1], format='csr') / (dz**2)

    # Boundary conditions: pinned-pinned (y=0, y''=0 at ends)
    # We will just solve for the interior points 1 to n_points-2
    n_interior = n_points - 2
    D2_int = D2[1:-1, 1:-1]

    # B matrix
    B_int = sp.diags([B[1:-1]], [0], format='csr')

    # Operator A = D2 * B * D2
    A_int = D2_int.dot(B_int).dot(D2_int)

    # M matrix
    M_int = sp.diags([Q[1:-1]], [0], format='csr')

    # Solve generalized eigenvalue problem A y = \lambda M y
    # Try to find the smallest magnitude eigenvalues
    try:
        vals, vecs = eigs(A_int, k=3, M=M_int, which='SM')
    except:
        # Fallback if eigs fails
        import scipy.linalg as la
        A_dense = A_int.toarray()
        M_dense = M_int.toarray()
        vals, vecs = la.eig(A_dense, M_dense)
        idx = np.argsort(np.abs(vals))
        vals = vals[idx[:3]]
        vecs = vecs[:, idx[:3]]

    eigenvalues = np.real(vals)
    eigenmodes_int = np.real(vecs)

    # Add boundary points back
    eigenmodes = np.zeros((n_points, eigenmodes_int.shape[1]))
    eigenmodes[1:-1, :] = eigenmodes_int

    # Normalize eigenmodes
    for i in range(eigenmodes.shape[1]):
        max_idx = np.argmax(np.abs(eigenmodes[:, i]))
        eigenmodes[:, i] /= eigenmodes[max_idx, i]

    # Sort by eigenvalue
    idx = np.argsort(eigenvalues)
    return eigenvalues[idx], eigenmodes[:, idx], z
