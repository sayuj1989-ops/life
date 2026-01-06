# Archivist Plan

This document tracks the daily incremental refactor of the repository towards publication-grade quality.

**Status:**
- [ ] Checked items are complete.
- [ ] Unchecked items are pending.

**Goal:** Clean, organized, reproducible, and well-documented research code.

## Phase 1: Repository Cleanup & Organization (High Priority)

- [ ] **Consolidate Legacy Folders**: Move `biology_research`, `life`, `life-1`, `life-paper`, `research_repo` into `archive/`. These appear to be duplicate or older versions of the project.
- [ ] **Fix Typos**: Rename any clearly typoed directories (e.g., `biology_research`) if they are kept or archived.
- [ ] **Standardize Source Layout**:
    - [ ] Decide on the canonical source location (likely `src/`).
    - [ ] Move top-level packages (`alphafold_analysis`, `countercurvature`) into `src/` or `research/` as appropriate.
    - [ ] Clarify `ragflow`'s role (vendor code vs. project code) and move/document accordingly.
- [ ] **Root Directory Cleanup**:
    - [ ] Move root-level python scripts (`02_validate_solvers.py`, `benchmark_analysis.py`, etc.) to `scripts/` or `tests/`.
    - [ ] Consolidate configuration files where possible.
- [ ] **Data Organization**: Ensure `data/` has a clear structure and `README`.
- [ ] **Archive Redundant Content**: Identify and move unused code to `archive/`.

## Phase 2: Documentation (Medium Priority)

- [ ] **Create Repo-Level README**: Rewrite root `README.md` to point to correct components (`src`, `research`, `docs`).
- [ ] **Documentation Index**: Ensure `docs/index.md` is up-to-date with new paths.
- [ ] **Style Guide**: Create `docs/CONTRIBUTING.md` or `docs/STYLE_GUIDE.md`.
- [ ] **Audit Docstrings**: Ensure public modules have docstrings.

## Phase 3: Code Quality & Testing (Medium Priority)

- [ ] **Unify Requirements**: Audit `requirements.txt` vs `pyproject.toml` vs `envs/`.
- [ ] **CI/CD Fixes**: Update GitHub workflows to reflect path changes.
- [ ] **Linter Setup**: Ensure `flake8` or `ruff` config is valid and running.
- [ ] **Test Discovery**: Ensure `pytest` can find all tests in the new structure.

## Phase 4: Final Polish (Low Priority)

- [ ] **Version Bump**: Establish versioning strategy.
- [ ] **Citation**: Ensure `CITATION.cff` is accurate.
- [ ] **License**: Verify `LICENSE` applicability to all components.
