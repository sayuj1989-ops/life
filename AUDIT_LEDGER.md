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

### R-6 — Short-form theory and conclusion contradicted the abstract (found 2026-09-12)
After the 08-07 audit fixed the abstract and results, `theory_summary.tex:12` still asserted
the universal `B_g ≈ 0.1` threshold and "Humans occupy a unique position", `conclusion.tex:3`
still said AIS is "a predictable consequence of crossing this boundary", the abstract's own
Conclusions called `B_g` a "robust proxy" one paragraph after calling the same `r` a
consistency check, T8–T10 was labelled "the thoracolumbar junction" (×3), one paragraph
carried both "∼80 %" and "31.1 %" for the same reduction, the species count read 10 in two
sections and 12 in two others (12 rows = 11 species + human ×2; 10 rows analysed), and the
synthetic-cohort calibration was called validation "against gold-standard datasets" (×2).
Full table with PDF line numbers:
`reports/manuscript_consistency_review_2026-09-09/REVIEW.md`. Fixed in `9150ba50`
(text only; no computed number moved) and verified in `pdftotext` of the recompiled PDF.
Also: `theory.tex`, `methods.tex`, `biophysical_origins.tex` now start with an `% ORPHANED`
line so gotcha 1 stops recurring.

### R-7 — Newton ratchet-rod experiment measured the wrong quantity in the wrong plane (found 2026-09-12)
Not a manuscript defect (no active section cites `results/newton_ratchet_rod/`), recorded
here because the README and the 09-08 review point at it. Three defects (the third found by the
Codex continuation the same afternoon, `reports/newton_readout_audit_2026-09-12/`):
(i) `joint_dtheta` took `atan2(px, py)` of body *positions* — the azimuth of each body about
the vertical, numerically undefined for a rod in the x–z plane — and the ratchet law
consumed it; the 15,628° "Cobb" is this. (ii) The permanent set was written to
`joint_rod_rest_kb_local[:, 0]` in 1/m; Newton's rod joint stores the DER curvature binormal
(an angle per joint) in the parent-local frame with x–z bending in component 1, so the law
prescribed rest bending in the y–z plane, 48× too large. Fixed in `f9d5b042`
(`scripts/experiments/newton/rod_measure.py`, unit tests in
`tests/test_newton_rod_measure.py`); every number from the 2026-09-03 run is void and kept as
`*.pre-measurement-fix-2026-09-12.*`. (iii) The reported "Cobb" summed joint curvature (rad/m) and called it degrees without the
segment length — 48× too large; the smoke values first recorded in the pre-registration file
(10.6–56.2°) are really 0.22–1.17° of total absolute planar bend, and the control drift was
mis-defined as well. Fixed in `rod_measure.total_absolute_bend_deg` / `control_drift_deg`; the
running process's output is corrected on read by `ratchet_rod_readout.py`. The pre-registered
sanity bound (1–40°) was set on the inflated scale and is now known to be mis-scaled — an open
author decision (card t_40524ff0), not silently retuned. (iv) **Material-slot overwrite (Codex, same evening; withdraws the reading).** Newton rod
joints carry four `joint_target_ke` slots (stretch, shear, bend, twist); `batched_model()` wrote
the bending stiffness into all four per world and copied it into `joint_target_kd`, so every
batched run simulated axial/shear stiffness ≈ 1.77 N/m instead of 10⁷. Reproduced in memory
(`[1e7, 1e7, 1.77, 1.77]` → `[1.77, 1.77, 1.77, 1.77]`). The re-run was read on 2026-09-12 under a
pre-registered amendment (`results/newton_ratchet_rod/PREREG_2026-09-12.md`; corrected view
`reports/newton_readout_audit_2026-09-12/full/READOUT.md`) as Gate C holding at `B_g` 0.3 and
0.5 with `B_g` 0.2 excluded — **that reading is withdrawn as a physical result**: reproducible
numbers, unintended mechanics, no mechanical conclusion of any sign. A corrected-material
campaign runs under a new frozen protocol (board).

### R-8 — Both citations on the Hueter–Volkmann sentence were phantom records (found 2026-09-12)
`introduction.tex` and `theory_summary.tex` supported "a sustained asymmetric deviation is
progressively cemented by asymmetric growth-plate activity" with `stokes2006hueter` ("Hueter-Volkmann
effect in the growth plate…", Eur Spine J 2006;15(7):1044) and `villemure2009growth` ("Growth
biomechanics in the cause and progression of idiopathic scoliosis", Spine 2009). Neither exists:
both DOIs return 404 at Crossref, both titles return 0 PubMed hits, and Stokes's only 2006 Eur Spine J
paper is on trunk-muscle activation in low back pain (PMID 15906102). Found while the comparator
work (t_9f29fa3b) verified its own references. **The nightly `verify_bib` scored both as clean
because its fabrication heuristic checks that a DOI is *present*, not that it resolves** — a DOI
string is the cheapest thing to fabricate. Replaced with verified records (PubMed esummary +
Crossref, 2026-09-12): Stokes 2007 Eur Spine J 16(10):1621 (PMID 17653775), Villemure & Stokes 2009
J Biomech 42(12):1793 (PMID 19540500), and Stokes et al. 1996 Spine 21(10):1162 (PMID 8727190) added
to the same sentence; the uncited composite `stokes2002mechanical` (1996 title, 2002 volume) became
the real 1996 record and the uncited `stokes2006biomechanics` (journal "Spinal Deformity", which did
not exist in 2006) was deleted. Verified in the recompiled PDF reference list.

**Full pass, same day** (`scoliosis_publication_strategy/scripts/verify_doi.py`, new: Crossref then
DataCite per DOI, PubMed then Crossref-title for DOI-less journal items; run by hand, not on the
03:00 hotspot cron). Over the 57 keys the compiled manuscript cites: two more phantoms —
`wuest2025vim` ("Vimentin intermediate filaments act as a gravitational strain gauge…", journal
"Nature Microgravity", which does not exist; replaced by Hu et al. PNAS 2019;116:17175,
`hu2019vimentin`) and `aubin2004brace` (paraphrased title, its own `note` called it a
"representative example"; replaced by Périé et al. Spine 2003;28:1672 and Clin et al. Spine
2010;35:1706); two wrong records — `lang1985nerve` (paraphrased title, "other authors"; the real
paper is Lang et al. Muscle Nerve 1985;8:38) and `wolpert1998internal` (right paper, wrong journal
"Neural Computation" and dead DOI; it is Trends Cogn Sci 1998;2:338); and 15 real entries that
carried no DOI (added). Result: 57/57 resolve. Printed-provenance `note` fields I had added were
removed again — `note` prints in the reference list.

### R-9 — Retracted claims survived outside the sections the fixes edited (found 2026-09-23)
A claim audit of the compiled PDF (manual read of all 458 claim-bearing sentences + TypeSafe Jev
screen, pre-registered: `~/jupyterlab/scoliosis_publication_strategy/jev_claim_audit/`) found 11
residues of R-1/R-4/R-6/O-1 plus 9 overstatements in the introduction, captions, conclusion,
supplementary and Table 5 — copies the earlier fixes to abstract/results missed. Examples: the
introduction still claimed a unique human "Allometric Trap" at B_g > 0.1; the conclusion credited
the rejected DDE framework; the clinical figure was titled "Clinical Validation" with p = 1.66e-59
on a deterministic correlation; Table 5 said the anisotropy gap "does not survive FDR" against
S2's q = 0.049; results asserted a "supercritical bifurcation" and R > 1 against the
prefactor-free theory and the graded-progression statement; Fig 2 gave Human-Child B_g = 0.06
(Table 3: 0.0201 — author ruled 0.0201). Patch list with before/after:
`scoliosis_publication_strategy/patches/claim_audit_2026-09-23.md`. The clinical figure title
lives in `correlation_09_clinical_validation.py` (cron-regenerated nightly into
`manuscript/figures/`), so it was fixed in the script. Verified absent/present in `pdftotext`
of the recompiled PDF. Still open: the Fig 1 caption describes panels (passive beam, B_g across
species, Energy Deficit Window) that `fig_gene_to_geometry.pdf` does not contain — caption and
image do not match; needs an author decision.

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

## OPEN — OX-series (2026-10-14): optogenetics-lane rod solver
Lane: `~/jupyterlab/scoliosis_publication_strategy/optogenetic_gravity_feedback_20261008/continuation_20261012/hermes_research` (board `spine-research`, card t_4af299e8). Adjudication of the 2026-10-14 external Codex audit revision; every number below re-derived against the live code on this box.

1. **Frame defect is real** (`code/rod3d.py:101`): `qrel = q_i* ⊗ q_{i+1}` already yields
   `v = qlog_vec(qrel)` in material frame *i* (line-100 comment "world" is the wrong premise);
   `R_i^T` is applied a second time, and with anisotropic `D=diag(EI,EI,GJ)` a global world
   rotation mixes bend into twist. Repro (N=4, L=1, κ0=0, q_i=qexp([0.1i,0.05i,0.02i]),
   left-mult Q0=qexp([0.4,0.2,0.3])): Eb 0.07644000 → 0.0755205547, max |Δkmat| 0.09024995,
   while `v` itself is invariant to 1e-16. Replacing `kmat = R_i^T v/l0` with `kmat = v/l0`
   restores invariance to ~2e-17.
2. **The one-line fix is not sufficient**: FD-vs-analytic torque error is 4.31e-2 for BOTH
   the current and the corrected energy (matches V1 `max_abs_err_rotation` 0.0428) — a second,
   independent bug in the torque assembly (log-Jacobian / eta-convention); the exact
   `J_r^{-1}(v)` right-Jacobian treatment is required. V1 axial error 10.09 also makes the
   `l`-flow inconsistent (observed integrate blow-up at step 189 under numpy 2.x/py3.14;
   recorded env is py3.12/numpy 2.2.6 — env-dependence flag).
3. **Two gates can never pass as coded**: `V2_zero_state` `apex_max_dev` = max|r_tip| = L
   (=1.0 for a straight vertical rod — it measures the axial coordinate); `V10_no_growth`
   `k0_change` = the drive amplitude (1.2) switched off at withdrawal by protocol design
   ("Withdrawal: drives and control off"). Metrics must be fixed before "all gates pass" means anything.
4. **Axis-convention swap already inside the suite**: `kref_vec=[κ_ref/L,0,0]` is commented
   "pure sagittal x-bend", but Darboux `d3' = κ2 d1 − κ1 d2` gives x̂-bend → d3 deflects along
   −ŷ (coronal in the d1=x̂,d2=ŷ convention). `V3_arc` circumcenter solve hardcodes the z=0
   plane while the drive `kgrow ∥ x̂` puts the arc in y–z → `max_radius_err = NaN`. Fiber
   matching `ε_g = ε̄ + a cosφ + b sinφ` requires (κ1,κ2) = (+b/R, −a/R), not (a/R, b/R).
5. **Results/code provenance gap**: `VERIFICATION_RESULTS.json` (15:13, records
   rod3d_sha256 19498f05…) predates current `rod3d.py` (mtime 15:33, sha256 b6e77592…). The
   results file does not describe the code on disk; regenerate both.
6. **Oct-12 checker n3** (`scripts/analysis/verify_derivations_20261012.py`) right conclusion,
   wrong printed boundary: for `z²+b+a e^{−z}`, crossing lines are `b ∓… = n²π²` families;
   on its own ray (a,b)=(τ²,2τ²) with I=1,B=2,K=1, `N_RHP=2` at τ=1.814 (its printed
   `π/√((B+K)/I)`) and first turns 0 at τ=π=π/√((B−K)/I); small-τ is unstable for all τ>0
   (Re λ≈Kτ/2I). Full verified stability set: wedges `b−a>(2m+1)²π², b+a<(2m+2)²π²`;
   argument-principle counts: a=0.5: (b=12,50,100)→(0,2,0) ✓; 8 further directional points
   all match crossing-direction theory; `N_RHP` reaches 4 deep in a (ray τ=9.4).
7. **Citations checked**: Simsek 2023 Nature 613:153 (PMC9846577) = pulsatile FGFR(SU5402)/MEK
   *pharmacology* in clock-deficient zebrafish, not optogenetics, not somitoids; Bos 2025
   Commun Biol 8:1233 (PMC12356878) = mouse slices, cervical/lumbar tonic vs thoracic
   single-spiking. No compiled manuscript section contains optogenetics, `S_co`, or a π/2
   DDE claim — those live in the proposal/HISTORICAL notes only; the 25-arm table vs
   "31 primary runs" line in the lane's MODEL_PROTOCOL.md (and 25+5dt+2N=32 arithmetic) need AMEND-02.
   `verify.py` runs on import (no main guard).

### OX-series RESOLUTION (2026-10-14)

All seven findings closed on the pinned env (py 3.12.3 / numpy 2.2.6,
`~/jupyterlab/.venv`): (1) frame defect fixed — `kmat = v/ℓ0`, SO(3) energy invariance
~2e-17; (2) torque assembly exact (analytic vs FD ≤1e-10); (3) axial penalty flow
exponential-integrated (was |1−μₐdt·kA·l0/lg²| = 7 blow-up/step; the py3.14 "step-189"
crash was environment-independent); (4) base clamp enforced per frozen protocol (free base
= inverted-pendulum fall); (5) axis convention locked (κ₂ sagittal; kgrow = A(sin φ, −cos φ))
— B-arms now exactly planar (oop 0.0), V6 mirror err 0.0e+00, V4 screw radius 5e-10,
V2b axial strain 5e-17, V5 cantilever 0.0022 vs 0.0025; (6) results/code hash now matches,
VERIFICATION_RESULTS.json ALL: true (13 gates), regenerated with env+sha256; (7) AMEND-01/
02/03 written to the lane's AMENDMENTS.md; run table reconciled 32 rows = 30 executed
(C4≡C1, H2≡B2 dedup); C3 = literal Ω-flip (phase 0); n3 boundary corrected in the checker;
manuscript files untouched (zero S_co/π2/optogenetics hits confirmed). Frozen 30-run
campaign + AMEND-03 perturbation-modes results in the lane's results/.

---

## LOST

Roughly 60 findings from the 2026-08-06/07 audit, including all of the M-series beyond
M30/M31, are unrecoverable. M30 (a citation in a non-existent journal) and M31 (a
placeholder bib entry) both scan clean against `references.bib` as of 2026-08-17 (231
entries, all articles carry journal and year) and appear to have been resolved by
`dafcc3af` "Evidence + citation integrity v1.6".

A re-audit is worthwhile **after** the open items above are closed, so it does not
rediscover known work.
