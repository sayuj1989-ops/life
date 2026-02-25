# Evidence Freshness Audit Report
**Date:** 2026-03-12
**Scope:** `outputs/afcc/` from 2026-01-09 to 2026-02-16 (18 runs analyzed)
**Source:** `reports/evidence_freshness_audit_raw.txt`

## Executive Summary
This audit evaluates whether the time-series data in the AFCC outputs represents genuine structural evolution (e.g., new AlphaFold runs, relaxation steps) or the repeated reporting of static cached values.

**Key Finding:** The core structural metrics for **LBX1** (Anisotropy, pLDDT, PAE Blockiness) are **effectively static** across the entire 6-week window. Narrative descriptions implying "evolution" or "emergence" of LBX1 structural features during this period are not supported by the metric changes, which are limited to floating-point noise or metadata updates.

## 1. Schema Stability
*   **Base Schema:** 28 columns (established 2026-01-09).
*   **Drift:** None. The schema has remained consistent across all 18 analyzed files.

## 2. LBX1 Specific Audit
LBX1 appears in 17 of the 18 analyzed runs.

| Date | Anisotropy Index | pLDDT Mean | PAE Blockiness | Status |
| :--- | :--- | :--- | :--- | :--- |
| 2026-01-09 | 2.2664 | 66.8678 | 7.3547 | Baseline |
| 2026-01-14 | 2.2664 | 66.8678 | 7.3547 | Static |
| ... | ... | ... | ... | ... |
| 2026-02-16 | 2.2664 | 66.8678 | 7.3547 | Static |

*Note: Minor floating-point variations (e.g., `2.2664106664642834` vs `2.266410666464284`) are present but structurally negligible.*

**Conclusion:** LBX1 structural data is a single snapshot being re-reported. Any claim of "increasing anisotropy" or "crystallizing blockiness" over this period is **FALSE**.

## 3. General Freshness
*   **Total Genes Analyzed:** 57 (with >1 data point)
*   **Static Vectors:** 2 genes (FLNB, HIF1A) showed bit-for-bit identical vectors across all columns.
*   **Variable Vectors:** 55 genes showed *some* change.
    *   **Nature of Changes:** Most changes are in derived/metadata columns:
        *   `dise_score` (added/updated in later runs)
        *   `plddt_fraction_ok`/`high` (minor binning adjustments)
        *   `charged_patch_score`
        *   `curvature_summary`
    *   **Core Structural Stability:** For most key genes (PIEZO2, ADGRG6, POC5), the core geometric parameters (Anisotropy, Radius of Gyration) are highly stable, showing only minor fluctuations consistent with floating-point non-determinism or minor post-processing tweaks, rather than new folding events.

## 4. Recommendations
1.  **Stop "Trend" Narratives:** Cease describing LBX1 or similar static candidates using temporal verbs ("becoming," "emerging") unless a new AF2 run is explicitly triggered.
2.  **Version Snapshots:** Explicitly tag the underlying PDB/JSON source version in the metrics file to distinguish re-analysis from re-folding.
3.  **Flag Static Data:** Future reports should automatically flag metrics that have not changed by >1% since the previous report to prevent false positives in trend analysis.
