# Confidence-Weighted Structural Evidence Report

**Date**: 2026-02-19
**Source Data**: `outputs/afcc/2026-02-16/metrics.csv`

## Methodology

Candidates were re-ranked based on anisotropy, with explicit separation by structural confidence (pLDDT).
- **High Anisotropy Threshold**: >= 3.0
- **Adequate Confidence Threshold**: pLDDT >= 70.0

## High-Anisotropy + Adequate-Confidence (Strong Structural Signal)

| Gene | Anisotropy | pLDDT | PAE Blockiness |
|------|------------|-------|----------------|
| CNNM2 | 8.54 | 70.37 | 4.83 |
| FBLN5 | 7.05 | 83.34 | 3.55 |
| STOML3 | 5.56 | 84.33 | 0.00 |
| PANX3 | 5.08 | 81.72 | 2.77 |
| PIEZO2 | 4.44 | 79.44 | 2.80 |
| ROCK1 | 3.29 | 76.13 | 4.95 |
| ADGRG6 | 3.06 | 73.73 | 6.78 |

## High-Anisotropy + Low-Confidence (Exploratory Only)

| Gene | Anisotropy | pLDDT | PAE Blockiness |
|------|------------|-------|----------------|
| POC5 | 24.69 | 63.97 | 3.51 |
| GHR | 5.13 | 58.70 | 5.31 |
| EMD | 4.29 | 60.25 | 9.13 |
| MESP2 | 4.03 | 54.17 | 0.00 |
| ARNTL | 3.32 | 65.53 | 3.59 |

## LBX1 Comparator Analysis

Comparing LBX1 against key mechanosensors and structural candidates:

| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence Category |
|------|------------|-------|----------------|---------------------|
| LBX1 | 2.27 | 66.87 | 7.35 | Low |
| PIEZO2 | 4.44 | 79.44 | 2.80 | Adequate |
| LMNA | N/A | N/A | N/A | Not in latest snapshot |
| ADGRG6 | 3.06 | 73.73 | 6.78 | Adequate |
| RUNX3 | N/A | N/A | N/A | Not in latest snapshot |
| POC5 | 24.69 | 63.97 | 3.51 | Low |
| GHR | 5.13 | 58.70 | 5.31 | Low |

## Conclusions

- **LBX1 Context**: LBX1 presents an intermediate anisotropy with low structural confidence. Its values are more static than dynamic, suggesting it may not be a primary structural tension rod, but rather a regulatory hub.
- **Reliable Signals**: PIEZO2 and ADGRG6 show both high anisotropy and adequate confidence, making them stronger candidates for direct mechanosensory roles based purely on predicted structure.
- **Caveats**: Candidates like POC5 and GHR show extreme anisotropy but suffer from low confidence. These metrics might reflect intrinsically disordered regions modeled as extended coils by AlphaFold, requiring orthogonal validation.