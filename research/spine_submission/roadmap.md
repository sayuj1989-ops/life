# Spine Submission Roadmap

**Target:** *Spine* (IF: 3.30, Q1, H-index: 300)
**Strategy:** "A computational framework predicting adolescent scoliosis onset" with clinical validation against published cohort data.
**Start Date:** 2026-02-23
**Target Submission Date:** 2026-04-06 (6 Weeks)

## Phase 1: Computational Framework (Weeks 1-2)

- [x] **Core Model:** Establish "Energy Deficit" model (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff:** Validate "Rescue Cliff" at Anisotropy ~2.4 (Simulated in `outputs/sim/2026-02-22/`).
- [x] **Spinal Jetlag:** Run "Spinal Jetlag" simulation to demonstrate circadian modulation of curvature (`experiment_spinal_jetlag.py`).
- [x] **Robustness:** Ensure model stability across parameter sweeps (Sensitivity Analysis). (`scripts/weekly_sim_defect_sensitivity.py`)

## Phase 2: Clinical Validation (Weeks 3-4)

- [x] **Cohort Data Extraction:** Extract Weinstein 1983 / Lonstein 1984 curve progression data to `data/clinical_cohort_targets.csv`.
- [x] **Clinical Script:** Implement `scripts/validate_clinical_data.py` to automate these comparisons.
- [ ] **PHV Timing:** Compare model "Instability Window" with clinical Peak Height Velocity (PHV) timing data.
- [ ] **Sexual Dimorphism:** Validate model predictions for female vs. male prevalence against epidemiological data.
- [ ] **Curve Types:** Verify if model can reproduce common curve types (e.g., Lenke classification patterns) based on initial conditions.

## Phase 3: Manuscript Preparation (Weeks 5-6)

- [ ] **Reformatting:** Adapt `nature_manuscript.tex` to *Spine* format (IMRaD structure).
- [ ] **Abstract:** Draft Structured Abstract (Study Design, Objective, Summary of Background Data, Methods, Results, Conclusions).
- [ ] **Clinical Relevance:** Write "Clinical Relevance" section highlighting the predictive value for early intervention.
- [ ] **Figures:** Generate "Clinical Translation" figures (Model vs. Patient Data overlays).
- [ ] **References:** Update bibliography to include relevant *Spine* and *Eur Spine J* citations.

## Progress Tracking

**Current Phase:** Phase 2: Clinical Validation (Weeks 3-4)
**Percent Complete:** 42.9%
**Projected Completion:** 2026-03-18
**Status:** In Progress
