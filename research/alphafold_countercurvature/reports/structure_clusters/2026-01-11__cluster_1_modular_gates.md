# Structure Cluster Report: The "Modular Mechanogate" Complex
**Date:** 2026-01-11
**Cluster:** 1 (Moderate Anisotropy, High Blockiness)
**Analysis Type:** Unsupervised K-Means on AFCC Metrics

## 1. Cluster Members
LBX1, YAP1, ADGRG6, ITGB1, WWTR1, FLNB, FGFR1, CDH2, DLL3, HES7, PTK2, COL2A1, CELSR1, COL11A1, SHH, LFNG, RUNX2, PKD1L1, COMP, KIF6, MATN1, SCUBE3.

## 2. Structural Signature
*   **Moderate Anisotropy (~2.68):** These proteins have extended shapes but are not as strictly linear as the "Strain Antennas" (Cluster 0).
*   **High Blockiness (~6.58):** This is the defining feature. High blockiness (high inter-domain PAE vs low intra-domain PAE) indicates a "beads-on-a-string" architecture where rigid, well-folded domains are connected by flexible, disordered linkers.
*   **Interpretation:** These are **"Modular Integrators"** or **"Logic Gates"**. The flexible hinges allow significant conformational change (bending/folding) without disrupting the individual domains.

## 3. Biological Context
*   **Effectors:** YAP1/WWTR1 (Hippo), LBX1 (Transcription Factor).
*   **Adhesion/Receptors:** ADGRG6 (GPR126), ITGB1 (Integrin), CDH2 (Cadherin), FGFR1.
*   **ECM:** COL2A1, COL11A1, COMP, MATN1.
*   **Pattern:** This cluster contains the *downstream* effectors and the *binding* interfaces of the mechanotransduction system.

## 4. Hypothesis: Hinge-Mediated Signal Integration
**Statement:** Cluster 1 proteins function as **"Modular Mechanogates"**. Their high-blockiness architecture allows them to integrate multiple signals (mechanical strain + chemical ligand) via **Hinge Unfolding**.
*   **Mechanism:** Tension across the protein (e.g., pulling on ITGB1 or ADGRG6) extends the flexible linkers, exposing "cryptic" binding sites or phosphorylation motifs that are occluded in the relaxed (folded) state.
*   **Logic:** Unlike the "Antennas" (Cluster 0) which *transmit* the vector, these proteins *process* the scalar magnitude of strain by unfolding.

## 5. Proposed Test
*   **Experiment:** "FRET-Hinge Strain Sensing"
*   **System:** HEK293T cells expressing FRET biosensors inserted into the high-PAE hinge regions of Cluster 1 candidates (e.g., ADGRG6 linker region, YAP1 linker).
*   **Method:** Apply graded uniaxial stretch. Measure FRET efficiency change (unfolding) vs. strain magnitude.
*   **Prediction:** Cluster 1 proteins will show a sharp, non-linear FRET decrease (unfolding) at physiological strain thresholds, acting as binary switches, whereas Cluster 0 proteins (stiff) will show negligible conformational change.
