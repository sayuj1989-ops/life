#!/usr/bin/env python3
"""Cross-species B_g panel vs Greenhill self-buckling threshold, done correctly.

Dimensional bookkeeping (the trap that produced the wrong first pass):
  Greenhill alpha = rho*g*A*L^3/EI is the mass loading / flexural resistance.
  The manuscript's B_g = EI/(M g L^2) equals alpha/L for a column of length L
  with M = rho*A*L held FIXED. So B_g > alpha_c/L only under a
  constant-mass scaling (M fixed, L varies) -- which is NOT isometry.
  Under isometry (M ∝ L^3, EI ∝ L^4): alpha ∝ L^3, B_g ∝ L, and the
  threshold in B_g units is alpha_c/L^3.

Which convention is used decides whether the panel looks stable or not,
so this script reports BOTH conventions plus the empirical isometry-slope
check (regress log M vs log L across the panel) that picks one.

Analysis-only; writes results/newton_greenhill/bg_vs_greenhill.{json,csv}.
"""
import csv, json
from pathlib import Path

ALPHA_C = 7.837347
G = 9.81
ROOT = Path.home() / "life"
OUT = ROOT / "results" / "newton_greenhill"

EXCLUDED = {"Giraffe", "Dolphin"}

rows = []
with open(ROOT / "data" / "species_parameters.csv") as f:
    for r in csv.DictReader(f):
        r["Mass_kg"] = float(r["Mass_kg"]); r["Length_m"] = float(r["Length_m"])
        r["EI_Nm2"] = float(r["EI_Nm2"]); r["Bg_reported"] = float(r["Bg"])
        rows.append(r)

for r in rows:
    M, L, EI = r["Mass_kg"], r["Length_m"], r["EI_Nm2"]
    r["Bg_recomputed"] = EI / (M * G * L * L)
    r["alpha"] = (M * G * L**3) / EI
    r["margin_alpha"] = r["alpha"] / ALPHA_C                      # <1 => below critical
    # Convention A: constant-mass scaling (B_g = alpha/L) -> thr = alpha_c/L
    r["thr_constmass"] = ALPHA_C / L
    # Convention B: isometry (B_g ∝ L) -> thr = alpha_c/L^3
    r["thr_iso"] = ALPHA_C / L**3
    r["stable_constmass"] = r["Bg_recomputed"] > r["thr_constmass"]
    r["stable_iso"] = r["Bg_recomputed"] > r["thr_iso"]

panel = [r for r in rows if r["Species"] not in EXCLUDED]

# Empirical isometry slope: log M vs log L across the n=10 panel
import math as st
xs = [st.log(r["Mass_kg"]) for r in panel]; ys = [st.log(r["Length_m"]) for r in panel]
n = len(xs); sx = sum(xs); sy = sum(ys)
slope_ml = sum((x - sx/n) * (y - sy/n) for x, y in zip(xs, ys)) / sum((x - sx/n)**2 for x in xs)
# also EI vs L slope (isometry predicts 4 for solid geometrically similar bodies)
ei_slope = sum((x - sx/n) * (st.log(r["EI_Nm2"]) - sum(st.log(q["EI_Nm2"]) for q in panel)/n)
               for x, r in zip(xs, panel)) / sum((x - sx/n)**2 for x in xs)
print(f"empirical d(log EI)/d(log M) = {ei_slope:.3f}   (solid isometry: EI∝M^2 => slope 2;")
print(f"  length-M∝L^3: EI∝L^4, B_g∝L^1 => thr_iso)")

hdr = (f"{'Species':<14}{'M kg':>8}{'L m':>6}{'Bg':>9}{'alpha':>10}{'a/alphac':>10}"
       f"{'thr/L':>9}{'thr/L3':>10}{'stabA':>7}{'stabB':>7}")
print(hdr)
for r in sorted(rows, key=lambda x: x["Mass_kg"]):
    tag = " (excl)" if r["Species"] in EXCLUDED else ""
    print(f"{r['Species']:<14}{r['Mass_kg']:>8.4g}{r['Length_m']:>6.2f}{r['Bg_recomputed']:>9.4f}"
          f"{r['alpha']:>10.3f}{r['margin_alpha']:>10.3f}{r['thr_constmass']:>9.2f}"
          f"{r['thr_iso']:>10.2f}{str(r['stable_constmass']):>7}{str(r['stable_iso']):>7}{tag}")

for label, key in (("const-mass (thr=alpha_c/L)", "stable_constmass"),
                   ("isometry  (thr=alpha_c/L^3)", "stable_iso")):
    above = [r["Species"] for r in panel if r[key]]
    print(f"\n{n} species above threshold [{label}]: {len(above)}/{n} -> {above}")

# alpha vs L: is alpha^(-1/3) proportional to L? (i.e. does margin scale with length)
print(f"\nlog-log slope d(log alpha)/d(log M) = "
      f"{sum((x - sx/n)*(st.log(r['alpha']) - sum(st.log(q['alpha']) for q in panel)/n) for x,r in zip(xs,panel)) / sum((x-sx/n)**2 for x in xs):.3f}"
      f"   (isometry predicts ~4 for alpha∝L^3 with M∝L^3... check)")

result = {
    "alpha_c": ALPHA_C, "n_panel": n,
    "empirical_dlogEI_dlogM": ei_slope,
    "n_above_constmass": sum(r["stable_constmass"] for r in panel),
    "n_above_iso": sum(r["stable_iso"] for r in panel),
    "species_above_constmass": [r["Species"] for r in panel if r["stable_constmass"]],
    "species_above_iso": [r["Species"] for r in panel if r["stable_iso"]],
    "rows": [{k: r[k] for k in ("Species","Mass_kg","Length_m","EI_Nm2","Posture",
                                "Bg_reported","Bg_recomputed","alpha","margin_alpha",
                                "thr_constmass","thr_iso","stable_constmass","stable_iso")} for r in rows],
}
with open(OUT / "bg_vs_greenhill.json", "w") as f:
    json.dump(result, f, indent=2)
with open(OUT / "bg_vs_greenhill.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(result["rows"][0].keys())
    for r in result["rows"]: w.writerow(r.values())
print(f"\nwrote {OUT}/bg_vs_greenhill.{{json,csv}}")
