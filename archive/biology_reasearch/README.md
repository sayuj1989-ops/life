# Biological Countercurvature of Spacetime

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

This repository contains the official implementation of the **Information-Elasticity Coupling (IEC)** framework for biological morphogenesis, focusing on the emergence of spinal counter-curvature. The project bridges developmental genetics (HOX patterning), structural biology (AlphaFold), and Cosserat rod mechanics to explain both healthy spinal geometry and the onset of Adolescent Idiopathic Scoliosis (AIS).

## 🚀 Key Features

- **Information-Cosserat Solver**: A high-performance 3D beam solver that incorporates metric warping driven by developmental information fields.
- **Countercurvature Metrics**: Implementation of the normalized geodesic curvature deviation $\widehat{D}_{\mathrm{geo}}$, a novel metric for classifying biological stability regimes.
- **Scoliosis Bifurcation Analysis**: Automated workflows for modeling symmetry-breaking and the temporal dynamics of spinal growth during the adolescent growth spurt.
- **AlphaFold Integration**: Programmatic bridge to the AlphaFold Protein Structure Database, mapping molecular-scale protein stability (HOXC8, LBX1, ADGRG6) to macroscopic mechanical parameters.

## 📂 Repository Structure

```text
biology_reasearch/
├── manuscript/          # Nature-standard LaTeX manuscript files
│   ├── main.tex         # Main document
│   ├── references.bib   # Bibliography
│   ├── sections/        # Modularized LaTeX sections
│   └── figures/         # High-resolution PDF/PNG figure panels
├── src/spinalmodes/     # Core Python package implementing the IEC framework
│   ├── countercurvature/# Mathematical definitions and metrics
│   ├── experiments/     # Reproduction scripts for all manuscript figures
│   └── external/        # AlphaFold Database API integration
├── experiments/         # Standalone scripts for quick reproduction
├── tests/               # Comprehensive pytest suite for model validation
├── docs/                # Detailed documentation and project plans
└── pyproject.toml       # Package management and dependencies
```

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/sayujks0071/biology_reasearch.git
cd biology_reasearch

# Install dependencies (requires Poetry or pip)
pip install -r requirements.txt
pip install -e .
```

## 📊 Reproducing Results

To generate the figure panels used in the manuscript, run the following scripts:

```bash
# Generate Figure 1 (Gene to Geometry mapping)
python -m spinalmodes.experiments.countercurvature.generate_figure1_gene_geometry

# Generate Figure 2 (Mode Selection analysis)
python -m spinalmodes.experiments.countercurvature.generate_figure2_mode_spectrum

# Generate Figure 5 (Scoliosis and Growth Dynamics)
python -m spinalmodes.experiments.countercurvature.experiment_scoliosis_bifurcation
```

Outputs will be saved to the `outputs/` directory.

## 🧬 Structural Biology Support

The IEC framework is anchored by structural data from the **AlphaFold Protein Structure Database**. Our analysis demonstrates that the structural rigidity of HOX transcription factors (e.g., HOXC8, avg pLDDT ~64.1) provides the physical substrate for the information field that shapes the spinal axis.

Refer to `src/spinalmodes/external/alphafold_summary.txt` for the detailed proteomic report.

## 📝 Citation

If you use this framework or code in your research, please cite:

```bibtex
@article{krishnan2025biological,
  title={Biological Countercurvature of Spacetime: An Information--Cosserat Framework for Spinal Geometry},
  author={Krishnan S., Sayuj},
  journal={Nature},
  year={2025},
  note={Under Review}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📝 Structured Research Summary

For a unified overview of the research project, including Abstract, Theory, Methods, Results, and Figures in a single document, see:
- [**STRUCTURED_RESEARCH_REPORT.md**](./STRUCTURED_RESEARCH_REPORT.md)
- [**UNIFIED_MANUSCRIPT.tex**](./UNIFIED_MANUSCRIPT.tex) (Complete LaTeX source)
