# Research Roadmap: Biological Countercurvature

**Target:** *Spine* Submission (IF: 3.30, Q1, H-index: 300)
**Strategy:** "A computational framework predicting adolescent scoliosis onset" with clinical validation against published cohort data.
**Timeline:** 6 Weeks (Feb 23 - April 06, 2026)
**Latest Progress Update:** [docs/progress_update_2026-03-28.md](progress_update_2026-03-28.md)

## Phase 1: Computational Framework (Weeks 1-2)

- [x] **Core Model:** Establish "Energy Deficit" model (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff:** Validate "Rescue Cliff" at Anisotropy ~2.4 (`experiment_anisotropy_rescue.py`).
- [x] **Spinal Jetlag:** Run "Spinal Jetlag" simulation to demonstrate circadian modulation of curvature.
- [ ] **Robustness:** Ensure model stability across parameter sweeps (Sensitivity Analysis).

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

- **Best Case:** 1-2 Weeks. Cohort data extraction proceeds smoothly; simulations map perfectly to clinical data. IMRaD format quickly adapted.
- **Expected:** 2-3 Weeks. Accounts for potential difficulties in aligning abstract physics parameters to clinical metrics.
- **Worst Case:** 4 Weeks. Clinical validation mapping requires significant re-tuning of PyElastica Cosserat parameters to match human physiological ranges.

## Risks & Mitigations

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map perfectly to clinical metrics like Cobb angle progression.
    *   *Mitigation:* Focus on relative scaling and qualitative onset timing rather than exact degree predictions.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging.
    *   *Mitigation:* Treat the simulation strictly as an *in silico* experiment in the Methods section.

## Next 7 / 30 Days Plan

**Next 7 Days (Phase 2 Clinical Sprint):**
- Execute **CLIN-01**: Map PHV data.
- Execute **CLIN-02**: Finalize Lenke Classifications mapping.
- Execute **CLIN-03**: Map sexual dimorphism metrics.
- Begin structural draft overhaul for **MS-01**.

**Next 30 Days:**
- Finalize all figures and IMRaD manuscript reformatting.
- Internal PI Review.
- Final submission process.
