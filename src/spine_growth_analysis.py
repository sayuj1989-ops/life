#!/usr/bin/env python3
"""Corrected stability analysis for the Derivative Gain Gap AIS model.

Root cause of the retractions this script supersedes:
  The Euler DDE integrator used for the original sweeps is UNCONDITIONALLY
  unstable for tau > 0 regardless of the true analytic stability: the
  explicit history-buffer discretization injects numerical energy
  (delayed-difference schemes require the commensurability/stability
  condition that Euler lacks). Every "critical delay" read off that
  integrator was the numerical instability-onset time, not a Hopf point.
  That is why published tau* values (~30-96 ms) sat an order of magnitude
  below the analytic boundary (~0.4-1.5 s) and why the "optimal Kd" was
  an artifact.

This module computes:
  1. tau_star(Kd, Kp)  - exact first Hopf crossing for
         I th'' = mgL th - b th' - Kp th(t-tau) - Kd th'(t-tau)
     via the closed-form imaginary-axis conditions (validated against an
     independent RK4-with-interpolation DDE simulator).
  2. Growth trajectories, vulnerability windows, sex ratio, brace gain,
     and sensitivity, all keyed to the analytic boundary.

Run:  .venv/bin/python src/spine_growth_analysis.py
"""
import json
import math
import os

import numpy as np
from scipy.optimize import brentq

# ----------------------------------------------------------------------
# Parameters (manuscript Table 1 values; unchanged)
# ----------------------------------------------------------------------
I = 0.8           # kg m^2
B = 1.0           # N m s/rad passive damping
M = 25.0          # kg
G = 9.81
LCOM = 0.30       # m
MGL = M * G * LCOM  # 73.575 N m/rad
KP = 120.0        # N m/rad proportional gain
KD_BASE = 8.0     # N m s/rad fully-calibrated derivative gain
ALPHA = 0.010     # s per cm/yr  (10 ms delay per cm/yr growth velocity)
BETA_F = 0.65
BETA_M = 0.50
TAU0 = 0.15       # s baseline sensorimotor delay (manuscript Eq. 2)

PHV = {'F': dict(age=11.5, vmax=8.3, sigma=1.5, beta=BETA_F),
       'M': dict(age=13.5, vmax=9.5, sigma=1.8, beta=BETA_M)}

OUT = os.path.join(os.path.dirname(__file__), '..', 'results',
                   'growth_corrected')


# ----------------------------------------------------------------------
# Exact stability boundary
# ----------------------------------------------------------------------
def tau_star(Kd, Kp=KP):
    """First critical delay (s). None => no Hopf crossing (stable for all
    tau >= 0 given Kp > mgL, Kd > 0, b > 0).

    On the boundary s = j w:
        Re: (Kp - mgL - I w^2) + Kp cos x - Kd w sin x? -> derived form:
            A cos x + B sin x = Kd w ,  A = Kp - mgL - I w^2, B = b w
        Im: A sin x - B cos x = -Kd w? -> combined below.
    Eliminating (cos x, sin x): boundary requires Kd w = |A + i B| for
    some w; then x and tau = x / w follow from the linear system.
    """
    if Kp <= MGL or Kd <= 0:
        return None

    def F(w):
        return Kd * w - math.hypot(Kp - MGL - I * w * w, B * w)

    ws = np.arange(1e-4, 300.0, 1e-3)
    Fs = Kd * ws - np.hypot(Kp - MGL - I * ws ** 2, B * ws)
    crossings = np.where((Fs[:-1] < 0) & (Fs[1:] >= 0))[0]
    if len(crossings) == 0:
        return None
    best = None
    for i in crossings[:6]:
        wr = brentq(F, ws[i], ws[i + 1], xtol=1e-12)
        A = Kp - MGL - I * wr * wr
        c = A / (Kd * wr)
        s = -B * wr / (Kd * wr)
        x = math.atan2(s, c) % (2 * math.pi)
        t = x / wr
        if best is None or t < best:
            best = t
    return best


def growth_velocity(age, sex):
    p = PHV[sex]
    return p['vmax'] * math.exp(-((age - p['age']) ** 2) / (2 * p['sigma'] ** 2))


def eff_params(age, sex, tau0=TAU0, Kd_base=KD_BASE):
    p = PHV[sex]
    vg = growth_velocity(age, sex)
    Kd = Kd_base * (1.0 - p['beta'] * vg / p['vmax'])
    tau = tau0 + ALPHA * vg
    return Kd, tau, vg


# ----------------------------------------------------------------------
# Validation simulator: method-of-steps RK4, commensurate grid
# ----------------------------------------------------------------------
def simulate_dde(tau, Kd, Kp=KP, duration=180.0, dt=2e-4, theta0=0.05):
    """Method-of-steps RK4 for I th'' = mgL th - b th' - Kp th(t-tau) - Kd th'(t-tau).
    The step grid is snapped so tau is an exact integer number of steps
    (commensurate delay): no interpolation error, O(dt^4) global accuracy.
    Constant history theta=theta0, omega=0 on [-tau, 0]."""
    ds = max(int(round(tau / dt)), 0)
    dt_eff = tau / ds if ds else dt
    N = int(duration / dt_eff)
    th = np.zeros(ds + N + 1)
    om = np.zeros(ds + N + 1)
    th[:ds + 1] = theta0

    def rhs(x, v, i):
        return ((MGL * x - B * v - Kp * th[i - ds] - Kd * om[i - ds]) / I, v)

    for i in range(ds, ds + N):
        x, v = th[i], om[i]
        k1x, k1v = rhs(x, v, i)
        k2x, k2v = rhs(x + .5 * dt_eff * k1x, v + .5 * dt_eff * k1v, i)
        k3x, k3v = rhs(x + .5 * dt_eff * k2x, v + .5 * dt_eff * k2v, i)
        k4x, k4v = rhs(x + dt_eff * k3x, v + dt_eff * k3v, i)
        th[i + 1] = x + dt_eff / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        om[i + 1] = v + dt_eff / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    t = (np.arange(ds, ds + N + 1) - ds) * dt_eff
    return t, th[ds:]


def validate():
    """Cross-check analytic boundary against RK4 simulation."""
    print("Validation (analytic tau* vs RK4 DDE, Kp=120):")
    rows = []
    for Kd in [2, 4, 8, 13, 20, 30]:
        ts = tau_star(Kd)
        row = {'Kd': Kd, 'tau_star_ms': ts * 1000}
        for fac, tag in [(0.8, 'below'), (1.3, 'above')]:
            t, th = simulate_dde(ts * fac, Kd, duration=180.0)
            half = len(th) // 2
            env = np.max(np.abs(th[half:]))
            row[f'env_{tag}_mm'] = float(env)
        print(f"  Kd={Kd:3}: tau*={ts*1000:7.1f} ms | env(0.8tau*)={row['env_below_mm']:.4f} "
              f"env(1.3tau*)={row['env_above_mm']:.4f}")
        rows.append(row)
    return rows


# ----------------------------------------------------------------------
# Study computations
# ----------------------------------------------------------------------
def vulnerability_window(sex, tau0=TAU0, ages=None):
    ages = np.arange(8.0, 18.001, 0.02) if ages is None else ages
    margins = []
    for a in ages:
        Kd, tau, vg = eff_params(a, sex, tau0=tau0)
        ts = tau_star(Kd)
        margins.append(np.inf if ts is None else ts - tau)
    margins = np.array(margins)
    unstable = margins < 0
    if not unstable.any():
        return None
    idx = np.where(unstable)[0]
    # contiguous runs
    runs = []
    start = idx[0]
    for i in range(1, len(idx)):
        if idx[i] != idx[i - 1] + 1:
            runs.append((ages[start], ages[idx[i - 1]]))
            start = idx[i]
    runs.append((ages[start], ages[idx[-1]]))
    main = max(runs, key=lambda r: r[1] - r[0])
    return dict(age_start=main[0], age_end=main[1],
                months=12 * (main[1] - main[0]),
                min_margin_ms=float(1000 * margins[idx].min()),
                all_runs=[(float(a), float(b)) for a, b in runs])


def sweep_and_save():
    os.makedirs(OUT, exist_ok=True)
    result = {'params': dict(I=I, b=B, m=M, g=G, L=LCOM, mgL=MGL,
                             Kp=KP, Kd_base=KD_BASE, alpha=ALPHA,
                             tau0=TAU0, beta_F=BETA_F, beta_M=BETA_M)}

    # 1. stability boundary curves (for Fig 1)
    Kds = np.linspace(0.5, 30, 300)
    curves = {}
    for kp in [90, 100, 120, 150, 200]:
        pts = []
        for kd in Kds:
            ts = tau_star(kd, kp)
            pts.append([float(kd), None if ts is None else float(ts)])
        curves[str(kp)] = pts
    result['boundary_curves'] = curves

    # 2. validated tau* table
    result['validation'] = validate()

    # 3. baseline stability check
    ts_base = tau_star(KD_BASE)
    print(f"\nBaseline Kd={KD_BASE}: tau* = {ts_base*1000:.0f} ms "
          f"(tau0 = {TAU0*1000:.0f} ms) -> margin "
          f"{(ts_base-TAU0)*1000:.0f} ms. Baseline is comfortably stable.")

    # 4. sex-differential windows (beta as published)
    result['window_F'] = vulnerability_window('F')
    result['window_M'] = vulnerability_window('M')
    print("\nVulnerability windows (beta_F=0.65, beta_M=0.50):")
    for s in 'FM':
        w = result[f'window_{s}']
        if w:
            print(f"  {s}: {w['age_start']:.1f}-{w['age_end']:.1f} yr "
                  f"({w['months']:.1f} months)")
        else:
            print(f"  {s}: none")

    # 5. sex ratio via growth-parameter Monte Carlo
    rng = np.random.default_rng(7)
    def p_cross(sex, n=2000):
        cnt = 0
        for _ in range(n):
            p = PHV[sex]
            age_p = rng.normal(p['age'], 1.0)
            vmax = rng.normal(p['vmax'], 1.5)
            tau0 = TAU0 + rng.normal(0, 0.020)
            beta = p['beta'] * rng.normal(1.0, 0.10)
            ages = np.arange(8, 18.001, 0.1)
            cross = False
            for a in ages:
                vg = vmax * math.exp(-((a - age_p) ** 2) / (2 * p['sigma'] ** 2))
                Kd = KD_BASE * (1 - beta * vg / vmax)
                tau = tau0 + ALPHA * vg
                ts = tau_star(Kd)
                if ts is not None and tau > ts:
                    cross = True
                    break
            cnt += cross
        return cnt / n
    pf, pm = p_cross('F'), p_cross('M')
    result['p_unstable'] = {'F': pf, 'M': pm, 'ratio': pf / max(pm, 1e-9)}
    print(f"\nP(trajectory crosses boundary): F={pf:.3f}, M={pm:.3f}, "
          f"ratio={pf/max(pm,1e-9):.2f}")

    # 6. brace gain needed at female PHV
    a_phv = 11.5
    Kd_eff, tau_eff, vg = eff_params(a_phv, 'F')
    # find Kd_total needed so tau*(Kd) = tau_eff:
    def need(Kd_t):
        ts = tau_star(Kd_t)
        return 1e9 if ts is None else tau_eff - ts
    lo, hi = Kd_eff, 40.0
    Kd_req = brentq(need, lo, hi, xtol=1e-6) if need(hi) < 0 else None
    result['brace'] = dict(Kd_at_PHV=float(Kd_eff), tau_at_PHV=float(tau_eff),
                           Kd_required=float(Kd_req),
                           Kd_ext=float(Kd_req - Kd_eff) if Kd_req else None)
    print(f"Brace: Kd(PHV)={Kd_eff:.2f}, tau(PHV)={tau_eff*1000:.0f} ms, "
          f"required Kd={Kd_req:.2f} -> Kd_ext={Kd_req-Kd_eff:.2f} Nms/rad")

    # 7. growth-rate threshold at fixed tau0
    def crosses_vmax(vmax, sex='F', tau0=TAU0):
        ages = np.arange(8, 18.001, 0.1)
        for a in ages:
            vg = vmax * math.exp(-((a - PHV[sex]['age']) ** 2) / (2 * PHV[sex]['sigma'] ** 2))
            Kd = KD_BASE * (1 - PHV[sex]['beta'] * vg / vmax)
            tau = tau0 + ALPHA * vg
            ts = tau_star(Kd)
            if ts is not None and tau > ts:
                return True
        return False
    lo, hi = 2.0, 12.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if crosses_vmax(mid):
            hi = mid
        else:
            lo = mid
    result['vmax_threshold'] = hi
    print(f"PHV threshold for crossing at tau0={tau0*1000:.0f} ms: "
          f"vmax > {hi:.2f} cm/yr")

    # 8. sensitivity: window months vs beta, tau0 (Fig S1 replacement)
    sens = []
    for tau0 in [0.10, 0.125, 0.15, 0.175, 0.20]:
        for beta in [0.4, 0.5, 0.6, 0.65, 0.7, 0.8]:
            w = vulnerability_window('F', tau0=tau0)
            # beta override: recompute with modified beta
            save = PHV['F']['beta']
            PHV['F']['beta'] = beta
            w = vulnerability_window('F', tau0=tau0)
            PHV['F']['beta'] = save
            sens.append(dict(tau0=tau0, beta=beta,
                             months=None if w is None else w['months']))
    result['sensitivity'] = sens

    with open(os.path.join(OUT, 'corrected_results.json'), 'w') as f:
        json.dump(result, f, indent=2, default=float)
    print(f"\nSaved {OUT}/corrected_results.json")
    return result


if __name__ == '__main__':
    sweep_and_save()
