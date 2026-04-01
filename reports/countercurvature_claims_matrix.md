# Countercurvature Claims Matrix

## Overview
This matrix categorizes claims related to the Biological Countercurvature hypothesis into three tiers, mapping each to its exact source file and establishing discipline for manuscript drafting. It distinguishes direct measurements from speculative narrative.

---

### Tier 1: Confirmed by Metrics
These claims are directly supported by reproducible, quantitative data and can be robustly defended in a manuscript.

| Claim | Quantitative Support / Evidence | Source File / Date |
| :--- | :--- | :--- |
| **Strong Structural Mechanosensors Exist** | CNNM2, FBLN5, STOML3, PANX3, and PIEZO2 exhibit high anisotropy (> 4.4) and adequate confidence (pLDDT > 70). | `outputs/afcc/2026-02-16/metrics.csv` (Rows: CNNM2, FBLN5, STOML3, PANX3, PIEZO2) |
| **LBX1 Geometry is Static** | LBX1 metrics (anisotropy ~2.27, pLDDT ~66.9, PAE blockiness ~7.35) have zero variance across 17 runs in the trend window. | `reports/evidence_freshness_audit.md` |
| **PIEZO2 and LMNA are Static** | PIEZO2 and LMNA metrics have zero variance across all runs in which they appear in the trend window. | `reports/evidence_freshness_audit.md` |
| **LBX1 is Low Confidence** | LBX1 pLDDT is consistently ~66.9 (< 70 threshold), classifying its structural prediction as low-confidence. | `outputs/afcc/2026-02-16/metrics.csv` (Row: LBX1) |
| **LBX1 is Intermediate Anisotropy** | LBX1 anisotropy is ~2.27, classifying it as intermediate morphology. | `outputs/afcc/2026-02-16/metrics.csv` (Row: LBX1) |

---

### Tier 2: Supported but Uncertain
These claims have some basis in data or literature but rely on metrics that are either low-confidence or require orthogonal validation before being considered causal.

| Claim | Quantitative Support / Evidence | Source File / Date |
| :--- | :--- | :--- |
| **Extreme Anisotropy in POC5/GHR** | POC5 (24.69) and GHR (5.13) show high anisotropy but suffer from low pLDDT (< 65). This may indicate structural tension rods or merely long disordered regions. | `outputs/afcc/2026-02-16/metrics.csv` (Rows: POC5, GHR); `reports/confidence_weighted_structural_evidence.md` |
| **LBX1 Modular Architecture** | LBX1 exhibits high PAE blockiness (~7.35), supporting a modular architecture hypothesis, though confidence in the exact domain boundaries is low. | `outputs/afcc/2026-02-16/metrics.csv` (Row: LBX1) |
| **Tension Rod Persistence** | GHR remains the top anisotropic candidate (5.13) across multiple runs, supporting a potential structural role, despite low confidence. | `outputs/afcc/2026-02-16/metrics.csv` (Row: GHR); `reports/afcc_latest.md` (e.g., 2026-03-05 run) |

---

### Tier 3: Speculative Narrative (Avoid or Heavily Caveat in Manuscript)
These claims are inferences, hypotheses, or interpretations that over-extrapolate from static metrics or assert causality without direct measurement.

| Claim | Quantitative Support / Evidence (or lack thereof) | Source File / Date |
| :--- | :--- | :--- |
| **LBX1 Geometry Changed Recently** | Narrative notes suggest evolving LBX1 geometry, but metrics show zero variance (SD=0) over the trend window. | `reports/alphafold_data_assessment_2026-02-16.md` (Potential hypothesis inflation flags) |
| **PIEZO2/LMNA Structural Evolution** | Narrative notes suggest structural evolution, but metrics show zero variance (SD=0) over the trend window. | `reports/alphafold_data_assessment_2026-02-16.md` (Potential hypothesis inflation flags) |
| **LBX1 is a Primary Tension Sensor** | Based on its low-confidence, intermediate-anisotropy geometry, it is highly speculative to cast LBX1 as a primary mechanical tension sensor comparable to PIEZO2. | `reports/confidence_weighted_structural_evidence.md`; `reports/lbx1_falsifiability_plan.md` |
