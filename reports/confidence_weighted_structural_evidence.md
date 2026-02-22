# Confidence-Weighted Structural Evidence
Based on metrics from: /app/research/alphafold_countercurvature/data/processed/protein_metrics.csv

## 1. Executive Summary
This analysis re-evaluates structural candidates by weighting their anisotropy with AlphaFold confidence metrics (pLDDT and PAE).
High anisotropy in low-confidence regions (IDRs) is distinguished from rigid, high-confidence structural anisotropy.

## 2. Comparator Analysis: LBX1 vs Controls
We compare LBX1 against known mechanosensors (PIEZO2) and structural proteins (LMNA, GHR).

| gene_symbol   |   anisotropy_index |   plddt_mean |   PAE_mean | Confidence_Tier   | Anisotropy_Tier   |   Weighted_Anisotropy | morphology       |
|:--------------|-------------------:|-------------:|-----------:|:------------------|:------------------|----------------------:|:-----------------|
| POC5          |           24.6864  |      63.9748 |    25.648  | Low               | Extreme (>3.5)    |             10.1036   | Fibrous/Extended |
| PIEZO2        |            4.44118 |      79.4436 |    16.9875 | Medium            | Extreme (>3.5)    |              2.80296  | Fibrous/Extended |
| LMNA          |            4.75167 |      76.3707 |    24.8748 | Medium            | Extreme (>3.5)    |              2.7714   | Fibrous/Extended |
| GHR           |            5.13247 |      58.6975 |    25.8273 | Low               | Extreme (>3.5)    |              1.76834  | Fibrous/Extended |
| ADGRG6        |            3.06011 |      73.7281 |    24.4288 | Medium            | High (>2.0)       |              1.66343  | Fibrous/Extended |
| ARNTL         |            3.31928 |      65.5286 |    22.8182 | Low               | High (>2.0)       |              1.4253   | Fibrous/Extended |
| LBX1          |            2.26641 |      66.8678 |    25.0821 | Low               | High (>2.0)       |              1.01338  | Intermediate     |
| IGF1R         |            1.42663 |      78.0179 |    23.5864 | Medium            | Standard          |              0.868361 | Globular         |
| DMD           |            1.31553 |      76.3493 |    19.0087 | Medium            | Standard          |              0.766853 | Globular         |
| RUNX3         |            2.06117 |      60.5641 |    25.59   | Low               | High (>2.0)       |              0.756038 | Intermediate     |
| MYLK          |            1.46405 |      65.8451 |    26.6029 | Low               | Standard          |              0.634751 | Globular         |
| PPARGC1A      |            2.18505 |      52.7429 |    28.0889 | Low               | High (>2.0)       |              0.60784  | Intermediate     |

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
| PIEZO2        |            4.44118 |      79.4436 |    16.9875 | Medium            | Extreme (>3.5)    |               2.80296 | Fibrous/Extended |
| LMNA          |            4.75167 |      76.3707 |    24.8748 | Medium            | Extreme (>3.5)    |               2.7714  | Fibrous/Extended |
| ADGRG6        |            3.06011 |      73.7281 |    24.4288 | Medium            | High (>2.0)       |               1.66343 | Fibrous/Extended |

## 4. Low-Confidence Artifact Risks
These proteins show high anisotropy but have Low confidence, posing a risk of false positives due to IDRs.
| gene_symbol   |   anisotropy_index |   plddt_mean |   PAE_mean | Confidence_Tier   | Anisotropy_Tier   |   Weighted_Anisotropy | morphology       |
|:--------------|-------------------:|-------------:|-----------:|:------------------|:------------------|----------------------:|:-----------------|
| POC5          |           24.6864  |      63.9748 |    25.648  | Low               | Extreme (>3.5)    |             10.1036   | Fibrous/Extended |
| GHR           |            5.13247 |      58.6975 |    25.8273 | Low               | Extreme (>3.5)    |              1.76834  | Fibrous/Extended |
| ARNTL         |            3.31928 |      65.5286 |    22.8182 | Low               | High (>2.0)       |              1.4253   | Fibrous/Extended |
| LBX1          |            2.26641 |      66.8678 |    25.0821 | Low               | High (>2.0)       |              1.01338  | Intermediate     |
| RUNX3         |            2.06117 |      60.5641 |    25.59   | Low               | High (>2.0)       |              0.756038 | Intermediate     |
| PPARGC1A      |            2.18505 |      52.7429 |    28.0889 | Low               | High (>2.0)       |              0.60784  | Intermediate     |