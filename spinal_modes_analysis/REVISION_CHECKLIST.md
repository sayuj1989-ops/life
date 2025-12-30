# Nature Revision Checklist

Quick reference for remaining tasks before resubmission.

---

## 🔴 CRITICAL (Must Complete Before Resubmission)

- [ ] **Figure 1: Gene-to-Geometry Mapping**
  - [ ] Run: `python life/src/spinalmodes/experiments/countercurvature/generate_figure1_gene_geometry.py`
  - [ ] Verify output: `manuscript/fig_gene_geometry.pdf`
  - [ ] Check Results section text matches figure content
  - ⏱️ Est. time: 1 hour

- [ ] **Figure 2: Mode Spectrum Analysis**
  - [ ] Run: `python life/src/spinalmodes/experiments/countercurvature/generate_figure2_mode_spectrum.py`
  - [ ] Verify output: `manuscript/fig_mode_spectrum.pdf`
  - [ ] Check eigenvalue spectrum shows mode crossing
  - ⏱️ Est. time: 2 hours

- [ ] **Figure 5: Scoliosis Emergence**
  - [ ] Decide: Run simulation OR mark as "predicted"?
  - [ ] If simulating: Run scoliosis experiment with high χ_κ
  - [ ] If predicting: Add note in caption and Results text
  - [ ] Generate figure: 3 panels (asymmetric I(s), 3D curves, Cobb vs χ_κ)
  - ⏱️ Est. time: 3 hours (simulation) OR 30 min (clarification)

- [ ] **Clinical Angle Comparison**
  - [ ] Run simulation with Table 1 parameters
  - [ ] Compute sagittal Cobb angles: cervical, thoracic, lumbar
  - [ ] Add Results paragraph: "Model predicts [X±Y°, A±B°, C±D°] vs clinical [ranges]"
  - [ ] Add comparison to Discussion
  - ⏱️ Est. time: 4 hours

- [ ] **Manuscript Compilation Check**
  - [ ] `cd manuscript && pdflatex main.tex`
  - [ ] `bibtex main`
  - [ ] `pdflatex main.tex` (2x)
  - [ ] Verify: All figures appear, no citation errors, no overfull hboxes
  - ⏱️ Est. time: 30 min

---

## 🟡 IMPORTANT (Strengthen Impact)

- [ ] **Uncertainty Quantification**
  - [ ] Monte Carlo: Vary parameters ±10%
  - [ ] Report: $\widehat{D}_{\mathrm{geo}}$ = X ± Y across (χ_κ, g) space
  - [ ] Add error bars to Phase Diagram
  - ⏱️ Est. time: 1 day

- [ ] **Convergence Analysis**
  - [ ] Run simulations: n = 25, 50, 75, 100, 150, 200 elements
  - [ ] Plot: $\widehat{D}_{\mathrm{geo}}$ vs n
  - [ ] Add Supplementary Figure S1
  - ⏱️ Est. time: 4 hours

- [ ] **Eigenvalue Spectrum (Fig 2 enhancement)**
  - [ ] Solve eigenvalue problem: Eq. 3
  - [ ] Plot: λ_n vs χ_κ showing ground state transition
  - [ ] Identify χ_κ,crit for S-mode selection
  - ⏱️ Est. time: 2 days (if solver not implemented)

---

## 🟢 RECOMMENDED (Polish)

- [ ] **Code Reproducibility**
  - [ ] Create: `requirements.txt` with versions
  - [ ] OR: `environment.yml` for conda
  - [ ] Document: Python version, OS tested
  - ⏱️ Est. time: 30 min

- [ ] **Unit Tests**
  - [ ] Install pytest
  - [ ] Write tests: `test_info_fields.py`, `test_coupling.py`, `test_metrics.py`
  - [ ] CI: Add GitHub Actions for automated testing
  - ⏱️ Est. time: 1 day

- [ ] **API Documentation**
  - [ ] Install Sphinx
  - [ ] Configure: `docs/conf.py`
  - [ ] Generate: HTML docs from docstrings
  - [ ] Host: ReadTheDocs or GitHub Pages
  - ⏱️ Est. time: 4 hours

- [ ] **Supplementary Material**
  - [ ] Create: `supplement.tex`
  - [ ] Include: Validation benchmarks, derivations, convergence
  - [ ] Move: Detailed code snippets from main text
  - ⏱️ Est. time: 1 day

---

## 📝 Writing Tasks

- [ ] **Cover Letter**
  - [ ] Address each reviewer's main concerns explicitly
  - [ ] Highlight: Figures now complete, clinical comparison added
  - [ ] Thank: Reviewers for constructive feedback
  - ⏱️ Est. time: 2 hours

- [ ] **Response to Reviewers Document**
  - [ ] Format: Point-by-point response
  - [ ] For each comment: Quote → Response → Location in manuscript
  - [ ] Highlight: Text added in blue/italics
  - ⏱️ Est. time: 3 hours

- [ ] **Proofreading**
  - [ ] Check: Math notation consistency
  - [ ] Check: Figure references (Fig. X vs Figure X)
  - [ ] Check: Citation format
  - [ ] Check: Typos and grammar
  - ⏱️ Est. time: 2 hours

---

## 📊 Quality Checks

### Before Submission:
- [ ] All figures referenced in text exist as files
- [ ] All citations in text exist in references.bib
- [ ] Table 1 values match code parameters
- [ ] Equation numbers sequential and referenced correctly
- [ ] Supplementary Material uploaded (if applicable)
- [ ] Code repository public and functional
- [ ] Zenodo DOI obtained for code/data archive

### Sanity Checks:
- [ ] Predicted spinal angles within ±50% of clinical norms
- [ ] $\widehat{D}_{\mathrm{geo}}$ values between 0 and 1 (by definition)
- [ ] Phase diagram shows three distinct regimes
- [ ] Microgravity simulation shows persistence (not collapse)

---

## 📅 Timeline Tracker

| Date | Task | Status | Notes |
|------|------|--------|-------|
| Dec 17 | Peer review complete | ✅ | |
| Dec 17 | Theory revisions | ✅ | Added metric justification, D_geo definition |
| Dec 17 | Methods revisions | ✅ | Added parameter table, I(s) specification |
| Dec 17 | Discussion revisions | ✅ | Alternative mechanisms, quantitative predictions |
| Dec 17 | Bibliography | ✅ | Added 8 missing references |
| Dec 18 | Generate Figures 1,2,5 | ⏳ | **Start here** |
| Dec 18 | Clinical comparison | ⏳ | |
| Dec 19 | Manuscript compilation | ⏳ | |
| Dec 19 | Cover letter | ⏳ | |
| Dec 20 | **RESUBMIT** | 🎯 | Target date |

---

## 🚀 Quick Start Commands

### Generate Figures
```bash
cd /Users/mac/LIFE
source .venv/bin/activate  # if using virtual env

# Figure 1
python life/src/spinalmodes/experiments/countercurvature/generate_figure1_gene_geometry.py

# Figure 2
python life/src/spinalmodes/experiments/countercurvature/generate_figure2_mode_spectrum.py

# Check outputs
ls -lh manuscript/fig_*.pdf
```

### Compile Manuscript
```bash
cd /Users/mac/LIFE/manuscript
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
open main.pdf
```

### Run Clinical Comparison
```bash
# Create new script
cat > manuscript_clinical_angles.py << 'EOF'
"""Compute model-predicted spinal angles for clinical comparison."""
import numpy as np
from spinalmodes.countercurvature import run_spine_simulation
from spinalmodes.utils.metrics import compute_sagittal_cobb_angles

# Run with Table 1 parameters
result = run_spine_simulation(
    length=0.40,
    chi_kappa=0.05,  # cooperative regime
    chi_E=0.10,
    g=1.0  # Earth gravity
)

# Compute angles
angles = compute_sagittal_cobb_angles(result.centerline, result.s)
print(f"Cervical lordosis: {angles['cervical']:.1f}°")
print(f"Thoracic kyphosis: {angles['thoracic']:.1f}°")
print(f"Lumbar lordosis: {angles['lumbar']:.1f}°")
EOF

python manuscript_clinical_angles.py
```

---

## 📞 Need Help?

- **Figure generation failing?** Check that PyElastica is installed: `pip list | grep elastica`
- **LaTeX errors?** Install missing packages: `tlmgr install <package>`
- **Parameter confusion?** See [manuscript/sections/methods.tex Table 1](manuscript/sections/methods.tex#L13-L51)
- **Citation errors?** Run `bibtex main` and check `.blg` file for details

---

## ✅ Definition of Done

**Manuscript is ready for resubmission when:**

1. All 5 figures present and referenced correctly
2. Clinical angle comparison in Results (with numbers)
3. PDF compiles without errors
4. All citations resolve (no "?" in text)
5. Cover letter addresses specific reviewer points
6. Code repository link functional

**Stretch goal (for high-impact journals):**
- Uncertainty bars on key metrics
- Convergence analysis in supplement
- Comprehensive documentation

---

**Last updated:** December 17, 2025
**Status:** 7/15 critical items complete (47%)
**Estimated completion:** December 20, 2025 (3 days)
