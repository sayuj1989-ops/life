# Archivist Plan

This document tracks the daily incremental refactor of the repository towards publication-grade quality.

**Status:**
- [x] Checked items are complete.
- [ ] Unchecked items are pending.

**Goal:** Clean, organized, reproducible, and well-documented research code.

## Phase 1: Repository Cleanup & Organization (High Priority)

- [x] **Consolidate Legacy Folders**: Move `biology_research`, `life`, `life-1`, `life-paper`, `research_repo` into `archive/`. These appear to be duplicate or older versions of the project.
- [x] **Fix Typos**: Rename any clearly typoed directories (e.g., `biology_research`) if they are kept or archived.
- [x] **Standardize Source Layout**:
    - [x] Decide on the canonical source location (likely `src/`).
    - [x] Move top-level packages (`alphafold_analysis`, `countercurvature`) into `src/` or `research/` as appropriate.
        - *Decision*: Moved to `archive/` as they were legacy versions. Active code is in `src/` and `research/alphafold_countercurvature`.
    - [x] Clarify `ragflow`'s role (vendor code vs. project code) and move/document accordingly.
        - *Decision*: Moved to `archive/ragflow/` as it is a vendored tool not currently used in the active pipeline. Added `README_ARCHIVIST.md` to explain its status.
- [x] **Root Directory Cleanup**:
    - [x] Move root-level python scripts (`02_validate_solvers.py`, `benchmark_analysis.py`, etc.) to `scripts/` or `tests/`.
    - [x] Consolidate configuration files where possible.
- [x] **Data Organization**: Ensure `data/` has a clear structure and `README`.
- [x] Archive Redundant Content: Identify and move unused code to `archive/`.

## Phase 2: Documentation (Medium Priority)

- [x] **Create Repo-Level README**: Rewrite root `README.md` to point to correct components (`src`, `research`, `docs`).
- [x] **Documentation Index**: Ensure `docs/index.md` is up-to-date with new paths.
- [x] **Style Guide**: Create `docs/CONTRIBUTING.md` or `docs/STYLE_GUIDE.md`.
- [x] **Audit Docstrings**: Ensure public modules have docstrings.

## Phase 3: Code Quality & Testing (Medium Priority)

- [x] **Unify Requirements**: Audit `requirements.txt` vs `pyproject.toml` vs `envs/`.
- [x] **CI/CD Fixes**: Update GitHub workflows to reflect path changes.
- [x] **Linter Setup**: Ensure `flake8` or `ruff` config is valid and running.
- [x] **Test Discovery**: Ensure `pytest` can find all tests in the new structure.

## Phase 4: Final Polish (Low Priority)

- [x] **Version Bump**: Establish versioning strategy.
- [x] **Citation**: Ensure `CITATION.cff` is accurate.
- [x] **License**: Verify `LICENSE` applicability to all components.

## Phase 5: Scripts & Experiments Organization (Medium Priority)

- [x] **Organize `scripts/`**: Group scripts into logical subdirectories (`experiments/`, `pipeline/`, `data_management/`) to reduce clutter.
- [x] **Fix Script Imports**: Ensure moved scripts can still import `src` correctly (sys.path or package install).
- [x] **Standardize Experiment Interface**: Ensure all experiment scripts have a standard CLI or main function. (Created `experiment_utils.py` and refactored key scripts).

## Phase 6: Reproducibility & QA (High Priority)

- [x] **Add Reproducibility Guide**: Create `docs/reproducibility.md` explaining how to run the full pipeline.
- [x] **Verify Example Scripts**: Ensure examples in `README.md` and `docs/` are runnable.
- [x] **Automated Pipeline Test**: Create a test or script that runs a minimal version of the full pipeline (AlphaFold -> CounterCurvature -> Analysis).

## Phase 7: Manuscript & Submission Cleanup (High Priority)

- [x] **Consolidate Submission Directories**:
    - [x] Decide between `submission/` and `submission_package/` (likely keep `submission_package` and archive `submission`).
    - [x] Ensure all submission artifacts (cover letter, checklist) are in one place.
- [x] **Clean Root of Drafts**:
    - [x] Move `.docx` files (`IEC_*.docx`, `NATURE_*.docx`) to `manuscript/drafts/`.
    - [x] Move template files (`*_Template.docx`) to `manuscript/templates/`.
- [x] **Organize Manuscript Scripts**:
    - [x] Move `create_abstract.js`, `create_cover_letter.js`, `create_nature_manuscript.js` to `scripts/manuscript/`.
- [x] **Organize Prompts**:
    - [x] Move `AI_*.md` and `*_PROMPT.md` to `docs/prompts/` or `notes/prompts/`.
- [x] **Submission Checklist**:
    - [x] Consolidate `SUBMISSION_MASTER_CHECKLIST.md` and `SUBMISSION_PACKAGE_SUMMARY.txt` into the submission folder.

## Phase 8: Root Directory Final Cleanup & Consolidation (High Priority)

- [x] **Consolidate Submission Artifacts**: Move `submission_manuscript.pdf`, `cover_letter.txt`, and `checklist_compliance.txt` from the root to `submission_package/`.
- [x] **Archive Legacy Submission**: Move `submission/` to `archive/submission/`.
- [x] **Clean Root Drafts**: Move root `.docx` files to `manuscript/drafts/`.
- [x] **Clean Root Markdown/Text Files**: Move manuscript-related markdown and text files (e.g. `MANUSCRIPT_CONTENTS_AND_NEXT_STEPS.md`, `NATURE_MANUSCRIPT_FORMATTING_GUIDE.md`) to `docs/manuscript/`.

## Phase 9: Additional Root Cleanup (High Priority)

- [x] **Organize Root Images**: Move root image files (e.g., `js_creature_*.png`) to an appropriate directory like `figures/` or `archive/`.
- [x] **Clean Root Markdown Files**: Move root markdown/text files (e.g., `AlphaFold_Analysis_Summary.md`, `Supplementary_Methods_Statistics.md`, `00_START_HERE.txt`) to `docs/` or `manuscript/`.
- [x] **Move AlphaFold Scripts**: Move `alphafold_pipeline_v2.py`, `gen_alphafold_figs.py`, and related scripts to `scripts/pipeline/` or `scripts/alphafold/`.
- [x] **Move Benchmark Scripts**: Move benchmark scripts (`benchmark_pae.py`, `benchmark_pae2.py`, `benchmark_pae_domain.py`, `benchmark_rg.py`, `benchmark_var.py`) to `scripts/benchmarks/`.
- [x] **Clean Root Miscellany**: Move loose scripts like `create_alphafold_section.js`, `generate_submission.py`, `main.py`, `test_genai.py`, `run_cluster.py` to `scripts/` or `archive/` depending on relevance. Move artifacts like `plan.md` and `test_output_2.txt` to `archive/`.

## Phase 10: Additional Root Cleanup (Part 2)

- [x] **Clean Root Text Files**: Move root text files (e.g., `jules_lenke_6_types.txt`, `jules_lenke_multi_segment.txt`, `jules_mechanism_derivative_gain_trap.txt`, `jules_mechanism_vim_cascade.txt`, `jules_polygenic_stacking_lenke.txt`, `jules_visual_abstract_biological_countercurvature.txt`, `jules_visual_abstract_metabolic_buckling.txt`) to `notes/` or `archive/`.
- [ ] **Clean Root Scripts**: Move root scripts like `check_elastica.py` to `scripts/` or `tests/`.
- [ ] **Clean Plan and Messages**: Move `plan_draft.md` and `commit_message.txt` to `archive/`.
- [ ] **Clean Root Markdown**: Move `research_schedule_gravity_optimization.md` to `docs/` or `notes/`.
- [ ] **Consolidate Figures**: Investigate `figures/`, `figures_alphafold/`, `figures_v2/`, `alphafold_figures/` and consolidate into a single `figures/` directory or move to `archive/`.
