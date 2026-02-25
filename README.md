# Metabolic Buckling: An Energy Deficit Window Explains Adolescent Idiopathic Scoliosis

**Formerly: Biological Countercurvature of Spacetime**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Overview

This repository contains the manuscript, reproducible analysis code, and datasets supporting a theoretical framework that explains how developmental information shapes biological structures against gravity. The work bridges developmental genetics, biomechanics, and differential geometry to understand spinal curvature in normal development, microgravity adaptation, and pathological conditions like scoliosis.

**Key Insight:** Adolescent Idiopathic Scoliosis (AIS) is a "Metabolic Buckling" event caused by a mismatch between the scaling laws of mechanical demand ($L^4$) and metabolic supply ($L^2$). This "Energy Deficit Window" forces the spine to buckle into a lower-energy configuration to survive.

📄 **Manuscript:** [manuscript/nature_submission_manuscript.tex](manuscript/nature_submission_manuscript.tex)
📊 **Figures:** [figures/main/](figures/main/)  
🔬 **Core Logic:** [src/spinalmodes/](src/spinalmodes/)

---

## Repository Structure

The repository is organized into clear functional domains:

```
.
├── theory/                       # Theoretical frameworks, derivations, and living hypotheses
│
├── src/                          # Core Python packages
│   ├── spinalmodes/              # Main IEC model and Cosserat implementation
│   └── afcc/                     # Protein structure utilities
│
├── research/                     # Active research modules (e.g., AlphaFold Countercurvature)
│
├── manuscript/                   # Camera-ready manuscript sources
│   ├── nature_submission_manuscript.tex  # Main LaTeX file
│   └── references.bib            # Bibliography
│
├── scripts/                      # Reproducible experiment runners
│   ├── experiments/              # Core simulation runners
│
├── docs/                         # Project documentation and admin plans
├── data/                         # Datasets (tracked and external)
└── archive/                      # Legacy code and prior iterations
```

---

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/sayujks0071/life.git
cd life

# Create virtual environment (Python 3.10+ required)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run a Basic Simulation

To run the minimal Elastica experiment utilizing the Counter-Curvature Rod System:

```bash
python scripts/experiments/experiment_minimal_elastica.py
```

### 3. AlphaFold Counter-Curvature Analysis

For protein structure analysis steps, refer to `research/alphafold_countercurvature/README.md` (if available) or explore the module directly.

---

## Key Results

### 1. S-Curve Emergence

The model demonstrates that the characteristic spinal S-curve emerges as the **energetic ground state** when developmental information (HOX patterning) couples to mechanical properties via the Information-Elasticity Coupling (IEC).

### 2. Phase Diagram

Three distinct regimes identified in the parameter space:

- **Gravity-dominated**: Structure follows passive gravitational geodesics.
- **Cooperative**: Information and gravity balance (normal physiology).
- **Information-dominated**: Strong geometric distortion (potential pathology).

### 3. Microgravity Persistence

Model predicts spinal curvature **persists in microgravity**, identifying a "Stagnant Pool" effect driven by fluid shifts that may drive inflammatory scoliosis.

---

## Citation

If you use this work, please cite:

```bibtex
@article{krishnan2026metabolic_buckling,
  title   = {Metabolic Buckling: An Energy Deficit Window Explains Adolescent Idiopathic Scoliosis},
  author  = {Krishnan, Sayuj},
  journal = {preprint},
  year    = {2026},
  url     = {https://github.com/sayujks0071/life}
}
```

---

## License

This project adopts a dual-licensing model:

- **Source Code**: Licensed under the **MIT License**.
- **Manuscript & Documentation**: Licensed under **CC BY 4.0**.

See [docs/LICENSING.md](docs/LICENSING.md) for full details on component licensing, including third-party and legacy code in `archive/`.
