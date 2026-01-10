# Biological Countercurvature: An Information-Geometry Framework

## Table of Contents

- [Abstract](01_Abstract.md)
- [Introduction](02_Introduction.md)
- [Theory](03_Theory.md)
- [Methods](04_Methods.md)
- [Results](05_Results.md)
- [Discussion](06_Discussion.md)
- [Conclusion](07_Conclusion.md)

## Analysis Code

- [AlphaFold Molecular Analysis](analysis/alphafold_analysis/): Code and reports for protein structure-information correlation.
- [AlphaFold Report](analysis/alphafold_analysis/analysis_report.md)

## Reproducibility

All quantitative results and figures are reproducible from a clean environment:

- `make data` generates CSVs in `results/`
- `make figs` regenerates all manuscript figures in `figures/`
- `make all` runs data + figs and updates derived-number placeholders in the manuscript

Configuration lives in:

- `config/default.yaml` (simulation + sweeps)
- `config/alphafold.yaml` (AlphaFold reanalysis)
