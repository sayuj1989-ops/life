# LBX1 Falsifiability Plan

**Date Generated:** 2026-03-23
**Source Data:** `outputs/afcc/2026-02-16/metrics.csv`, `reports/confidence_weighted_structural_evidence.md`

## Overview
To move beyond speculative structural interpretations of AlphaFold geometry, we must define explicit, quantitative criteria that would falsify the claim that LBX1 acts as a mechanosensor or mechanical transducer in spinal development.

## Experiment 1: Domain-Specific Deletion and Tension Response
**Hypothesis**: If LBX1's high-blockiness, intermediate-anisotropy domains act as a direct mechanical spring or tension sensor, deleting the specific disordered linker domains will abolish its localization or transcriptional response to nuclear tension.
- **Assay Design**: Create wild-type and linker-deleted LBX1-GFP constructs. Express in neural crest / spinal progenitor cell lines. Apply controlled cyclic stretch (via flexible substrate) to modulate nuclear tension.
- **Quantitative Readout**: Ratio of nuclear-to-cytoplasmic GFP fluorescence and downstream target gene (e.g., *Atoh1*) transcript levels via qPCR.
- **Expected Direction**: WT LBX1 nuclear localization and target transcription increases with tension. Deletion mutant shows no tension-dependent change.
- **Falsification Threshold**: If the WT construct shows < 1.5-fold change in nuclear localization under tension, OR if the deletion mutant responds identically to WT (p > 0.05), the hypothesis that LBX1's specific geometry acts as a mechanical sensor is falsified.

## Experiment 2: Biophysical Stiffness Measurement
**Hypothesis**: High PAE blockiness in AlphaFold predicts a modular architecture that behaves as a compliant mechanical element (spring) under physiological force.
- **Assay Design**: Purify recombinant full-length LBX1. Perform single-molecule Force Spectroscopy using Atomic Force Microscopy (AFM) or Optical Tweezers to pull the protein from its N- and C-termini.
- **Quantitative Readout**: Persistence length ($L_p$) and unfolding forces (pN) from force-extension curves.
- **Expected Direction**: LBX1 should exhibit a characteristic sawtooth pattern with distinct unfolding forces for its structured domains, separated by highly extensible (low persistence length) linker regions.
- **Falsification Threshold**: If the persistence length of the full-length protein is equivalent to a completely disordered random coil, OR if the force required to unfold the complex is < 5 pN (indistinguishable from thermal noise), it cannot function as a stable mechanical load-bearing element in vivo.

## Experiment 3: LINC Complex Uncoupling
**Hypothesis**: LBX1's putative mechanical role requires physical coupling to the nuclear envelope tension network (LINC complex) mediated by Lamin A/C (LMNA).
- **Assay Design**: Co-immunoprecipitation (Co-IP) of LBX1 and LMNA/SUN/KASH domain proteins under high vs. low tension (e.g., latrunculin A treatment to disrupt actin). Additionally, measure LBX1 transcriptional activity in an LMNA-knockout background.
- **Quantitative Readout**: Western blot densitometry ratio of Co-IP'd LBX1 to LMNA; luciferase reporter activity for LBX1 targets.
- **Expected Direction**: Tension increases physical association between LBX1 and LINC components; removing LMNA abolishes LBX1 tension-sensitivity.
- **Falsification Threshold**: If Co-IP shows no significant binding between LBX1 and LINC components under any tension state, OR if LBX1 transcriptional activity remains fully tension-responsive in LMNA-KO cells, the hypothesis of direct mechanical coupling via the LINC complex is falsified.
