# Countercurvature Claims Matrix

**Generated:** 2026-02-26
**Purpose:** Discipline manuscript claims by mapping them to data confidence tiers.

## 1. Confirmed Claims (Tier 1)
*Supported by direct measurement (pLDDT > 70) and reproducible metric trends.*

| Claim | Status | Evidence Source | Confidence |
|---|---|---|---|
| **"PIEZO2 is a stiff, extended molecular rod."** | **CONFIRMED** | `outputs/afcc/2026-02-16/metrics.csv` (Aniso: 4.44, pLDDT: 79.4) | **High** |
| **"LMNA acts as a nuclear tension element."** | **CONFIRMED** | `outputs/afcc/2026-02-18/metrics.csv` (Aniso: 4.75, pLDDT: 76.4) | **High** |
| **"FBLN5 and STOML3 are viable high-stiffness candidates."** | **CONFIRMED** | `outputs/afcc/confidence_weighted_ranking.csv` (Weighted: ~5.8-4.7) | **High** |
| **"LBX1 is structurally distinct from PIEZO2/LMNA."** | **CONFIRMED** | `reports/confidence_weighted_structural_evidence.md` (Aniso: 2.27 vs 4.44) | **High** |

## 2. Supported Claims (Tier 2)
*Supported by data trends but requiring specific context or caveat (e.g., Low pLDDT).*

| Claim | Status | Evidence Source | Caveat |
|---|---|---|---|
| **"POC5 forms extreme anisotropic fibers."** | **SUPPORTED** | `outputs/afcc/2026-02-16/metrics.csv` (Aniso: 24.7) | Low Confidence (pLDDT 64.0); likely IDR-extended. |
| **"LBX1 structure is consistent with condensate formation."** | **SUPPORTED** | `outputs/afcc/2026-02-16/metrics.csv` (Blockiness: 7.35, High IDR) | Metric supports "Phase Separation" but does not prove function. |
| **"CNNM2 is a high-anisotropy magnesium transporter."** | **SUPPORTED** | `outputs/afcc/confidence_weighted_ranking.csv` (Weighted: 6.01) | Medium Confidence (pLDDT 70.4). |

## 3. Speculative / Refuted Claims (Tier 3)
*Hypotheses not supported by current structural data or actively contradicted.*

| Claim | Status | Evidence Against | Recommendation |
|---|---|---|---|
| **"LBX1 acts as a 'Stiff Caliper' or rigid rod."** | **REFUTED** | `reports/confidence_weighted_structural_evidence.md` (Weighted Score: 1.52) | **Abandon.** Pivot to Condensate Sensor. |
| **"GHR is a high-stiffness structural rod."** | **SPECULATIVE** | `outputs/afcc/2026-02-16/metrics.csv` (pLDDT: 58.7) | **Weak.** Low confidence suggests disorder, not stiffness. |
| **"Structural evolution of candidates driven by time."** | **REFUTED** | `reports/evidence_freshness_audit.md` (Freshness: < 0.20) | **Stop.** Static vectors prove no evolution occurred. |

## 4. Manuscript Guidelines
- **DO NOT** claim LBX1 is stiff. Use "condensate-forming" or "disordered domain-rich".
- **DO NOT** imply "trends" in structure over Jan-Feb. State "consistent AlphaFold predictions".
- **DO** highlight FBLN5 and STOML3 as new, high-confidence mechanosensory candidates.
- **DO** flag POC5 as "putative fiber" pending experimental validation of its folded state.
