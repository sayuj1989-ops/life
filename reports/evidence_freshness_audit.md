# Evidence Freshness Audit Report

## Overview
This report audits the AlphaFold Counter-Curvature (AFCC) run history to identify when metrics are reused versus dynamically updated.
Auditing trend window: 2026-01-09 to 2026-02-16 (18 runs detected).

## Schema Drift Analysis
No schema drift detected within scoped window.

## Static Vector Analysis (Identical per-gene vectors)
- **LBX1**: Present in 17 runs with exact identical vector `(anisotropy=2.27, pLDDT=66.87, PAE=7.35)`.
- **POC5**: Present in 7 runs with exact identical vector `(anisotropy=24.69, pLDDT=63.97, PAE=3.51)`.
- **ITGB1**: Present in 6 runs with exact identical vector `(anisotropy=3.23, pLDDT=85.87, PAE=4.90)`.
- **MESP2**: Present in 3 runs with exact identical vector `(anisotropy=4.03, pLDDT=54.17, PAE=0.00)`.
- **WWTR1**: Present in 3 runs with exact identical vector `(anisotropy=2.39, pLDDT=59.14, PAE=5.85)`.
- **FLNB**: Present in 2 runs with exact identical vector `(anisotropy=2.25, pLDDT=76.26, PAE=8.93)`.
- **IFT88**: Present in 7 runs with exact identical vector `(anisotropy=2.80, pLDDT=76.35, PAE=2.43)`.
- **LMNA**: Present in 11 runs with exact identical vector `(anisotropy=4.75, pLDDT=76.37, PAE=2.56)`.
- **METTL3**: Present in 3 runs with exact identical vector `(anisotropy=1.65, pLDDT=75.38, PAE=5.07)`.
- **NF1**: Present in 10 runs with exact identical vector `(anisotropy=1.93, pLDDT=87.17, PAE=2.42)`.
- **COL1A1**: Present in 4 runs with exact identical vector `(anisotropy=2.80, pLDDT=52.73, PAE=6.55)`.
- **FLNA**: Present in 3 runs with exact identical vector `(anisotropy=2.50, pLDDT=76.55, PAE=9.88)`.
- **CEP290**: Present in 3 runs with exact identical vector `(anisotropy=2.29, pLDDT=60.54, PAE=9.06)`.
- **NTRK3**: Present in 11 runs with exact identical vector `(anisotropy=1.94, pLDDT=76.82, PAE=6.34)`.
- **RUNX3**: Present in 11 runs with exact identical vector `(anisotropy=2.06, pLDDT=60.56, PAE=0.00)`.
- **OTOP1**: Present in 8 runs with exact identical vector `(anisotropy=1.75, pLDDT=75.69, PAE=1.83)`.
- **EGR3**: Present in 8 runs with exact identical vector `(anisotropy=3.76, pLDDT=49.97, PAE=0.00)`.
- **PLOD1**: Present in 5 runs with exact identical vector `(anisotropy=3.40, pLDDT=92.73, PAE=2.31)`.
- **ARNTL**: Present in 6 runs with exact identical vector `(anisotropy=3.32, pLDDT=65.53, PAE=3.59)`.
- **DMD**: Present in 6 runs with exact identical vector `(anisotropy=1.32, pLDDT=76.35, PAE=6.91)`.
- **GHR**: Present in 6 runs with exact identical vector `(anisotropy=5.13, pLDDT=58.70, PAE=5.31)`.
- **IGF1R**: Present in 6 runs with exact identical vector `(anisotropy=1.43, pLDDT=78.02, PAE=5.85)`.
- **PPARGC1A**: Present in 6 runs with exact identical vector `(anisotropy=2.19, pLDDT=52.74, PAE=6.56)`.
- **MYLK**: Present in 6 runs with exact identical vector `(anisotropy=1.46, pLDDT=65.85, PAE=8.29)`.
- **TGFBR2**: Present in 2 runs with exact identical vector `(anisotropy=2.48, pLDDT=80.98, PAE=6.49)`.
- **MYO7A**: Present in 2 runs with exact identical vector `(anisotropy=2.34, pLDDT=77.28, PAE=6.48)`.
- **CDH23**: Present in 2 runs with exact identical vector `(anisotropy=11.93, pLDDT=76.73, PAE=3.39)`.
- **FBN2**: Present in 2 runs with exact identical vector `(anisotropy=1.49, pLDDT=68.39, PAE=7.14)`.
- **SERPINH1**: Present in 2 runs with exact identical vector `(anisotropy=1.97, pLDDT=91.14, PAE=1.24)`.
- **ETV1**: Present in 2 runs with exact identical vector `(anisotropy=5.32, pLDDT=67.89, PAE=3.50)`.
- **EMD**: Present in 3 runs with exact identical vector `(anisotropy=4.29, pLDDT=60.25, PAE=9.13)`.
- **ROR2**: Present in 2 runs with exact identical vector `(anisotropy=2.51, pLDDT=68.29, PAE=8.58)`.
- **FERMT2**: Present in 2 runs with exact identical vector `(anisotropy=2.50, pLDDT=79.87, PAE=5.38)`.
- **TGFBR1**: Present in 2 runs with exact identical vector `(anisotropy=3.65, pLDDT=84.19, PAE=7.83)`.
- **SMAD3**: Present in 2 runs with exact identical vector `(anisotropy=2.41, pLDDT=83.61, PAE=3.07)`.
- **ACAN**: Present in 2 runs with exact identical vector `(anisotropy=2.66, pLDDT=51.89, PAE=5.01)`.
- **CCDC40**: Present in 2 runs with exact identical vector `(anisotropy=5.70, pLDDT=70.73, PAE=2.51)`.
- **KIF7**: Present in 2 runs with exact identical vector `(anisotropy=2.11, pLDDT=67.16, PAE=6.01)`.
- **KIF3A**: Present in 2 runs with exact identical vector `(anisotropy=2.90, pLDDT=75.45, PAE=4.44)`.
- **DZIP1**: Present in 2 runs with exact identical vector `(anisotropy=2.54, pLDDT=64.35, PAE=3.83)`.
- **BNC2**: Present in 2 runs with exact identical vector `(anisotropy=1.96, pLDDT=53.50, PAE=6.97)`.
- **TLN1**: Present in 2 runs with exact identical vector `(anisotropy=2.04, pLDDT=75.89, PAE=7.60)`.
- **FBLN5**: Present in 2 runs with exact identical vector `(anisotropy=7.05, pLDDT=83.34, PAE=3.55)`.
- **COL11A2**: Present in 2 runs with exact identical vector `(anisotropy=2.46, pLDDT=49.26, PAE=5.25)`.
- **SSPOP**: Present in 2 runs with exact identical vector `(anisotropy=1.92, pLDDT=60.13, PAE=8.62)`.
- **STOML3**: Present in 2 runs with exact identical vector `(anisotropy=5.56, pLDDT=84.33, PAE=0.00)`.
- **PANX3**: Present in 2 runs with exact identical vector `(anisotropy=5.08, pLDDT=81.72, PAE=2.77)`.
- **GDF5**: Present in 2 runs with exact identical vector `(anisotropy=2.97, pLDDT=69.98, PAE=3.50)`.
- **ROCK1**: Present in 2 runs with exact identical vector `(anisotropy=3.29, pLDDT=76.13, PAE=4.95)`.
- **AQP4**: Present in 2 runs with exact identical vector `(anisotropy=1.97, pLDDT=81.04, PAE=5.21)`.
- **CNNM2**: Present in 2 runs with exact identical vector `(anisotropy=8.54, pLDDT=70.37, PAE=4.83)`.
- **HIF1A**: Present in 3 runs with exact identical vector `(anisotropy=3.42, pLDDT=60.75, PAE=1.66)`.

## Missing Linked Outputs Analysis
All expected metrics.csv files exist in the scoped run folders.

## Conclusion
Frequent metric stasis across runs confirms that the pipeline reuses cached predictions. Narrative updates claiming changes in structural states (e.g. for LBX1, PIEZO2) over this time period are not supported by the underlying data.