# Pending Work

**Last Updated:** 2026-03-15
**Status:** In Progress
**Priority Level:** High (Final Push to Submission: References and Figures)

## 1. Data Gaps (Completed)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-01** | **Cross-Species Dataset** | Compile cross-species scaling data (Mass_kg, Length_m, EI_Nm2) for 9 species. Required for Figure 3. | 2 days | Literature search | ✅ **Completed** |
| **DATA-02** | **Mutation Parameter Mapping** | Define explicit mappings for "5 matrix protein variants" mentioned in Figure 4. | 1 day | Literature search | ✅ **Completed** |

## 2. Code Implementation (Completed)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | **Create `experiment_cross_species_scaling.py`** | Script to load species data and plot $B_g$ number vs Mass/Length. | 1 day | DATA-01 | ✅ **Completed** |
| **CODE-02** | **Update `experiment_optimization_failure.py`** | Generate Figure 4 with specific mutation labels. | 0.5 day | DATA-02 | ✅ **Completed** |
| **CODE-04** | **Create `experiment_anisotropy_rescue.py`** | Validate vector constraints via anisotropy sweeps against critical buckling. | 0.5 day | None | ✅ **Completed** |

## 3. Pending Work (Prioritized)

| Theme | Task | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Manuscript** | **MS-01: Reference Completeness** | 2 days | None | High | `.bib` contains 80-100 valid, *Nature*-formatted citations supporting all key claims. |
| **Manuscript** | **MS-01b: Abstract Trimming** | 0.5 days | None | High | Trim abstract to strict <150 word limit required by *Nature*. |
| **Figures** | **MS-02: Figure Finalization** | 3 days | Output scripts | High | Final 300dpi Panels 1-7 assembled, uniform styling applied, captions finalized. |
| **Figures** | **MS-02b: Unified Phase Diagram** | 1 day | `experiment_energy_phase_diagram.py` | Med | Generate unified `outputs/figures/energy_phase_diagram.png` for manuscript placement. |
| **Review** | **MS-04: Internal PI Review Package** | 1 day | MS-01, MS-02 | Low | Full package (PDF + Supplement) ready for pre-submission checks. |
| **Supplementary** | **SUPP-01: Extended Data** | 1 day | MS-02 | Low | Extended data tables/figures and methods text assembled for submission package. |
