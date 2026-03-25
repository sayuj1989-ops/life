# Evidence Freshness Audit
Audit Date: 2026-03-25 19:56:56 UTC
Trend window: 2026-01-09 to 2026-02-16

## Missing Linked Outputs
- **2026-02-16**: Missing summary.md

## Schema Drifts
- **2026-01-09**: Columns mismatch baseline schema (`2026-02-16`).

## Freshness Check: Identical Per-Gene Vectors Across Runs
The following identifies when 'new' runs reused exactly unchanged per-gene values from previous dates (stretches of >1 run).
- **PIEZO2**: Values exactly identical across 2 consecutive runs (2026-01-09 to 2026-01-14).
- **PIEZO2**: Values exactly identical across 12 consecutive runs (2026-01-18 to 2026-02-13).
- **LBX1**: Values exactly identical across 16 consecutive runs (2026-01-09 to 2026-02-13).
- **YAP1**: Values exactly identical across 2 consecutive runs (2026-01-09 to 2026-01-14).
- **YAP1**: Values exactly identical across 3 consecutive runs (2026-01-21 to 2026-02-13).
- **POC5**: Values exactly identical across 6 consecutive runs (2026-01-09 to 2026-02-13).
- **ITGB1**: Values exactly identical across 6 consecutive runs (2026-01-09 to 2026-02-13).
- **MESP2**: Values exactly identical across 2 consecutive runs (2026-01-09 to 2026-02-10).
- **WWTR1**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **ADGRG6**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **FLNB**: Values exactly identical across 2 consecutive runs (2026-01-09 to 2026-02-10).
- **IFT88**: Values exactly identical across 7 consecutive runs (2026-01-14 to 2026-02-13).
- **PIEZO1**: Values exactly identical across 8 consecutive runs (2026-01-18 to 2026-02-13).
- **LMNA**: Values exactly identical across 4 consecutive runs (2026-01-14 to 2026-01-21).
- **LMNA**: Values exactly identical across 7 consecutive runs (2026-01-27 to 2026-02-13).
- **METTL3**: Values exactly identical across 3 consecutive runs (2026-01-14 to 2026-02-13).
- **NF1**: Values exactly identical across 10 consecutive runs (2026-01-18 to 2026-02-13).
- **COL1A1**: Values exactly identical across 4 consecutive runs (2026-01-18 to 2026-02-13).
- **FLNA**: Values exactly identical across 2 consecutive runs (2026-01-20 to 2026-02-10).
- **CEP290**: Values exactly identical across 3 consecutive runs (2026-01-20 to 2026-02-13).
- **NTRK3**: Values exactly identical across 11 consecutive runs (2026-01-27 to 2026-02-13).
- **RUNX3**: Values exactly identical across 11 consecutive runs (2026-01-27 to 2026-02-13).
- **OTOP1**: Values exactly identical across 8 consecutive runs (2026-01-27 to 2026-02-13).
- **EGR3**: Values exactly identical across 8 consecutive runs (2026-01-27 to 2026-02-13).
- **PLOD1**: Values exactly identical across 5 consecutive runs (2026-02-05 to 2026-02-13).
- **ARNTL**: Values exactly identical across 5 consecutive runs (2026-02-09 to 2026-02-13).
- **DMD**: Values exactly identical across 5 consecutive runs (2026-02-09 to 2026-02-13).
- **GHR**: Values exactly identical across 5 consecutive runs (2026-02-09 to 2026-02-13).
- **IGF1R**: Values exactly identical across 5 consecutive runs (2026-02-09 to 2026-02-13).
- **PPARGC1A**: Values exactly identical across 5 consecutive runs (2026-02-09 to 2026-02-13).
- **MYLK**: Values exactly identical across 5 consecutive runs (2026-02-09 to 2026-02-13).
- **TGFBR2**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **CDH23**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **FBN2**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **SERPINH1**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **ETV1**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **ROR2**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **FERMT2**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **TGFBR1**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **SMAD3**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **ACAN**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **CCDC40**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **KIF7**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **KIF3A**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **TLN1**: Values exactly identical across 2 consecutive runs (2026-02-10 to 2026-02-13).
- **HIF1A**: Values exactly identical across 3 consecutive runs (2026-02-11 to 2026-02-13).

## Conclusion & Caveat
- Repeatedly reused vectors falsely inflate evidence weight if interpreted as independent confirmations.
- Reports based on these dates should be explicitly caveated that underlying AFCC metrics for these genes were reused/static.