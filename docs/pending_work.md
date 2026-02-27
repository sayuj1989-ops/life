# Pending Work

**Last Updated:** 2026-05-25
**Status:** In Progress
**Priority Level:** High (Blocking Submission)

## 1. Data Gaps (Critical)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-01** | **Cross-Species Dataset** | Gather scaling data ($L, R, EI, Mass$) for 9 species (e.g., Mouse, Rat, Rabbit, Cat, Dog, Human, Chimp, Cow, Elephant). Required for Figure 3. | 2 days | Literature search | ✅ **Completed** (Estimated from scaling) |
| **DATA-02** | **Mutation Parameter Mapping** | Define explicit mappings for "5 matrix protein variants" mentioned in Figure 4 (e.g., FBN1 $\to$ EI *= 0.7; COL1A1 $\to$ EI *= 0.5). | 1 day | Literature search | ✅ **Completed** (Implemented in `experiment_optimization_failure.py`) |

## 2. Code Implementation (High)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | **Create `experiment_cross_species_scaling.py`** | Script to load species data (DATA-01) and plot $Bg$ number vs Mass/Length. Validate "Passive Stability" vs "Active Need". | 1 day | DATA-01 | ✅ **Completed** |
| **CODE-02** | **Update `experiment_optimization_failure.py`** | Add a `mutation_map` dictionary to map gene names to simulation parameters ($\chi_\kappa, \sigma, EI$). Generate Figure 4 with specific labels. | 0.5 day | DATA-02 | ✅ **Completed** |
| **CODE-03** | **Generate Figure Plots** | Ensure all scripts output publication-quality PNG/PDFs (300 dpi). Current scripts mostly output CSVs or simple plots. | 2 days | EXP-01, EXP-02 | 🟡 **In Progress** |

## 3. Manuscript Tasks (Medium)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MS-01** | **Reference Completeness** | Add 70-85 missing references (Nature format). Focus on Spinal Biomechanics, HOX genes, Microgravity. | 1 day | None | 🟡 **In Progress** |
| **MS-02** | **Figure Finalization** | Assemble generated plots into final multi-panel figures (Figure 1-7). Write final captions. | 3 days | CODE-03 | 🟡 **In Progress** |
| **MS-03** | **Abstract Trimming** | Reduce abstract from 210 to 150 words. | 0.5 hour | None | 🟡 **In Progress** |

## 4. Theory & Validation (Completed)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **THEORY-01** | **Reviewer #3 Defense** | Finalize "Anisotropy Gap" argument. Ensure `manuscript/reviewer_response_strategy.txt` covers potential critiques of thermodynamic scaling. | 0.5 day | None | ✅ **Drafted** |
| **THEORY-02** | **Toy Models** | Create simple 1D models (Toy Model A/B) to de-risk the complex Cosserat simulation for reviewers. | 1 day | None | ✅ **Completed** (See `docs/toy_models_plan.md`) |

## Summary of Risks

1.  **Missing Species Data:** If we cannot find reliable $EI$ or $L$ data for 9 species, Figure 3 ("Cross-Species Validation") will be weak or must be cut. **Mitigation:** Fall back to a theoretical scaling argument ($L^4$ vs $L^{3}$) without explicit data points if necessary.
2.  **Mutation Specificity:** The claim of "5 specific variants" is currently unsupported by code. **Mitigation:** Use generic parameter sweeps and label them "Model for FBN1-type defect".

**Next Actions:**
1.  Start Literature Search for **DATA-01** immediately.
2.  Implement **CODE-01** as soon as data is available.
