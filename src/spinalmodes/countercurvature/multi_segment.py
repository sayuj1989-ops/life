"""Multi-segment spatial parameter generation for Lenke curve modeling.

This module provides utilities to construct spatially varying parameter arrays
(stiffness multipliers and instability drives) for the multi-segment Cosserat
rod model. It maps clinical definitions of Lenke curve types to regional parameter
profiles.
"""
import numpy as np

def build_regional_stiffness_multiplier(z: np.ndarray) -> np.ndarray:
    """Build the base regional stiffness multiplier for the spine.

    Thoracic region is stiffened (rib cage), thoracolumbar junction is weakened,
    and lumbar is slightly stiffened (lordosis structural bulk).

    Parameters
    ----------
    z : np.ndarray
        Normalized spine coordinate array (0=Sacrum, 1=T1).

    Returns
    -------
    np.ndarray
        Array of stiffness multipliers.
    """
    N = len(z)
    B_mult = np.ones(N) * 1.0

    lumbar_idx = (z >= 0.0) & (z < 0.3)      # L5-L1
    tl_junction_idx = (z >= 0.3) & (z < 0.4) # T12-T11
    thoracic_idx = (z >= 0.4) & (z < 0.8)    # T10-T2

    B_mult[thoracic_idx] *= 1.5      # Rib cage buttressing
    B_mult[tl_junction_idx] *= 0.689 # Thoracolumbar vulnerability
    B_mult[lumbar_idx] *= 1.2        # Lumbar structural bulk

    # Smooth the profile
    return np.convolve(B_mult, np.ones(5)/5, mode='same')

def build_lenke_instability_drive(z: np.ndarray, lenke_type: int) -> np.ndarray:
    """Build the effective destabilizing drive Q(s) for a specific Lenke type.

    Parameters
    ----------
    z : np.ndarray
        Normalized spine coordinate array (0=Sacrum, 1=T1).
    lenke_type : int
        Lenke curve type (1-6).

    Returns
    -------
    np.ndarray
        Array representing the spatially varying instability drive.
    """
    N = len(z)
    Q = np.ones(N) * 0.1

    lumbar_idx = (z >= 0.0) & (z < 0.3)
    tl_junction_idx = (z >= 0.3) & (z < 0.4)
    thoracic_idx = (z >= 0.4) & (z < 0.8)
    proximal_t_idx = (z >= 0.8) & (z <= 1.0)

    if lenke_type == 1:
        Q[thoracic_idx] *= 5.0
    elif lenke_type == 2:
        Q[thoracic_idx] *= 4.0
        Q[proximal_t_idx] *= 4.0
    elif lenke_type == 3:
        Q[thoracic_idx] *= 4.0
        Q[lumbar_idx] *= 4.0
    elif lenke_type == 4:
        Q[proximal_t_idx] *= 3.0
        Q[thoracic_idx] *= 3.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 5:
        Q[tl_junction_idx] *= 6.0
        Q[lumbar_idx] *= 3.0
    elif lenke_type == 6:
        Q[thoracic_idx] *= 2.5
        Q[tl_junction_idx] *= 5.0
        Q[lumbar_idx] *= 5.0

    return np.convolve(Q, np.ones(5)/5, mode='same')
