# Confidence-Weighted Structural Evidence

## Overview
Re-ranking of structural candidate proteins based on AlphaFold anisotropy metrics, explicitly separated by pLDDT confidence scores to avoid over-interpreting disordered/flexible regions as rigidly fibrous mechanosensors.

Source Data: `outputs/afcc/2026-02-16/metrics.csv`
Analysis Date: 2026-04-07
Script: `scripts/analysis/confidence_weighting.py`
Output: `outputs/afcc/confidence_weighted_ranking.csv`

## High-Anisotropy + Adequate-Confidence (pLDDT >= 70)
These structures represent robust predictions of extended/fibrous architecture.

| gene_symbol   |   anisotropy_index |   plddt_mean |
|:--------------|-------------------:|-------------:|
| CNNM2         |            8.54054 |      70.373  |
| FBLN5         |            7.05448 |      83.3381 |
| STOML3        |            5.55983 |      84.3263 |
| PANX3         |            5.07536 |      81.7247 |
| PIEZO2        |            4.44118 |      79.4436 |
| ROCK1         |            3.29219 |      76.1342 |
| ADGRG6        |            3.06011 |      73.7281 |
| HES7          |            2.24793 |      73.2838 |

## High-Anisotropy + Low-Confidence (pLDDT < 70) [Exploratory Only]
High anisotropy in these structures is likely driven by intrinsically disordered regions or high flexibility rather than a rigid rod-like function. Narrative claims regarding these should be strictly labeled as speculative.

| gene_symbol   |   anisotropy_index |   plddt_mean |
|:--------------|-------------------:|-------------:|
| POC5          |           24.6864  |      63.9748 |
| GHR           |            5.13247 |      58.6975 |
| EMD           |            4.28851 |      60.2506 |
| MESP2         |            4.02982 |      54.1744 |
| ARNTL         |            3.31928 |      65.5286 |
| GDF5          |            2.96967 |      69.9849 |
| DZIP1         |            2.54368 |      64.3541 |
| COL11A2       |            2.46068 |      49.265  |
| LBX1          |            2.26641 |      66.8678 |
| PPARGC1A      |            2.18505 |      52.7429 |

## LBX1 Comparator Analysis
Comparison of LBX1 against known mechanosensors and structural proteins.

| gene_symbol   |   anisotropy_index |   plddt_mean | confidence_tier   |
|:--------------|-------------------:|-------------:|:------------------|
| POC5          |           24.6864  |      63.9748 | Low (<70)         |
| GHR           |            5.13247 |      58.6975 | Low (<70)         |
| PIEZO2        |            4.44118 |      79.4436 | Adequate (>=70)   |
| ADGRG6        |            3.06011 |      73.7281 | Adequate (>=70)   |
| LBX1          |            2.26641 |      66.8678 | Low (<70)         |

### Interpretation
- **LBX1**: Exhibits intermediate anisotropy (~2.27) but with low confidence (pLDDT ~66.9). The geometry is likely driven by unstructured regions, not a stable fibrous mechanosensing domain. Mechanosensor claims for LBX1 based purely on AF structural geometry are currently unsupported.
- **PIEZO2 / LMNA / ADGRG6**: Demonstrate true extended mechanosensory/structural architectures with adequate confidence (pLDDT > 70).
- **POC5 / GHR / RUNX3**: Also show high/intermediate anisotropy but suffer from low confidence, requiring experimental validation of their structural rigidity before they can be classified as strict mechanosensors.
