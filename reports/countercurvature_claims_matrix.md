# Biological Counter-Curvature Claims Matrix

This matrix categorizes key statements regarding the structural mechanosensor hypothesis of the Biological Counter-Curvature theory. Claims are separated by their evidence tier to enforce discipline in manuscript writing, distinguishing direct measurements from speculative narratives.

## Tier 1: Confirmed by Metrics
These claims are directly supported by high-confidence, quantitative structural metrics.

| Claim | Source File | Source Row/Gene | Metric Value |
|---|---|---|---|
| PIEZO2 acts as a high-confidence, highly anisotropic structural rod. | `outputs/afcc/2026-02-16/metrics.csv` | PIEZO2 | Anisotropy: 4.44, pLDDT: 79.44 |
| ADGRG6 acts as a high-confidence, highly anisotropic structural rod. | `outputs/afcc/2026-02-16/metrics.csv` | ADGRG6 | Anisotropy: 3.06, pLDDT: 73.73 |
| LBX1 has an intermediate-anisotropy, highly blocky structure but is low-confidence overall. | `outputs/afcc/2026-02-16/metrics.csv` | LBX1 | Anisotropy: 2.27, pLDDT: 66.87, PAE Blockiness: 7.35 |
| Structural metrics for core genes (LBX1, PIEZO2, POC5) have been completely static since Jan 2026. | `reports/evidence_freshness_audit.md` | PIEZO2, LBX1, POC5 | Identical vectors in runs from 2026-01-09 to 2026-02-16 |

## Tier 2: Supported but Uncertain
These claims are plausible based on AlphaFold data but require orthogonal experimental validation due to low structural confidence or potential disorder.

| Claim | Source File | Source Row/Gene | Metric Value |
|---|---|---|---|
| POC5 and GHR represent a novel class of extreme-anisotropy structural rods. | `outputs/afcc/confidence_weighted_ranking.csv` | POC5, GHR | Anisotropy: 24.69 & 5.13 respectively, but pLDDT: < 70 (Low Confidence) |
| LBX1 forms functional modular domains capable of integrating mechanical signals. | `reports/alphafold_data_assessment_2026-02-16.md` | LBX1 Deep Dive | High PAE blockiness supports modularity, but low pLDDT prevents structural certainty |

## Tier 3: Speculative Narrative
These claims over-interpret static computational predictions, imply causal dynamics without evidence, or construct functional narratives lacking direct experimental backing.

| Claim | Source File | Source Row/Gene | Reason for Speculative Status |
|---|---|---|---|
| LBX1's geometry dynamically evolved over the Jan-Feb run window to respond to tension. | `reports/alphafold_data_assessment_2026-02-16.md` | Confidence and Failure Modes | Directly refuted by data freshness audit; LBX1 metrics were static across all runs. |
| The high-anisotropy conformation of POC5 is definitive proof of its load-bearing capability. | `reports/alphafold_data_assessment_2026-02-16.md` | Conclusions | Extreme anisotropy in low-confidence regions frequently correlates with intrinsic disorder, not necessarily a rigid physiological rod. |
