# spinalmodes: Information--Cosserat Framework for Spinal Geometry

The `spinalmodes` package implements the Information-Elasticity Coupling (IEC) framework for modeling biological rods (spines, plant stems, flagella).

## Core Features

- **IEC-Modified Cosserat Rods**: Extension of the Cosserat rod model to include information-dependent rest curvature and stiffness.
- **Spectral Mode Analysis**: Tools for analyzing the eigenvalue spectrum of biological beams in gravity.
- **Geodesic Deviation Metrics**: Quantitative measures for "biological spacetime" distortion.
- **Scoliosis Simulation**: Bifurcation analysis of lateral symmetry breaking.

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
