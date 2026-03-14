# Countercurvature Claims Matrix

This matrix categorizes claims related to the Biological Countercurvature hypothesis, LBX1, and mechanosensor architectures, strictly mapped to project metrics and separating verified data from narrative hypothesis.

## 1. Confirmed by Metrics
*These claims are directly supported by quantitative outputs and cross-run audits.*

| Claim | Quantitative Support / Source | Date / File |
| :--- | :--- | :--- |
| **LBX1 structure is intermediate and low-confidence.** | LBX1 anisotropy ~2.27, pLDDT ~66.9, PAE_blockiness ~7.35. | `outputs/afcc/2026-02-16/metrics.csv` |
| **LBX1 metrics are static across recent analyses.** | Variance for LBX1 anisotropy and pLDDT is 0.0 across 17 runs. | `reports/evidence_freshness_audit.md` |
| **PIEZO2 and LMNA are strong "Tension Rod" candidates.** | PIEZO2 (Aniso: 4.44, pLDDT: 79.4), LMNA (Aniso: 4.75, pLDDT: 76.4) show highly extended shapes with adequate confidence. | `outputs/afcc/2026-02-16/metrics.csv`, `scripts/analysis/confidence_weighted_structural_evidence.py` |
| **POC5 and GHR show high anisotropy but lack structural confidence.** | POC5 (Aniso: 24.69, pLDDT: 64.0), GHR (Aniso: 5.13, pLDDT: 58.7) are low confidence and may reflect intrinsic disorder rather than stable extended structures. | `outputs/afcc/2026-02-16/metrics.csv` |

## 2. Supported but Uncertain
*These claims are plausible based on current data but require orthogonal experimental validation or better models.*

| Claim | Source / Context | Falsifiability / Caveat |
| :--- | :--- | :--- |
| **POC5 acts as a highly extended fibrous mechanosensor.** | High anisotropy (24.69) suggests a highly extended structure. | Low pLDDT (64.0) means the structure could simply be disordered rather than a functional "tension rod." Requires biophysical stiffness assay. |
| **ADGRG6 operates as a functional mechanosensor.** | Intermediate/High anisotropy (3.06) with adequate confidence (pLDDT 73.7). | Needs experimental verification of force-dependent activation. |

## 3. Speculative Narrative
*These claims have appeared in reports or cluster notes but are NOT supported by the structural metrics, or they over-interpret static data.*

| Claim | Source / Context | Why it is Speculative / Evidence Against |
| :--- | :--- | :--- |
| **LBX1's structural geometry is evolving to suggest a new structural class.** | Mentioned in `reports/structure_clusters/*.md` (e.g., 2026-01-20). | LBX1 structural metrics have been perfectly static across the entire trend window (`reports/evidence_freshness_audit.md`). Any "evolution" is purely narrative inflation. |
| **LBX1 directly bears mechanical load as a structural scaffold.** | Hypothesis derived from "Blocky Scaffolds" cluster narrative. | LBX1's low confidence and intermediate anisotropy do not support load-bearing capacity comparable to PIEZO2 or LMNA. Needs direct testing (`reports/lbx1_falsifiability_plan.md`). |
