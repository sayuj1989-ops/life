# Pending Work

**Last Updated:** 2026-04-12
**Status:** In Progress
**Priority Level:** High (Phase 2: Clinical Validation for Spine Submission)

## Group: Validation

| Theme | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Validation** | **CLIN-01: PHV Timing Mapping** | Extract Peak Height Velocity data from literature and graph against model instability window. | 2 days | Literature search | Medium | Clear overlay plot of model deficit vs clinical PHV age |
| **Validation** | **CLIN-02: Curve Type Prediction** | Refine `toy_model_lenke_classes.py` to robustly predict Lenke 1-6 classifications from spatial deficits. | 2 days | Toy Model D | High | Robust prediction of Lenke types 1-6 from inputs |
| **Validation** | **CLIN-03: Sexual Dimorphism** | Map model parameters (e.g., stiffness ratios, growth rates) to female/male prevalence epidemiological data. | 1.5 days | Literature search | Low | Text and plot comparing parameters to 7:1 ratio |
| **Validation** | **CLIN-04: ALSPAC/Marfan Cross-check** | Validate "Energy Deficit" vs low BMI (ALSPAC) and anisotropy vs Marfan syndrome prevalence. | 1 day | None | Low | Supplementary text and correlation stats |

## Group: Manuscript

| Theme | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Manuscript** | **MS-01: IMRaD Restructuring** | Convert theory-dense draft into standard Introduction, Methods, Results, and Discussion sections. | 3 days | CLIN-01, CLIN-02 | Medium | Completed Spine-formatted IMRaD manuscript draft |
| **Manuscript** | **MS-02: "Clinical Relevance" Section** | Draft dedicated section detailing the predictive clinical value for early intervention. | 1 day | MS-01 | Low | Compelling 2-3 paragraph Clinical Relevance section |
| **Manuscript** | **MS-04: Targeted References** | Update bibliography focusing on *Spine*, *Eur Spine J*, and clinical biomechanics. | 1.5 days | None | Low | References include key recent Spine journal articles |

## Group: Figures

| Theme | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Figures** | **MS-03: Figure Finalization (Clinical)** | Assemble "Clinical Translation" figures overlaying model predictions on patient cohort data. | 2 days | Output scripts | Medium | Finalized publication-quality overlay figures |

## Group: Code

| Theme | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Code** | **CODE-03: Robustness Analysis** | Ensure model stability across parameter sweeps (Sensitivity Analysis). | 2 days | None | Medium | Robustness sweep metrics showing no exploding gradients |

## Group: Theory (Completed Phase 1)

| Theme | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Theory** | **DATA-01/02, CODE-01/02, THEORY-01** | Prior Phase 1 tasks (Cross-Species Dataset, Mutation Parameter Mapping, Energy Deficit Model, Spinal Jetlag Simulation, Toy Models A-E) | - | - | - | - |
