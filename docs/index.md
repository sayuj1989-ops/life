# spinalmodes: Information--Cosserat Framework for Spinal Geometry

The `spinalmodes` package implements the Information-Elasticity Coupling (IEC) framework for modeling biological rods (spines, plant stems, flagella).

## Core Features

- **IEC-Modified Cosserat Rods**: Extension of the Cosserat rod model to include information-dependent rest curvature and stiffness.
- **Spectral Mode Analysis**: Tools for analyzing the eigenvalue spectrum of biological beams in gravity.
- **Geodesic Deviation Metrics**: Quantitative measures for "biological spacetime" distortion.
- **Scoliosis Simulation**: Bifurcation analysis of lateral symmetry breaking.
- **Countercurvature Coupling**: Growth-driven mechanisms opposing gravitational bending.

## Documentation

- [CLI Reference](cli.md) - Command-line interface documentation
- [Figure Guide](figures.md) - Generated figures and interpretation
- [Manuscript](manuscript/SpinalCountercurvature_IEC.md) - Full research manuscript
- [Countercurvature Model Notes](Countercurvature_Model_Notes.md) - Detailed explanation of growth opposing gravity

## Overview

This project implements a computational framework for studying biological counter-curvature and Information-Elasticity Coupling (IEC) in spinal development. The model integrates:

- **Developmental genetics:** HOX/PAX expression, segmentation clocks
- **Biomechanics:** Beam/Cosserat rod models, buckling analysis
- **Clinical relevance:** Scoliosis as symmetry-breaking phenomenon

## Three IEC Mechanisms

### IEC-1: Target Curvature Bias (χ_κ)
Information gradients shift neutral geometric states, causing pattern shifts without wavelength changes.

### IEC-2: Constitutive Bias (χ_E, χ_C)
Information levels modulate tissue stiffness and damping, affecting deformation amplitude and dynamics.

### IEC-3: Active Moments (χ_f)
Information gradients drive active cellular forces, reducing helical instability thresholds.

## Quick Start

```bash
# Install dependencies
poetry install

# Run demo
poetry run spinalmodes iec demo --out-prefix outputs/csv/demo

# Generate phase diagram
poetry run spinalmodes iec phase \
  --delta-b 0.0:0.2:41 \
  --gradI 0.0:0.1:21 \
  --out-csv outputs/csv/phase_map.csv \
  --out-fig outputs/figs/phase.png

# Validate outputs
poetry run python tools/validate_figures.py
```

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
from spinalmodes.iec import solve_beam_static
from spinalmodes.countercurvature import make_uniform_grid

# Define grid
s = make_uniform_grid(0.4, 100)

# Solve for equilibrium
# ...
```

## Reference

If you use this code, please cite:
S. Krishnan (2025) "Biological Countercurvature of Spacetime"
