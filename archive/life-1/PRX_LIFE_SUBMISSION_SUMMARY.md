# PRX Life Submission - Complete File Guide

**Date:** 2025-11-18  
**Status:** ✅ Ready to Submit  
**Zenodo DOI:** 10.5281/zenodo.17634760  
**GitHub Release:** v0.1.0

---

## 🎯 Quick Start: What You Need Right Now

### **Primary Submission Files** (Copy-Paste Ready)

1. **Data & Code Availability Statement**
   - **File:** `PRX_LIFE_DATA_CODE_BLURB.md`
   - **Use:** Copy Version 1 (full) or Version 2 (concise) into submission form
   - **Status:** ✅ Updated with Zenodo DOI

2. **Suggested Reviewers**
   - **File:** `SUGGESTED_REVIEWERS_PRX_LIFE.md`
   - **Use:** Copy the 5 reviewers from "Bottom Line" section
   - **Status:** ✅ Ready (5 reviewers, all tiers covered)

3. **Manuscript PDF**
   - **File:** Compile `manuscript/main_countercurvature.tex`
   - **Instructions:** See `manuscript/COMPILE_INSTRUCTIONS.md`
   - **Status:** ⚠️ Need to compile (use Overleaf or local LaTeX)

4. **Figures**
   - **Location:** `manuscript/fig_*.pdf` (5 files)
   - **Status:** ✅ All present

---

## 📋 Complete File Inventory

### **Submission Guides** (Choose One)

| File | Purpose | When to Use |
|------|---------|-------------|
| `PRX_LIFE_READY.md` | **Comprehensive guide** (278 lines) | Full step-by-step walkthrough |
| `SUBMIT_NOW.md` | **Ultra-compact checklist** (165 lines) | Quick reference, already done most steps |
| `SHIP_IT.md` | **Detailed submission guide** | Alternative comprehensive version |

**Recommendation:** Use `PRX_LIFE_READY.md` as your primary guide.

---

### **Copy-Paste Content Files**

| File | Content | Submission Form Field |
|------|---------|---------------------|
| `PRX_LIFE_DATA_CODE_BLURB.md` | Data/code availability (3 versions) | "Data Availability" |
| `SUGGESTED_REVIEWERS_PRX_LIFE.md` | 5 reviewers with emails | "Suggested Reviewers" |

---

### **Manuscript Files**

| File | Status | Notes |
|------|--------|-------|
| `manuscript/main_countercurvature.tex` | ✅ Final | LaTeX source |
| `manuscript/refs.bib` | ✅ Complete | Bibliography |
| `manuscript/fig_countercurvature_panelA-D.pdf` | ✅ Ready | 4 panels for Fig 1 |
| `manuscript/fig_phase_diagram_scoliosis.pdf` | ✅ Ready | Fig 2 phase diagram |
| `manuscript/COMPILE_INSTRUCTIONS.md` | ✅ Updated | How to compile PDF |

---

### **Quality Control Files**

| File | Purpose |
|------|---------|
| `MANUSCRIPT_PREVIEW.md` | Human-readable preview of full manuscript |
| `FINAL_PDF_CHECK.md` | Pre-submission checklist for compiled PDF |
| `FINAL_PRE_SUBMISSION_SUMMARY.md` | Repository status summary |

---

## 🚀 Submission Checklist (Final Steps)

### ✅ Already Complete

- [x] GitHub repository public
- [x] Release v0.1.0 tagged and pushed
- [x] Zenodo DOI obtained: 10.5281/zenodo.17634760
- [x] CITATION.cff updated with DOI
- [x] All figures generated (5 PDFs)
- [x] Manuscript LaTeX source final
- [x] Bibliography complete
- [x] Code tested and working
- [x] Data availability statement ready
- [x] Reviewers list prepared

### ⚠️ Remaining Tasks

- [ ] **Compile manuscript PDF** (30 min)
  - Option A: Upload to Overleaf → Compile
  - Option B: Local LaTeX → `pdflatex` + `bibtex` (3 passes)
  - Verify: All figures appear, citations resolve, no errors

- [ ] **Final PDF check** (15 min)
  - Use `FINAL_PDF_CHECK.md` checklist
  - Verify figure quality, equation numbering, references

- [ ] **Submit to PRX Life** (30 min)
  - Portal: https://journals.aps.org/prxlife/authors
  - Upload: PDF + figures (if separate upload)
  - Paste: Data availability from `PRX_LIFE_DATA_CODE_BLURB.md`
  - Paste: 5 reviewers from `SUGGESTED_REVIEWERS_PRX_LIFE.md`
  - Fill: Cover letter, keywords, conflicts

---

## 📝 What to Copy-Paste Where

### **1. Data & Code Availability**

**Source:** `PRX_LIFE_DATA_CODE_BLURB.md` → Version 1 (Full Statement)

**Paste into:** PRX Life submission form → "Data Availability" field

**Content:**
```
All code, data, and analysis scripts required to reproduce the results in this manuscript are openly available:

Code Repository:
https://github.com/sayujks0071/life (archived at Zenodo: 10.5281/zenodo.17634760)

Version: v0.1.0

Software: The spinalmodes Python package (MIT License) implements:
- Information-Elasticity Coupling (IEC) beam and Cosserat rod solvers
- Biological countercurvature metric and geodesic curvature deviation (D̂_geo)
- Scoliosis metrics (S_lat, Cobb-like angles)
- Full integration with PyElastica for 3D Cosserat rod dynamics

Data: All numerical results are regenerable by running experiment scripts in src/spinalmodes/experiments/countercurvature/ with default parameters. Pre-computed experiment outputs (curvature profiles, metrics, phase diagram data) are included in outputs/ and documented in docs/manuscript_code_data_availability.md.

Reproducibility: Minimal working examples are provided in examples/quickstart.py and examples/quickstart.ipynb. Full reproduction requires Python 3.10+, NumPy, SciPy, Matplotlib, and PyElastica (all listed in pyproject.toml). Typical runtime: 5-30 minutes per experiment on a standard workstation.

Contact: For questions about code or data, contact Dr. Sayuj Krishnan (dr.sayujkrishnan@gmail.com) or open an issue on the GitHub repository.
```

---

### **2. Suggested Reviewers**

**Source:** `SUGGESTED_REVIEWERS_PRX_LIFE.md` → "Bottom Line" section

**Paste into:** PRX Life submission form → "Suggested Reviewers" (5 reviewers)

**Format (one per reviewer):**
```
Reviewer 1:
Name: Mattia Gazzola
Email: mgazzola@illinois.edu
Institution: University of Illinois Urbana-Champaign
Expertise: Cosserat rod mechanics, soft matter mechanics, PyElastica

Reviewer 2:
Name: Diane Grimes
Email: dgrimes@kumc.edu
Institution: University of Kansas Medical Center
Expertise: Zebrafish models of scoliosis, cilia-CSF-spine axis

Reviewer 3:
Name: Alain Goriely
Email: goriely@maths.ox.ac.uk
Institution: University of Oxford
Expertise: Mathematical biology, growth mechanics, morphoelasticity

Reviewer 4:
Name: Carol Wise
Email: carolw@mail.nih.gov
Institution: NIH/NHGRI
Expertise: Genetic basis of idiopathic scoliosis

Reviewer 5:
Name: Carlos Barceló
Email: carlos@iaa.es
Institution: Instituto de Astrofísica de Andalucía (CSIC)
Expertise: Analog gravity models, emergent spacetime
```

---

### **3. Keywords** (Suggested)

- biological countercurvature
- information-elasticity coupling
- spinal biomechanics
- scoliosis
- analog gravity
- Cosserat rod mechanics
- geodesic curvature
- developmental patterning

---

### **4. Cover Letter** (Brief Template)

**Source:** `docs/cover_letter_template.md` (if exists) or create from:

```
Dear PRX Life Editors,

We submit our manuscript "Biological Countercurvature of Spacetime: An Information--Cosserat Framework for Spinal Geometry" for consideration as a Research Article.

This work presents a quantitative framework that interprets spinal curvature as information-selected modes in an effective gravitational geometry, providing a unified model for normal sagittal curvature and scoliosis-like lateral deviations. The framework combines Information-Elasticity Coupling (IEC) with three-dimensional Cosserat rod mechanics, treating the spine in gravity as an analog spacetime.

Key contributions:
- A biological metric derived from information fields that quantifies countercurvature
- A phase diagram mapping gravity-dominated, cooperative, and information-dominated regimes
- Predictions of scoliosis-like symmetry breaking in the information-dominated regime
- Full computational implementation with open-source code (GitHub + Zenodo DOI)

This work bridges theoretical physics (analog gravity), computational mechanics (Cosserat rods), and developmental biology (HOX/PAX patterning, cilia-CSF flow), making it well-suited for PRX Life's interdisciplinary scope.

All code and data are openly available at https://github.com/sayujks0071/life (Zenodo: 10.5281/zenodo.17634760).

We suggest the following reviewers [list 3-5 from SUGGESTED_REVIEWERS_PRX_LIFE.md].

Thank you for your consideration.

Sincerely,
Dr. Sayuj Krishnan S
```

---

## 🔗 Important Links

- **PRX Life Submission Portal:** https://journals.aps.org/prxlife/authors
- **GitHub Repository:** https://github.com/sayujks0071/life
- **Zenodo Archive:** https://zenodo.org/records/17634760
- **GitHub Release:** https://github.com/sayujks0071/life/releases/tag/v0.1.0

---

## 📊 Submission Status Summary

| Component | Status | File/URL |
|-----------|--------|----------|
| Manuscript LaTeX | ✅ Ready | `manuscript/main_countercurvature.tex` |
| Bibliography | ✅ Complete | `manuscript/refs.bib` |
| Figures (5 PDFs) | ✅ Generated | `manuscript/fig_*.pdf` |
| Manuscript PDF | ⚠️ Need to compile | See `manuscript/COMPILE_INSTRUCTIONS.md` |
| Code Repository | ✅ Public | https://github.com/sayujks0071/life |
| Zenodo DOI | ✅ Assigned | 10.5281/zenodo.17634760 |
| Data Statement | ✅ Ready | `PRX_LIFE_DATA_CODE_BLURB.md` |
| Reviewers List | ✅ Ready | `SUGGESTED_REVIEWERS_PRX_LIFE.md` |
| Citation Metadata | ✅ Updated | `CITATION.cff` |

---

## ⏱️ Estimated Time to Submit

- **Compile PDF:** 30 minutes (Overleaf) or 15 minutes (local LaTeX)
- **Final PDF check:** 15 minutes
- **Fill submission form:** 30 minutes
- **Total:** ~1.5 hours

---

## 🎯 Next Action

**Right now:** Compile the manuscript PDF using Overleaf or local LaTeX.

**Then:** Use this guide to fill out the PRX Life submission form.

**You're 90% done!** Just need to compile PDF and submit. 🚀

---

**Last Updated:** 2025-11-18  
**Contact:** dr.sayujkrishnan@gmail.com

