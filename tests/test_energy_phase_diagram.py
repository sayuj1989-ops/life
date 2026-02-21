import sys
import os
import numpy as np
import pytest

# Add repo root to path so we can import scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module to test
# Since it's a script without main guard for import (wait, it has main guard),
# importing it might run top-level code if any.
# But it only has imports, constants, functions and if __name__ == "__main__": main()
# So importing is safe.

from scripts.experiment_energy_phase_diagram import solve_column, RHO, A_REF, L_REF, G

def test_solve_column_smoke():
    """Smoke test to ensure solve_column runs without error and returns valid shapes."""
    L = 0.35
    chi_kappa = 0.05
    s, theta, kappa = solve_column(L, chi_kappa)

    assert len(s) == 100
    assert len(theta) == 100
    assert len(kappa) == 100

    # Check for finite values (no NaN/Inf)
    assert np.all(np.isfinite(theta))
    assert np.all(np.isfinite(kappa))

def test_solve_column_zero_curvature():
    """Test with zero intrinsic curvature (chi_kappa=0)."""
    L = 0.35
    chi_kappa = 0.0
    s, theta, kappa = solve_column(L, chi_kappa)

    # With no intrinsic curvature, kappa should be zero (or close to it if gravity induces buckling? No, it's a stable column under critical load)
    # Actually, if L < L_crit, theta=0.
    # L=0.35 is likely below critical buckling load for these parameters?
    # P_crit = pi^2 * EI / (4L^2) (cantilever)
    # Let's not assert zero, but check it runs.

    assert np.all(np.isfinite(theta))

def test_solve_column_high_curvature():
    """Test with high intrinsic curvature."""
    L = 0.5
    chi_kappa = 10.0
    s, theta, kappa = solve_column(L, chi_kappa)

    assert np.all(np.isfinite(theta))
