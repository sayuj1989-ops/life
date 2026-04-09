# Countercurvature Claims Matrix

## Overview
This matrix categorizes claims regarding the Biological Countercurvature hypothesis based on the strength of supporting evidence from the repository. It enforces claim discipline for manuscript preparation by distinguishing measured structural metrics from narrative interpretation.

## 1. Confirmed by Metrics
These claims are directly supported by reproducible AlphaFold outputs.

| Claim | Evidence Source | Confidence | Notes |
|---|---|---|---|
| LBX1 is a low-confidence, modular structure. | `outputs/afcc/*/metrics.csv` | High | Consistently pLDDT < 70, high PAE blockiness. |
| Structural metric estimates for core candidates (LBX1, PIEZO2, LMNA) are static across the Jan-Feb run window. | `scripts/analysis/evidence_freshness_audit.py`, `reports/evidence_freshness_audit.md` | High | Demonstrates reuse of predictions; no metric evolution occurred. |
| PIEZO2 and LMNA exhibit high anisotropy with adequate confidence (pLDDT > 70). | `outputs/afcc/confidence_weighted_ranking.csv` | High | Validates their classification as extended, structurally defined elements. |

## 2. Supported but Uncertain
These claims are plausible based on current data but require orthogonal validation.

| Claim | Evidence Source | Confidence | Notes |
|---|---|---|---|
| High-anisotropy outliers (POC5, GHR) represent extended structures relevant to countercurvature. | `outputs/afcc/2026-02-16/metrics.csv` | Moderate to Low | Anisotropy is high, but pLDDT is < 70, suggesting extended disorder rather than rigid rods. |
| The Anisotropic Membrane-Nucleus Axis (PIEZO1/2 -> LMNA) forms a continuous tension transmission pathway. | `reports/structure_clusters/2026-07-23__cluster_note.md` | Moderate | Structurally sound based on individual protein geometries, but physical coupling in vivo is inferred, not measured. |

## 3. Speculative Narrative
These claims over-interpret structural data and lack direct quantitative support. They should not be presented as findings in a manuscript without new experimental data.

| Claim | Evidence Source | Confidence | Notes |
|---|---|---|---|
| LBX1 geometry "evolved" or provided "new insights" across consecutive daily runs. | `reports/afcc_latest.md`, `reports/structure_clusters/*` | Very Low | Disproved by the `evidence_freshness_audit.md` which confirms static metrics. |
| The loss of tension in microgravity directly causes "decoherence" of the PIEZO1-PIEZO2-LMNA axis. | `reports/structure_clusters/2026-07-23__cluster_note.md` | Hypothesis-level | A mechanistic hypothesis based on structure; requires the polarization anisotropy microscopy test to validate. |
| Nuclear import of EGR3 is mechanically gated by cytoskeletal tension. | `reports/structure_clusters/2026-10-31__cluster_note.md` | Hypothesis-level | Plausible given EGR3 anisotropy, but purely inferential. Requires tension-dependent translocation assay. |
