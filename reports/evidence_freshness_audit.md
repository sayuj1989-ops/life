# Evidence Freshness Audit Report

## Data Integrity and Freshness
- **Runs Audited**: 31
- **Missing Linked Outputs**: 0 (None)
- **Schema Drifts Detected**: 2
  - 2026-01-06 missing columns: anisotropy_index, pLDDT_mean, PAE_domain_blockiness_score
  - 2026-01-07 missing columns: anisotropy_index, pLDDT_mean, PAE_domain_blockiness_score

## Identical Per-Gene Vectors Across Runs (Static Metrics)
The following genes have identical metrics (anisotropy, pLDDT, PAE blockiness) across all their runs, indicating reused static inputs rather than fresh measurements:

| Gene | Runs Present | First Date | Last Date | Anisotropy | pLDDT |
|------|--------------|------------|-----------|------------|-------|
| LBX1 | 20 | 2026-01-09 | 2026-02-28 | 2.27 | 66.87 |
| NTRK3 | 18 | 2026-01-27 | 2026-03-05 | 1.94 | 76.82 |
| RUNX3 | 14 | 2026-01-27 | 2026-03-05 | 2.06 | 60.56 |
| LMNA | 13 | 2026-01-14 | 2026-02-26 | 4.75 | 76.37 |
| NF1 | 12 | 2026-01-18 | 2026-02-26 | 1.93 | 87.17 |
| OTOP1 | 10 | 2026-01-27 | 2026-02-26 | 1.75 | 75.69 |
| EGR3 | 10 | 2026-01-27 | 2026-02-26 | 3.76 | 49.97 |
| POC5 | 8 | 2026-01-09 | 2026-02-18 | 24.69 | 63.97 |
| IFT88 | 8 | 2026-01-14 | 2026-02-18 | 2.80 | 76.35 |
| ITGB1 | 7 | 2026-01-09 | 2026-02-18 | 3.23 | 85.87 |
| PLOD1 | 7 | 2026-02-05 | 2026-02-26 | 3.40 | 92.73 |
| COL1A1 | 5 | 2026-01-18 | 2026-02-18 | 2.80 | 52.73 |
| HIF1A | 5 | 2026-02-11 | 2026-02-23 | 3.42 | 60.75 |
| METTL3 | 4 | 2026-01-14 | 2026-02-18 | 1.65 | 75.38 |
| FLNA | 4 | 2026-01-20 | 2026-02-18 | 2.50 | 76.55 |
| CEP290 | 4 | 2026-01-20 | 2026-02-18 | 2.29 | 60.54 |
| EMD | 4 | 2026-02-10 | 2026-02-18 | 4.29 | 60.25 |
| MESP2 | 3 | 2026-01-09 | 2026-02-16 | 4.03 | 54.17 |
| WWTR1 | 3 | 2026-01-09 | 2026-02-13 | 2.39 | 59.14 |
| TGFBR2 | 3 | 2026-02-10 | 2026-02-18 | 2.48 | 80.98 |
| MYO7A | 3 | 2026-02-10 | 2026-02-18 | 2.34 | 77.28 |
| CDH23 | 3 | 2026-02-10 | 2026-02-18 | 11.93 | 76.73 |
| FBN2 | 3 | 2026-02-10 | 2026-02-18 | 1.49 | 68.39 |
| SERPINH1 | 3 | 2026-02-10 | 2026-02-18 | 1.97 | 91.14 |
| ETV1 | 3 | 2026-02-10 | 2026-02-18 | 5.32 | 67.89 |
| ROR2 | 3 | 2026-02-10 | 2026-02-18 | 2.51 | 68.29 |
| FERMT2 | 3 | 2026-02-10 | 2026-02-18 | 2.50 | 79.87 |
| TGFBR1 | 3 | 2026-02-10 | 2026-02-18 | 3.65 | 84.19 |
| BNC2 | 3 | 2026-02-10 | 2026-02-18 | 1.96 | 53.50 |
| FLNB | 2 | 2026-01-09 | 2026-02-10 | 2.25 | 76.26 |
| SMAD3 | 2 | 2026-02-10 | 2026-02-13 | 2.41 | 83.61 |
| ACAN | 2 | 2026-02-10 | 2026-02-13 | 2.66 | 51.89 |
| CCDC40 | 2 | 2026-02-10 | 2026-02-13 | 5.70 | 70.73 |
| KIF7 | 2 | 2026-02-10 | 2026-02-13 | 2.11 | 67.16 |
| KIF3A | 2 | 2026-02-10 | 2026-02-13 | 2.90 | 75.45 |
| SYNE2 | 2 | 2026-02-10 | 2026-02-18 | 2.12 | 83.33 |
| DZIP1 | 2 | 2026-02-10 | 2026-02-16 | 2.54 | 64.35 |
| RPL38 | 2 | 2026-02-10 | 2026-02-18 | 1.52 | 95.35 |
| SUN1 | 2 | 2026-02-10 | 2026-02-18 | 2.34 | 60.36 |
| TLN1 | 2 | 2026-02-10 | 2026-02-13 | 2.04 | 75.89 |
| FBLN5 | 2 | 2026-02-10 | 2026-02-16 | 7.05 | 83.34 |
| COL11A2 | 2 | 2026-02-10 | 2026-02-16 | 2.46 | 49.26 |
| SSPOP | 2 | 2026-02-10 | 2026-02-16 | 1.92 | 60.13 |
| STOML3 | 2 | 2026-02-10 | 2026-02-16 | 5.56 | 84.33 |
| PANX3 | 2 | 2026-02-10 | 2026-02-16 | 5.08 | 81.72 |
| GDF5 | 2 | 2026-02-10 | 2026-02-16 | 2.97 | 69.98 |
| ROCK1 | 2 | 2026-02-10 | 2026-02-16 | 3.29 | 76.13 |
| AQP4 | 2 | 2026-02-10 | 2026-02-16 | 1.97 | 81.04 |
| CNNM2 | 2 | 2026-02-10 | 2026-02-16 | 8.54 | 70.37 |
| NR1D1 | 2 | 2026-02-13 | 2026-02-18 | 1.80 | 62.89 |
| TEAD1 | 2 | 2026-02-13 | 2026-02-18 | 1.91 | 76.48 |
| CLOCK | 2 | 2026-02-13 | 2026-02-18 | 1.83 | 60.61 |
| COL1A2 | 2 | 2026-02-13 | 2026-02-18 | 2.88 | 53.64 |

## When 'New' Reports Reuse Unchanged Values

- **2026-01-14**: Reused static metrics for 5 genes (e.g., PIEZO2, LBX1, YAP1, POC5, ITGB1)
- **2026-01-18**: Reused static metrics for 5 genes (e.g., LBX1, POC5, ITGB1, IFT88, LMNA)
- **2026-01-20**: Reused static metrics for 7 genes (e.g., PIEZO2, LBX1, IFT88, PIEZO1, LMNA...)
- **2026-01-21**: Reused static metrics for 8 genes (e.g., PIEZO2, LBX1, POC5, ITGB1, IFT88...)
- **2026-01-27**: Reused static metrics for 5 genes (e.g., PIEZO2, LBX1, PIEZO1, LMNA, NF1)
- **2026-01-31**: Reused static metrics for 9 genes (e.g., PIEZO2, LBX1, PIEZO1, LMNA, NF1...)
- **2026-02-05**: Reused static metrics for 8 genes (e.g., PIEZO2, LBX1, LMNA, NF1, NTRK3...)
- **2026-02-06**: Reused static metrics for 9 genes (e.g., PIEZO2, LBX1, LMNA, NF1, NTRK3...)
- **2026-02-07**: Reused static metrics for 9 genes (e.g., PIEZO2, LBX1, LMNA, NF1, NTRK3...)
- **2026-02-08**: Reused static metrics for 9 genes (e.g., PIEZO2, LBX1, IFT88, PIEZO1, LMNA...)
- **2026-02-09**: Reused static metrics for 4 genes (e.g., PIEZO2, LBX1, NTRK3, RUNX3)
- **2026-02-10**: Reused static metrics for 26 genes (e.g., PIEZO2, LBX1, YAP1, POC5, ITGB1...)
- **2026-02-11**: Reused static metrics for 9 genes (e.g., LBX1, NTRK3, RUNX3, ARNTL, DMD...)
- **2026-02-12**: Reused static metrics for 10 genes (e.g., LBX1, NTRK3, RUNX3, ARNTL, DMD...)
- **2026-02-13**: Reused static metrics for 43 genes (e.g., PIEZO2, LBX1, YAP1, POC5, ITGB1...)
- **2026-02-16**: Reused static metrics for 22 genes (e.g., PIEZO2, LBX1, POC5, MESP2, ARNTL...)
- **2026-02-17**: Reused static metrics for 8 genes (e.g., NTRK3, RUNX3, ARNTL, DMD, GHR...)
- **2026-02-18**: Reused static metrics for 46 genes (e.g., PIEZO2, LBX1, YAP1, POC5, ITGB1...)
- **2026-02-20**: Reused static metrics for 10 genes (e.g., PIEZO2, NTRK3, ARNTL, DMD, GHR...)
- **2026-02-22**: Reused static metrics for 3 genes (e.g., PIEZO2, LBX1, NTRK3)
- **2026-02-23**: Reused static metrics for 8 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A...)
- **2026-02-26**: Reused static metrics for 10 genes (e.g., PIEZO2, LMNA, NF1, NTRK3, OTOP1...)
- **2026-02-28**: Reused static metrics for 10 genes (e.g., PIEZO2, LBX1, NTRK3, ARNTL, DMD...)
- **2026-03-02**: Reused static metrics for 6 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A...)
- **2026-03-04**: Reused static metrics for 6 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A...)
- **2026-03-05**: Reused static metrics for 9 genes (e.g., NTRK3, RUNX3, ARNTL, DMD, GHR...)

## Conclusion
- **Actionable Insight**: The audit confirms that many candidates (including core ones) reuse static values across the trend window. This underlines the core caveat: high-anisotropy narratives in these reports may over-interpret static structural inputs rather than reflecting new experimental measurements or evolving geometric estimates.
