# Spinal Modes: IEC Model Documentation

Welcome to the documentation for the **Spinal Modes** project, implementing the Information-Elasticity Coupling (IEC) model for spinal biomechanics.

## Quick Links

- [CLI Reference](cli.md) - Command-line interface documentation
- [Figure Guide](figures.md) - Generated figures and interpretation
- [Manuscript](manuscript/SpinalCountercurvature_IEC.md) - Full research manuscript

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

Requirements:
- Python 3.10+
- Poetry for dependency management

```bash
git clone https://github.com/[username]/spinalmodes.git
cd spinalmodes
poetry install
```

## Testing

```bash
# Run all tests
poetry run pytest tests/ -v

# Run with coverage
poetry run pytest tests/ --cov=src/spinalmodes --cov-report=term-missing

# Run all checks (lint + format + type + test)
make green
```

## Citation

If you use this code, please cite:

```bibtex
@article{krishnan2025iec,
  title={Biological Counter-Curvature and Information-Elasticity Coupling in Spinal Development},
  author={Krishnan, Sayuj and others},
  journal={[Journal TBD]},
  year={2025}
}
```

## License

MIT License - see [LICENSE](../LICENSE) file.

## Contact

For questions or collaboration inquiries, please contact:
- Dr. Sayuj Krishnan: [email]
- GitHub: [github.com/username/spinalmodes]

## Acknowledgments

This work integrates concepts from developmental biology, biomechanics, and applied mathematics. We thank the research community for foundational work on HOX patterning, ciliary mechanics, and spinal biomechanics.

