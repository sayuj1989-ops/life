# Evidence Freshness Audit Report

## Data Integrity and Freshness
- **Runs Audited**: 37
- **Missing Linked Outputs**: 12 (outputs/afcc/2026-01-06/metrics.csv, outputs/afcc/2026-01-07/metrics.csv, outputs/afcc/2026-01-09/metrics.csv, outputs/afcc/2026-02-05/metrics.csv, outputs/afcc/2026-02-11/metrics.csv, outputs/afcc/2026-02-12/metrics.csv, outputs/afcc/2026-02-16/metrics.csv, outputs/afcc/FOXO3/metrics.csv, outputs/afcc/KLOTHO/metrics.csv, outputs/afcc/manual_longevity/metrics.csv, outputs/afcc/manual_longevity_yap1/metrics.csv, outputs/afcc/manual_metabolic_update/metrics.csv)
- **Schema Drifts**: Detected across scoped files.

## Identical Per-Gene Vectors Across Runs (Static Metrics)
The following genes have identical metrics (anisotropy, pLDDT, PAE blockiness) across multiple runs, indicating reused static inputs rather than fresh measurements:

| Gene | Runs Present | First Date | Last Date | Anisotropy | pLDDT |
|------|--------------|------------|-----------|------------|-------|
| LBX1 | 20 | 2026-01-09 | 2026-02-28 | 2.27 | 66.9 |
| NTRK3 | 18 | 2026-01-27 | 2026-03-05 | 1.94 | 76.8 |
| ARNTL | 17 | 2026-02-09 | manual_metabolic_update | 3.32 | 65.5 |
| DMD | 17 | 2026-02-09 | manual_metabolic_update | 1.32 | 76.3 |
| GHR | 17 | 2026-02-09 | manual_metabolic_update | 5.13 | 58.7 |
| IGF1R | 16 | 2026-02-09 | manual_metabolic_update | 1.43 | 78.0 |
| PPARGC1A | 16 | 2026-02-09 | manual_metabolic_update | 2.19 | 52.7 |
| MYLK | 16 | 2026-02-09 | manual_metabolic_update | 1.46 | 65.8 |
| RUNX3 | 14 | 2026-01-27 | 2026-03-05 | 2.06 | 60.6 |
| LMNA | 13 | 2026-01-14 | 2026-02-26 | 4.75 | 76.4 |
| NF1 | 12 | 2026-01-18 | 2026-02-26 | 1.93 | 87.2 |
| OTOP1 | 10 | 2026-01-27 | 2026-02-26 | 1.75 | 75.7 |
| EGR3 | 10 | 2026-01-27 | 2026-02-26 | 3.76 | 50.0 |
| POC5 | 8 | 2026-01-09 | 2026-02-18 | 24.69 | 64.0 |
| IFT88 | 8 | 2026-01-14 | 2026-02-18 | 2.80 | 76.3 |
| ITGB1 | 7 | 2026-01-09 | 2026-02-18 | 3.23 | 85.9 |
| PLOD1 | 7 | 2026-02-05 | 2026-02-26 | 3.40 | 92.7 |
| DAG1 | 7 | 2026-02-17 | 2026-03-05 | 2.39 | 68.2 |
| COL1A1 | 5 | 2026-01-18 | 2026-02-18 | 2.80 | 52.7 |
| HIF1A | 5 | 2026-02-11 | 2026-02-23 | 3.42 | 60.8 |
| METTL3 | 4 | 2026-01-14 | 2026-02-18 | 1.65 | 75.4 |
| FLNA | 4 | 2026-01-20 | 2026-02-18 | 2.50 | 76.5 |
| CEP290 | 4 | 2026-01-20 | 2026-02-18 | 2.29 | 60.5 |
| EMD | 4 | 2026-02-10 | 2026-02-18 | 4.29 | 60.3 |
| MESP2 | 3 | 2026-01-09 | 2026-02-16 | 4.03 | 54.2 |
| WWTR1 | 3 | 2026-01-09 | 2026-02-13 | 2.39 | 59.1 |
| TGFBR2 | 3 | 2026-02-10 | 2026-02-18 | 2.48 | 81.0 |
| MYO7A | 3 | 2026-02-10 | 2026-02-18 | 2.34 | 77.3 |
| CDH23 | 3 | 2026-02-10 | 2026-02-18 | 11.93 | 76.7 |
| FBN2 | 3 | 2026-02-10 | 2026-02-18 | 1.49 | 68.4 |
| SERPINH1 | 3 | 2026-02-10 | 2026-02-18 | 1.97 | 91.1 |
| ETV1 | 3 | 2026-02-10 | 2026-02-18 | 5.32 | 67.9 |
| ROR2 | 3 | 2026-02-10 | 2026-02-18 | 2.51 | 68.3 |
| FERMT2 | 3 | 2026-02-10 | 2026-02-18 | 2.50 | 79.9 |
| TGFBR1 | 3 | 2026-02-10 | 2026-02-18 | 3.65 | 84.2 |
| BNC2 | 3 | 2026-02-10 | 2026-02-18 | 1.96 | 53.5 |
| ALPL | 3 | 2026-02-17 | 2026-02-23 | 1.63 | 93.3 |
| ACVR1 | 3 | 2026-02-18 | 2026-02-23 | 3.41 | 83.1 |
| FLNB | 2 | 2026-01-09 | 2026-02-10 | 2.25 | 76.3 |
| SMAD3 | 2 | 2026-02-10 | 2026-02-13 | 2.41 | 83.6 |
| ACAN | 2 | 2026-02-10 | 2026-02-13 | 2.66 | 51.9 |
| CCDC40 | 2 | 2026-02-10 | 2026-02-13 | 5.70 | 70.7 |
| KIF7 | 2 | 2026-02-10 | 2026-02-13 | 2.11 | 67.2 |
| KIF3A | 2 | 2026-02-10 | 2026-02-13 | 2.90 | 75.4 |
| SYNE2 | 2 | 2026-02-10 | 2026-02-18 | 2.12 | 83.3 |
| DZIP1 | 2 | 2026-02-10 | 2026-02-16 | 2.54 | 64.4 |
| RPL38 | 2 | 2026-02-10 | 2026-02-18 | 1.52 | 95.3 |
| SUN1 | 2 | 2026-02-10 | 2026-02-18 | 2.34 | 60.4 |
| TLN1 | 2 | 2026-02-10 | 2026-02-13 | 2.04 | 75.9 |
| FBLN5 | 2 | 2026-02-10 | 2026-02-16 | 7.05 | 83.3 |
| COL11A2 | 2 | 2026-02-10 | 2026-02-16 | 2.46 | 49.3 |
| SSPOP | 2 | 2026-02-10 | 2026-02-16 | 1.92 | 60.1 |
| STOML3 | 2 | 2026-02-10 | 2026-02-16 | 5.56 | 84.3 |
| PANX3 | 2 | 2026-02-10 | 2026-02-16 | 5.08 | 81.7 |
| GDF5 | 2 | 2026-02-10 | 2026-02-16 | 2.97 | 70.0 |
| ROCK1 | 2 | 2026-02-10 | 2026-02-16 | 3.29 | 76.1 |
| AQP4 | 2 | 2026-02-10 | 2026-02-16 | 1.97 | 81.0 |
| CNNM2 | 2 | 2026-02-10 | 2026-02-16 | 8.54 | 70.4 |
| NR1D1 | 2 | 2026-02-13 | 2026-02-18 | 1.80 | 62.9 |
| TEAD1 | 2 | 2026-02-13 | 2026-02-18 | 1.91 | 76.5 |
| CLOCK | 2 | 2026-02-13 | 2026-02-18 | 1.83 | 60.6 |
| COL1A2 | 2 | 2026-02-13 | 2026-02-18 | 2.88 | 53.6 |

## When 'New' Reports Reuse Unchanged Values
- **2026-01-14**: Reused static metrics for 3 genes (e.g., LBX1, POC5, ITGB1)
- **2026-01-18**: Reused static metrics for 5 genes (e.g., LBX1, POC5, ITGB1, IFT88, LMNA)
- **2026-01-20**: Reused static metrics for 5 genes (e.g., LBX1, IFT88, LMNA, NF1, COL1A1)
- **2026-01-21**: Reused static metrics for 6 genes (e.g., LBX1, POC5, ITGB1, IFT88, LMNA...)
- **2026-01-27**: Reused static metrics for 3 genes (e.g., LBX1, LMNA, NF1)
- **2026-01-31**: Reused static metrics for 7 genes (e.g., LBX1, LMNA, NF1, NTRK3, RUNX3...)
- **2026-02-05**: Reused static metrics for 7 genes (e.g., LBX1, LMNA, NF1, NTRK3, RUNX3...)
- **2026-02-06**: Reused static metrics for 8 genes (e.g., LBX1, LMNA, NF1, NTRK3, RUNX3...)
- **2026-02-07**: Reused static metrics for 8 genes (e.g., LBX1, LMNA, NF1, NTRK3, RUNX3...)
- **2026-02-08**: Reused static metrics for 7 genes (e.g., LBX1, IFT88, LMNA, NTRK3, RUNX3...)
- **2026-02-09**: Reused static metrics for 3 genes (e.g., LBX1, NTRK3, RUNX3)
- **2026-02-10**: Reused static metrics for 23 genes (e.g., LBX1, POC5, ITGB1, MESP2, WWTR1...)
- **2026-02-11**: Reused static metrics for 9 genes (e.g., LBX1, NTRK3, RUNX3, ARNTL, DMD...)
- **2026-02-12**: Reused static metrics for 10 genes (e.g., LBX1, NTRK3, RUNX3, ARNTL, DMD...)
- **2026-02-13**: Reused static metrics for 39 genes (e.g., LBX1, POC5, ITGB1, WWTR1, IFT88...)
- **2026-02-16**: Reused static metrics for 21 genes (e.g., LBX1, POC5, MESP2, ARNTL, DMD...)
- **2026-02-17**: Reused static metrics for 8 genes (e.g., NTRK3, RUNX3, ARNTL, DMD, GHR...)
- **2026-02-18**: Reused static metrics for 42 genes (e.g., LBX1, POC5, ITGB1, IFT88, LMNA...)
- **2026-02-20**: Reused static metrics for 9 genes (e.g., NTRK3, ARNTL, DMD, GHR, IGF1R...)
- **2026-02-22**: Reused static metrics for 9 genes (e.g., LBX1, NTRK3, ARNTL, DMD, GHR...)
- **2026-02-23**: Reused static metrics for 10 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A...)
- **2026-02-26**: Reused static metrics for 9 genes (e.g., LMNA, NF1, NTRK3, OTOP1, EGR3...)
- **2026-02-28**: Reused static metrics for 9 genes (e.g., LBX1, NTRK3, ARNTL, DMD, GHR...)
- **2026-03-02**: Reused static metrics for 6 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A...)
- **2026-03-04**: Reused static metrics for 6 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A...)
- **2026-03-05**: Reused static metrics for 9 genes (e.g., NTRK3, RUNX3, ARNTL, DMD, GHR...)
- **manual_metabolic_update**: Reused static metrics for 6 genes (e.g., ARNTL, DMD, GHR, IGF1R, PPARGC1A...)

## Conclusion
- **Actionable Insight**: Many core candidates (e.g., LBX1, PIEZO2, LMNA) show static values across the trend window. This confirms the caveat that high-anisotropy narratves may over-interpret static inputs.