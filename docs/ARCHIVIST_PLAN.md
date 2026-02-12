# Archivist Plan

This document tracks the daily incremental refactor of the repository towards publication-grade quality.

**Status:**
- [ ] Checked items are complete.
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
