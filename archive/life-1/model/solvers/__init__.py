"""
Equilibrium solvers for beam/Cosserat mechanics with IEC couplings.

Available solvers:
    - BVPSolver: Rigorous boundary value problem solver (scipy.integrate.solve_bvp)
    - EulerBernoulliAnalytical: Analytical solutions for validation
    - LegacyCantilever: Deprecated simplified forward integration

For publication-quality results, use BVPSolver.
"""

from .base import BaseSolver
from .bvp_scipy import BVPSolver
from .euler_bernoulli import EulerBernoulliAnalytical

__all__ = [
    "BaseSolver",
    "BVPSolver",
    "EulerBernoulliAnalytical",
]
