# LBX1 Falsifiability Plan

## Overview
This document defines concrete, experimental falsification criteria for the hypothesized link between LBX1 and mechanotransduction in the Biological Countercurvature model. It is designed to constrain narrative speculation with direct measurement. Generated from `outputs/afcc/2026-02-16/metrics.csv` evidence.

## Evidence Landscape
- **[Confirmed by metrics]**: AlphaFold metrics consistently place LBX1 in a low-confidence, intermediate-anisotropy state. It is highly blocky (PAE domains).
- **[Speculative narrative]**: LBX1 acts as a "structural integration hub" or directly modulates its signaling based on mechanical tension along an anisotropic axis.

## Falsification Experiments

### Experiment 1: The Force-Displacement Assay
- **Hypothesis**: LBX1 function depends on its ability to sustain tension as an intermediate scaffolding element.
- **Assay Design**: Perform single-molecule optical tweezers or atomic force microscopy (AFM) pulling on purified, full-length LBX1 protein.
- **Quantitative Readout**: Unfolding force (pN) and contour length extension (nm) of the predicted blocky domains versus the low-confidence linker regions.
- **Expected Direction**: If LBX1 is a tension element, the low-confidence regions should act as entropic springs, while the blocky domains unfold cooperatively under specific force thresholds.
- **Falsification Threshold**: If LBX1 unfolding forces are universally low (e.g., < 5-10 pN) and show no cooperative domain unfolding, the protein cannot transmit significant mechanical force in vivo. The "tension rod / structural hub" hypothesis is falsified.

### Experiment 2: Tension-Dependent Nuclear Localization
- **Hypothesis**: LBX1 nuclear localization or retention is mechanically gated, linking its transcriptional role to cell shape.
- **Assay Design**: Culture human sensory neurons or muscle precursors (where LBX1 is expressed) on hydrogels of varying stiffness (e.g., 1 kPa vs 20 kPa) or subject them to cyclic stretch.
- **Quantitative Readout**: Nuclear to cytoplasmic fluorescence ratio of endogenous LBX1 via immunocytochemistry.
- **Expected Direction**: Localization should scale linearly or non-linearly with applied tension or substrate stiffness.
- **Falsification Threshold**: If the nuclear/cytoplasmic ratio of LBX1 is statistically indistinguishable ($p > 0.05$) between unloaded (soft) and mechanically loaded (stiff/stretched) conditions, its function is chemically, not mechanically, gated.

### Experiment 3: Domain-Deletion Rescue
- **Hypothesis**: The specific high-PAE blocky domains identified by AlphaFold are required for its hypothesized countercurvature function.
- **Assay Design**: Create CRISPR knockout cell lines for LBX1. Rescue with either wild-type LBX1 or mutants lacking specific blocky domains or low-confidence linker regions. Apply a mechanical challenge (e.g., fluid shear or cyclic stretch).
- **Quantitative Readout**: Transcriptional output of known mechanosensitive target genes (e.g., EGR1, FOS) or downstream proprioceptive markers.
- **Expected Direction**: Deletion of putative mechanical coupling domains will fail to rescue tension-induced transcription.
- **Falsification Threshold**: If a construct lacking the extended/blocky architecture (e.g., just the DNA binding domain and minimal transactivation domain) fully rescues the mechanosensitive transcriptional response, the complex spatial geometry proposed by AFCC is functionally irrelevant to its mechanical role.

## Conclusion
If experiments 1-3 cross their respective falsification thresholds, LBX1 must be reclassified strictly as a downstream chemical effector of proprioceptive identity, and removed from models requiring its physical participation in mechanotransduction or tension integration.
