# Pending Work

**Last Updated:** 2026-04-10
**Status:** In Progress
**Priority Level:** High (Phase 2: Clinical Validation for Spine Submission)

## 1. Validation (Clinical Validation Mapping)

| ID | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CLIN-01** | **PHV Timing Mapping** | Extract Peak Height Velocity data from literature and graph against model instability window. | 2 days | Literature search | High | $L_{crit}$ crossing successfully overlaid on clinical 10-13 year PHV chart |
| **CLIN-02** | **Curve Type Prediction** | Refine `toy_model_lenke_classes.py` to robustly predict Lenke 1-6 classifications from spatial deficits. | 2 days | Toy Model D | Medium | Script reliably generates outputs matching all 6 typical Lenke profiles |
| **CLIN-03** | **Sexual Dimorphism** | Map model parameters (e.g., stiffness ratios, growth rates) to female/male prevalence epidemiological data. | 1.5 days | Literature search | Low | Text and plot explaining 7:1 ratio based on stiffness parameters |
| **CLIN-04** | **ALSPAC/Marfan Cross-check** | Validate "Energy Deficit" vs low BMI (ALSPAC) and anisotropy vs Marfan syndrome prevalence. | 1 day | None | Low | Validated supplementary text describing correlation |

## 2. Manuscript (Spine IMRaD Reformatting)

| ID | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MS-01** | **IMRaD Restructuring** | Convert theory-dense draft into standard Introduction, Methods, Results, and Discussion sections. | 3 days | CLIN-01, CLIN-02 | Medium | Document converted without losing core argument; math moved to supplement |
| **MS-02** | **"Clinical Relevance" Section** | Draft dedicated section detailing the predictive clinical value for early intervention. | 1 day | MS-01 | Low | Compelling 500-word section aimed at clinicians |
| **MS-03** | **Figure Finalization (Clinical)** | Assemble "Clinical Translation" figures overlaying model predictions on patient cohort data. | 2 days | Output scripts | Medium | Publication-ready multi-panel figure for clinical relevance |
| **MS-04** | **Targeted References** | Update bibliography focusing on *Spine*, *Eur Spine J*, and clinical biomechanics. | 1.5 days | None | Low | 80+ references properly citing clinical biomechanics journals |

## 3. Data Gaps (Completed Phase 1)

| ID | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-01** | **Cross-Species Dataset** | Compile cross-species scaling data for 9 species. | 2 days | None | Low | ✅ **Completed** |
| **DATA-02** | **Mutation Parameter Mapping** | Define explicit mappings for FBN1/matrix protein variants. | 1 day | None | Low | ✅ **Completed** |

## 4. Theory & Models (Completed Phase 1)

| ID | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | **Energy Deficit / Rescue Cliff**| Establish fundamental physics models and parameter sweeps. | - | None | Low | ✅ **Completed** |
| **CODE-02** | **Spinal Jetlag Simulation** | Demonstrate circadian modulation of curvature. | - | None | Low | ✅ **Completed** |
| **THEORY-01** | **Physical Toy Models A-E** | Create simple 1D models to build intuition for PyElastica behavior. | - | None | Low | ✅ **Completed** |

## Summary of Risks

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. **Mitigation:** Focus on qualitative onset timing and relative scaling.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging. **Mitigation:** Treat the simulation strictly as an *in silico* experiment in the Methods section.

**Next Actions:**
1.  Target **CLIN-01**: Execute literature search for high-quality Peak Height Velocity (PHV) cohort charts.
2.  Target **CLIN-02**: Finalize output parameters of the Lenke classification script.
