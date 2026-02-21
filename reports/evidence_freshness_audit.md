# Evidence Freshness Audit Report
Generated on: 2026-02-21 19:44:31

## Run-to-Run Consistency Check
| Date | Rows | Columns | Identical to Prev? | Changes |
|---|---|---|---|---|
| 2026-01-06 | 10 | 40 | False | N/A |
| 2026-01-07 | 9 | 40 | False | Row count: 10 -> 9 |
| 2026-01-09 | 9 | 40 | False | Changed cols: morphology, anisotropy, radius_of_gyration... |
| 2026-01-14 | 9 | 40 | False | Changed cols: gene_symbol, uniprot, source_category... |
| 2026-01-16 | 3 | 40 | False | Row count: 9 -> 3 |
| 2026-01-18 | 9 | 40 | False | Row count: 3 -> 9 |
| 2026-01-20 | 9 | 40 | False | Changed cols: gene_symbol, uniprot, source_category... |
| 2026-01-21 | 9 | 40 | False | Changed cols: gene_symbol, uniprot, source_category... |
| 2026-01-27 | 9 | 40 | False | Changed cols: gene_symbol, uniprot, source_category... |
| 2026-01-31 | 9 | 40 | True | None |
| 2026-02-05 | 9 | 40 | False | Changed cols: gene_symbol, uniprot, radius_of_gyration... |
| 2026-02-06 | 9 | 40 | True | None |
| 2026-02-07 | 9 | 40 | False | Changed cols: source_category... |
| 2026-02-08 | 9 | 40 | False | Changed cols: gene_symbol, uniprot, source_category... |
| 2026-02-09 | 10 | 40 | False | Row count: 9 -> 10 |
| 2026-02-10 | 219 | 40 | False | Row count: 10 -> 219 |
| 2026-02-11 | 10 | 40 | False | Row count: 219 -> 10 |
| 2026-02-12 | 10 | 40 | True | None |
| 2026-02-13 | 48 | 40 | False | Row count: 10 -> 48 |
| 2026-02-16 | 25 | 40 | False | Row count: 48 -> 25 |
| 2026-02-17 | 10 | 40 | False | Row count: 25 -> 10 |
| 2026-02-18 | 58 | 40 | False | Row count: 10 -> 58 |
| 2026-02-20 | 10 | 40 | False | Row count: 58 -> 10 |

## Gene-Level Freshness
Checking for genes that have static metrics across multiple runs (indicating potential reuse or lack of update).
- Total Genes Tracked: 71
- Static Genes (Unchanged across runs): 70
- Dynamic Genes (Changed at least once): 1

### Top 10 Static Genes (Most Runs)
| Gene     |   Runs | First_Run   | Last_Run   | Status   | Anisotropy_Range   |
|:---------|-------:|:------------|:-----------|:---------|:-------------------|
| PIEZO2   |     20 | 2026-01-06  | 2026-02-20 | Static   | 4.44-4.44          |
| LBX1     |     20 | 2026-01-06  | 2026-02-18 | Static   | 2.27-2.27          |
| NTRK3    |     14 | 2026-01-27  | 2026-02-20 | Static   | 1.94-1.94          |
| RUNX3    |     13 | 2026-01-27  | 2026-02-18 | Static   | 2.06-2.06          |
| LMNA     |     12 | 2026-01-14  | 2026-02-18 | Static   | 4.75-4.75          |
| PIEZO1   |     11 | 2026-01-14  | 2026-02-18 | Static   | 3.90-3.90          |
| NF1      |     11 | 2026-01-18  | 2026-02-18 | Static   | 1.93-1.93          |
| POC5     |     10 | 2026-01-06  | 2026-02-18 | Static   | 24.69-24.69        |
| MYLK     |      9 | 2026-02-09  | 2026-02-20 | Static   | 1.46-1.46          |
| PPARGC1A |      9 | 2026-02-09  | 2026-02-20 | Static   | 2.19-2.19          |

### Top 10 Dynamic Genes (Most Variability)
| Gene   |   Runs | First_Run   | Last_Run   | Status   | Anisotropy_Range   |
|:-------|-------:|:------------|:-----------|:---------|:-------------------|
| ADGRG6 |      6 | 2026-01-06  | 2026-02-16 | Dynamic  | 2.69-3.06          |

### Key Candidate Status
| Gene   |   Runs | First_Run   | Last_Run   | Status   | Anisotropy_Range   |
|:-------|-------:|:------------|:-----------|:---------|:-------------------|
| PIEZO2 |     20 | 2026-01-06  | 2026-02-20 | Static   | 4.44-4.44          |
| LBX1   |     20 | 2026-01-06  | 2026-02-18 | Static   | 2.27-2.27          |
| POC5   |     10 | 2026-01-06  | 2026-02-18 | Static   | 24.69-24.69        |
| LMNA   |     12 | 2026-01-14  | 2026-02-18 | Static   | 4.75-4.75          |
| GHR    |      9 | 2026-02-09  | 2026-02-20 | Static   | 5.13-5.13          |