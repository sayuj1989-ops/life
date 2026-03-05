# Research Roadmap: Biological Countercurvature

**Target:** *Nature* Submission
**Timeline:** 4 Weeks (March 01 - March 29, 2026)

## Phase 1: Data Gathering & Code (Completed)

- [x] **Data:** Collect literature data for cross-species validation (10 species; parameters: $L, EI, \text{Mass}$). **CRITICAL**
- [x] **Code:** Create `experiment_cross_species_scaling.py` and reproduce Figure 3.
- [x] **Code:** Implement Specific Mutation Mapping in `experiment_optimization_failure.py`.
- [x] **Validation:** Run all scripts and ensure clean outputs (CSV/PNG). (Core & Toy Models Done)
- [x] **Toy Models:** Develop Toy Models A & B for Reviewer Defense. (Done)
- [x] **Simulation Sweeps:** Completed advanced PyElastica sweeps (Taper, Kyphosis, Torsion).

## Phase 2: Manuscript Polish & Theory (Weeks 1-2: March 01 - March 15)

- [ ] **Figures:** Generate Final Publication-Quality Figures (1-7).
- [x] **Text:** Finalize Manuscript Text (Abstract, Methods, Discussion). Format updated to Nature standards.
- [ ] **References:** Complete Bibliography (80-100 refs).

## Phase 3: Review & Submission (Weeks 3-4: March 16 - March 29)

- [ ] **Internal Review:** PI Review of full package (Manuscript + Supp Info).
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.
- [ ] **Submission:** Submit to *Nature*.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (Mar 01)** | Code & Sweep Validation | Team | ✅ **Completed** |
| **Week 2 (Mar 08)** | Manuscript Final Text & Refs | PI | 🟡 **In Progress** |
| **Week 3 (Mar 15)** | Figure Assembly (1-7) & Polish | Design/Team | 🚨 **Starting** |
| **Week 4 (Mar 22)** | Internal Review & **SUBMISSION** | PI | ⚪ Planned |

## Risks & Mitigations

1.  **Figure Inconsistency:** Script outputs may lack unified visual styling. **Risk: Medium.** *Mitigation:* Unify style across scripts immediately via standard generation scripts.
2.  **Missing References:** The Nature manuscript is still missing critical references (around 70-85 needed). **Risk: High.** *Mitigation:* Focus heavily on literature review and reference expansion in the next few days.
3.  **Reviewer Skepticism:** Toy models essential to clarify "Metabolic Buckling" vs simple Euler Buckling. **Mitigation:** Toy Models A, B, and C are now fully implemented and documented. **Risk: Low.**
