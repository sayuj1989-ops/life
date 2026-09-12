import numpy as np
import pytest
from scipy.linalg import expm

from spinalmodes.recovery_two_state import simulate


def test_impulse_matches_exact_competing_rate_fraction():
    t = np.linspace(0, 20, 101)
    result = simulate(t, kr=0.7, kg=0.3, initial=(0.02, 0))
    np.testing.assert_allclose(result['recoverable'], 0.02 * np.exp(-t), atol=2e-12)
    np.testing.assert_allclose(result['remodeled'], 0.006 * (1 - np.exp(-t)), atol=2e-12)


def test_constant_load_and_recovery_match_matrix_exponential():
    t = np.linspace(0, 10, 41)
    result = simulate(t, kr=0.7, kg=0.3, kh=0.1, forcing=0.02, initial=(0.01, -0.02))
    matrix = np.array([[-1, 0, 0.02], [0.3, -0.1, 0], [0, 0, 0]])
    expected = np.array([expm(matrix * x) @ [0.01, -0.02, 1] for x in t])
    np.testing.assert_allclose(result['recoverable'], expected[:, 0], atol=2e-12)
    np.testing.assert_allclose(result['remodeled'], expected[:, 1], atol=2e-12)


def test_zero_load_does_not_invent_a_curve():
    result = simulate([0, 10], kr=0.3, kg=1)
    np.testing.assert_array_equal(result['total'], [0, 0])


def test_no_growth_does_not_create_remodeled_deviation():
    result = simulate([0, 10], kr=0.3, kg=0, forcing=0.02)
    np.testing.assert_array_equal(result['remodeled'], [0, 0])


def test_mirrored_forcing_preserves_sign_symmetry_and_convergence():
    t = np.linspace(0, 10, 101)
    kwargs = dict(kr=0.3, kg=lambda x: 0.5 * np.exp(-((x - 5) / 2)**2), kh=0.1)
    positive = simulate(t, forcing=lambda x: 0.02 * np.sin(x), **kwargs)
    negative = simulate(t, forcing=lambda x: -0.02 * np.sin(x), **kwargs)
    fine = simulate(t, forcing=lambda x: 0.02 * np.sin(x), max_step=0.025, **kwargs)
    np.testing.assert_allclose(positive['total'], -negative['total'], atol=1e-12)
    np.testing.assert_allclose(positive['total'], fine['total'], atol=1e-10)


def test_reverse_remodeling_allows_correction_after_growth_ceases():
    t = np.linspace(0, 10, 21)
    result = simulate(t, kr=1, kg=0, kh=0.2, initial=(0, 0.02))
    np.testing.assert_allclose(result['remodeled'], 0.02 * np.exp(-0.2*t), atol=2e-12)


@pytest.mark.parametrize('kwargs', [dict(kr=-1, kg=0), dict(kr=0, kg=np.nan),
                                     dict(kr=0, kg=0, forcing=np.inf)])
def test_invalid_physical_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        simulate([0, 1], **kwargs)
