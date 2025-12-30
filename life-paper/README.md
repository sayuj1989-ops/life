# Biological Countercurvature: Longevity Analysis

This repository contains the **publication-ready** analysis code and data for the longevity protein correlation study.

## Quick Start

Reproduce all results with a single command:

```bash
make reproduce
```

This will:
1. Set up a Python virtual environment
2. Install dependencies
3. Run the longevity analysis
4. Copy generated figures and tables to `paper/`

## Repository Structure

```
life-paper/
├── README.md                    # This file
├── Makefile                     # Reproducibility automation
├── requirements.txt             # Python dependencies
├── CITATION.cff                 # Citation metadata
│
├── data/
│   └── processed/
│       └── bcc_analysis_data.json  # Frozen input dataset
│
├── analysis/
│   └── longevity/
│       ├── longevity_deep_dive.py  # Main analysis script
│       └── README.md              # Analysis documentation
│
├── results/                     # Generated outputs (gitignored)
│   └── longevity/
│       ├── longevity_report.md
│       ├── longevity_metrics.json
│       └── fig_entropy_curvature.pdf
│
└── paper/                       # Publication artifacts
    ├── figures/                 # Final figures (copied from results)
    └── tables/                  # Final tables (copied from results)
```

## Analysis Details

The longevity analysis (`analysis/longevity/longevity_deep_dive.py`) performs:

1. **Protein Extraction**: Identifies longevity-related proteins using alias matching
   - FOXO3, SIRT1, KLOTHO, PGC1A, AMPK
   - Handles name variations (e.g., PPARGC1A → PGC1A)

2. **Statistical Analysis**:
   - Pearson correlation with Fisher z-transformation CI
   - Permutation testing (20,000 permutations by default)
   - Leave-one-out robustness checks
   - Partial correlations controlling for length and pLDDT

3. **Confidence-Weighted Metrics**:
   - Uses `mean_curvature_plddt` (pLDDT ≥ 70) when available
   - Falls back to `mean_curvature` if pLDDT-filtered data unavailable

## Requirements

- Python 3.8+
- See `requirements.txt` for package versions

## Reproducibility

All results are generated deterministically from the frozen dataset in `data/processed/bcc_analysis_data.json`.

To verify reproducibility:

```bash
make clean
make reproduce
```

## Citation

If you use this code or data, please cite:

```bibtex
@software{bcc_longevity_2024,
  author = {...},
  title = {Biological Countercurvature: Longevity Protein Analysis},
  year = {2024},
  url = {...}
}
```

## License

See `LICENSE` file.


