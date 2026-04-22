"""
Multi-segment Cosserat rod extension for predicting Lenke curve types (1-6).

This module provides functions to create regional parameter profiles representing
different structural modifiers along the spine (main thoracic, thoracolumbar, lumbar).
"""
import numpy as np

def create_lenke_profile(s: np.ndarray, lenke_type: int) -> dict:
    """
    Generate regional parameter profiles for a given Lenke type.

    Parameters
    ----------
    s : np.ndarray
        Arc length array (normalized from 0 to 1).
    lenke_type : int
        Lenke curve type (1-6).

    Returns
    -------
    dict
        Dictionary containing spatially varying parameter arrays:
        - chi_kappa: Coupling gain for planar curvature
        - chi_tau: Coupling gain for torsion
        - tau_delay: Proprioceptive delay (ms)
        - damping_b: Local damping variations
        - EI_modifier: Regional variation in stiffness EI
        - asymmetric_load: Asymmetric loading profile
    """
    n_points = len(s)

    # Base profiles
    chi_kappa = np.ones(n_points) * 0.1
    chi_tau = np.ones(n_points) * 0.01
    tau_delay = np.ones(n_points) * 70.0 # baseline delay in ms
    damping_b = np.ones(n_points) * 1.0  # baseline damping
    EI_modifier = np.ones(n_points) * 1.0 # baseline stiffness
    asymmetric_load = np.zeros(n_points) # baseline asymmetric load

    # Regions
    thoracic_mask = s < 0.6
    lumbar_mask = s >= 0.6
    transition_mask = (s >= 0.4) & (s < 0.7)

    if lenke_type == 1:
        # Type 1: Main Thoracic
        chi_kappa[thoracic_mask] *= 2.5
        tau_delay[thoracic_mask] = 95.0
        damping_b[thoracic_mask] = 0.8
        EI_modifier[lumbar_mask] *= 1.5 # Lumbar stiffer, resists buckling
        asymmetric_load[thoracic_mask] = 0.2 # E.g., aortic pulsation, cardiac offset

    elif lenke_type == 2:
        # Type 2: Double Thoracic
        chi_kappa[s < 0.8] *= 2.2
        tau_delay[s < 0.8] = 90.0
        damping_b[s < 0.8] = 0.85
        asymmetric_load[s < 0.8] = 0.15

    elif lenke_type == 3:
        # Type 3: Double Major (Thoracic and Lumbar)
        chi_kappa *= 2.0
        tau_delay[:] = 92.0
        damping_b[:] = 0.8
        asymmetric_load[:] = 0.1

    elif lenke_type == 4:
        # Type 4: Triple Major
        chi_kappa *= 2.3
        tau_delay[:] = 94.0
        damping_b[:] = 0.75
        asymmetric_load[:] = 0.2

    elif lenke_type == 5:
        # Type 5: Thoracolumbar/Lumbar
        chi_kappa[transition_mask] *= 2.5
        chi_kappa[lumbar_mask] *= 2.2
        tau_delay[transition_mask] = 95.0
        tau_delay[lumbar_mask] = 93.0
        damping_b[lumbar_mask] = 0.7
        EI_modifier[thoracic_mask] *= 1.5 # Thoracic stiffer
        asymmetric_load[lumbar_mask] = 0.25 # Lumbar side-bending modifier effect

    elif lenke_type == 6:
        # Type 6: Thoracolumbar/Lumbar - Main Thoracic
        chi_kappa[lumbar_mask] *= 2.8
        chi_kappa[thoracic_mask] *= 1.5
        tau_delay[lumbar_mask] = 98.0
        tau_delay[thoracic_mask] = 85.0
        damping_b[lumbar_mask] = 0.65
        damping_b[thoracic_mask] = 0.9
        asymmetric_load[lumbar_mask] = 0.3
    else:
        raise ValueError("Lenke type must be between 1 and 6.")

    return {
        'chi_kappa': chi_kappa,
        'chi_tau': chi_tau,
        'tau_delay': tau_delay,
        'damping_b': damping_b,
        'EI_modifier': EI_modifier,
        'asymmetric_load': asymmetric_load
    }
