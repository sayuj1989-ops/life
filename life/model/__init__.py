"""
Information-Elasticity Coupling (IEC) Model - Core Framework

This package provides publication-ready implementations of the IEC model
for spinal biomechanics research.

Modules:
    core: Parameter definitions, model state, units validation
    coherence_fields: Information field generators I(s)
    couplings: IEC-1/2/3 coupling mechanisms
    solvers: Beam/Cosserat equilibrium solvers
    experiments: Parameter sweeps, sensitivity, ablations
"""

__version__ = "0.2.0-beta"
__author__ = "Dr. Sayuj Krishnan"

from .core import IECParameters, ModelState, PhysicalUnits
from .coherence_fields import generate_coherence_field
from .couplings import apply_iec_coupling
from .countercurvature import apply_countercurvature

__all__ = [
    "IECParameters",
    "ModelState",
    "PhysicalUnits",
    "generate_coherence_field",
    "apply_iec_coupling",
    "apply_countercurvature",
]
