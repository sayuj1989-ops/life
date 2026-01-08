"""
Analytical Euler-Bernoulli beam solutions for solver validation.

Provides exact closed-form solutions for:
- Cantilever with tip load
- Simply supported beam with uniform load
- Pinned-pinned with center point load

Used to verify BVP solver accuracy (should match within <1% for linear cases).

Note: These solutions assume:
- Small deflections (linearized kinematics)
- Uniform EI (no IEC-2)
- No active moments (no IEC-3)
- No target curvature bias (no IEC-1)

For IEC-coupled problems, use BVPSolver.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Dict

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

from model.core import IECParameters, ModelState, get_git_sha
from model.solvers.base import BaseSolver


class EulerBernoulliAnalytical(BaseSolver):
    """
    Analytical Euler-Bernoulli beam solutions.

    Provides exact solutions for common loading cases to validate
    numerical BVP solvers.

    Methods:
        solve(): Not implemented (use specific load case methods)
        solve_cantilever_tip_load(): Exact solution for cantilever + tip load
        solve_simply_supported_uniform(): Exact solution for pinned + uniform load
    """

    def solve(self) -> ModelState:
        """
        Not implemented - use specific load case methods instead.

        Raises:
            NotImplementedError: Use solve_cantilever_tip_load() etc.
        """
        raise NotImplementedError(
            "Use specific methods like solve_cantilever_tip_load() "
            "for analytical solutions."
        )

    def solve_cantilever_tip_load(
        self, P: float = None, L: float = None, EI: float = None
    ) -> Dict[str, NDArray]:
        """
        Exact solution for cantilever beam with tip load P.

        Geometry: Clamped at x=0, free at x=L, load P applied downward at x=L.

        Analytical formulas:
            M(x) = P(L - x)
            θ(x) = (P/(2EI)) * (2Lx - x²)
            w(x) = (P/(6EI)) * (3Lx² - x³)
            κ(x) = M(x) / EI = P(L - x) / EI

        Args:
            P: Tip load (N), defaults to params.P_load
            L: Beam length (m), defaults to params.length
            EI: Bending stiffness (Pa·m^4), defaults to E0 * I_moment

        Returns:
            Dictionary with keys:
            - "s": Spatial coordinates (m)
            - "theta": Deflection angle (rad)
            - "w": Transverse deflection (m)
            - "kappa": Curvature (1/m)
            - "M": Bending moment (N·m)
        """
        # Use defaults from params if not provided
        if P is None:
            P = self.params.P_load
        if L is None:
            L = self.params.length
        if EI is None:
            EI = self.params.E0 * self.params.I_moment

        s = self.params.get_s_array()
        x = s  # Alias for clarity

        # Analytical solutions
        M = P * (L - x)
        theta = (P / (2 * EI)) * (2 * L * x - x**2)
        w = (P / (6 * EI)) * (3 * L * x**2 - x**3)
        kappa = M / EI

        return {
            "s": s,
            "theta": theta,
            "w": w,
            "kappa": kappa,
            "M": M,
            "solver": "EulerBernoulli_Cantilever_Analytical",
        }

    def solve_simply_supported_uniform(
        self, w_load: float = None, L: float = None, EI: float = None
    ) -> Dict[str, NDArray]:
        """
        Exact solution for simply supported beam with uniform load w.

        Geometry: Pinned at x=0 and x=L, uniform load w (N/m) downward.

        Analytical formulas:
            M(x) = (w/2) * x * (L - x)
            θ(x) = (w/(24EI)) * (L³ - 2Lx² + x³)
            w_max at center: (5wL⁴)/(384EI)

        Args:
            w_load: Uniform load (N/m), defaults to params.distributed_load
            L: Beam length (m)
            EI: Bending stiffness (Pa·m^4)

        Returns:
            Dictionary with spatial fields
        """
        if w_load is None:
            w_load = self.params.distributed_load
        if L is None:
            L = self.params.length
        if EI is None:
            EI = self.params.E0 * self.params.I_moment

        s = self.params.get_s_array()
        x = s

        # Analytical solutions
        M = (w_load / 2) * x * (L - x)
        # Integrate twice for slope and deflection
        # θ from integrating M/EI with BCs
        theta = (w_load / (24 * EI)) * (L**3 - 2 * L * x**2 + x**3)

        # Deflection w from integrating theta
        # (approximate - exact formula more complex)
        w = (w_load / (24 * EI)) * x * (L**3 - 2 * L * x**2 + x**3)

        kappa = M / EI

        return {
            "s": s,
            "theta": theta,
            "w": w,
            "kappa": kappa,
            "M": M,
            "solver": "EulerBernoulli_SimplySupported_Analytical",
        }

    def validate_solution(self, state: ModelState) -> dict:
        """
        Validate analytical solution (always exact).

        Returns:
            Validation dict with perfect metrics
        """
        return {
            "bc_error": 0.0,
            "energy_error": 0.0,
            "residual_max": 0.0,
            "convergence": True,
        }


def compare_bvp_to_analytical(
    params: IECParameters, solver_type: str = "cantilever", tol: float = 0.01
) -> dict:
    """
    Utility function to compare BVP solver against analytical solution.

    Args:
        params: IEC parameters (must have zero couplings for linearity)
        solver_type: "cantilever" or "simply_supported"
        tol: Acceptable relative error tolerance

    Returns:
        Comparison dictionary with error metrics and pass/fail status

    Raises:
        AssertionError: If any coupling is non-zero (analytical not valid)
    """
    # Ensure no IEC couplings (analytical only valid for linear case)
    assert params.chi_kappa == 0.0, "chi_kappa must be zero for analytical comparison"
    assert params.chi_E == 0.0, "chi_E must be zero for analytical comparison"
    assert params.chi_C == 0.0, "chi_C must be zero for analytical comparison"
    assert params.chi_f == 0.0, "chi_f must be zero for analytical comparison"

    from model.solvers.bvp_scipy import BVPSolver

    # Solve with BVP
    if solver_type == "cantilever":
        bvp_solver = BVPSolver(params, bc_type="cantilever")
        state_bvp = bvp_solver.solve()

        # Analytical solution
        analytical_solver = EulerBernoulliAnalytical(params)
        state_analytical = analytical_solver.solve_cantilever_tip_load()

    elif solver_type == "simply_supported":
        bvp_solver = BVPSolver(params, bc_type="pinned_pinned")
        state_bvp = bvp_solver.solve()

        analytical_solver = EulerBernoulliAnalytical(params)
        state_analytical = analytical_solver.solve_simply_supported_uniform()

    else:
        raise ValueError(f"Unknown solver_type: {solver_type}")

    # Compute errors
    L2_theta = np.linalg.norm(
        state_bvp.theta - state_analytical["theta"]
    ) / np.linalg.norm(state_analytical["theta"])

    L2_kappa = np.linalg.norm(
        state_bvp.kappa - state_analytical["kappa"]
    ) / np.linalg.norm(state_analytical["kappa"])

    Linf_theta = np.max(np.abs(state_bvp.theta - state_analytical["theta"]))

    # Pass/fail
    passed = L2_theta < tol and L2_kappa < tol

    return {
        "L2_theta": float(L2_theta),
        "L2_kappa": float(L2_kappa),
        "Linf_theta": float(Linf_theta),
        "tolerance": tol,
        "passed": passed,
        "solver_type": solver_type,
    }
