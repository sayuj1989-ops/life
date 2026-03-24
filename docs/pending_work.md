# Pending Work

**Last Updated:** 2026-03-24
**Status:** In Progress
**Priority Level:** High (Phase 2: Clinical Validation for Spine Submission)

## 1. Clinical Validation Mapping (Current Sprint)

| ID | Task | Description | Effort | Dependencies | Risk Level | Status | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CLIN-01** | **PHV Timing Mapping** | Extract Peak Height Velocity data from literature and graph against model instability window. | 2 days | Literature search | High | 🔴 **Pending** | Code output matches literature timing (10-14 yrs). |
| **CLIN-02** | **Curve Type Prediction** | Refine `toy_model_lenke_classes.py` to robustly predict Lenke 1-6 classifications from spatial deficits. | 2 days | Toy Model D | Medium | 🟡 **In Progress** | Generates 6 distinct spatial patterns. |
| **CLIN-03** | **Sexual Dimorphism** | Map model parameters (e.g., stiffness ratios, growth rates) to female/male prevalence epidemiological data. | 1.5 days | Literature search | Medium | ⚪ **Planned** | Validates 7:1 ratio for parameter variances. |
| **CLIN-04** | **ALSPAC/Marfan Cross-check** | Validate "Energy Deficit" vs low BMI (ALSPAC) and anisotropy vs Marfan syndrome prevalence. | 1 day | None | Low | ⚪ **Planned** | Correlates BMI and anisotropy with prevalence. |

## 2. Manuscript Reformatting (Spine IMRaD)

| ID | Task | Description | Effort | Dependencies | Risk Level | Status | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MS-01** | **IMRaD Restructuring** | Convert theory-dense draft into standard Introduction, Methods, Results, and Discussion sections. | 3 days | CLIN-01, CLIN-02 | Medium | ⚪ **Planned** | Text is reformatted without losing core claims. |
| **MS-02** | **"Clinical Relevance" Section** | Draft dedicated section detailing the predictive clinical value for early intervention. | 1 day | MS-01 | Low | ⚪ **Planned** | Minimum 500 words addressing clinical audience. |
| **MS-03** | **Figure Finalization (Clinical)** | Assemble "Clinical Translation" figures overlaying model predictions on patient cohort data. | 2 days | Output scripts | Medium | ⚪ **Planned** | All figures high-res, with overlays. |
| **MS-04** | **Targeted References** | Update bibliography focusing on *Spine*, *Eur Spine J*, and clinical biomechanics. | 1.5 days | None | Low | ⚪ **Planned** | Addition of 10+ relevant clinical papers. |

## 3. Data Gaps (Completed Phase 1)

| ID | Task | Description | Effort | Dependencies | Risk Level | Status | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-01** | **Cross-Species Dataset** | Compile cross-species scaling data for 9 species. | 2 days | None | Low | ✅ **Completed** | Full parameters for 9 species gathered. |
| **DATA-02** | **Mutation Parameter Mapping** | Define explicit mappings for FBN1/matrix protein variants. | 1 day | None | Low | ✅ **Completed** | Mappings applied to existing models. |

## 4. Theory & Models (Completed Phase 1)

| ID | Task | Description | Effort | Dependencies | Risk Level | Status | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | **Energy Deficit / Rescue Cliff**| Establish fundamental physics models and parameter sweeps. | - | None | Low | ✅ **Completed** | Scripts run without error. |
| **CODE-02** | **Spinal Jetlag Simulation** | Demonstrate circadian modulation of curvature. | - | None | Low | ✅ **Completed** | Script outputs relevant graphs. |
| **THEORY-01** | **Physical Toy Models A-E** | Create simple 1D models to build intuition for PyElastica behavior. | - | None | Low | ✅ **Completed** | Validates baseline assumptions. |

## Summary of Risks

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. **Mitigation:** Focus on qualitative onset timing and relative scaling.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging. **Mitigation:** Treat the simulation strictly as an *in silico* experiment in the Methods section.

**Next Actions:**
1.  Target **CLIN-01**: Execute literature search for high-quality Peak Height Velocity (PHV) cohort charts.
2.  Target **CLIN-02**: Finalize output parameters of the Lenke classification script.