# Countercurvature Claims Matrix

## Overview
This matrix disciplines the claims regarding the Biological Countercurvature hypothesis by mapping them to three evidentiary tiers: Confirmed by metrics, Supported but uncertain, and Speculative narrative. It explicitly separates direct measurement from inference.

## Tier 1: Confirmed by Metrics (Direct Measurement)
These claims are strictly supported by reproducible metric outputs, specifically derived from AlphaFold structural predictions.

*   **Claim:** Certain genes (e.g., ADGRG6, PIEZO2, FBLN5) exhibit highly anisotropic (extended/fibrous) architectures with adequate confidence.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Evidence:** ADGRG6 (anisotropy = 3.06, pLDDT = 73.7); PIEZO2 (anisotropy = 4.44, pLDDT = 79.4); FBLN5 (anisotropy = 7.05, pLDDT = 83.3).
*   **Claim:** Several previously analyzed runs incorrectly reused static, cached metric vectors instead of regenerating fresh AlphaFold measurements.
    *   **Source:** `reports/evidence_freshness_audit.md`
    *   **Evidence:** Identical values for Anisotropy and pLDDT were found across 10+ consecutive daily runs for proteins like PIEZO2, LBX1, and ARNTL.

## Tier 2: Supported but Uncertain (Inference)
These claims are grounded in data but require further experimental validation to confirm causality or in vivo relevance.

*   **Claim:** Proteins with high structural anisotropy (like ADGRG6 and PIEZO2) are mechanically primed to act as load-bearing mechanosensors in spinal tissue.
    *   **Source:** `reports/confidence_weighted_structural_evidence.md`
    *   **Evidence:** Their extended structure is highly confident (pLDDT > 70), which is consistent with mechanosensory geometry, but this is an *inference* of function from predicted structure, not a direct measurement of mechanotransduction in vivo.
*   **Claim:** The dataset contains significant "structural false positives" where high anisotropy is an artifact of low-confidence intrinsically disordered regions rather than true functional rigidity.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv` & `reports/confidence_weighted_structural_evidence.md`
    *   **Evidence:** POC5 (anisotropy = 24.69, pLDDT = 64.0) and GHR (anisotropy = 5.13, pLDDT = 58.7) show high anisotropy but low confidence, weakening the hypothesis that they are stable, rigid structural rods.

## Tier 3: Speculative Narrative (Evidence AGAINST / Weakening the Hypothesis)
These claims lack quantitative support in the current metrics and risk over-interpretation.

*   **Claim:** LBX1 acts as a stable, structurally extended mechanosensor that directly senses biomechanical loading to drive S-shaped spinal curvature.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Evidence AGAINST:** LBX1 shows only intermediate anisotropy (2.27) and has low structural confidence (pLDDT = 66.9). The assertion that it acts as a mechanical "tension rod" is speculative and not supported by current AlphaFold data.
*   **Claim:** Dynamic daily changes in AlphaFold metrics reflect ongoing biological discovery regarding mechanosensor adaptation.
    *   **Source:** `reports/evidence_freshness_audit.md`
    *   **Evidence AGAINST:** The freshness audit confirmed that many daily "updates" were simply re-publishing identical, static cached values for genes like LBX1.
