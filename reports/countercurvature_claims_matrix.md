# Countercurvature Claims Matrix

## Overview
This matrix categorizes key structural and mechanistic claims regarding candidate proteins in the Biological Countercurvature hypothesis according to their level of evidentiary support.

## Claim Tiers

### Tier 1: Confirmed by Metrics (Direct Measurement)
These claims are directly supported by measured quantitative data in authoritative metric files.
*   **Claim 1.1:** PIEZO2, CNNM2, FBLN5, and STOML3 are high-anisotropy structures with adequate confidence (pLDDT >= 70).
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Data:** PIEZO2 (Anisotropy 4.44, pLDDT 79.4), CNNM2 (Anisotropy 8.54, pLDDT 70.4).
*   **Claim 1.2:** LBX1 is a low-confidence, intermediate-anisotropy structure with high PAE blockiness.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Data:** LBX1 (Anisotropy 2.27, pLDDT 66.9, PAE Blockiness 7.35).
*   **Claim 1.3:** Structural metric vectors for key candidates (e.g., PIEZO2, LMNA, RUNX3, NTRK3) were static across multiple historical AFCC runs during Jan-Feb 2026.
    *   **Source:** `reports/evidence_freshness_audit.md`
    *   **Data:** E.g., RUNX3 identical in 14 runs, LMNA identical in 13 runs.

### Tier 2: Supported but Uncertain (Hypothesis requiring validation)
These claims represent plausible mechanistic bridges derived from confirmed metrics, but lack direct experimental validation of function.
*   **Claim 2.1:** The high PAE blockiness of proteins like LBX1 and FLNA may represent tension-gated unfolding domains (cryptic signal reservoirs) rather than mere unstructured regions.
    *   **Source:** `reports/structure_clusters/2026-01-20__cluster_note.md`
    *   **Uncertainty:** High PAE blockiness can also result from natively disordered regions (IDRs) with no specific mechanical function, especially given the low pLDDT.
*   **Claim 2.2:** Extreme anisotropy candidates with low confidence (e.g., POC5, GHR) may serve as extended structural mechanosensors.
    *   **Source:** `reports/alphafold_data_assessment_2026-02-16.md`
    *   **Uncertainty:** The low pLDDT (e.g., POC5 = 64.0) suggests these extended shapes may simply be AlphaFold artifacts for disordered sequences.

### Tier 3: Speculative Narrative (Unsupported or Falsified)
These claims are narrative inferences that overreach the available measured data or are contradicted by it.
*   **Claim 3.1:** LBX1 functions directly as a rigid, load-bearing "tension rod" analogous to PIEZO2.
    *   **Status:** Falsified.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv` (Anisotropy 2.27 does not support a fibrous rod morphology).
*   **Claim 3.2:** The structures of key mechanosensors "evolved" or shifted into distinct new clusters during Jan-Feb 2026 based on new AlphaFold insights.
    *   **Status:** Falsified.
    *   **Source:** `reports/evidence_freshness_audit.md` (Metrics were static; changes were purely narrative re-interpretations of the same data, e.g., in `reports/structure_clusters/2026-01-13__cluster_note.md`).
