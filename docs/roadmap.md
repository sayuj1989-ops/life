# Research Roadmap: Biological Countercurvature

**Timeline:** 4 Weeks (March 01 - April 29, 2026)

## Phase 1: Data Gathering & Code (Completed)

- [x] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$). **CRITICAL**
- [x] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [x] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)
- [x] **Toy Models:** Develop Toy Models A & B for Reviewer Defense. (Done)

## Phase 2: Manuscript Polish & Theory (Weeks 1-2: April 05 - April 19)

- [ ] **Figures:** Generate Final Publication-Quality Figures (1-7).
- [ ] **Text:** Finalize Manuscript Text (Abstract, Methods, Discussion, IMRaD restructure).
- [ ] **References:** Complete Bibliography (80-100 refs).
- [ ] **Validation:** Clinical mapping of simulation models against human data (PHV, Lenke).

## Phase 3: Review & Submission (Weeks 3-4: April 19 - April 29)

- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (Apr 05)** | Clinical Validation (PHV/Lenke/Sex) | PI / Design | 🚨 **Starting** |
| **Week 2 (Apr 12)** | IMRaD Manuscript Final Text | PI | ⚪ Planned |
| **Week 3 (Apr 19)** | Internal Review & Polish | Team | ⚪ Planned |
| **Week 4 (Apr 26)** | **SUBMISSION** | PI | ⚪ Planned |

## Timeline Estimate

- **Best Case:** 2 Weeks. Assuming figure assembly goes smoothly and internal review clears quickly.
- **Expected:** 3 Weeks. Allowing some buffer for editing the manuscript sections and verifying specific Spine formatting requirements.
- **Worst Case:** 4 Weeks. If figure redesign is requested during internal review or if clinical data mapping needs tuning.

## Risks & Mitigations

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. **Risk: Medium.** *Mitigation:* Focus on qualitative onset timing and relative scaling.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging. **Risk: Medium.** *Mitigation:* Treat the simulation strictly as an *in silico* experiment in the Methods section.
3.  **Figure Inconsistency:** Script outputs may lack unified visual styling. **Risk: Medium.** *Mitigation:* Unify style across scripts immediately.

## Next 7 / 30 Days Plan

**Next 7 Days (Sprint):**
- **Day 1-2:** Output all final plot figures from updated scripts (Cross-Species, Optimization Failure, S-Shape).
- **Day 3-4:** Assemble finalized Panels for Figures 1-4.
- **Day 5-6:** Finish expanding the manuscript bibliography (`references.bib`) and integrate into `manuscript/submission_manuscript.tex`.
- **Day 7:** Trim the Abstract and finalize standard Spine text styling requirements.

**Next 30 Days:**
- **Weeks 2-3:** Finalize all text formatting, complete internal team review of the full manuscript and supplementary data.
- **Week 4:** Pre-submission Checklist and submit to *Spine*.
