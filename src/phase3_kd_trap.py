#!/usr/bin/env python3
"""
Phase 3: The Derivative Gain Trap — Expanded Simulations
=========================================================
Tests Hypothesis B: Non-monotonic K_d–τ* relationship creates a
therapeutic paradox where over-aggressive corrective velocity
worsens stability.

New sweeps:
  A) Fine-grained K_d sweep (50 values) at multiple K_p levels
  B) K_d × τ 2D stability map (heat map)
  C) Growth-phase transient at different K_d values
  D) Optimal K_d envelope across K_p values
  E) Stochastic K_d sensitivity (noise near boundary)
"""

import json
import os

import numpy as np

# ============================================================
# Physical parameters (same as original)
# ============================================================
I = 0.8
b = 1.0
m = 25.0
g = 9.81
L = 0.30
mgl = m * g * L  # 73.575
K_p_default = 120.0
K_d_default = 8.0

print("=" * 60)
print("PHASE 3: DERIVATIVE GAIN TRAP — EXPANDED SIMULATIONS")
print("=" * 60)
print(f"  mgL = {mgl:.3f}")
print(f"  K_p(default) = {K_p_default}, margin = {K_p_default - mgl:.1f}")
print()


def simulate_dde(tau_eff, duration=20.0, dt=0.0005, theta0=0.05,
                 Kp=None, Kd=None, noise_sigma=0.0, seed=42,
                 Kp_func=None, Kd_func=None):
    if Kp is None: Kp = K_p_default
    if Kd is None: Kd = K_d_default

    N = int(duration / dt)
    ds = max(int(tau_eff / dt), 1) if tau_eff > 0 else 0

    th = np.zeros(N + ds)
    dth = np.zeros(N + ds)
    th[:ds+1] = theta0

    rng = np.random.RandomState(seed)
    AMP_CAP = 50.0

    for i in range(ds, ds + N - 1):
        t_now = (i - ds) * dt
        Kp_now = Kp_func(t_now) if Kp_func else Kp
        Kd_now = Kd_func(t_now) if Kd_func else Kd

        th_d = th[i - ds] if ds > 0 else th[i]
        dth_d = dth[i - ds] if ds > 0 else dth[i]

        noise = noise_sigma * rng.randn() * np.sqrt(dt) if noise_sigma > 0 else 0.0
        ddth = (mgl * th[i] - b * dth[i] - Kp_now * th_d - Kd_now * dth_d + noise) / I

        dth[i+1] = dth[i] + ddth * dt
        th[i+1] = th[i] + dth[i+1] * dt

        if abs(th[i+1]) > AMP_CAP:
            th[i+1:] = AMP_CAP * np.sign(th[i+1])
            dth[i+1:] = 0
            break

    t = np.arange(N) * dt
    return t, th[ds:ds+N]


def stability_metrics(t, theta):
    N = len(theta)
    e = int(N * 0.15)
    l_idx = int(N * 0.85)

    early_rms = np.sqrt(np.mean(theta[:e]**2)) + 1e-15
    late_rms = np.sqrt(np.mean(theta[l_idx:]**2)) + 1e-15
    ratio = late_rms / early_rms
    mx = np.max(np.abs(theta))

    sig = theta[l_idx:]
    dt_val = t[1] - t[0]
    freqs = np.fft.rfftfreq(len(sig), d=dt_val)
    mag = np.abs(np.fft.rfft(sig))
    if len(mag) > 1:
        dom_idx = np.argmax(mag[1:]) + 1
        dom_freq = freqs[dom_idx]
    else:
        dom_freq = 0.0

    return {
        'amp_ratio': float(ratio),
        'max_amp': float(mx),
        'early_rms': float(early_rms),
        'late_rms': float(late_rms),
        'unstable': bool(ratio > 2.5 or mx > 1.0),
        'dom_freq_hz': float(dom_freq)
    }


def analytical_hopf_boundary(Kp, Kd):
    omega_grid = np.linspace(0.5, 40, 2000)
    best_residual = np.inf
    best_tau = None

    for omega in omega_grid:
        lhs = Kp**2 + (Kd * omega)**2
        rhs = (b * omega)**2 + (I * omega**2 + mgl)**2
        if abs(lhs - rhs) / max(lhs, rhs) < 0.001:
            A = I * omega**2 + mgl
            B = b * omega
            denom = Kp**2 + (Kd * omega)**2
            cos_wt = (A * Kp - B * Kd * omega) / denom
            sin_wt = (A * Kd * omega + B * Kp) / denom
            if abs(cos_wt) <= 1.01 and abs(sin_wt) <= 1.01:
                cos_wt = np.clip(cos_wt, -1, 1)
                sin_wt = np.clip(sin_wt, -1, 1)
                wt = np.arctan2(sin_wt, cos_wt)
                if wt < 0: wt += 2 * np.pi
                tau_c = wt / omega
                if 0.001 < tau_c < 0.5:
                    r_real = -I*omega**2 - mgl + Kp*np.cos(omega*tau_c) + Kd*omega*np.sin(omega*tau_c)
                    r_imag = b*omega - Kp*np.sin(omega*tau_c) + Kd*omega*np.cos(omega*tau_c)
                    residual = r_real**2 + r_imag**2
                    if residual < best_residual:
                        best_residual = residual
                        best_tau = tau_c
    return best_tau


# ============================================================
# SWEEP A: Fine-grained K_d sweep at multiple K_p levels
# ============================================================
print("SWEEP A: Fine K_d sweep across K_p levels")
print("-" * 50)

Kd_fine = np.concatenate([
    np.linspace(1, 5, 10),
    np.linspace(5, 20, 30),
    np.linspace(20, 50, 15)
])
Kp_levels = [90, 100, 120, 150, 200]

sweep_a = {}
for kp in Kp_levels:
    results_kp = []
    for kd in Kd_fine:
        # Find tau_crit via simulation
        tc = None
        for tau in np.arange(0, 0.401, 0.004):
            t, th = simulate_dde(tau, Kd=kd, Kp=kp, duration=15.0)
            met = stability_metrics(t, th)
            if met['unstable']:
                tc = tau
                break
        # Also analytical
        tc_ana = analytical_hopf_boundary(kp, kd)
        results_kp.append({
            'Kd': float(kd),
            'tau_crit_sim': float(tc) if tc else None,
            'tau_crit_ana': float(tc_ana) if tc_ana else None
        })
    sweep_a[str(kp)] = results_kp

    # Print summary
    best = max(results_kp, key=lambda x: x['tau_crit_sim'] if x['tau_crit_sim'] else 0)
    print(f"  Kp={kp}: optimal Kd={best['Kd']:.1f} → τ*={best['tau_crit_sim']:.3f}s")


# ============================================================
# SWEEP B: K_d × τ 2D stability map
# ============================================================
print("\nSWEEP B: K_d × τ stability heat map")
print("-" * 50)

Kd_grid = np.linspace(1, 50, 50)
tau_grid = np.arange(0, 0.301, 0.004)
stability_map = np.zeros((len(Kd_grid), len(tau_grid)))

for i, kd in enumerate(Kd_grid):
    for j, tau in enumerate(tau_grid):
        t, th = simulate_dde(tau, Kd=kd, duration=15.0)
        met = stability_metrics(t, th)
        stability_map[i, j] = min(met['amp_ratio'], 100)

print(f"  Grid: {len(Kd_grid)} Kd × {len(tau_grid)} tau = {len(Kd_grid)*len(tau_grid)} simulations")


# ============================================================
# SWEEP C: Growth transient at different K_d values
# ============================================================
print("\nSWEEP C: Growth-phase transient at varying K_d")
print("-" * 50)

tau_growth = 0.06  # Near critical — in the interesting zone
sweep_c = {}

for kd in [3, 5, 8, 10, 13, 16, 20, 30]:
    def kp_func(t, kd_val=kd):
        Kp_base = 150.0
        Kp_min = 90.0
        dip = (Kp_base - Kp_min) * np.exp(-0.5 * ((t - 7.5) / 2.0)**2)
        return Kp_base - dip

    t_sim, th = simulate_dde(tau_growth, duration=15.0, Kp_func=kp_func, Kp=150.0, Kd=kd)
    mx = np.max(np.abs(th))
    # Also get the time of max amplitude
    t_max = t_sim[np.argmax(np.abs(th))]

    sweep_c[str(kd)] = {
        'theta': th.tolist()[:3000],
        'max_amp': float(mx),
        'max_deg': float(np.degrees(mx)),
        't_peak': float(t_max)
    }
    s = "RUNAWAY" if mx > 1.0 else ("oscillating" if mx > 0.2 else "stable")
    print(f"  Kd={kd:2d}  max|θ|={mx:.4f} rad ({np.degrees(mx):6.1f}°)  peak@{t_max:.1f}s  [{s}]")


# ============================================================
# SWEEP D: Optimal K_d envelope across K_p values
# ============================================================
print("\nSWEEP D: Optimal K_d envelope")
print("-" * 50)

Kp_envelope = np.linspace(80, 300, 45)
sweep_d = []

for kp in Kp_envelope:
    best_kd = None
    best_tc = 0
    all_kd_data = []
    for kd in np.linspace(2, 40, 40):
        tc = None
        for tau in np.arange(0, 0.401, 0.004):
            t, th = simulate_dde(tau, Kd=kd, Kp=kp, duration=12.0)
            met = stability_metrics(t, th)
            if met['unstable']:
                tc = tau
                break
        tc_val = tc if tc else 0.4
        all_kd_data.append({'Kd': float(kd), 'tau_crit': float(tc_val)})
        if tc_val > best_tc:
            best_tc = tc_val
            best_kd = kd

    sweep_d.append({
        'Kp': float(kp),
        'optimal_Kd': float(best_kd) if best_kd else None,
        'max_tau_crit': float(best_tc),
        'kd_profile': all_kd_data
    })
    print(f"  Kp={kp:6.1f}  optimal Kd={best_kd:5.1f}  max τ*={best_tc:.3f}s")


# ============================================================
# SWEEP E: Stochastic K_d sensitivity
# ============================================================
print("\nSWEEP E: Stochastic sensitivity across K_d values")
print("-" * 50)

sweep_e = []
tau_test = 0.06  # Near boundary

for kd in [5, 8, 10, 13, 16, 20, 30]:
    for sigma in [0, 1.0, 3.0, 5.0]:
        trials = []
        for seed in range(30):
            t, th = simulate_dde(tau_test, noise_sigma=sigma, seed=seed,
                                 duration=15.0, Kd=kd)
            trials.append(float(np.max(np.abs(th))))
        sweep_e.append({
            'Kd': float(kd),
            'sigma': float(sigma),
            'tau': float(tau_test),
            'mean_max': float(np.mean(trials)),
            'std_max': float(np.std(trials)),
            'pct_unstable': float(100 * np.mean([x > 0.5 for x in trials])),
            'max_max': float(np.max(trials)),
            'min_max': float(np.min(trials))
        })

    print(f"  Kd={kd:2d}  σ=0: {sweep_e[-4]['mean_max']:.4f}  "
          f"σ=5: {sweep_e[-1]['mean_max']:.4f}  "
          f"({sweep_e[-1]['pct_unstable']:.0f}% unstable)")


# ============================================================
# SWEEP F: Time-series at key K_d values for illustration
# ============================================================
print("\nSWEEP F: Illustrative time series at varying K_d")
print("-" * 50)

tau_illustrate = 0.07  # Slightly past boundary for some Kds
sweep_f = {}

for kd in [5, 10, 15, 25]:
    t_sim, th = simulate_dde(tau_illustrate, Kd=kd, duration=15.0)
    met = stability_metrics(t_sim, th)
    sweep_f[str(kd)] = {
        't': t_sim[::20].tolist(),  # Subsample for storage
        'theta': th[::20].tolist(),
        'metrics': met
    }
    s = "UNSTABLE" if met['unstable'] else "stable"
    print(f"  Kd={kd:2d}  τ={tau_illustrate}s  max={met['max_amp']:.4f}  [{s}]")


# ============================================================
# Save all results
# ============================================================
results = {
    'params': {
        'I': I, 'b': b, 'm': m, 'g': g, 'L': L, 'mgl': mgl,
        'Kp_default': K_p_default, 'Kd_default': K_d_default
    },
    'sweep_a_kd_fine': sweep_a,
    'sweep_b_stability_map': {
        'Kd': Kd_grid.tolist(),
        'tau': tau_grid.tolist(),
        'map': stability_map.tolist()
    },
    'sweep_c_growth_kd': sweep_c,
    'sweep_d_optimal_envelope': sweep_d,
    'sweep_e_stochastic_kd': sweep_e,
    'sweep_f_timeseries': sweep_f,
    'tau_growth_sweep_c': tau_growth,
    'tau_illustrate_sweep_f': tau_illustrate
}

os.makedirs('/sessions/gracious-relaxed-dirac/mnt/life/results', exist_ok=True)
with open('/sessions/gracious-relaxed-dirac/mnt/life/results/kd_trap_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n✓ All Phase 3 sweeps complete. Results saved to results/kd_trap_results.json")
