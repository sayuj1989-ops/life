# Biological Countercurvature of Spacetime

**An Information-Cosserat Framework for Spinal Geometry**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Overview

This repository contains the manuscript, reproducible analysis code, and datasets supporting a theoretical framework that explains how developmental information shapes biological structures against gravity. The work bridges developmental genetics, biomechanics, and differential geometry to understand spinal curvature in normal development, microgravity adaptation, and pathological conditions like scoliosis.

**Key Insight:** Developmental information acts as biological "countercurvature"—modifying the effective spacetime metric experienced by living structures, enabling them to maintain complex geometries against gravitational loading.

📄 **Manuscript:** [manuscript/main.tex](manuscript/main.tex)  
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
│   └── alphafold/                # Protein structure utilities
│
├── research/                     # Active research modules (e.g., AlphaFold Countercurvature)
│
├── manuscript/                   # Camera-ready manuscript sources
│   ├── main.tex                  # Main LaTeX file
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

### 2. Run the Analysis Pipeline

To run the master reproducing script that executes the core analyses (Integrated Simulation, Energy Deficit Bifurcation, Thermodynamic Cost):

```bash
python main.py
```

Outputs will be saved dynamically to the `outputs/` directory (or `../results` if run via Code Ocean).

### 3. Code Ocean Deployment

The repository is configured for submission via Code Ocean. Execute the full environment run using the provided entry point:

```bash
bash run.sh
```

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
@article{krishnan2025biological_countercurvature,
  title   = {Biological Countercurvature of Spacetime: An Information--Cosserat Framework for Spinal Geometry},
  author  = {Krishnan, Sayuj},
  journal = {preprint},
  year    = {2025},
  url     = {https://github.com/sayujks0071/life}
}
```

---

## License

This project adopts a dual-licensing model:

- **Source Code**: Licensed under the **MIT License**.
- **Manuscript & Documentation**: Licensed under **CC BY 4.0**.

See [docs/LICENSING.md](docs/LICENSING.md) for full details on component licensing, including third-party and legacy code in `archive/`.
