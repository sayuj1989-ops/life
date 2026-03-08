# Confidence-Weighted Structural Evidence Report

## Overview

- **Source Data**: `outputs/afcc/2026-02-16/metrics.csv` (supplemented with most recent available data for missing comparator genes)

- **Adequate Confidence Threshold**: `pLDDT >= 70.0`

- **High Anisotropy Threshold**: `Anisotropy >= 3.0`

This report re-ranks candidates with explicit confidence weighting to distinguish robust structural signals from exploratory, low-confidence predictions.


## 1. High-Anisotropy + Adequate-Confidence (Strong Signal)

These proteins exhibit extended, load-bearing morphologies and their structural predictions are reliable.

| Rank | Gene | Anisotropy | pLDDT (Mean) | PAE Blockiness |

|------|------|------------|--------------|----------------|
| 1 | CNNM2 | 8.54 | 70.4 | 4.83 |
| 2 | FBLN5 | 7.05 | 83.3 | 3.55 |
| 3 | STOML3 | 5.56 | 84.3 | 0.00 |
| 4 | PANX3 | 5.08 | 81.7 | 2.77 |
| 5 | LMNA | 4.75 | 76.4 | 2.56 |
| 6 | PIEZO2 | 4.44 | 79.4 | 2.80 |
| 7 | ROCK1 | 3.29 | 76.1 | 4.95 |
| 8 | ADGRG6 | 3.06 | 73.7 | 6.78 |

## 2. High-Anisotropy + Low-Confidence (Exploratory Only)

These proteins exhibit extended morphologies but their structural predictions are low-confidence. Their high anisotropy may be an artifact of long, unstructured regions (IDRs). **Hypothesis-generating only; requires orthogonal validation.**

| Rank | Gene | Anisotropy | pLDDT (Mean) | PAE Blockiness |

|------|------|------------|--------------|----------------|
| 1 | POC5 | 24.69 | 64.0 | 3.51 |
| 2 | GHR | 5.13 | 58.7 | 5.31 |
| 3 | EMD | 4.29 | 60.3 | 9.13 |
| 4 | MESP2 | 4.03 | 54.2 | 0.00 |
| 5 | ARNTL | 3.32 | 65.5 | 3.59 |

## 3. LBX1 Comparator Panel Analysis

Comparison of LBX1 against key anchors and speculative sensors. Note: LMNA and RUNX3 are supplemented from their most recent historical snapshot if missing from 2026-02-16.

| Gene | Anisotropy | pLDDT (Mean) | PAE Blockiness | Confidence | Anisotropy Class |

|------|------------|--------------|----------------|------------|------------------|
| LBX1 | 2.27 | 66.9 | 7.35 | Low | Intermediate/Low |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Adequate | High |
| LMNA | 4.75 | 76.4 | 2.56 | Adequate | High |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Adequate | High |
| RUNX3 | 2.06 | 60.6 | 0.00 | Low | Intermediate/Low |
| POC5 | 24.69 | 64.0 | 3.51 | Low | High |
| GHR | 5.13 | 58.7 | 5.31 | Low | High |

### Interpretation

- **LBX1** remains a low-confidence, intermediate-anisotropy candidate with high PAE blockiness. It is structurally dissimilar to strong mechanosensor anchors like PIEZO2.

- **PIEZO2** maintains high anisotropy and adequate confidence, supporting its role as a robust structural anchor.

- **POC5** and **GHR** show extreme or high anisotropy but suffer from low confidence. Their structural signals must be treated as speculative and not definitive proof of a tension-rod architecture.
