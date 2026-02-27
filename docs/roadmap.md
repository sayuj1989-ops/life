# Research Roadmap: Biological Countercurvature

**Target:** *Nature* Submission
**Timeline:** 6 Weeks (May 25 - July 06, 2026)

## Phase 1: Data Gathering & Code (Weeks 1-2: May 25 - June 08)

- [ ] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$). **CRITICAL**
- [ ] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [ ] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)
- [x] **Toy Models:** Develop Toy Models A & B for Reviewer Defense. (Done)

## Phase 2: Manuscript Polish & Theory (Weeks 3-4: June 09 - June 22)

- [ ] **Figures:** Generate Final Publication-Quality Figures (1-7).
- [ ] **Text:** Finalize Manuscript Text (Abstract, Methods, Discussion).
- [ ] **References:** Complete Bibliography (80-100 refs).

## Phase 3: Review & Submission (Weeks 5-6: June 23 - July 06)

- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.
- [ ] **Submission:** Submit to *Nature*.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (May 25)** | Species Data Collection | **CRITICAL** | 🚨 **Starting** |
| **Week 2 (Jun 01)** | Cross-Species Script & Plot | Comp Bio | ⚪ Planned |
| **Week 3 (Jun 08)** | Figure Assembly (1-7) | PI / Design | ⚪ Planned |
| **Week 4 (Jun 15)** | Manuscript Final Text | PI | ⚪ Planned |
| **Week 5 (Jun 22)** | Internal Review & Polish | Team | ⚪ Planned |
| **Week 6 (Jun 29)** | **SUBMISSION** | PI | ⚪ Planned |

## Risks & Mitigations

1.  **Species Data Gap:** If data is unavailable, revert to theoretical scaling argument ($L^4$ vs $L^3$). **Risk: High.**
2.  **Simulation Artifacts:** Ensure `experiment_optimization_failure.py` results are robust to noise seeds. **Risk: Low.**
3.  **Reviewer Skepticism:** Toy models essential to clarify "Metabolic Buckling" vs simple Euler Buckling. **Mitigation:** Toy Models A & B are implemented. **Risk: Low.**
