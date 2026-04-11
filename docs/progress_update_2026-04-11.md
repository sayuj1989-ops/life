# Research Progress Update: Biological Countercurvature

**Date:** 2026-04-11
**Role:** PI / Program Manager / Computational Scientist
**Target Journal:** Spine (IF: 3.30, Q1, H-index: 300)

## Executive summary
The project strategy is officially reframed as "A computational framework predicting adolescent scoliosis onset" for the *Spine* journal. Phase 1 (Computational Framework) is 75% complete, with the core "Energy Deficit" model, Rescue Cliff, and Spinal Jetlag simulations validated. We are pivoting to Phase 2 (Clinical Validation) to explicitly map model outputs (e.g., instability windows) against published epidemiological data such as Peak Height Velocity (PHV) and Lenke classifications. The manuscript must be reformatted to a standard IMRaD structure to meet clinical audience expectations. Overall completion is roughly 23.1%.

## Current state
**What's done/in progress:**
- [x] **Core Model:** "Energy Deficit" bifurcation established (`experiment_energy_deficit_window.py`).
- [x] **Rescue Cliff Validation:** Validated anisotropy cliff at ~2.4 (`experiment_anisotropy_rescue.py`).
- [x] **Spinal Jetlag:** Circadian modulation of curvature demonstrated (`experiment_spinal_jetlag.py`).
- [x] **Toy Models:** Physical intuitions (Thermostatic, Anisotropy, Lenke classes) implemented (`docs/toy_models_plan.md`).
- [ ] **Phase 1 Robustness:** Final robustness checks and sensitivity analysis across parameter sweeps.
- [ ] **Clinical Validation (Phase 2):** Cohort data extraction and alignment of model predictions with human data (PHV timing, curve types).

## Pending work
| Theme | Task | Effort | Dependencies | Risk Level |
| :--- | :--- | :--- | :--- | :--- |
| **Validation** | CLIN-01: PHV Timing Mapping | 2 days | Literature | High |
| **Validation** | CLIN-02: Curve Type Prediction | 2 days | Toy Model D | Medium |
| **Validation** | CLIN-03: Sexual Dimorphism | 1.5 days | Literature | Medium |
| **Manuscript** | MS-01: IMRaD Reformatting | 3 days | CLIN-01/02 | Low |
| **Figures** | FIG-01: Clinical Overlays | 2 days | CLIN-01/02 | Medium |

## Experimental results summary
| Experiment | Setup / Script | Result Summary | Reproducibility |
| :--- | :--- | :--- | :--- |
| **Energy Deficit** | `experiment_energy_deficit_window.py` | Confirms crossover $L_{crit} pprox 0.35$m ($P \sim L^2$ vs $S \sim L^{0.5}$). | ✅ Validated |
| **Rescue Cliff** | `experiment_anisotropy_rescue.py` | Validates vector constraints via anisotropy sweeps against critical buckling. | ✅ Validated |
| **Spinal Jetlag** | `experiment_spinal_jetlag.py` | Supports microgravity stagnation and circadian mismatch. | ✅ Validated |
| **Lenke Classes** | `toy_model_lenke_classes.py` | Predicts specific scoliotic curves based on deficit localization. | ✅ Validated |

## Gaps to publication
The biomechanical models lack direct statistical overlays against human clinical data. We need explicit "Clinical Translation" figures comparing simulated trajectories against epidemiological cohort means (e.g., PHV timing).

## Proposed toy models
The core mechanistic toy models (A-E) are completed. Future validations center on real-world clinical proxies:
1. **ALSPAC Cohort Validation:** Low BMI at age 10 predicting AIS at age 15.
2. **Marfan Syndrome Comparison:** ~63% scoliosis prevalence in Marfan mapped to FBN1 anisotropy metrics.

## Timeline estimate
**Target Submission Date:** 2026-04-06 (Currently Overdue)
**Projected Completion based on Velocity:** 2026-09-14
- **Revised Best Case:** 3 Weeks if cohort data extraction and mapping cleanly align.
- **Expected:** 4-5 Weeks to allow thorough literature extraction matching simulation parameters.
- **Critical Path:** Cohort Data Extraction -> Clinical Validation Experiments -> IMRaD Manuscript Reformatting -> Final Submission.

## Risks
1. **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. *Mitigation:* Focus on qualitative onset timing and relative scaling.
2. **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow. *Mitigation:* Treat the simulation strictly as an *in silico* experiment in the Methods section.

## Next 7/30 days plan
**Next 7 Days:**
- **Days 1-2:** Complete Phase 1 Robustness sweep.
- **Days 3-4:** Execute CLIN-01. Extract Peak Height Velocity (PHV) cohort data from literature and overlay with instability window.
- **Days 5-6:** Execute CLIN-02. Finalize figure mapping spatial deficits to Lenke Classifications.
- **Day 7:** Execute CLIN-03. Map sexual dimorphism metrics to parameters.

**Next 30 Days:**
- **Weeks 2-3:** Overhaul manuscript structural draft (IMRaD) for *Spine* (MS-01). Finalize "Clinical Translation" figures.
- **Week 4:** Address internal review feedback, run pre-submission checks, and submit.
