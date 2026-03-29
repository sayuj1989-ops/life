# LBX1 Falsifiability Plan

## Objective
Establish rigorous, testable criteria to confirm or refute the hypothesis that LBX1 acts directly as a structural mechanosensor or primary "tension rod" in spine morphogenesis, based on the findings that its AlphaFold structural confidence is low (pLDDT: 66.9) and blocky (PAE: 7.35).

## Core Question
Does LBX1 transduce mechanical force directly via its extended geometry, or is it purely a biochemical transcription factor acting downstream of true mechanosensors (like PIEZO2 or ADGRG6)?

---

### Experiment 1: In vitro Nuclear Tension Perturbation

**Hypothesis:** If LBX1 is a direct mechanosensor reliant on its geometry, altering nuclear stiffness or LINC complex connectivity will shift its nuclear localization or transcriptional activity independently of biochemical signaling cascades.

**Assay Design:**
1. Isolate primary human myoblasts/somite progenitors expressing wild-type LBX1.
2. Perturb nuclear tension via LMNA knock-down (siRNA) or LINC complex disruption (KASH domain overexpression).
3. Apply cyclic mechanical stretch to the substrate.

**Quantitative Readout:**
- Ratio of nucleoplasmic to chromatin-bound LBX1 (via cellular fractionation and Western blot).
- Transcriptional activity of direct LBX1 targets (via RT-qPCR).

**Expected Direction (if Mechanosensor):**
LBX1 chromatin binding and target transcription should heavily scale with mechanical stretch in wild-type cells, but become blunted or randomized in LMNA/LINC-disrupted cells.

**Falsification Threshold:**
If LBX1 localization/activity changes by less than 20% between mechanically stretched vs. static cells, or if its activity is unaffected by LINC/LMNA disruption, the direct structural mechanosensor hypothesis is **falsified**.

---

### Experiment 2: Domain-Fragment Geometry Disruption

**Hypothesis:** If the highly blocky, low-confidence regions of LBX1 (predicted by AlphaFold) are critical for mechanical force transmission, deleting the non-DNA-binding "linker" regions will abolish its mechanosensitivity while preserving baseline biochemical activity.

**Assay Design:**
1. Synthesize full-length LBX1, and a truncated mutant ($\Delta$-linker) missing the highest-PAE (most flexible/uncertain) regions while retaining the DNA-binding homeobox domain.
2. Rescue LBX1 knockout cells with either construct.
3. Apply mechanical load (e.g., fluid shear or substrate stiffening).

**Quantitative Readout:**
- Transcriptional reporter assay (e.g., Luciferase driven by an LBX1 consensus promoter) measured across a stiffness gradient (1 kPa vs. 50 kPa).

**Expected Direction (if Mechanosensor):**
The $\Delta$-linker mutant should lose stiffness-dependent transcriptional scaling compared to full-length LBX1.

**Falsification Threshold:**
If the $\Delta$-linker mutant retains identical stiffness-dependent scaling to the wild-type, or if neither construct scales with stiffness, the hypothesis that LBX1's specific extended geometry is mechanically load-bearing is **falsified**.

---

### Experiment 3: Biophysical Stiffness Measurement (AFM/Tweezer)

**Hypothesis:** For LBX1 to act as a tension rod, the folded protein must possess a non-trivial mechanical yield strength capable of sustaining physiological intracellular forces without catastrophic unfolding, unlike purely globular or highly disordered biochemical factors.

**Assay Design:**
1. Purify recombinant human LBX1 protein.
2. Perform single-molecule Force Spectroscopy using Optical Tweezers or Atomic Force Microscopy (AFM).
3. Compare force-extension curves against a known rigid rod (e.g., LMNA fragment) and a known globular protein (e.g., GAPDH).

**Quantitative Readout:**
- Peak unfolding force (pN).
- Persistence length ($L_p$) derived from the Worm-Like Chain (WLC) model fit.

**Expected Direction (if Mechanosensor):**
LBX1 should exhibit a distinct force-extension profile with high initial stiffness, comparable to structural scaffolding proteins, rather than the low-force continuous stretching of a purely disordered IDP.

**Falsification Threshold:**
If LBX1 exhibits a peak unfolding force of < 10 pN (indistinguishable from thermal noise or highly disordered proteins) or lacks a clear cooperative unfolding step characteristic of mechanically resistant domains, the structural tension-rod hypothesis is **falsified**.

---
**References & Sources:**
- Latest Authoritative Snapshot: `outputs/afcc/2026-02-16/metrics.csv`
- Confidence-Weighted Evidence: `reports/confidence_weighted_structural_evidence.md`
