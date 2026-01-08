"""
Abstract base class for all equilibrium solvers.

Ensures consistency across solver implementations with:
- Deterministic execution (fixed random seed)
- Solution validation (BC satisfaction, energy conservation)
- Benchmark comparison interfaces
"""

from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

from model.core import IECParameters, ModelState


class BaseSolver(ABC):
    """
    Abstract solver interface for beam/Cosserat equilibrium problems.

    All solver implementations must:
    1. Solve for equilibrium state given IEC parameters
    2. Validate solution quality (BC, energy, convergence)
    3. Provide benchmark comparison methods

    Attributes:
        params: IEC parameters defining the problem
    """

    def __init__(self, params: IECParameters):
        """
        Initialize solver with parameters.

        Args:
            params: IEC parameters
        """
        self.params = params
        np.random.seed(params.random_seed)

    @abstractmethod
    def solve(self) -> ModelState:
        """
        Solve for equilibrium state.

        Returns:
            ModelState with complete spatial fields (theta, kappa, etc.)

        Raises:
            RuntimeError: If solver fails to converge or solution is invalid
        """
        pass

    @abstractmethod
    def validate_solution(self, state: ModelState) -> dict:
        """
        Validate solution quality.

        Args:
            state: Model state to validate

        Returns:
            Dictionary with validation metrics:
            - "bc_error": Boundary condition residual norm
            - "energy_error": Relative energy conservation error
            - "convergence": Boolean, True if converged
            - "residual_max": Maximum equation residual
        """
        pass

    def benchmark_against_analytical(
        self, analytical_solution: callable
    ) -> dict:
        """
        Compare numerical solution against known analytical solution.

        Args:
            analytical_solution: Function returning analytical state dict

        Returns:
            Dictionary with error metrics:
            - "L2_theta": L2 relative error in theta
            - "L2_kappa": L2 relative error in kappa
            - "Linf_theta": L∞ error in theta
        """
        state_numerical = self.solve()
        state_analytical = analytical_solution()

        # L2 relative error
        L2_theta = np.linalg.norm(
            state_numerical.theta - state_analytical["theta"]
        ) / np.linalg.norm(state_analytical["theta"])

        L2_kappa = np.linalg.norm(
            state_numerical.kappa - state_analytical["kappa"]
        ) / np.linalg.norm(state_analytical["kappa"])

        # L∞ error
        Linf_theta = np.max(np.abs(state_numerical.theta - state_analytical["theta"]))

        return {
            "L2_theta": float(L2_theta),
            "L2_kappa": float(L2_kappa),
            "Linf_theta": float(Linf_theta),
        }
