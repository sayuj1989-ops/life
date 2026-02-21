# Confidence-Weighted Structural Evidence
Based on metrics from: outputs/afcc/2026-02-16/metrics.csv

## 1. Executive Summary
This analysis re-evaluates structural candidates by weighting their anisotropy with AlphaFold confidence metrics (pLDDT and PAE).
High anisotropy in low-confidence regions (IDRs) is distinguished from rigid, high-confidence structural anisotropy.

## 2. Comparator Analysis: LBX1 vs Controls
We compare LBX1 against known mechanosensors (PIEZO2) and structural proteins (LMNA, GHR).

| gene_symbol   |   anisotropy_index |   plddt_mean |   PAE_mean | Confidence_Tier   | Anisotropy_Tier   |   Weighted_Anisotropy | morphology       |
|:--------------|-------------------:|-------------:|-----------:|:------------------|:------------------|----------------------:|:-----------------|
| POC5          |           24.6864  |      63.9748 |    25.648  | Low               | Extreme (>3.5)    |              10.1036  | Fibrous/Extended |
| PIEZO2        |            4.44118 |      79.4436 |    16.9875 | Medium            | Extreme (>3.5)    |               2.80296 | Fibrous/Extended |
| GHR           |            5.13247 |      58.6975 |    25.8273 | Low               | Extreme (>3.5)    |               1.76834 | Fibrous/Extended |
| ADGRG6        |            3.06011 |      73.7281 |    24.4288 | Medium            | High (>2.0)       |               1.66343 | Fibrous/Extended |
| LBX1          |            2.26641 |      66.8678 |    25.0821 | Low               | High (>2.0)       |               1.01338 | Intermediate     |

### Key Observations
- **LBX1**: Anisotropy 2.27, pLDDT 66.9 (Low).
  - Weighted Score: 1.01
  - **CRITICAL CAVEAT**: LBX1's anisotropy is flagged as Low Confidence. This suggests the shape elongation might be due to disordered loops rather than a rigid structural feature.
- **PIEZO2**: Anisotropy 4.44, pLDDT 79.4 (Medium).
  - Weighted Score: 2.80
  - PIEZO2 maintains high anisotropy even when weighted by confidence, supporting its role as a rigid tension rod.

## 3. Top High-Confidence Anisotropic Structures
These proteins have confirmed structural elongation (High/Medium Confidence + High/Extreme Anisotropy).
| gene_symbol   |   anisotropy_index |   plddt_mean |   PAE_mean | Confidence_Tier   | Anisotropy_Tier   |   Weighted_Anisotropy | morphology       |
|:--------------|-------------------:|-------------:|-----------:|:------------------|:------------------|----------------------:|:-----------------|
| FBLN5         |            7.05448 |      83.3381 |    18.9889 | Medium            | Extreme (>3.5)    |               4.8995  | Fibrous/Extended |
| CNNM2         |            8.54054 |      70.373  |    22.413  | Medium            | Extreme (>3.5)    |               4.22958 | Fibrous/Extended |
| STOML3        |            5.55983 |      84.3263 |    13.6189 | High              | Extreme (>3.5)    |               3.95356 | Fibrous/Extended |
| PANX3         |            5.07536 |      81.7247 |    12.8535 | High              | Extreme (>3.5)    |               3.3898  | Fibrous/Extended |
| PIEZO2        |            4.44118 |      79.4436 |    16.9875 | Medium            | Extreme (>3.5)    |               2.80296 | Fibrous/Extended |
| ROCK1         |            3.29219 |      76.1342 |    24.3405 | Medium            | High (>2.0)       |               1.90829 | Fibrous/Extended |
| ADGRG6        |            3.06011 |      73.7281 |    24.4288 | Medium            | High (>2.0)       |               1.66343 | Fibrous/Extended |
| HES7          |            2.24793 |      73.2838 |    22.8848 | Medium            | High (>2.0)       |               1.20725 | Intermediate     |

## 4. Low-Confidence Artifact Risks
These proteins show high anisotropy but have Low confidence, posing a risk of false positives due to IDRs.
| gene_symbol   |   anisotropy_index |   plddt_mean |   PAE_mean | Confidence_Tier   | Anisotropy_Tier   |   Weighted_Anisotropy | morphology       |
|:--------------|-------------------:|-------------:|-----------:|:------------------|:------------------|----------------------:|:-----------------|
| POC5          |           24.6864  |      63.9748 |    25.648  | Low               | Extreme (>3.5)    |             10.1036   | Fibrous/Extended |
| GHR           |            5.13247 |      58.6975 |    25.8273 | Low               | Extreme (>3.5)    |              1.76834  | Fibrous/Extended |
| EMD           |            4.28851 |      60.2506 |    26.4501 | Low               | Extreme (>3.5)    |              1.55679  | Fibrous/Extended |
| GDF5          |            2.96967 |      69.9849 |    20.2226 | Low               | High (>2.0)       |              1.45451  | Intermediate     |
| ARNTL         |            3.31928 |      65.5286 |    22.8182 | Low               | High (>2.0)       |              1.4253   | Fibrous/Extended |
| MESP2         |            4.02982 |      54.1744 |    26.8834 | Low               | Extreme (>3.5)    |              1.1827   | Fibrous/Extended |
| DZIP1         |            2.54368 |      64.3541 |    26.7206 | Low               | High (>2.0)       |              1.05345  | Intermediate     |
| LBX1          |            2.26641 |      66.8678 |    25.0821 | Low               | High (>2.0)       |              1.01338  | Intermediate     |
| PPARGC1A      |            2.18505 |      52.7429 |    28.0889 | Low               | High (>2.0)       |              0.60784  | Intermediate     |
| COL11A2       |            2.46068 |      49.265  |    27.1683 | Low               | High (>2.0)       |              0.597216 | Intermediate     |