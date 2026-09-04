#!/usr/bin/env python3
"""Re-derive every protein-panel statistic printed in the manuscript, directly
from the two authoritative CSVs (outputs/afcc/2026-02-10/metrics.csv and
outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv).

Why this exists: AUDIT_LEDGER O-1 found Table 3 agrees with neither source
(8/22 rows) and the published p=0.011 does not reproduce under any panel
definition. This script is the single source of truth for the corrected
numbers; the manuscript must quote what it prints.
"""
import csv, math, os
from itertools import product

import numpy as np
from scipy.stats import mannwhitneyu

ROOT = os.path.expanduser("~/life")
AFCC = os.path.join(ROOT, "outputs/afcc/2026-02-10/metrics.csv")
THERMO = os.path.join(ROOT, "outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv")

def load(path, key):
    rows = {}
    with open(path) as f:
        for r in csv.DictReader(f):
            rows[r[key]] = r
    return rows

afcc = load(AFCC, "gene_symbol")
thermo = load(THERMO, "gene")

def mwu(a, b):
    u, p = mannwhitneyu(a, b, alternative="greater")
    n1, n2 = len(a), len(b)
    pooled = math.sqrt(((n1-1)*np.var(a, ddof=1) + (n2-1)*np.var(b, ddof=1)) / (n1+n2-2))
    d = (np.mean(a) - np.mean(b)) / pooled if pooled else float("nan")
    return p, d

print("=" * 72)
print("PANEL 1: thermodynamic CSV, term column (a-p = Demand, Gamma_m = Supply)")
dem = [float(r["anisotropy"]) for r in thermo.values() if r["term"] in ("eta_p","eta_a")]
sup = [float(r["anisotropy"]) for r in thermo.values() if r["term"] == "Gamma_m"]
print(f"Demand n={len(dem)} mean={np.mean(dem):.3f}  Supply n={len(sup)} mean={np.mean(sup):.3f}")
p, d = mwu(dem, sup); print(f"MWU p={p:.4f}  d={d:.3f}")

print("=" * 72)
print("PANEL 2: Table-3 membership, values taken from AFCC v6 metrics")
TABLE3_DEMAND = ["VIM","PTK7","LMNA","DSTYK","PIEZO2","PIEZO1","CAV1","FLNA","RUNX3","NTRK3","EGR3","LBX1"]
TABLE3_SUPPLY = ["COL1A1","SHH","SOX9","CDKN1A","COMP","SIRT1","PPARGC1A","ARNTL","ACAN","MMP3","MMP1"]
for gene in TABLE3_DEMAND + TABLE3_SUPPLY:
    src = afcc.get(gene) or thermo.get(gene)
    have = "AFCC" if gene in afcc else ("thermo" if gene in thermo else "MISSING")
    print(f"  {gene:10s} {have}")

def vals(genes, source):
    out = []
    for g in genes:
        if g in source:
            col = "anisotropy_index" if source is afcc else "anisotropy"
            out.append(float(source[g][col]))
    return out

dem2 = vals(TABLE3_DEMAND, afcc)
sup2 = vals(TABLE3_SUPPLY, afcc)
print(f"Demand n={len(dem2)} mean={np.mean(dem2):.3f}  Supply n={len(sup2)} mean={np.mean(sup2):.3f}")
p, d = mwu(dem2, sup2); print(f"MWU p={p:.4f}  d={d:.3f}")

print("=" * 72)
print("PANEL 3: AFCC extended, source_category-based (afcc pipeline categorisation)")
# Demand tags per manuscript: mechanotransduction/cilia/cytoskeleton; Supply: Thermodynamic_Cost
def cat(r): return [c.strip() for c in r["source_category"].split(",")]
dem3 = [float(r["anisotropy_index"]) for r in afcc.values()
        if any(t in ("Mechanotransduction","Cilia","Cytoskeleton") for t in cat(r))]
sup3 = [float(r["anisotropy_index"]) for r in afcc.values()
        if "Thermodynamic_Cost" in cat(r) and not any(t in ("Mechanotransduction","Cilia","Cytoskeleton") for t in cat(r))]
print(f"Demand n={len(dem3)} mean={np.mean(dem3):.3f}  Supply n={len(sup3)} mean={np.mean(sup3):.3f}")
p, d = mwu(dem3, sup3); print(f"MWU p={p:.4f}  d={d:.3f}")

print("=" * 72)
print("PANEL 4: hinge density, AFCC 61 genes (mechanosensor-tagged vs rest)")
hemi = lambda r: float(r["hinge_candidates"]) / int(r["n_residues"]) * 100.0
mech = [hemi(r) for r in afcc.values() if any(t in ("Mechanotransduction","Cilia") for t in cat(r))]
rest = [hemi(r) for r in afcc.values() if not any(t in ("Mechanotransduction","Cilia") for t in cat(r))]
print(f"mech n={len(mech)} mean={np.mean(mech):.3f}/100res  rest n={len(rest)} mean={np.mean(rest):.3f}")
u, p = mannwhitneyu(mech, rest, alternative="less")
print(f"MWU (mech < rest) p={p:.5f}")
# LOO robustness on hinge density
ps = []
for drop in range(len(mech)):
    sub = mech[:drop] + mech[drop+1:]
    ps.append(mannwhitneyu(sub, rest, alternative="less")[1])
ps = np.array(ps)
print(f"LOO over mechanosensors: median p={np.median(ps):.5f}  max p={ps.max():.5f}  frac p<0.05 = {(ps<0.05).mean():.3f}")

print("=" * 72)
print("PANEL 5: narrow 'extended-filament/channel' demand set vs Gamma_m supply (afcc values)")
NARROW = ["VIM","PIEZO2","PIEZO1","SCRIB","PTK7","CELSR1","VANGL1","VANGL2"]
dem5 = vals(NARROW, afcc)
sup5 = [float(r["anisotropy_index"]) for r in afcc.values() if "Thermodynamic_Cost" in cat(r)]
print(f"Demand n={len(dem5)}  Supply n={len(sup5)}  mean {np.mean(dem5):.3f} vs {np.mean(sup5):.3f}")
p, d = mwu(dem5, sup5); print(f"MWU p={p:.4f}  d={d:.3f}")
ps = []
for drop in range(len(dem5)):
    sub = dem5[:drop] + dem5[drop+1:]
    ps.append(mannwhitneyu(sub, sup5, alternative="greater")[1])
ps = np.array(ps)
print(f"LOO over demand genes: median p={np.median(ps):.4f}  max p={ps.max():.4f}  frac p<0.05 = {(ps<0.05).mean():.3f}")
