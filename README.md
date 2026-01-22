# Biological Countercurvature of Spacetime

**An Information-Cosserat Framework for Spinal Geometry**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## Overview

This repository contains the manuscript, reproducible analysis code, and datasets supporting a theoretical framework that explains how developmental information shapes biological structures against gravity. The work bridges developmental genetics, biomechanics, and differential geometry to understand spinal curvature in normal development, microgravity adaptation, and pathological conditions like scoliosis.

**Key Insight:** Developmental information acts as biological "countercurvature"—modifying the effective spacetime metric experienced by living structures, enabling them to maintain complex geometries against gravitational loading.

📄 **Manuscript:** [manuscript/main.tex](manuscript/main.tex)  
📊 **Figures:** [figures/main/](figures/main/)  
🔬 **Research Modules:** [research/](research/)

---

## Repository Structure

The repository is organized into four main components:

- **`src/`**: Core Python package containing the theoretical model and simulation framework (`spinalmodes`).
- **`research/`**: Self-contained research modules for specific sub-projects (e.g., `alphafold_countercurvature`).
- **`manuscript/`**: LaTeX source for the manuscript and generated figures.
- **`docs/`**: Documentation, hypothesis registry, and project plans.
- **`archive/`**: Legacy code and previous iterations.

```
.
├── manuscript/                   # Camera-ready manuscript
│   ├── main.tex                  # Main manuscript file
│   └── sections/                 # Individual sections
│
├── research/
│   └── alphafold_countercurvature/ # Protein structure analysis pipeline
│       ├── scripts/              # Analysis scripts
│       └── README.md             # Specific instructions
│
├── src/
│   └── spinalmodes/              # Core Cosserat rod model & IEC framework
│       ├── iec.py                # Information-Elasticity Coupling logic
│       └── iec_cli.py            # Command-line interface
│
├── docs/                         # Project documentation
│   ├── notes/                    # Evidence and synthesis notes
│   └── ARCHIVIST_PLAN.md         # Refactoring plan
│
└── archive/                      # Retired code and drafts
```

---

## Quick Start

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

### 2. Running Simulations (Core Model)

The core rod mechanics model is located in `src/spinalmodes`. You can run a demo simulation using the CLI:

```bash
# Run a demo simulation
python -m src.spinalmodes.iec_cli demo
```

This will generate a CSV file and a summary JSON in `outputs/csv/`.

### 3. AlphaFold Analysis Pipeline

For the structural biology analysis pipeline (identifying tension-sensitive proteins), please refer to the specific documentation in:
[research/alphafold_countercurvature/README.md](research/alphafold_countercurvature/README.md)

### 4. Compile Manuscript

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
- **Gravity-dominated**: Structure follows passive gravitational geodesics.
- **Cooperative**: Information and gravity balance (normal physiology).
- **Information-dominated**: Strong geometric distortion (potential pathology).

### 3. Microgravity Persistence
Model predicts spinal curvature **persists in microgravity** (unlike passive structures), with lumbar lordosis decreasing <20% (vs >80% passive prediction).

### 4. Scoliosis as Amplified Asymmetry
Small information field asymmetries (ε_asym ~3-5%) **amplify into scoliotic deformities** in the information-dominated regime.

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

## Contributing

This is an active research project. Contributions welcome in:
1. **Experimental validation** — Connect model to real data
2. **Parameter estimation** — Inverse problem solvers
3. **Extensions** — Growth dynamics, patient-specific modeling

**Contact:** dr.sayujkrishnan@gmail.com

---

## License

- **Code:** MIT License (see [LICENSE](LICENSE))
- **Manuscript:** © 2025 Dr. Sayuj Krishnan S
