# PRX Life Submission Checklist

**Date:** 2025-01-XX  
**Manuscript:** `manuscript/main_countercurvature.tex`  
**Status:** Ready for submission

---

## Pre-Submission Verification

### ✅ 1. LaTeX Compilation

**Action Required:**
```bash
cd manuscript
pdflatex main_countercurvature.tex
bibtex main_countercurvature
pdflatex main_countercurvature.tex
pdflatex main_countercurvature.tex
```

**Check:**
- [ ] PDF compiles without errors
- [ ] No "Undefined citation" warnings
- [ ] All figures load correctly
- [ ] Equation numbers are sequential
- [ ] No "??" or "[?]" in references

**Note:** If `pdflatex` is not installed, you may need to:
- Install MacTeX (macOS): `brew install --cask mactex`
- Or use an online LaTeX compiler (Overleaf, etc.)
- Or compile on a system with LaTeX installed

---

### ✅ 2. PDF Content Review

**Figures:**
- [ ] **Fig. 1**: Countercurvature panels (A-D) display correctly
  - Panel A: Curvature profiles κ₀ vs κ_I
  - Panel B: Countercurvature metric g_eff(s)
  - Panel C: D̂_geo vs χ_κ
  - Panel D: Microgravity adaptation
- [ ] **Fig. 2**: Phase diagram with scoliosis regimes displays correctly
  - Contours show D̂_geo
  - Scoliosis regime markers visible

**Equations:**
- [ ] All equation numbers are sequential
- [ ] Symbols consistent: `g_\mathrm{eff}`, `\widehat{D}_\mathrm{geo}`, `\chi_{\kappa}`, etc.
- [ ] No broken equation formatting

**References:**
- [ ] All `\cite{}` commands resolve to bibliography entries
- [ ] No `[?]` or `??` placeholders
- [ ] Bibliography style is consistent (unsrtnat)

**Text:**
- [ ] No TODOs or "in this work we will..." placeholders
- [ ] All numerical values are present (e.g., D̂_geo ≈ 0.14, etc.)
- [ ] Author information is complete and correct

---

## Submission Package

### ✅ 3. Required Files

**Main Document:**
- [x] `manuscript/main_countercurvature.tex` - Main LaTeX source
- [x] `manuscript/refs.bib` - Bibliography file
- [ ] `manuscript/main_countercurvature.pdf` - Compiled PDF (generate after compilation)

**Figures:**
- [x] `manuscript/fig_countercurvature_panelA.pdf`
- [x] `manuscript/fig_countercurvature_panelB.pdf`
- [x] `manuscript/fig_countercurvature_panelC.pdf`
- [x] `manuscript/fig_countercurvature_panelD.pdf`
- [x] `manuscript/fig_phase_diagram_scoliosis.pdf`
- [x] `figure1.png` (root directory, referenced as `../figure1.png`)

**Source Bundle (if requested):**
- [x] LaTeX source files
- [x] Bibliography file
- [x] Figure PDFs
- [x] Code repository URL: `https://github.com/sayujks0071/life`

---

### ✅ 4. Cover Letter

**Key Points to Highlight:**

1. **New Conceptual Framework:**
   - Biological countercurvature: information-driven modification of effective geometry
   - Information–Cosserat framework unifying normal and pathological spinal curvature
   - Analog-gravity perspective (rod in gravity as effective spacetime)

2. **Key Quantitative Results:**
   - Sine-like S-curve: max-to-RMS curvature ratio ≈ 1.81, D̂_geo ≈ 0.14
   - Microgravity persistence: D̂_geo ≈ 0.091 unchanged as g → 0.10
   - Phase diagram: distinct gravity-dominated, cooperative, and information-dominated regimes
   - Scoliosis-like symmetry breaking predicted in information-dominated regime

3. **Relevance to PRX Life:**
   - Interdisciplinary physics–biology framework
   - Quantitative, testable predictions
   - Fully reproducible open-source code (`spinalmodes` v0.1.0)
   - Links information processing, mechanics, and geometry in living systems

**Cover Letter Template:**
```
Dear Editors,

I would like to submit our manuscript, "Biological Countercurvature of 
Spacetime: An Information--Cosserat Framework for Spinal Geometry," for 
consideration as an Article in PRX Life.

[Insert 2-3 paragraphs from docs/cover_letter_expansion_template.md]

[Key highlights: new framework, quantitative results, reproducibility]

Thank you for considering our work.

Sincerely,
Dr. Sayuj Krishnan S
```

**Location:** `docs/cover_letter_expansion_template.md` (PRX Life version already prepared)

---

### ✅ 5. Author Information

**Already in Manuscript:**
- [x] Name: Dr. Sayuj Krishnan S, MBBS, DNB (Neurosurgery)
- [x] Affiliation: Consultant Neurosurgeon and Spine Surgeon, Yashoda Hospitals, Malakpet, Hyderabad, India
- [x] Email: dr.sayujkrishnan@gmail.com
- [x] ORCID: https://orcid.org/0009-0009-5523-9979

**Also in:**
- [x] `CITATION.cff` - Complete author information
- [x] `docs/author_information.md` - Centralized author details

---

### ✅ 6. Code and Data Availability

**Repository:**
- [x] URL: `https://github.com/sayujks0071/life`
- [x] Version: v0.1.0 (tagged release)
- [x] `CITATION.cff` file present

**Code Availability Statement (in manuscript):**
- [x] Package name: `spinalmodes` (v0.1.0)
- [x] Key functions listed
- [x] Experiment scripts documented
- [x] Quickstart examples provided

**Data Availability Statement (in manuscript):**
- [x] CSV outputs documented
- [x] Reproducibility instructions provided
- [x] No proprietary data

---

## Final Pre-Submission Steps

### 7. Last-Minute Checks

- [ ] **Spell-check**: Run spell-checker on PDF or LaTeX source
- [ ] **Grammar**: Review for typos and grammatical errors
- [ ] **Consistency**: Verify all notation is consistent throughout
- [ ] **Numbers**: Double-check all numerical values match extracted anchor numbers
- [ ] **Figure quality**: Verify all figures are high-resolution and clear
- [ ] **Bibliography**: Ensure all cited works are in `refs.bib`

### 8. Submission System Preparation

**Information to Have Ready:**
- [x] Manuscript title: "Biological Countercurvature of Spacetime: An Information--Cosserat Framework for Spinal Geometry"
- [x] Abstract (from manuscript)
- [x] Keywords (if required): countercurvature, spinal biomechanics, information-elasticity coupling, Cosserat rods, scoliosis, microgravity, analog gravity
- [x] Author details (see section 5)
- [x] Cover letter text (see section 4)
- [x] GitHub repository URL
- [x] ORCID ID

**Files to Upload:**
- [ ] Main manuscript PDF
- [ ] Source files (if requested)
- [ ] Supplementary materials (if any)

---

## Post-Submission

### 9. After Submission

- [ ] Save submission confirmation/reference number
- [ ] Note expected review timeline (check PRX Life website)
- [ ] Update `PROJECT_STATUS.md` or similar tracking document
- [ ] Consider posting preprint to arXiv (optional)

---

## Quick Reference

**Repository:** https://github.com/sayujks0071/life  
**Version:** v0.1.0  
**ORCID:** https://orcid.org/0009-0009-5523-9979  
**Email:** dr.sayujkrishnan@gmail.com

**Key Documents:**
- Cover letter: `docs/cover_letter_expansion_template.md`
- Author info: `docs/author_information.md`
- Key claims: `docs/key_claims_bullets.md`

---

**Status:** ✅ Ready for LaTeX compilation and final PDF review

**Next Action:** Compile LaTeX → Review PDF → Submit to PRX Life

