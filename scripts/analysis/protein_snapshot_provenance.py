#!/usr/bin/env python3
"""Provenance audit for the two protein tables in the manuscript.

FINDING (2026-09-04): there are TWO AlphaFold snapshots of the same proteins and
they do not agree:

  * research/alphafold_v6_analysis/protein_metrics.json  ("v6" snapshot)
      -> 72% anisotropy gap, p=0.0105 one-sided (0.021 two-sided), d=1.12,
         n=23 (12 demand / 11 supply).  Matches the printed headline.
  * outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv  (earlier snapshot)
      -> VIM 7.47 (v6: 5.57), PIEZO2 4.44 (v6: 3.45), LBX1 length 281 (v6: 348),
         different uniprot for LBX1 (P52954 vs P52951).  Matches the OLD
         hand-typed dissipation table.

Rule adopted: the v6 JSON is authoritative for every shared protein; proteins
present only in the thermodynamic CSV (NTRK3, DMD, MYLK, FLNA) keep their CSV
values and are flagged with a dagger in the tables. This script prints the
reconciliation so any future table edit is checkable.
"""
import csv
import json
import os

import numpy as np
from scipy.stats import mannwhitneyu

ROOT = os.path.expanduser("~/life")
V6 = os.path.join(ROOT, "research/alphafold_v6_analysis/protein_metrics.json")
THERMO = os.path.join(ROOT, "outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv")

if __name__ == "__main__":
    v6 = json.load(open(V6))
    thermo = {r["gene"]: r for r in csv.DictReader(open(THERMO))}

    print("=== value disagreements between the two snapshots (shared genes) ===")
    for g in sorted(set(v6) & {k.upper() for k in ()} | set(v6)):
        pass
    for g, v in sorted(v6.items()):
        t = thermo.get(g)
        if not t:
            print(f"{g:9s} v6-only")
            continue
        ta = float(t["anisotropy"])
        if abs(ta - v["anisotropy"]) > 0.05:
            print(f"{g:9s} v6={v['anisotropy']:.2f}  thermo={ta:.2f}  delta={ta-v['anisotropy']:+.2f}")

    print("\n=== printed v6-panel statistic (authoritative) ===")
    a_d = [v["anisotropy"] for v in v6.values() if v["category"] == "Demand"]
    a_s = [v["anisotropy"] for v in v6.values() if v["category"] == "Supply"]
    p1 = mannwhitneyu(a_d, a_s, alternative="greater")[1]
    pooled = np.sqrt(((len(a_d)-1)*np.var(a_d, ddof=1) + (len(a_s)-1)*np.var(a_s, ddof=1)) / (len(a_d)+len(a_s)-2))
    print(f"n={len(a_d)}/{len(a_s)} mean {np.mean(a_d):.2f} vs {np.mean(a_s):.2f}"
          f" p1={p1:.4f} p2={2*p1:.4f} d={(np.mean(a_d)-np.mean(a_s))/pooled:.2f}"
          f" ratio={np.mean(a_d)/np.mean(a_s):.3f}")

    print("\n=== genes only in thermodynamic CSV (dagger-flagged) ===")
    print(sorted(set(thermo) - set(v6)))
