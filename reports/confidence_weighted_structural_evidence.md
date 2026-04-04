# Confidence-Weighted Structural Evidence

**Data Source:** `outputs/afcc/2026-02-16/metrics.csv`
**Date:** 2026-04-04

## 1. High-Anisotropy + Adequate-Confidence (>70 pLDDT)
These proteins represent structurally verified anisotropic candidates.

| Gene | Anisotropy | pLDDT Mean | Morphology | Notes |
|---|---|---|---|---|
| CNNM2 | 8.54 | 70.4 | Fibrous/Extended | |
| FBLN5 | 7.05 | 83.3 | Fibrous/Extended | |
| STOML3 | 5.56 | 84.3 | Fibrous/Extended | |
| PANX3 | 5.08 | 81.7 | Fibrous/Extended | |
| PIEZO2 | 4.44 | 79.4 | Fibrous/Extended | |
| ROCK1 | 3.29 | 76.1 | Fibrous/Extended | |
| ADGRG6 | 3.06 | 73.7 | Fibrous/Extended | |
| HES7 | 2.25 | 73.3 | Intermediate | |
| AQP4 | 1.97 | 81.0 | Intermediate | |
| GAPDH | 1.78 | 98.1 | Intermediate | |

## 2. High-Anisotropy + Low-Confidence (<70 pLDDT) (Exploratory Only)
High anisotropy in these proteins may be driven by unstructured regions. Proceed with caution.

| Gene | Anisotropy | pLDDT Mean | Morphology | Notes |
|---|---|---|---|---|
| POC5 | 24.69 | 64.0 | Fibrous/Extended | |
| GHR | 5.13 | 58.7 | Fibrous/Extended | |
| EMD | 4.29 | 60.3 | Fibrous/Extended | |
| MESP2 | 4.03 | 54.2 | Fibrous/Extended | |
| ARNTL | 3.32 | 65.5 | Fibrous/Extended | |
| GDF5 | 2.97 | 70.0 | Intermediate | |
| DZIP1 | 2.54 | 64.4 | Intermediate | |
| COL11A2 | 2.46 | 49.3 | Intermediate | |
| LBX1 | 2.27 | 66.9 | Intermediate | |
| PPARGC1A | 2.19 | 52.7 | Intermediate | |

## 3. LBX1 Comparator Analysis
Comparing LBX1 to key markers.

| Gene | Anisotropy | pLDDT Mean | Confidence | Comparison |
|---|---|---|---|---|
| LBX1 | 2.27 | 66.9 | Low | |
| PIEZO2 | 4.44 | 79.4 | Adequate | |
| ADGRG6 | 3.06 | 73.7 | Adequate | |
| POC5 | 24.69 | 64.0 | Low | |
| GHR | 5.13 | 58.7 | Low | |

**LBX1 Context:** LBX1 shows intermediate anisotropy (2.27) and low confidence (66.9 pLDDT). It is less anisotropic than PIEZO2 or GHR, and its predicted structure is likely flexible/disordered, suggesting its role might not be a pure rigid mechanosensor but a flexible scaffold or its anisotropy is an artifact of low-confidence regions.
