# Pending Work

**Last Updated:** 2026-03-14
**Status:** In Progress
**Priority Level:** High (Final Push to Submission: Clinical Validation and Manuscript Prep)
**Target:** *Spine* Submission

## 1. Clinical Validation (High Priority)

| ID | Task | Description | Effort | Dependencies | Status | Risk Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CLIN-01** | **Extract Cohort Data** | Extract clinical cohort data (Cobb angle distributions, progression rates) from published literature. | 3 days | Literature search | 🔴 **Pending** | High |
| **CLIN-02** | **Validate PHV Timing** | Compare model "Instability Window" with clinical Peak Height Velocity (PHV) timing data. | 2 days | CLIN-01 | 🔴 **Pending** | Medium |
| **CLIN-03** | **Sexual Dimorphism** | Validate model predictions for female vs. male prevalence against epidemiological data. | 1 day | CLIN-01 | 🔴 **Pending** | Medium |
| **CLIN-04** | **Curve Types** | Verify if model can reproduce common curve types (e.g., Lenke classification patterns) based on initial conditions. | 2 days | Model parameters | 🔴 **Pending** | Medium |

## 2. Manuscript Preparation (Medium Priority)

| ID | Task | Description | Effort | Dependencies | Status | Risk Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MS-01** | **Reformat Manuscript** | Adapt `nature_manuscript.tex` to *Spine* format (IMRaD structure). | 2 days | None | 🔴 **Pending** | Low |
| **MS-02** | **Draft Abstract** | Draft Structured Abstract (Study Design, Objective, Summary of Background Data, Methods, Results, Conclusions). | 0.5 day | None | 🔴 **Pending** | Low |
| **MS-03** | **Clinical Relevance** | Write "Clinical Relevance" section highlighting the predictive value for early intervention. | 1 day | None | 🔴 **Pending** | Medium |
| **MS-04** | **Clinical Figures** | Generate "Clinical Translation" figures (Model vs. Patient Data overlays). | 3 days | CLIN-01 | 🔴 **Pending** | Medium |
| **MS-05** | **Update References** | Update bibliography to include relevant *Spine* and *Eur Spine J* citations. | 2 days | Literature search | 🔴 **Pending** | Low |

## 3. Data & Code Implementation (Completed)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-01** | **Cross-Species Dataset** | Compile cross-species scaling data for 10 species. | 2 days | Literature search | ✅ **Completed** |
| **CODE-01** | **Cross-Species Scaling** | Script to load species data and plot $B_g$ number vs Mass/Length. | 1 day | DATA-01 | ✅ **Completed** |
| **CODE-02** | **Optimization Failure** | Generate Figure 4 with specific mutation labels. | 0.5 day | None | ✅ **Completed** |
| **CODE-04** | **Anisotropy Rescue** | Validate vector constraints via anisotropy sweeps. | 0.5 day | None | ✅ **Completed** |

## 4. Theory & Validation (Completed)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **THEORY-02** | **Toy Models** | Create simple 1D models (Toy A-E) to de-risk Cosserat simulation for reviewers. | 1-4 days | None | ✅ **Completed** |

## Summary of Risks

1.  **Clinical Data Fit:** Model predictions might not perfectly align with messy clinical cohort data. **Mitigation:** Focus on qualitative trends rather than perfect quantitative fits.
2.  **Manuscript Tone:** *Spine* requires a highly clinical focus, which our current theoretical draft lacks. **Mitigation:** Dedicate the "Clinical Relevance" section to explicitly defining how this framework aids early prediction and intervention.
