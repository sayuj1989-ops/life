"""Validation utilities for countercurvature analog models.

This module provides metrics that quantify how information-driven countercurvature
deviates from passive gravitational equilibria. These metrics interpret the
information-driven corrections as effective "metric deviations" in the analog
spacetime model.

The key metrics are:
- Countercurvature energy: Integrated deviation between passive and info-driven shapes
- Effective metric deviation: L2 norm of curvature corrections
- Shape preservation index: How well information maintains structure against gravity
"""

from __future__ import annotations

from typing import Optional

import numpy as np
from numpy.typing import NDArray

from .info_fields import InfoField1D

ArrayF64 = NDArray[np.float64]


def compute_countercurvature_metric(
    info: InfoField1D,
    beta1: float = 1.0,
    beta2: float = 0.5,
    eps: float = 1e-9,
) -> ArrayF64:
    """Compute the 1D "biological countercurvature" metric g_eff(s) along the rod.

    We treat the body axis s as a 1D manifold with effective line element

        dℓ_eff^2 = g_eff(s) ds^2,

    where g_eff(s) is a conformal factor derived from the information field I(s)
    and its gradient dI/ds. Intuitively:

    - Regions with high / rapidly changing information are weighted more heavily
      in the geometry (strong "biological countercurvature").
    - Regions with low, flat information are close to the baseline metric.

    **Scientific Note**: This is a phenomenological metric, not derived from
    first principles. The functional form g_eff(s) = exp(2φ(s)) with
    φ(s) = β₁·Ĩ_centered + β₂·Ĩ' is chosen to encode the hypothesis that
    information density and gradients modify effective geometry, but the specific
    weighting (beta1, beta2) and normalization are empirical choices.

    Parameters
    ----------
    info:
        1D information field (s, I, dIds) along the rod.
    beta1:
        Weight for excess information amplitude.
    beta2:
        Weight for information gradient.
    eps:
        Small constant to avoid division by zero.

    Returns
    -------
    g_eff : np.ndarray, shape (N,)
        Positive-definite conformal metric factor g_eff(s) = exp(2 φ(s)).
    """
    s = info.s
    I = info.I
    dIds = info.dIds

    if I.ndim != 1 or dIds.ndim != 1 or s.ndim != 1:
        raise ValueError("InfoField1D arrays must be 1D.")

    if not (I.shape == dIds.shape == s.shape):
        raise ValueError("InfoField1D arrays must have the same shape.")

    # Normalize I to ~[0, 1]
    I_min = float(np.min(I))
    I_max = float(np.max(I))
    I_norm = (I - I_min) / (I_max - I_min + eps)

    # Centered, so "excess" information is relative to mean
    I_centered = I_norm - float(np.mean(I_norm))

    # Normalize gradient to ~[-1, 1]
    max_grad = float(np.max(np.abs(dIds))) + eps
    dI_norm = dIds / max_grad

    # Build φ(s) (dimensionless)
    phi = beta1 * I_centered + beta2 * dI_norm

    # Conformal metric factor: strictly positive
    g_eff = np.exp(2.0 * phi)
    return g_eff


def geodesic_curvature_deviation(
    s: ArrayF64,
    kappa_passive: ArrayF64,
    kappa_info: ArrayF64,
    g_eff: ArrayF64,
    eps: float = 1e-9,
) -> dict[str, float]:
    """Geodesic curvature deviation between passive and information-driven
    curvature profiles, measured in the countercurvature metric g_eff(s).

    **Scientific Note**: The normalized version D̂_geo = D_geo / √(∫ g_eff κ₀² ds)
    can inflate as gravity → 0 because the denominator (base_energy) collapses
    while D_geo may remain finite. This is expected behavior: when passive
    curvature energy is very small, even small information-driven deviations
    appear large in the normalized metric. Interpret D̂_geo with caution in
    the microgravity limit.

    We define the squared distance

        D_geo^2 = ∫ g_eff(s) [κ_info(s) - κ_passive(s)]^2 ds,

    which is a Riemannian distance in the space of curvature profiles with
    metric weight g_eff(s). Regions with strong information (large g_eff)
    contribute more to the deviation.

    Parameters
    ----------
    s:
        Arc-length grid, shape (N,).
    kappa_passive:
        Curvature profile in the gravity-only, "passive" configuration.
    kappa_info:
        Curvature profile in the information-coupled configuration.
    g_eff:
        Countercurvature metric factor g_eff(s) along the rod.
    eps:
        Small constant to avoid division by zero.

    Returns
    -------
    metrics : dict
        "D_geo"      : float, geodesic curvature deviation.
        "D_geo_sq"   : float, squared deviation.
        "D_geo_norm" : float, normalized by passive curvature energy.
        "base_energy": float, weighted energy of κ_passive in g_eff.
    """
    if not (s.shape == kappa_passive.shape == kappa_info.shape == g_eff.shape):
        raise ValueError("All input arrays must have the same shape.")

    # Difference in curvature
    dkappa = kappa_info - kappa_passive

    # Weighted L2 distance in the countercurvature metric
    integrand = g_eff * dkappa**2
    D_geo_sq = float(np.trapz(integrand, s))
    D_geo = float(np.sqrt(max(D_geo_sq, 0.0)))

    # Baseline: passive curvature "energy" in g_eff
    base_integrand = g_eff * kappa_passive**2
    base_energy = float(np.trapz(base_integrand, s))

    # Normalized distance (dimensionless)
    D_geo_norm = D_geo / (np.sqrt(base_energy) + eps)

    return {
        "D_geo": D_geo,
        "D_geo_sq": D_geo_sq,
        "D_geo_norm": D_geo_norm,
        "base_energy": base_energy,
    }


def compute_countercurvature_energy(
    centerline_passive: ArrayF64,
    centerline_info: ArrayF64,
    *,
    method: str = "l2_distance",
) -> float:
    """Compute the energy-like metric quantifying countercurvature deviation.

    This metric measures the "biological work" done by information processing
    to reshape the rod against passive gravitational sag. It is interpreted as
    the energy stored in the countercurvature field—an analog of the deviation
    from the passive spacetime metric.

    Parameters
    ----------
    centerline_passive:
        Rod centerline coordinates for passive (no info coupling) case.
        Shape (n_points, 2) for 2D or (n_points, 3) for 3D.
    centerline_info:
        Rod centerline coordinates for information-driven case.
        Same shape as centerline_passive.
    method:
        Method for computing energy:
        - "l2_distance": Integrated squared distance between centerlines
        - "curvature_diff": Integrated squared difference in curvature
        - "arc_length": Arc-length weighted L2 distance

    Returns
    -------
    float
        Countercurvature energy (dimensionless or with units depending on method).

    Notes
    -----
    The countercurvature energy represents the deviation from the passive
    gravitational equilibrium. In the biological countercurvature hypothesis,
    this is interpreted as the "biological work" done by information processing
    to modify the effective spacetime curvature experienced by the rod.
    """
    if centerline_passive.shape != centerline_info.shape:
        raise ValueError(
            f"Centerline shapes must match: {centerline_passive.shape} vs {centerline_info.shape}"
        )

    if method == "l2_distance":
        # Integrated squared distance
        diff = centerline_info - centerline_passive
        squared_distances = np.sum(diff**2, axis=-1)
        return float(np.trapz(squared_distances))

    elif method == "curvature_diff":
        # Compute curvature from centerline and compare
        # Simplified: use finite differences
        kappa_passive = _compute_curvature_from_centerline(centerline_passive)
        kappa_info = _compute_curvature_from_centerline(centerline_info)
        diff_squared = (kappa_info - kappa_passive) ** 2
        return float(np.trapz(diff_squared))

    elif method == "arc_length":
        # Arc-length weighted distance
        ds = _compute_arc_length_elements(centerline_info)
        diff = centerline_info - centerline_passive
        squared_distances = np.sum(diff**2, axis=-1)
        return float(np.trapz(squared_distances, x=ds))

    else:
        raise ValueError(f"Unknown method: {method}")


def compute_effective_metric_deviation(
    kappa_passive: ArrayF64,
    kappa_info: ArrayF64,
    *,
    s: Optional[ArrayF64] = None,
) -> float:
    """Compute the L2 norm of curvature deviation as a metric deviation.

    This metric interprets the difference between passive and information-driven
    curvature as an effective deviation from the passive spacetime metric.
    In the biological countercurvature hypothesis, information processing creates
    a local correction to the gravitational curvature field.

    Parameters
    ----------
    kappa_passive:
        Passive curvature profile κ_passive(s) (1/m).
    kappa_info:
        Information-driven curvature profile κ_info(s) (1/m).
    s:
        Optional arc-length coordinate. If None, assumes uniform spacing.

    Returns
    -------
    float
        L2 norm of curvature deviation, interpreted as metric deviation.

    Notes
    -----
    The metric deviation δκ = κ_info - κ_passive represents the information-driven
    correction to the passive gravitational curvature. The L2 norm quantifies the
    magnitude of this correction, which is interpreted as a local modification
    of the effective spacetime metric by biological information processing.
    """
    if kappa_passive.shape != kappa_info.shape:
        raise ValueError("Curvature arrays must have the same shape")

    delta_kappa = kappa_info - kappa_passive

    if s is not None:
        # Integrate with respect to arc-length
        integrand = delta_kappa**2
        metric_dev = np.sqrt(np.trapz(integrand, x=s))
    else:
        # Uniform spacing
        metric_dev = np.linalg.norm(delta_kappa) / np.sqrt(len(delta_kappa))

    return float(metric_dev)


def compute_shape_preservation_index(
    centerline_initial: ArrayF64,
    centerline_final: ArrayF64,
    centerline_passive: ArrayF64,
) -> float:
    """Compute how well information preserves shape against gravitational sag.

    This index measures the ratio of shape preservation in the information-driven
    case compared to passive gravitational sag. A value > 1 indicates that
    information countercurvature maintains shape better than passive mechanics.

    Parameters
    ----------
    centerline_initial:
        Initial rod centerline (reference shape).
    centerline_final:
        Final centerline with information coupling.
    centerline_passive:
        Final centerline for passive (no info) case.

    Returns
    -------
    float
        Shape preservation index. Values > 1 indicate information preserves
        shape better than passive mechanics.
    """
    # Compute deviation from initial shape
    dev_info = np.linalg.norm(centerline_final - centerline_initial, axis=-1)
    dev_passive = np.linalg.norm(centerline_passive - centerline_initial, axis=-1)

    # Average deviation
    mean_dev_info = np.mean(dev_info)
    mean_dev_passive = np.mean(dev_passive)

    if mean_dev_passive < 1e-10:
        # No passive deviation (trivial case)
        return 1.0 if mean_dev_info < 1e-10 else 0.0

    # Preservation index: ratio of passive to info deviation
    # Higher values mean info preserves shape better
    return float(mean_dev_passive / (mean_dev_info + 1e-10))


def compare_with_beam_solver(
    centerline_pyelastica: ArrayF64,
    theta_beam: ArrayF64,
    s: ArrayF64,
    *,
    tolerance: float = 0.01,
) -> dict[str, float | bool]:
    """Compare PyElastica results with existing beam/BVP solver.

    This validation function checks that the PyElastica countercurvature
    implementation produces results consistent with the existing beam solver
    for passive (no info coupling) cases.

    Parameters
    ----------
    centerline_pyelastica:
        Centerline from PyElastica simulation, shape (n_points, 2) or (n_points, 3).
    theta_beam:
        Angle profile from beam solver (radians), shape (n_points,).
    s:
        Arc-length coordinate (metres).
    tolerance:
        Relative tolerance for agreement.

    Returns
    -------
    dict
        Dictionary with:
        - "max_angle_error": Maximum difference in angles (rad)
        - "rms_angle_error": RMS difference in angles (rad)
        - "agrees": Boolean indicating if results agree within tolerance
    """
    # Reconstruct centerline from beam solver angles
    centerline_beam = _reconstruct_centerline_from_theta(theta_beam, s)

    # Extract 2D projection if needed
    if centerline_pyelastica.shape[1] == 3:
        centerline_py = centerline_pyelastica[:, [0, 2]]  # x-z plane
    else:
        centerline_py = centerline_pyelastica

    # Compute angles from centerlines
    theta_py = _compute_angle_from_centerline(centerline_py)
    theta_beam_interp = np.interp(
        np.linspace(0, s[-1], len(theta_py)), s, theta_beam
    )

    # Compare angles
    angle_diff = theta_py - theta_beam_interp
    max_error = float(np.max(np.abs(angle_diff)))
    rms_error = float(np.sqrt(np.mean(angle_diff**2)))

    agrees = max_error < tolerance * np.max(np.abs(theta_beam))

    return {
        "max_angle_error": max_error,
        "rms_angle_error": rms_error,
        "agrees": agrees,
    }


# Helper functions


def _compute_curvature_from_centerline(centerline: ArrayF64) -> ArrayF64:
    """Compute curvature from centerline coordinates using finite differences."""
    if centerline.shape[1] == 2:
        # 2D: κ = |d²r/ds²|
        dr = np.diff(centerline, axis=0)
        ds = np.linalg.norm(dr, axis=1)
        ds = np.concatenate([[ds[0]], ds])  # Pad for same length

        # Normalized tangent
        t = dr / (ds[:, np.newaxis] + 1e-10)
        dt = np.diff(t, axis=0, prepend=t[0:1])
        kappa = np.linalg.norm(dt, axis=1) / (ds + 1e-10)
        return kappa
    else:
        # 3D: simplified
        dr = np.diff(centerline, axis=0)
        ds = np.linalg.norm(dr, axis=1)
        ds = np.concatenate([[ds[0]], ds])
        t = dr / (ds[:, np.newaxis] + 1e-10)
        dt = np.diff(t, axis=0, prepend=t[0:1])
        kappa = np.linalg.norm(dt, axis=1) / (ds + 1e-10)
        return kappa


def _compute_arc_length_elements(centerline: ArrayF64) -> ArrayF64:
    """Compute arc-length element lengths."""
    dr = np.diff(centerline, axis=0)
    ds = np.linalg.norm(dr, axis=1)
    # Pad to match centerline length
    ds = np.concatenate([[ds[0] if len(ds) > 0 else 0.0], ds])
    return ds


def _reconstruct_centerline_from_theta(theta: ArrayF64, s: ArrayF64) -> ArrayF64:
    """Reconstruct 2D centerline from angle profile."""
    # Integrate: dx/ds = cos(θ), dz/ds = sin(θ)
    x = np.zeros_like(s)
    z = np.zeros_like(s)

    ds = np.diff(s)
    x[1:] = np.cumsum(np.cos(theta[:-1]) * ds)
    z[1:] = np.cumsum(np.sin(theta[:-1]) * ds)

    return np.column_stack([x, z])


def _compute_angle_from_centerline(centerline: ArrayF64) -> ArrayF64:
    """Compute angle profile from 2D centerline."""
    dr = np.diff(centerline, axis=0)
    angles = np.arctan2(dr[:, 1], dr[:, 0])
    # Pad to match centerline length
    angles = np.concatenate([[angles[0]], angles])
    return angles


__all__ = [
    "compute_countercurvature_metric",
    "geodesic_curvature_deviation",
    "compute_countercurvature_energy",
    "compute_effective_metric_deviation",
    "compute_shape_preservation_index",
    "compare_with_beam_solver",
]
