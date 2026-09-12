"""Signed recovery/remodeling comparator proposed in the 2026-09-08 review.

e and p are curvature deviations (1/m); forcing is curvature rate (1/m/year).
kr, kg, kh are nonnegative rates (1/year). This is a reduced hypothesis model,
not a clinical Cobb-angle model or a validated stress-to-growth law.
"""
from collections.abc import Callable

import numpy as np
from scipy.integrate import solve_ivp

Rate = float | Callable[[float], float]


def simulate(times, *, kr: Rate, kg: Rate, kh: Rate = 0.0,
             forcing: Rate = 0.0, initial=(0.0, 0.0), max_step=np.inf):
    """Integrate de/dt=u-(kr+kg)e and dp/dt=kg*e-kh*p.

    Time starts at times[0]. Callables allow measured growth/load histories.
    For discontinuous histories, integrate separate intervals at each jump.
    No rectification, fixed positive seed, or flexibility ratio is imposed.
    """
    times = np.asarray(times, dtype=float)
    initial = np.asarray(initial, dtype=float)
    if (times.ndim != 1 or len(times) < 2 or not np.isfinite(times).all()
            or not np.all(np.diff(times) > 0)):
        raise ValueError("times must be finite, strictly increasing, and contain at least 2 points")
    if initial.shape != (2,) or not np.isfinite(initial).all():
        raise ValueError("initial must contain two finite signed curvature deviations")
    if np.isnan(max_step) or max_step <= 0:
        raise ValueError("max_step must be positive")

    def value(rate, t, name, nonnegative=True):
        result = float(rate(t) if callable(rate) else rate)
        if not np.isfinite(result) or (nonnegative and result < 0):
            raise ValueError(f"{name} must be finite" + (" and nonnegative" if nonnegative else ""))
        return result

    def rhs(t, state):
        r, g, h = (value(rate, t, name) for rate, name in
                   ((kr, "kr"), (kg, "kg"), (kh, "kh")))
        u = value(forcing, t, "forcing", nonnegative=False)
        e, p = state
        return [u - (r + g) * e, g * e - h * p]

    solution = solve_ivp(rhs, (times[0], times[-1]), initial, t_eval=times,
                         rtol=1e-10, atol=1e-12, max_step=max_step)
    if not solution.success:
        raise RuntimeError(solution.message)
    return {"time_years": solution.t, "recoverable": solution.y[0],
            "remodeled": solution.y[1], "total": solution.y.sum(axis=0)}
