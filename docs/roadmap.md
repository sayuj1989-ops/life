# Research Roadmap: Biological Countercurvature

**Target:** *Nature* Submission
**Timeline:** 6 Weeks (March 12 - April 23, 2026)

## Phase 1: Data Gathering & Code (Weeks 1-2: March 12 - March 26)

- [ ] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$). **CRITICAL**
- [ ] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [ ] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)

## Phase 2: Manuscript Polish & Theory (Weeks 3-4: March 26 - April 09)

- [ ] **Figures:** Generate Final Publication-Quality Figures (1-7).
- [ ] **Text:** Finalize Manuscript Text (Abstract, Methods, Discussion).
- [x] **Theory:** Develop Toy Models A & B for Reviewer Defense. (Done)
- [ ] **References:** Complete Bibliography (80-100 refs).

## Phase 3: Review & Submission (Weeks 5-6: April 09 - April 23)

- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.
- [ ] **Submission:** Submit to *Nature*.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (Mar 12)** | Species Data Collection | **CRITICAL** | 🚨 **Starting** |
| **Week 2 (Mar 19)** | Cross-Species Script & Plot | Comp Bio | ⚪ Planned |
| **Week 3 (Mar 26)** | Figure Assembly (1-7) | PI / Design | ⚪ Planned |
| **Week 4 (Apr 02)** | Manuscript Final Text | PI | ⚪ Planned |
| **Week 5 (Apr 09)** | Internal Review & Polish | Team | ⚪ Planned |
| **Week 6 (Apr 16)** | **SUBMISSION** | PI | ⚪ Planned |

## Risks & Mitigations

1.  **Species Data Gap:** If data is unavailable, revert to theoretical scaling argument ($L^4$ vs $L^3$). **Risk: High.**
2.  **Simulation Artifacts:** Ensure `experiment_optimization_failure.py` results are robust to noise seeds. **Risk: Low.**
3.  **Reviewer Skepticism:** Toy models essential to clarify "Metabolic Buckling" vs simple Euler Buckling. **Mitigation:** Toy Models A & B are implemented. **Risk: Low.**
