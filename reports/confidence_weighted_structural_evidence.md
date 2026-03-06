# Confidence-Weighted Structural Evidence Report

**Source Data:** `outputs/afcc/2026-02-16/metrics.csv`
**Generated:** 2026-03-06 20:06:18

## 1. High-Anisotropy + Adequate-Confidence (Strong Signal)
Thresholds: Anisotropy >= 3.0, pLDDT >= 70.0

| Gene | Anisotropy | pLDDT | Morphology |
|---|---|---|---|
| CNNM2 | 8.54 | 70.37 | Fibrous/Extended |
| FBLN5 | 7.05 | 83.34 | Fibrous/Extended |
| STOML3 | 5.56 | 84.33 | Fibrous/Extended |
| PANX3 | 5.08 | 81.72 | Fibrous/Extended |
| PIEZO2 | 4.44 | 79.44 | Fibrous/Extended |
| ROCK1 | 3.29 | 76.13 | Fibrous/Extended |
| ADGRG6 | 3.06 | 73.73 | Fibrous/Extended |

## 2. High-Anisotropy + Low-Confidence (Exploratory Only)
Thresholds: Anisotropy >= 3.0, pLDDT < 70.0. *These candidates require orthogonal validation.*

| Gene | Anisotropy | pLDDT | Morphology |
|---|---|---|---|
| POC5 | 24.69 | 63.97 | Fibrous/Extended |
| GHR | 5.13 | 58.70 | Fibrous/Extended |
| EMD | 4.29 | 60.25 | Fibrous/Extended |
| MESP2 | 4.03 | 54.17 | Fibrous/Extended |
| ARNTL | 3.32 | 65.53 | Fibrous/Extended |

## 3. LBX1 Comparator Analysis
Comparing LBX1 metrics against anchor mechanosensors and other highly anisotropic targets.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence Tier |
|---|---|---|---|---|
| ADGRG6 | 3.06 | 73.73 | 6.78 | Adequate |
| GHR | 5.13 | 58.70 | 5.31 | Low |
| LBX1 | 2.27 | 66.87 | 7.35 | Low |
| PIEZO2 | 4.44 | 79.44 | 2.80 | Adequate |
| POC5 | 24.69 | 63.97 | 3.51 | Low |

*Note: The following comparators were absent from the 2026-02-16 snapshot: LMNA, RUNX3*

### Comparator Interpretation
- **LBX1** remains an intermediate-anisotropy candidate with low confidence and high blockiness, distinguishing it from rigid structural rods like PIEZO2.
- **PIEZO2** and **ADGRG6** represent true adequate-confidence mechanosensors, showing high anisotropy and acceptable pLDDT.
- **POC5** and **GHR** show extreme anisotropy but are structurally low-confidence, meaning they are exploratory and their geometry could be an artifact of intrinsic disorder.
