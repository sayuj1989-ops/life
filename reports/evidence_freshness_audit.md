# Evidence Freshness Audit Report

- **Audit Date:** 2026-03-05 19:43:32 UTC
- **Time Window:** 2026-01-09 to 2026-02-16
- **Total Runs Audited:** 18
- **Data Source:** `outputs/afcc/*/metrics.csv`

## 1. Schema Drift Analysis
Detected 17 schema drifts.
- **2026-01-14**: Differs from baseline.
- **2026-01-16**: Differs from baseline.
- **2026-01-18**: Differs from baseline.
- **2026-01-20**: Differs from baseline.
- **2026-01-21**: Differs from baseline.
- **2026-01-27**: Differs from baseline.
- **2026-01-31**: Differs from baseline.
- **2026-02-05**: Differs from baseline.
- **2026-02-06**: Differs from baseline.
- **2026-02-07**: Differs from baseline.
- **2026-02-08**: Differs from baseline.
- **2026-02-09**: Differs from baseline.
- **2026-02-10**: Differs from baseline.
- **2026-02-11**: Differs from baseline.
- **2026-02-12**: Differs from baseline.
- **2026-02-13**: Differs from baseline.
- **2026-02-16**: Differs from baseline.

## 2. Missing Linked Outputs
Found 1 runs missing `summary.md`:
- `2026-02-16`

## 3. Identical Per-Gene Vectors Across Runs (Static Metrics)
The following genes appear multiple times with **identical** metric vectors (no new computational inference):

| Gene | Total Appearances | Static Appearances | % Static |
|------|-------------------|--------------------|----------|
| LBX1 | 17 | 8 | 50.0% |
| PIEZO2 | 16 | 6 | 40.0% |
| LMNA | 11 | 7 | 70.0% |
| NTRK3 | 11 | 6 | 60.0% |
| RUNX3 | 11 | 6 | 60.0% |
| PIEZO1 | 10 | 3 | 33.3% |
| NF1 | 10 | 5 | 55.6% |
| OTOP1 | 8 | 4 | 57.1% |
| EGR3 | 8 | 4 | 57.1% |
| POC5 | 7 | 1 | 16.7% |
| IFT88 | 7 | 2 | 33.3% |
| ITGB1 | 6 | 1 | 20.0% |
| ARNTL | 6 | 2 | 40.0% |
| DMD | 6 | 2 | 40.0% |
| GHR | 6 | 2 | 40.0% |
| IGF1R | 6 | 2 | 40.0% |
| PPARGC1A | 6 | 2 | 40.0% |
| MYLK | 6 | 2 | 40.0% |
| PLOD1 | 5 | 1 | 25.0% |
| COL1A1 | 4 | 1 | 33.3% |
| WWTR1 | 3 | 1 | 50.0% |
| METTL3 | 3 | 1 | 50.0% |
| HIF1A | 3 | 2 | 100.0% |

### Spotlight: Core Mechanosensors & LBX1
- **LBX1**: 8 static re-appearances out of 17 total (50.0% static).
- **PIEZO2**: 6 static re-appearances out of 16 total (40.0% static).
- **LMNA**: 7 static re-appearances out of 11 total (70.0% static).
- **POC5**: 1 static re-appearances out of 7 total (16.7% static).
- **GHR**: 2 static re-appearances out of 6 total (40.0% static).

## 4. Conclusion
- **[Measurement vs Inference]** Many core genes (e.g., LBX1, PIEZO2) show completely static metric vectors across runs. Narrative updates on these genes during this window reflect hypothesis exploration rather than new structural measurements.
- **[Data Freshness]** Future pipeline runs should tag records as 'cached' vs 'recomputed' to prevent conflating static reuse with independent replication.
