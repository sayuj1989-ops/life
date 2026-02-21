# Research Roadmap: Biological Countercurvature

**Target:** *Nature* Submission
**Timeline:** 6 Weeks (March 02 - April 13, 2026)

## Phase 1: Data Gathering & Code (Weeks 1-2)

- [ ] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$).
- [ ] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [ ] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [ ] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG).

## Phase 2: Manuscript Polish & Theory (Weeks 3-4)

- [ ] **Figures:** Generate Final Publication-Quality Figures (1-7).
- [ ] **Text:** Finalize Manuscript Text (Abstract, Methods, Discussion).
- [ ] **Theory:** Develop Toy Models A & B for Reviewer Defense.
- [ ] **References:** Complete Bibliography (80-100 refs).

## Phase 3: Review & Submission (Weeks 5-6)

- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.
- [ ] **Submission:** Submit to *Nature*.

## Gantt Chart

| Week | Task | Owner |
| :--- | :--- | :--- |
| **Week 1 (Mar 02)** | Species Data Collection | **CRITICAL** |
| **Week 2 (Mar 09)** | Cross-Species Script & Plot | Comp Bio |
| **Week 3 (Mar 16)** | Figure Assembly (1-7) | PI / Design |
| **Week 4 (Mar 23)** | Manuscript Final Text | PI |
| **Week 5 (Mar 30)** | Internal Review & Polish | Team |
| **Week 6 (Apr 06)** | **SUBMISSION** | PI |

## Risks & Mitigations

1.  **Species Data Gap:** If data is unavailable, revert to theoretical scaling argument ($L^4$ vs $L^3$). **Risk: High.**
2.  **Simulation Artifacts:** Ensure `experiment_optimization_failure.py` results are robust to noise seeds. **Risk: Low.**
3.  **Reviewer Skepticism:** Toy models essential to clarify "Metabolic Buckling" vs simple Euler Buckling. **Risk: Medium.**
