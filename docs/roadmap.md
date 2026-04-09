# Research Roadmap: Biological Countercurvature

**Timeline:** 4 Weeks (March 22 - April 19, 2026)

## Phase 1: Computational Framework (Completed)

- [x] **Core Model:** Establish "Energy Deficit" model (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff:** Validate "Rescue Cliff" at Anisotropy ~2.4 (`experiment_anisotropy_rescue.py`).
- [x] **Spinal Jetlag:** Run "Spinal Jetlag" simulation to demonstrate circadian modulation of curvature.
- [x] **Robustness:** Ensure model stability across parameter sweeps (Sensitivity Analysis).

## Phase 2: Clinical Validation (Weeks 1-2: March 22 - April 05)

- [x] **PHV Timing Mapping:** Map instability window against clinical PHV (`scripts/experiment_phv_timing.py`).
- [x] **Curve Type Prediction:** Refine Lenke 1-6 classifications prediction (`scripts/experiments/toy_model_lenke_classes.py`).
- [x] **Sexual Dimorphism:** Map model parameters to prevalence data (`scripts/experiment_sexual_dimorphism.py`).
- [ ] **ALSPAC/Marfan Cross-check:** Validate "Energy Deficit" vs low BMI (ALSPAC) and anisotropy vs Marfan syndrome prevalence.

## Phase 3: Manuscript Polish & Theory (Weeks 3-4: April 05 - April 19)

- [ ] **IMRaD Restructuring:** Convert theory-dense draft into standard Introduction, Methods, Results, and Discussion sections.
- [ ] **"Clinical Relevance" Section:** Draft dedicated section detailing the predictive clinical value for early intervention.
- [ ] **Figure Finalization:** Assemble "Clinical Translation" figures overlaying model predictions on patient cohort data.
- [ ] **Targeted References:** Update bibliography focusing on *Spine*, *Eur Spine J*, and clinical biomechanics.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (Mar 01)** | Figure Assembly (1-7) | PI / Design | 🚨 **Starting** |
| **Week 2 (Mar 08)** | Manuscript Final Text | PI | ⚪ Planned |
| **Week 3 (Mar 15)** | Internal Review & Polish | Team | ⚪ Planned |
| **Week 4 (Mar 22)** | **SUBMISSION** | PI | ⚪ Planned |

## Timeline Estimate

- **Best Case:** 2 Weeks. Assuming figure assembly goes smoothly and internal review clears quickly.
- **Expected:** 3 Weeks. Allowing some buffer for editing the manuscript sections and verifying specific Nature formatting requirements.
- **Worst Case:** 5 Weeks. If figure redesign is requested during internal review or if more parameter sweeps are deemed necessary.

## Risks & Mitigations

1.  **Figure Inconsistency:** Script outputs may lack unified visual styling. **Risk: Medium.** *Mitigation:* Unify style across scripts immediately.
2.  **Missing References:** The Nature manuscript is still missing critical references (around 70-85 needed). **Risk: High.** *Mitigation:* Focus heavily on literature review and reference expansion in the next few days.
3.  **Reviewer Skepticism:** Toy models essential to clarify "Metabolic Buckling" vs simple Euler Buckling. **Mitigation:** Toy Models A & B are implemented. **Risk: Low.**

## Next 7 / 30 Days Plan

**Next 7 Days (Sprint):**
- **Day 1-2:** Output all final plot figures from updated scripts (Cross-Species, Optimization Failure, S-Shape).
- **Day 3-4:** Assemble finalized Panels for Figures 1-4.
- **Day 5-6:** Finish expanding the manuscript bibliography (`references.bib`) and integrate into `manuscript/submission_manuscript.tex`.
- **Day 7:** Trim the Abstract and finalize standard Nature text styling requirements.

**Next 30 Days:**
- **Weeks 2-3:** Finalize all text formatting, complete internal team review of the full manuscript and supplementary data.
- **Week 4:** Pre-submission Checklist and submit to *Nature*.
