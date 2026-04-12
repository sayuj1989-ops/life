# LBX1 Mechanics Link: Falsifiability Plan

**Date Generated:** 2026-04-12
**Source Data Baseline:** `outputs/afcc/2026-02-16/metrics.csv`

## Overview
This document outlines explicit criteria and experiments designed to formally test (and potentially falsify) the hypothesis that LBX1 plays a direct mechanical, structural, or geometric role in scoliosis pathogenesis, distinct from its known role as a developmental transcription factor.

AlphaFold metrics characterize LBX1 as an intermediate-anisotropy (2.27), highly blocky (PAE=7.35), but low-confidence (pLDDT=66.9) protein. Relying solely on static predictions risks narrative inflation. The following experiments provide concrete paths to reject the mechanosensor hypothesis.

---

## Experiment 1: Direct Mechanical Stiffness / Tension Measurement
**Hypothesis:** If LBX1 functions structurally (like a load-bearing tether or tension sensor in the nucleoskeleton/cytoskeleton network), it should physically resist deformation or localize under applied tension.
- **Assay Design:**
  1. Express fluorescently tagged LBX1 in primary somite/muscle-derived cells.
  2. Subject cells to cyclical mechanical stretching and measure LBX1 localization (does it move to high-tension regions?).
  3. Perform Atomic Force Microscopy (AFM) or magnetic tweezer pulling on isolated LBX1 domains to measure force-extension curves.
- **Quantitative Readout:** Piconewton (pN) unfolding forces and localization enrichment ratio (nuclear/cytoplasmic or matrix/cytoplasmic) under strain vs. rest.
- **Expected Direction:** If mechanical, LBX1 should exhibit a measurable force-extension curve distinct from random coil, or actively relocalize in a tension-dependent manner (like YAP/TAZ).
- **Falsification Threshold:** *Falsified if* LBX1 behaves as a generic random coil under AFM with no discrete unfolding steps, AND its localization ratio under mechanical strain shows no statistically significant difference from unstrained controls ($p > 0.05$).

---

## Experiment 2: Truncation/Mutagenesis of "Blocky" Domains
**Hypothesis:** The high PAE "blockiness" observed in AlphaFold predictions corresponds to distinct mechanical modules necessary for its theorized physical function. Removing non-DNA-binding modules should abrogate the structural/mechanical phenotype while preserving basic transcriptional ability.
- **Assay Design:**
  1. Generate LBX1 truncation mutants lacking the predicted structurally flexible/blocky regions (but retaining the homeobox domain).
  2. Rescue LBX1 knockout cells with either wild-type or truncated LBX1.
  3. Measure a downstream mechanical phenotype (e.g., cell stiffness, ECM traction forces).
- **Quantitative Readout:** Cellular traction force (measured via Traction Force Microscopy, TFM) and transcriptomic rescue profile.
- **Expected Direction:** Truncated LBX1 should fail to rescue mechanical phenotypes (traction force) despite successfully rescuing transcription of core targets.
- **Falsification Threshold:** *Falsified if* the truncation mutants fully rescue both transcriptional targets AND cellular mechanics equivalently to wild-type LBX1. This would prove the "blocky" non-DNA-binding regions do not possess an independent mechanical function.

---

## Experiment 3: Interaction with Known Mechanosensors (LINC Complex/LMNA)
**Hypothesis:** If LBX1 connects transcription directly to geometric/mechanical sensing in the spine, it must physically or functionally couple with known nuclear mechanotransducers (e.g., LMNA, the LINC complex).
- **Assay Design:**
  1. Perform co-immunoprecipitation (Co-IP) or proximity labeling (BioID) for LBX1 in cells subjected to stiff vs. soft extracellular matrices.
  2. Perform dual-knockdown of LBX1 and LMNA to test for epistatic or synergistic effects on nuclear morphology.
- **Quantitative Readout:** Fold enrichment of interaction partners (LMNA, SUN1/2) in mass spectrometry; quantitative nuclear shape index (circularity/aspect ratio).
- **Expected Direction:** LBX1 should physically interact with LINC/LMNA components, and this interaction should scale with matrix stiffness.
- **Falsification Threshold:** *Falsified if* proximity labeling reveals exclusively transcriptional machinery (no structural/LINC partners) regardless of matrix stiffness, AND dual-knockdown yields purely additive (non-epistatic) effects on cellular morphology.

---

## Conclusion
A failure to demonstrate tension-dependent localization, distinct unfolding mechanics, or direct coupling to the mechanosensory apparatus would strongly suggest that LBX1's link to scoliosis is entirely biochemical/transcriptional, and that geometric interpretation of its low-confidence AlphaFold structure is an artifact.
