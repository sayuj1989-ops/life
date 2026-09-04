#!/usr/bin/env python3
"""Exact Hopf boundary for the delayed-PD inverted-pendulum spine model.

    I*theta'' + b*theta' - mgL*theta + Kp*theta(t-tau) + Kd*theta'(t-tau) = 0
    Char eq:  I s^2 + b s - mgL + (Kp + Kd s) e^{-tau s} = 0

Substituting s = i*w, separating real/imaginary, and eliminating
(cos w*tau, sin w*tau) via cos^2+sin^2=1 gives an EXACT quadratic in x = w^2
(verified symbolically: cos^2+sin^2-1 == [quadratic] / (Kd^2 x + Kp^2)):

    I^2 x^2 + (2 I mgL + b^2 - Kd^2) x + (mgL^2 - Kp^2) = 0

Positive root -> omega = sqrt(x); tau* = atan2(sin, cos)/omega from the exact
2x2 linear system. No grid search, no simulation, no amplitude classifier.

Two structural facts, immediate from the coefficients:
  * Kp > mgL makes the constant term negative, so there is ALWAYS exactly one
    positive x: no (Kp > mgL, Kd >= 0) pair is delay-unconditionally stable.
  * tau*(Kd) is non-monotonic with a single interior maximum: the derivative
    gain trap ridge.
"""
import math
import numpy as np

# Paper parameters (phase3_kd_trap.py)
I, b, m, g, L = 0.8, 1.0, 25.0, 9.81, 0.30
mgL = m * g * L  # 73.575


def tau_star(Kp, Kd):
    """Exact critical delay (s) of the Hopf crossing, or None if no crossing."""
    A = I * I
    B = 2 * I * mgL + b * b - Kd * Kd
    C = mgL * mgL - Kp * Kp
    disc = B * B - 4 * A * C
    if disc < 0:
        return None
    xs = [x for x in ((-B + math.sqrt(disc)) / (2 * A),
                      (-B - math.sqrt(disc)) / (2 * A)) if x > 0]
    if not xs:
        return None
    w = math.sqrt(max(xs))
    # Exact linear system for c = cos(w tau), s = sin(w tau):
    #   Kd w c - Kp s   = -b w
    #   Kp c   + Kd w s = I w^2 + mgL
    det = (Kd * w) ** 2 + Kp ** 2
    c = (-b * w * Kd * w + Kp * (I * w * w + mgL)) / det
    s = (Kd * w * (I * w * w + mgL) + b * w * Kp) / det
    tau = math.atan2(s, c) / w
    if tau <= 0:
        tau += 2 * math.pi / w
    return tau, w


def peak(Kp, lo=0.5, hi=40.0):
    """Kd maximising tau*(Kp, Kd): coarse scan + ternary refine (ridge is unimodal)."""
    def f(k):
        r = tau_star(Kp, k)
        return r[0] if r else -1.0
    grid = np.linspace(lo, hi, 4000)
    j = int(np.argmax([f(k) for k in grid]))
    a, b_ = grid[max(j - 1, 0)], grid[min(j + 1, len(grid) - 1)]
    for _ in range(60):
        m1 = a + (b_ - a) / 3
        m2 = b_ - (b_ - a) / 3
        if f(m1) < f(m2):
            a = m1
        else:
            b_ = m2
    k = 0.5 * (a + b_)
    return k, f(k)


if __name__ == "__main__":
    print(f"mgL = {mgL}")
    print("Kp=120  exact tau* table:")
    for Kd in (4, 8, 12, 13, 20):
        t, w = tau_star(120.0, float(Kd))
        print(f"  Kd={Kd:2d}  tau* = {t*1000:5.1f} ms  (omega={w:.3f} rad/s)")
    k, t = peak(120.0)
    print(f"  peak: Kd* = {k:.1f}, tau* = {t*1000:.1f} ms")
    k, t = peak(200.0)
    print(f"  Kp=200 peak: Kd* = {k:.1f}, tau* = {t*1000:.1f} ms")
