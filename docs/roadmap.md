# Research Roadmap: Biological Countercurvature

**Timeline:** 4 Weeks (April 03, 2026 - May 01, 2026)
**Target Journal:** Spine (Pivot from Nature)

## Phase 1: Data Gathering & Computational Core (Completed)
- [x] **Data:** Collect Literature Data for Cross-Species Validation (9 Species).
- [x] **Code:** Core physics pipelines validated (Energy Deficit, Anisotropy Rescue, Spinal Jetlag).
- [x] **Toy Models:** Physical intuitions (Models A-E) completed.

## Phase 2: Clinical Validation Mapping (Current Phase: April 03 - April 17)
- [ ] **Data:** Extract Peak Height Velocity (PHV) cohort charts from literature (CLIN-01).
- [ ] **Data:** Map model parameters to 7:1 Female-to-Male prevalence (CLIN-03).
- [ ] **Code/Figures:** Refine Lenke class predictions (CLIN-02) and generate Clinical Overlay figures.

## Phase 3: Manuscript IMRaD Reformatting & Submission (April 17 - May 01)
- [ ] **Text:** Convert draft to standard IMRaD structure (MS-01).
- [ ] **Text:** Write "Clinical Relevance" section framing AIS progression as a delay-dependent bifurcation.
- [ ] **Review:** Internal PI review.
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.

## Gantt Chart

| Week | Task | Owner | Status |
| :--- | :--- | :--- | :--- |
| **Week 1 (Apr 03)** | Clinical Lit Extraction (PHV/Sex) | PI / Comp Bio | 🚨 **Starting** |
| **Week 2 (Apr 10)** | Clinical Figure Assembly / Overlays | Comp Bio | ⚪ Planned |
| **Week 3 (Apr 17)** | IMRaD Manuscript Reformatting | PI | ⚪ Planned |
| **Week 4 (Apr 24)** | Internal Review & **SUBMISSION** | Team | ⚪ Planned |

## Timeline Estimate
- **Best Case:** 2 Weeks.
- **Expected:** 3 Weeks. Buffer for extracting exact clinical parameters and textual rewrite.
- **Worst Case:** 4-5 Weeks. If PyElastica parameters require re-tuning to fit clinical ranges.

## Risks & Mitigations
1. **Clinical Data Mismatch:** Abstract parameters ($\chi_\kappa$) may not perfectly map to Cobb angle progression. *Mitigation:* Focus on qualitative onset timing and relative scaling.
2. **IMRaD Reformatting Burden:** Stripping dense theory into supplementary sections. *Mitigation:* Treat simulation strictly as *in silico* experiment in Methods.
