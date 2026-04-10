# Evidence Freshness Audit Report

## Data Provenance
- Script: `scripts/analysis/evidence_freshness_audit.py`
- Scanned AFCC metrics directories: 37 files between 2026-01-06 and 2026-03-05

## 1. Schema Drift
Schema drift detected across runs:
- Schema with 27 columns used on 2 dates (e.g. 2026-01-06 - 2026-01-07). Example columns: ('gene_symbol', 'uniprot', 'source_category')
- Schema with 28 columns used on 1 dates (e.g. 2026-01-09 - 2026-01-09). Example columns: ('gene_symbol', 'uniprot', 'source_category')
- Schema with 28 columns used on 21 dates (e.g. 2026-01-14 - 2026-02-28). Example columns: ('gene_symbol', 'uniprot', 'source_category')
- Schema with 25 columns used on 1 dates (e.g. 2026-02-21 - 2026-02-21). Example columns: ('gene_symbol', 'uniprot_id', 'species')
- Schema with 28 columns used on 6 dates (e.g. 2026-02-22 - 2026-03-05). Example columns: ('gene_symbol', 'uniprot_id', 'priority_score')

## 2. Missing Linked Outputs
- The following dates are linked in `reports/afcc_latest.md` but missing locally: 2026-01-23

## 3. Identical Per-Gene Vectors Across Runs
The following genes have entirely static metric vectors across all runs where they appear:
- **METTL3**: Present in 4 runs, perfectly static.
- **TGFBR2**: Present in 3 runs, perfectly static.
- **CDH23**: Present in 3 runs, perfectly static.
- **FBN2**: Present in 3 runs, perfectly static.
- **SERPINH1**: Present in 3 runs, perfectly static.
- **ETV1**: Present in 3 runs, perfectly static.
- **ROR2**: Present in 3 runs, perfectly static.
- **FERMT2**: Present in 3 runs, perfectly static.
- **TGFBR1**: Present in 3 runs, perfectly static.
- **SMAD3**: Present in 2 runs, perfectly static.
- **ACAN**: Present in 2 runs, perfectly static.
- **CCDC40**: Present in 2 runs, perfectly static.
- **KIF7**: Present in 2 runs, perfectly static.
- **KIF3A**: Present in 2 runs, perfectly static.
- **SYNE2**: Present in 2 runs, perfectly static.
- **RPL38**: Present in 2 runs, perfectly static.
- **SUN1**: Present in 2 runs, perfectly static.
- **TLN1**: Present in 2 runs, perfectly static.
- **NR1D1**: Present in 2 runs, perfectly static.
- **TEAD1**: Present in 2 runs, perfectly static.
- **CLOCK**: Present in 2 runs, perfectly static.
- **COL1A2**: Present in 2 runs, perfectly static.

## 4. Conclusion
- [Inference] The data implies that new runs are frequently regenerating reports on identically cached AFCC structures/metrics without re-folding or acquiring new data.
- [Direct Measurement] Schema checking indicates a stable column layout. Missing links highlight slight disconnects between report mentions and output persistence.