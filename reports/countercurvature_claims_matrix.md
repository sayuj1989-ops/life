# Biological Countercurvature Claims Matrix

## Overview
This matrix rigorously categorizes claims surrounding the Biological Countercurvature hypothesis into three tiers. By distinguishing measured evidence from structural speculation, we provide a disciplined foundation for manuscript drafting.

## 1. Confirmed by metrics (Directly Measured & Reliable)
Claims in this tier are backed by high-confidence numerical data (e.g., adequate pLDDT and high anisotropy). They constitute the strongest verifiable findings in the repository.

| Claim | Evidence / Exact Source | Details |
|---|---|---|
| **PIEZO2 is a highly extended 'Tension Rod'** | `outputs/afcc/2026-02-16/metrics.csv` (Row 18) | Anisotropy = 4.44; pLDDT = 79.44. Metric confirms a rigid, extended geometry. |
| **LMNA operates as a structural tension element** | `reports/structure_clusters/2026-02-27__tension_rods.md`; Historical AFCC runs (e.g., `outputs/afcc/2026-02-08/metrics.csv`) | Historical Anisotropy = 4.75; pLDDT = 76.37. Reliable rod-like architecture. |
| **LBX1 is structurally intermediate, blocky, and low-confidence** | `outputs/afcc/2026-02-16/metrics.csv` (Row 14) | Anisotropy = 2.27; pLDDT = 66.87; PAE_blockiness = 7.35. Falsifies 'rigid rod' narratives. |
| **Metrics for key candidates are completely static over Jan-Feb** | `reports/evidence_freshness_audit.md` | LBX1, POC5, LMNA, GHR metrics show zero variance across 17+ runs. They are not 'evolving' structurally. |

## 2. Supported but uncertain (Grounded in data, but low-confidence/proxies)
Claims here use measured parameters (like extreme anisotropy) but fall below confidence thresholds (pLDDT < 70) or rely on unvalidated proxy interpretations.

| Claim | Evidence / Exact Source | Details |
|---|---|---|
| **POC5 is an extreme anisotropic element** | `outputs/afcc/2026-02-16/metrics.csv` (Row 19) | Anisotropy = 24.69. However, pLDDT = 63.97. Needs orthogonal verification to prove it's not a modeling artifact of flexible linkers. |
| **GHR has a fibrous/extended geometry** | `outputs/afcc/2026-02-16/metrics.csv` (Row 11) | Anisotropy = 5.13; pLDDT = 58.70. Supports tension-rod role but lacks adequate structural confidence. |
| **LBX1, FLNA, COL1A1 belong to a 'Tension-Gated Scaffold' class** | `reports/structure_clusters/2026-01-20__cluster_note.md` | High PAE blockiness supports domain segregation. The "cryptic signal reservoir" behavior is a logical but unverified biophysical leap from the blockiness metric. |

## 3. Speculative narrative (Interpretations not strictly supported by metrics)
These are hypothesis-level claims that inflate structural snapshots into dynamic or causal mechanisms without longitudinal or functional verification.

| Claim | Evidence / Exact Source | Details |
|---|---|---|
| **LBX1 functional loss is uniquely gated by nuclear stiffness (unlike RUNX3)** | `reports/structure_clusters/2026-02-01__blocky_lbx1.md` | Derives from comparing LBX1 blockiness (7.35) to RUNX3 (0.00). It is a highly speculative functional inference lacking *in vitro* or *in vivo* validation. |
| **POC5 and IFT88 will undergo degradation/aggregation in microgravity** | `reports/structure_clusters/2026-06-01__cluster_note.md` | An entirely predictive narrative extending the structural classification into proteostasis consequences. |
| **Newly emerging 'classes' or metric shifts in Jan/Feb** | Various cluster notes (e.g., `2026-01-13__cluster_note.md`, `2026-01-15__cluster_note.md`) | `evidence_freshness_audit.md` proved metrics were static; narratives suggesting they changed are hallucinated. |

