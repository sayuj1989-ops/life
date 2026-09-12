"""Loading/growth protocol helpers and the three comparators for kanban t_9f29fa3b.

Units everywhere: time in years (age), signed lateral curvature deviation in
1/m, rates in 1/yr, forcing in 1/m/yr. Model (a) is reached through
`spinalmodes.recovery_ratchet.simulate` unchanged, model (b) through
`spinalmodes.recovery_two_state.simulate` unchanged, model (c) is a
one-degree-of-freedom linearisation of the Stokes stress-modulated-growth law
(sources and fairness caveats in results/recovery_comparators/METHODS.md).
Nothing here is calibrated to a clinical cohort.
"""
from collections.abc import Callable

import numpy as np
from scipy.integrate import solve_ivp

from spinalmodes import recovery_ratchet, recovery_two_state

T0, T1 = recovery_ratchet.AGE_START, recovery_ratchet.AGE_END
N_GRID = 601  # 0.025 yr step puts the declared switch ages 14.0 and 18.0 exactly on the grid

REFERENCE = {
    "kr": 0.3,                # 1/yr; the ratchet's own "progressor" restoration rate
    "kg_peak": 1.0,           # 1/yr; the ratchet's default remodeling rate at PHV
    "kappa_e0": recovery_ratchet.KAPPA_E0,  # 1/m; recoverable deviation under unit sustained load with no growth
    "c_load": 0.006,          # 1/m/yr = kr_ref*kappa_e0, so (b) at kg=0, b=1 relaxes to kappa_e0; fixed when kr is varied
    "kh": 0.2,                # 1/yr; optional reverse remodeling, the value used in checks.json
    "beta": 1.71,             # 1/MPa; 17.1 % per 0.1 MPa, mean of Stokes et al. 2006 J Orthop Res (abstract)
    "beta_range": (0.92, 2.39),  # 1/MPa; the 9.2-23.9 % per 0.1 MPa range from the same abstract
    "G_m_peak": 1.0e-3,       # m/yr; per-segment height growth at PHV, order-of-magnitude declaration
    "c_sigma": 0.1,           # MPa m; side-to-side stress asymmetry per unit curvature, order-of-magnitude declaration
    "w": 0.04,                # m; lateral width across which the growth-rate difference acts
    "h": 0.025,               # m; segment height turning a wedge angle into curvature
    "t_unload": 14.0,
    "t_cease": 18.0,
    "cease_width": 0.25,      # yr; tanh half-width of the growth cutoff
}

Segments = list[tuple[float, float, Callable[[float], float]]]


def grid():
    return np.linspace(T0, T1, N_GRID)


def growth(t):
    return recovery_ratchet.growth_velocity(t)


def growth_ceasing(t, t_cease=REFERENCE["t_cease"], width=REFERENCE["cease_width"]):
    return growth(t) * 0.5 * (1.0 - np.tanh((t - t_cease) / width))


def no_growth(t):
    return 0.0


def lam_peak(beta, G_m_peak, c_sigma, w, h):
    # growth-rate difference across width w is beta*G_m*c_sigma*kappa (m/yr); wedge-angle rate is that
    # over w (rad/yr); dividing by the segment height h makes it a curvature rate (1/m/yr per 1/m)
    return beta * G_m_peak * c_sigma / (w * h)


def constant(level) -> Segments:
    return [(T0, T1, lambda t: level)]


def step(before, after, t_switch) -> Segments:
    return [(T0, t_switch, lambda t: before), (t_switch, T1, lambda t: after)]


def noise(rng, n_modes=8, f_range=(0.25, 1.5)) -> Segments:
    # random-phase sinusoids: zero mean, law symmetric under b -> -b, and smooth so one solver segment is exact
    a = rng.standard_normal(n_modes)
    f = rng.uniform(*f_range, n_modes)
    ph = rng.uniform(0.0, 2.0 * np.pi, n_modes)
    return [(T0, T1, lambda t: float(np.sum(a * np.cos(2.0 * np.pi * f * t + ph))) / np.sqrt(n_modes))]


def transform(segments, fn) -> Segments:
    return [(a, b, (lambda g: (lambda t: fn(g(t))))(g)) for a, b, g in segments]


def value(segments, t):
    return next(g(t) for a, _, g in reversed(segments) if a <= t)


def _piecewise(times, segments, initial, step_fn):
    state, blocks = np.asarray(initial, dtype=float), []
    for i, (ta, tb, b) in enumerate(segments):
        t_seg = times[(times >= ta) & (times <= tb)]
        y = step_fn(t_seg, state, b)
        blocks.append(y[:, 1:] if i else y)
        state = y[:, -1]
    return np.concatenate(blocks, axis=1)


def _scalar_ode(times, segments, rate, rtol, atol, max_step):
    def step_fn(t_seg, state, b):
        sol = solve_ivp(lambda t, y: [rate(t, y[0], b)], (t_seg[0], t_seg[-1]), state,
                        t_eval=t_seg, method="RK45", rtol=rtol, atol=atol, max_step=max_step)
        return sol.y
    return _piecewise(times, segments, [0.0], step_fn)[0]


def _pack(times, structural, recoverable):
    total = structural + recoverable
    flexibility = np.full_like(total, np.nan)
    ok = np.abs(total) > 1e-15
    flexibility[ok] = recoverable[ok] / total[ok]
    return {"time": np.asarray(times, dtype=float), "structural": structural,
            "recoverable": recoverable, "total": total, "flexibility": flexibility}


def ratchet_api(times, *, kr, kg_peak, kappa_e0):
    r = recovery_ratchet.simulate(kr, kg_peak, kappa_e0=kappa_e0,
                                  t_span=(times[0], times[-1]), n=len(times))
    return _pack(r["age"], r["kappa_p"], r["kappa_e"])


def ratchet_law(times, *, kr, kg_peak, kappa_e0, growth, segments,
                rtol=1e-10, atol=1e-13, max_step=np.inf):
    def rate(t, _, b):
        kg = kg_peak * growth(t)
        return kg * kappa_e0 * b(t) * kg / (kr + kg)
    structural = _scalar_ode(times, segments, rate, rtol, atol, max_step)
    recoverable = kappa_e0 * np.array([value(segments, t) for t in times])
    return _pack(times, structural, recoverable)


def two_state(times, *, kr, kg_peak, kh, c_load, growth, segments,
              initial=(0.0, 0.0), max_step=np.inf):
    def step_fn(t_seg, state, b):
        r = recovery_two_state.simulate(t_seg, kr=kr, kg=lambda t: kg_peak * growth(t), kh=kh,
                                        forcing=lambda t: c_load * b(t), initial=state,
                                        max_step=max_step)
        return np.vstack([r["recoverable"], r["remodeled"]])
    y = _piecewise(times, segments, initial, step_fn)
    return _pack(times, y[1], y[0])


def stress_growth(times, *, lam_peak, kappa_e0, growth, segments,
                  rtol=1e-10, atol=1e-13, max_step=np.inf):
    def rate(t, kappa_w, b):
        # Hueter-Volkmann sign: the compressed (concave) side grows slower, so wedging carries the
        # sign of the total curvature; the elastic seed kappa_e0*b is quasi-static (no recovery state)
        return lam_peak * growth(t) * (kappa_w + kappa_e0 * b(t))
    structural = _scalar_ode(times, segments, rate, rtol, atol, max_step)
    recoverable = kappa_e0 * np.array([value(segments, t) for t in times])
    return _pack(times, structural, recoverable)


def summarize(run, t_mark=None, slope_window_years=1.0):
    t, S, R, T, F = (run[k] for k in ("time", "structural", "recoverable", "total", "flexibility"))
    n = int(round(slope_window_years / (t[1] - t[0])))
    out = {"structural_final": S[-1], "recoverable_final": R[-1], "total_final": T[-1],
           "total_peak_abs": np.max(np.abs(T)), "flexibility_final": F[-1],
           "flexibility_min": np.nanmin(F) if np.isfinite(F).any() else np.nan,
           "structural_slope_final": (S[-1] - S[-1 - n]) / (t[-1] - t[-1 - n])}
    out["flexibility_rebound"] = out["flexibility_final"] - out["flexibility_min"]
    # rate per unit structural deviation: (b) -> 0 as e decays, (c) -> lam(t) while growth continues
    out["structural_log_rate_final"] = out["structural_slope_final"] / S[-1] if S[-1] != 0 else np.nan
    if t_mark is not None:
        i = int(np.searchsorted(t, t_mark))
        # the grid point at t_mark already carries the post-switch load, so "before" reads R one step earlier
        S_m, T_m = S[i], S[i] + R[i - 1]
        out.update(structural_at_mark=S_m, total_before_mark=T_m,
                   structural_change_after_mark=S[-1] - S_m,
                   recovered_fraction=(T_m - T[-1]) / T_m if T_m != 0 else np.nan)
    return {k: float(v) for k, v in out.items()}
