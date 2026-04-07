# Evidence Freshness Audit

## Overview
Audit of AFCC run history to detect reused/static metrics, schema drifts, and missing outputs.

## Missing Outputs
- No missing metrics.csv files found.

## Schema Drifts
- No schema drifts found.

## Identical Per-Gene Vectors Across Runs
Warning: The following genes exhibit identical structural metrics (anisotropy and pLDDT) across consecutive dates, suggesting cached/static reuse rather than fresh analysis.

| Gene | Consecutive Reuses | Example Anisotropy | Example pLDDT |
|---|---|---|---|
| PIEZO2 | 16 | 4.441176983762356 | 79.4436389280677 |
| LBX1 | 15 | 2.266410666464284 | 66.86779359430605 |
| DMD | 14 | 1.3155342721236885 | 76.34927619047619 |
| ARNTL | 14 | 3.3192797281217827 | 65.52864217252394 |
| GHR | 14 | 5.13247062540886 | 58.69753918495297 |
| NTRK3 | 13 | 1.936111715585754 | 76.81557806912993 |
| PPARGC1A | 12 | 2.185052241061399 | 52.74286967418547 |
| IGF1R | 12 | 1.426632071596987 | 78.01789319678127 |
| MYLK | 12 | 1.4640526080343412 | 65.84507314524556 |
| RUNX3 | 11 | 2.0611670656856456 | 60.564096385542165 |
| LMNA | 8 | 4.751667397697646 | 76.37072289156627 |
| NF1 | 7 | 1.9279279346731688 | 87.17264755480608 |
| PIEZO1 | 6 | 3.896259474160542 | 72.0459182863943 |
| EGR3 | 5 | 3.762072398804325 | 49.96868217054263 |
| OTOP1 | 5 | 1.7507094616744632 | 75.68916666666668 |
| DAG1 | 3 | 2.3890770817089004 | 68.17016759776536 |
| PLOD1 | 2 | 3.3950779336885484 | 92.72865199449797 |
| POC5 | 2 | 24.686435126462467 | 63.974834782608696 |
| YAP1 | 2 | 1.9895190619317915 | 57.40202380952381 |
| IFT88 | 2 | 2.8032400603850034 | 76.34603155339805 |
