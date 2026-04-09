# Confidence-Weighted Structural Evidence

## Overview
This report re-evaluates the structural candidates for the Biological Countercurvature hypothesis by explicitly weighting their AlphaFold prediction confidence (pLDDT). High anisotropy (extended shapes) in low-confidence regions often reflects unstructured/disordered states rather than rigid mechanosensory rods. We must distinguish between adequate-confidence structures and low-confidence exploratory targets. Generated from `outputs/afcc/2026-02-16/metrics.csv`.

## 1. High-Anisotropy + Adequate-Confidence (>70 pLDDT)
These candidates possess strong structural evidence for an extended, potentially load-bearing conformation.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|---|---|---|---|---|
| CNNM2 | 8.54 | 70.4 | 4.83 | Fibrous/Extended |
| FBLN5 | 7.05 | 83.3 | 3.55 | Fibrous/Extended |
| STOML3 | 5.56 | 84.3 | 0.00 | Fibrous/Extended |
| PANX3 | 5.08 | 81.7 | 2.77 | Fibrous/Extended |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Fibrous/Extended |
| ROCK1 | 3.29 | 76.1 | 4.95 | Fibrous/Extended |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Fibrous/Extended |

## 2. High-Anisotropy + Low-Confidence (<70 pLDDT)
These candidates exhibit extended shapes but lack structural confidence. The anisotropy may simply reflect long unstructured loops rather than mechanosensory 'rods'. Use only for hypothesis generation.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|---|---|---|---|---|
| POC5 | 24.69 | 64.0 | 3.51 | Fibrous/Extended |
| GHR | 5.13 | 58.7 | 5.31 | Fibrous/Extended |
| EMD | 4.29 | 60.3 | 9.13 | Fibrous/Extended |
| MESP2 | 4.03 | 54.2 | 0.00 | Fibrous/Extended |
| ARNTL | 3.32 | 65.5 | 3.59 | Fibrous/Extended |

## 3. LBX1 Comparator Panel
Comparing LBX1 to known mechanosensors and structural regulators to contextualize its hypothesized role as a structural signaling hub.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence |
|---|---|---|---|---|
| LBX1 | 2.27 | 66.9 | 7.35 | Low |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Adequate |
| LMNA | N/A | N/A | N/A | N/A |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Adequate |
| RUNX3 | N/A | N/A | N/A | N/A |
| POC5 | 24.69 | 64.0 | 3.51 | Low |
| GHR | 5.13 | 58.7 | 5.31 | Low |

## 4. Conclusions and Labeling
- **[Confirmed by metrics]** LBX1 has low structural confidence (pLDDT ~66.9) and intermediate anisotropy (~2.27). It does not present as a rigid tension rod, but rather a modular or flexible entity.
- **[Confirmed by metrics]** True structural rods with adequate confidence (e.g., PIEZO2, FBLN5) exhibit pLDDT > 70 alongside high anisotropy.
- **Evidence AGAINST hypothesis strength**: Relying on candidates like POC5 or GHR as primary examples of 'anisotropic mechanosensors' is flawed because their extended shapes are driven by low-confidence (likely disordered) regions. This weakens the structural argument unless validated orthogonally.
