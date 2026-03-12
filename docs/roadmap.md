# Research Roadmap: Biological Countercurvature

**Target:** *Nature* Submission
**Timeline:** 4 Weeks (March 01 - March 29, 2026)

## Phase 1: Data Gathering & Code (Completed)
- [x] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$). **CRITICAL**
- [x] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [x] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)
- [x] **Toy Models:** Develop Toy Models A & B for Reviewer Defense. (Done)

## Phase 2: Manuscript Polish & Theory (Weeks 1-2: March 01 - March 15)
- [ ] **Figures:** Generate Final Publication-Quality Figures (1-7).
- [ ] **Text:** Finalize Manuscript Text (Abstract, Methods, Discussion).
- [ ] **References:** Complete Bibliography (80-100 refs).

## Phase 3: Review & Submission (Weeks 3-4: March 15 - March 29)
- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.
- [ ] **Submit:** Submit to *Nature*.

## Detailed Schedule

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

## 8. Next 7 / 30 Days Plan

**Next 7 Days (Sprint):**
- **Day 1-2:** Output all final plot figures from updated scripts (Cross-Species, Optimization Failure, S-Shape).
- **Day 3-4:** Assemble finalized Panels for Figures 1-4.
- **Day 5-6:** Finish expanding the manuscript bibliography (`references.bib`) and integrate into `manuscript/submission_manuscript.tex`.
- **Day 7:** Trim the Abstract and finalize standard Nature text styling requirements.

**Next 30 Days:**
- **Weeks 2-3:** Finalize all text formatting, complete internal team review of the full manuscript and supplementary data.
- **Week 4:** Pre-submission Checklist and submit to *Nature*.
