# LBX1 Falsifiability Plan: The "Disordered Mechanogating" Hypothesis

**Date**: 2026-02-22
**Status**: Proposed
**Context**: Structural analysis reveals LBX1 is not a rigid "tension rod" (Anisotropy 2.27, Confidence 0.26) but a "blocky scaffold" (Blockiness 7.35) with high intrinsic disorder. This suggests it acts as a "soft sensor" or "phase separator" rather than a force transmitter.

---

## Core Hypothesis: Disordered Nuclear Mechanogating
**Statement**: LBX1 nuclear translocation and chromatin binding are strictly regulated by cytoskeletal tension. The high intrinsic disorder (IDR) of LBX1 prevents nuclear import in relaxed (low-tension) cells, effectively silencing it in atrophic or unloaded paraspinal muscles.

**Falsifiability Criteria**: If LBX1 nuclear localization is constitutive (independent of substrate stiffness or cell tension), the hypothesis is false.

---

## Experiment 1: Stiffness-Dependent Nuclear Translocation
**Objective**: Determine if substrate stiffness gates LBX1 nuclear entry.

*   **Model**: C2C12 Myoblasts (murine).
*   **Conditions**:
    1.  **Soft Hydrogel (0.5 kPa)**: Mimics atrophic/unloaded muscle.
    2.  **Stiff Hydrogel (40 kPa)**: Mimics healthy/loaded muscle.
    3.  **Control**: Glass coverslips (>1 GPa).
*   **Method**: Immunofluorescence staining for LBX1 and YAP1 (positive control).
*   **Readout**: Nuclear-to-Cytoplasmic (N/C) fluorescence intensity ratio.
*   **Expected Result**:
    *   **Soft**: Low LBX1 N/C ratio (< 1.0).
    *   **Stiff**: High LBX1 N/C ratio (> 1.5).
*   **Falsification Threshold**:
    *   If LBX1 N/C ratio is statistically indistinguishable between Soft and Stiff conditions (p > 0.05).
    *   If LBX1 is nuclear in Soft conditions.

---

## Experiment 2: Force-Dependent Chromatin Binding (Stretch-ChIP)
**Objective**: Test if mechanical stretch is required for LBX1 to bind its target genes.

*   **Model**: Primary human paraspinal myotubes cultured on flexible silicone membranes.
*   **Conditions**:
    1.  **Static**: No stretch.
    2.  **Cyclic Stretch**: 10% strain, 0.5 Hz for 24 hours.
*   **Method**: ChIP-seq for LBX1.
*   **Readout**: Peak enrichment at known AIS susceptibility loci (e.g., *GPR126*, *PAX1*).
*   **Expected Result**: Significant (>2-fold) increase in peak height/number under Cyclic Stretch.
*   **Falsification Threshold**:
    *   If LBX1 binding profiles are identical between Static and Stretch.
    *   If LBX1 binds targets strongly in Static conditions (suggesting constitutive activity).

---

## Experiment 3: Rescue by Rigidification (Mutant Analysis)
**Objective**: Prove that the *intrinsic disorder* is the sensor.

*   **Design**: Construct a "Rigid-LBX1" mutant where the disordered linker regions are replaced by rigid alpha-helical spacers (e.g., EAAAK repeats), preserving the Homeobox DNA-binding domain.
*   **Model**: C2C12 cells on Soft Hydrogels (0.5 kPa).
*   **Method**: Transfect WT-LBX1 vs Rigid-LBX1. Measure myogenic differentiation (MYOD1 expression) which usually fails on soft matrices.
*   **Hypothesis**: The disorder "collapses" in low tension, blocking import. The Rigid mutant cannot collapse, so it should bypass the checkpoint.
*   **Readout**: % Myogenin-positive cells.
*   **Expected Result**:
    *   **WT-LBX1 on Soft**: Low differentiation.
    *   **Rigid-LBX1 on Soft**: High differentiation (Rescue).
*   **Falsification Threshold**:
    *   If Rigid-LBX1 fails to rescue differentiation on soft matrices.
    *   If Rigid-LBX1 localization mimics WT-LBX1.

---

## Conclusion
These experiments move the Biological Countercurvature hypothesis from "correlation" (LBX1 is mutated in AIS) to "mechanism" (LBX1 is a tension sensor). The failure of any of these tests would force a pivot back to purely biochemical or developmental explanations for LBX1's role.
