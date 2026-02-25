# Confidence-Weighted Structural Evidence Report
**Date:** 2026-03-12
**Source:** `outputs/afcc/confidence_weighted_ranking.csv`
**Methodology:** Candidates ranked by `Weighted Score = Anisotropy * (pLDDT / 100)`.

## Executive Summary
This report re-evaluates the "Biological Countercurvature" candidates by integrating AlphaFold confidence metrics (pLDDT). This filtering separates robust structural predictions from potential disordered artifacts.

**Critical Finding:** **LBX1** ranks **18th** out of 25 candidates, falling into **Tier 3 (Low Anisotropy / Low Confidence)**. It is **structurally distinct** from confirmed mechanosensors like PIEZO2 (Rank 6, Tier 1). The hypothesis that LBX1 acts as a "stiff rod" or "molecular caliper" is **unsupported** by current structural data. Its high PAE blockiness (7.35) suggests a modular/beads-on-a-string architecture rather than a rigid beam.

## 1. Top-Tier Structural Candidates (High Anisotropy + High Confidence)
These proteins have both extreme geometry (>3.0 anisotropy) and reliable folding (>70 pLDDT). They are the strongest candidates for "Passive Mechanical Elements."

| Rank | Gene | Anisotropy | pLDDT | Weighted Score | Function |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2 | **CNNM2** | 8.54 | 70.4 | 6.01 | Ion transport / Membrane |
| 3 | **FBLN5** | 7.05 | 83.3 | 5.88 | ECM / Elastic fibers |
| 4 | **STOML3** | 5.56 | 84.3 | 4.69 | Mechanotransduction |
| 5 | **PANX3** | 5.08 | 81.7 | 4.15 | Gap junction / Bone dev |
| 6 | **PIEZO2** | 4.44 | 79.4 | 3.53 | **Confirmed Mechanosensor** |
| 10 | **ADGRG6** | 3.06 | 73.7 | 2.26 | Scoliosis driver / G-protein |

*Inference:* PIEZO2 sets the "Gold Standard" for a mechanosensor (Score ~3.5). Candidates scoring above this (CNNM2, FBLN5) warrant immediate biophysical investigation.

## 2. High-Risk / Artifact Candidates (High Anisotropy + Low Confidence)
These proteins show extreme elongation but poor folding confidence. The anisotropy may be an artifact of disordered regions being modeled as extended threads.

| Rank | Gene | Anisotropy | pLDDT | Weighted Score | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **POC5** | 24.69 | 64.0 | 15.79 | Extreme outlier. Likely centriolar filament or artifact. |
| 7 | **GHR** | 5.13 | 58.7 | 3.01 | Growth Hormone Receptor. |
| 8 | **EMD** | 4.29 | 60.3 | 2.58 | Emerin (Nuclear envelope). |

*Caution:* POC5's score is inflated by extreme length. The low pLDDT (64.0) warns against treating it as a rigid rod without experimental validation.

## 3. LBX1 Comparator Analysis
LBX1 is the central focus of the "Countercurvature" hypothesis, but its structural metrics do not support a "rigid rod" mechanism.

| Feature | LBX1 | PIEZO2 (Control) | POC5 (Outlier) |
| :--- | :--- | :--- | :--- |
| **Tier** | **Tier 3** | Tier 1 | Tier 2 |
| **Weighted Score** | **1.52** | 3.53 | 15.79 |
| **Anisotropy** | **2.27** (Intermediate) | 4.44 (High) | 24.69 (Extreme) |
| **pLDDT** | **66.9** (Low) | 79.4 (High) | 64.0 (Low) |
| **PAE Blockiness** | **7.35** (High) | 2.80 (Low) | 3.51 (Low) |
| **Morphology** | **Modular / Blocky** | Curved Beam | Filament |

**Interpretation:**
*   LBX1 is **NOT** a stiff rod like PIEZO2.
*   LBX1 is **NOT** a filament like POC5.
*   LBX1 **IS** a modular protein with distinct domains (High PAE Blockiness).
*   *Hypothesis Adjustment:* LBX1 likely functions via **differential localization** (e.g., shuttling between stiff nuclear sites) or **condensation** (IDR-driven), rather than acting as a passive mechanical strut.

## 4. Conclusion
The "LBX1 as a Molecular Caliper" model is **weakened** by this analysis. The evidence points towards:
1.  **PIEZO2/ADGRG6** as the true "Structural Sensors".
2.  **POC5** as a potential "Filamentous Tether" (pending validation).
3.  **LBX1** as a "Downstream Integrator" whose mechanosensitivity is likely indirect or emergent (e.g., via phase separation or partner binding), not intrinsic to its solitary folded shape.
