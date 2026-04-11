# Research Roadmap: Biological Countercurvature

**Timeline:** 4 Weeks (March 01 - March 29, 2026) -> **Updated Target Submission Date:** 2026-04-06

## Phase 1: Data Gathering & Code (Completed)

- [x] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$). **CRITICAL**
- [x] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [x] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)
- [x] **Toy Models:** Develop Toy Models A & B for Reviewer Defense. (Done)
- [x] **Core Model:** Establish "Energy Deficit" model (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff:** Validate "Rescue Cliff" at Anisotropy ~2.4 (Simulated in `outputs/sim/2026-02-22/`).
- [x] **Spinal Jetlag:** Run "Spinal Jetlag" simulation to demonstrate circadian modulation of curvature.

## Phase 2: Clinical Validation (Weeks 3-4)

- [ ] **Cohort Data Extraction:** Extract clinical cohort data (Cobb angle distributions, progression rates) from published literature.
- [ ] **PHV Timing:** Compare model "Instability Window" with clinical Peak Height Velocity (PHV) timing data.
- [ ] **Sexual Dimorphism:** Validate model predictions for female vs. male prevalence against epidemiological data.
- [ ] **Curve Types:** Verify if model can reproduce common curve types (e.g., Lenke classification patterns) based on initial conditions.

## Phase 3: Manuscript Polish & Theory (Weeks 5-6)

- [ ] **Reformatting:** Adapt `nature_manuscript.tex` to *Spine* format (IMRaD structure).
- [ ] **Abstract:** Draft Structured Abstract (Study Design, Objective, Summary of Background Data, Methods, Results, Conclusions).
- [ ] **Clinical Relevance:** Write "Clinical Relevance" section highlighting the predictive value for early intervention.
- [ ] **Figures:** Generate "Clinical Translation" figures (Model vs. Patient Data overlays).
- [ ] **References:** Update bibliography to include relevant *Spine* and *Eur Spine J* citations.
- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1-2 (Mar 01)** | Computational Framework | PI | ✅ **Done** |
| **Week 3-4 (Mar 15)** | Clinical Validation | PI | 🚨 **Active** |
| **Week 5 (Mar 29)** | Manuscript IMRaD Rewrite | PI | ⚪ Planned |
| **Week 6 (Apr 05)** | Internal Review & Submission | PI | ⚪ Planned |

## Timeline Estimate

- **Best Case:** 2.5 Weeks. Assuming existing toy models map perfectly to clinical cohort data.
- **Expected:** 4 Weeks. Factoring in significant time for the IMRaD rewrite and bibliography expansion.
- **Worst Case:** 6 Weeks. If reviewer defense requires running full 3D PyElastica models over long developmental timelines instead of current pseudo-static approximations.

## Risks & Mitigations

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. **Risk: High.** *Mitigation:* Focus on qualitative onset timing and relative scaling.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging. **Risk: Medium.** *Mitigation:* Treat the simulation strictly as an *in silico* experiment in the Methods section.
3.  **Missing References:** The Nature manuscript is still missing critical references (around 70-85 needed). **Risk: High.** *Mitigation:* Focus heavily on literature review and reference expansion in the next few days.

## Next 7 / 30 Days Plan

**Next 7 Days (Sprint):**
- **Day 1-2:** Run and finalize `toy_model_lenke_classes.py` predictions.
- **Day 3-4:** Complete literature search for high-quality PHV vs. Cobb angle progression charts.
- **Day 5-6:** Generate clinical translation figures overlaying model data.
- **Day 7:** Begin structural reformatting of `main.tex` to IMRaD.

**Next 30 Days:**
- **Weeks 2-3:** Finish full manuscript rewrite.
- **Week 4:** Complete PI internal review and pre-submission checks for *Spine*.
