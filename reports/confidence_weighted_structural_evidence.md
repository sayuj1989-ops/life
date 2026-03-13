# Confidence-Weighted Structural Evidence

## Overview
Generated based on authoritative metrics snapshot: `outputs/afcc/2026-02-16/metrics.csv` (with missing comparators backfilled from recent runs).
To mitigate narrative over-interpretation of static, low-confidence AFDB structures, this report re-ranks mechanosensor candidates by explicitly weighting their anisotropy by predictive confidence.

## 1. High-Anisotropy, Adequate-Confidence (Structural Signal Strong)
Proteins exhibiting significant extended shapes (Anisotropy >= 3.0) and sufficient predictive reliability (pLDDT >= 70). These are prime candidates for direct mechanical force transmission.

| gene_symbol   |   anisotropy_index |   plddt_mean |   confidence_weighted_anisotropy | morphology       |
|:--------------|-------------------:|-------------:|---------------------------------:|:-----------------|
| FBLN5         |            7.05448 |      83.3381 |                          5.87957 | Fibrous/Extended |
| STOML3        |            5.55983 |      84.3263 |                          4.77121 | Fibrous/Extended |
| CNNM2         |            8.54054 |      70.373  |                          4.3499  | Fibrous/Extended |
| PANX3         |            5.07536 |      81.7247 |                          4.02536 | Fibrous/Extended |
| PIEZO2        |            4.44118 |      79.4436 |                          3.26911 | Fibrous/Extended |
| ROCK1         |            3.29219 |      76.1342 |                          2.15097 | Fibrous/Extended |
| ADGRG6        |            3.06011 |      73.7281 |                          1.81527 | Fibrous/Extended |

## 2. High-Anisotropy, Low-Confidence (Exploratory Only)
Proteins showing high theoretical anisotropy but lacking structural reliability (pLDDT < 70). These likely contain large Intrinsically Disordered Regions (IDRs). The 'fibrous' shape may be a simulation artifact of unbound states rather than a true biological rigid rod.

| gene_symbol   |   anisotropy_index |   plddt_mean |   confidence_weighted_anisotropy | morphology       |
|:--------------|-------------------:|-------------:|---------------------------------:|:-----------------|
| POC5          |           24.6864  |      63.9748 |                          8.62472 | Fibrous/Extended |
| ARNTL         |            3.31928 |      65.5286 |                          1.2886  | Fibrous/Extended |
| GHR           |            5.13247 |      58.6975 |                          1.116   | Fibrous/Extended |
| EMD           |            4.28851 |      60.2506 |                          1.099   | Fibrous/Extended |
| MESP2         |            4.02982 |      54.1744 |                          0.42055 | Fibrous/Extended |

## 3. LBX1 vs Mechanotransduction Comparators
LBX1 is hypothesized as a crucial sensor/integrator. How does its structural profile compare against known mechanosensors and other key candidates?

| gene_symbol   |   anisotropy_index |   plddt_mean |   confidence_weighted_anisotropy |   PAE_domain_blockiness_score | morphology       | run_date   |
|:--------------|-------------------:|-------------:|---------------------------------:|------------------------------:|:-----------------|:-----------|
| POC5          |           24.6864  |      63.9748 |                         8.62472  |                       3.50811 | Fibrous/Extended | 2026-02-16 |
| PIEZO2        |            4.44118 |      79.4436 |                         3.26911  |                       2.79999 | Fibrous/Extended | 2026-02-16 |
| ADGRG6        |            3.06011 |      73.7281 |                         1.81527  |                       6.77855 | Fibrous/Extended | 2026-02-16 |
| GHR           |            5.13247 |      58.6975 |                         1.116    |                       5.30902 | Fibrous/Extended | 2026-02-16 |
| LBX1          |            2.26641 |      66.8678 |                         0.955734 |                       7.35466 | Intermediate     | 2026-02-16 |
| LMNA          |            4.75167 |      76.3707 |                         3.13262  |                       2.5622  | Fibrous/Extended | 2026-02-26 |
| RUNX3         |            2.06117 |      60.5641 |                         0.544359 |                       0       | Intermediate     | 2026-03-05 |

**Synthesis:**
LBX1 exhibits an intermediate, low-confidence structure (Anisotropy ~2.27, pLDDT ~66.9). Unlike true fibrous mechanosensors (e.g., PIEZO2, LMNA), its predicted structure lacks the rigid, extended architecture necessary to directly sustain or transmit significant tensile loads. Its role is likely downstream (biochemical/transcriptional integration) rather than primary mechanical load-bearing.