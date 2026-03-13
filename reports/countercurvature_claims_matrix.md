# Countercurvature Claims Matrix

## Overview
Generated based on authoritative structural metrics snapshot: `outputs/afcc/2026-02-16/metrics.csv` and freshness audit `reports/evidence_freshness_audit.md`. To address snapshot availability limitations, certain candidates lacking 2026-02-16 presence map to their most recent backfilled run dates.

## 1. Confirmed by Metrics (High Confidence)
Claims backed by reproducible data points, primarily high-anisotropy and high-predictive-confidence AlphaFold models.

| Claim | Quantitative Support | Exact Source Row/File |
| :--- | :--- | :--- |
| **LMNA operates as a structurally rigorous fibrous sensor.** | Anisotropy = 4.75, pLDDT = 76.37. Highly extended architecture correlates with tension-bearing capacity. | `outputs/afcc/2026-02-26/metrics.csv` (LMNA row) |
| **PIEZO2 operates as an extended structural mechanotransducer.** | Anisotropy = 4.44, pLDDT = 79.44. Reliable extended architecture capable of tension sensing. | `outputs/afcc/2026-02-16/metrics.csv` (PIEZO2 row) |
| **Data Reuse Over-Interpretation.** | 60 proteins (including LBX1, PIEZO2) show completely static metrics across multiple runs (e.g., LBX1 reused 22 times since 2026-01-06), skewing apparent trends. | `reports/evidence_freshness_audit.md` |

## 2. Supported but Uncertain (Medium Confidence)
Claims dependent on structurally low-confidence, intermediate, or intrinsically disordered proteins where "fibrous" morphology may be an artifact of unbound simulation.

| Claim | Quantitative Support | Exact Source Row/File |
| :--- | :--- | :--- |
| **LBX1 acts as an intermediate integrating node.** | Anisotropy = 2.27, pLDDT = 66.87, PAE Blockiness = 7.35. Globular/intermediate nature suggests biochemical regulation, not direct load-bearing. | `outputs/afcc/2026-02-16/metrics.csv` (LBX1 row) |
| **RUNX3 acts as an intermediate integrating node.** | Anisotropy = 2.06, pLDDT = 60.56, PAE Blockiness = 0.00. Globular/intermediate nature suggests biochemical regulation, not direct load-bearing. | `outputs/afcc/2026-03-05/metrics.csv` (RUNX3 row) |
| **GHR functions as a primary tension rod.** | Anisotropy = 5.13, pLDDT = 58.70. High theoretical anisotropy but low confidence suggests large disordered domains, requiring experimental validation. | `outputs/afcc/2026-02-16/metrics.csv` (GHR row) |
| **POC5 is an extreme high-anisotropy structural driver.** | Anisotropy = 24.69, pLDDT = 63.97. Massive anisotropy signal is compromised by low structural confidence, likely indicating IDRs. | `outputs/afcc/2026-02-16/metrics.csv` (POC5 row) |

## 3. Speculative Narrative (Low Confidence)
Claims that over-extrapolate beyond static structural capabilities or infer direct causality without dynamic/experimental evidence.

| Claim | Quantitative Support | Exact Source Row/File |
| :--- | :--- | :--- |
| **High-anisotropy static inputs directly cause dynamic mechanosensitive response.** | (Inference without dynamic validation) Static structural data cannot explicitly confirm dynamic tension propagation or conformational shifts under mechanical load. | `reports/alphafold_data_assessment_2026-02-16.md` |
| **LBX1 directly senses primary mechanical strain.** | (Counter-evidence) LBX1 lacks the extreme anisotropy (>3.0) and high structural confidence characteristic of known tension rods (PIEZO2, LMNA). | `outputs/afcc/2026-02-16/metrics.csv` (LBX1 row) |
