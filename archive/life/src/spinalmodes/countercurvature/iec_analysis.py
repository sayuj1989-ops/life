"""Analytical utilities for IEC energy functionals and stability analysis.

This module fills in the theoretical pieces referenced in the manuscript:

- Eq. (2): an information–elasticity energy that couples genetic gradients
  (∂I/∂s) to mechanical bending and gravity.
- Eq. (4): an eigenproblem for scoliosis-like instabilities, solved via a
  finite-difference beam operator with information-driven potentials.
- Standing-wave analogy: a dispersion relation for S-shaped modes treated
  as standing waves in the effective metric.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from numpy.linalg import eigh

from .coupling import CounterCurvatureParams, compute_effective_stiffness
from .info_fields import InfoField1D

ArrayF64 = NDArray[np.float64]


def information_elasticity_energy(
    info: InfoField1D,
    kappa_profile: ArrayF64,
    *,
    bending_stiffness: float | ArrayF64 | None = None,
    kappa_reference: ArrayF64 | None = None,
    rhoA: float = 1.0,
    gravity: float = 9.81,
    k_info: float = 1.0,
    metric: ArrayF64 | None = None,
) -> dict[str, float]:
    """Compute the IEC energy functional (Eq. 2 style).

    The functional integrates an information-gradient term with gravitational /
    bending energy to quantify when genetic patterning overcomes gravity:

        E = ∫ [½ k_info (∂I/∂s)²
               + ½ ρA g · (κ - κ_ref)²
               + ½ B(s) (κ - κ_ref)² ] ds

    Parameters
    ----------
    info:
        Information field I(s), ∂I/∂s evaluated on the same grid as κ.
    kappa_profile:
        Realized curvature κ(s) (1/m).
    bending_stiffness:
        Optional stiffness B(s)=E·I field (N·m²). If None, uses a unit field.
    kappa_reference:
        Reference curvature κ_ref(s); defaults to zero (flat reference).
    rhoA:
        Linear mass density (kg/m). Couples gravity into the energy.
    gravity:
        Gravitational acceleration (m/s²).
    k_info:
        Coupling strength between genetic gradients and stiffness.
    metric:
        Optional metric weight g_eff(s). If None, uses a flat metric.

    Returns
    -------
    dict
        Components and total energy.
    """
    s = info.s
    if kappa_profile.shape != s.shape:
        raise ValueError("kappa_profile must share the same shape as the information grid.")

    metric_field = np.ones_like(s) if metric is None else np.asarray(metric, dtype=float)
    if metric_field.shape != s.shape:
        raise ValueError("metric must match the shape of the information grid.")

    kappa_ref = np.zeros_like(kappa_profile) if kappa_reference is None else kappa_reference
    if kappa_ref.shape != kappa_profile.shape:
        raise ValueError("kappa_reference must match kappa_profile.")

    if bending_stiffness is None:
        B_field = np.ones_like(s)
    else:
        B_field = np.asarray(bending_stiffness, dtype=float)
        if B_field.shape not in (s.shape, ()):
            raise ValueError("bending_stiffness must be scalar or match the grid shape.")

    delta_kappa = kappa_profile - kappa_ref

    info_energy = 0.5 * k_info * float(np.trapz(info.dIds**2, s))
    gravity_energy = 0.5 * float(np.trapz(metric_field * (rhoA * gravity) * delta_kappa**2, s))
    bending_energy = 0.5 * float(np.trapz(metric_field * B_field * delta_kappa**2, s))

    total = info_energy + gravity_energy + bending_energy
    return {
        "total": total,
        "info_energy": info_energy,
        "gravity_energy": gravity_energy,
        "bending_energy": bending_energy,
    }


def standing_wave_dispersion_relation(
    kappa_profile: ArrayF64,
    info: InfoField1D,
    *,
    rho: float = 1.0,
    beta: float = 1.0,
) -> dict[str, ArrayF64 | float]:
    """Return the standing-wave dispersion relation ω²(s).

    Uses the analog-gravity ansatz:
        ω² = (1/ρ) [ κ(s)² + β (∂I/∂s)² ],
    treating the S-curve as a standing wave in the effective metric.
    """
    if kappa_profile.shape != info.s.shape:
        raise ValueError("kappa_profile must match the information grid.")
    if rho <= 0:
        raise ValueError("Density ρ must be positive.")

    omega_sq = (kappa_profile**2 + beta * info.dIds**2) / float(rho)
    omega = np.sqrt(np.clip(omega_sq, a_min=0.0, a_max=None))
    return {
        "omega_sq": omega_sq,
        "omega": omega,
        "omega_mean": float(np.mean(omega)),
        "omega_peak": float(np.max(omega)),
    }


def solve_countercurvature_eigenproblem(
    info: InfoField1D,
    params: CounterCurvatureParams,
    *,
    E0: float = 1e9,
    I_moment: float = 1e-8,
    rhoA: float = 1.0,
    gravity: float = 9.81,
    n_modes: int = 5,
    metric: ArrayF64 | None = None,
    k_info: float = 1.0,
) -> dict[str, ArrayF64 | float | bool]:
    """Solve the IEC eigenproblem for scoliosis thresholds (Eq. 4 analogue).

    We discretize a clamped-free beam with information-driven stiffness and a
    destabilizing information-gradient potential. Negative eigenvalues flag
    symmetry-breaking instabilities.

    Returns eigenvalues (λ) and eigenmodes (φ) satisfying:
        [ B̄ D⁴ + diag(ρA g_eff) - diag(V_info) ] φ = λ φ

    Parameters
    ----------
    info:
        Information field on a uniform grid.
    params:
        Countercurvature coupling parameters.
    E0:
        Baseline Young's modulus (Pa).
    I_moment:
        Second moment of area (m⁴).
    rhoA:
        Linear mass density (kg/m).
    gravity:
        Gravitational acceleration (m/s²).
    n_modes:
        Number of leading modes to return.
    metric:
        Optional metric weight g_eff(s); defaults to flat.
    k_info:
        Weight on the destabilizing information-gradient potential.
    """
    s = info.s
    if s.ndim != 1 or s.size < 4:
        raise ValueError("Information grid must be 1D with at least 4 points.")
    ds = np.diff(s)
    if np.max(np.abs(ds - ds.mean())) > 1e-8:
        raise ValueError("Eigenproblem assumes a uniform spatial grid.")
    h = float(ds.mean())

    g_eff = np.ones_like(s) if metric is None else metric
    if g_eff.shape != s.shape:
        raise ValueError("metric must match the information grid.")

    # Effective stiffness and destabilizing potential from ∂I/∂s
    E_field = compute_effective_stiffness(info, params, E0, model="linear")
    B_avg = float(np.mean(E_field) * I_moment)
    V_info = k_info * (params.nondimensional_gradient(info.dIds) ** 2)

    # Finite-difference biharmonic operator with clamped-free BC (pinned surrogate)
    n = s.size
    main = -2.0 * np.ones(n)
    off = np.ones(n - 1)
    D2 = (np.diag(main) + np.diag(off, 1) + np.diag(off, -1)) / (h**2)

    # Clamped (y=0, y'=0) at s=0 and free at s=L approximated by pinned rows
    D2[0, :] = 0.0
    D2[0, 0] = 1.0
    D2[-1, :] = 0.0
    D2[-1, -1] = 1.0

    D4 = D2 @ D2

    gravity_diag = np.diag(rhoA * gravity * g_eff)
    info_diag = np.diag(V_info)
    operator = B_avg * D4 + gravity_diag - info_diag

    eigvals, eigvecs = eigh(operator)
    eigvals = eigvals[:n_modes]
    eigvecs = eigvecs[:, :n_modes]

    return {
        "eigenvalues": eigvals,
        "eigenmodes": eigvecs,
        "critical_eigenvalue": float(eigvals[0]),
        "unstable": bool(eigvals[0] < 0.0),
        "destabilizing_profile": V_info,
    }


__all__ = [
    "information_elasticity_energy",
    "standing_wave_dispersion_relation",
    "solve_countercurvature_eigenproblem",
]
