# Phase 1 & Phase 2 — Independent Reanalysis Blueprint (Revised)

## Scope and stance
This document is a **fresh, de novo analysis plan** built from direct inspection of repository code and datasets. It explicitly distinguishes:
1) what is already implemented in the codebase, versus
2) what is newly proposed for a manuscript-level contribution.

---

## Phase 1 — Deep Ingestion & Schema Mapping

### 1. Repository structure: analytical spine of the project

### A) Mechanistic model layer (`src/spinalmodes/`)
- `iec.py`: defines IEC parameters and the coupling operators linking information-field gradients to target curvature, constitutive stiffness modulation, and active moment terms.
- `model/core.py`: minimal dataclasses and helper functions for state and parameterized curvature targets.
- `countercurvature/`: metrics, coupling utilities, and validation helpers.
- `experiments/`: compact model experiments (S-shape emergence and integrated rod simulations).

**Inference:** the canonical scientific engine is a 1D rod/Cosserat-inspired reduced model where spatially varying information fields are the control input and morphology is the output.

### B) Experiment orchestration layer (`scripts/experiments/` and `scripts/analysis/`)
- Large sweep ecosystem for growth anisotropy, torsion coupling, tilt, hydraulic buckling, and energy-deficit windows.
- Dedicated scripts for narrative claims (e.g., Lenke-class toy modalization, sexual dimorphism, phase diagrams).

**Inference:** this layer explores parameter-space phenomenology and converts equations into publication figures.

### C) Evidence and translational layer (`data/`)
- `candidates_master.csv`: curated gene/protein candidate registry with explanatory text fields.
- `species_parameters.csv`: compact comparative biomechanics table (`Mass`, `Length`, `EI`, `Bg`, posture).
- `clinical_cohort_targets.csv`: sparse aggregate clinical anchors (age/Cobb/sex/sample sizes).
- `Supplementary_Statistics_Table.csv`: manuscript-ready statistical summaries.

**Inference:** the project links mechanistic simulation to biologically curated plausibility and limited clinical calibration points.

### D) Publication layer (`manuscript/`, `submission_package/`)
- Multiple manuscript variants and figure assets indicate an actively iterated submission workflow.

---

### 2. Data schema map and variable dictionary

### Dataset 1: `data/candidates_master.csv` (511 rows × 8 cols)
- `gene_symbol` *(string)*: HGNC-like symbol.
- `uniprot_id` *(string)*: protein accession.
- `organism` *(string)*: currently homogeneous (Homo sapiens).
- `pathway_tags` *(string, comma-separated labels)*: functional pathway taxonomy.
- `gravity_link` *(free text)*: rationale for gravity/mechanobiology relevance.
- `spine_curvature_link` *(free text)*: scoliosis/spinal evidence rationale.
- `priority_score` *(int; ~70–100 observed)*: curation ranking.
- `justification` *(free text)*: integrated summary rationale.

**Key schema implications:**
- A **semi-structured evidence graph** is encoded in text rather than normalized relational tables.
- `priority_score` is likely expert-derived and potentially endogenous to text evidence.

### Dataset 2: `data/species_parameters.csv` (12 × 7)
- `Species` *(string)*
- `Mass_kg` *(float)*
- `Length_m` *(float)*
- `EI_Nm2` *(float)*
- `Posture` *(categorical)*
- `Bg` *(float; dimensionless load-like quantity)*
- `Notes` *(text)*

**Key schema implications:**
- Extremely small N with probable leverage sensitivity.
- Biomechanical collinearity likely (`Mass`, `Length`, `EI`).

### Dataset 3: `data/clinical_cohort_targets.csv` (5 × 6)
- `source` *(string)*
- `age` *(int)*
- `cobb_angle` *(int)*
- `sex` *(categorical)*
- `n_patients` *(int)*
- `notes` *(text)*

**Key schema implications:**
- Aggregate, literature-extracted anchors; not individual-level progression trajectories.

### Dataset 4: `Supplementary_Statistics_Table.csv` (24 × 11)
- Statistical results table with mixed-type numeric fields (`P_value`, `Value`, and `N` partly non-numeric text encodings).

**Key schema implications:**
- Requires parsing harmonization before any direct meta-analytic reuse.

---

### 3. Confounders and inferential risk map

1. **Curation circularity**
   - The same biological priors may influence both textual rationale and `priority_score`, inflating apparent signal.

2. **Single-species candidate catalog**
   - Candidate inference is human-only despite species mechanics claims, constraining external validity.

3. **Small-sample comparative mechanics**
   - Species-level claims vulnerable to leverage points and posture-class imbalance.

4. **Clinical aggregation bias**
   - Cohort-level summaries hide within-group heterogeneity and progression variance.

5. **Phenomenology–evidence asymmetry**
   - Rich simulation manifold but sparse clinical constraints increases risk of plausible-yet-underdetermined narratives.

6. **Model identifiability**
   - Multiple parameter combinations may yield similar curve phenotypes (equifinality), requiring explicit identifiability analysis.

---

### 4. Original intent of the codebase (reconstructed)

The repository appears to target a unifying claim:

> Spatially patterned biological information fields (developmental/proprioceptive control) can counteract gravitational loading to generate and stabilize vertebral geometry; dysregulation in this coupling can shift systems into scoliosis-like regimes.

In operational terms, the codebase tries to:
- formalize coupling mathematics (IEC operators),
- map phase behavior via broad sweeps,
- and bridge to translational plausibility via curated molecular candidates plus limited clinical anchors.

---

## Phase 2 — Fresh Analytical Strategy & Hypothesis Generation

## What has already been explored (to avoid repetition)
The repository already contains explicit energy-deficit-window simulations and many mechanical phase sweeps. Therefore, a new manuscript should **not** simply restate: “demand exceeds supply with growth.”

## New hypothesis candidates (not explicit in current scripts/manuscripts)

### Hypothesis 1 (novel, actionable): **Control-Delay Bifurcation Hypothesis**
AIS-like escalation is driven less by absolute anisotropy and more by a **lag between mechanical perturbation and adaptive information-field correction**. Above a critical response delay, the system transitions from damped correction to oscillatory error amplification (runaway curvature progression).

- **Why novel here:** current scripts sweep amplitudes/stiffness/load extensively, but a dedicated *delay-control* bifurcation framing is not the central manuscript axis.
- **Actionability:** predicts benefit of interventions that shorten sensorimotor/adaptive latency (neuromuscular training schedules, feedback-timed bracing, stimulation timing).

### Hypothesis 2 (novel, actionable): **Sex-Specific Gain-Scheduling Hypothesis**
Observed sex disparity in AIS progression is better explained by **different growth-phase gain scheduling** (coupling gain vs growth-rate trajectory mismatch), not by a single static structural difference.

- **Why novel here:** sex effects appear as outputs in scripts, but a formal gain-scheduling systems hypothesis is not a primary inferential target.
- **Actionability:** enables sex- and maturation-stage-specific risk windows and treatment intensity profiles.

### Hypothesis 3 (backup): **Hidden Under-ranked Mechanotransduction Modules**
Within `candidates_master.csv`, text/pathway structure likely contains modules with high mechanistic coherence but relatively lower curated `priority_score`; these represent tractable discovery targets.

- **Why novel here:** turns curation table into a quantitative discovery problem.
- **Actionability:** directly yields shortlist for wet-lab validation.

---

## Selected primary hypothesis for the new manuscript

## **Selected: Hypothesis 1 — Control-Delay Bifurcation**

### Why this is strongest scientifically
1. **Distinct from existing narrative:** moves beyond static demand–supply imbalance to dynamic systems instability.
2. **Mechanistically deep:** naturally integrates IEC field adaptation, proprioceptive control, and growth dynamics.
3. **Clinically meaningful:** predicts *timing-sensitive tipping points* and progression acceleration.
4. **Empirically falsifiable:** longitudinal datasets can test whether inferred adaptive lag precedes Cobb acceleration.
5. **Computationally tractable:** can be simulated by introducing delayed feedback in existing rod/IEC pipeline without redefining core physics.

---

## Proposed analytical angle for Phase 3 (preview)

Use a delayed-feedback state equation over curvature error:
- Define curvature error: `e(t) = kappa_target(t) - kappa_observed(t)`
- Adaptive correction term depends on delayed state `e(t-τ)`.
- Sweep delay `τ`, coupling gain, and growth rate to find Hopf-like transition boundaries.

Primary outputs:
- critical delay `τ*` for instability,
- progression velocity index (`dCobb/dt` proxy),
- resilience margin under intervention (effective delay reduction).

---

## Pause point
Awaiting your confirmation to proceed with:
- **Phase 3:** stepwise simulated testing and extracted findings for the Control-Delay Bifurcation hypothesis.
- **Phase 4:** full publication-ready manuscript draft built on that analysis.
