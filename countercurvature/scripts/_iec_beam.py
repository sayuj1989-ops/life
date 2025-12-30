from __future__ import annotations

from dataclasses import asdict
from typing import Any

import numpy as np

from ._config import BCCConfig


def info_field(s: np.ndarray, cfg: BCCConfig) -> np.ndarray:
    """Phenomenological HOX-like field with cervical + lumbar peaks and thoracic dip."""
    ip = cfg.iec.info_profile
    g1 = np.exp(-0.5 * ((s - ip.cervical_center) / ip.sigma) ** 2)
    g2 = np.exp(-0.5 * ((s - ip.lumbar_center) / ip.sigma) ** 2)
    thor = np.exp(-0.5 * ((s - ip.thoracic_center) / ip.thoracic_sigma) ** 2)
    I = g1 + g2 - ip.thoracic_depth * thor
    I = (I - I.min()) / (I.max() - I.min() + 1e-12)
    return I


def gamma_field(I: np.ndarray, cfg: BCCConfig) -> np.ndarray:
    return 1.0 + cfg.iec.chi_g * I


def geff_field(gamma: np.ndarray) -> np.ndarray:
    return gamma**2


def intrinsic_curvature(s: np.ndarray, I: np.ndarray, cfg: BCCConfig) -> np.ndarray:
    dIds = np.gradient(I, s)
    return cfg.iec.chi_kappa * dIds


def _d2_matrix(n: int, h: float) -> np.ndarray:
    D2 = np.zeros((n, n), dtype=float)
    for i in range(1, n - 1):
        D2[i, i - 1] = 1.0
        D2[i, i] = -2.0
        D2[i, i + 1] = 1.0
    return D2 / (h * h)


def solve_equilibrium_beam(s: np.ndarray, q: np.ndarray, B: np.ndarray, kappa0: np.ndarray) -> dict[str, Any]:
    """
    Linear Euler–Bernoulli surrogate:
      minimize  0.5 ∫ B (y''-kappa0)^2 ds + ∫ q y ds
    with clamped-free BC.
    """
    n = len(s)
    h = float(s[1] - s[0])

    D2 = _d2_matrix(n, h)
    W = np.diag(B)
    K = D2.T @ W @ D2
    f_k0 = D2.T @ (B * kappa0)
    f_q = q

    A = K.copy()
    b = (f_k0 - f_q).copy()

    # y(0)=0
    A[0, :] = 0.0
    A[0, 0] = 1.0
    b[0] = 0.0
    # y'(0)=0
    A[1, :] = 0.0
    A[1, 0] = -3.0 / (2.0 * h)
    A[1, 1] = 4.0 / (2.0 * h)
    A[1, 2] = -1.0 / (2.0 * h)
    b[1] = 0.0

    # y''(L)=kappa0(L)
    A[-2, :] = 0.0
    A[-2, -3] = 1.0 / (h * h)
    A[-2, -2] = -2.0 / (h * h)
    A[-2, -1] = 1.0 / (h * h)
    b[-2] = float(kappa0[-1])

    # y'''(L)=kappa0'(L) proxy
    dk0 = np.gradient(kappa0, s)
    A[-1, :] = 0.0
    A[-1, -4] = 1.0 / (h**3)
    A[-1, -3] = -3.0 / (h**3)
    A[-1, -2] = 3.0 / (h**3)
    A[-1, -1] = -1.0 / (h**3)
    b[-1] = float(dk0[-1])

    y = np.linalg.solve(A, b)
    kappa = D2 @ y
    kappa[0] = kappa[1]
    kappa[-1] = float(kappa0[-1])
    return {"y": y, "kappa": kappa}


def compute_metrics(
    s: np.ndarray,
    y: np.ndarray,
    kappa: np.ndarray,
    kappa0: np.ndarray,
    B: np.ndarray,
    q: np.ndarray,
    geff: np.ndarray,
    passive_kappa: np.ndarray,
) -> dict[str, float]:
    ds = float(s[1] - s[0])

    E_bend = 0.5 * float(np.sum(B * (kappa - kappa0) ** 2) * ds)
    E_stretch = 0.0
    E_shear = 0.0
    E_grav = float(np.sum(q * y) * ds)
    E_total = E_bend + E_stretch + E_shear + E_grav

    signs = np.sign(kappa)
    signs[np.abs(kappa) < 1e-8] = 0.0
    for i in range(1, len(signs)):
        if signs[i] == 0.0:
            signs[i] = signs[i - 1]
    inflections = int(np.sum(signs[1:] * signs[:-1] < 0))

    D_geo_sq = float(np.sum(geff * (kappa - passive_kappa) ** 2) * ds)
    denom = float(np.sqrt(np.sum(geff * passive_kappa**2) * ds) + 1e-12)
    D_geo_hat = float(np.sqrt(D_geo_sq) / denom)

    A_pos = float(np.sum(np.clip(kappa, 0.0, None)) * ds)
    A_neg = float(np.sum(np.clip(-kappa, 0.0, None)) * ds)
    mode_score = float(1.0 - abs(A_pos - A_neg) / (A_pos + A_neg + 1e-12))

    return {
        "E_total": E_total,
        "E_bend": E_bend,
        "E_shear": E_shear,
        "E_stretch": E_stretch,
        "E_grav": E_grav,
        "curv_mean": float(np.mean(kappa)),
        "curv_std": float(np.std(kappa)),
        "curv_min": float(np.min(kappa)),
        "curv_max": float(np.max(kappa)),
        "curv_abs_max": float(np.max(np.abs(kappa))),
        "D_geo_hat": D_geo_hat,
        "mode_score": mode_score,
        "tip_deflection": float(y[-1]),
        "tip_slope": float(np.gradient(y, s)[-1]),
        "inflection_count": float(inflections),
    }


def run_single(cfg: BCCConfig, gravity: float | None = None, chi_kappa: float | None = None) -> dict[str, Any]:
    n = cfg.simulation.n_nodes
    L = cfg.simulation.length
    s = np.linspace(0.0, L, n)

    g = float(cfg.simulation.gravity if gravity is None else gravity)
    chi_k = float(cfg.iec.chi_kappa if chi_kappa is None else chi_kappa)

    I = info_field(s, cfg)
    kappa0 = chi_k * np.gradient(I, s)
    gamma = gamma_field(I, cfg)
    geff = geff_field(gamma)

    B = cfg.material.B0 * (1.0 + cfg.iec.chi_E * I)
    q = cfg.material.rhoA * g * np.ones_like(s)

    passive = solve_equilibrium_beam(s, q=q, B=B, kappa0=np.zeros_like(kappa0))
    info = solve_equilibrium_beam(s, q=q, B=B, kappa0=kappa0)

    metrics = compute_metrics(
        s=s,
        y=info["y"],
        kappa=info["kappa"],
        kappa0=kappa0,
        B=B,
        q=q,
        geff=geff,
        passive_kappa=passive["kappa"],
    )

    row: dict[str, Any] = {
        "gravity": g,
        "chi_kappa": chi_k,
        "n_nodes": int(n),
        "length": float(L),
        "B0": float(cfg.material.B0),
        "rhoA": float(cfg.material.rhoA),
        "chi_g": float(cfg.iec.chi_g),
        "chi_E": float(cfg.iec.chi_E),
        **metrics,
    }

    return {
        "row": row,
        "fields": {
            "s": s,
            "I": I,
            "gamma": gamma,
            "g_eff": geff,
            "kappa0": kappa0,
            "y_passive": passive["y"],
            "kappa_passive": passive["kappa"],
            "y_info": info["y"],
            "kappa_info": info["kappa"],
        },
        "config": asdict(cfg),
    }


