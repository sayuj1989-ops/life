# Confidence-Weighted Structural Evidence Report

**Date Generated:** 2026-04-12
**Source Data:** `outputs/afcc/2026-02-16/metrics.csv` (Snapshot from 2026-02-16)

## Overview
This report re-ranks candidates with explicit confidence weighting based on AlphaFold's pLDDT scores and PAE domain blockiness. It isolates strong signals from low-confidence exploratory narrative, penalizing highly blocky structures where global shape is less certain.

## 1. High-Anisotropy + Adequate-Confidence (>70 pLDDT)
These proteins are structurally confident to have an elongated or extended shape.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Anisotropy | Morphology |
|------|------------|-------|----------------|---------------------|------------|
| FBLN5 | 7.05 | 83.3 | 3.55 | 4.84 | Fibrous/Extended |
| STOML3 | 5.56 | 84.3 | 0.00 | 4.69 | Fibrous/Extended |
| CNNM2 | 8.54 | 70.4 | 4.83 | 4.56 | Fibrous/Extended |
| PANX3 | 5.08 | 81.7 | 2.77 | 3.57 | Fibrous/Extended |
| PIEZO2 | 4.44 | 79.4 | 2.80 | 3.03 | Fibrous/Extended |
| ROCK1 | 3.29 | 76.1 | 4.95 | 1.89 | Fibrous/Extended |
| ADGRG6 | 3.06 | 73.7 | 6.78 | 1.49 | Fibrous/Extended |

## 2. High-Anisotropy + Low-Confidence (Exploratory Only)
These proteins exhibit high calculated anisotropy but lack structural confidence. Their "shape" may be an artifact of predicted disordered regions. Avoid strong mechanistic claims here until orthogonally verified.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Anisotropy | Morphology |
|------|------------|-------|----------------|---------------------|------------|
| POC5 | 24.69 | 64.0 | 3.51 | 13.02 | Fibrous/Extended |
| GHR | 5.13 | 58.7 | 5.31 | 2.21 | Fibrous/Extended |
| MESP2 | 4.03 | 54.2 | 0.00 | 2.18 | Fibrous/Extended |
| ARNTL | 3.32 | 65.5 | 3.59 | 1.79 | Fibrous/Extended |
| EMD | 4.29 | 60.3 | 9.13 | 1.40 | Fibrous/Extended |

## 3. LBX1 Comparator Panel
Comparison of LBX1 against key anchor genes to contextualize its structural signal.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Anisotropy | Confidence Class | Signal Status |
|------|------------|-------|----------------|---------------------|------------------|---------------|
| LBX1 | 2.27 | 66.9 | 7.35 | 0.96 | Low | Weak |
| PIEZO2 | 4.44 | 79.4 | 2.80 | 3.03 | Adequate/High | High-anisotropy + adequate-confidence |
| LMNA | N/A | N/A | N/A | N/A | N/A | Not in latest snapshot |
| ADGRG6 | 3.06 | 73.7 | 6.78 | 1.49 | Adequate/High | High-anisotropy + adequate-confidence |
| RUNX3 | N/A | N/A | N/A | N/A | N/A | Not in latest snapshot |
| POC5 | 24.69 | 64.0 | 3.51 | 13.02 | Low | High-anisotropy + low-confidence (exploratory) |
| GHR | 5.13 | 58.7 | 5.31 | 2.21 | Low | High-anisotropy + low-confidence (exploratory) |
