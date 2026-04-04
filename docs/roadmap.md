# Research Roadmap: Biological Countercurvature

**Timeline:** 4 Weeks (May 26 - June 23, 2026)
**Target:** *Spine* Submission (July 2026)

## Phase 1: Computational Framework (Completed)
- [x] **Core Model:** "Energy Deficit" bifurcation established (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff Validation:** Validated anisotropy cliff at ~2.4 (`experiment_anisotropy_rescue.py`).
- [x] **Spinal Jetlag:** Circadian modulation of curvature demonstrated (`experiment_spinal_jetlag.py`).
- [x] **Toy Models:** Physical intuitions (A-E) implemented (`docs/toy_models_plan.md`).

## Phase 2: Clinical Validation (Weeks 1-2: May 26 - June 09)
- [ ] **Cohort Data Extraction:** Extract clinical cohort data (Cobb angle distributions, progression rates) from published literature.
- [ ] **PHV Timing:** Compare model "Instability Window" with clinical Peak Height Velocity (PHV) timing data.
- [ ] **Sexual Dimorphism:** Validate model predictions for female vs. male prevalence against epidemiological data.
- [ ] **Curve Types:** Verify if model can reproduce common curve types (e.g., Lenke classification patterns) based on initial conditions.

## Phase 3: Manuscript Preparation (Weeks 3-4: June 09 - June 23)
- [ ] **Reformatting:** Adapt manuscript to *Spine* format (IMRaD structure).
- [ ] **Abstract:** Draft Structured Abstract (Study Design, Objective, Summary of Background Data, Methods, Results, Conclusions).
- [ ] **Clinical Relevance:** Write "Clinical Relevance" section highlighting the predictive value for early intervention.
- [ ] **Figures:** Generate "Clinical Translation" figures (Model vs. Patient Data overlays).

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (May 26)** | Clinical Data Extraction & Overlays | PI / Comp Sci | 🚨 **Starting** |
| **Week 2 (Jun 02)** | Clinical Overlays & Curve Types | Comp Sci | ⚪ Planned |
| **Week 3 (Jun 09)** | Manuscript IMRaD Reformatting | PI | ⚪ Planned |
| **Week 4 (Jun 16)** | Internal Review & Submission Prep | Team | ⚪ Planned |

## Timeline Estimate

- **Best Case:** 2 Weeks. Assuming clinical data maps directly and reformatting goes quickly.
- **Expected:** 4 Weeks. Allowing buffer for finding the right epidemiological datasets and internal review.
- **Worst Case:** 6 Weeks. If clinical validation mapping fails and requires significant re-tuning of the PyElastica Cosserat parameters to match human physiological ranges.

## Risks & Mitigations

1.  **Clinical Data Mismatch:** Abstract physics parameters may not map linearly to clinical metrics like Cobb angle progression. **Mitigation:** Focus on qualitative onset timing and relative scaling.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections is challenging. **Mitigation:** Treat the simulation strictly as an *in silico* experiment in the Methods section.
