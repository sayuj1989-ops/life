# Research Roadmap: Biological Countercurvature

**Target:** *Spine* Submission (IF: 3.30, Q1, H-index: 300)
**Strategy:** "A computational framework predicting adolescent scoliosis onset" with clinical validation against published cohort data.
**Timeline:** 6 Weeks (Feb 23 - April 06, 2026)
**Latest Progress Update:** [docs/progress_update_2026-03-30.md](progress_update_2026-03-30.md)

## Phase 1: Computational Framework (Weeks 1-2)

- [x] **Core Model:** Establish "Energy Deficit" model (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff:** Validate "Rescue Cliff" at Anisotropy ~2.4 (`experiment_anisotropy_rescue.py`).
- [x] **Spinal Jetlag:** Run "Spinal Jetlag" simulation to demonstrate circadian modulation of curvature.
- [x] **Robustness:** Ensure model stability across parameter sweeps (Sensitivity Analysis).

## Phase 2: Clinical Validation (Weeks 3-4)

- [ ] **Cohort Data Extraction:** Extract clinical cohort data (Cobb angle distributions, progression rates) from published literature.
- [ ] **PHV Timing:** Compare model "Instability Window" with clinical Peak Height Velocity (PHV) timing data.
- [ ] **Sexual Dimorphism:** Validate model predictions for female vs. male prevalence against epidemiological data.
- [ ] **Curve Types:** Verify if model can reproduce common curve types (e.g., Lenke classification patterns) based on initial conditions.

## Phase 3: Manuscript Preparation (Weeks 5-6)

- [ ] **Reformatting:** Adapt manuscript to *Spine* format (IMRaD structure).
- [ ] **Abstract:** Draft Structured Abstract (Study Design, Objective, Summary of Background Data, Methods, Results, Conclusions).
- [ ] **Clinical Relevance:** Write "Clinical Relevance" section highlighting predictive value.
- [ ] **Figures:** Generate "Clinical Translation" figures (Model vs. Patient Data overlays).
- [ ] **References:** Update bibliography to include relevant *Spine* and *Eur Spine J* citations.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1-2** | Computational Framework | Team | ✅ **Mostly Complete** |
| **Week 3-4** | Clinical Validation Mapping | PI | 🚨 **Active Sprint** |
| **Week 5** | Manuscript Reformatting (IMRaD) | PI | ⚪ Planned |
| **Week 6 (Apr 06)**| Internal Review & **SUBMISSION** | PI | ⚪ Planned |

## Timeline Estimate

- **Best Case:** 2 Weeks. Cohort data extraction is straightforward; existing simulations cleanly map to PHV timing and Lenke classes. Manuscript reformatting completed swiftly.
- **Expected:** 3 Weeks. Buffer for complex literature extraction matching specific simulation parameters, plus internal iterations on the "Clinical Relevance" text.
- **Worst Case:** 4 Weeks. Clinical validation mapping requires significant re-tuning of PyElastica Cosserat parameters to match human physiological ranges.

## Risks & Mitigations

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle.
    *   *Mitigation:* Use relative scaling and clear proxy definitions. Focus on qualitative timing (e.g., onset at PHV) rather than exact degree predictions.
2.  **IMRaD Reformatting:** The existing Nature-style draft is theory-dense and lacks a traditional Methods section.
    *   *Mitigation:* Strip extensive math to Supplementary material. Build a highly structured, plain-language Methods section detailing the simulation setup as an *in silico* experiment.

## Next 7 / 30 Days Plan

**Next 7 Days (Sprint - Phase 2 Initiation):**
- **Day 1-2:** Extract Peak Height Velocity (PHV) cohort data from literature and overlay with our PyElastica instability window.
- **Day 3-4:** Refine `toy_model_lenke_classes.py` to produce a finalized figure mapping spatial deficits to Lenke Classifications.
- **Day 5-6:** Map sexual dimorphism metrics to model parameters based on literature review.
- **Day 7:** Begin structural draft overhaul (IMRaD) for *Spine*.

**Next 30 Days:**
- **Weeks 2-3:** Finalize all "Clinical Translation" figures, complete the IMRaD manuscript reformatting, and circulate the updated draft for PI review.
- **Week 4:** Address final internal review feedback, run submission checklist, and submit to *Spine*.
