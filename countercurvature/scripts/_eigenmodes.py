from __future__ import annotations

import numpy as np


def _d2(n: int, h: float) -> np.ndarray:
    D2 = np.zeros((n, n), dtype=float)
    for i in range(1, n - 1):
        D2[i, i - 1] = 1.0
        D2[i, i] = -2.0
        D2[i, i + 1] = 1.0
    return D2 / (h * h)


def beam_stiffness_matrix(B: np.ndarray, s: np.ndarray) -> np.ndarray:
    """
    Euler–Bernoulli stiffness operator K ≈ D2^T * diag(B) * D2 with clamped-free BC
    enforced by strong constraints for y(0)=0 and y'(0)=0.
    """
    n = len(s)
    h = float(s[1] - s[0])
    D2 = _d2(n, h)
    W = np.diag(B)
    K = D2.T @ W @ D2

    Kc = K.copy()
    # Strongly constrain y(0)=0 and y'(0)=0 (proxy) by locking first 2 DOF.
    for i in (0, 1):
        Kc[i, :] = 0.0
        Kc[:, i] = 0.0
        Kc[i, i] = 1.0
    return Kc


def eigenmodes(B: np.ndarray, s: np.ndarray, n_modes: int = 6) -> dict[str, np.ndarray]:
    """
    Lowest eigenmodes of K y = lambda y (mass ~ I). omega = sqrt(lambda).
    Uses dense eigensolve (fine for n~200).
    """
    K = beam_stiffness_matrix(B=B, s=s)
    w, V = np.linalg.eigh(K)
    idx = np.argsort(w)
    w = w[idx]
    V = V[:, idx]

    mask = w > 1e-8
    w = w[mask]
    V = V[:, mask]

    w = w[:n_modes]
    V = V[:, :n_modes]

    # normalize
    for i in range(V.shape[1]):
        norm = float(np.sqrt(np.trapezoid(V[:, i] ** 2, s)) + 1e-12)
        V[:, i] /= norm

    omega = np.sqrt(np.clip(w, 0.0, None))
    return {"lambda": w, "omega": omega, "modes": V}


