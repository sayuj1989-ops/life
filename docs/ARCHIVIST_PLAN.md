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

## Phase 9: Root Directory Final Polish & Script Cleanup (High Priority)

- [x] **Archive Benchmark Scripts**: Move all temporary `benchmark_*.py` scripts from the root directory to `archive/benchmarks/`.
- [ ] **Clean Up Root Image Files**: Move `js_creature_*.png` files from the root to `archive/images/`.
- [ ] **Organize Remaining Root Scripts**: Move root scripts (`alphafold_pipeline_v2.py`, `check_elastica.py`, `gen_alphafold_figs.py`, `generate_submission.py`, `main.py`, `run_cluster.py`, `test_genai.py`, `create_alphafold_section.js`) to `scripts/` or `archive/`.
- [ ] **Clean Up Root Markdown/CSV Files**: Move `AlphaFold_Analysis_Summary.md`, `Supplementary_Methods_Statistics.md`, `Supplementary_Statistics_Table.csv`, `00_START_HERE.txt`, `test_output_2.txt`, `commit_message.txt`, `plan.md` to appropriate folders or `archive/`.
- [ ] **Re-execute Submission Artifacts Consolidation**: Ensure `submission_manuscript.pdf`, `cover_letter.txt`, and `checklist_compliance.txt` are moved to `submission_package/` as they are still present in the root.
