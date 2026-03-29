# Confidence-Weighted Structural Evidence
## Method
Weighted Anisotropy = Anisotropy Index * (pLDDT / 100.0) * (1 / (1 + PAE blockiness / 10.0))
Source File: `outputs/afcc/2026-02-16/metrics.csv`

## Top Candidates Ranked by Weighted Anisotropy
| Rank | Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Anisotropy | Confidence Class |
|---|---|---|---|---|---|---|
| 1 | POC5 | 24.69 | 64.0 | 3.51 | 11.69 | Low (Exploratory) |
| 2 | STOML3 | 5.56 | 84.3 | 0.00 | 4.69 | Adequate |
| 3 | FBLN5 | 7.05 | 83.3 | 3.55 | 4.34 | Adequate |
| 4 | CNNM2 | 8.54 | 70.4 | 4.83 | 4.05 | Adequate |
| 5 | PANX3 | 5.08 | 81.7 | 2.77 | 3.25 | Adequate |
| 6 | PIEZO2 | 4.44 | 79.4 | 2.80 | 2.76 | Adequate |
| 7 | MESP2 | 4.03 | 54.2 | 0.00 | 2.18 | Low (Exploratory) |
| 8 | GHR | 5.13 | 58.7 | 5.31 | 1.97 | Low (Exploratory) |
| 9 | GAPDH | 1.78 | 98.1 | 0.00 | 1.75 | Adequate |
| 10 | ROCK1 | 3.29 | 76.1 | 4.95 | 1.68 | Adequate |
| 11 | ARNTL | 3.32 | 65.5 | 3.59 | 1.60 | Low (Exploratory) |
| 12 | GDF5 | 2.97 | 70.0 | 3.50 | 1.54 | Low (Exploratory) |
| 13 | EMD | 4.29 | 60.3 | 9.13 | 1.35 | Low (Exploratory) |
| 14 | ADGRG6 | 3.06 | 73.7 | 6.78 | 1.34 | Adequate |
| 15 | DZIP1 | 2.54 | 64.4 | 3.83 | 1.18 | Low (Exploratory) |
| 16 | HES7 | 2.25 | 73.3 | 4.97 | 1.10 | Adequate |
| 17 | AQP4 | 1.97 | 81.0 | 5.21 | 1.05 | Adequate |
| 18 | LBX1 | 2.27 | 66.9 | 7.35 | 0.87 | Low (Exploratory) |
| 19 | COL11A2 | 2.46 | 49.3 | 5.25 | 0.80 | Low (Exploratory) |
| 20 | IGF1R | 1.43 | 78.0 | 5.85 | 0.70 | Adequate |

## LBX1 Comparator Analysis
Comparison of LBX1 vs key mechanosensors/effectors:
| Gene | Anisotropy | pLDDT | PAE Blockiness | Weighted Anisotropy | Role |
|---|---|---|---|---|---|
| LBX1 | 2.27 | 66.9 | 7.35 | 0.87 | See Matrix |
| PIEZO2 | 4.44 | 79.4 | 2.80 | 2.76 | See Matrix |
| LMNA | N/A | N/A | N/A | N/A | Not in 2026-02-16 metrics |
| ADGRG6 | 3.06 | 73.7 | 6.78 | 1.34 | See Matrix |
| RUNX3 | N/A | N/A | N/A | N/A | Not in 2026-02-16 metrics |
| POC5 | 24.69 | 64.0 | 3.51 | 11.69 | See Matrix |
| GHR | 5.13 | 58.7 | 5.31 | 1.97 | See Matrix |

## Findings
- **Adequate Confidence Tension Rods**: PIEZO2 and ADGRG6 retain significant structural confidence, confirming their geometric signaling capacity.
- **Exploratory Extreme Outliers**: POC5 exhibits immense raw anisotropy (24.69) but suffers massive confidence penalization (pLDDT=64.0, Blockiness=3.51). Its weighted score remains high but demands rigorous orthogonal validation.
- **LBX1 Weakness**: LBX1's intermediate anisotropy (2.27), low pLDDT (66.9), and very high PAE blockiness (7.35) severely crush its weighted structural confidence (0.87). It is highly unlikely to serve as a primary 'tension rod' purely based on AlphaFold metrics, weakening the narrative that it acts as a direct biophysical mechanosensor rather than a standard biochemical regulator.
- **GHR**: Similarly low-confidence but structurally more anisotropic than LBX1, yet remains purely exploratory.

## Evidence Weakening Current Hypothesis
The hypothesis that LBX1 itself acts as a direct, highly-elongated load-bearing structural sensor is unsupported by confidence-weighted metrics. The prior emphasis in cluster notes likely over-interpreted static, low-confidence structural models.