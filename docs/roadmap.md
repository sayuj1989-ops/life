# Research Roadmap: Biological Countercurvature

**Target:** *Nature* Submission
**Timeline:** 6 Weeks (March 05 - April 16, 2026)

## Phase 1: Data Gathering & Code (Weeks 1-2: March 05 - March 19)

- [x] **Data:** Collect Literature Data for Cross-Species Validation (9 Species: $L, R, EI, Mass$). **COMPLETED** (See `data/species_parameters.csv`)
- [x] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3. **COMPLETED** (See `scripts/analysis/cross_species_scaling.py`)
- [ ] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`. (Next Priority)
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)

## Phase 2: Manuscript Polish & Theory (Weeks 3-4: March 20 - April 02)

- [ ] **Figures:** Generate Final Publication-Quality Figures (1-7).
- [ ] **Text:** Finalize Manuscript Text (Abstract, Methods, Discussion).
- [x] **Theory:** Develop Toy Models A & B for Reviewer Defense. (Done)
- [ ] **References:** Complete Bibliography (80-100 refs).

## Phase 3: Review & Submission (Weeks 5-6: April 03 - April 16)

- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.
- [ ] **Submission:** Submit to *Nature*.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (Mar 05)** | Cross-Species Validation (Done) & Mutation Mapping | Comp Bio | 🟡 **In Progress** |
| **Week 2 (Mar 12)** | Figure Generation (High DPI) | Comp Bio | ⚪ Planned |
| **Week 3 (Mar 19)** | Manuscript Text Finalization | PI | ⚪ Planned |
| **Week 4 (Mar 26)** | Reference Completion | PI | ⚪ Planned |
| **Week 5 (Apr 02)** | Internal Review & Polish | Team | ⚪ Planned |
| **Week 6 (Apr 09)** | **SUBMISSION** | PI | ⚪ Planned |

## Risks & Mitigations

1.  **Mutation Specificity:** The claim of "5 specific variants" is currently unsupported by code. **Mitigation:** Use generic parameter sweeps and label them "Model for FBN1-type defect".
2.  **Figure Consistency:** Ensuring all panels (simulation, protein, theory) share a consistent aesthetic. **Mitigation:** Use a centralized plotting script or style guide.
