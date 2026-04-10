# Confidence-Weighted Structural Evidence

## Data Provenance
- Date: 2026-02-16 (Authoritative snapshot)
- File: `outputs/afcc/2026-02-16/metrics.csv`

## Ranking Tiers
Thresholds: High Anisotropy >= 3.0, Adequate Confidence >= 70.0 pLDDT.

### 1. High-Anisotropy + Adequate-Confidence (Strongest Signals)
| Gene | Anisotropy | pLDDT | Morphology |
|------|------------|-------|------------|
| CNNM2 | 8.54 | 70.4 | Fibrous/Extended |
| FBLN5 | 7.05 | 83.3 | Fibrous/Extended |
| STOML3 | 5.56 | 84.3 | Fibrous/Extended |
| PANX3 | 5.08 | 81.7 | Fibrous/Extended |
| PIEZO2 | 4.44 | 79.4 | Fibrous/Extended |
| ROCK1 | 3.29 | 76.1 | Fibrous/Extended |
| ADGRG6 | 3.06 | 73.7 | Fibrous/Extended |

### 2. High-Anisotropy + Low-Confidence (Exploratory Only)
| Gene | Anisotropy | pLDDT | Morphology |
|------|------------|-------|------------|
| POC5 | 24.69 | 64.0 | Fibrous/Extended |
| GHR | 5.13 | 58.7 | Fibrous/Extended |
| EMD | 4.29 | 60.3 | Fibrous/Extended |
| MESP2 | 4.03 | 54.2 | Fibrous/Extended |
| ARNTL | 3.32 | 65.5 | Fibrous/Extended |

## LBX1 Comparator Analysis
Comparison against PIEZO2, LMNA, ADGRG6, RUNX3, POC5, GHR.

| Gene | Anisotropy | pLDDT | Confidence Tier | Notes |
|------|------------|-------|-----------------|-------|
| LBX1 | 2.27 | 66.9 | Low | Intermediate/Globular |
| PIEZO2 | 4.44 | 79.4 | Adequate | Strong struct signal |
| LMNA | N/A | N/A | N/A | Not found in snapshot |
| ADGRG6 | 3.06 | 73.7 | Adequate | Strong struct signal |
| RUNX3 | N/A | N/A | N/A | Not found in snapshot |
| POC5 | 24.69 | 64.0 | Low | Exploratory |
| GHR | 5.13 | 58.7 | Low | Exploratory |

## Conclusions
- [Confirmed by metrics] PIEZO2 and ADGRG6 possess solid structural confidence (pLDDT > 70) to ground their anisotropic morphology claims.
- [Supported but uncertain] LBX1 continues to sit below the pLDDT confidence threshold, requiring caution when applying functional narrative directly from computationally derived architecture.
- [Evidence AGAINST / Weakening] Low-confidence predictions (e.g., POC5, GHR, LBX1) introduce high risk if interpreted purely as tension-rods or mechanosensors without validation, weakening the blanket narrative that high computational anisotropy equals biological mechanosensing.