# Evidence Freshness Audit

## Context
This audit reviews the AFCC metrics generated between `2026-01-09` and `2026-02-16` to determine data provenance and flag potential reuse of static inputs across runs. It checks for identical per-gene vectors, missing linked outputs, and schema drifts.

## Summary
- **Trend window analyzed**: 2026-01-09 to 2026-02-16
- **Total runs in window**: 18
- **Total unique genes across runs**: 227

## Data Reuse Analysis
We examined the metrics `anisotropy_index`, `pLDDT_mean`, and `PAE_domain_blockiness_score` for each gene over time.

- **Static Genes** (identical values across all appearances): 52
- **Dynamic Genes** (values changed at least once): 5
- **Missing Metrics** (genes missing one or more of the core metrics): 0

### Key Findings
- **Identical per-gene vectors**: The majority of structural inferences in recent reports appear to be derived from identical, static underlying metrics (52 genes are static across all runs they appear in).
- **LBX1 Status**: LBX1 was found to be static across the 17 runs it appeared in, confirming that any narrative updates regarding its geometry over this period were not based on new AlphaFold structural data.
- **Missing Linked Outputs**: The following dates were referenced in `reports/afcc_latest.md` but lack corresponding `metrics.csv` files: 2026-01-23.
- **Schema Drifts**: No significant schema drift was detected for the core metrics in the analyzed snapshot window.
- **Narrative over-interpretation risk**: Cluster reports that claim "emerging" or "evolving" structural classes for genes in the 'Static' list are over-interpreting static baseline inputs.

### Core Genes Freshness Audit
- **LBX1**: Static across 17 runs.
- **PIEZO2**: Dynamic across 16 runs.
- **LMNA**: Static across 11 runs.
- **POC5**: Static across 7 runs.
- **GHR**: Static across 6 runs.

