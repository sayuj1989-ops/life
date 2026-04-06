# Research Roadmap: Biological Countercurvature

**Timeline:** 4 Weeks (April 06 - May 04, 2026)

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

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (Apr 06)** | PHV & Clinical Mapping | PI / Comp Sci | 🚨 **Starting** |
| **Week 2 (Apr 13)** | IMRaD Restructuring | PI | ⚪ Planned |
| **Week 3 (Apr 20)** | Figure Assembly (Clinical) | Design | ⚪ Planned |
| **Week 4 (Apr 27)** | Internal Review & SUBMISSION | PI / Team | ⚪ Planned |

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
- **Day 1-2:** Conduct targeted literature search for Peak Height Velocity (PHV) cohort charts.
- **Day 3-4:** Complete `CLIN-02`: Finalize parameters for Lenke classification script.
- **Day 5-6:** Write `experiment_phv_timing.py` (CLIN-01) mapping model to extracted PHV data.
- **Day 7:** Update `docs/pending_work.md` and initiate MS-01 (IMRaD Restructuring).

**Next 30 Days:**
- **Weeks 2-3:** Complete IMRaD restructuring, generate final Clinical Translation figures (MS-03), and draft "Clinical Relevance" section (MS-02).
- **Week 4:** Final Internal Review of IMRaD version, targeted reference updates, and Pre-Submission checklist completion.
