# Pending Work

**Last Updated:** 2026-04-11
**Status:** In Progress
**Priority Level:** High (Phase 2: Clinical Validation for Spine Submission)

## 1. Clinical Validation Mapping (Current Sprint)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CLIN-01** | **PHV Timing Mapping** | Extract Peak Height Velocity data from literature and graph against model instability window. | 2 days | Literature search | 🔴 **Pending** |
| **CLIN-02** | **Curve Type Prediction** | Refine `toy_model_lenke_classes.py` to robustly predict Lenke 1-6 classifications from spatial deficits. | 2 days | Toy Model D | 🟡 **In Progress** |
| **CLIN-03** | **Sexual Dimorphism** | Map model parameters (e.g., stiffness ratios, growth rates) to female/male prevalence epidemiological data. | 1.5 days | Literature search | ⚪ **Planned** |
| **CLIN-04** | **ALSPAC/Marfan Cross-check** | Validate "Energy Deficit" vs low BMI (ALSPAC) and anisotropy vs Marfan syndrome prevalence. | 1 day | None | ⚪ **Planned** |

## 2. Manuscript Reformatting (Spine IMRaD)

| ID | Task | Description | Effort | Dependencies | Risk Level | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MS-01** | **IMRaD Restructuring** | Convert theory-dense draft into standard Introduction, Methods, Results, and Discussion sections. | 3 days | CLIN-01, CLIN-02 | Medium | ⚪ **Planned** |
| **MS-02** | **"Clinical Relevance" Section** | Draft dedicated section detailing the predictive clinical value for early intervention. | 1 day | MS-01 | Low | ⚪ **Planned** |
| **MS-03** | **Figure Finalization (Clinical)** | Assemble "Clinical Translation" figures overlaying model predictions on patient cohort data. | 2 days | Output scripts | Medium | ⚪ **Planned** |
| **MS-04** | **Targeted References** | Update bibliography focusing on *Spine*, *Eur Spine J*, and clinical biomechanics. | 1.5 days | None | Low | ⚪ **Planned** |

## 3. Data Gaps (Completed Phase 1)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-01** | **Cross-Species Dataset** | Compile cross-species scaling data for 9 species. | 2 days | None | ✅ **Completed** |
| **DATA-02** | **Mutation Parameter Mapping** | Define explicit mappings for FBN1/matrix protein variants. | 1 day | None | ✅ **Completed** |

## 4. Theory & Models (Completed Phase 1)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | **Energy Deficit / Rescue Cliff**| Establish fundamental physics models and parameter sweeps. | - | None | ✅ **Completed** |
| **CODE-02** | **Spinal Jetlag Simulation** | Demonstrate circadian modulation of curvature. | - | None | ✅ **Completed** |
| **THEORY-01** | **Physical Toy Models A-E** | Create simple 1D models to build intuition for PyElastica behavior. | - | None | ✅ **Completed** |

## Summary of Risks

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. **Mitigation:** Focus on qualitative onset timing and relative scaling.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging. **Mitigation:** Treat the simulation strictly as an *in silico* experiment in the Methods section.

**Next Actions:**
1.  Target **CLIN-01**: Execute literature search for high-quality Peak Height Velocity (PHV) cohort charts.
2.  Target **CLIN-02**: Finalize output parameters of the Lenke classification script.
