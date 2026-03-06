import numpy as np


def build_matrix(N, L, T, EI, active_factor=0.0):
    T_eff = T * (1 - active_factor)
    h = L / (N + 1)
    M = np.zeros((N, N), dtype=complex)
    for j in range(N):
        M[j, j] += EI * 6 / h**4
        if j - 1 >= 0:
            M[j, j-1] += EI * (-4) / h**4 - 1j * T_eff * 2 / (2*h**3)
        if j + 1 < N:
            M[j, j+1] += EI * (-4) / h**4 - 1j * T_eff * (-2) / (2*h**3)
        if j - 2 >= 0:
            M[j, j-2] += EI * 1 / h**4 - 1j * T_eff * (-1) / (2*h**3)
        else:
            if j == 0:
                M[j, 0] -= (EI * 1 / h**4 - 1j * T_eff * (-1) / (2*h**3))
        if j + 2 < N:
            M[j, j+2] += EI * 1 / h**4 - 1j * T_eff * 1 / (2*h**3)
        else:
            if j == N - 1:
                M[j, N-1] -= (EI * 1 / h**4 - 1j * T_eff * 1 / (2*h**3))
    return M

def find_T_crit(N, L, EI, active_factor=0.0):
    T_vals = np.linspace(5.0, 15.0, 500)
    min_svs = []
    for T in T_vals:
        M = build_matrix(N, L, T, EI, active_factor)
        s = np.linalg.svd(M, compute_uv=False)
        min_svs.append(np.min(s))
    idx = np.argmin(min_svs)
    return T_vals[idx]

N = 40
EI = 1.0
L = 1.0
T_crit = find_T_crit(N, L, EI, 0.0)
print(f"Numerical: {T_crit}, Analytical: {2*np.pi*EI/L}")
