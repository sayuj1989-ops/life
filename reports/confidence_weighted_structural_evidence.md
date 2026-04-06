# Confidence-Weighted Structural Evidence

*Authoritative Snapshot used:* `outputs/afcc/2026-02-16/metrics.csv`

## 1. High-Anisotropy + Adequate-Confidence Candidates
These proteins exhibit strong structural asymmetry while maintaining reliable AlphaFold predictions (pLDDT $\ge$ 70). These are the strongest candidates for structurally grounded mechanosensor models.

| gene_symbol   |   anisotropy_index |   plddt_mean |   PAE_domain_blockiness_score | morphology       | confidence_class   |
|:--------------|-------------------:|-------------:|------------------------------:|:-----------------|:-------------------|
| CNNM2         |            8.54054 |      70.373  |                       4.82678 | Fibrous/Extended | adequate           |
| FBLN5         |            7.05448 |      83.3381 |                       3.55056 | Fibrous/Extended | adequate           |
| STOML3        |            5.55983 |      84.3263 |                       0       | Fibrous/Extended | adequate           |
| PANX3         |            5.07536 |      81.7247 |                       2.77405 | Fibrous/Extended | adequate           |
| PIEZO2        |            4.44118 |      79.4436 |                       2.79999 | Fibrous/Extended | adequate           |
| ROCK1         |            3.29219 |      76.1342 |                       4.9481  | Fibrous/Extended | adequate           |
| ADGRG6        |            3.06011 |      73.7281 |                       6.77855 | Fibrous/Extended | adequate           |

## 2. High-Anisotropy + Low-Confidence Candidates (Exploratory Only)
These proteins exhibit high anisotropy, but their pLDDT scores indicate significant disorder or low modeling confidence (pLDDT < 70). The structural asymmetry may be an artifact of long intrinsically disordered regions rather than a true fibrous morphology.

| gene_symbol   |   anisotropy_index |   plddt_mean |   PAE_domain_blockiness_score | morphology       | confidence_class   |
|:--------------|-------------------:|-------------:|------------------------------:|:-----------------|:-------------------|
| POC5          |           24.6864  |      63.9748 |                       3.50811 | Fibrous/Extended | low                |
| GHR           |            5.13247 |      58.6975 |                       5.30902 | Fibrous/Extended | low                |
| EMD           |            4.28851 |      60.2506 |                       9.12696 | Fibrous/Extended | low                |
| MESP2         |            4.02982 |      54.1744 |                       0       | Fibrous/Extended | low                |
| ARNTL         |            3.31928 |      65.5286 |                       3.58564 | Fibrous/Extended | low                |

## 3. LBX1 Comparator Analysis

We compare LBX1 against key benchmark proteins:
| gene_symbol   |   anisotropy_index |   plddt_mean |   PAE_domain_blockiness_score | morphology       | confidence_class   |
|:--------------|-------------------:|-------------:|------------------------------:|:-----------------|:-------------------|
| POC5          |           24.6864  |      63.9748 |                       3.50811 | Fibrous/Extended | low                |
| GHR           |            5.13247 |      58.6975 |                       5.30902 | Fibrous/Extended | low                |
| PIEZO2        |            4.44118 |      79.4436 |                       2.79999 | Fibrous/Extended | adequate           |
| ADGRG6        |            3.06011 |      73.7281 |                       6.77855 | Fibrous/Extended | adequate           |
| LBX1          |            2.26641 |      66.8678 |                       7.35466 | Intermediate     | low                |

**Key Observations:**
- LBX1 presents an intermediate anisotropy with low confidence.
- PIEZO2 serves as a robust mechanosensor benchmark, presenting high anisotropy and adequate confidence.
- LMNA is absent from the current snapshot.
- POC5 and GHR show extremely high anisotropy but suffer from low confidence, likely due to IDRs.
