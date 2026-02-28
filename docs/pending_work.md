# Pending Work

**Last Updated:** 2026-02-28
**Status:** In Progress

## 1. Manuscript & Figures (High Priority)

| Theme | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Figures** | **Figure 3: Cross-Species Polish** | Update `experiment_cross_species_scaling.py` plotting to be publication quality (300dpi, clean labels, colorblind friendly). | 1 day | None | Low | High-res PNG/PDF generated in `figures/main/`. |
| **Figures** | **Figure 4: Digital Twin Polish** | Update `experiment_optimization_failure.py` plotting to clearly show gene mappings. | 1 day | None | Low | High-res PNG/PDF generated in `figures/main/`. |
| **Figures** | **Assemble Figure Panels** | Combine sub-plots into cohesive multi-panel figures as required by the manuscript text. | 2 days | FIG-01, FIG-02 | Medium | All figures called out in `.tex` exist and look professional. |
| **Manuscript** | **Resolve LaTeX TODOs** | Scan `manuscript/` for `% TODO:` comments and replace with actual numbers/claims from `outputs/`. | 2 days | Core Simulations | Medium | `grep -r "TODO" manuscript/` returns zero relevant hits. |
| **Manuscript** | **Bibliography Review** | Clean `manuscript/references.bib` of self-citations and future-dated entries. | 0.5 days | None | Low | Bibliography compiles cleanly and follows strict rules. |
| **Validation** | **Result Consistency Check** | Ensure values in `data/clinical_cohort_targets.csv` match what is reported in the text. | 1 day | None | Medium | No contradiction between data files and text. |
| **Code** | **Consolidate Output Paths** | Ensure all scripts dump outputs to clearly defined subdirectories in `outputs/` instead of scattering them. | 1 day | None | Low | Clean execution of `scripts/experiments/*.py`. |
