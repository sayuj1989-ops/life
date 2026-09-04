# Audit Ledger — AIS manuscript

Durable record of manuscript-integrity findings. **Created 2026-08-17 because the
original 98 KB `AUDIT_REPORT.md` from the 2026-08-06/07 twelve-agent audit was written
to a session scratchpad and has been lost.** Roughly 60 of its ~70 findings are
unrecoverable; what follows is everything that survived, plus findings verified since.

Rules for this file:
- A finding is only marked RESOLVED when the fix is committed **and** verified in the
  compiled PDF text, not merely in the `.tex` source and not by `latexmk` exit code.
- Numbers here are re-derived from source data, not copied from prior summaries.
  Two figures in the previous summary were wrong (see H-1).

---

## Standing gotchas that let these survive

1. **`main.tex` does not input `sections/theory.tex` or `sections/methods.tex`.** It
   inputs `theory_summary.tex` and `methods_summary.tex` (Springer word limit). Edits to
   the full files never reach the PDF. Check `grep '\\input' manuscript/main.tex` before
   assuming an edit landed.
2. **A clean `latexmk` proves nothing about content.** The supplementary carried the same
   equation under two different labels, presented as two different equations, and the
   build exited 0 with zero undefined refs for months. Verify with `pdftotext main.pdf -`
   and assert on strings present/absent.
3. **Printed tables are hand-entered and drift from their source CSVs.** This has now
   caused three separate defects (B_g column, Table 3 anisotropy column, Table 3
   membership). Treat any hand-typed number in a table as unverified until diffed
   against the generating file.

---

## RESOLVED

### R-1 — Table 1 `B_g` column was decimal-shifted (~100x on 7 rows)
Printed values inflated vs `outputs/thermodynamic_cost/cross_species_scaling.csv`.
On correct values **the human adult ranks 7th of 12** and is indistinguishable from the
rabbit; the caption claimed humans occupied "the deepest position in the Allometric Trap".
The cross-species uniqueness claim was an arithmetic artifact.
Fixed in `62d68cab`; reported as an explicit negative result in abstract, results,
tables, discussion and supplementary. No published downstream number moved — all
consumers recompute `B_g`.

### R-2 — `r = 0.983` was not a correlation
`L = np.linspace(0.25, 0.55, 30)` is a swept grid, not a sample; `mean_sq_diff` spread
is 1.4e-17, so Cobb is a deterministic function of L. It is `Pearson(x, f(x))`:
**setting `chi_kappa = 0`, deleting the entire IEC coupling, still gives r = 0.9816**,
and p is a function of grid density (`linspace(...,8)` -> 1.5e-05; `,200` -> 2.9e-150).
It appeared in 6 places including the abstract. Removed in `62d68cab`; the monotone
relationship is now stated without a coefficient.

### R-3 — Anisotropy sign was inverted
`experiment_anisotropy_rescue.py:103` sets `P_eff = P_counter * (A/mean_A)`, making
structural anisotropy a multiplier on **demand**, so `L_crit` *falls* (r = -0.88).
The manuscript called this "protective scaling". Root cause: two opposite-sense
quantities both called "anisotropy" — a stiffness ratio (high = stable) and a demand
multiplier (high = costly). Separate symbols introduced in `62d68cab`; explicit symbol
caution added to the supplementary in `2c394c24`. Also 20/50 sweep points sit on the
search bounds (16 floor, 4 ceiling), so the "saturation at >= 6" was the floor.

### R-4 (B7-B9) — Supplementary asserted the retracted delay-Hopf mechanism
`supplementary.tex` **is** inputted by `main.tex` and compiles. It carried
"Hopf Bifurcation and the Onset of Scoliosis" stating the theory "precisely explains why
AIS uniquely coincides with the growth spurt", while `figures.tex` already told the
reader the ratchet had replaced it. Retained but retitled as a falsified alternative in
`2c394c24`. See H-1 for the corrected numbers.

### R-5 — Supplementary/main-text contradictions (4, all in compiled text)
Fixed in `2c394c24`:
- Demand scaling given as `L^4` in two places; main text derives `L^3` in five.
- `B_g` defined twice, incompatibly, 28 lines apart: `EI/MgL^2` (threshold 0.1) and
  `chi_M<|grad I|>/rho A g L^2` (threshold 1). Second definition removed.
- The same equation (`kappa_rest = kappa_gen + chi_kappa grad I`) displayed under two
  labels as both "the control law" and "the characteristic equation" — both were
  copy-paste overwrites and neither intended equation was present. Both supplied; the
  stranded IEC stiffness/energy equations moved to their own subsection.
- `discussion.tex` still asserted the "sharp demarcation at `B_g ~ 0.1`".

None of the seven supplementary equations is referenced anywhere in the document, which
is part of why the duplicate survived.

---

## OPEN — blockers

### O-1 (was B21, and worse than labelled) — the Demand/Supply anisotropy result does not reproduce
**RESOLVED 2026-09-04 (branch `fix/protein-table-provenance`).** The root cause was two
divergent AlphaFold snapshots: `research/alphafold_v6_analysis/protein_metrics.json`
("v6") and the earlier `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv`.
Every Table-3/dissipation-table discrepancy in the original finding is a CSV-vs-v6
delta (VIM 7.47 vs 5.57, PIEZO2 4.44 vs 3.45, GHR 5.13 vs 2.27, LBX1 P52954 vs
P52951). Fix adopted:
- **v6 JSON is the single source of truth** for shared proteins; CSV-only genes
  (NTRK3, DMD, MYLK, FLNA) keep CSV values, dagger-flagged.
- Both tables are now **generated files**
  (`scripts/analysis/regenerate_table_thermodynamic.py`,
  `regenerate_table_dissipation.py` → `manuscript/tables_generated/`), spliced into
  `sections/tables.tex`. No hand-typed anisotropy values remain.
- `scripts/analysis/protein_snapshot_provenance.py` prints the full snapshot
  reconciliation + the headline statistic for any future check.
- Headline restated at reproducible v6 values: 72% (ratio 1.72),
  **p = 0.021 two-sided / 0.011 one-sided, d = 1.13, n = 23**. The one-sided p is what
  the old `p = 0.011` was; the two-sided is now always shown alongside. Cohen's d
  corrected 1.19 → 1.13 (pooled-SD definition).
- S2 BH row rescored two-sided: p = 0.021 → **q = 0.049** (still < 0.05, flagged as
  marginal in the S2 caption). Results §3.4 q-values updated (0.018 / 0.033 / 0.049).
- Abstract, results, theory, figures caption all show two-sided + one-sided together.
- Verified in compiled PDF text (pdftotext), not just source.

What is NOT fixed: the CSV snapshot itself is unversioned and its provenance (which
AlphaFold release produced VIM 7.47) is unknown. If the CSV is ever regenerated the
dissipation-table daggers must be revisited.

Original finding (kept as history):

**Verified 2026-08-17. This is the most serious open finding.**

Two independent source pipelines —
`outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv` and
`outputs/afcc/2026-02-10/metrics.csv` — agree to six decimal places. **Table 3 in the
manuscript matches neither.** Only 8 of 22 rows agree; 12 differ and 2 are absent from
the AFCC metrics. The discrepancies are one-directional (every differing Table 3 value
is *lower* than the v6 source), which is the signature of an older AlphaFold release
despite the caption reading "AlphaFold Database v6".

Table 3 also differs from the source in *membership*: 5 proteins are in Table 3 but not
in the thermodynamic panel (PTK7, DSTYK, ACAN, MMP3, MMP1) and 5 are in the panel but
not the table (PIEZO2, DMD, MYLK, IGF1R, GHR). The swap is not neutral — it drops the
highest-anisotropy Supply protein (GHR, 5.13) and the two lowest-anisotropy Demand
proteins (DMD 1.32, MYLK 1.46), and adds three very low Supply proteins.

Recomputing the headline statistic on authoritative AFCC v6 values, under all three
panel definitions the manuscript itself implies:

| Panel | n | p (MWU) | Cohen's d |
|---|---|---|---|
| Thermodynamic CSV: Demand (eta_p+eta_a)=12 vs Supply (Gamma_m)=10 | 22 | **0.307** | 0.565 |
| Table 3's own membership, v6 values | 20 | **0.068** | 1.089 |
| Abstract's curated 5-protein subset vs Gamma_m | 14 | **0.106** | 1.801 |
| **Published claim** | 23 | **0.011** | 1.19 |

**None reaches p < 0.05.** The abstract's "72% more elongated" ratio also does not
reproduce (curated subset gives 2.167, i.e. 117%). `LMNA` (P02545) is absent from the
AFCC v6 metrics entirely but appears in Table 3 at 4.71 and in the thermodynamic CSV
at 4.752.

Independent corroboration: the GSC 2027 abstract (written 2026-08-05, before this check)
had already **excluded** this result as too fragile to present, noting "the v3 re-run
with explicit groups gives p=0.035/d=0.67, LOO significant in only 84.6% of iterations,
and broadening the demand panel dilutes it to p=0.33". That is the same instability seen
here from a different direction.

Affects: abstract, Table 3 caption, results, supplementary. ~~**Blocks resubmission**~~
— resolved per the fix note at the head of this finding: restated at the reproducible
effect size (72%, p = 0.021 two-sided / 0.011 one-sided, d = 1.13) rather than
withdrawn, with hinge density (q = 0.018) as the lead protein-level claim.

### O-2 (B16) — cover letter describes the pre-reframe paper
**RESOLVED 2026-09-04 (branch `fix/protein-table-provenance`).** `cover_letter.txt`
rewritten around the current title and the recovery-ratchet reframe. The old letter
pitched "Metabolic Buckling" / "Thermodynamic Standing Wave" / "perfectly predicts" and
the R^2=0.775 anisotropy-rescue claim — none of which survives the audit. The new
letter leads with the negative results, states which BrAIST numbers were calibration
targets, and marks the protein result's marginal FDR status, so the letter cannot
overshoot the manuscript.

### O-3 (B17) — availability statement false in three ways
**RESOLVED 2026-09-04 (branch `fix/protein-table-provenance`).** `sections/availability.tex`
now names the public fork `github.com/sayuj1989-ops/life` (the `sayujks0071` remote
cannot be pushed to — no token), lists only tags that actually exist
(`v1.0.0-submission`, `v1.4.7-editorial`, `v1.5-scaling-falsification` — verified via
`git tag` and `git ls-remote`), and `.zenodo.json` was created (it had been cited but
never existed). Zenodo DOI minting remains a post-acceptance human step; the statement
no longer claims a tag that does not exist.
`sections/availability.tex` names submission tag `v1.4-editorial` (repo is past v1.6),
says the Zenodo DOI "will be minted", and points at
`github.com/sayujks0071/scoliosis` — which per memory **never received the June/July
commits**, because pushing needs a `sayujks0071` token that is not configured. An editor
can check the URL in 30 seconds.

---

## OPEN — corrections to the previous audit summary

### H-1 — two numbers in the prior summary were wrong
Re-derived 2026-08-17 by solving the delayed-PD inverted-pendulum characteristic
equation directly (`lam^2 - g/L + (p + d*lam)exp(-lam*tau) = 0`, `p = 20/L`, `d = 8/L`,
model's own logistic `L(t)`):

- The prior summary attributed utilisation **0.806 -> 0.655** to `v = 55 m/s`. It is
  actually at the simulation's own **`v = 15 m/s`**. At `v = 55 m/s` it is 0.546 -> 0.324.
- The prior summary reported the dimensionless delay falling **-27.7%** at `v = 55`.
  It falls **-21.1%**.

**The correction strengthens the rejection.** The prior framing made the falsification
contingent on disputing the conduction velocity. It is not: utilisation falls
monotonically and peaks at **age 5** — before the spurt — under *both* velocities, and
never approaches unity. `tau_c` grows with `L` faster than `tau` does, because
lengthening the spine lowers its natural frequency and buys more delay tolerance than
growth consumes. Growth moves the system *away* from the Hopf boundary.

Reproduce with the script archived alongside this ledger's commit message, or re-derive
from `scripts/experiments/experiment_temporal_mismatch_dynamics.py` lines 85-110.

---

## LOST

Roughly 60 findings from the 2026-08-06/07 audit, including all of the M-series beyond
M30/M31, are unrecoverable. M30 (a citation in a non-existent journal) and M31 (a
placeholder bib entry) both scan clean against `references.bib` as of 2026-08-17 (231
entries, all articles carry journal and year) and appear to have been resolved by
`dafcc3af` "Evidence + citation integrity v1.6".

A re-audit is worthwhile **after** the open items above are closed, so it does not
rediscover known work.
