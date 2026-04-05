# Countercurvature Claims Matrix

## Overview
This matrix categorizes the claims regarding the Biological Countercurvature hypothesis and specific candidates (especially LBX1) into three tiers of confidence, mapping each to its exact source.

## Tier 1: Confirmed by Metrics
| Claim | Source | Evidence |
|---|---|---|
| The top high-anisotropy/high-confidence candidates include CNNM2, FBLN5, STOML3, PANX3, and PIEZO2. | `outputs/afcc/2026-02-16/metrics.csv` | Anisotropy > 3.0 and pLDDT >= 70 |
| LBX1 has intermediate anisotropy, high PAE blockiness, and low structural confidence. | `outputs/afcc/2026-02-16/metrics.csv` | Anisotropy = 2.27, PAE Blockiness = 7.35, pLDDT = 66.9 |
| The predicted structural metrics for core candidates (LBX1, PIEZO2, LMNA, POC5, GHR) are static across multiple analysis runs. | `reports/evidence_freshness_audit.md`, `reports/alphafold_data_assessment_2026-02-16.md` | Vectors remain identical across scoped window |

## Tier 2: Supported but Uncertain
| Claim | Source | Caveat |
|---|---|---|
| Proteins like POC5 and GHR may serve as structural "tension rods" due to extreme anisotropy. | `outputs/afcc/2026-02-16/metrics.csv` | Low confidence scores (pLDDT < 70) require orthogonal validation. High anisotropy could be an artifact of extended unstructured regions. |
| LBX1's high PAE blockiness indicates a modular architecture suitable for mechanical coupling. | `outputs/afcc/2026-02-16/metrics.csv` | Derived from computational predictions on a low-confidence structure; functional modularity must be biophysically confirmed. |

## Tier 3: Speculative Narrative
| Claim | Source | Caveat |
|---|---|---|
| LBX1 structure is dynamically evolving or displaying new mechanically relevant geometries over time. | `reports/structure_clusters/*_cluster_note.md` | Falsified by metrics audit; the input data has not changed across runs. |
| High anisotropy directly implies a functional mechanosensing role in vivo. | Various cluster narratives | Correlation only; sequence properties could drive extended forms without dedicated mechanical function. |
