# Longevity Protein Analysis

## Overview

This analysis extracts longevity-related proteins from the BCC AlphaFold dataset and computes entropy-curvature correlations with rigorous statistical controls.

## Proteins Analyzed

- **FOXO3** (Forkhead box O3)
- **SIRT1** (Sirtuin 1)
- **KLOTHO** (Klotho)
- **PGC1A** (PPARGC1A, Peroxisome proliferator-activated receptor gamma coactivator 1-alpha)
- **AMPK** (PRKAA1/PRKAA2, AMP-activated protein kinase)

## Statistical Methods

### Primary Analysis
- **Pearson correlation** between sequence entropy and structural curvature
- **Fisher z-transformation** for 95% confidence intervals
- **Permutation testing** (20,000 permutations) for non-parametric p-values

### Robustness Checks
- **Leave-one-out** correlation analysis
- **Partial correlations** controlling for:
  - Protein length
  - Mean pLDDT (confidence score)

### Data Quality
- Uses **confidence-weighted curvature** (pLDDT ≥ 70) when available
- Falls back to all-residue curvature if pLDDT data unavailable

## Running the Analysis

```bash
# From repository root
make longevity

# Or directly:
python analysis/longevity/longevity_deep_dive.py \
  --input data/processed/bcc_analysis_data.json \
  --outdir results/longevity
```

## Outputs

- `longevity_report.md`: Human-readable analysis report
- `longevity_metrics.json`: Machine-readable metrics
- `fig_entropy_curvature.pdf`: Scatter plot with regression line

## Interpretation

A positive correlation between entropy and curvature suggests that:
- Sequence information content (heterogeneity) correlates with structural curvature
- This supports the information-geometry coupling hypothesis
- Longevity proteins may exhibit distinct structural signatures

**Note**: Small sample sizes (n < 5) limit statistical power. Results should be interpreted cautiously and validated with larger datasets.


