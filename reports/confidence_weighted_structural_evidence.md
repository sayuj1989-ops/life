# Confidence-Weighted Structural Evidence Report

## Data Source
- **Primary Snapshot:** `outputs/afcc/2026-02-16/metrics.csv`
- **Methodology:** pLDDT >= 70 defines 'Adequate Confidence'. Anisotropy >= 3.0 defines 'High Anisotropy'.

## 1. High-Anisotropy + Adequate-Confidence (Strongest Evidence)
These candidates possess both extended geometries and high structural reliability.

| Gene | Anisotropy | pLDDT Mean | PAE Blockiness |
|---|---|---|---|
| CNNM2 | 8.54 | 70.4 | 4.83 |
| FBLN5 | 7.05 | 83.3 | 3.55 |
| STOML3 | 5.56 | 84.3 | 0.00 |
| PANX3 | 5.08 | 81.7 | 2.77 |
| LMNA | 4.75 | 76.4 | 2.56 |
| PIEZO2 | 4.44 | 79.4 | 2.80 |
| ROCK1 | 3.29 | 76.1 | 4.95 |
| ADGRG6 | 3.06 | 73.7 | 6.78 |

## 2. High-Anisotropy + Low-Confidence (Exploratory Only)
These candidates show extended geometries but low structural reliability, often indicating intrinsic disorder. They should generate hypotheses, not conclusions.

| Gene | Anisotropy | pLDDT Mean | PAE Blockiness |
|---|---|---|---|
| POC5 | 24.69 | 64.0 | 3.51 |
| GHR | 5.13 | 58.7 | 5.31 |
| EMD | 4.29 | 60.3 | 9.13 |
| MESP2 | 4.03 | 54.2 | 0.00 |
| ARNTL | 3.32 | 65.5 | 3.59 |

## 3. LBX1 Comparator Analysis
Comparing LBX1 against key anchor genes to contextualize its structural plausibility as a direct mechanosensor.

| Gene | Anisotropy | pLDDT Mean | PAE Blockiness | Confidence | Notes |
|---|---|---|---|---|---|
| LBX1 | 2.27 | 66.9 | 7.35 | Low | Baseline, static, blocky |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Adequate | Strong tension rod |
| LMNA | 4.75 | 76.4 | 2.56 | Adequate | Strong tension rod |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Adequate |  |
| RUNX3 | 2.06 | 60.6 | 0.00 | Low |  |
| POC5 | 24.69 | 64.0 | 3.51 | Low | Low-confidence outlier |
| GHR | 5.13 | 58.7 | 5.31 | Low |  |
