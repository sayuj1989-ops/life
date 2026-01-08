"""Lightweight Euler–Bernoulli beam utilities for validation and IEC demos."""

from __future__ import annotations

import numpy as np


def integrate_shape_from_curvature(s: np.ndarray, kappa: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Integrate curvature to angle and centerline in the small-slopes regime.

    θ'(s) = κ(s); x'(s) = cos θ; y'(s) = sin θ with x(0)=0, y(0)=0, θ(0)=0.
    """
    ds = np.gradient(s)
    theta = np.cumsum(kappa * ds)
    x = np.cumsum(np.cos(theta) * ds)
    y = np.cumsum(np.sin(theta) * ds)
    # enforce clamped base at the origin
    x -= x[0]
    y -= y[0]
    return x, y


def analytic_sinusoid(s: np.ndarray, A: float, k: float) -> np.ndarray:
    """Analytic small-slope solution y(s) = A sin(ks)."""
    return A * np.sin(k * s)


def l2_error(a: np.ndarray, b: np.ndarray) -> float:
    """L2 error between two arrays."""
    return float(np.sqrt(np.mean((a - b) ** 2)))

