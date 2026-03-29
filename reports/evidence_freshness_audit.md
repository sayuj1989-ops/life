# Evidence Freshness Audit

## Data Integrity
- **Runs Audited**: 31
- **Missing Linked Outputs**: 0 (None)
- **Schema Drifts**: 3 (2026-01-06: missing columns ['anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score'], 2026-01-07: missing columns ['anisotropy_index', 'plddt_mean', 'PAE_domain_blockiness_score'], 2026-02-21: missing columns ['plddt_mean'])

## Static Per-Gene Vectors Across Runs
Identical metrics (anisotropy, pLDDT, PAE blockiness) indicating reused inputs:
| Gene | Runs Present | First Date | Last Date | Anisotropy | pLDDT | PAE Blockiness |
|---|---|---|---|---|---|---|
| LBX1 | 20 | 2026-01-09 | 2026-02-28 | 2.27 | 66.9 | 7.35 |
| NTRK3 | 18 | 2026-01-27 | 2026-03-05 | 1.94 | 76.8 | 6.34 |
| ARNTL | 16 | 2026-02-09 | 2026-03-05 | 3.32 | 65.5 | 3.59 |
| DMD | 16 | 2026-02-09 | 2026-03-05 | 1.32 | 76.3 | 6.91 |
| GHR | 16 | 2026-02-09 | 2026-03-05 | 5.13 | 58.7 | 5.31 |
| IGF1R | 15 | 2026-02-09 | 2026-03-05 | 1.43 | 78.0 | 5.85 |
| PPARGC1A | 15 | 2026-02-09 | 2026-03-05 | 2.19 | 52.7 | 6.56 |
| MYLK | 15 | 2026-02-09 | 2026-03-05 | 1.46 | 65.8 | 8.29 |
| RUNX3 | 14 | 2026-01-27 | 2026-03-05 | 2.06 | 60.6 | 0.00 |
| LMNA | 13 | 2026-01-14 | 2026-02-26 | 4.75 | 76.4 | 2.56 |
| NF1 | 12 | 2026-01-18 | 2026-02-26 | 1.93 | 87.2 | 2.42 |
| OTOP1 | 10 | 2026-01-27 | 2026-02-26 | 1.75 | 75.7 | 1.83 |
| EGR3 | 10 | 2026-01-27 | 2026-02-26 | 3.76 | 50.0 | 0.00 |
| POC5 | 8 | 2026-01-09 | 2026-02-18 | 24.69 | 64.0 | 3.51 |
| IFT88 | 8 | 2026-01-14 | 2026-02-18 | 2.80 | 76.3 | 2.43 |
| ITGB1 | 7 | 2026-01-09 | 2026-02-18 | 3.23 | 85.9 | 4.90 |
| PLOD1 | 7 | 2026-02-05 | 2026-02-26 | 3.40 | 92.7 | 2.31 |
| DAG1 | 7 | 2026-02-17 | 2026-03-05 | 2.39 | 68.2 | 5.63 |
| COL1A1 | 5 | 2026-01-18 | 2026-02-18 | 2.80 | 52.7 | 6.55 |
| HIF1A | 5 | 2026-02-11 | 2026-02-23 | 3.42 | 60.8 | 1.66 |
| METTL3 | 4 | 2026-01-14 | 2026-02-18 | 1.65 | 75.4 | 5.07 |
| FLNA | 4 | 2026-01-20 | 2026-02-18 | 2.50 | 76.5 | 9.88 |
| CEP290 | 4 | 2026-01-20 | 2026-02-18 | 2.29 | 60.5 | 9.06 |
| EMD | 4 | 2026-02-10 | 2026-02-18 | 4.29 | 60.3 | 9.13 |
| MESP2 | 3 | 2026-01-09 | 2026-02-16 | 4.03 | 54.2 | 0.00 |
| WWTR1 | 3 | 2026-01-09 | 2026-02-13 | 2.39 | 59.1 | 5.85 |
| TGFBR2 | 3 | 2026-02-10 | 2026-02-18 | 2.48 | 81.0 | 6.49 |
| MYO7A | 3 | 2026-02-10 | 2026-02-18 | 2.34 | 77.3 | 6.48 |
| CDH23 | 3 | 2026-02-10 | 2026-02-18 | 11.93 | 76.7 | 3.39 |
| FBN2 | 3 | 2026-02-10 | 2026-02-18 | 1.49 | 68.4 | 7.14 |
| SERPINH1 | 3 | 2026-02-10 | 2026-02-18 | 1.97 | 91.1 | 1.24 |
| CCDC57 | 3 | 2026-02-10 | 2026-02-18 | 1.92 | 62.0 | 4.29 |
| ETV1 | 3 | 2026-02-10 | 2026-02-18 | 5.32 | 67.9 | 3.50 |
| ROR2 | 3 | 2026-02-10 | 2026-02-18 | 2.51 | 68.3 | 8.58 |
| FERMT2 | 3 | 2026-02-10 | 2026-02-18 | 2.50 | 79.9 | 5.38 |
| TGFBR1 | 3 | 2026-02-10 | 2026-02-18 | 3.65 | 84.2 | 7.83 |
| BNC2 | 3 | 2026-02-10 | 2026-02-18 | 1.96 | 53.5 | 6.97 |
| ALPL | 3 | 2026-02-17 | 2026-02-23 | 1.63 | 93.3 | 0.00 |
| ACVR1 | 3 | 2026-02-18 | 2026-02-23 | 3.41 | 83.1 | 7.08 |
| FLNB | 2 | 2026-01-09 | 2026-02-10 | 2.25 | 76.3 | 8.93 |
| SMAD3 | 2 | 2026-02-10 | 2026-02-13 | 2.41 | 83.6 | 3.07 |
| ACAN | 2 | 2026-02-10 | 2026-02-13 | 2.66 | 51.9 | 5.01 |
| CCDC40 | 2 | 2026-02-10 | 2026-02-13 | 5.70 | 70.7 | 2.51 |
| KIF7 | 2 | 2026-02-10 | 2026-02-13 | 2.11 | 67.2 | 6.01 |
| KIF3A | 2 | 2026-02-10 | 2026-02-13 | 2.90 | 75.4 | 4.44 |
| SYNE2 | 2 | 2026-02-10 | 2026-02-18 | 2.12 | 83.3 | 1.80 |
| DZIP1 | 2 | 2026-02-10 | 2026-02-16 | 2.54 | 64.4 | 3.83 |
| RPL38 | 2 | 2026-02-10 | 2026-02-18 | 1.52 | 95.3 | 0.00 |
| SUN1 | 2 | 2026-02-10 | 2026-02-18 | 2.34 | 60.4 | 7.01 |
| TLN1 | 2 | 2026-02-10 | 2026-02-13 | 2.04 | 75.9 | 7.60 |
| FBLN5 | 2 | 2026-02-10 | 2026-02-16 | 7.05 | 83.3 | 3.55 |
| COL11A2 | 2 | 2026-02-10 | 2026-02-16 | 2.46 | 49.3 | 5.25 |
| SSPOP | 2 | 2026-02-10 | 2026-02-16 | 1.92 | 60.1 | 8.62 |
| STOML3 | 2 | 2026-02-10 | 2026-02-16 | 5.56 | 84.3 | 0.00 |
| PANX3 | 2 | 2026-02-10 | 2026-02-16 | 5.08 | 81.7 | 2.77 |
| GDF5 | 2 | 2026-02-10 | 2026-02-16 | 2.97 | 70.0 | 3.50 |
| ROCK1 | 2 | 2026-02-10 | 2026-02-16 | 3.29 | 76.1 | 4.95 |
| AQP4 | 2 | 2026-02-10 | 2026-02-16 | 1.97 | 81.0 | 5.21 |
| CNNM2 | 2 | 2026-02-10 | 2026-02-16 | 8.54 | 70.4 | 4.83 |
| NR1D1 | 2 | 2026-02-13 | 2026-02-18 | 1.80 | 62.9 | 5.19 |
| TEAD1 | 2 | 2026-02-13 | 2026-02-18 | 1.91 | 76.5 | 5.61 |
| CLOCK | 2 | 2026-02-13 | 2026-02-18 | 1.83 | 60.6 | 4.03 |
| COL1A2 | 2 | 2026-02-13 | 2026-02-18 | 2.88 | 53.6 | 1.44 |

## Reused Unchanged Values in 'New' Reports
- **2026-01-14**: Reused static metrics for 3 genes (e.g., LBX1, POC5, ITGB1... )
- **2026-01-18**: Reused static metrics for 5 genes (e.g., LBX1, POC5, ITGB1, IFT88, LMNA... )
- **2026-01-20**: Reused static metrics for 5 genes (e.g., LBX1, IFT88, LMNA, NF1, COL1A1... )
- **2026-01-21**: Reused static metrics for 6 genes (e.g., LBX1, POC5, ITGB1, IFT88, LMNA... )
- **2026-01-27**: Reused static metrics for 3 genes (e.g., LBX1, LMNA, NF1... )
- **2026-01-31**: Reused static metrics for 7 genes (e.g., LBX1, LMNA, NF1, NTRK3, RUNX3... )
- **2026-02-05**: Reused static metrics for 7 genes (e.g., LBX1, LMNA, NF1, NTRK3, RUNX3... )
- **2026-02-06**: Reused static metrics for 8 genes (e.g., LBX1, LMNA, NF1, NTRK3, RUNX3... )
- **2026-02-07**: Reused static metrics for 8 genes (e.g., LBX1, LMNA, NF1, NTRK3, RUNX3... )
- **2026-02-08**: Reused static metrics for 7 genes (e.g., LBX1, IFT88, LMNA, NTRK3, RUNX3... )
- **2026-02-09**: Reused static metrics for 3 genes (e.g., LBX1, NTRK3, RUNX3... )
- **2026-02-10**: Reused static metrics for 23 genes (e.g., LBX1, POC5, ITGB1, MESP2, WWTR1... )
- **2026-02-11**: Reused static metrics for 9 genes (e.g., LBX1, NTRK3, RUNX3, ARNTL, DMD... )
- **2026-02-12**: Reused static metrics for 10 genes (e.g., LBX1, NTRK3, RUNX3, ARNTL, DMD... )
- **2026-02-13**: Reused static metrics for 40 genes (e.g., LBX1, POC5, ITGB1, WWTR1, IFT88... )
- **2026-02-16**: Reused static metrics for 21 genes (e.g., LBX1, POC5, MESP2, ARNTL, DMD... )
- **2026-02-17**: Reused static metrics for 8 genes (e.g., NTRK3, RUNX3, ARNTL, DMD, GHR... )
- **2026-02-18**: Reused static metrics for 43 genes (e.g., LBX1, POC5, ITGB1, IFT88, LMNA... )
- **2026-02-20**: Reused static metrics for 9 genes (e.g., NTRK3, ARNTL, DMD, GHR, IGF1R... )
- **2026-02-22**: Reused static metrics for 9 genes (e.g., LBX1, NTRK3, ARNTL, DMD, GHR... )
- **2026-02-23**: Reused static metrics for 10 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A... )
- **2026-02-26**: Reused static metrics for 9 genes (e.g., LMNA, NF1, NTRK3, OTOP1, EGR3... )
- **2026-02-28**: Reused static metrics for 9 genes (e.g., LBX1, NTRK3, ARNTL, DMD, GHR... )
- **2026-03-02**: Reused static metrics for 6 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A... )
- **2026-03-04**: Reused static metrics for 6 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A... )
- **2026-03-05**: Reused static metrics for 9 genes (e.g., NTRK3, RUNX3, ARNTL, DMD, GHR... )

## Conclusion
- Many core candidates (e.g., LBX1, PIEZO2, LMNA) show effectively static metrics across runs.
- **Finding**: Cluster narratives have updated, but underlying structural measurements are reused. We must strictly interpret these signals as low-confidence static anchors rather than evolving measurements.