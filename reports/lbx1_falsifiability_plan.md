# LBX1 Falsifiability Plan

## Overview
LBX1 is central to the biological counter-curvature hypothesis as a somite-derived biomechanical effector. However, its AlphaFold structural predictions indicate a low-confidence, intermediate-anisotropy geometry with high PAE blockiness (pLDDT ~66.9, Anisotropy ~2.27, based on `outputs/afcc/2026-02-16/metrics.csv`). This document outlines explicit criteria and three concrete experiments that would falsify the hypothesized link between LBX1 and spinal mechanics.

## Falsification Criteria
The LBX1-mechanics link will be considered falsified if:
1. LBX1 does not physically interact with or regulate mechanosensory complexes (e.g., PIEZO2, integrins, or LMNA) in somite-derived tissues.
2. Perturbation of LBX1 does not alter cellular stiffness, nuclear tension, or extracellular matrix organization.
3. The "blocky" modular geometry predicted by AlphaFold does not correspond to actual biomechanical hinges or tension-bearing domains in vivo.

## Experiment 1: Nuclear Tension and LINC Complex Localization
**Hypothesis:** If LBX1 acts as a mechanotransducer or structural node, it localizes to or modulates tension-bearing structures like the LINC complex (e.g., LMNA) under mechanical stress.
- **Assay Design:** Subject somite-derived myoblasts to cyclic stretch (via flexible culture substrates). Measure LBX1 nuclear/cytoplasmic localization and its co-immunoprecipitation with LMNA and nesprins.
- **Quantitative Readout:** Ratio of nuclear to cytoplasmic LBX1 fluorescence intensity; normalized co-IP enrichment fold-change versus static control.
- **Expected Direction:** LBX1 nuclear localization and LINC interaction increase under cyclic stretch.
- **Falsification Threshold:** If the nuclear/cytoplasmic ratio does not significantly increase (p > 0.05) or co-IP enrichment is < 1.5-fold under mechanical loading, LBX1 is unlikely to function as a tension-responsive node at the nuclear envelope.

## Experiment 2: Cellular Stiffness and Proprioceptive Architecture
**Hypothesis:** If LBX1 dictates somitic structural architecture, its knockdown will reduce overall cellular stiffness and disrupt proprioceptive mechanosensor (e.g., PIEZO2) cluster formation.
- **Assay Design:** Perform siRNA knockdown of LBX1 in muscle progenitor cells. Measure single-cell stiffness using Atomic Force Microscopy (AFM) and quantify PIEZO2 surface cluster density via super-resolution microscopy.
- **Quantitative Readout:** Young's Modulus (kPa) via AFM; PIEZO2 cluster count per square micron.
- **Expected Direction:** LBX1 knockdown significantly decreases Young's Modulus and reduces PIEZO2 clustering.
- **Falsification Threshold:** If the reduction in Young's Modulus is < 10% or PIEZO2 cluster density remains statistically unchanged (p > 0.05) compared to scrambled siRNA controls, the structural role of LBX1 is falsified.

## Experiment 3: Domain-Fragment Structural Integrity
**Hypothesis:** If the high PAE blockiness of LBX1 (score ~7.35, referenced in `outputs/afcc/2026-02-16/metrics.csv`) reflects true mechanical hinges, isolated inter-block domains will exhibit flexible tethering behavior while individual blocks remain rigidly folded.
- **Assay Design:** Express full-length LBX1 and isolated block domains (identified via AlphaFold PAE matrices) as recombinant proteins. Perform Small Angle X-ray Scattering (SAXS) and single-molecule Fluorescence Resonance Energy Transfer (smFRET) to measure conformational dynamics and radius of gyration (Rg).
- **Quantitative Readout:** Rg from SAXS; FRET efficiency distributions (histogram width) between terminal fluorophores.
- **Expected Direction:** Full-length LBX1 shows a bimodal or highly dispersed FRET efficiency (indicating a flexible hinge), while isolated domains show narrow FRET distributions (rigid folding).
- **Falsification Threshold:** If full-length LBX1 exhibits a singular, narrow FRET distribution (indicating a rigidly compact or entirely unstructured protein rather than a hinged scaffold) or if SAXS Rg strictly matches a purely globular protein (Rg < 25 Å), the hypothesized "blocky hinge" mechanism is falsified.
