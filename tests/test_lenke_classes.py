import pytest
import numpy as np
from scripts.experiments.experiment_lenke_classes import get_lenke_parameters, solve_buckling_eigenmodes

def test_get_lenke_parameters():
    N = 100
    for lenke_type in range(1, 7):
        B, Q = get_lenke_parameters(lenke_type, N)
        assert B.shape == (N,)
        assert Q.shape == (N,)
        assert np.all(B > 0), f"Stiffness B array contains non-positive values for Lenke type {lenke_type}"
        assert np.all(Q > 0), f"Instability Q array contains non-positive values for Lenke type {lenke_type}"

def test_solve_buckling_eigenmodes():
    N = 100
    # Test a simple constant profile first
    B = np.ones(N)
    Q = np.ones(N) * 0.1
    z, evals, evecs = solve_buckling_eigenmodes(B, Q, N)

    assert z.shape == (N,)
    assert evals.shape[0] == N - 4, "Number of eigenvalues doesn't match the interior nodes (N-4)"
    assert evecs.shape == (N - 4, N - 4)
    # Ensure eigenvalues are sorted
    assert np.all(np.diff(evals) >= 0)

def test_lenke_types_eigenmodes():
    N = 50 # smaller N for faster tests
    for lenke_type in range(1, 7):
        B, Q = get_lenke_parameters(lenke_type, N)
        z, evals, evecs = solve_buckling_eigenmodes(B, Q, N)

        # Verify valid eigenmodes returned
        assert evals.shape[0] > 0
        assert not np.any(np.isnan(evals))
        assert not np.any(np.isnan(evecs))
        assert evals[0] > 0 # Buckling load (first eigenvalue) should be positive for our physical system
