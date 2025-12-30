"""Coupling rules converting information fields into mechanical countercurvature.

This module expresses the central hypothesis of the project in concrete numerical terms:
information processing along a biological rod imprints effective *countercurvature* onto
its mechanical state.  The functions provided here map gradients of information density
into rest curvature, stiffness and active moments that augment or oppose gravity-driven
bending when fed to a Cosserat rod solver (e.g. PyElastica).
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
from numpy.typing import NDArray

from .info_fields import InfoField1D

ArrayF64 = NDArray[np.float64]


class CounterCurvatureParams(NamedTuple):
    """Dimensioned parameters governing information–mechanics coupling.

    Attributes
    ----------
    chi_kappa:
        Coupling gain transforming information gradients (``∂I/∂s``) into corrections of
        the rod's rest curvature (units: 1/m per unit information gradient).
    chi_E:
        Coupling gain for stiffness modulation by the information density (dimensionless
        multiplier on the baseline Young's modulus).
    chi_M:
        Coupling gain converting information gradients into active internal moments
        (units: N·m per unit gradient).  This represents the "effort" expended by the
        living system to steer curvature against gravity.
    scale_length:
        Optional length scale used when non-dimensionalising information gradients.  Set
        to ``1.0`` to operate directly in SI units.
    """

    chi_kappa: float = 0.0
    chi_E: float = 0.0
    chi_M: float = 0.0
    scale_length: float = 1.0

    def nondimensional_gradient(self, dIds: ArrayF64) -> ArrayF64:
        """Return a gradient scaled by ``scale_length`` if provided."""

        if self.scale_length <= 0.0:
            raise ValueError("scale_length must be positive.")
        return dIds * float(self.scale_length)


def _validate_shapes(info: InfoField1D, *arrays: ArrayF64) -> None:
    for array in arrays:
        if array.shape != info.s.shape:
            raise ValueError(
                "All arrays must share the same shape as the information grid."
            )


def compute_rest_curvature(
    info: InfoField1D, params: CounterCurvatureParams, kappa_gen: ArrayF64
) -> ArrayF64:
    """Compute information-biased rest curvature ``κ_rest``.

    Parameters
    ----------
    info:
        Information field describing ``I(s)`` and ``∂I/∂s`` along the rod.
    params:
        Coupling parameters mapping information gradients to curvature corrections.
    kappa_gen:
        Baseline geometric curvature (e.g. from evolutionary morphology) with the same
        discretisation as ``info``.

    Returns
    -------
    numpy.ndarray
        The rest curvature profile ``κ_rest(s)`` incorporating biological countercurvature.

    Notes
    -----
    ``κ_rest = κ_gen + χ_κ * scale_length * ∂I/∂s`` encapsulates the IEC-1 coupling where
    organised information flows create effective modifications to the reference geometry.
    This is interpreted as biological countercurvature acting analogously to a local
    correction of spacetime curvature perceived by the rod.
    """

    _validate_shapes(info, kappa_gen)
    grad = params.nondimensional_gradient(info.dIds)
    return np.asarray(kappa_gen, dtype=float) + params.chi_kappa * grad


def compute_effective_stiffness(
    info: InfoField1D, params: CounterCurvatureParams, E0: float, *, model: str = "linear"
) -> ArrayF64:
    """Compute the information-modulated stiffness field ``E_eff``.

    Parameters
    ----------
    info:
        Information field describing ``I(s)`` along the rod.
    params:
        Coupling parameters; only ``chi_E`` is used here.
    E0:
        Baseline Young's modulus of the rod (Pa).
    model:
        Functional form of the coupling.  ``"linear"`` implements ``E_eff = E0 * (1 + chi_E * I)``
        while ``"exponential"`` uses ``E_eff = E0 * exp(chi_E * I)``.

    Returns
    -------
    numpy.ndarray
        Spatially varying effective stiffness.

    Raises
    ------
    ValueError
        If an unsupported model is requested or shapes are inconsistent.
    """

    if E0 <= 0.0:
        raise ValueError("Baseline stiffness E0 must be positive.")
    I = np.asarray(info.I, dtype=float)

    if model == "linear":
        return E0 * (1.0 + params.chi_E * I)
    if model == "exponential":
        return E0 * np.exp(params.chi_E * I)
    raise ValueError(f"Unsupported stiffness coupling model: {model}")


def compute_active_moments(info: InfoField1D, params: CounterCurvatureParams) -> ArrayF64:
    """Return an information-driven active moment field ``M_info``.

    The active moment encodes the biological ``effort`` or internal actuation required to
    maintain countercurvature against gravity.  In our analog model it is a direct,
    gradient-driven term ``M_info = χ_M * scale_length * ∂I/∂s``.
    """

    grad = params.nondimensional_gradient(info.dIds)
    return params.chi_M * grad
