# Biological Countercurvature Claims Matrix

This document explicitly categorizes claims regarding the Biological Countercurvature hypothesis, distinguishing direct quantitative measurements from derived support and speculative narrative.

## Claim Discipline Tiers

| Claim Tier | Definition |
| :--- | :--- |
| **Confirmed by metrics** | Claims directly measured and replicated across reliable quantitative outputs (e.g., AFCC metrics CSVs with `pLDDT >= 70`). |
| **Supported but uncertain** | Claims grounded in data but relying on low-confidence proxies or requiring orthogonal validation (e.g., high-anisotropy predictions with `pLDDT < 70`). |
| **Speculative narrative** | Interpretations, causal inferences, or "emerging trend" narratives that are not strictly supported by the underlying static metrics, often found in cluster notes. |

---

## 1. Confirmed by metrics
These claims are robustly supported by the latest authoritative snapshot (`outputs/afcc/2026-02-16/metrics.csv`) and historical data.

*   **Claim 1.1**: **PIEZO2 is a high-confidence, high-anisotropy structural anchor.**
    *   **Source Data**: `outputs/afcc/2026-02-16/metrics.csv`
    *   **Evidence**: PIEZO2 consistently shows high anisotropy (4.44) and adequate confidence (pLDDT = 79.4, `PAE_blockiness` = 2.80).
*   **Claim 1.2**: **LBX1 is a low-confidence, intermediate-anisotropy candidate with high blockiness.**
    *   **Source Data**: `outputs/afcc/2026-02-16/metrics.csv`
    *   **Evidence**: LBX1 metrics (anisotropy = 2.27, pLDDT = 66.9, `PAE_blockiness` = 7.35) define it as an intermediate, modular structure rather than a pure tension rod.
*   **Claim 1.3**: **Core candidates' structural metrics (e.g., LBX1, PIEZO2, LMNA) are static across recent AFCC runs.**
    *   **Source Data**: `reports/evidence_freshness_audit.md` (derived from `outputs/afcc/2026-01-09` to `outputs/afcc/2026-02-16`)
    *   **Evidence**: The per-gene vectors for these candidates remain mathematically identical across runs, indicating static inputs rather than evolving structural estimates.
*   **Claim 1.4**: **CNNM2, FBLN5, STOML3, and PANX3 possess robust extended morphologies.**
    *   **Source Data**: `outputs/afcc/confidence_weighted_ranking.csv` (derived from 02-16 snapshot)
    *   **Evidence**: These proteins meet the criteria for both high anisotropy ($\geq 3.0$) and adequate confidence ($\geq 70.0$ pLDDT).

---

## 2. Supported but uncertain
These claims have a basis in data but suffer from methodological caveats, primarily low structural confidence (high predicted disorder).

*   **Claim 2.1**: **POC5 and GHR may represent extreme tension-rod architectures.**
    *   **Source Data**: `outputs/afcc/2026-02-16/metrics.csv` and daily refresh reports (`reports/afcc_latest.md`).
    *   **Evidence**: POC5 exhibits extreme anisotropy (24.69) and GHR shows high anisotropy (5.13).
    *   **Caveat**: Both suffer from low confidence (pLDDT = 64.0 and 58.7, respectively). The high anisotropy might be an artifact of long, unstructured IDRs in the AlphaFold model rather than a true rigid rod.
*   **Claim 2.2**: **LBX1's "blocky" PAE matrix suggests a modular spring-like function.**
    *   **Source Data**: `outputs/afcc/2026-02-16/metrics.csv` (`PAE_domain_blockiness_score` = 7.35).
    *   **Evidence**: The high blockiness score implies distinct structural domains separated by flexible hinges.
    *   **Caveat**: The overall low pLDDT (66.9) means the relative orientation of these blocks is highly uncertain, requiring smFS or other validation.

---

## 3. Speculative narrative
These claims represent hypothesis inflation where static data was over-interpreted as causal or temporal trends in previous narrative reports.

*   **Claim 3.1**: **LBX1 or PIEZO2 structural geometry "evolved" or "emerged" over the Jan-Feb 2026 observation window.**
    *   **Source Data**: E.g., `2026-01-20__cluster_note.md`, `reports/alphafold_data_assessment_2026-02-16.md` (Potential hypothesis inflation flags).
    *   **Evidence AGAINST**: The metrics for LBX1 and PIEZO2 were completely static across this window (`reports/evidence_freshness_audit.md`). Narrative updates implying dynamic changes were inferring motion from repeated identical snapshots.
*   **Claim 3.2**: **High-anisotropy/low-confidence proteins (like POC5) are definitively novel mechanosensors driving scoliotic progression.**
    *   **Source Data**: Various daily refresh summaries highlighting POC5 as "Top Mover" (`reports/afcc_latest.md`).
    *   **Evidence AGAINST**: As established in Tier 2, low pLDDT prevents definitive mechanistic assignment without orthogonal biological assays. The label "Top Mover" only reflects extreme metric values, not structural reliability.
