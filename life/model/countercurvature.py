"""Countercurvature mechanisms opposing gravitational bending.

This module elaborates the "countercurvature" hypothesis: developing tissue
actively reorients growth to reject the gravitational curvature that would
otherwise emerge from body weight.  Gravity is still represented as a classic
distributed load, but we provide explicit utilities to compute the induced
moments/curvature and then modulate the IEC target fields so that growth can
either oppose (default) or reinforce that bending.  The calculations remain
strictly mechanical—no general relativistic terms are introduced—but the
biological interpretation is that morphogenetic programs measure the direction
of gravity and apply growth in the opposite direction to maintain posture.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np

from numpy.typing import NDArray

from .core import IECParameters


def compute_gravitational_load(params: IECParameters) -> float:
    """Compute the uniform gravitational load per unit length (N/m).

    Assumes the segment is horizontal so that gravity induces a constant
    downward force density ``q = ρ A g``.  This is the baseline load that the
    countercurvature mechanism reacts against.
    """
    return params.rho * params.A_cross * params.g_magnitude


def compute_gravitational_moment_profile(
    s: NDArray[np.float64], params: IECParameters
) -> NDArray[np.float64]:
    """Cantilever bending moment induced by uniform gravitational load.

    The spinal segment is modeled as a cantilevered beam fixed at ``s=0`` with
    free tip at ``s=L``.  Under a uniform load ``q`` the internal bending
    moment follows ``M(s) = q (L s - s²/2)``.  This quantity feeds directly into
    the active moment compensation term when countercurvature is enabled.
    """
    q = compute_gravitational_load(params)
    L = params.length
    x = s
    return q * (L * x - 0.5 * x**2)


def compute_gravitational_curvature_profile(
    s: NDArray[np.float64], params: IECParameters
) -> NDArray[np.float64]:
    """Curvature profile induced by gravitational bending.

    Using Euler–Bernoulli beam theory, curvature is the bending moment divided
    by the flexural rigidity ``EI``.  The countercurvature controller scales and
    signs this profile to represent growth opposing or reinforcing gravity.
    """
    EI = params.E0 * params.I_moment
    if EI <= 0:
        raise ValueError("Product E0 * I_moment must be positive for curvature calculation")
    moments = compute_gravitational_moment_profile(s, params)
    return moments / EI


def apply_countercurvature(
    s: NDArray[np.float64],
    params: IECParameters,
    kappa_target: NDArray[np.float64],
    M_active: NDArray[np.float64],
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Oppose gravitational bending by modulating curvature and active moments.

    Parameters
    ----------
    s:
        Spatial coordinates (m) for the discretized segment.
    params:
        ``IECParameters`` containing countercurvature controls.  The
        ``countercurvature_gain`` tunes how strongly growth reacts, while
        ``countercurvature_orientation`` selects whether that reaction pushes
        against or with gravity.
    kappa_target:
        Baseline target curvature profile (1/m) from IEC-1 and other sources.
    M_active:
        Active moment distribution (N·m) from IEC-3 and other effects.

    Returns
    -------
    Tuple of adjusted ``(kappa_target, M_active)`` incorporating the chosen
    countercurvature orientation.  When opposing gravity (default) a positive
    gain subtracts the gravitational curvature/moment from the fields; when set
    to "with_gravity" the same gain reinforces the gravitational bending.
    """
    if params.countercurvature_gain == 0.0:
        return kappa_target, M_active

    if params.countercurvature_orientation == "against_gravity":
        sign = -1.0
    elif params.countercurvature_orientation == "with_gravity":
        sign = 1.0
    else:
        raise ValueError(
            "countercurvature_orientation must be 'against_gravity' or 'with_gravity'"
        )

    kappa_gravity = compute_gravitational_curvature_profile(s, params)
    M_gravity = compute_gravitational_moment_profile(s, params)

    kappa_adjusted = kappa_target + sign * params.countercurvature_gain * kappa_gravity
    M_adjusted = M_active + sign * params.countercurvature_gain * M_gravity

    return kappa_adjusted, M_adjusted


__all__ = [
    "compute_gravitational_load",
    "compute_gravitational_moment_profile",
    "compute_gravitational_curvature_profile",
    "apply_countercurvature",
]
