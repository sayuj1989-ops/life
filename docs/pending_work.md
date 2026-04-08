# Pending Work

**Last Updated:** 2026-04-08
**Status:** In Progress
**Priority Level:** High (Phase 2: Clinical Validation for Spine Submission)

## 1. Clinical Validation Mapping (Current Sprint)

| ID | Task | Description | Effort | Dependencies | Risk Level | Status | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CLIN-01** | **PHV Timing Mapping** | Extract Peak Height Velocity data from literature and graph against model instability window. | 2 days | Literature search | Medium | 🔴 **Pending** | Cohort data digitized and plotted alongside theoretical $L_{crit}$ boundaries. |
| **CLIN-02** | **Curve Type Prediction** | Refine `toy_model_lenke_classes.py` to robustly predict Lenke 1-6 classifications from spatial deficits. | 2 days | Toy Model D | Low | 🟡 **In Progress** | Script accurately generates expected spatial modes corresponding to Types 1-6. |
| **CLIN-03** | **Sexual Dimorphism** | Map model parameters (e.g., stiffness ratios, growth rates) to female/male prevalence epidemiological data. | 1.5 days | Literature search | Low | ⚪ **Planned** | Parameter justification added to manuscript mapping 7:1 clinical ratio. |
| **CLIN-04** | **ALSPAC/Marfan Cross-check** | Validate "Energy Deficit" vs low BMI (ALSPAC) and anisotropy vs Marfan syndrome prevalence. | 1 day | None | Low | ⚪ **Planned** | Cross-check complete and summarized in clinical validation section. |

## 2. Manuscript Reformatting (Spine IMRaD)

| ID | Task | Description | Effort | Dependencies | Risk Level | Status | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MS-01** | **IMRaD Restructuring** | Convert theory-dense draft into standard Introduction, Methods, Results, and Discussion sections. | 3 days | CLIN-01, CLIN-02 | Medium | ⚪ **Planned** | Document fully conforms to structural requirements; heavy theory moved to supplement. |
| **MS-02** | **"Clinical Relevance" Section** | Draft dedicated section detailing the predictive clinical value for early intervention. | 1 day | MS-01 | Low | ⚪ **Planned** | Section complete and reviewed by clinical co-authors. |
| **MS-03** | **Figure Finalization (Clinical)** | Assemble "Clinical Translation" figures overlaying model predictions on patient cohort data. | 2 days | Output scripts | Medium | ⚪ **Planned** | High-resolution multi-panel figures generated with unified styling. |
| **MS-04** | **Targeted References** | Update bibliography focusing on *Spine*, *Eur Spine J*, and clinical biomechanics. | 1.5 days | None | Low | ⚪ **Planned** | Citations updated to focus heavily on clinical precedents and observations. |

## Summary of Risks

1.  **Clinical Data Mismatch:** Abstract physics parameters ($\chi_\kappa$, Anisotropy) may not map linearly to clinical metrics like Cobb angle progression. **Mitigation:** Focus on qualitative onset timing and relative scaling.
2.  **IMRaD Reformatting Burden:** Stripping dense mathematical theory into supplementary sections while maintaining narrative flow is challenging. **Mitigation:** Treat the simulation strictly as an *in silico* experiment in the Methods section.

**Next Actions:**
1.  Target **CLIN-01**: Execute literature search for high-quality Peak Height Velocity (PHV) cohort charts.
2.  Target **CLIN-02**: Finalize output parameters of the Lenke classification script.
