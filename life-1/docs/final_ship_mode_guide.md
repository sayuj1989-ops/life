# Final Ship Mode Guide

## 🚀 Last Leg: From "Almost Done" to "Submitted"

This guide sequences the final steps to get from "ship mode" to actual submission.

---

## 1️⃣ Lock in the Code Side (Same Day Job)

### Step 1: Run Full Sanity Check

Execute these commands as if you're a reviewer:

```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# All tests (if pytest installed)
pytest -v

# Quick experiments (verify nothing broke)
python3 -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity --quick
python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram --quick
python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation --quick

# Figure + demo
python3 -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
python3 examples/quickstart.py
```

**Expected results:**
- ✅ All tests pass (or skip gracefully for optional deps)
- ✅ All experiments complete without errors
- ✅ CSV files created in `outputs/experiments/*/`
- ✅ Figures generated in `outputs/figs/` and `outputs/examples/`

### Step 2: Version Consistency Check

Verify these all say `v0.1.0`:

- [ ] `CITATION.cff` → `version: 0.1.0`
- [ ] `src/spinalmodes/__init__.py` → `__version__ = "0.1.0"`
- [ ] `manuscript/main_countercurvature.tex` → Code Availability section says "version 0.1.0"
- [ ] `pyproject.toml` (if present) → `version = "0.1.0"`

### Step 3: Tag v0.1.0 on GitHub

```bash
# Commit any final changes
git add .
git commit -m "Finalize v0.1.0 for publication"

# Tag the release
git tag -a v0.1.0 -m "Publication version: Biological Countercurvature of Spacetime"
git push origin v0.1.0
```

### Step 4: Run Pre-Submission Checklist

Go through `docs/pre_submission_checklist.md` and verify all items:

- [ ] Versioning consistency
- [ ] Reproducibility (all commands work)
- [ ] Code ↔ Math ↔ Text alignment
- [ ] Examples run correctly
- [ ] Limitations clearly stated

**Status**: Once all checks pass, code side is **locked**. ✅

---

## 2️⃣ Choose the Cover Letter Flavor

### Journal-Specific Recommendations

#### **PRX Life / Nature Communications** (Broad Interest)
- **Use**: Version 1 (concise) + 1-2 sentences from Version 3
- **Focus**: Unifying framework, broad biological interest, reproducibility
- **Length**: ~150-200 words

#### **J. Biomechanics / Computational Biology** (Technical)
- **Use**: Version 2 (more technical)
- **Focus**: IEC details, Cosserat mechanics, computational methods
- **Length**: ~200-250 words

#### **Open Science / Methods-Heavy Journals**
- **Use**: Version 3 (reproducibility emphasis)
- **Focus**: Fully open pipeline, versioned releases, reproducible scripts
- **Length**: ~200-250 words

### Customization Template

For PRX Life / Nat Comms, combine Version 1 + Version 3:

> This work introduces a quantitative framework for "biological countercurvature of spacetime" that unifies normal spinal curvature and scoliosis-like symmetry breaking within a single Information-Elasticity Coupling (IEC) model. All simulations and analyses are implemented in the open-source Python package `spinalmodes` (v0.1.0), which provides a stable public API for countercurvature metrics, geodesic curvature deviation, and scoliosis indices. The complete codebase, reproducible experiment scripts, and all data underlying the figures are available at [GitHub URL], with versioned releases and comprehensive documentation. The framework can be invoked via simple command-line interfaces, and a minimal 30-line example (`examples/quickstart.py`) demonstrates the core workflow from information fields to countercurvature metrics. This fully reproducible pipeline enables direct testing of the "biological countercurvature" hypothesis and provides a foundation for future extensions to experimental data and clinical applications.

**Next step**: If you tell me your target journal, I can expand this into a full 3-4 paragraph cover letter with:
- Why now (timing/context)
- What's new vs existing spinal biomechanics
- Why this journal (fit/audience)

---

## 3️⃣ Scientific Last Mile: Numbers & Sentences

### Step 1: Run Full Parameter Sweeps

**DO NOT use `--quick` flags** - these are for verification only. Run full sweeps:

```bash
# Full phase diagram (may take 10-30 minutes)
python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram

# Full microgravity sweep
python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation

# Full scoliosis bifurcation
python3 -m spinalmodes.experiments.countercurvature.experiment_scoliosis_bifurcation
```

**Expected outputs:**
- `outputs/experiments/phase_diagram/phase_diagram_data.csv` (full grid)
- `outputs/experiments/microgravity/microgravity_summary.csv` (full g range)
- `outputs/experiments/scoliosis_bifurcation/scoliosis_bifurcation_data.csv` (full sweep)

### Step 2: Extract Anchor Numbers

Use `docs/DATA_EXTRACTION_TEMPLATE.md` to pull:

#### A. D̂_geo Values
- [ ] Gravity-dominated regime: D̂_geo ≈ ? (for χ_κ = 0.01, g = 9.81)
- [ ] Cooperative regime: D̂_geo ≈ ? (for χ_κ = 0.04, g = 9.81)
- [ ] Information-dominated regime: D̂_geo ≈ ? (for χ_κ = 0.08, g = 0.1)

#### B. Scoliosis Metrics
- [ ] Symmetric case: S_lat ≈ ?, Cobb-like ≈ ? (baseline)
- [ ] Asymmetric case (ε_asym = 0.05) in gravity-dominated: S_lat ≈ ?, Cobb-like ≈ ?
- [ ] Asymmetric case (ε_asym = 0.05) in info-dominated: S_lat ≈ ?, Cobb-like ≈ ?

#### C. Microgravity Persistence
- [ ] At g = 9.81: D̂_geo ≈ ?, passive energy ≈ ?
- [ ] At g = 0.01: D̂_geo ≈ ?, passive energy ≈ ?
- [ ] Ratio: D̂_geo(g=0.01) / D̂_geo(g=9.81) ≈ ? (should be ~1.0, showing persistence)

#### D. Bifurcation Point
- [ ] Critical χ_κ where scoliosis emerges: χ_κ ≈ ? (for fixed g = 9.81, ε_asym = 0.05)
- [ ] Amplification factor: S_lat / ε_asym ≈ ? (in info-dominated regime)

### Step 3: Quantitative Language Pass

Go through Abstract + Results and replace vague language with numbers:

**Before:**
> "In the information-dominated regime, small asymmetries produce large lateral deviations."

**After:**
> "In the information-dominated regime (D̂_geo > 0.3), a 5% asymmetry (ε_asym = 0.05) produces lateral deviations with S_lat ≈ 0.12 and Cobb-like angles > 10°, representing a 2-3× amplification relative to the gravity-dominated regime."

**Target replacements:**
- "small/large/modest/pronounced" → specific numbers
- "increased/decreased" → "from X to Y" or "by Z%"
- "significant" → "> threshold" with actual threshold value

### Step 4: Update Manuscript with Numbers

**Abstract:**
- [ ] Add 1-2 quantitative statements (e.g., "D̂_geo ranges from <0.1 in gravity-dominated to >0.3 in information-dominated regimes")

**Results:**
- [ ] Panel A (curvature profiles): Add "κ_info differs from κ_passive by up to X%"
- [ ] Panel B (g_eff): Add "g_eff peaks at Y in regions of high information density"
- [ ] Panel C (D̂_geo vs χ_κ): Add "D̂_geo increases from 0.05 to 0.35 as χ_κ increases from 0 to 0.08"
- [ ] Panel D (microgravity): Add "D̂_geo remains ≈0.25 while passive energy collapses by 95% as g → 0.01"

**Phase Diagram:**
- [ ] Add "Scoliotic regime (S_lat ≥ 0.05, Cobb-like ≥ 5°) emerges for D̂_geo > 0.3 and χ_κ > 0.06"

---

## 4️⃣ Final Manuscript Checks

### Before Submission

- [ ] Replace `<your GitHub URL>` with actual repository URL
- [ ] Verify all figure paths exist and are correct
- [ ] Check all citations have entries in `refs.bib`
- [ ] Run LaTeX compilation: `pdflatex main_countercurvature.tex` (no errors)
- [ ] Verify bibliography compiles: `bibtex main_countercurvature`
- [ ] Final PDF has all figures, correct page numbers, complete references

### Optional: Zenodo Archive

If archiving on Zenodo for DOI:

1. Create Zenodo account
2. Create new upload
3. Upload repository (or zip of v0.1.0 tag)
4. Fill metadata (use `CITATION.cff` as reference)
5. Get DOI: `10.5281/zenodo.XXXXXXX`
6. Add to manuscript: "Archived at Zenodo (DOI: 10.5281/zenodo.XXXXXXX)"

---

## 5️⃣ Submission Package

### What to Submit

1. **Manuscript PDF** (`main_countercurvature.pdf`)
2. **Cover Letter** (using chosen paragraph + journal-specific expansion)
3. **Figures** (high-resolution PDFs or PNGs, as required by journal)
4. **Supplementary Materials** (if any):
   - Extended methods
   - Additional figures
   - Data tables

### Cover Letter Structure

1. **Opening** (1 paragraph): Why this work matters now
2. **Framework paragraph** (1 paragraph): Use chosen version from `docs/cover_letter_paragraph.md`
3. **Key results** (1 paragraph): 2-3 highlight bullets
4. **Why this journal** (1 sentence): Fit and audience

**I can expand your chosen paragraph into a full cover letter if you tell me:**
- Target journal name
- Why this journal (fit/audience)
- 2-3 key results you want to highlight

---

## Timeline Estimate

- **Code lock-in**: 1-2 hours (sanity checks + tagging)
- **Cover letter**: 30 minutes (choose version + customize)
- **Full sweeps**: 1-2 hours (depending on parameter grid size)
- **Data extraction**: 1 hour (pull numbers + update manuscript)
- **Quantitative pass**: 1-2 hours (replace vague language)
- **Final checks**: 30 minutes (LaTeX, citations, figures)

**Total**: ~5-7 hours of focused work to go from "ship mode" to "submitted"

---

## Status

✅ **Code side**: Ready to lock (run sanity checks)
⏳ **Cover letter**: Choose version based on target journal
⏳ **Scientific**: Run full sweeps + extract numbers
⏳ **Manuscript**: Quantitative language pass

**You're 95% there!** The last 5% is just running the sweeps and replacing vague language with real numbers. 🚀

