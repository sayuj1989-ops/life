# Research Roadmap: Biological Countercurvature

**Timeline:** April 07 - May 07, 2026

## Phase 1: Data Gathering & Code (Completed)

- [x] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$).
- [x] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [x] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)
- [x] **Toy Models:** Develop Toy Models A-E for Reviewer Defense. (Done)
- [x] **Evidence Collection:** Continuous evidence notes generated.

## Phase 2: Clinical Validation & Spine Pivot (Current)

- [ ] **CLIN-01:** Map model instability windows against Peak Height Velocity (PHV) clinical growth charts.
- [ ] **CLIN-02:** Refine `toy_model_lenke_classes.py` to predict Lenke 1-6 classifications.
- [ ] **CLIN-03:** Map sexual dimorphism metrics to model parameters.
- [ ] **CLIN-04:** Extract and map ALSPAC, Marfan data to model parameters.
- [ ] **MS-01:** Structural draft overhaul (IMRaD) for *Spine*.
- [ ] **MS-02:** Integrate "Clinical Relevance" section.

## Phase 3: Review & Submission (Future)

- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.

## Gantt Chart

| Phase | Task | Status |
| :--- | :--- | :--- |
| **Phase 2 (Sprint)** | CLIN-01: PHV Mapping | 🚨 **Starting** |
| **Phase 2 (Sprint)** | CLIN-02: Lenke Prediction | ⚪ Planned |
| **Phase 2 (Sprint)** | CLIN-03 & CLIN-04: Data Mapping | ⚪ Planned |
| **Phase 2 (Sprint)** | MS-01 & MS-02: IMRaD & Clinical Relevance | ⚪ Planned |
| **Phase 3 (Next 30 Days)** | Internal Review & Submission | ⚪ Planned |

## Timeline Estimate

- **Best Case:** 2 Weeks. Cohort data extraction is straightforward; existing simulations cleanly map to PHV timing and Lenke classes. Manuscript reformatting completed swiftly.
- **Expected:** 3 Weeks. Allows buffer for complex literature extraction to find exact epidemiological datasets matching simulation parameters, plus internal iterations on the "Clinical Relevance" text.
- **Worst Case:** 4-5 Weeks. If the clinical validation mapping fails and requires significant re-tuning of the PyElastica Cosserat parameters to match human physiological ranges.

## Risks & Mitigations

1.  **Clinical Mapping Complexity:** Finding exact cohort data matching simulation parameters might be difficult. **Risk: High.** *Mitigation:* Focus on qualitative and relative mappings initially.
2.  **IMRaD Reformatting:** Transitioning from theory-heavy to standard IMRaD could be time-consuming. **Risk: Medium.** *Mitigation:* Ensure sections are explicitly dedicated to specific clinical relevance points.

## Next 7 / 30 Days Plan

**Next 7 Days (Sprint):**
- **Days 1-2:** Address **CLIN-01**: Execute literature search for high-quality Peak Height Velocity (PHV) cohort charts and begin `experiment_phv_timing.py`.
- **Days 3-4:** Address **CLIN-02**: Finalize output parameters of the Lenke classification script (`toy_model_lenke_classes.py`) to robustly predict Lenke 1-6 classifications.
- **Days 5-6:** Address **CLIN-03** & **CLIN-04**: Extract and map ALSPAC, Marfan, and Sexual Dimorphism data to model parameters.
- **Day 7:** Begin **MS-01**: Structural draft overhaul (IMRaD) for *Spine* and integrate "Clinical Relevance" section (**MS-02**).

**Next 30 Days:**
- **Weeks 2-3:** Complete MS-01, MS-02. Finalize all "Clinical Translation" figures (MS-03) and update bibliography (MS-04).
- **Week 4:** Complete internal PI review of the IMRaD manuscript and supplementary data. Run submission checklist and finalize the package for *Spine*.
