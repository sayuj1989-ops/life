# Confidence-Weighted Structural Evidence Report

## Overview

This report re-ranks structural candidates by prioritizing adequate-confidence predictions (pLDDT >= 70) over low-confidence predictions. This distinguishes reproducible geometric features from potentially disordered or spurious extended geometries.

**Source Data**: `outputs/afcc/2026-02-16/metrics.csv`


## High-Anisotropy + Adequate-Confidence (Strongest Evidence)

| Gene | Anisotropy | pLDDT | PAE Blockiness |

|------|------------|-------|----------------|
| CNNM2 | 8.54 | 70.4 | 4.83 |
| FBLN5 | 7.05 | 83.3 | 3.55 |
| STOML3 | 5.56 | 84.3 | 0.00 |
| PANX3 | 5.08 | 81.7 | 2.77 |
| PIEZO2 | 4.44 | 79.4 | 2.80 |
| ROCK1 | 3.29 | 76.1 | 4.95 |
| ADGRG6 | 3.06 | 73.7 | 6.78 |

## High-Anisotropy + Low-Confidence (Exploratory Only)

These candidates exhibit high anisotropy but low confidence, suggesting possible extended structures that require experimental validation or ensemble modeling.

| Gene | Anisotropy | pLDDT | PAE Blockiness |

|------|------------|-------|----------------|
| POC5 | 24.69 | 64.0 | 3.51 |
| GHR | 5.13 | 58.7 | 5.31 |
| EMD | 4.29 | 60.3 | 9.13 |
| MESP2 | 4.03 | 54.2 | 0.00 |
| ARNTL | 3.32 | 65.5 | 3.59 |

## LBX1 Comparator Analysis

Analysis of LBX1 relative to key reference proteins to contextualize its structural plausibility:

| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence | Source Run |

|------|------------|-------|----------------|------------|------------|
| LBX1 | 2.27 | 66.9 | 7.35 | Low | 2026-02-16 |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Adequate | 2026-02-16 |
| LMNA | 4.75 | 76.4 | 2.56 | Adequate | 2026-02-26 |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Adequate | 2026-02-16 |
| RUNX3 | 2.06 | 60.6 | 0.00 | Low | 2026-02-18 |
| POC5 | 24.69 | 64.0 | 3.51 | Low | 2026-02-16 |
| GHR | 5.13 | 58.7 | 5.31 | Low | 2026-02-16 |

### Interpretation

- **LBX1** exhibits intermediate anisotropy and low confidence, with high PAE blockiness. This contrasts sharply with robust mechanosensors like **PIEZO2** and **LMNA**, which maintain high anisotropy with adequate confidence.

- **POC5** and **GHR** show extremely high anisotropy but fall into the low-confidence tier, meaning their extended morphologies are currently speculative.

- Any strong mechanical or structural claims regarding LBX1 must be framed as hypotheses requiring experimental confirmation, rather than confirmed geometry.
