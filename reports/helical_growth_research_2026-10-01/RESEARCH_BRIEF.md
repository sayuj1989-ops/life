# Helical spinal growth under gravity: evidence and next experiment

Prepared 2026-10-01 from current files in `/home/sayuj/life`, current process/GPU
inspection, and targeted primary-literature retrieval. This is a focused research
review, not a systematic review, an established cause of scoliosis, or a treatment
recommendation. The user's broad request is interpreted as testing the mechanism
of three-dimensional scoliosis and identifying a computational correction hypothesis.

## The useful target

Test whether **regional asymmetric loading during remaining growth, combined with
an independently measurable recovery process, predicts structural progression**
better than conventional stress-dependent growth modulation. If it does, that model
can become a candidate tool for comparing correction strategies. Gravity is one
external load; muscles, ribs, pelvic constraints, discs and supports determine its
tissue-level consequences.

A spine's centerline torsion, vertebral axial rotation, disc wedging and vertebral
wedging are different observables. A visually helical centerline does not establish
helical growth or tissue twist. Initiation and progression require separate tests.

## What the existing project establishes

- `src/spinalmodes/iec.py:compute_helical_threshold` returns
  `max(0.01, 0.1 + delta_b - 4 * chi_f * grad_I_norm)`. Its own comment says the
  coefficient is tuned to acceptance criteria. It has no measured material,
  geometry, loading or growth inputs and solves no mechanical eigenproblem.
  Use it as an illustrative heuristic; it cannot establish a physical threshold.
- The old Newton rod's material assignment overwrote axial/shear stiffness. Its
  intended-mechanics conclusions remain withdrawn in `AUDIT_LEDGER.md`, R-7(iv).
- The corrected campaign's ledger last updated at **2026-09-13 10:20:19 UTC**.
  It records **14.918 active hours**, eight completed jobs, four failed evaluated
  convergence comparisons and six unevaluated comparisons. Its assessment is
  **NUMERICALLY_UNRESOLVED**. No matching controller/worker was found in the current
  process inspection. A saved `waiting_for_window` label is not evidence of ongoing work.
- The corrected worker explicitly reports **total absolute planar bend, not clinical
  Cobb**, and rejects loss of planarity. Completing that protocol could establish
  validity for its planar experiment; it cannot demonstrate a helical instability.
- The existing CPU comparator report contains 252 synthetic model/protocol cases.
  The reported recovery differences are consequences of the equations and do not
  identify a biologically correct model. This review did not rerun that grid.
- Untracked local research edits and the manuscript are preserved. No historical
  result, frozen protocol or source seal is rewritten by this review.

The fresh `gravity_torque_checks.json` records comparison verdicts and hashes. Its
source-seal check covers ordinary files only, not installed dependency directories.

## A fresh mechanical check

`check_gravity_torque.py` computes the gravitational moment from distal segment
weights and projects it onto each local tangent:

\[
\tau_g(s)=\mathbf t(s)\cdot\int_s^L
[\mathbf r(u)-\mathbf r(s)]\times[\mathbf g\,dm(u)].
\]

Segment masses are placed at midpoints, positions are metres, masses kilograms,
and torque N m. Reverse cumulative moments make the calculation linear in the
number of segments. It is a load-geometry identity, **not a simulation of growth,
equilibrium, instability, or vertebral rotation**.

Controls test a straight column, a sagittal curve, a vertical-plane curve rotated
about gravity, a mirrored nonplanar curve, zero gravity, doubled gravity and rigid
translation. A synthetic circular helix is checked against an independent
closed-form integral through six mesh resolutions. The unchanged criteria are
control residual <1e-10 N m and final analytic error <1e-4 N m. The first attempt's
insufficient quadrature resolution is retained in `ATTEMPT_01.md`.

Interpretation: a centerline lying in a plane containing gravity has zero axial
gravity moment about its local tangent in this external-load calculation.
Nonplanar geometry can produce such a moment, and reflecting the geometry reverses
its sign. Gravity alone supplies no preferred right/left direction in a symmetric
model. This does **not** exclude compression-driven buckling, spontaneous symmetry
breaking, muscle-generated torque, asymmetric anatomy or growth: those mechanisms
are outside this check. It identifies a control a future 3D model must pass.

## Primary evidence and its limits

1. **Drevelle et al., 2010:** patient-specific models of 12 mildly scoliotic and
   six asymptomatic subjects compared gravity, anterior growth and disc softening.
   Their combination amplified preexisting deformity; the tested healthy geometries
   did not develop scoliosis. This supports a progression hypothesis under those
   model assumptions, not an established initiating cause.
   [Primary study](https://pubmed.ncbi.nlm.nih.gov/20393388/).
2. **Adam et al., 2008:** static calculations and images in a small scoliotic group
   related gravity-induced torque to intravertebral rotation, with computed moments
   up to 7.5 N m. The authors proposed that initial lateral deviation preceded the
   rotation. Association and mechanical plausibility do not independently establish
   longitudinal causation.
   [Primary study](https://pubmed.ncbi.nlm.nih.gov/18197088/).
3. **Kouwenhoven et al., 2007:** 14 human and 14 porcine functional spinal units
   showed greater rotation under eccentric dorsal than ventral shear in relevant
   thoracic levels. This establishes a loading-direction effect in vitro. It does
   not prove that the same mechanism initiates AIS in vivo.
   [Primary experiment](https://pubmed.ncbi.nlm.nih.gov/17978652/).
4. **Chen et al., 2026:** an accessible article-in-press reports a single severe
   human traction case and cell/mouse experiments linking unloading to PIEZO1 and
   growth-plate changes. This offers a measurable mechanosensing candidate. It does
   not establish a routine unloading treatment, a safe drug intervention or a cure;
   the human observation is uncontrolled and the authors describe traction as a
   pre-surgical adjunct. Reducing gravity in a rod model is not equivalent to their
   traction or random-positioning experiments.
   [Primary paper, article-in-press PDF](https://www.nature.com/articles/s41526-026-00604-1_reference.pdf).
5. **BrAIST, 2013:** the randomized intention-to-treat cohort had 75% success with
   bracing versus 42% with observation; success meant reaching skeletal maturity
   without a curve of at least 50 degrees. This provides a clinical benchmark for
   progression prevention in the studied high-risk adolescents. It does not identify
   the causal initiation mechanism or validate this project's model.
   [Primary trial](https://pubmed.ncbi.nlm.nih.gov/24047455/).

No claim of novelty follows from this focused search. The new review separates
model implications from empirical results and avoids importing the paper's
stronger therapeutic language into the project's conclusions.

## Proposed experiment and decision criteria

**Stage 1 — establish mechanics before interpreting biology.** Preserve the old
campaign. Resolve its numerical discrepancies under a separately documented
diagnostic protocol if required. Independently verify axial/shear/bend/twist arrays,
units, clamp reactions and simple analytic loading cases. A future spatial model
must include measured sagittal geometry and explicit coronal/torsional degrees of
freedom. Report frame twist, centerline shape and image-derived Cobb separately.
It needs mesh, timestep and solver convergence and checks for contact/self-crossing.
Numerical validity is a prerequisite, not biological validation.

**Stage 2 — challenge initiation and handedness.** Run zero bias, paired mirrored
perturbations, reversed bias, no growth, no gravity and matched stiffness controls.
Use the same random draws for paired stochastic cases. No imposed positive seed,
rectification or prescribed curve direction may be counted as emergent handedness.
An unexplained direction preference in a symmetric implementation fails the
implementation check. Persistent absence of predicted deformation in an appropriate
measured cohort is a biological challenge, not a reason to retune its inputs.

**Stage 3 — distinguish reversible disc response from structural remodeling.**
Compare a conventional stress-growth model, a viscoelastic model, and the same
model with a fitted recovery component. Obtain approved longitudinal measurements
of growth/maturity, standardized loading/unloading response, three-dimensional
vertebral orientation and disc versus bone wedging. Supine Cobb alone is not a
measurement of permanent bone deformity. The current slow model's yearly recovery
rates cannot be identified from a minutes-long unloading test. Fast and slow
recovery require separate state variables and observation intervals.

Before fitting, freeze the anatomical coordinate frame, primary prospective
endpoint, patient-level train/test split, conventional comparator, measurement
repeatability, missing-data rules and clinical relevance criterion. Fit no
patient-specific progression or handedness seed from that patient's future data.
Evaluate incremental held-out prediction with uncertainty after adjusting for
baseline curve, maturity, growth and brace adherence. If the recovery term adds no
prespecified benefit, retain the simpler comparator and reject that addition.

**Stage 4 — test a correction hypothesis only after Stage 3.** Compare interventions
that reduce regional asymmetric stress during remaining growth, while maintaining
sagittal alignment and respecting measured support, mobility and loading constraints.
The objective is to reduce predicted *future* structural change with uncertainty,
not just instantaneously straighten an image. Compare with standard bracing and
simple unloading under identical model assumptions. A simulated advantage is a
candidate for independent prospective validation, not a treatment recommendation.

PIEZO1 could become a tissue-level intermediate in a separate experimental study;
protein shape or expression alone does not provide a patient-specific stiffness or
growth-rate law. Do not add molecular parameters until the mechanical and recovery
comparison is identifiable.

## Compute status and reproducibility

On `spark-89c4` / aarch64, the current `nvidia-smi` query reports **No devices were
found**, including outside the execution sandbox, despite NVIDIA device nodes being
present. A Flash-Next process exists, but that does not prove a working CUDA context.
The geometry check uses the existing life NumPy environment on CPU and loads no model.
No GPU validation, driver repair, model stop or long-running campaign is performed.

Run from `/home/sayuj/life`:

```sh
.venv/bin/python reports/helical_growth_research_2026-10-01/check_gravity_torque.py
```

Read `gravity_torque_checks.json` for numerical results and provenance. The next
meaningful advance is an identified, converged 3D model confronted with independent
longitudinal data. More GPU computation alone cannot substitute for either.
