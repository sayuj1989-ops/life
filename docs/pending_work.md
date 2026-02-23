# Pending Work

**Last Updated:** 2026-03-05
**Status:** In Progress
**Priority Level:** High (Blocking Submission)

## 1. Data Gaps (Critical)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-01** | **Cross-Species Dataset** | Gather scaling data ($L, R, EI, Mass$) for 9 species (Mouse to Elephant). | 2 days | None | ✅ **Completed** (See `data/species_parameters.csv`) |
| **DATA-02** | **Mutation Parameter Mapping** | Define explicit mappings for "5 matrix protein variants" mentioned in Figure 4 (e.g., FBN1 $\to$ EI *= 0.7; COL1A1 $\to$ EI *= 0.5). | 1 day | Literature search | 🟠 **Pending** |

## 2. Code Implementation (High)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | **Create `experiment_cross_species_scaling.py`** | Script to load species data (DATA-01) and plot $Bg$ number vs Mass/Length. | 1 day | DATA-01 | ✅ **Completed** (See `scripts/analysis/cross_species_scaling.py`) |
| **CODE-02** | **Update `experiment_optimization_failure.py`** | Add a `mutation_map` dictionary to map gene names to simulation parameters ($\chi_\kappa, \sigma, EI$). Generate Figure 4 with specific labels. | 0.5 day | DATA-02 | 🟠 **Pending** |
| **CODE-03** | **Generate Figure Plots** | Ensure all scripts output publication-quality PNG/PDFs (300 dpi). | 2 days | EXP-01, EXP-02 | 🟡 **In Progress** |

## 3. Manuscript Tasks (Medium)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MS-01** | **Reference Completeness** | Add 70-85 missing references (Nature format). Focus on Spinal Biomechanics, HOX genes, Microgravity. | 1 day | None | 🟡 **In Progress** |
| **MS-02** | **Figure Finalization** | Assemble generated plots into final multi-panel figures (Figure 1-7). Write final captions. | 3 days | CODE-03 | 🟡 **In Progress** |
| **MS-03** | **Abstract Trimming** | Reduce abstract from 210 to 150 words. | 0.5 hour | None | 🟡 **In Progress** |

## 4. Theory & Validation (Low)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **THEORY-01** | **Reviewer #3 Defense** | Finalize "Anisotropy Gap" argument. Ensure `manuscript/reviewer_response_strategy.txt` covers potential critiques of thermodynamic scaling. | 0.5 day | None | ✅ **Drafted** |
| **THEORY-02** | **Toy Models** | Create simple 1D models (Toy Model A/B) to de-risk the complex Cosserat simulation for reviewers. | 1 day | None | ✅ **Completed** (See `docs/toy_models_plan.md`) |

## Summary of Risks

1.  **Mutation Specificity:** The claim of "5 specific variants" is currently unsupported by code. **Mitigation:** Use generic parameter sweeps and label them "Model for FBN1-type defect".
2.  **Figure Quality:** Need to ensure all figures are generated at high resolution (300 dpi).

**Next Actions:**
1.  Implement **CODE-02** (Mutation Mapping) immediately.
2.  Finalize **MS-02** (Figures).
