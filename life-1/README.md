# Spinal Modes: Biological Countercurvature of Spacetime

[![Status](https://img.shields.io/badge/status-publication_ready-green.svg)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**An Information–Cosserat Framework for Spinal Geometry**

This repository contains the reference implementation for the **Information-Elasticity Coupling (IEC)** model of spinal geometry. It treats the spine in gravity as an analog to a body in curved spacetime, where biological information (genetic patterning, neural control) modifies the effective metric.

## Key Features

- **IEC Beam Solver:** Coupled ODEs for information-driven curvature
- **Countercurvature Metric:** $g_{\mathrm{eff}}(s)$ derived from information fields $I(s)$
- **Geodesic Deviation:** Quantify "distance" between gravity-selected and information-selected curvatures
- **Scoliosis Analysis:** Phase diagrams for symmetry breaking (Fig 2)
- **PyElastica Bridge:** Full 3D Cosserat rod simulations

## Quickstart

### 1. Install

```bash
pip install -r envs/requirements.txt
```

### 2. Run Microgravity Experiment (Fig 1D)

```bash
python -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation --quick
```

### 3. Run Full Experiment Suite

```bash
./run_experiments.sh
```

### 4. Generate Manuscript Figures

```bash
# Spine modes vs. gravity (Fig 1A-C)
python -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity

# Phase diagram (Fig 2)
python -m spinalmodes.experiments.countercurvature.experiment_phase_diagram
```

## Installation (Detailed)

### Option 1: Conda (Recommended)

```bash
# Create environment from spec
conda env create -f envs/environment.yml
conda activate spinalmodes

# Run tests
pytest tests/
```

### Option 2: pip

```bash
# Install dependencies
pip install -r envs/requirements.txt

# Run tests
pytest tests/
```

### Option 3: Docker

```bash
# Build container
docker build -t spinalmodes:0.1.0 -f envs/Dockerfile .

# Run experiments
docker run --rm -v $(pwd):/workspace -w /workspace spinalmodes:0.1.0 \
    python -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation
```

## Overview

This package implements:
- **IEC Model**: Three coupling mechanisms linking information fields to mechanical properties
  - IEC-1: Target curvature bias (χ_κ)
  - IEC-2: Constitutive bias (χ_E, χ_C)
  - IEC-3: Active moment (χ_f)
- **Beam/Cosserat Solvers**: For spinal mechanics with coupled oscillators
- **Phase Analysis**: Parameter sweeps, node drift, helical threshold computations
- **Figure Generation**: Publication-ready figures with validation

## Installation (Alternative: Poetry)

```bash
# Install dependencies (development environment)
poetry install

# Verify installation
poetry run spinalmodes --help
```

> **For reproducibility**, prefer Conda/pip/Docker (see Quickstart above).

## Quick Start (Using CLI)

```bash
# Run IEC demo
poetry run spinalmodes iec demo --out-prefix outputs/csv/iec_demo

# Generate phase diagram
poetry run spinalmodes iec phase \
  --delta-b 0.0:0.2:41 \
  --gradI 0.0:0.1:21 \
  --out-csv outputs/csv/iec_phase_map.csv \
  --out-fig outputs/figs/fig_iec_phase.png

# Node drift analysis
poetry run spinalmodes iec node-drift \
  --I-mode step \
  --chi-kappa 0.04 \
  --out-fig outputs/figs/fig_iec_node_drift.png
```

## 3-command quickstart (countercurvature)

```bash
python examples/quickstart.py
python -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity --quick
python -m spinalmodes.experiments.countercurvature.experiment_phase_diagram --quick
```

## One-command reproduce

```bash
python -m pip install -e ".[dev]"
make all  # env + tests + figures + (optional) paper
```

### Build & install wheel

```bash
python -m pip install build
make build && make dist
python -c "import spinalmodes, sys; print('ok', sys.version)"
```

## Development

```bash
# Run all checks
make green

# Run tests
make test

# Format code
make format

# Validate figures
poetry run python tools/validate_figures.py
```

## Project Structure

```
spinalmodes/
├── src/spinalmodes/       # Core package
│   ├── iec.py            # IEC model utilities
│   ├── iec_cli.py        # CLI commands
│   ├── fig_*.py          # Figure generation
│   └── solvers/          # Beam/Cosserat solvers
├── tests/                # Unit tests
├── docs/                 # Documentation & manuscript
├── outputs/              # Generated outputs
│   ├── figs/            # Figures (PNG + JSON)
│   ├── csv/             # Data tables
│   ├── aor/             # Analysis of record
│   └── reports/         # Reports
└── tools/               # Validation scripts
```

## Documentation

- [CLI Reference](docs/cli.md)
- [Figure Guide](docs/figures.md)
- [Manuscript](docs/manuscript/SpinalCountercurvature_IEC.md)

## Citation

If you use this code, please cite:
```
Krishnan, S. et al. (2025). Biological Counter-Curvature and Information-Elasticity
Coupling in Spinal Development. [Journal TBD].
```

## License

MIT License - see LICENSE file for details.
