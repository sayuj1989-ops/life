# LBX1 Falsifiability Plan: Challenging the Mechanosensor Hypothesis
**Date:** 2026-02-19
**Status:** Draft

## Objective
To rigorously test and potentially falsify the hypothesis that **LBX1 acts as a direct mechanosensor or structural tension rod** in the developing spine. Current structural evidence (Anisotropy ~2.27, Tier 4) weakens the "structural rod" model, shifting the burden of proof to functional mechanotransduction.

## Experiment 1: The "Strain-Silence" Test (Transcriptional Independence)
**Rationale:** If LBX1 is a mechanosensor (like YAP/TAZ), its expression or localization must respond to physiological strain.
- **Hypothesis:** LBX1 expression and nuclear localization are **independent** of mechanical strain.
- **Assay Design:**
  - **System:** Human paraspinal muscle progenitor cells (iPSCs).
  - **Condition:** Apply cyclic tensile strain (10% elongation, 1Hz, 24h) using a Flexcell system.
  - **Controls:** Static culture (Negative), YAP/TAZ nuclear translocation (Positive).
- **Quantitative Readout:**
  - RT-qPCR for *LBX1* mRNA (Fold Change).
  - Immunofluorescence for LBX1 Nuclear/Cytoplasmic ratio.
- **Expected Direction (if Mechanics Link is FALSE):** LBX1 levels and localization remain unchanged between Static and Strained conditions, while YAP/TAZ shows >2-fold nuclear enrichment in Strained.
- **Falsification Threshold (for the "Mechanosensor" Hypothesis):**
  - **Falsified if:** Fold Change < 1.5x AND Nuclear/Cyto ratio change < 20% (p > 0.05).
  - **Supported if:** Fold Change > 2.0x OR Nuclear/Cyto ratio significant shift.

## Experiment 2: The "Ghost Rod" Test (Structural Stiffness)
**Rationale:** The Countercurvature hypothesis posits anisotropic proteins act as "stiffeners". If LBX1 is structural, it must stiffen the cell.
- **Hypothesis:** LBX1 does **not** contribute to cellular stiffness or cytoskeletal rigidity.
- **Assay Design:**
  - **System:** HEK293T cells (low baseline stiffness).
  - **Condition:** Overexpression of LBX1-GFP vs GFP control.
  - **Measurement:** Atomic Force Microscopy (AFM) nano-indentation to measure cortical stiffness.
- **Quantitative Readout:** Young's Modulus (kPa).
- **Expected Direction (if Structural Link is FALSE):** No significant increase in stiffness in LBX1-overexpressing cells.
- **Falsification Threshold (for the "Structural Rod" Hypothesis):**
  - **Falsified if:** $\Delta$ Stiffness (LBX1 - GFP) < 0.5 kPa.
  - **Supported if:** $\Delta$ Stiffness > 2.0 kPa (comparable to Lamin A/C overexpression).

## Experiment 3: The "Metabolic Mimicry" Test (Signal Dissection)
**Rationale:** We hypothesize LBX1 "mechanosensitivity" is actually metabolic sensing (ATP gating). If true, metabolic shifts should mimic mechanical unloading.
- **Hypothesis:** LBX1 downregulation in scoliosis is driven by **energy deficit**, not lack of tension.
- **Assay Design:**
  - **System:** Paraspinal muscle organoids.
  - **Condition A (Mechanical):** Microgravity/Unloading simulation (Clinostat).
  - **Condition B (Metabolic):** ATP depletion (Oligomycin/2DG titration) to match ATP levels of Cond A.
  - **Condition C (Rescue):** Unloading + NAD+ precursor (NR/NMN).
- **Quantitative Readout:** LBX1 protein levels (Western Blot).
- **Expected Direction (if Mechanics Link is Secondary):**
  - Condition B (Metabolic) suppresses LBX1 to the same extent as Condition A (Mechanical).
  - Condition C (Rescue) restores LBX1 despite unloading.
- **Falsification Threshold (for the "Pure Mechanics" Hypothesis):**
  - **Falsified if:** Metabolic depletion alone reduces LBX1 levels by >50% OR NAD+ rescues LBX1 under unloading.
  - **Supported if:** Only mechanical unloading reduces LBX1; metabolic manipulation has no effect.

## Summary of Criteria
| Hypothesis Component | Test | Falsification (Evidence AGAINST Hypothesis) |
| :--- | :--- | :--- |
| **Direct Mechanosensor** | Exp 1 (Strain) | No response to 10% strain (FC < 1.5). |
| **Structural Element** | Exp 2 (AFM) | No stiffness gain (< 0.5 kPa). |
| **Mechanics > Metabolism** | Exp 3 (Mimicry) | ATP depletion mimics unloading; NAD+ rescues unloading. |
