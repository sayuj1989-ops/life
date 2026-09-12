#!/usr/bin/env python3
"""Kanban t_9f29fa3b: scalar ratchet (a), signed two-state (b) and stress-modulated growth (c)
under one declared loading/growth protocol, with controls, convergence and sensitivity.

Run from ~/life:  PYTHONPATH=src:. .venv/bin/python scripts/experiments/recovery_comparators/run_comparators.py
Writes results/recovery_comparators/results.json and comparators.png.
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
for p in (ROOT, ROOT / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from scripts.experiments.recovery_comparators import models as M  # noqa: E402

OUT = ROOT / "results" / "recovery_comparators"
P = M.REFERENCE
T = M.grid()
MODELS = ("a_ratchet_api", "a_ratchet_law", "b_two_state_kh0", "b_two_state_kh0.2", "c_stress_growth")
GROWTH = {"standard": M.growth, "ceasing_at_18": M.growth_ceasing, "none": M.no_growth}
CONVERGENCE_TOL = 1e-9
NOISE_SUBJECTS, NOISE_SEED = 200, 20260912

UNITS = {
    "time": "years (age)",
    "structural, recoverable, total": "1/m, signed lateral curvature deviation",
    "flexibility": "dimensionless, recoverable/total; null where total is 0",
    "kr, kg_peak, kh, lam_peak, structural_slope_final*": "1/yr (slope: 1/m/yr)",
    "c_load": "1/m/yr", "kappa_e0": "1/m", "beta": "1/MPa", "G_m_peak": "m/yr",
    "c_sigma": "MPa m", "w, h": "m",
    "b(t)": "dimensionless loading-asymmetry index; b=1 is the declared reference asymmetry that "
            "yields recoverable deviation kappa_e0 with no growth",
}


def protocols():
    return {
        "baseline_sustained_unit_load": (M.constant(1.0), "standard"),
        "no_growth": (M.constant(1.0), "none"),
        "zero_bias": (M.constant(0.0), "standard"),
        "reversed_bias": (M.constant(-1.0), "standard"),
        "unload_at_14": (M.step(1.0, 0.0, P["t_unload"]), "standard"),
        "growth_ceases_at_18": (M.constant(1.0), "ceasing_at_18"),
        "unload_at_14_growth_ceases_at_18": (M.step(1.0, 0.0, P["t_unload"]), "ceasing_at_18"),
        "reverse_load_at_14": (M.step(1.0, -1.0, P["t_unload"]), "standard"),
        "reverse_load_at_18_growth_ceases_at_18": (M.step(1.0, -1.0, P["t_cease"]), "ceasing_at_18"),
    }


def api_expressible(segments, growth_key):
    return len(segments) == 1 and growth_key in ("standard", "none")


def run(model, segments, growth_key, p=P, **solver):
    g = GROWTH[growth_key]
    if model == "a_ratchet_api":
        level = segments[0][2](T[0])
        kg_peak = 0.0 if growth_key == "none" else p["kg_peak"]
        with np.errstate(invalid="ignore"):  # the unchanged API divides 0/0 for its flexibility ratio when level=0
            return M.ratchet_api(T, kr=p["kr"], kg_peak=kg_peak, kappa_e0=p["kappa_e0"] * level)
    if model == "a_ratchet_law":
        return M.ratchet_law(T, kr=p["kr"], kg_peak=p["kg_peak"], kappa_e0=p["kappa_e0"],
                             growth=g, segments=segments, **solver)
    if model.startswith("b_two_state"):
        kh = p["kh"] if model.endswith("0.2") else 0.0
        return M.two_state(T, kr=p["kr"], kg_peak=p["kg_peak"], kh=kh, c_load=p["c_load"], growth=g,
                           segments=segments, **{k: v for k, v in solver.items() if k == "max_step"})
    lam = M.lam_peak(p["beta"], p["G_m_peak"], p["c_sigma"], p["w"], p["h"])
    return M.stress_growth(T, lam_peak=lam, kappa_e0=p["kappa_e0"], growth=g, segments=segments, **solver)


def t_mark_for(segments, growth_key):
    if len(segments) > 1:
        return segments[1][0]
    return P["t_cease"] if growth_key == "ceasing_at_18" else None


def downsample(r, every=10):
    return {k: v[::every] for k, v in r.items()}


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, (float, np.floating)):
        return float(o) if np.isfinite(o) else None
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def all_runs():
    full, table = {}, {}
    for model in MODELS:
        full[model], table[model] = {}, {}
        for key, (seg, gk) in protocols().items():
            if model == "a_ratchet_api" and not api_expressible(seg, gk):
                table[model][key] = {"status": "not_expressible",
                                     "why": "recovery_ratchet.simulate has no load input, no growth-history "
                                            "argument and a fixed zero initial state"}
                continue
            r = run(model, seg, gk)
            full[model][key] = r
            table[model][key] = {"status": "ok", "growth": gk, "t_mark": t_mark_for(seg, gk),
                                 "scalars": M.summarize(r, t_mark_for(seg, gk)),
                                 "trajectory": downsample(r)}
    return full, table


def efold_after_unload(r):
    i = int(np.searchsorted(T, P["t_unload"]))
    e0 = r["recoverable"][i]
    j = i + int(np.argmax(np.abs(r["recoverable"][i:]) <= abs(e0) / np.e))
    rate = P["kr"] + P["kg_peak"] * M.growth(T[i:])
    integral = np.concatenate([[0.0], np.cumsum(0.5 * (rate[1:] + rate[:-1]) * np.diff(T[i:]))])
    return {"measured_years": float(T[j] - T[i]),
            "predicted_years_from_int_kr_plus_kg": float(np.interp(1.0, integral, T[i:] - T[i])),
            "instantaneous_1_over_kr_plus_kg_at_unload_years": float(1.0 / rate[0])}


def controls(full, table):
    def sc(model, key, name):
        return table[model][key]["scalars"][name] if table[model][key]["status"] == "ok" else None
    out = {
        "no_growth_max_abs_structural": {m: float(np.max(np.abs(full[m]["no_growth"]["structural"])))
                                         for m in MODELS},
        "zero_bias_max_abs_total": {m: float(np.max(np.abs(full[m]["zero_bias"]["total"]))) for m in MODELS},
        "reversed_bias_mirror_max_abs_residual": {
            m: float(np.max(np.abs(full[m]["baseline_sustained_unit_load"]["total"]
                                   + full[m]["reversed_bias"]["total"]))) for m in MODELS},
        "unload_at_14": {m: {k: sc(m, "unload_at_14", k) for k in
                             ("structural_at_mark", "total_before_mark", "total_final", "recovered_fraction",
                              "structural_change_after_mark", "structural_slope_final",
                              "structural_log_rate_final")} for m in MODELS},
        "unload_recoverable_efold": {m: efold_after_unload(full[m]["unload_at_14"])
                                     for m in ("b_two_state_kh0", "b_two_state_kh0.2")},
        "growth_ceases_at_18": {m: {k: sc(m, "growth_ceases_at_18", k) for k in
                                    ("structural_at_mark", "structural_change_after_mark",
                                     "structural_slope_final", "flexibility_final")} for m in MODELS},
        "correction": {
            "a_ratchet_api": "not expressible: dkappa_p/dt >= 0 by construction and no reverse term",
            "b_kh0.2_vs_kh0_structural_final_baseline": [sc("b_two_state_kh0.2", "baseline_sustained_unit_load", "structural_final"),
                                                         sc("b_two_state_kh0", "baseline_sustained_unit_load", "structural_final")],
            "b_kh0.2_vs_kh0_structural_final_unload14_cease18": [
                sc("b_two_state_kh0.2", "unload_at_14_growth_ceases_at_18", "structural_final"),
                sc("b_two_state_kh0", "unload_at_14_growth_ceases_at_18", "structural_final")],
            "c_no_autonomous_reverse_term": "the Stokes law G=G_m(1-beta(sigma-sigma_m)) reverses wedging only "
                                            "when the net stress asymmetry reverses while G_m>0; no kh analogue",
            "c_reverse_load_at_14_structural_change_after_mark": sc("c_stress_growth", "reverse_load_at_14",
                                                                    "structural_change_after_mark"),
            "c_reverse_load_at_14_structural_at_mark": sc("c_stress_growth", "reverse_load_at_14", "structural_at_mark"),
            "c_reverse_load_at_18_after_cessation_structural_change_after_mark": sc(
                "c_stress_growth", "reverse_load_at_18_growth_ceases_at_18", "structural_change_after_mark"),
        },
    }
    return out


def zero_bias_population():
    from scipy.stats import binomtest, ttest_1samp
    rng = np.random.default_rng(NOISE_SEED)
    finals = {"a_ratchet_law_signed": [], "a_ratchet_law_rectified_abs_b": [], "b_two_state_kh0": [],
              "c_stress_growth": [], "b_two_state_kh0_antithetic_minus_b": []}
    lam = M.lam_peak(P["beta"], P["G_m_peak"], P["c_sigma"], P["w"], P["h"])
    for _ in range(NOISE_SUBJECTS):
        seg = M.noise(rng)
        # same draw with the sign flipped: a linear model must give the exact negative, so any departure of
        # the sign fraction from 0.5 is a property of these draws, not of the model
        finals["b_two_state_kh0_antithetic_minus_b"].append(M.two_state(
            T, kr=P["kr"], kg_peak=P["kg_peak"], kh=0.0, c_load=P["c_load"], growth=M.growth,
            segments=M.transform(seg, lambda x: -x))["total"][-1])
        finals["a_ratchet_law_signed"].append(M.ratchet_law(
            T, kr=P["kr"], kg_peak=P["kg_peak"], kappa_e0=P["kappa_e0"], growth=M.growth, segments=seg)["total"][-1])
        finals["a_ratchet_law_rectified_abs_b"].append(M.ratchet_law(
            T, kr=P["kr"], kg_peak=P["kg_peak"], kappa_e0=P["kappa_e0"], growth=M.growth,
            segments=M.transform(seg, abs))["structural"][-1])
        finals["b_two_state_kh0"].append(M.two_state(
            T, kr=P["kr"], kg_peak=P["kg_peak"], kh=0.0, c_load=P["c_load"], growth=M.growth, segments=seg)["total"][-1])
        finals["c_stress_growth"].append(M.stress_growth(
            T, lam_peak=lam, kappa_e0=P["kappa_e0"], growth=M.growth, segments=seg)["total"][-1])
    out = {"n_subjects": NOISE_SUBJECTS, "seed": NOISE_SEED,
           "forcing": "b(t)=sum_k a_k cos(2 pi f_k t + phi_k)/sqrt(8), a~N(0,1), f~U(0.25,1.5)/yr, phi~U(0,2pi)",
           "a_ratchet_api": "not expressible: kappa_e0 is a fixed magnitude, i.e. rectified by construction"}
    for k, v in finals.items():
        v = np.asarray(v)
        out[k] = {"mean_total_final": float(v.mean()), "sem": float(v.std(ddof=1) / np.sqrt(len(v))),
                  "mean_abs_total_final": float(np.abs(v).mean()),
                  "fraction_positive": float(np.mean(v > 0)), "fraction_negative": float(np.mean(v < 0)),
                  "p_sign_test_two_sided": float(binomtest(int(np.sum(v > 0)), len(v), 0.5).pvalue),
                  "p_mean_zero_two_sided": float(ttest_1samp(v, 0.0).pvalue),
                  "mean_within_2_sem_of_zero": bool(abs(v.mean()) <= 2 * v.std(ddof=1) / np.sqrt(len(v)))}
    out["b_antithetic_max_abs_sum"] = float(np.max(np.abs(np.asarray(finals["b_two_state_kh0"])
                                                          + np.asarray(finals["b_two_state_kh0_antithetic_minus_b"]))))
    out["total_final_per_subject"] = {k: v for k, v in finals.items()}
    return out


def convergence():
    seg = M.step(1.0, 0.0, P["t_unload"])
    levels = [dict(rtol=1e-6, atol=1e-9, max_step=np.inf), dict(rtol=1e-8, atol=1e-11, max_step=0.1),
              dict(rtol=1e-10, atol=1e-13, max_step=0.05)]
    out = {"declared_tolerance_abs_1_per_m": CONVERGENCE_TOL, "protocol": "unload_at_14, standard growth"}
    for model in ("a_ratchet_law", "c_stress_growth"):
        runs = [run(model, seg, "standard", **lv)["total"] for lv in levels]
        out[model] = {"levels": [{k: (None if v == np.inf else v) for k, v in lv.items()} for lv in levels],
                      "max_abs_diff_vs_tightest": [float(np.max(np.abs(r - runs[-1]))) for r in runs[:-1]],
                      "passes": bool(np.max(np.abs(runs[-2] - runs[-1])) < CONVERGENCE_TOL)}
    steps = [np.inf, 0.1, 0.05]
    runs = [run("b_two_state_kh0", seg, "standard", max_step=s)["total"] for s in steps]
    out["b_two_state_kh0"] = {"note": "API pins rtol=1e-10, atol=1e-12; only max_step can be tightened",
                              "max_step_levels": [None, 0.1, 0.05],
                              "max_abs_diff_vs_tightest": [float(np.max(np.abs(r - runs[-1]))) for r in runs[:-1]],
                              "passes": bool(np.max(np.abs(runs[-2] - runs[-1])) < CONVERGENCE_TOL)}
    api = run("a_ratchet_api", M.constant(1.0), "standard")["structural"]
    law = run("a_ratchet_law", M.constant(1.0), "standard", **levels[-1])["structural"]
    out["a_api_LSODA_vs_a_law_RK45_max_abs_diff"] = float(np.max(np.abs(api - law)))
    out["a_api_vs_law_passes"] = bool(np.max(np.abs(api - law)) < CONVERGENCE_TOL)
    return out


def sensitivity():
    base, unload = M.constant(1.0), M.step(1.0, 0.0, P["t_unload"])
    enters = {"a_ratchet_law": ("kr", "kg_peak"), "b_two_state_kh0": ("kr", "kg_peak", "c_load"),
              "c_stress_growth": ("beta",)}
    outputs = ("structural_final", "flexibility_final", "total_peak_abs", "recovered_fraction",
               "structural_change_after_mark")

    def observe(model, p):
        s = M.summarize(run(model, base, "standard", p=p))
        u = M.summarize(run(model, unload, "standard", p=p), t_mark=P["t_unload"])
        return {"structural_final": s["structural_final"], "flexibility_final": s["flexibility_final"],
                "total_peak_abs": s["total_peak_abs"], "recovered_fraction": u["recovered_fraction"],
                "structural_change_after_mark": u["structural_change_after_mark"]}

    out = {"design": "one-at-a-time x0.5 and x1.5 on kr, kg_peak, beta, c_load; outputs from the baseline "
                     "and unload_at_14 protocols; relative change vs reference",
           "degeneracy_note": "in (c) beta, G_m_peak, c_sigma and 1/(w h) enter only through lam_peak, so a "
                              "factor on beta is a factor on any of them; in (b) c_load scales every "
                              "output linearly by construction"}
    for model, params in enters.items():
        ref = observe(model, P)
        out[model] = {"reference": ref}
        for name in ("kr", "kg_peak", "beta", "c_load"):
            if name not in params:
                out[model][name] = "not a parameter of this model"
                continue
            out[model][name] = {}
            for f in (0.5, 1.5):
                p = dict(P, **{name: P[name] * f})
                obs = observe(model, p)
                out[model][name][f"x{f}"] = {
                    k: {"value": obs[k], "relative_change": (obs[k] - ref[k]) / abs(ref[k]) if ref[k] else None,
                        "moves": bool(abs(obs[k] - ref[k]) > 1e-6 * max(abs(ref[k]), 1e-12))}
                    for k in outputs}
    out["c_beta_sweep_declared_range"] = []
    for beta in (P["beta_range"][0], P["beta"], P["beta_range"][1]):
        p = dict(P, beta=beta)
        s = M.summarize(run("c_stress_growth", base, "standard", p=p))
        u = M.summarize(run("c_stress_growth", unload, "standard", p=p), t_mark=P["t_unload"])
        out["c_beta_sweep_declared_range"].append({
            "beta": beta, "lam_peak": M.lam_peak(beta, P["G_m_peak"], P["c_sigma"], P["w"], P["h"]),
            "structural_final_baseline": s["structural_final"],
            "structural_final_over_kappa_e0": s["structural_final"] / P["kappa_e0"],
            "unload_structural_final_over_structural_at_14": u["structural_final"] / u["structural_at_mark"]})
    return out


def imposed_vs_discriminating(table):
    sc = lambda m, k, n: table[m][k]["scalars"][n]
    return {
        "imposed_by_construction": {
            "a_ratchet": ["dkappa_p/dt >= 0 whenever kappa_e0 >= 0: kappa_p monotone, flexibility monotone falling",
                          "kappa_e0 is a fixed unsigned magnitude: the load is a deviation amplitude, not a load, and the "
                          "sign is rectified",
                          "event-rate multiplier nu = kg: rate is kg*kappa_e0*kg/(kr+kg), i.e. kg/kr times the (b) "
                          "quasi-steady rate kg*e_ss with e_ss = kr*kappa_e0/(kr+kg)",
                          "no onset threshold at kg = kr (smooth in kg)", "no recovery and no reverse term",
                          "growth_velocity has a 0.074 baseline at age 20, so set accumulates indefinitely"],
            "b_two_state": ["linear in the forcing: zero bias gives zero, reversal mirrors, output scales with c_load",
                            "e relaxes at kr+kg, so recoverable deviation is smaller during growth by construction",
                            "with kh = 0 p is monotone under one-signed forcing; kh > 0 is a declared, not derived, term",
                            "no onset threshold; no anatomy, no handedness, no 3D"],
            "c_stress_growth": ["dkappa_w/dt = lam(t)*kappa_total with lam > 0 whenever beta*c_sigma > 0 and G_m > 0: "
                                "exponential-type positive feedback with no threshold in this linearisation",
                                "elastic seed kappa_e0*b(t) is quasi-static: unloading removes it instantly",
                                "no recovery variable and no reverse term; correction needs a reversed net stress "
                                "asymmetry during remaining growth",
                                "one-DOF linearisation of the Stokes law, not his finite-element geometry"],
        },
        "discriminating_under_identical_protocol": {
            "unload_at_14_structural_change_after_mark": {m: sc(m, "unload_at_14", "structural_change_after_mark")
                                                          for m in MODELS[1:]},
            "unload_at_14_structural_slope_final": {m: sc(m, "unload_at_14", "structural_slope_final")
                                                    for m in MODELS[1:]},
            "unload_at_14_structural_log_rate_final": {m: sc(m, "unload_at_14", "structural_log_rate_final")
                                                       for m in MODELS[1:]},
            "unload_at_14_recovered_fraction_of_total": {m: sc(m, "unload_at_14", "recovered_fraction")
                                                         for m in MODELS[1:]},
            "baseline_flexibility_rebound_after_PHV": {m: sc(m, "baseline_sustained_unit_load", "flexibility_rebound")
                                                       for m in MODELS},
            "baseline_structural_final_a_over_b_kh0": sc("a_ratchet_api", "baseline_sustained_unit_load", "structural_final")
                                                      / sc("b_two_state_kh0", "baseline_sustained_unit_load", "structural_final"),
            "statement": "the sign and time course of structural change after a load change, and whether the "
                         "recoverable part decays over years or vanishes instantly, differ between models under "
                         "the same protocol; the falling flexibility under sustained load does not",
        },
    }


def figure(full, table, noise):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors = {"a_ratchet_api": "#555555", "b_two_state_kh0": "#2c7bb6", "b_two_state_kh0.2": "#7fb3d5",
              "c_stress_growth": "#d7191c"}
    labels = {"a_ratchet_api": "(a) scalar ratchet", "b_two_state_kh0": "(b) two-state kh=0",
              "b_two_state_kh0.2": "(b) two-state kh=0.2", "c_stress_growth": "(c) stress-modulated growth"}
    fig, ax = plt.subplots(2, 2, figsize=(11, 7.5))
    g = M.growth(T)
    for a in ax[0]:
        a.fill_between(T, 0, g * 0.02, color="0.92", zorder=0)
    for m in colors:
        r = full[m]["baseline_sustained_unit_load"]
        ax[0, 0].plot(T, r["structural"], color=colors[m], lw=1.8, label=labels[m])
        ax[0, 1].plot(T, r["flexibility"], color=colors[m], lw=1.8)
        u = full[m]["unload_at_14"] if m != "a_ratchet_api" else full["a_ratchet_law"]["unload_at_14"]
        ax[1, 0].plot(T, u["total"], color=colors[m], lw=1.8)
    ax[0, 0].set_title("A  structural deviation, b=1 sustained (grey: growth velocity)")
    ax[0, 0].set_ylabel("1/m"); ax[0, 0].legend(fontsize=7)
    ax[0, 1].set_title("B  flexibility = recoverable/total, b=1 sustained"); ax[0, 1].set_ylim(0, 1.05)
    ax[1, 0].set_title("C  total deviation, load removed at 14 y"); ax[1, 0].set_ylabel("1/m")
    ax[1, 0].axvline(P["t_unload"], color="0.6", ls=":")
    finals = noise["total_final_per_subject"]
    bins = np.linspace(-0.06, 0.06, 49)
    for k, c, lab in (("a_ratchet_law_rectified_abs_b", "#555555", "(a) rectified |b|"),
                      ("c_stress_growth", "#d7191c", "(c)"), ("b_two_state_kh0", "#2c7bb6", "(b) kh=0")):
        ax[1, 1].hist(finals[k], bins=bins, color=c, alpha=0.55, label=lab)
    ax[1, 1].axvline(0, color="0.3", lw=0.8)
    ax[1, 1].set_title("D  zero-bias population: total at 20 y (n=%d)" % noise["n_subjects"])
    ax[1, 1].set_xlabel("1/m"); ax[1, 1].legend(fontsize=7)
    for a in ax.flat[:3]:
        a.set_xlabel("age (years)")
    fig.tight_layout()
    fig.savefig(OUT / "comparators.png", dpi=130)
    plt.close(fig)


def summary_table(table, noise):
    def sc(m, k, n):
        return table[m][k]["scalars"][n] if table[m][k]["status"] == "ok" else None
    fmt = lambda v: "   n/a  " if v is None else f"{v:+.2e}" if abs(v) < 1e-3 or abs(v) >= 1e3 else f"{v:8.4f}"
    print(f"{'model':<20}{'S20 base':>10}{'F20 base':>10}{'Frebound':>10}{'unld rec':>10}{'unld dS':>10}"
          f"{'unld dS/dt':>11}{'S20 cease':>10}{'noise f>0':>10}")
    for m in MODELS:
        noise_key = {"a_ratchet_law": "a_ratchet_law_signed", "b_two_state_kh0": "b_two_state_kh0",
                     "c_stress_growth": "c_stress_growth"}.get(m)
        fpos = noise[noise_key]["fraction_positive"] if noise_key else None
        print(f"{m:<20}{fmt(sc(m, 'baseline_sustained_unit_load', 'structural_final')):>10}"
              f"{fmt(sc(m, 'baseline_sustained_unit_load', 'flexibility_final')):>10}"
              f"{fmt(sc(m, 'baseline_sustained_unit_load', 'flexibility_rebound')):>10}"
              f"{fmt(sc(m, 'unload_at_14', 'recovered_fraction')):>10}"
              f"{fmt(sc(m, 'unload_at_14', 'structural_change_after_mark')):>10}"
              f"{fmt(sc(m, 'unload_at_14', 'structural_slope_final')):>11}"
              f"{fmt(sc(m, 'growth_ceases_at_18', 'structural_final')):>10}"
              f"{fmt(fpos):>10}")


def main():
    t0 = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    full, table = all_runs()
    noise = zero_bias_population()
    results = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "kanban": "t_9f29fa3b", "script": str(Path(__file__).relative_to(ROOT)),
        "scope": "synthetic comparison of three reduced models under one declared protocol; no clinical calibration",
        "units": UNITS,
        "declared_parameters": {k: v for k, v in P.items()},
        "lam_peak_1_per_yr": M.lam_peak(P["beta"], P["G_m_peak"], P["c_sigma"], P["w"], P["h"]),
        "grid": {"t0": M.T0, "t1": M.T1, "n": M.N_GRID, "trajectory_downsample": 10},
        "growth_history": "recovery_ratchet.growth_velocity(t) for every model; 'ceasing_at_18' multiplies by "
                          "0.5*(1-tanh((t-18)/0.25))",
        "runs": table, "controls": controls(full, table), "zero_bias_population": noise,
        "convergence": convergence(), "sensitivity": sensitivity(),
        "imposed_vs_discriminating": imposed_vs_discriminating(table),
        "reference_verification_2026-09-12": {
            "PMID_17653775": "Stokes 2007 Eur Spine J 16(10):1621-8, doi 10.1007/s00586-007-0442-7, PMC2078290; PubMed+Crossref+abstract",
            "PMID_8727190": "Stokes, Spence, Aronsson, Kilmer 1996 Spine 21(10):1162-7, doi 10.1097/00007632-199605150-00007; PubMed+abstract",
            "PMID_16705695": "Stokes et al. 2006 J Orthop Res 24(6):1327-34, doi 10.1002/jor.20189, PMC1513139; beta range from abstract",
            "doi_10.1186/1748-7161-1-16": "Stokes, Burwell, Dangerfield 2006 Scoliosis 1:16; Crossref",
            "bib_stokes2006hueter": "doi 10.1007/s00586-006-0082-x -> Crossref 404; title has 0 PubMed hits; unverified",
            "bib_stokes2002mechanical": "doi 10.1097/01.BRS.0000033092.42767.55 -> Crossref 404; carries the 1996 title with "
                                        "2002 volume/pages; PubMed's Stokes Spine 2002 vol 27 record is 27(24):2801-5, a different paper",
        },
        "runtime_s": None,
    }
    results["runtime_s"] = time.perf_counter() - t0
    (OUT / "results.json").write_text(json.dumps(clean(results), indent=1))
    figure(full, table, noise)
    summary_table(table, noise)
    print(f"wrote {OUT / 'results.json'} and comparators.png in {results['runtime_s']:.1f} s")


if __name__ == "__main__":
    main()
