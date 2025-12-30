"""Core dataclasses and helpers for the Information–Elasticity Coupling model."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True, slots=True)
class Params:
    L: float = 1.0  # beam length (m)
    n: int = 801  # grid points
    chi_k: float = 0.0  # IEC-1: phase drift via dI/ds
    chi_E: float = 0.0  # IEC-2: amplitude/material scaling (applied in solver)
    g: float = 0.0  # gravitational load proxy
    seed: int = 1337


@dataclass(slots=True)
class State:
    s: np.ndarray  # arc-length grid [0..L]
    kappa0: np.ndarray  # baseline curvature κ0(s)
    I: np.ndarray | None = None  # information field I(s)
    E: np.ndarray | None = None  # local stiffness (optional)


def uniform_grid(L: float, n: int) -> np.ndarray:
    """Uniform grid on [0, L]."""
    return np.linspace(0.0, L, n, dtype=float)


def iec_kappa_target(st: State, p: Params) -> np.ndarray:
    """
    IEC target curvature: κ_target(s) = κ0(s) + χ_k * dI/ds.

    IEC-2 (χ_E) is applied in solver/load amplitude rather than adding a second derivative term here.
    """
    kappa = np.copy(st.kappa0)
    if st.I is not None and p.chi_k != 0.0:
        dIds = np.gradient(st.I, st.s, edge_order=2)
        kappa += p.chi_k * dIds
    return kappa

