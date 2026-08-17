"""Re-derive the delay-Hopf falsification numbers from the model's own parameters.

Model (experiment_temporal_mismatch_dynamics.py):
    L(t)  logistic 0.6 -> 1.7 m, k=1.2, centred age 12
    tau   = tau_0 + L/v,  tau_0 = 0.05 s
    gains Kp = 20*L, Kd = 8*L, m = 1  (so Kp/(mL^2)=20/L, Kd/(mL^2)=8/L)

Delayed-PD inverted pendulum characteristic equation:
    lam^2 - g/L + (p + d*lam) exp(-lam*tau) = 0,   p = 20/L, d = 8/L

Hopf boundary: lam = i*w  =>
    real:  -w^2 - a + p cos(w tau) + d w sin(w tau) = 0
    imag:  -p sin(w tau) + d w cos(w tau) = 0
"""
import numpy as np
from scipy.optimize import brentq

G = 9.81


def L_of_age(age):
    return 0.6 + 1.1 / (1.0 + np.exp(-1.2 * (age - 12.0)))


def tau_of(age, v):
    return 0.05 + L_of_age(age) / v


def tau_crit(L):
    """Smallest tau>0 on the Hopf boundary for the delayed-PD inverted pendulum."""
    a, p, d = G / L, 20.0 / L, 8.0 / L

    # From imag part: tan(w*tau) = d*w/p  ->  w*tau = arctan(d*w/p) in (0, pi/2)
    # Substitute into real part and solve for w.
    def real_resid(w):
        wt = np.arctan(d * w / p)
        return -w * w - a + p * np.cos(wt) + d * w * np.sin(wt)

    # real_resid(0) = -a + p > 0 requires p > a i.e. 20/L > 9.81/L  -> always true
    lo, hi = 1e-6, 1e-6
    for _ in range(400):
        hi *= 1.05
        if real_resid(hi) < 0:
            break
    else:
        return np.nan
    w = brentq(real_resid, lo, hi, xtol=1e-14)
    return np.arctan(d * w / p) / w


ages = np.array([5.0, 20.0])
print(f"{'v (m/s)':>8} | {'age':>4} {'L (m)':>7} {'tau (s)':>8} "
      f"{'tau/sqrt(L/g)':>14} {'tau_c (s)':>10} {'tau/tau_c':>10}")
print("-" * 78)

for v in (15.0, 55.0):
    vals = {}
    for age in ages:
        L = L_of_age(age)
        tau = tau_of(age, v)
        dimless = tau / np.sqrt(L / G)
        tc = tau_crit(L)
        vals[age] = (dimless, tau / tc)
        print(f"{v:>8.0f} | {age:>4.0f} {L:>7.4f} {tau:>8.5f} "
              f"{dimless:>14.5f} {tc:>10.5f} {tau/tc:>10.4f}")
    d0, u0 = vals[5.0]
    d1, u1 = vals[20.0]
    print(f"{'':>8} | dimensionless delay change 5->20: {100*(d1-d0)/d0:+.1f}%")
    print(f"{'':>8} | utilisation tau/tau_c        5->20: {u0:.3f} -> {u1:.3f} "
          f"({100*(u1-u0)/u0:+.1f}%)")
    print("-" * 78)

# Does utilisation cross 1 at ANY age, for either velocity?
fine = np.linspace(5, 20, 601)
for v in (15.0, 55.0):
    u = np.array([tau_of(a, v) / tau_crit(L_of_age(a)) for a in fine])
    print(f"v={v:>4.0f} m/s: max utilisation over ages 5-20 = {u.max():.4f} "
          f"at age {fine[u.argmax()]:.1f}  -> crossing tau_c? {'YES' if u.max() >= 1 else 'NO'}")
