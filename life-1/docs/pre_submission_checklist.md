# Pre-Submission Sanity Checklist

## Project-Specific Verification

This checklist ensures code, manuscript, and documentation are aligned before submission.

---

## 1. Versioning

- [ ] Tag `v0.1.0` in GitHub and make sure `CITATION.cff` and manuscript say the same version.
- [ ] Confirm the repo URL in the manuscript is final (public or "to be public on acceptance" if needed).
- [ ] Check that `src/spinalmodes/__init__.py` has `__version__ = "0.1.0"`.
- [ ] Verify `pyproject.toml` version matches (if using Poetry).

**Files to check:**
- `manuscript/main_countercurvature.tex` (Code Availability section)
- `CITATION.cff` (version field)
- `src/spinalmodes/__init__.py` (__version__)
- `pyproject.toml` (if present)

---

## 2. Reproducibility

### Tests
- [ ] Run: `pytest -v` (all green, or graceful skips for optional dependencies).
- [ ] Verify test coverage: `test_pyelastica_bridge.py` (2 tests), `test_countercurvature_metrics.py` (8 tests).

### Quick Experiments
Run these exact commands and verify they complete without errors:

- [ ] `python3 -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity --quick`
  - **Expected output**: `outputs/experiments/spine_modes/spine_modes_results.csv`
  - **Check**: CSV contains `I`, `dIds`, `D_geo_norm` columns

- [ ] `python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram --quick`
  - **Expected output**: `outputs/experiments/phase_diagram/phase_diagram_data.csv`
  - **Check**: CSV contains `S_lat_asym`, `cobb_asym_deg`, `D_geo_norm` columns

- [ ] `python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation --quick`
  - **Expected output**: `outputs/experiments/microgravity/microgravity_summary.csv`
  - **Check**: CSV contains `D_geo_norm` for multiple gravity values

- [ ] `python3 -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure`
  - **Expected output**: `outputs/figs/fig_countercurvature_metrics.png`
  - **Check**: Figure is generated (may warn if data missing, but should handle gracefully)

### Output File Verification
- [ ] Check that the output filenames/paths these scripts print match what you reference in the paper/metrics docs.
- [ ] Verify all CSV files have expected column names (no typos in column headers).
- [ ] Confirm figure paths in manuscript match actual generated files.

---

## 3. Code ↔ Math ↔ Text Alignment

### Symbol-to-Function Mapping
For every new mathematical symbol in the manuscript, verify it maps to code:

- [ ] `g_{\mathrm{eff}}(s)` → `compute_countercurvature_metric()` (mentioned in Code Availability)
- [ ] `\widehat{D}_{\mathrm{geo}}` → `geodesic_curvature_deviation()` (mentioned in Code Availability)
- [ ] `S_{\mathrm{lat}}` → `compute_scoliosis_metrics()` (mentioned in Code Availability)
- [ ] `\chi_{\kappa}` → `CounterCurvatureParams.chi_kappa` (documented in API)
- [ ] `I(s)` → `InfoField1D` (documented in API)

### Threshold Consistency
- [ ] Your "scoliotic regime" thresholds in the text match the defaults in `RegimeThresholds`:
  - Check `src/spinalmodes/countercurvature/scoliosis_metrics.py` for default values
  - Verify manuscript uses same thresholds (e.g., `S_lat >= 0.05` or `Cobb >= 5°`)

### Function Name Verification
- [ ] All function names in Code Availability section exist in `src/spinalmodes/countercurvature/api.py`
- [ ] All function names are spelled correctly (check underscores, capitalization)

**Files to cross-check:**
- `manuscript/main_countercurvature.tex` (Methods, Results, Code Availability)
- `src/spinalmodes/countercurvature/api.py` (__all__ exports)
- `docs/public_api_reference.md` (function signatures)

---

## 4. Examples & Onboarding

- [ ] `examples/quickstart.py` runs and produces the expected plot:
  - **Command**: `python3 examples/quickstart.py` (with PYTHONPATH set)
  - **Expected output**: `outputs/examples/quickstart_curvature.png`
  - **Check**: Plot shows κ_passive vs κ_info with D̂_geo value

- [ ] `examples/quickstart.ipynb` can be opened and run in Jupyter:
  - **Check**: All cells execute without errors
  - **Check**: Final cell produces 4-panel figure

- [ ] README and `docs/countercurvature_overview.md` both show at least one working command for a new user:
  - **Check**: README has "Quickstart" section with copy-paste commands
  - **Check**: Overview doc has example usage

---

## 5. Limitations & Framing

- [ ] Limitations section clearly states:
  - [ ] Analog gravity (not fundamental GR modification)
  - [ ] Phenomenological metric (g_eff is empirical, not derived from first principles)
  - [ ] 2D pseudo-coronal scoliosis in some experiments (full 3D would use actual coronal coordinates)

- [ ] No place in the paper implies you are modifying GR; everything is framed as an analog-model language:
  - [ ] Check Abstract: uses "analog spacetime" or "analog model"
  - [ ] Check Discussion: "Analog gravity interpretation" subsection explicitly fences off over-claims
  - [ ] Check Methods: "analog model" language, not "modification of Einstein's equations"

**Files to check:**
- `manuscript/main_countercurvature.tex` (Abstract, Methods, Discussion, Limitations)
- `docs/paper_draft_limitations_outlook.md` (if referenced)

---

## 6. Documentation Completeness

- [ ] `docs/public_api_reference.md` exists and documents all public functions
- [ ] `docs/manuscript_code_data_availability.md` maps figures to data files
- [ ] `SANITY_CHECK.md` has working commands
- [ ] `CITATION.cff` has correct author name and ORCID (if available)

---

## 7. Manuscript-Specific Checks

- [ ] All figure references use correct labels (e.g., `\ref{fig:countercurvature_main}`)
- [ ] All citations have corresponding entries in `manuscript/refs.bib`
- [ ] Code Availability section has correct GitHub URL (replace `<your GitHub URL>`)
- [ ] Data Availability section lists actual file paths that exist
- [ ] No TODO comments remain in final manuscript

---

## Quick Verification Script

Run this to check basic functionality:

```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Quick experiments (should complete in < 1 minute each)
python3 -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity --quick
python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram --quick

# Check outputs exist
ls outputs/experiments/spine_modes/spine_modes_results.csv
ls outputs/experiments/phase_diagram/phase_diagram_data.csv

# Verify CSV columns
python3 -c "import pandas as pd; df = pd.read_csv('outputs/experiments/spine_modes/spine_modes_results.csv'); print('Columns:', df.columns.tolist())"
```

---

## Final Pre-Submission Checklist

Before submitting, ensure:

- [ ] All checkboxes above are checked
- [ ] GitHub repository is public (or "to be public on acceptance" noted)
- [ ] v0.1.0 tag exists on GitHub
- [ ] Zenodo archive created (optional, but recommended for DOI)
- [ ] Manuscript PDF compiles without errors
- [ ] All figures are included and referenced correctly
- [ ] Bibliography is complete

---

## Notes

- **If pytest is not installed**: Tests will fail, but experiments should still run. Note this in documentation.
- **If PyElastica is not installed**: PyElastica tests will skip gracefully; experiments use beam solver only.
- **Quick mode**: Use `--quick` flags for fast verification; full runs take longer but are needed for final figures.

---

## Status

Once all items are checked, the codebase is **ready for submission**. Remaining work is scientific (data extraction, paper tightening with real numbers, figure finalization).

