# Evidence Freshness Audit

## Audit Scope
- Trend window: 2026-01-09 to 2026-02-16
- Directories checked: 18
- Missing metrics.csv outputs: 0 (None)

## Data Reuse Findings
- Total unique genes evaluated: 227
- Genes with perfectly static metrics across multiple runs: 56
- Total instances of reused identical vectors: 194

## Schema Drift
- No significant schema drift detected preventing extraction of core metrics.

## Flagged Static Genes
The following genes show identical per-gene vectors across all their evaluated runs, indicating reused/static metrics rather than fresh structural evidence:
ACAN, AQP4, ARNTL, BNC2, CCDC40, CCDC57, CDH23, CEP290, CNNM2, COL11A2, COL1A1, DMD, DZIP1, EGR3, EMD, ETV1, FBLN5, FBN2, FERMT2, FLNA, FLNB, GDF5, GHR, HIF1A, IFT88, IGF1R, ITGB1, KIF3A, KIF7, LBX1, LMNA, MESP2, METTL3, MYLK, MYO7A, NF1, NTRK3, OTOP1, PANX3, PIEZO1, PIEZO2, PLOD1, POC5, PPARGC1A, ROCK1, ROR2, RUNX3, SERPINH1, SMAD3, SSPOP, STOML3, TGFBR1, TGFBR2, TLN1, WWTR1, YAP1

## Conclusion
Many "new" reports in the trend window simply reused unchanged per-gene values. Cluster narratives interpreting changing shapes over time are likely over-interpreting static inputs.
