# LBX1 Falsifiability Plan

**Date:** 2026-02-19
**Focus:** Isolating the role of LBX1 in Biological Countercurvature
**Status:** High-Priority Rigor Enforcer

## The Challenge
Current hypotheses (e.g., 2026-01-20 "The Silenced Spring") suggest LBX1 acts mechanically via "tension-gated scaffolds." However, quantitative metrics (Anisotropy 2.27, pLDDT 66.9, Blockiness 7.35) are static and low-confidence. We must pivot from descriptive narrative to falsifiable experimentation.

## Falsifiability Package: "What would falsify the LBX1-Mechanics Link?"

If LBX1 is purely a downstream developmental transcription factor, insensitive to direct or local mechanical forces, then these experiments will yield negative results, directly refuting the structural-mechanical hypothesis for LBX1.

### Experiment 1: The Tension-Unfolding Assay (In Vitro)
**Hypothesis:** LBX1's "blocky" domains undergo tension-dependent unfolding to expose cryptic binding sites or alter localization (The "Silenced Spring" model).
**Assay Design:**
1. Recombinant expression of LBX1 linked to a FRET tension-sensor cassette (e.g., cpstFRET).
2. Immobilize LBX1 on a stretchable PDMS substrate via specific tags.
3. Apply graded uniaxial cyclic stretch (0%, 5%, 10%, 15% strain) at 1 Hz for 4 hours.
**Quantitative Readout:** Change in FRET efficiency ($\Delta E_{FRET}$) indicating intramolecular distance changes between blocky domains.
**Expected Direction:** Tension (stretch) should decrease FRET efficiency (unfolding/extension).
**Falsification Threshold:** If $\Delta E_{FRET} < 5\%$ (indistinguishable from noise) between 0% and 15% strain, LBX1 is **NOT** a direct mechanosensor or tension-gated scaffold. The hypothesis is falsified.

### Experiment 2: The Nuclear-Tension Decoupling Assay (In Vivo)
**Hypothesis:** LBX1 transcriptional activity is directly regulated by cytoskeletal tension transmitted to the nucleus (e.g., via LMNA/LINC complex).
**Assay Design:**
1. Use zebrafish embryos (somite stage) expressing an LBX1-responsive GFP reporter.
2. Perturb nuclear mechanotransduction using a dominant-negative KASH domain construct (dnKASH) to decouple the LINC complex, isolating the nucleus from cytoskeletal forces.
3. Compare reporter activity in normal 1g conditions versus simulated microgravity (unloading).
**Quantitative Readout:** Total GFP fluorescence intensity in somitic mesoderm.
**Expected Direction:** dnKASH should phenocopy microgravity unloading, reducing LBX1 reporter activity.
**Falsification Threshold:** If dnKASH embryos show **NO significant difference** in LBX1 reporter activity compared to controls under normal 1g conditions (p > 0.05), LBX1 expression is governed purely by biochemical gradients (e.g., Wnt/Hedgehog) and is mechanically insulated. The hypothesis is falsified.

### Experiment 3: The Iso-Volumetric Compression Assay (Ex Vivo)
**Hypothesis:** LBX1 responds to the Information-Elasticity Coupling (IEC) and gravitational loading independent of gross tissue deformation.
**Assay Design:**
1. Explant murine embryonic presomitic mesoderm (PSM).
2. Apply isotropic hydrostatic pressure (compressing volume without uniaxial strain) to simulate loading without tissue distortion.
3. Perform rapid-fixation and single-cell RNA sequencing (scRNA-seq) or q-RT-PCR for LBX1 and downstream targets.
**Quantitative Readout:** Log2 fold-change in LBX1 transcript levels compared to unpressurized controls.
**Expected Direction:** Compression should increase LBX1 expression if it acts as a generalized mechanical integrator.
**Falsification Threshold:** If hydrostatic pressure fails to upregulate LBX1 expression (Log2FC < 0.5, p > 0.05), LBX1 is **NOT** a generalized load-sensor. If it only responds to shear/strain (Experiment 1/2), its role is localized; if it responds to neither, it is mechanically uncoupled. The hypothesis is falsified.

## Conclusion
Executing these three experiments will categorically determine if LBX1 is a direct participant in the mechanical aspects of biological countercurvature, or if it is merely a biochemical prerequisite.
