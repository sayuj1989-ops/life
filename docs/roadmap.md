# Spine Submission Roadmap (Updated 2026-03-10)

**Target:** *Spine* (IF: 3.30, Q1) or *JOR Spine* (Tier 1)
**Submission Strategy:** "A computational framework predicting adolescent scoliosis onset" with clinical validation against published cohort data.
**Start Date:** 2026-02-23
**Target Submission Date:** 2026-04-06 (4 Weeks Remaining)

## Phase 1: Computational Framework (Complete)

- [x] **Core Model:** Establish "Energy Deficit" model (`experiment_energy_deficit_window.py`).
    - *Result:* Confirmed ~41% deficit at critical lengths.
- [x] **Rescue Cliff:** Validate "Rescue Cliff" at Anisotropy ~2.4 (`outputs/sim/2026-02-22/`).
    - *Result:* Found critical value.
- [x] **Spinal Jetlag:** Run "Spinal Jetlag" simulation (`experiment_spinal_jetlag.py`).
    - *Result:* Confirmed $\phi=\pi$ yields higher Cobb angles (15° vs 10°).
- [ ] **Robustness:** Ensure model stability across parameter sweeps (Sensitivity Analysis).
    - *Result:* Preliminary `experiment_optimization_failure.py` shows stability up to $\chi_\kappa=20$. Needs higher range.

## Phase 2: Clinical Validation (Weeks 3-4: Mar 10 - Mar 24)

- [ ] **Cohort Data Extraction:** Extract clinical cohort data (Cobb angle distributions, progression rates) from published literature.
    - *Focus:* Peak Height Velocity (PHV) timing vs. Cobb progression.
- [ ] **PHV Timing:** Compare model "Instability Window" with clinical PHV timing data.
- [ ] **Sexual Dimorphism:** Validate model predictions for female vs. male prevalence against epidemiological data.
- [ ] **Curve Types:** Verify if model can reproduce common curve types (e.g., Lenke classification patterns) based on initial conditions.

## Phase 3: Manuscript Preparation (Weeks 5-6: Mar 24 - Apr 06)

- [ ] **Reformatting:** Adapt `NATURE_MANUSCRIPT_BiologicalCountercurvature.docx` to *Spine* format (IMRaD structure).
    - *Current:* 70% complete (Introduction, Results, Discussion drafted).
- [ ] **Abstract:** Draft Structured Abstract (Study Design, Objective, Summary of Background Data, Methods, Results, Conclusions).
    - *Current:* Needs shortening (210 -> 150 words).
- [ ] **Clinical Relevance:** Write "Clinical Relevance" section highlighting the predictive value for early intervention.
- [ ] **Figures:** Generate "Clinical Translation" figures (Model vs. Patient Data overlays).
    - *Current:* Figure legends written, images missing.
- [ ] **References:** Update bibliography to include relevant *Spine* and *Eur Spine J* citations.
    - *Current:* 15 core refs, need 80+.

## Progress Tracking

**Current Phase:** Phase 2 (Clinical Validation)
**Percent Complete:** 35% (Computational mostly done, Clinical 0%, Manuscript 70% drafted but needs major polish)
**Status:** On Track (but tight timeline)
