# TODO: Remaining Work for Publication-Ready IEC Model

**Current Status:** Core computational framework upgraded ✅
**Completion:** ~85% complete
**Remaining Effort:** ~1 week (5-7 days)

---

## 🔴 HIGH PRIORITY (Must Do for Publication)

### 1. Environment Specifications (2 hours) - **DO THIS FIRST**

**Why:** Reproducibility requirement for publication

```bash
# Tasks
- [ ] Create envs/environment.yml
      - Pin exact versions: numpy==1.24.3, scipy==1.11.2, etc.
      - Test: conda env create -f envs/environment.yml

- [ ] Create envs/requirements.txt
      - Pin with hashes: pip-compile --generate-hashes
      - Test: pip install -r envs/requirements.txt

- [ ] Create envs/Dockerfile
      - FROM python:3.10.12-slim
      - Deterministic build (no cache, pinned versions)
      - Test: docker build -t spinalmodes:0.2.0 -f envs/Dockerfile .

- [ ] Update root README.md with quickstart:
      ```
      # Quickstart
      conda env create -f envs/environment.yml
      conda activate spinalmodes
      python test_solver_upgrade.py  # Should pass all 4 tests
      ```
```

**Deliverables:**
- `envs/environment.yml` (Conda)
- `envs/requirements.txt` (pip)
- `envs/Dockerfile` (Docker)
- Updated `README.md`

---

### 2. Generate Publication Figures (3-4 hours)

**Why:** Manuscript needs figures with provenance

#### Figure 1: IEC Discriminators (3-panel)

```bash
# Create analysis/03_iec_discriminators.py
python3 <<'EOF'
# Panel A: IEC-1 node drift vs chi_kappa
# Panel B: IEC-2 amplitude vs chi_E
# Panel C: IEC-3 helical threshold vs ||gradI||
# Output: outputs/figs/fig_iec_discriminators.png (300 DPI)
#         outputs/figs/fig_iec_discriminators.json (provenance)
EOF
```

Tasks:
- [ ] Write `analysis/03_iec_discriminators.py`
- [ ] Run and verify output (18x5 inches, 300 DPI)
- [ ] Check provenance JSON includes git SHA, timestamp, seed
- [ ] Validate with `python tools/validate_figures.py`

#### Figure 2: Solver Validation

```bash
# Create analysis/02_solver_benchmarks.py
# - BVP vs analytical comparison
# - Convergence study (n=50,100,200,400)
# - Error vs. nodes plot
```

Tasks:
- [ ] Write `analysis/02_solver_benchmarks.py`
- [ ] Generate convergence plots
- [ ] Output: `outputs/figs/fig_solver_validation.png`

#### Figure 3: Phase Diagram

```bash
# Create analysis/05_phase_diagrams.py
# - (ΔB, ||∇I||) parameter space
# - Planar vs helical boundary
# - Heatmap with contours
```

Tasks:
- [ ] Write `analysis/05_phase_diagrams.py`
- [ ] Generate phase map
- [ ] Output: `outputs/figs/fig_phase_diagram.png`

**Deliverables:**
- `outputs/figs/fig_iec_discriminators.png` + JSON
- `outputs/figs/fig_solver_validation.png` + JSON
- `outputs/figs/fig_phase_diagram.png` + JSON

---

### 3. Sensitivity Analysis (3-4 hours)

**Why:** Required for parameter robustness claims

```bash
# Install SALib
pip install SALib==1.4.7

# Create analysis/04_sensitivity_analysis.py
# - 4D parameter space: (chi_kappa, chi_E, chi_C, chi_f)
# - Latin Hypercube Sampling (N=1000 runs)
# - Sobol indices: S1 (first-order), ST (total-order)
# - Morris screening for interactions
```

Tasks:
- [ ] Install SALib
- [ ] Write `analysis/04_sensitivity_analysis.py`
- [ ] Run LHS sweep (may take 10-20 minutes)
- [ ] Generate sensitivity bar plots
- [ ] Output: `outputs/figs/fig_sensitivity.png`, `outputs/tables/sensitivity_indices.csv`

**Expected Results:**
- Wavelength most sensitive to χ_E (S1 ~ 0.71)
- Node drift exclusively controlled by χ_κ (S1 ~ 0.94)
- Helical threshold: χ_f and ||∇I|| interaction (S12 ~ 0.52)

**Deliverables:**
- `analysis/04_sensitivity_analysis.py`
- `outputs/figs/fig_sensitivity.png`
- `outputs/tables/sensitivity_indices.csv`

---

### 4. Comprehensive Test Suite (2-3 hours)

**Why:** >80% coverage required for scientific software

```bash
# Create tests/test_model_core.py
pytest tests/test_model_core.py -v --cov=model --cov-report=html
```

Tests to add:
- [ ] `tests/test_model_core.py` (parameter validation, state consistency)
- [ ] `tests/test_solvers.py` (convergence, energy, BC, benchmarks)
- [ ] `tests/test_couplings.py` (IEC-1/2/3 correctness)
- [ ] `tests/test_experiments.py` (parameter sweeps)

Target: **>80% coverage**

**Deliverables:**
- `tests/test_*.py` (4 new test modules)
- `htmlcov/index.html` (coverage report)

---

### 5. Manuscript Assembly (2-3 days)

**Why:** Primary deliverable

#### Option A: LaTeX (Recommended for arXiv/Elsevier)

```bash
mkdir -p manuscript/sections
# Create manuscript/main.tex with journal template
# Sections: abstract, intro, theory, methods, results, discussion
```

Tasks:
- [ ] Download journal template (arXiv, PLOS Comp Bio, etc.)
- [ ] Write `manuscript/main.tex`
- [ ] Create `manuscript/sections/*.tex` (modular)
- [ ] Integrate figures: `\includegraphics{../outputs/figs/fig_*.png}`
- [ ] Complete `manuscript/references.bib`
- [ ] Add reproducibility checklist box
- [ ] Compile: `cd manuscript && pdflatex main.tex`

#### Option B: Markdown + Pandoc (Alternative)

```bash
# Create manuscript/main.md
# Convert: pandoc main.md --bibliography=references.bib -o main.pdf
```

**Content checklist:**
- [ ] Abstract (200 words)
- [ ] Introduction (with biological motivation)
- [ ] Theory (IEC-1/2/3 formulas, governing equations)
- [ ] Methods (BVP solver, validation, parameters)
- [ ] Results (3 main figures + sensitivity)
- [ ] Discussion (connection to Grimes 2016, scoliosis, ciliopathies)
- [ ] Conclusions (testable predictions)
- [ ] References (>30 papers, including Wellik, Grimes, Lefebvre)
- [ ] Reproducibility checklist (seed, Docker, make targets)

**Deliverables:**
- `manuscript/main.pdf` (compiled manuscript)
- `manuscript/references.bib` (>30 entries)
- `manuscript/sections/*.tex` or `manuscript/main.md`

---

## 🟡 MEDIUM PRIORITY (Nice to Have)

### 6. Extended Makefile (30 minutes)

```makefile
# Add to root Makefile

env:
	conda env create -f envs/environment.yml

figures:
	python analysis/02_solver_benchmarks.py
	python analysis/03_iec_discriminators.py
	python analysis/04_sensitivity_analysis.py
	python analysis/05_phase_diagrams.py
	python tools/validate_figures.py

paper:
	cd manuscript && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

all: test figures paper
	@echo "✅ Complete pipeline executed"
```

Tasks:
- [ ] Extend Makefile with new targets
- [ ] Test `make all` end-to-end
- [ ] Document in README

---

### 7. GitHub Actions CI (1-2 hours)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: conda-incubator/setup-miniconda@v2
      - run: conda env create -f envs/environment.yml
      - run: conda activate spinalmodes && pytest tests/ -v
      - run: python test_solver_upgrade.py  # Smoke test
```

Tasks:
- [ ] Create `.github/workflows/ci.yml`
- [ ] Add badge to README: ![CI](https://github.com/user/repo/workflows/CI/badge.svg)
- [ ] Test on push

---

### 8. CITATION.cff (15 minutes)

```yaml
# CITATION.cff
cff-version: 1.2.0
title: "Spinal Modes: Information-Elasticity Coupling Model"
authors:
  - family-names: Krishnan
    given-names: Sayuj
version: 0.2.0
date-released: 2025-11-04
repository-code: "https://github.com/sayujks0071/life"
```

Tasks:
- [ ] Create `CITATION.cff`
- [ ] Test at https://citation-file-format.github.io/cff-initializer-javascript/

---

## 🟢 LOW PRIORITY (Future Work)

### 9. Uncertainty Quantification (1-2 days)

```python
# analysis/06_uncertainty_bands.py
# Bootstrap resampling (N=1000)
# Or Bayesian posterior sampling (PyMC3/Stan)
# Add error bars to all main figures
```

---

### 10. Cosserat Rod Upgrade (1-2 weeks)

```bash
# Option A: PyElastica integration
pip install pyelastica
# Create model/solvers/cosserat_pyelastica.py

# Option B: Custom lightweight Cosserat (6-DOF)
# Create model/solvers/cosserat_custom.py
```

**Benefits:**
- Full 3D torsion and helical modes
- Better scoliosis modeling

**Trade-off:** Heavy dependency (PyElastica) or significant dev time (custom)

---

### 11. Time-Dependent I(s,t) (3-5 days)

```python
# Couple to segmentation clock
# I(s,t) = ⟨cos θ_oscillator(s,t)⟩
# Dynamic simulations with RK4
```

---

## 📋 Quick Reference: File Locations

```
Key files to create/modify:

envs/
├── environment.yml    ← CREATE (Conda)
├── requirements.txt   ← CREATE (pip)
└── Dockerfile         ← CREATE (Docker)

analysis/
├── 02_solver_benchmarks.py     ← CREATE
├── 03_iec_discriminators.py    ← CREATE (Priority!)
├── 04_sensitivity_analysis.py  ← CREATE
└── 05_phase_diagrams.py        ← CREATE

tests/
├── test_model_core.py          ← CREATE
├── test_solvers.py             ← CREATE
├── test_couplings.py           ← CREATE
└── test_experiments.py         ← CREATE

manuscript/
├── main.tex (or main.md)       ← CREATE
├── sections/*.tex              ← CREATE
├── references.bib              ← CREATE/UPDATE
└── figures/ → ../outputs/figs/ (symlink)

outputs/
├── figs/                       ← GENERATE
│   ├── fig_iec_discriminators.png + .json
│   ├── fig_solver_validation.png + .json
│   ├── fig_phase_diagram.png + .json
│   └── fig_sensitivity.png + .json
└── tables/
    └── sensitivity_indices.csv

Root:
├── Makefile                    ← UPDATE (add env, figures, paper, all)
├── CITATION.cff                ← CREATE
├── CHANGELOG.md                ← CREATE
└── README.md                   ← UPDATE (quickstart, docker)

.github/workflows/
└── ci.yml                      ← CREATE (optional but recommended)
```

---

## 🎯 Recommended Execution Order

### Day 1 (4-5 hours)
1. ✅ Environment specs (2h) - **DO THIS FIRST**
2. ✅ Figure 1: IEC discriminators (2-3h)

### Day 2 (4-5 hours)
3. ✅ Figures 2-3: Validation + phase diagram (2-3h)
4. ✅ Sensitivity analysis (2-3h)

### Day 3 (3-4 hours)
5. ✅ Comprehensive test suite (3-4h)

### Days 4-5 (Full days)
6. ✅ Manuscript assembly (2 days)
   - Day 4: Sections (intro, theory, methods, results)
   - Day 5: Discussion, references, polish

### Day 6 (Half day)
7. ✅ Makefile, CI, CITATION.cff (3h)
8. ✅ Final smoke test: `make all` (30min)

### Day 7 (Buffer)
- Polish, review, final checks
- arXiv submission prep (if targeting)

---

## ✅ Definition of Done

Publication-ready when:

- [ ] `make all` succeeds (env → test → figures → paper)
- [ ] All 4+ tests pass (smoke + comprehensive)
- [ ] All figures exist in `outputs/figs/` with provenance JSON
- [ ] `manuscript/main.pdf` compiles
- [ ] Coverage >80%
- [ ] Docker builds: `docker build -t spinalmodes:0.2.0 -f envs/Dockerfile .`
- [ ] README has one-command reproduce: `conda env create -f envs/environment.yml && make all`

---

## 📞 Getting Help

**Stuck on:**
- **Environment issues:** Check Python 3.10+, try `pip install -r envs/requirements.txt` directly
- **Solver convergence:** Increase `max_nodes` or reduce `tol` in BVPSolver
- **Figure generation:** Review `test_solver_upgrade.py` for working examples
- **Manuscript:** See `docs/manuscript/SpinalCountercurvature_IEC.md` (433-line draft)

**Resources:**
- `UPGRADE_COMPLETE_SUMMARY.md` - Full upgrade report
- `UPGRADE_ARCHITECTURE.md` - Design specification
- `project_summary.json` - Complete inventory
- `test_solver_upgrade.py` - Working code examples

---

**Last Updated:** 2025-11-04
**Next Review:** After completing HIGH PRIORITY items (Days 1-3)

**Remember:** Core computational upgrade is DONE ✅. You now have publication-quality solvers. The remaining work is "wrapping" - environments, figures, manuscript. All doable in ~1 week.

🚀 **You've got this!**
