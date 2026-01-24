# spinalmodes: Information-Cosserat Framework for Spinal Geometry

The `spinalmodes` package implements the Information-Elasticity Coupling (IEC) framework for modeling biological rods (spines, plant stems, flagella). It provides tools for simulating how bioelectric and biochemical information fields modulate the mechanical properties of growing tissues.

## Documentation Index

### Theory & Formalism
- **[Formalism 01: The Plumb-Line Number](theory/formalism_01.md)**: Mathematical derivation of the dimensionless numbers governing spinal alignment in gravity.
- **[Scoliosis Mechanism Map](scoliosis_mechanism_map.md)**: Concept map linking microgravity, fluid dynamics, and mechanotransduction to curvature.

### Implementation & API
- **[Public API Reference](public_api_reference.md)**: Stable API for constructing information fields and running countercurvature simulations.
- **[Implementation Summary](countercurvature_implementation_summary.md)**: Overview of the codebase architecture and key algorithms.
- **[CLI Reference](cli.md)**: Command-line tools for running simulations and analysis.

### Research & Hypotheses
- **[Hypothesis Register](hypothesis_register.md)**: Catalogue of testable predictions regarding microgravity-induced scoliosis.
- **[Candidate Registry](candidate_registry.md)**: List of gene/protein candidates identified by the AlphaFold-Countercurvature pipeline.

### Simulations & Data
- **[Simulations Status](simulations_status.md)**: Log of simulation runs, parameter sweeps, and outcomes.
- **[Data Linkage Plan](DATA_LINKAGE_PLAN.md)**: Strategy for connecting simulation outputs with biological datasets.

### Project Management
- **[Project Plan](PROJECT_PLAN.md)**: High-level roadmap and research goals.
- **[Archivist Plan](ARCHIVIST_PLAN.md)**: Daily refactoring and code quality tracking.
- **[Performance Summary](PERFORMANCE_SUMMARY.md)**: Benchmarks and optimization tracking.

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
import numpy as np
from spinalmodes.countercurvature import make_uniform_grid, InfoField1D

# Define grid
s = make_uniform_grid(0.4, 100)
# Create an information field
density = np.exp(-((s - 0.2)**2) / 0.01)
info = InfoField1D.from_array(s, density)
```

## Reference

If you use this code, please cite:
S. Krishnan (2025) "Biological Countercurvature of Spacetime"
