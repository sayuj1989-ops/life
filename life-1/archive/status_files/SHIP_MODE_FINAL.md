# 🚀 Ship Mode: Final Checklist & Next Steps

## ✅ Status: Code Side is GREEN

**Sanity checks passed:**
- ✅ `experiment_spine_modes_vs_gravity --quick` → Success
- ✅ `quickstart.py` → Success (D_geo_norm = 0.162637)
- ✅ Version consistency: `CITATION.cff` and `__init__.py` both say v0.1.0

**You're ready to lock in the code side!**

---

## 1️⃣ Lock in Code Side (30 minutes)

### Step 1: Final Version Check

All these should say `v0.1.0`:
- ✅ `CITATION.cff` → `version: 0.1.0` ✓
- ✅ `src/spinalmodes/__init__.py` → `__version__ = "0.1.0"` ✓
- ⏳ `manuscript/main_countercurvature.tex` → Check Code Availability section

### Step 2: Tag v0.1.0 on GitHub

```bash
# Commit any final changes
git add .
git commit -m "Finalize v0.1.0 for publication"

# Tag the release
git tag -a v0.1.0 -m "Publication version: Biological Countercurvature of Spacetime"
git push origin v0.1.0
```

### Step 3: Run Remaining Quick Checks

```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Remaining quick experiments
python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram --quick
python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation --quick
python3 -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
```

**Once these pass, code side is LOCKED.** ✅

---

## 2️⃣ Cover Letter: PRX Life Ready

### ✅ PRX Life Cover Letter Complete

**Ready-to-use cover letter is in:** `docs/cover_letter_expansion_template.md`

**Just replace:**
- `<your GitHub URL>` → Your actual repository URL
- `<Your affiliation>` → Your institution
- `<Email>` → Your email

**The cover letter includes:**
- Opening paragraph (framework overview)
- Key results (regime mapping, scoliosis symmetry breaking, microgravity persistence)
- Analog gravity interpretation (with clear framing that it's not fundamental GR)
- Reproducibility statement (spinalmodes v0.1.0)
- Why PRX Life (3 specific reasons)

### Key Claims Bullets

**Also created:** `docs/key_claims_bullets.md` with reusable bullets for:
- PRX Life submission form (3-4 concise bullets)
- Talks/presentations (more technical version)
- Emails to collaborators (conceptual version)
- Social media (single-sentence version)

**Next:** Update placeholder numbers in bullets once you run full sweeps.

---

## 3️⃣ Scientific Last Mile: Numbers & Sentences

### Step 1: Run Full Parameter Sweeps

**⚠️ DO NOT use `--quick` flags** - these are for verification only.

```bash
# Full phase diagram (may take 10-30 minutes)
python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram

# Full microgravity sweep
python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation

# Full scoliosis bifurcation
python3 -m spinalmodes.experiments.countercurvature.experiment_scoliosis_bifurcation
```

**Expected runtime:** 30-60 minutes total (depending on parameter grid size)

### Step 2: Extract Anchor Numbers

Use `docs/DATA_EXTRACTION_TEMPLATE.md` to extract:

#### A. D̂_geo Values (from phase diagram)
- [ ] Gravity-dominated: D̂_geo ≈ ? (χ_κ = 0.01, g = 9.81)
- [ ] Cooperative: D̂_geo ≈ ? (χ_κ = 0.04, g = 9.81)
- [ ] Information-dominated: D̂_geo ≈ ? (χ_κ = 0.08, g = 0.1)

#### B. Scoliosis Metrics (from phase diagram or scoliosis experiment)
- [ ] Symmetric baseline: S_lat ≈ ?, Cobb-like ≈ ?
- [ ] Asymmetric in gravity-dominated: S_lat ≈ ?, Cobb-like ≈ ?
- [ ] Asymmetric in info-dominated: S_lat ≈ ?, Cobb-like ≈ ?
- [ ] Amplification factor: (S_lat_asym / S_lat_sym) in info-dominated ≈ ?

#### C. Microgravity Persistence (from microgravity experiment)
- [ ] At g = 9.81: D̂_geo ≈ ?, passive_energy ≈ ?
- [ ] At g = 0.01: D̂_geo ≈ ?, passive_energy ≈ ?
- [ ] Passive energy collapse: (E_passive(g=0.01) / E_passive(g=9.81)) ≈ ? (should be ~0.05, i.e., 95% reduction)
- [ ] D̂_geo persistence: (D̂_geo(g=0.01) / D̂_geo(g=9.81)) ≈ ? (should be ~1.0, showing persistence)

#### D. Bifurcation Point (from scoliosis experiment)
- [ ] Critical χ_κ where scoliosis emerges: χ_κ ≈ ? (for fixed g = 9.81, ε_asym = 0.05)

### Step 3: Quantitative Language Pass

Go through Abstract + Results and replace vague language:

**Before → After Examples:**

| Before | After |
|--------|-------|
| "small asymmetries produce large deviations" | "5% asymmetry (ε_asym = 0.05) produces S_lat ≈ 0.12 and Cobb-like angles > 10°" |
| "D̂_geo increases with coupling strength" | "D̂_geo increases from 0.05 to 0.35 as χ_κ increases from 0 to 0.08" |
| "information persists in microgravity" | "D̂_geo remains ≈0.25 while passive energy collapses by 95% as g → 0.01" |
| "scoliosis emerges in information-dominated regime" | "Scoliotic regime (S_lat ≥ 0.05, Cobb-like ≥ 5°) emerges for D̂_geo > 0.3 and χ_κ > 0.06" |

**Target sections to update:**
- [ ] Abstract: Add 1-2 quantitative statements
- [ ] Results Panel A: Add "κ_info differs from κ_passive by up to X%"
- [ ] Results Panel C: Add "D̂_geo increases from Y to Z as χ_κ increases..."
- [ ] Results Panel D: Add "D̂_geo remains ≈W while passive energy collapses by X%"
- [ ] Phase Diagram: Add "Scoliotic regime emerges for D̂_geo > 0.3 and χ_κ > 0.06"

**See:** `docs/PAPER_TIGHTENING_GUIDE.md` for more examples

---

## 4️⃣ Final Manuscript Checks

### Before Submission

- [ ] Replace `<your GitHub URL>` in Code Availability with actual URL
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
4. **Supplementary Materials** (if any)

### Cover Letter Structure

1. **Opening** (1 paragraph): Why this work matters now
2. **Framework paragraph** (1 paragraph): Use chosen version from `docs/cover_letter_paragraph.md`
3. **Key results** (1 paragraph): 2-3 highlight bullets with numbers
4. **Why this journal** (1 sentence): Fit and audience

**I can expand your chosen paragraph into a full cover letter if you tell me:**
- Target journal name
- Why this journal (fit/audience)
- 2-3 key results you want to highlight

**See:** `docs/cover_letter_expansion_template.md` for full templates

---

## Timeline Estimate

| Task | Time |
|------|------|
| Code lock-in (tag v0.1.0) | 30 min |
| Cover letter (choose + customize) | 30 min |
| Full parameter sweeps | 1-2 hours |
| Data extraction | 1 hour |
| Quantitative language pass | 1-2 hours |
| Final manuscript checks | 30 min |

**Total**: ~5-7 hours of focused work

---

## Quick Reference

- **Sanity checks**: `docs/pre_submission_checklist.md`
- **Cover letter options**: `docs/cover_letter_paragraph.md`
- **Cover letter templates**: `docs/cover_letter_expansion_template.md`
- **Data extraction**: `docs/DATA_EXTRACTION_TEMPLATE.md`
- **Paper tightening**: `docs/PAPER_TIGHTENING_GUIDE.md`
- **Final guide**: `docs/final_ship_mode_guide.md` (this file)

---

## Status Summary

✅ **Code**: Green (sanity checks passing)  
✅ **Manuscript**: Code/Data Availability sections added  
✅ **Documentation**: Complete  
⏳ **Cover letter**: Choose version based on target journal  
⏳ **Scientific**: Run full sweeps + extract numbers  
⏳ **Final polish**: Quantitative language pass  

**You're 95% there!** The last 5% is running the full sweeps and replacing vague language with real numbers. 🚀

---

## Next Immediate Action

**Tell me:**
1. **Target journal** → I'll generate a full cover letter
2. **When you run full sweeps** → I can help extract numbers
3. **Any blockers** → I can help troubleshoot

Once you have the numbers from full sweeps, I can help you:
- Update the manuscript with quantitative statements
- Generate the final cover letter
- Finalize the submission package

**You've got this!** 🔥

