# SUBMIT NOW - Ultra-Compact Checklist

**Time to complete:** 1-2 hours
**Target:** PRX Life submission within 48 hours

---

## ✅ Pre-Flight (30 min)

### 1. Remove PyElastica vendored directory
```bash
git rm -r PyElastica/
git commit -m "Remove vendored PyElastica, rely on pip install pyelastica"
```

Add to `pyproject.toml` under `[tool.poetry.dependencies]`:
```toml
pyelastica = "^0.3.0"
```

Verify:
```bash
pip install pyelastica
pytest  # Must pass
python examples/quickstart.py  # Must generate plot
```

---

### 2. Tag release
```bash
git tag -a v0.1.0 -m "Publication version"
git push origin main --tags
```

---

### 3. Make repo public + Get Zenodo DOI
- GitHub → Settings → Change visibility → Public
- https://zenodo.org/account/settings/github/ → Enable for `life`
- Trigger release → Note DOI: `10.5281/zenodo.XXXXXXX`

---

### 4. Update metadata
Edit `CITATION.cff`:
```yaml
date-released: 2025-11-18
doi: 10.5281/zenodo.XXXXXXX  # From step 3
```

```bash
git add CITATION.cff
git commit -m "Update citation with Zenodo DOI"
git push origin main
```

---

## 📄 Manuscript (30 min)

### 5. Compile final PDF
```bash
cd manuscript/
pdflatex main_countercurvature.tex
bibtex main_countercurvature
pdflatex main_countercurvature.tex
pdflatex main_countercurvature.tex
```

**Check:**
- [ ] All figures appear
- [ ] No `[?]` citations
- [ ] Author info correct
- [ ] ~10-15 pages

---

### 6. Prepare submission folder
```bash
mkdir PRX_Life_Submission
cp manuscript/main_countercurvature.pdf PRX_Life_Submission/
cp manuscript/fig_*.pdf PRX_Life_Submission/
```

---

## 📝 Supporting Docs (30 min)

### 7. Write cover letter
Use template: `docs/cover_letter_expansion_template.md`

**Key points:**
- Unifies normal curvature + scoliosis as countercurvature regimes
- Introduces $\widehat{D}_{\mathrm{geo}}$ metric
- Phase diagram quantifies gravity vs. information
- Open code/data on GitHub/Zenodo

Save as: `PRX_Life_Submission/cover_letter.pdf`

---

## 🚀 Submit (20 min)

### 8. Go to PRX Life portal
https://journals.aps.org/prxlife/authors

**Upload:**
- `main_countercurvature.pdf`
- 5 figure files (if separate upload)
- `cover_letter.pdf`

**Paste Data Availability** (from `PRX_LIFE_DATA_CODE_BLURB.md`):
> All code, data, and analysis scripts required to reproduce the results in this manuscript are openly available:
>
> **Code Repository:** https://github.com/sayujks0071/life (archived at Zenodo: 10.5281/zenodo.XXXXXXX)
>
> **Version:** v0.1.0
>
> **Software:** The `spinalmodes` Python package (MIT License) implements Information-Elasticity Coupling (IEC) beam and Cosserat rod solvers, biological countercurvature metric and geodesic curvature deviation ($\widehat{D}_{\mathrm{geo}}$), scoliosis metrics, and full integration with PyElastica for 3D Cosserat rod dynamics.
>
> **Data:** All numerical results are regenerable by running experiment scripts in `src/spinalmodes/experiments/countercurvature/` with default parameters. Pre-computed outputs are in `outputs/` and documented in `docs/manuscript_code_data_availability.md`.
>
> **Reproducibility:** Minimal examples in `examples/quickstart.py`. Full reproduction requires Python 3.10+, NumPy, SciPy, Matplotlib, PyElastica (listed in `pyproject.toml`). Typical runtime: 5-30 minutes per experiment.
>
> **Contact:** dr.sayujkrishnan@gmail.com

**Suggested Reviewers** (from `SUGGESTED_REVIEWERS_PRX_LIFE.md`):
1. Mattia Gazzola (mgazzola@illinois.edu) - Cosserat rods, PyElastica
2. Diane Grimes (dgrimes@kumc.edu) - Scoliosis biology, cilia-CSF
3. Alain Goriely (goriely@maths.ox.ac.uk) - Mathematical biology
4. Carol Wise (carolw@mail.nih.gov) - Genetic basis of IS
5. Carlos Barceló (carlos@iaa.es) - Analog gravity

**Keywords:**
biological countercurvature, information-elasticity coupling, spinal biomechanics, scoliosis, analog gravity, Cosserat rod mechanics

---

## ✅ Done!

- [ ] Submission confirmation email received
- [ ] Note manuscript tracking number
- [ ] Update `README.md` status to "Under review"

---

**Review timeline:** 6-12 weeks
**Expected acceptance:** Q1 2026

**You did it.** 🎉

---

**All supporting docs:**
- [FINAL_REPO_MAP.md](FINAL_REPO_MAP.md) - Full audit
- [FINAL_SUBMISSION_CHECKLIST.md](FINAL_SUBMISSION_CHECKLIST.md) - Detailed guide
- [PRX_LIFE_DATA_CODE_BLURB.md](PRX_LIFE_DATA_CODE_BLURB.md) - Copy-paste text
- [SUGGESTED_REVIEWERS_PRX_LIFE.md](SUGGESTED_REVIEWERS_PRX_LIFE.md) - Reviewer strategy
- [SHIP_IT.md](SHIP_IT.md) - Comprehensive overview

**Questions?** You have all the docs. Just execute the checklist above.

**GO.** 🚀
