"""
Coherence field generators I(s) for developmental information.

Implements prototypical spatial patterns representing:
- HOX/PAX expression gradients
- Morphogen gradients (RA, FGF, Wnt)
- Ciliary flow fields
- Segmentation clock coherence

All fields are dimensionless and normalized.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Literal

from .core import IECParameters


def generate_coherence_field(
    s: NDArray[np.float64], params: IECParameters
) -> NDArray[np.float64]:
    """
    Generate information/coherence field I(s).

    Args:
        s: Spatial coordinates (m), shape (n_nodes,)
        params: IEC parameters specifying field mode and parameters

    Returns:
        Coherence field I(s), dimensionless, shape (n_nodes,)

    Raises:
        ValueError: If I_mode is not recognized

    Examples:
        >>> params = IECParameters(I_mode="linear", I_gradient=0.5)
        >>> s = params.get_s_array()
        >>> I_field = generate_coherence_field(s, params)
        >>> assert I_field[0] == pytest.approx(1.0)
        >>> assert I_field[-1] > I_field[0]
    """
    if len(s) == 0:
        return np.array([])

    s_norm = s / params.length

    if params.I_mode == "constant":
        return _constant_field(s, params)

    elif params.I_mode == "linear":
        return _linear_gradient_field(s_norm, params)

    elif params.I_mode == "gaussian":
        return _gaussian_bump_field(s_norm, params)

    elif params.I_mode == "step":
        return _step_function_field(s_norm, params)

    else:
        raise ValueError(f"Unknown I_mode: {params.I_mode}")


def _constant_field(s: NDArray[np.float64], params: IECParameters) -> NDArray[np.float64]:
    """
    Constant uniform field.

    I(s) = I_amplitude

    Use case: Uniform expression domain (e.g., thoracic HOX)
    """
    return np.ones_like(s) * params.I_amplitude


def _linear_gradient_field(
    s_norm: NDArray[np.float64], params: IECParameters
) -> NDArray[np.float64]:
    """
    Linear rostro-caudal gradient.

    I(s) = I_amplitude * (1 + I_gradient * s_normalized)

    Use case: RA gradient in presomitic mesoderm
    Biological reference: Dubrulle et al. 2001 (Cell)
    """
    return params.I_amplitude * (1.0 + params.I_gradient * s_norm)


def _gaussian_bump_field(
    s_norm: NDArray[np.float64], params: IECParameters
) -> NDArray[np.float64]:
    """
    Gaussian localized signaling center.

    I(s) = I_amplitude * exp[-(s - s_center)^2 / (2 * width^2)]

    Use case: FGF8 signaling from tail bud
    Biological reference: Delfini et al. 2005 (Dev Cell)
    """
    return params.I_amplitude * np.exp(
        -((s_norm - params.I_center) ** 2) / (2 * params.I_width**2)
    )


def _step_function_field(
    s_norm: NDArray[np.float64], params: IECParameters
) -> NDArray[np.float64]:
    """
    Sharp domain boundary (Heaviside step).

    I(s) = 0 if s < s_center, I_amplitude if s >= s_center

    Use case: HOX domain boundaries (e.g., cervical-thoracic transition)
    Biological reference: Wellik 2007 (Dev Dyn)
    """
    I_field = np.zeros_like(s_norm)
    I_field[s_norm >= params.I_center] = params.I_amplitude
    return I_field


def compute_gradient(
    field: NDArray[np.float64], s: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    Compute spatial gradient of a field using finite differences.

    Args:
        field: Field values at spatial points, shape (n,)
        s: Spatial coordinates (m), shape (n,)

    Returns:
        Gradient ∂field/∂s, shape (n,)

    Note:
        Uses numpy.gradient with second-order accurate central differences
        (except at boundaries where forward/backward differences are used).
    """
    return np.gradient(field, s)


def compute_gradient_norm(
    field: NDArray[np.float64], s: NDArray[np.float64]
) -> float:
    """
    Compute L2 norm of spatial gradient (magnitude measure).

    Args:
        field: Field values
        s: Spatial coordinates

    Returns:
        ||∇I|| = sqrt(∫ (∂I/∂s)^2 ds) / L
    """
    grad = compute_gradient(field, s)
    return float(np.sqrt(np.trapz(grad**2, s)) / (s[-1] - s[0]))
