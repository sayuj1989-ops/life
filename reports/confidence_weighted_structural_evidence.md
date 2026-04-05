# Confidence-Weighted Structural Evidence
Generated: 2026-04-05 20:13:58
Data Source: `outputs/afcc/2026-02-16/metrics.csv`

## Overview
This report re-ranks candidates with explicit confidence weighting based on pLDDT scores.
Thresholds used: High Anisotropy >= 3.0, Adequate Confidence (pLDDT >= 70).

## 1. High-Anisotropy + Adequate-Confidence (Strong Evidence)
| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|---|---|---|---|---|
| CNNM2 | 8.54 | 70.4 | 4.83 | Fibrous/Extended |
| FBLN5 | 7.05 | 83.3 | 3.55 | Fibrous/Extended |
| STOML3 | 5.56 | 84.3 | 0.00 | Fibrous/Extended |
| PANX3 | 5.08 | 81.7 | 2.77 | Fibrous/Extended |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Fibrous/Extended |
| ROCK1 | 3.29 | 76.1 | 4.95 | Fibrous/Extended |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Fibrous/Extended |

## 2. High-Anisotropy + Low-Confidence (Exploratory Only)
| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|---|---|---|---|---|
| POC5 | 24.69 | 64.0 | 3.51 | Fibrous/Extended |
| GHR | 5.13 | 58.7 | 5.31 | Fibrous/Extended |
| EMD | 4.29 | 60.3 | 9.13 | Fibrous/Extended |
| MESP2 | 4.03 | 54.2 | 0.00 | Fibrous/Extended |
| ARNTL | 3.32 | 65.5 | 3.59 | Fibrous/Extended |

## 3. LBX1 Comparator Analysis
Comparing LBX1 to key structural anchors and outliers:
| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence |
|---|---|---|---|---|
| ADGRG6 | 3.06 | 73.7 | 6.78 | Adequate |
| GHR | 5.13 | 58.7 | 5.31 | Low |
| LBX1 | 2.27 | 66.9 | 7.35 | Low |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Adequate |
| POC5 | 24.69 | 64.0 | 3.51 | Low |
| LMNA | N/A | N/A | N/A | N/A (Missing from snapshot) |
| RUNX3 | N/A | N/A | N/A | N/A (Missing from snapshot) |