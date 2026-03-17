# Countercurvature Claims Matrix

*Generated Date: 2026-02-19*

## Confirmed by metrics
*   **Claim:** High-anisotropy/high-confidence candidates exist and include CNNM2, FBLN5, STOML3, PANX3, PIEZO2, ROCK1, and ADGRG6.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Value:** Anisotropy $\ge 3.0$, pLDDT $\ge 70$.
*   **Claim:** LBX1 is a low-confidence, intermediate-anisotropy candidate.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Value:** Anisotropy $\approx 2.27$, pLDDT $\approx 66.9$, high PAE blockiness $\approx 7.35$.
*   **Claim:** The reported structures for PIEZO2, LMNA, POC5, GHR, and LBX1 are effectively static across runs.
    *   **Source:** `reports/evidence_freshness_audit.md`
    *   **Value:** Identical vectors across multiple runs.
*   **Claim:** PIEZO2 is more structurally reliable as a mechanosensor geometry candidate than LBX1.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Value:** PIEZO2 pLDDT ($79.4$) vs LBX1 pLDDT ($66.9$).

## Supported but uncertain
*   **Claim:** Extreme anisotropy outliers like POC5 and GHR may serve unique structural roles (e.g., tension rods).
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Caveat:** Low confidence (pLDDT $< 70$). High anisotropy in low-pLDDT proteins often indicates intrinsically disordered regions rather than rigid fibrous structures.
*   **Claim:** LBX1's high PAE blockiness supports a modular architecture.
    *   **Source:** `outputs/afcc/2026-02-16/metrics.csv`
    *   **Caveat:** LBX1's overall low confidence (pLDDT $\approx 66.9$) limits the certainty of inter-domain flexibility/rigidity.

## Speculative narrative
*   **Claim:** Novel structural geometries or classes are dynamically "emerging" for core proteins like LBX1, LMNA, or PIEZO2 over the analysis window.
    *   **Source:** Narrative cluster notes (e.g., `reports/structure_clusters/2026-01-13__cluster_note.md`, `reports/structure_clusters/2026-01-20__cluster_note.md`).
    *   **Caveat:** As shown in `reports/evidence_freshness_audit.md`, the underlying AlphaFold metrics for these proteins have not changed. The narratives extrapolate temporal dynamism from identical static inputs.
