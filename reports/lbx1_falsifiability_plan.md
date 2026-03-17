# LBX1 Falsifiability Plan

*Generated Date: 2026-02-19*

## Core Hypothesis
LBX1 functions as a mechanosensor or structural signaling node critical to spinal curvature and symmetry, as suggested by its PAE blockiness and presence in mechanotransduction clusters.

## Caveat Addressed
Current AlphaFold data (`outputs/afcc/2026-02-16/metrics.csv`) indicates LBX1 is intermediate in anisotropy (~2.27) and has low confidence (pLDDT ~66.9). The structural mechanics inference is currently underdetermined by these static, low-confidence in-silico metrics.

## Falsification Experiments

### Experiment 1: Direct Force Application (Magnetic Tweezers)
- **Hypothesis**: LBX1 domains undergo force-dependent conformational changes (unfolding of blocky domains) under physiological tensions (e.g., 5-15 pN), acting as a mechanosensitive switch.
- **Assay Design**: Single-molecule magnetic tweezers on purified full-length LBX1 constructs flanked by handle domains.
- **Quantitative Readout**: Stepwise unfolding extension length (nm) vs. Applied force (pN).
- **Expected Direction**: If LBX1 is a mechanosensor, we expect reproducible unfolding steps at physiological forces (analogous to talin or alpha-catenin), exposing cryptic binding sites.
- **Falsification Threshold**: If LBX1 requires forces > 30 pN to unfold (non-physiological for paraspinal nuclei/cytoplasm) or shows no discrete, reversible unfolding steps, the mechanosensor structural hypothesis is falsified.

### Experiment 2: Subcellular Localization under Substrate Strain
- **Hypothesis**: LBX1 nuclear/cytoplasmic localization is dynamically responsive to extracellular matrix (ECM) stiffness and cyclic strain.
- **Assay Design**: Culture LBX1-GFP tagged paraspinal muscle progenitors on tunable polyacrylamide gels (soft 1 kPa vs. stiff 20 kPa) and apply cyclic uniaxial stretch (10% strain, 1 Hz).
- **Quantitative Readout**: Nuclear-to-cytoplasmic (N/C) ratio of LBX1 fluorescence intensity.
- **Expected Direction**: Increased N/C ratio on stiff substrates and under stretch, typical of mechanosensitive transcriptional regulators (like YAP/TAZ).
- **Falsification Threshold**: If the N/C ratio remains constant (variance < 10%) regardless of substrate stiffness or cyclic strain, LBX1 is not directly responsive to tissue-level mechanical state.

### Experiment 3: Interactome Re-wiring by Mechanical Load
- **Hypothesis**: The blocky PAE structure of LBX1 mediates condition-specific protein-protein interactions (PPIs) that shift under mechanical loading.
- **Assay Design**: BioID or AP-MS on LBX1 in paraspinal cells subjected to either static culture or equibiaxial mechanical stretch.
- **Quantitative Readout**: Differential fold-change in spectral counts/intensity of LBX1-interacting proteins (e.g., LMNA, actin, chromatin modifiers).
- **Expected Direction**: Significant shift (>2-fold change, p<0.05) in interactors towards cytoskeletal/nuclear lamina components under stretch.
- **Falsification Threshold**: If the LBX1 interactome shows no significant loading-dependent restructuring (Spearman correlation between static and stretched interactome > 0.9), its role as a dynamic mechanotransducer node is falsified.
