import numpy as np

from spinalmodes.model.solvers.euler_bernoulli import (
    integrate_shape_from_curvature,
    analytic_sinusoid,
    l2_error,
)


def run_error(n: int) -> float:
    L, A, k = 1.0, 0.01, 6 * np.pi
    s = np.linspace(0, L, n)
    y_true = analytic_sinusoid(s, A, k)
    kappa = -A * (k**2) * np.sin(k * s)
    _, y_num = integrate_shape_from_curvature(s, kappa)
    return l2_error(y_true, y_num)


def test_refinement_improves_accuracy():
    coarse = run_error(401)
    fine = run_error(1601)
    assert fine < coarse * 0.7
