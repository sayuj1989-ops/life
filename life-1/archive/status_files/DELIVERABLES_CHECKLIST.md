# Deliverables Checklist (Prototype Status)

**Project:** Spinal Modes – IEC Model  
**Date:** October 24, 2025  
**Status:** ⚠️ In Progress — Foundation Built, Validation Pending

---

## 1. Manuscript
- **Draft present:** `docs/manuscript/SpinalCountercurvature_IEC.md` (~433 lines).
- **Outstanding:** Add affiliations/contact info, integrate real figures/data once generated, audit references.

## 2. Core Code
- **IEC module:** `src/spinalmodes/iec.py` implements IEC couplings and utilities (toy solver flagged for replacement).
- **CLI:** `src/spinalmodes/iec_cli.py` exposes five commands ready for end-to-end testing.
- **Figure script:** `src/spinalmodes/fig_iec_discriminators.py` prepared to export PNG/CSV/JSON after solver validation.

## 3. Tests & Quality
- **Unit tests:** `tests/test_iec.py` (15+ cases) cover core logic; rely on simplified solver.
- **CI:** No workflows in `.github/workflows/`; manual `pytest`/`make` runs required.
- **Validation tool:** `tools/validate_figures.py` available but not yet exercised.

## 4. Outputs
- **Current state:** `outputs/` contains only `.gitkeep` placeholders. No CSV/PNG artifacts committed yet.
- **Next step:** Execute CLI commands to populate outputs and verify with validation script.

## 5. Documentation & Communication
- **README:** Updated with prototype disclaimer and pointer to `ACTUAL_STATUS.md`.
- **Supporting docs:** `docs/cli.md`, `docs/figures.md`, `PROJECT_SUMMARY.md`, `VERIFICATION_LOG.md` refreshed for honesty; continue syncing as development progresses.

---

## Immediate Priorities
1. Upgrade or replace `solve_beam_static` and confirm acceptance tests against the new solver.
2. Produce at least one complete run of each CLI command and commit the resulting artifacts.
3. Stand up minimal CI (lint + pytest) to guard against regressions.
4. Finalize manuscript metadata and align claims with generated evidence.
