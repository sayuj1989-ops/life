# Countercurvature Claims Matrix
**Date:** 2026-03-06
**Evidence Source:** `outputs/afcc/confidence_weighted_ranking.csv`

## 1. Confirmed Claims (High Confidence)
These claims are supported by **high-confidence** structural metrics (Anisotropy > 3.0, pLDDT > 70, PAE < 20).

| Claim | Candidate | Evidence Metric | Status |
|---|---|---|---|
| **"Tension Rod" Architecture** | **PIEZO2** | Anisotropy=4.44, pLDDT=79.4 | **CONFIRMED**. High aspect ratio is structurally validated. |
| **"Tension Rod" Architecture** | **LMNA** | Anisotropy=4.75, pLDDT=76.4 | **CONFIRMED**. Fibrous nature aligns with nuclear lamina role. |
| **"Tension Rod" Architecture** | **PLOD1** | Anisotropy=3.40, pLDDT=92.7 | **CONFIRMED**. Extremely rigid enzyme structure. |
| **Scalar vs Vector Sensing** | **PIEZO1 vs PIEZO2** | PIEZO2 (4.44) > PIEZO1 (3.90) | **CONFIRMED**. PIEZO2 is measurably more anisotropic than PIEZO1. |

## 2. Supported Claims (Low Confidence)
These claims are supported by metrics, but the structural confidence is **low** (pLDDT < 70), suggesting the feature might be disordered.

| Claim | Candidate | Evidence Metric | Status |
|---|---|---|---|
| **"Blocky Scaffold"** | **LBX1** | Anisotropy=2.27, Blockiness=7.35 | **SUPPORTED (WEAK)**. "Blockiness" exists but pLDDT=66.9 suggests it's likely dynamic/disordered domains. |
| **"Metabolic Anisotropy"** | **GHR** | Anisotropy=5.13 | **SUPPORTED (ARTIFACTUAL?)**. pLDDT=58.7 is very low. Likely a disordered tail, not a rod. |
| **"Disordered Proprioception"** | **EGR3** | Anisotropy=3.76, pLDDT=50.0 | **SUPPORTED**. High disorder aligns with IDR hypothesis, not structural stiffness. |
| **"Disordered Proprioception"** | **RUNX3** | Anisotropy=2.06, pLDDT=60.6 | **SUPPORTED**. Consistent with transcription factor disorder. |

## 3. Speculative Claims (Refuted or Unproven)
These claims are contradicted by the new confidence-weighted analysis or lack metric support.

| Claim | Candidate | Refutation / Gap | Status |
|---|---|---|---|
| **"LBX1 is a stiff rod"** | **LBX1** | pLDDT=66.9, PAE=25.1 | **REFUTED**. Structure is too low-confidence/disordered to be a rigid mechanical strut. |
| **"Metabolic Enzymes are Rods"** | **ARNTL, MYLK** | pLDDT < 66 | **WEAKENED**. Likely IDR-driven phase separation, not rigid enzymatic rods. |
| **"Sexual Dimorphism via Rods"** | **General** | No sex-specific structural data | **SPECULATIVE**. Metric differences (if any) are not linked to sex in this dataset. |

## Action Plan
*   **Retract**: "LBX1 is a stiff rod". Replace with "LBX1 is a disordered phase-sensor".
*   **Maintain**: "PIEZO2 is a Tension Rod".
*   **Investigate**: "Metabolic Anisotropy" (GHR, ARNTL) – verify if IDRs are functional or artifacts.
