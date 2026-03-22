# Evidence Freshness Audit

## Context
This audit reviews the AFCC runs from `2026-01-09` to `2026-02-16` to assess data freshness, identify identical per-gene vectors across runs (static metrics), and detect missing linked outputs or schema drift.

## Data Freshness Flags
1. **Identical Per-Gene Vectors Across Runs**:
   - LBX1: Present in 17 runs, static metrics (Aniso=2.27, pLDDT=66.87, PAE_blockiness=7.35).
   - POC5: Present in 7 runs, static metrics (Aniso=24.69, pLDDT=63.97, PAE_blockiness=3.51).
   - LMNA: Present in 11 runs, static metrics (Aniso=4.75, pLDDT=76.37, PAE_blockiness=2.56).
   - GHR: Present in 6 runs, static metrics (Aniso=5.13, pLDDT=58.70, PAE_blockiness=5.31).
   - *Implication*: Narrative updates (like "new" properties or cluster assignments) across these dates are over-interpretations of static data.

2. **Missing Linked Outputs**:
   - No missing linked metrics folders detected in `reports/afcc_latest.md`.
   - 2026-01-20: FBN1 missing in AFDB.

3. **Schema Drift**:
   - No schema drifts were detected across the scoped run window.

## Conclusion
Data outputs have high structural stability but zero temporal evolution for core genes. Narratives should explicitly disavow any implication of metric evolution over the January-February window.
