#!/usr/bin/env python3
"""
Recovery-Ratchet model of AIS onset.
====================================

Replaces the inverted-pendulum / delay-Hopf "Derivative Gain Trap" (phase3_kd_trap.py,
now a complementary fast-loop model in Supplementary) as the LEAD onset mechanism.

Core idea: the spine actively recovers its reference geometry after perturbation. AIS is
NOT an oscillatory balance instability (that is the signature of CP/Down-type global
sensorimotor disease; AIS patients are dynamically fit). It is a slow RATE COMPETITION:

    geometric-restoration rate k_r   vs   growth-remodeling rate k_g(t)

k_g(t) tracks growth velocity and peaks at peak-height-velocity (PHV). Hueter-Volkmann:
a sustained elastic deviation is cemented into permanent set at rate k_g. When
k_g >~ k_r during the spurt, each perturbation is partly cemented before it can be
recovered -> the deviation RATCHETS (a loaded spring that cannot recoil) -> permanent
progressive curve. This reproduces: PHV-clustered onset, asymptomatic/incidental
detection (the failed loop is slow-geometric, not fast-balance), and -- the falsifiable
clinical signature -- DECLINING CURVE FLEXIBILITY/REDUCIBILITY as the curve progresses.

State (deviation from healthy reference curvature, arbitrary units):
    kappa_e   passive ELASTIC (recoverable) deflection under gravity load -- the part
              that disappears supine / under bending. ~constant reducible deflection.
    kappa_p   permanently remodeled ("set") component   (monotone non-decreasing)
    kappa     total standing curve = kappa_e + kappa_p

Derivation of the cementing law (why it is k_g/(k_r+k_g), not ad hoc):
A perturbation injects an elastic deflection that (i) recoils at rate k_r and (ii) is
cemented by Hueter-Volkmann remodeling at rate k_g. For an impulse A,
kappa_e(t)=A e^{-(k_r+k_g)t}; the cemented amount is integral(k_g*kappa_e) = A*k_g/(k_r+k_g).
=> the CEMENTED FRACTION per perturbation is exactly k_g/(k_r+k_g): ~0 when k_r>>k_g
(spring recoils, nothing sets), ~>=1/2 when k_g>~k_r (cannot recoil before it sets).
So with a characteristic reducible deflection kappa_e0 and growth-driven k_g(t):

    dkappa_p/dt = k_g(t) * kappa_e0 * [ k_g(t) / (k_r + k_g(t)) ]

OBSERVABLE  flexibility(t) = kappa_e0 / (kappa_e0 + kappa_p) = reducible fraction of the
standing curve = what disappears supine / under bending. Declines as kappa_p ratchets up
-> directly testable on supine-vs-standing Cobb and bending-film reducibility
(see flexibility_validation_PLAN).
"""
from __future__ import annotations
import json
import os
import numpy as np
from scipy.integrate import solve_ivp

# ----------------------------------------------------------------------------
# Developmental growth-velocity profile (drives k_g). Normalized human spine
# growth: near-zero in childhood, sharp PHV peak ~12 y, decaying to maturity ~18 y.
# Window 5-20 y matches results.tex Lambda(t) / Energy-Deficit-Window timing.
# ----------------------------------------------------------------------------
AGE_START, AGE_END = 5.0, 20.0
PHV_AGE, PHV_SIGMA = 12.0, 1.6          # peak-height-velocity centre / spread (years)
KAPPA_E0 = 0.02                          # characteristic reducible (elastic) deflection;
                                         # the passive gravity deflection seen standing

def growth_velocity(t):
    """Normalized growth velocity, peak 1.0 at PHV (Gaussian spurt on a low baseline)."""
    baseline = 0.08
    spurt = np.exp(-0.5 * ((t - PHV_AGE) / PHV_SIGMA) ** 2)
    v = baseline + spurt
    return v / (baseline + 1.0)

def simulate(k_r, k_g_peak, kappa_e0=KAPPA_E0, t_span=(AGE_START, AGE_END), n=600):
    """Integrate the recovery-ratchet over the growth window. The cemented fraction of
    the reducible deflection is k_g/(k_r+k_g) (derived above); k_g(t)=k_g_peak*growth_velocity(t)."""
    def rhs(t, y):
        kappa_p = y[0]
        k_g = k_g_peak * growth_velocity(t)
        cemented_fraction = k_g / (k_r + k_g)
        return [k_g * kappa_e0 * cemented_fraction]      # >=0 -> kappa_p monotone (ratchet)

    t_eval = np.linspace(*t_span, n)
    sol = solve_ivp(rhs, t_span, [0.0], t_eval=t_eval, method="LSODA",
                    rtol=1e-9, atol=1e-12)
    kappa_p = sol.y[0]
    kappa_e = np.full_like(kappa_p, kappa_e0)            # reducible deflection (constant)
    kappa = kappa_e + kappa_p                            # total standing curve
    flexibility = kappa_e / kappa                        # reducible fraction in (0,1]
    return {
        "age": sol.t, "kappa": kappa, "kappa_p": kappa_p,
        "kappa_e": kappa_e, "flexibility": flexibility,
        "kappa_p_final": float(kappa_p[-1]),
        "flexibility_final": float(flexibility[-1]),
    }

def phase_sweep(k_r_vals, k_g_vals):
    """Final permanent set kappa_p(maturity) over the (k_r, k_g_peak) grid -> the
    recover-vs-ratchet vulnerability surface that replaces the Hopf tau_c boundary."""
    Z = np.zeros((len(k_g_vals), len(k_r_vals)))
    for i, kg in enumerate(k_g_vals):
        for j, kr in enumerate(k_r_vals):
            Z[i, j] = simulate(kr, kg, n=300)["kappa_p_final"]
    return Z

# ----------------------------------------------------------------------------
def main(outdir=None, figdir=None):
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))      # ~/life
    outdir = outdir or os.path.join(root, "results")
    figdir = figdir or os.path.join(root, "manuscript", "figures")   # manuscript \graphicspath
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(figdir, exist_ok=True)

    # Two representative subjects: fit recoverer vs constitutional progressor.
    # Same growth spurt (k_g_peak); difference is restoration capacity k_r.
    K_G_PEAK = 1.0
    recover = simulate(k_r=6.0, k_g_peak=K_G_PEAK)   # k_r >> k_g  -> recovers
    ratchet = simulate(k_r=0.3, k_g_peak=K_G_PEAK)   # k_r <~ k_g  -> ratchets

    # Phase surface
    k_r_vals = np.linspace(0.1, 3.0, 60)
    k_g_vals = np.linspace(0.1, 3.0, 60)
    Z = phase_sweep(k_r_vals, k_g_vals)

    results = {
        "model": "recovery-ratchet (k_r vs k_g), two-state kappa/kappa_p",
        "params": {"PHV_AGE": PHV_AGE, "PHV_SIGMA": PHV_SIGMA, "kappa_e0": KAPPA_E0,
                   "k_g_peak": K_G_PEAK, "window": [AGE_START, AGE_END]},
        "recover_case": {"k_r": 6.0, "kappa_p_final": recover["kappa_p_final"],
                         "flexibility_final": recover["flexibility_final"]},
        "ratchet_case": {"k_r": 0.3, "kappa_p_final": ratchet["kappa_p_final"],
                         "flexibility_final": ratchet["flexibility_final"]},
        "phase_sweep": {"k_r_vals": k_r_vals.tolist(), "k_g_vals": k_g_vals.tolist(),
                        "kappa_p_final": Z.tolist()},
    }
    jpath = os.path.join(outdir, "recovery_ratchet_results.json")
    with open(jpath, "w") as f:
        json.dump(results, f, indent=2)

    _figure(recover, ratchet, k_r_vals, k_g_vals, Z, figdir)
    print(f"recover: kappa_p_final={recover['kappa_p_final']:.3f}, "
          f"flex_final={recover['flexibility_final']:.2f}")
    print(f"ratchet: kappa_p_final={ratchet['kappa_p_final']:.3f}, "
          f"flex_final={ratchet['flexibility_final']:.2f}")
    print(f"wrote {jpath}")
    return results

def _figure(recover, ratchet, k_r_vals, k_g_vals, Z, figdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))

    # Panel A: trajectories (total kappa + cemented kappa_p) with growth velocity behind
    age = recover["age"]
    gv = np.array([growth_velocity(a) for a in age])
    axb = ax[0].twinx()
    axb.fill_between(age, 0, gv, color="0.85", zorder=0, label="growth velocity")
    axb.set_ylabel("growth velocity (norm.)", color="0.5"); axb.set_ylim(0, 1.6)
    axb.tick_params(axis="y", colors="0.5")
    ax[0].plot(age, recover["kappa"], color="#2c7bb6", lw=2, label="recoverer: total")
    ax[0].plot(age, recover["kappa_p"], color="#2c7bb6", lw=2, ls="--", label="recoverer: set")
    ax[0].plot(age, ratchet["kappa"], color="#d7191c", lw=2, label="progressor: total")
    ax[0].plot(age, ratchet["kappa_p"], color="#d7191c", lw=2, ls="--", label="progressor: set")
    ax[0].set_xlabel("age (years)"); ax[0].set_ylabel("curvature deviation (a.u.)")
    ax[0].set_title("A  Recover vs ratchet")
    ax[0].axvline(PHV_AGE, color="0.6", ls=":", lw=1)
    ax[0].legend(fontsize=7, loc="upper left")

    # Panel B: flexibility(t) -- the clinical observable (reducibility)
    ax[1].plot(age, 100 * recover["flexibility"], color="#2c7bb6", lw=2, label="recoverer")
    ax[1].plot(age, 100 * ratchet["flexibility"], color="#d7191c", lw=2, label="progressor")
    ax[1].axvspan(PHV_AGE - PHV_SIGMA, PHV_AGE + PHV_SIGMA, color="0.9", zorder=0)
    ax[1].set_xlabel("age (years)"); ax[1].set_ylabel("curve flexibility (%)")
    ax[1].set_ylim(0, 105)
    ax[1].set_title("B  Flexibility / reducibility falls as curve sets")
    ax[1].legend(fontsize=8, loc="lower left")

    # Panel C: phase surface -- final permanent set over (k_r, k_g_peak)
    KR, KG = np.meshgrid(k_r_vals, k_g_vals)
    pcm = ax[2].pcolormesh(KR, KG, Z, shading="auto", cmap="magma_r")
    ax[2].plot(k_r_vals, k_r_vals, color="cyan", lw=1.8, ls="--", label="k_g = k_r")
    fig.colorbar(pcm, ax=ax[2], label="permanent curve at maturity (a.u.)")
    ax[2].set_xlabel("restoration rate $k_r$"); ax[2].set_ylabel("peak growth-remodeling $k_g$")
    ax[2].set_title("C  Vulnerability surface (replaces Hopf $\\tau_c$)")
    ax[2].legend(fontsize=8, loc="upper right")

    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(figdir, f"fig_recovery_ratchet.{ext}"), dpi=150,
                    bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {os.path.join(figdir, 'fig_recovery_ratchet.png')}")


if __name__ == "__main__":
    main()
