# Research Progress Update: Biological Countercurvature

**Date:** 2026-04-11
**Role:** PI / Program Manager / Computational Scientist
**Target Journal:** Spine (IF: 3.30, Q1, H-index: 300)
**Why:** The highest prestige spine journal by H-index. Publishes basic science.
**Fit score:** 6/10 — High bar; will need experimental validation or strong clinical dataset comparison.
**Strategy:** Reframe as "A computational framework predicting adolescent scoliosis onset" with clinical validation against published cohort data.

## Executive summary
The project strategy has officially pivoted from a *Nature* submission to the *Spine* journal, reframing the core thesis as "A computational framework predicting adolescent scoliosis onset." Phase 1 (Computational Framework) is 75% complete, with the core "Energy Deficit" model, Rescue Cliff, and Spinal Jetlag simulations validated. We are now transitioning to Phase 2 (Clinical Validation) to explicitly map model outputs (e.g., instability windows) against published epidemiological data such as Peak Height Velocity (PHV), Lenke classifications, and sexual dimorphism prevalence. The manuscript will be reformatted to a standard IMRaD structure to meet clinical audience expectations.

## Current state
Phase 1 is largely complete. Phase 2 (Clinical Validation) and Phase 3 (Manuscript Preparation) are yet to begin.

## What's done/in progress
**What's Done:**
- **Core Model:** "Energy Deficit" bifurcation established (`experiment_energy_deficit_window.py`).
- **Rescue Cliff Validation:** Validated anisotropy cliff at ~2.4 (`experiment_anisotropy_rescue.py`).
- **Spinal Jetlag:** Circadian modulation of curvature demonstrated (`experiment_spinal_jetlag.py`).
- **Toy Models:** Physical intuitions (Thermostatic, Anisotropy, Lenke classes) implemented (`docs/toy_models_plan.md`).

**In Progress:**
- **Clinical Validation (Phase 2):** Explicit alignment of model predictions with human cohort data (Cobb angle distributions, PHV timing).
- **Manuscript Pivot:** Restructuring the existing draft from *Nature* (dense theory) to *Spine* (IMRaD, Clinical Relevance).
- **Model Robustness:** Final sensitivity analysis across parameter sweeps.

## Pending work
| Theme | Task | Effort | Dependencies | Risk Level |
| :--- | :--- | :--- | :--- | :--- |
| **Validation** | **CLIN-01: PHV Timing Mapping** | 2 days | Literature | High |
| **Validation** | **CLIN-02: Curve Type Prediction** | 2 days | Toy Model D | Medium |
| **Validation** | **CLIN-03: Sexual Dimorphism** | 1.5 days | Literature | Medium |
| **Manuscript** | **MS-01: IMRaD Reformatting** | 3 days | CLIN-01/02 | Low |
| **Figures** | **FIG-01: Clinical Overlays** | 2 days | CLIN-01/02 | Medium |

## Experimental results summary
| Experiment | Setup / Script | Result Summary | Reproducibility Status |
| :--- | :--- | :--- | :--- |
| **Energy Deficit** | `experiment_energy_deficit_window.py` | Confirms critical crossover $L_{crit} \approx 0.35$m. | ✅ Validated |
| **Rescue Cliff** | `experiment_anisotropy_rescue.py` | Validates vector constraints via anisotropy sweeps. | ✅ Validated |
| **Spinal Jetlag** | `experiment_spinal_jetlag.py` | Supports microgravity stagnation and circadian $\phi$ mismatch. | ✅ Validated |
| **Cross-Species** | `experiment_cross_species_scaling.py`| Validates Passive vs Active metabolic need. | ✅ Validated |
| **Lenke Classes** | `toy_model_lenke_classes.py` | Predicts specific scoliotic curves based on deficit localization. | ✅ Validated |

## Gaps to publication
While the biomechanical models are robust, they lack direct statistical overlays against human clinical data. We need to generate explicit "Clinical Translation" figures comparing our simulated trajectories against epidemiological cohort means (e.g., progression rates).

## Proposed toy models
1. **The ALSPAC Cohort Validation:** Use published ALSPAC data (low BMI at age 10 predicts AIS at age 15) to validate the "Energy Deficit" prior to the curve onset.
2. **Marfan Syndrome Comparison:** Use the ~63% scoliosis prevalence in Marfan (FBN1 mutations) to validate the anisotropy rescue prediction and optimization failure maps.

## Timeline estimate
**Target Submission Date:** 2026-04-06 (Deadline missed, re-evaluating, projected 2026-09-14)
- **Best Case (2 Weeks):** Cohort data extraction is straightforward; existing simulations cleanly map to PHV timing and Lenke classes.
- **Expected (3 Weeks):** Allows buffer for complex literature extraction to find exact epidemiological datasets matching our simulation parameters.
- **Worst Case (4 Weeks):** If the clinical validation mapping fails and requires significant re-tuning of the PyElastica Cosserat parameters.

## Risks
1. **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. **Mitigation:** Focus on qualitative onset timing and relative scaling.
2. **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging. **Mitigation:** Treat the simulation strictly as an *in silico* experiment in the Methods section.

## Next 7/30 days plan
**Next 7 Days (Sprint - Phase 2 Initiation):**
- Execute **CLIN-01**. Extract Peak Height Velocity (PHV) cohort data from literature.
- Execute **CLIN-02**. Refine `toy_model_lenke_classes.py` to produce a finalized figure.
- Execute **CLIN-03**. Map sexual dimorphism metrics to model parameters.
- Begin structural draft overhaul (IMRaD) for *Spine* (**MS-01**).

**Next 30 Days:**
- Finalize all "Clinical Translation" figures, complete the IMRaD manuscript reformatting, and circulate the updated draft for PI review.
- Address final internal review feedback, run submission checklist, and submit to *Spine*.
