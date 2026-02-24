# Evidence Freshness Audit Report
**Date:** 2026-03-06
**Scope:** Audit of `outputs/afcc/*/metrics.csv` for data staleness and schema drift.
**Method:** `scripts/analysis/evidence_freshness_audit.py`

## Executive Summary
The "Daily Refresh" pipeline exhibits a bimodal behavior:
1.  **Static Legacy Data**: Core structural candidates (PIEZO2, LBX1, LMNA) have shown **identical metric values** for over 20 runs (since Jan 2026). This indicates they are being reported from cache without re-computation, or the underlying computation code has not changed for them.
2.  **Active Metabolic Update**: A subset of candidates (ARNTL, DMD, GHR, IGF1R, PPARGC1A, MYLK) shows **significant metric changes** and schema evolution between Feb 20-23, 2026. This correlates with the "Metabolic Buckling" hypothesis development.

**Critical Risk**: The evidence for the core "Countercurvature" candidates (LBX1, PIEZO2) is **stale**. Recent improvements in metric calculation (evident in the metabolic set) have likely *not* been applied to these core drivers.

## Detailed Findings

### 1. Static Candidates (Potential Stale Evidence)
The following key candidates have had **zero metric changes** across all observed transitions (>20 runs for some), suggesting no re-analysis has occurred despite codebase evolution:
*   **LBX1**: Static since Jan 06 (22 runs).
*   **PIEZO2**: Static since Jan 06 (22 runs).
*   **LMNA**: Static since Jan 14 (12 runs).
*   **IFT88**: Static since Jan 14 (8 runs).
*   **NF1**: Static since Jan 18 (11 runs).

**Implication**: Claims about these proteins are based on code/metrics from early January. If the pipeline has improved (e.g., better anisotropy calculation, new confidence weighting), these candidates are **out of date**.

### 2. Active Development (Fresh Evidence)
The following candidates show recent activity (metric changes) in late Feb (Feb 20-23), indicating they are the focus of recent work:
*   **ARNTL**
*   **DMD**
*   **GHR**
*   **IGF1R**
*   **PPARGC1A**
*   **MYLK**

**Implication**: The "Metabolic" evidence is fresher and likely uses more robust/recent metric definitions than the "Structural" evidence.

### 3. Schema Drift
Significant schema drift occurred between **Feb 20 and Feb 23**.
*   **Changes**: casing changes (`plddt_fraction_high` -> `pLDDT_fraction_high`), column additions (`priority_score`, `source_category`), and removals.
*   **Risk**: Downstream analysis scripts (like ranking or plotting) must be robust to these column name changes or they will fail/misinterpret data.

## Recommendations
1.  **Force Refresh Core Candidates**: We must re-run the *current* analysis pipeline on PIEZO2, LBX1, and LMNA to ensure they are evaluated with the same rigor and code as the metabolic candidates.
2.  **Standardize Schema**: The `metrics.csv` output format needs to be locked down to prevent further drift.
3.  **Confidence Weighting**: The static nature of LBX1 (low confidence) vs PIEZO2 (high confidence) needs to be re-evaluated with the new pipeline to see if the "confidence gap" persists or narrows.

## Artifacts
*   **Raw Audit Log**: `reports/evidence_freshness_audit_raw.txt`
*   **Audit Script**: `scripts/analysis/evidence_freshness_audit.py`
