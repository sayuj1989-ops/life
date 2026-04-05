# LBX1 Falsifiability Plan

## Overview
This document defines concrete, measurable experiments to test the hypothesized link between LBX1 and spinal mechanotransduction. The objective is to provide a rigorous framework for identifying whether the structural observations of LBX1 translate to mechanically active roles in vivo or in vitro, distinguishing direct mechanistic involvement from correlated artifacts.

## Source Data & Citations
- Base hypotheses are derived from predicted structural data: `outputs/afcc/2026-02-16/metrics.csv`
- Structural confidence context established in: `reports/confidence_weighted_structural_evidence.md`

## Experiment 1: Nuclear Deformation and LBX1 Relocalization
**Hypothesis**: If LBX1 acts as a mechanosensitive transcription factor linking tension to growth, altering cytoskeletal tension will result in quantifiable relocalization of LBX1 between the nucleoplasm and functional nuclear domains.
- **Assay Design**: Apply controlled cyclical strain to patient-derived osteoblasts or somite-derived mesenchyme cells using a deformable substrate system (e.g., Flexcell). Use pharmacological modulators of tension (e.g., Blebbistatin to relax, Calyculin A to increase tension).
- **Quantitative Readout**: Ratio of nuclear to cytoplasmic LBX1 fluorescence intensity, and intranuclear clustering fraction measured via high-resolution confocal microscopy and automated image analysis.
- **Expected Direction**: Increased cyclic strain will increase nuclear localization and specific clustering of LBX1.
- **Falsification Threshold**: If the nuclear/cytoplasmic ratio or clustering fraction changes by less than 15% across extreme tension conditions (baseline vs. maximum viable strain/pharmacological tension), the hypothesis that LBX1 dynamically responds to mechanical state is falsified.

## Experiment 2: LINC Complex Uncoupling
**Hypothesis**: LBX1's mechano-response is mediated through direct or indirect physical coupling to the nuclear envelope via the LINC complex (involving LMNA).
- **Assay Design**: Disrupt the LINC complex in a stable LBX1-expressing cell line using dominant-negative KASH domain constructs or SUN1/2 knockdowns. Subject the cells to standard mechanical load.
- **Quantitative Readout**: Expression levels of a selected downstream target gene of LBX1 (measured via qPCR) and chromatin accessibility at known LBX1 binding sites (measured via ATAC-seq).
- **Expected Direction**: Uncoupling the nucleus from the cytoskeleton should abolish the tension-induced upregulation of LBX1 target genes.
- **Falsification Threshold**: If the target gene expression response to load is maintained (i.e., not significantly reduced compared to controls, p > 0.05) after LINC uncoupling, the hypothesis that LBX1's activity depends on force transmission through the nuclear envelope is falsified.

## Experiment 3: Biophysical Validation of High-Blockiness Structure
**Hypothesis**: The high PAE blockiness and intermediate anisotropy observed in AlphaFold models of LBX1 represent true structural modularity critical for binding under tension, rather than merely an artifact of low-confidence unstructured regions.
- **Assay Design**: Purify full-length LBX1 protein. Use single-molecule FRET (smFRET) or small-angle X-ray scattering (SAXS) to measure the conformational ensemble of the protein in solution, both with and without the addition of specific target DNA oligonucleotides and crowding agents to mimic nuclear conditions.
- **Quantitative Readout**: The radius of gyration (Rg) from SAXS or the FRET efficiency histogram spread.
- **Expected Direction**: The protein should exhibit distinct, stable sub-populations (blocks) that compact or shift upon target binding, supporting functional modularity rather than pure random coil behavior.
- **Falsification Threshold**: If the smFRET profile shows a single, broad distribution characteristic of a pure random coil, and SAXS analysis yields a Kratky plot typical of fully unfolded proteins with no stable globular sub-domains (Rg purely scales with chain length), the hypothesis that the predicted blockiness reflects stable structural modules is falsified.
