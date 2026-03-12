# Pending Work

**Last Updated:** 2026-03-12
**Status:** In Progress
**Priority Level:** High (Final Push to Submission: References and Figures)

## 1. Data Gaps (Completed)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DATA-01** | **Cross-Species Dataset** | Compile cross-species scaling data (Mass_kg, Length_m, EI_Nm2) for 10 species. Required for Figure 3. | 2 days | Literature search | ✅ **Completed** |
| **DATA-02** | **Mutation Parameter Mapping** | Define explicit mappings for "5 matrix protein variants" mentioned in Figure 4. | 1 day | Literature search | ✅ **Completed** |

## 2. Code Implementation (Completed)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CODE-01** | **Create `experiment_cross_species_scaling.py`** | Script to load species data and plot $B_g$ number vs Mass/Length. | 1 day | DATA-01 | ✅ **Completed** |
| **CODE-02** | **Update `experiment_optimization_failure.py`** | Generate Figure 4 with specific mutation labels. | 0.5 day | DATA-02 | ✅ **Completed** |
| **CODE-04** | **Create `experiment_anisotropy_rescue.py`** | Validate vector constraints via anisotropy sweeps against critical buckling. | 0.5 day | None | ✅ **Completed** |

## 3. Manuscript & Validation Tasks (High Priority)

| ID | Task | Description | Effort | Dependencies | Risk Level | Acceptance Criteria | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MS-01** | **Reference Completeness** | Add 70-85 missing references (Nature format) directly into `references.bib` covering biomechanics and mechanotransduction. | 2 days | None | High | >80 citations cleanly compiling without LaTeX warnings. | 🔴 **Critical Block** |
| **MS-02** | **Figure Finalization** | Assemble output plots into standardized 300dpi final multi-panel figures (Figure 1-7), applying visual unification scripts. | 3 days | Output scripts | Medium | All 7 panels present in `figures/main/` with exact Nature style. | 🟡 **In Progress** |
| **VAL-01** | **Validate Specialized Experiments** | Verify outputs for `experiment_piezo_cilia_lock.py`, `experiment_squat_stand_cycle.py`, etc., exist and match manuscript text. | 1 day | Python execution | Medium | Exact output file paths tracked in `experiment_registry.md`. | ⚪ **Planned** |
| **MS-04** | **Internal PI Review Package** | Combine updated manuscript text, final figures, and expanded bibliography for final review. | 1 day | MS-01, MS-02 | Low | Single unified PDF exists and is circulated to PI. | ⚪ **Planned** |

## 4. Theory & Validation (Completed)

| ID | Task | Description | Effort | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **THEORY-01** | **Reviewer #3 Defense** | Finalize "Anisotropy Gap" argument for thermodynamics. | 0.5 day | None | ✅ **Drafted** |
| **THEORY-02** | **Toy Models** | Create simple 1D models (Toy A-E) to de-risk Cosserat simulation for reviewers. | 1-4 days | None | ✅ **Completed** |
| **THEORY-03** | **Real Experiments List** | Propose 2-5 real physical/in vivo validations (clinostat, circadian jetlag, KO mice). | 0.5 day | None | ✅ **Drafted** |

## Summary of Risks

1.  **Figure Styling:** Script outputs currently lack uniform stylistic alignment. **Mitigation:** Run or construct small visual unification wrappers to enforce fonts/styles before final panel assembly.
2.  **Missing References:** The Nature manuscript requires a comprehensive reference list, which remains bare. **Mitigation:** Execute intense literature extraction over the next 48-72 hours directly into `references.bib`.
3.  **Missing Special Artifacts:** Some physiological experiment scripts run successfully but do not explicitly emit verified plots. **Mitigation:** Run them individually (`VAL-01`) and catalog outputs directly in `experiment_registry.md`.

**Next Actions:**
1.  Target **MS-01**: Massive expansion of the `.bib` file.
2.  Target **VAL-01**: Validate explicit visual outputs of Piezo Lock, Squat-Stand, Hydraulic experiments.
3.  Target **MS-02**: Verify and format all plot artifacts for Figure 1-7 assembly into `figures/main/`.
