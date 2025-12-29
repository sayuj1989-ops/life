# Biological Countercurvature of Spacetime

**An Information-Cosserat Framework for Spinal Geometry**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://img.shields.io/badge/DOI-10.0000%2Fplaceholder-blue.svg)](https://doi.org/10.0000/placeholder-doi)

---

## Overview

This repository contains the manuscript, reproducible analysis code, and datasets supporting a theoretical framework that explains how developmental information shapes biological structures against gravity. The work bridges developmental genetics, biomechanics, and differential geometry to understand spinal curvature in normal development, microgravity adaptation, and pathological conditions like scoliosis.

**Key Insight:** Developmental information acts as biological "countercurvature"—modifying the effective spacetime metric experienced by living structures, enabling them to maintain complex geometries against gravitational loading.

📄 **Manuscript:** [manuscript/main.tex](manuscript/main.tex)  
📊 **Figures:** [figures/main/](figures/main/)  
🔬 **Analysis Code:** [alphafold_analysis/](alphafold_analysis/)

---

## Repository Structure

```
.
├── manuscript/                   # Camera-ready manuscript
│   ├── main.tex                  # Main manuscript file
│   ├── sections/                 # Individual sections
│   ├── numbers/                  # Extracted numbers for claims
│   ├── extended_data/            # Extended data tables & figures
│   └── references.bib            # Complete bibliography
│
├── figures/
│   ├── main/                     # Final publication-ready figures (tracked)
│   ├── extended_data/            # Supplementary figures (tracked)
│   └── src/                      # Plotting scripts
│
├── data/
│   ├── derived/                  # Small derived datasets for claims (tracked)
│   └── external/                 # Large downloads (NOT tracked)
│
├── alphafold_analysis/           # AlphaFold DB structure analysis
├── scripts/                      # CLI entry scripts
├── src/                          # Core Python package
├── tests/                        # Unit tests
│
└── docs/
    ├── notes/                    # Integration guides, setup docs
    └── archive/                  # Historical drafts, reviews
```

---

## Quick Start: Reproducibility

### 1. Installation

```bash
# Clone repository
git clone https://github.com/sayujks0071/life.git
cd life

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Complete Analysis Pipeline

**One-command reproducibility:**

```bash
make alphafold-all
```

This executes:
- `alphafold-data`: Build AlphaFold structure dataset index
- `alphafold-analyze`: Analyze BCC-related protein structures
- `alphafold-figs`: Generate publication figures
- `alphafold-numbers`: Extract quantitative numbers for manuscript

**Individual steps:**

```bash
# Step 1: Build dataset index
make alphafold-data

# Step 2: Run structural analysis
make alphafold-analyze

# Step 3: Generate figures
make alphafold-figs

# Step 4: Extract manuscript numbers
make alphafold-numbers
```

### 3. Compile Manuscript

```bash
cd manuscript
make all
# Output: manuscript/main.pdf
```

---

## Key Results

### 1. S-Curve Emergence from Information Patterning

The model demonstrates that the characteristic spinal S-curve emerges as the **energetic ground state** when developmental information (HOX patterning) couples to mechanical properties.

### 2. Phase Diagram of Countercurvature Regimes

Three distinct regimes identified in (χ_κ, g) parameter space:

| Regime | D̂_geo | Description |
|--------|-------|-------------|
| **Gravity-dominated** | < 0.1 | Structure follows passive gravitational geodesics |
| **Cooperative** | 0.1–0.3 | Information and gravity balance (normal physiology) |
| **Information-dominated** | > 0.3 | Strong geometric distortion (potential pathology) |

### 3. Microgravity Persistence

Model predicts spinal curvature **persists in microgravity** (unlike passive structures):
- D̂_geo remains >0.15 even as g → 0
- Lumbar lordosis decreases <20% (vs >80% passive prediction)

### 4. Scoliosis as Amplified Asymmetry

Small information field asymmetries (ε_asym ~3-5%) **amplify into scoliotic deformities** in information-dominated regime.

---

## Citation

If you use this work, please cite:

```bibtex
@article{krishnan2025biological_countercurvature,
  title   = {Biological Countercurvature of Spacetime: An Information--Cosserat Framework for Spinal Geometry},
  author  = {Krishnan, Sayuj},
  journal = {preprint},
  year    = {2025},
  url     = {https://github.com/sayujks0071/life}
}
```

See [CITATION.cff](CITATION.cff) for structured citation metadata.

---

## Dependencies

### Core Requirements
- **Python:** 3.8+
- **NumPy:** 1.20+
- **SciPy:** 1.7+
- **Matplotlib:** 3.4+
- **PyElastica:** 0.3.0+ (Cosserat rod mechanics)

See [requirements.txt](requirements.txt) for complete list.

### LaTeX (for manuscript compilation)
- **TeX Live** or **MikTeX**
- Required packages: amsmath, tikz, natbib, booktabs, siunitx

---

## Project Status

**Current Status:** Research code and manuscript for publication

**Key Features:**
- ✅ Full theoretical framework (Information-Elasticity Coupling)
- ✅ Numerical implementation (Cosserat rod solver)
- ✅ Phase diagram analysis
- ✅ Testable predictions
- ✅ Reproducible analysis pipeline

---

## Contributing

This is an active research project. Contributions welcome in:
1. **Experimental validation** — Connect model to real data
2. **Parameter estimation** — Inverse problem solvers
3. **Extensions** — Growth dynamics, patient-specific modeling
4. **Documentation** — Tutorials, examples

**Contact:** dr.sayujkrishnan@gmail.com

---

## License

- **Code:** MIT License (see [LICENSE](LICENSE))
- **Manuscript:** © 2025 Dr. Sayuj Krishnan S

---

## Acknowledgments

- **PyElastica Team** — Open-source Cosserat rod framework
- **AlphaFold DB** — Protein structure data
- **Yashoda Hospitals** — Institutional support

---

**Last Updated:** December 29, 2025  
**Version:** 1.0.0  
**Status:** Publication-ready
