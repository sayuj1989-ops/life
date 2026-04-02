# Research Roadmap: Biological Countercurvature (Spine Submission)

**Timeline:** 4 Weeks (April 02 - April 30, 2026)

## Phase 1: Computational Framework (Completed)

- [x] **Core Model:** Establish "Energy Deficit" model (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff:** Validate "Rescue Cliff" at Anisotropy ~2.4.
- [x] **Spinal Jetlag:** Run "Spinal Jetlag" simulation to demonstrate circadian modulation of curvature.
- [x] **Toy Models:** Develop Toy Models A-E for Reviewer Defense.

## Phase 2: Clinical Validation (Weeks 1-2: April 02 - April 16)

- [ ] **Cohort Data Extraction:** Extract clinical cohort data (Cobb angle distributions, progression rates) from literature.
- [ ] **PHV Timing:** Compare model "Instability Window" with clinical Peak Height Velocity (PHV) timing data.
- [ ] **Sexual Dimorphism:** Validate model predictions for female vs. male prevalence against epidemiological data.
- [ ] **Curve Types:** Verify if model can reproduce common curve types (Lenke classification) based on initial conditions (`experiment_lenke_classes.py`).

## Phase 3: Manuscript Polish & Review (Weeks 3-4: April 16 - April 30)

- [ ] **Reformatting:** Adapt `nature_manuscript.tex` to *Spine* format (IMRaD structure).
- [ ] **Abstract:** Draft Structured Abstract.
- [ ] **Clinical Relevance:** Write "Clinical Relevance" section highlighting predictive value.
- [ ] **Figures:** Generate "Clinical Translation" figures (Model vs. Patient Data overlays).
- [ ] **References:** Update bibliography to include relevant *Spine* and *Eur Spine J* citations.
- [ ] **Pre-Submission:** Run `SUBMISSION_MASTER_CHECKLIST.md`.

## Timeline Estimate

- **Best Case:** 2 Weeks. Assuming clinical mapping goes smoothly.
- **Expected:** 3 Weeks. Allowing buffer for finding exact epidemiological datasets.
- **Worst Case:** 4 Weeks. If PyElastica Cosserat parameters need re-tuning to match human physiological ranges.

## Risks & Mitigations

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. **Risk: Medium.** *Mitigation:* Focus on qualitative onset timing and relative scaling.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging. **Risk: High.** *Mitigation:* Treat the simulation strictly as an *in silico* experiment in the Methods section.
3.  **Missing References:** The manuscript may lack sufficient targeted clinical references. **Risk: Medium.** *Mitigation:* Execute targeted literature review prioritizing recent *Spine* and *Eur Spine J* papers.

## Next 7 / 30 Days Plan

**Next 7 Days (Sprint):**
- **Day 1-2:** Execute CLIN-01. Extract Peak Height Velocity (PHV) cohort data from literature and overlay with our PyElastica instability window.
- **Day 3-4:** Execute CLIN-02. Refine `experiment_lenke_classes.py` to produce a finalized figure mapping spatial deficits to Lenke Classifications.
- **Day 5-6:** Execute CLIN-03. Map sexual dimorphism metrics to model parameters.
- **Day 7:** Begin structural draft overhaul (IMRaD) for *Spine* (MS-01).

**Next 30 Days:**
- **Weeks 2-3:** Finalize all "Clinical Translation" figures, complete the IMRaD manuscript reformatting, and circulate the updated draft for PI review.
- **Week 4:** Address final internal review feedback, run submission checklist, and submit to *Spine*.
