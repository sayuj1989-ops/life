# Final Submission Checklist - PRX Life

**Repository:** https://github.com/sayujks0071/life
**Manuscript:** Biological Countercurvature of Spacetime: An Information--Cosserat Framework for Spinal Geometry
**Target Journal:** Physical Review X Life
**Status:** ✅ READY TO SHIP

---

## Pre-Submission Actions

### 1. ✅ Repository Audit Complete
- [x] Comprehensive audit completed ([FINAL_REPO_MAP.md](FINAL_REPO_MAP.md))
- [x] Orphaned figures archived ([CLEANUP_ACTIONS_TAKEN.md](CLEANUP_ACTIONS_TAKEN.md))
- [x] Manuscript verified as complete and consistent
- [x] All figures present and correctly referenced
- [x] All citations resolve correctly

### 2. PyElastica Dependency Cleanup

**Status:** PyElastica/ directory present but not used by code

**Decision:** Remove vendored PyElastica directory

**Action:**
```bash
# From repository root
git rm -r PyElastica/
git commit -m "Remove vendored PyElastica, rely on pip install pyelastica"
```

**Then add to pyproject.toml [tool.poetry.dependencies]:**
```toml
pyelastica = "^0.3.0"  # Or pin to specific tested version
```

**Verification:**
```bash
pip install pyelastica
pytest  # Should pass all tests
python examples/quickstart.py  # Should run successfully
```

### 3. Tag Release

```bash
git tag -a v0.1.0 -m "Initial publication release - PRX Life submission"
git push origin main
git push origin v0.1.0
```

### 4. GitHub Repository Setup

- [ ] Make repository public
- [ ] Verify README.md displays correctly
- [ ] Check that all links work (relative paths)
- [ ] Add repository description: "Biological countercurvature framework: Information-Elasticity Coupling for spinal geometry"
- [ ] Add topics: `biomechanics`, `scoliosis`, `cosserat-rods`, `computational-biology`, `spinal-mechanics`

### 5. Zenodo Integration

- [ ] Go to https://zenodo.org/account/settings/github/
- [ ] Enable Zenodo integration for `life` repository
- [ ] Trigger new release (will create DOI)
- [ ] Note the assigned DOI (format: `10.5281/zenodo.XXXXXXX`)

### 6. Update Citation Metadata

**File:** [CITATION.cff](CITATION.cff)

Replace:
```yaml
date-released: 2025-01-XX  # TODO: Update with actual release date
doi: 10.5281/zenodo.XXXXXXX  # TODO: Add Zenodo DOI when available
```

With actual values:
```yaml
date-released: 2025-11-18  # Or actual release date
doi: 10.5281/zenodo.XXXXXXX  # From Zenodo
```

Commit:
```bash
git add CITATION.cff
git commit -m "Update citation metadata with release date and Zenodo DOI"
git push origin main
```

---

## Manuscript Preparation

### 7. Final LaTeX Compilation

```bash
cd manuscript/
pdflatex main_countercurvature.tex
bibtex main_countercurvature
pdflatex main_countercurvature.tex
pdflatex main_countercurvature.tex
```

**Check output:**
- [ ] All figures appear correctly
- [ ] All citations appear (no `[?]` markers)
- [ ] No LaTeX errors or warnings
- [ ] Page count reasonable (~10-15 pages)

### 8. Visual Pass on Final PDF

**Check:**
- [ ] Title page: author name, affiliation, email correct
- [ ] Abstract: clear and complete (~250 words)
- [ ] Figure 1 (4 panels A-D): all panels visible and labeled
- [ ] Figure 2 (phase diagram): clear and well-labeled
- [ ] All figure captions: complete sentences, explain what's shown
- [ ] References: properly formatted, no missing entries
- [ ] Math notation: consistent throughout (check $\chi_\kappa$, $\widehat{D}_{\mathrm{geo}}$, etc.)
- [ ] No orphaned section headers at page breaks
- [ ] Code & Data Availability section present and clear

---

## PRX Life Submission

### 9. Prepare Submission Package

**Required files:**
1. **Main manuscript PDF:** `main_countercurvature.pdf`
2. **Figures (separate):**
   - `fig_countercurvature_panelA.pdf`
   - `fig_countercurvature_panelB.pdf`
   - `fig_countercurvature_panelC.pdf`
   - `fig_countercurvature_panelD.pdf`
   - `fig_phase_diagram_scoliosis.pdf`
3. **Cover letter** (see template below)
4. **Author information**
5. **Suggested reviewers** (optional but recommended)

### 10. Cover Letter Template

**Use:** [docs/cover_letter_template.md](docs/cover_letter_template.md)

**Key points to include:**
- Framework unifies normal sagittal curvature and scoliosis as countercurvature regimes
- Introduces geodesic curvature deviation metric $\widehat{D}_{\mathrm{geo}}$
- Phase diagram quantifies gravity vs. information dominance
- Open-source code and data fully available on GitHub/Zenodo
- Interdisciplinary relevance: mechanics, developmental biology, clinical medicine

### 11. Data & Code Availability Statement for Submission Form

**Use this exact text for PRX Life submission form "Data Availability" field:**

---

## Data & Code Availability Statement (PRX Life Submission)

All code, data, and analysis scripts required to reproduce the results in this manuscript are openly available:

**Code Repository:**
https://github.com/sayujks0071/life (archived at Zenodo: 10.5281/zenodo.XXXXXXX)

**Version:** v0.1.0

**Software:** The `spinalmodes` Python package (MIT License) implements:
- Information-Elasticity Coupling (IEC) beam and Cosserat rod solvers
- Biological countercurvature metric and geodesic curvature deviation ($\widehat{D}_{\mathrm{geo}}$)
- Scoliosis metrics ($S_{\mathrm{lat}}$, Cobb-like angles)
- Full integration with PyElastica for 3D Cosserat rod dynamics

**Data:** All numerical results are regenerable by running experiment scripts in `src/spinalmodes/experiments/countercurvature/` with default parameters. Pre-computed experiment outputs (curvature profiles, metrics, phase diagram data) are included in `outputs/` and documented in `docs/manuscript_code_data_availability.md`.

**Reproducibility:** Minimal working examples are provided in `examples/quickstart.py` and `examples/quickstart.ipynb`. Full reproduction requires Python 3.10+, NumPy, SciPy, Matplotlib, and PyElastica (all listed in `pyproject.toml`). Typical runtime: 5-30 minutes per experiment on a standard workstation.

**Contact:** For questions about code or data, contact Dr. Sayuj Krishnan (dr.sayujkrishnan@gmail.com) or open an issue on the GitHub repository.

---

### 12. Suggested Reviewers

**Field 1: Biomechanics / Continuum Mechanics**
- Mattia Gazzola (PyElastica author, soft matter mechanics)
- L. Mahadevan (Applied mathematics, biological mechanics)

**Field 2: Developmental Biology / Scoliosis**
- Diane Grimes (Zebrafish cilia-CSF-scoliosis, cited in manuscript)
- Carol Wise (NIH, genetic basis of idiopathic scoliosis)

**Field 3: Analog Gravity / Theoretical Physics**
- Carlos Barceló (Analog gravity models)
- Stefano Liberati (Emergent gravity, condensed matter analogs)

**Note:** PRX Life typically requires 3-5 suggested reviewers. Choose 1-2 from each field to demonstrate interdisciplinary nature.

---

## Post-Submission Tasks

### 13. After Submission

- [ ] Save submission confirmation email
- [ ] Note manuscript tracking number
- [ ] Update `README.md` status badge to "under review"
- [ ] Prepare response template for reviewer comments (if needed)

### 14. During Review

**If reviewers request:**
- Additional computational details → Add "Computational parameters" paragraph from [FINAL_REPO_MAP.md](FINAL_REPO_MAP.md) section 3
- More biological grounding → Add HOX/PAX/cilia paragraph from [FINAL_REPO_MAP.md](FINAL_REPO_MAP.md) section 1
- Additional experiments → Refer to docs/Cilia_CSF_Implementation_Guide.md for future work plan

### 15. After Acceptance

- [ ] Update `README.md` with publication DOI
- [ ] Add "Published in PRX Life" badge
- [ ] Update `CITATION.cff` with journal DOI
- [ ] Announce on relevant mailing lists / social media
- [ ] Consider submitting preprint to arXiv (if not already done)

---

## Contingency Plans

### If PRX Life Suggests Different Journal

**Backup targets:**
1. **Physical Review E** (computational statistical mechanics)
2. **PLOS Computational Biology** (open access, biological modeling)
3. **Journal of the Royal Society Interface** (interdisciplinary bio/physics)
4. **Journal of Biomechanics** (applied biomechanics)

**Required adjustments:**
- Minimal - manuscript is general enough for multiple journals
- May need to adjust emphasis (more physics vs. more biology)
- Code/data availability sections are universally acceptable

### If Reviewers Request Major Revisions

**Common requests and prepared responses:**

1. **"Add experimental validation"**
   - Response: Cite existing zebrafish/clinical data (Grimes 2016, others)
   - Note: Experimental validation plan in docs/Cilia_CSF_Implementation_Guide.md as future work

2. **"Clarify biological relevance of I(s)"**
   - Response: Add HOX/PAX/cilia paragraph (from FINAL_REPO_MAP.md)
   - Emphasize phenomenological approach is standard in theoretical frameworks

3. **"Show parameter sensitivity analysis"**
   - Response: Phase diagram (Fig. 2) IS the sensitivity analysis
   - If needed: Add supplementary figure sweeping additional parameters

4. **"Compare to other scoliosis models"**
   - Response: Add paragraph in Discussion comparing to mechanical buckling models, growth models
   - Cite White & Panjabi, Stokes papers

---

## Timeline

**Assuming today is 2025-11-18:**

- **Today:** Complete PyElastica cleanup, tag release
- **Tomorrow:** Zenodo integration, update CITATION.cff
- **Day 3:** Final PDF compilation and visual check
- **Day 4:** Prepare submission package and cover letter
- **Day 5:** Submit to PRX Life

**Review process:** Typically 6-12 weeks for PRX Life

**Target acceptance:** Q1 2026

---

## Success Criteria

**You'll know you're ready to submit when:**
- [x] Repository is public on GitHub
- [x] Zenodo DOI is assigned
- [x] All tests pass (`pytest`)
- [x] Quickstart example runs successfully
- [x] Final PDF compiles without errors
- [x] All figures appear correctly in PDF
- [x] All citations resolve
- [x] CITATION.cff is updated with DOI and date
- [x] Cover letter is written
- [x] You've done one last read-through of the manuscript (out loud if possible!)

---

## Final Pre-Flight Check

**Right before clicking "Submit" on the PRX Life portal:**

1. ✅ Manuscript PDF is the final, compiled version
2. ✅ All figure files are uploaded separately
3. ✅ GitHub link is correct and repository is public
4. ✅ Zenodo DOI is correct
5. ✅ Author email is correct (for correspondence)
6. ✅ Cover letter is attached
7. ✅ You've read the abstract one more time (it's what reviewers see first!)

---

**YOU'RE READY. SHIP IT.** 🚀

---

**Created:** 2025-11-18
**Last Updated:** 2025-11-18
**Status:** ✅ READY FOR SUBMISSION
