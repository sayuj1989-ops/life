# Research Roadmap: Biological Countercurvature

**Timeline:** 4 Weeks (April 01 - April 29, 2026)

## Phase 1: Data Gathering & Code (Completed)

- [x] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$).
- [x] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [x] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)
- [x] **Toy Models:** Develop Toy Models A & B for Reviewer Defense. (Done)

## Phase 2: Clinical Validation (Weeks 1-2: April 01 - April 15)

- [x] **CLIN-01:** Map PHV Timing against model instability window.
- [ ] **CLIN-02:** Map spatial deficits to predict Lenke Classifications 1-6.
- [ ] **CLIN-03:** Map parameters (stiffness ratio, growth rate) to test sexual dimorphism predictions.
- [ ] **FIG-01:** Generate Clinical Overlays showing simulated trajectories vs human cohort data.

## Phase 3: Manuscript Reformatting & Review (Weeks 3-4: April 15 - April 29)

- [ ] **MS-01:** IMRaD Restructuring for the *Spine* journal.
- [ ] **MS-02:** Draft dedicated "Clinical Relevance" section.
- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (Apr 01)** | Clinical Validation (Lenke, Sex Ratio) | Comp Bio | 🚨 **Starting** |
| **Week 2 (Apr 08)** | Clinical Overlay Figures Assembly | Design | ⚪ Planned |
| **Week 3 (Apr 15)** | Manuscript IMRaD Restructuring | PI | ⚪ Planned |
| **Week 4 (Apr 22)** | Internal Review & **SUBMISSION** | Team | ⚪ Planned |

## Timeline Estimate

- **Best Case:** 2 Weeks. Assuming validation mappings cleanly match human cohort shapes without major retuning.
- **Expected:** 3 Weeks. Allowing some buffer for editing the clinical sections and verifying *Spine* formatting requirements.
- **Worst Case:** 5 Weeks. If mapping sexual dimorphism requires rewriting core Cosserat assumptions or running larger parameter sweeps.

## Risks & Mitigations

1.  **Clinical Data Mismatch:** Abstract physics parameters might not smoothly map onto Lenke curve shapes. **Risk: Medium.** *Mitigation:* Focus on qualitative mappings and spatial deficit interactions rather than perfect Cobb angle matching.
2.  **IMRaD Reformatting Burden:** Rewriting from Nature format to Spine format means condensing heavy math. **Risk: High.** *Mitigation:* Move deep Cosserat derivations to the Supplement early, treating the code strictly as an *in silico* model in Methods.

## Next 7 / 30 Days Plan

**Next 7 Days (Sprint):**
- **Day 1-2:** Output final spatial predictions for Lenke 1-6.
- **Day 3-4:** Output validation plots for female/male incidence predictions based on growth duration.
- **Day 5-6:** Draft the new "Methods" structure for the *Spine* journal avoiding deep math derivations.
- **Day 7:** Assemble the PHV Timing and Lenke outputs into the new "Clinical Translation" multi-panel figure.

**Next 30 Days:**
- **Weeks 2-3:** Finalize all clinical plots, restructure the rest of the manuscript, complete internal team review.
- **Week 4:** Pre-submission Checklist and submit to *Spine*.
