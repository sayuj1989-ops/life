# Research Roadmap: Biological Countercurvature

**Target:** *Spine* Submission (IF: 3.30, Q1, H-index: 300)
**Strategy:** "A computational framework predicting adolescent scoliosis onset" with clinical validation against published cohort data.
**Timeline:** 6 Weeks (March 14 - April 25, 2026)
**Latest Progress Update:** [docs/progress_update_2026-03-14.md](progress_update_2026-03-14.md)

## Phase 1: Computational Framework (Completed)

- [x] **Core Model:** Establish "Energy Deficit" model (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff:** Validate "Rescue Cliff" at Anisotropy ~2.4 (Simulated in `outputs/sim/2026-02-22/`).
- [x] **Spinal Jetlag:** Run "Spinal Jetlag" simulation to demonstrate circadian modulation of curvature.
- [x] **Robustness:** Ensure model stability across parameter sweeps (Sensitivity Analysis).
- [x] **Toy Models:** Develop Toy Models A-E for Reviewer Defense.

## Phase 2: Clinical Validation (Weeks 1-3: March 14 - April 4)

- [ ] **Cohort Data Extraction:** Extract clinical cohort data (Cobb angle distributions, progression rates) from published literature.
- [ ] **PHV Timing:** Compare model "Instability Window" with clinical Peak Height Velocity (PHV) timing data.
- [ ] **Sexual Dimorphism:** Validate model predictions for female vs. male prevalence against epidemiological data.
- [ ] **Curve Types:** Verify if model can reproduce common curve types (e.g., Lenke classification patterns) based on initial conditions.

## Phase 3: Manuscript Preparation (Weeks 4-6: April 5 - April 25)

- [ ] **Reformatting:** Adapt `nature_manuscript.tex` to *Spine* format (IMRaD structure).
- [ ] **Abstract:** Draft Structured Abstract (Study Design, Objective, Summary of Background Data, Methods, Results, Conclusions).
- [ ] **Clinical Relevance:** Write "Clinical Relevance" section highlighting the predictive value for early intervention.
- [ ] **Figures:** Generate "Clinical Translation" figures (Model vs. Patient Data overlays).
- [ ] **References:** Update bibliography to include relevant *Spine* and *Eur Spine J* citations.

## Timeline Estimate

- **Best Case:** 4 Weeks. Assumes rapid extraction of clinical cohort data and smooth manuscript reformatting.
- **Expected:** 6 Weeks. Allowing buffer for clinical data integration and rigorous internal review.
- **Worst Case:** 8 Weeks. If clinical cohort data is difficult to extract or model fit is poor, requiring re-calibration of parameters.

## Risks & Mitigations

1.  **Clinical Data Fit:** Model predictions might not perfectly align with messy clinical cohort data.
    *   *Mitigation:* Focus on qualitative trends (e.g., onset timing, sex bias) rather than perfect quantitative fits, clearly stating limitations.
2.  **Manuscript Tone:** *Spine* requires a highly clinical focus, which our current theoretical draft lacks.
    *   *Mitigation:* Dedicate the "Clinical Relevance" section to explicitly defining how this framework aids early prediction and intervention.
