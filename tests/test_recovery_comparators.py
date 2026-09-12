import numpy as np
import pytest

from scripts.experiments.recovery_comparators import models as M

T = M.grid()
P = M.REFERENCE
LAM = M.lam_peak(P["beta"], P["G_m_peak"], P["c_sigma"], P["w"], P["h"])
CONVERGENCE_TOL = 1e-9

LAW = dict(kr=P["kr"], kg_peak=P["kg_peak"], kappa_e0=P["kappa_e0"])
TWO = dict(kr=P["kr"], kg_peak=P["kg_peak"], kh=0.0, c_load=P["c_load"])
STRESS = dict(lam_peak=LAM, kappa_e0=P["kappa_e0"])
UNLOAD = M.step(1.0, 0.0, 14.0)


def test_grid_carries_the_declared_switch_ages():
    assert 14.0 in T and 18.0 in T


def test_declared_gain_has_units_of_per_year():
    assert LAM == pytest.approx(1.71e-3 * 0.1 / (0.04 * 0.025))


def test_impulse_identity_two_state_with_zero_forcing():
    kr, kg, A = 0.7, 0.3, 0.02
    r = M.two_state(T, kr=kr, kg_peak=kg, kh=0.0, c_load=0.0, growth=lambda t: 1.0,
                    segments=M.constant(0.0), initial=(A, 0.0))
    tau = T - T[0]
    np.testing.assert_allclose(r["recoverable"], A * np.exp(-(kr + kg) * tau), atol=2e-12)
    np.testing.assert_allclose(r["structural"], A * kg / (kr + kg) * (1 - np.exp(-(kr + kg) * tau)),
                               atol=2e-12)


def test_zero_bias_is_exactly_zero_for_every_signed_model():
    zero = M.constant(0.0)
    with np.errstate(invalid="ignore"):  # the unchanged API divides 0/0 for its flexibility ratio
        api = M.ratchet_api(T, kr=P["kr"], kg_peak=P["kg_peak"], kappa_e0=0.0)
    for run in (M.two_state(T, growth=M.growth, segments=zero, **TWO),
                M.stress_growth(T, growth=M.growth, segments=zero, **STRESS),
                M.ratchet_law(T, growth=M.growth, segments=zero, **LAW), api):
        np.testing.assert_array_equal(run["total"], 0.0)


def test_reversed_bias_mirrors_exactly():
    neg = M.transform(UNLOAD, lambda x: -x)
    for fn, kw in ((M.two_state, TWO), (M.stress_growth, STRESS), (M.ratchet_law, LAW)):
        pos = fn(T, growth=M.growth, segments=UNLOAD, **kw)
        mir = fn(T, growth=M.growth, segments=neg, **kw)
        np.testing.assert_allclose(pos["total"], -mir["total"], atol=1e-14)


def test_no_growth_gives_zero_structural_in_all_three_models():
    api = M.ratchet_api(T, kr=P["kr"], kg_peak=0.0, kappa_e0=P["kappa_e0"])
    law = M.ratchet_law(T, growth=M.no_growth, segments=M.constant(1.0), **LAW)
    b = M.two_state(T, growth=M.no_growth, segments=M.constant(1.0), **TWO)
    c = M.stress_growth(T, growth=M.no_growth, segments=M.constant(1.0), **STRESS)
    for run in (api, law, b, c):
        np.testing.assert_array_equal(run["structural"], 0.0)
    # the declared c_load = kr_ref*kappa_e0 makes (b)'s no-growth elastic deviation match (a) and (c)
    assert b["recoverable"][-1] == pytest.approx(P["kappa_e0"] * (1 - np.exp(-P["kr"] * 15)), rel=1e-6)


def test_ratchet_law_quadrature_reproduces_the_unchanged_api():
    api = M.ratchet_api(T, **LAW)
    law = M.ratchet_law(T, growth=M.growth, segments=M.constant(1.0), **LAW)
    np.testing.assert_allclose(law["structural"], api["structural"], atol=CONVERGENCE_TOL)
    assert np.all(np.diff(api["structural"]) >= 0) and np.all(np.diff(api["flexibility"]) <= 0)


def test_integration_converges_within_declared_tolerance():
    for fn, kw in ((M.stress_growth, STRESS), (M.ratchet_law, LAW)):
        mid = fn(T, growth=M.growth, segments=UNLOAD, rtol=1e-8, atol=1e-11, max_step=0.1, **kw)
        tight = fn(T, growth=M.growth, segments=UNLOAD, rtol=1e-10, atol=1e-13, max_step=0.05, **kw)
        assert np.max(np.abs(mid["total"] - tight["total"])) < CONVERGENCE_TOL
    coarse = M.two_state(T, growth=M.growth, segments=UNLOAD, **TWO)
    fine = M.two_state(T, growth=M.growth, segments=UNLOAD, max_step=0.05, **TWO)
    assert np.max(np.abs(coarse["total"] - fine["total"])) < CONVERGENCE_TOL


def test_unloading_discriminates_the_three_models_under_the_declared_protocol():
    a = M.summarize(M.ratchet_law(T, growth=M.growth, segments=UNLOAD, **LAW), t_mark=14.0)
    b_run = M.two_state(T, growth=M.growth, segments=UNLOAD, **TWO)
    b = M.summarize(b_run, t_mark=14.0)
    c = M.summarize(M.stress_growth(T, growth=M.growth, segments=UNLOAD, **STRESS), t_mark=14.0)
    assert a["structural_change_after_mark"] == 0.0
    assert 0.0 < b["recovered_fraction"] < 1.0
    assert 0.0 < b["structural_change_after_mark"] < 0.1 * b["structural_at_mark"]
    assert c["structural_change_after_mark"] > 0.0
    assert c["structural_log_rate_final"] > 5 * b["structural_log_rate_final"] > 0.0
    # (b): the recoverable part decays as exp(-int(kr+kg)) after unloading, not instantly
    i = int(np.searchsorted(T, 14.0))
    from scipy.special import erf
    from spinalmodes.recovery_ratchet import PHV_AGE, PHV_SIGMA
    z = lambda t: (t - PHV_AGE) / (PHV_SIGMA * np.sqrt(2))
    growth_integral = (0.08 * (T[i:] - 14.0) + PHV_SIGMA * np.sqrt(np.pi / 2) * (erf(z(T[i:])) - erf(z(14.0)))) / 1.08
    predicted = np.exp(-(P["kr"] * (T[i:] - 14.0) + P["kg_peak"] * growth_integral))
    np.testing.assert_allclose(b_run["recoverable"][i:], b_run["recoverable"][i] * predicted,
                               rtol=1e-7, atol=1e-12)


def test_unloading_closed_forms_with_constant_growth():
    # with growth held at 1 after unloading both signed models have exact solutions: (b) plateaus at
    # p(14) + kg*e(14)/(kr+kg) (the impulse fraction), (c) keeps growing as kappa_w(14)*exp(lam*dt)
    const = lambda t: 1.0
    kr, kg = P["kr"], P["kg_peak"]
    i = int(np.searchsorted(T, 14.0))
    dt = T[i:] - 14.0
    b = M.two_state(T, growth=const, segments=UNLOAD, **TWO)
    e14, p14 = b["recoverable"][i], b["structural"][i]
    np.testing.assert_allclose(b["structural"][i:], p14 + e14 * kg / (kr + kg) * (1 - np.exp(-(kr + kg) * dt)),
                               atol=1e-10)
    c = M.stress_growth(T, growth=const, segments=UNLOAD, **STRESS)
    np.testing.assert_allclose(c["structural"][i:], c["structural"][i] * np.exp(LAM * dt), rtol=1e-8)
    assert c["structural"][-1] > c["structural"][i] * 2


def test_growth_cessation_stops_structural_change_in_all_three_models():
    seg = M.constant(1.0)
    for fn, kw in ((M.two_state, TWO), (M.stress_growth, STRESS), (M.ratchet_law, LAW)):
        s = M.summarize(fn(T, growth=M.growth_ceasing, segments=seg, **kw), t_mark=19.0)
        # the tanh cutoff leaves growth 3.4e-4 of nominal at 19 y, hence the 1e-4 rather than 0
        assert abs(s["structural_change_after_mark"]) < 1e-4 * abs(s["structural_final"])
