# Confidence-Weighted Structural Evidence

Data snapshot: outputs/afcc/2026-02-16/metrics.csv

## High-Anisotropy + Adequate-Confidence (pLDDT >= 70)
| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Score |
|------|------------|-------|----------------|----------------|
| STOML3 | 5.56 | 84.3 | 0.00 | 4.69 |
| FBLN5 | 7.05 | 83.3 | 3.55 | 4.34 |
| CNNM2 | 8.54 | 70.4 | 4.83 | 4.05 |
| PANX3 | 5.08 | 81.7 | 2.77 | 3.25 |
| PIEZO2 | 4.44 | 79.4 | 2.80 | 2.76 |
| ROCK1 | 3.29 | 76.1 | 4.95 | 1.68 |
| ADGRG6 | 3.06 | 73.7 | 6.78 | 1.34 |

## High-Anisotropy + Low-Confidence (Exploratory Only)
| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Score |
|------|------------|-------|----------------|----------------|
| POC5 | 24.69 | 64.0 | 3.51 | 11.69 |
| MESP2 | 4.03 | 54.2 | 0.00 | 2.18 |
| GHR | 5.13 | 58.7 | 5.31 | 1.97 |
| ARNTL | 3.32 | 65.5 | 3.59 | 1.60 |
| EMD | 4.29 | 60.3 | 9.13 | 1.35 |

## LBX1 Comparator Analysis
Comparison of LBX1 against key anchors (PIEZO2, LMNA, ADGRG6) and low-confidence outliers (POC5, GHR).

| Gene | Anisotropy | pLDDT | PAE Blockiness | Confidence |
|------|------------|-------|----------------|------------|
| ADGRG6 | 3.06 | 73.7 | 6.78 | Adequate |
| GHR | 5.13 | 58.7 | 5.31 | Low |
| LBX1 | 2.27 | 66.9 | 7.35 | Low |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Adequate |
| POC5 | 24.69 | 64.0 | 3.51 | Low |

### Interpretation
- **LBX1 Weakness**: LBX1 remains low confidence (pLDDT < 70) and is structurally intermediate. Its link to mechanosensing via pure geometry is weaker than PIEZO2 or ADGRG6.
- **Strongest Geometries**: CNNM2, FBLN5, and PIEZO2 present the most robust evidence for extended structural mechanosensors based on current modeling.