# LBX1 Falsifiability Plan
**Date:** 2026-03-25

## Overview
This document outlines explicit conditions that would falsify the hypothesis linking LBX1 structural blockiness to mechanosensitivity, specifically the "Nuclear Stiffness-Gated Transcription" hypothesis defined in `reports/structure_clusters/2026-02-01__blocky_lbx1.md`.

## Core Hypothesis
**Source:** `reports/structure_clusters/2026-02-01__blocky_lbx1.md` (Dated 2026-02-01)
**H_2026_02_01_Blocky_LBX1:** The high structural blockiness of LBX1 (PAE blockiness >7) renders its function uniquely dependent on nuclear stiffness (Lamin A/C tension). In a "soft" nucleus (e.g., loss of tension, microgravity, or scoliosis onset), the loss of tension causes LBX1 to undergo conformational collapse, reducing its transcriptional efficiency relative to structurally "monolithic" TFs like RUNX3.

## Falsifying Experiments

### Experiment 1: Lamin A/C Knockdown & LBX1 Localization
- **Hypothesis:** Decreasing nuclear stiffness via LMNA knockdown will cause LBX1 to mislocalize (reduce nuclear accumulation) or misfold, whereas RUNX3 localization will be unaffected.
- **Assay Design:** Transfect C2C12 myoblasts or neural progenitor cells with GFP-tagged LBX1 and RFP-tagged RUNX3. Induce a "soft" nucleus using Lamin A/C siRNA. Use confocal microscopy to measure the Nuclear/Cytoplasmic (N/C) fluorescence ratio.
- **Quantitative Readout:** Change in N/C ratio for LBX1 and RUNX3 relative to scrambled siRNA controls.
- **Expected Direction:** LBX1 N/C ratio decreases significantly; RUNX3 N/C ratio remains stable.
- **Falsification Threshold:** If the decrease in LBX1 N/C ratio is less than 15% relative to the control, or if RUNX3 shows an equal or greater decrease in nuclear localization than LBX1, the hypothesis is **falsified**.

### Experiment 2: Transcriptional Activity under Nuclear Softening
- **Hypothesis:** LBX1 transcriptional efficiency strictly requires nuclear tension, while RUNX3 does not.
- **Assay Design:** Use luciferase reporter constructs driven by LBX1-specific and RUNX3-specific promoters in the same cell line. Treat cells with Latrunculin B (actin depolymerization) to disrupt LINC complex-mediated nuclear tension.
- **Quantitative Readout:** Relative luciferase activity (luminescence) normalized to Renilla control.
- **Expected Direction:** LBX1-driven luciferase activity drops dramatically; RUNX3-driven activity remains at baseline.
- **Falsification Threshold:** If LBX1-driven transcriptional activity does not decrease by at least 30%, or if it behaves identically to RUNX3-driven activity under Latrunculin B treatment, the hypothesis is **falsified**.

### Experiment 3: Synthetic Linker Stiffening (Domain Manipulation)
- **Hypothesis:** The specific "beads-on-a-string" flexibility of LBX1 is required for its mechanosensitivity.
- **Assay Design:** Create a mutant LBX1 construct (LBX1-Stiff) where the intrinsically disordered flexible linkers between its domains are replaced with rigid alpha-helical linkers (e.g., EAAAK repeats). Expose cells to cyclical mechanical stretch (10% strain, 1Hz) vs. static culture.
- **Quantitative Readout:** Expression levels of downstream target genes (e.g., via RT-qPCR) in static vs. stretched conditions.
- **Expected Direction:** Wild-type LBX1 shows differential target gene expression between static and stretch conditions. LBX1-Stiff loses this differential response.
- **Falsification Threshold:** If the rigidified LBX1-Stiff mutant maintains the exact same mechanosensitive differential expression profile as Wild-type LBX1 under cyclical stretch, the specific "blocky" flexibility hypothesis is **falsified**.
