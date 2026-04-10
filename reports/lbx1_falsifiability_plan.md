# LBX1 Falsifiability Plan

## Introduction
The current hypothesis positions LBX1 as having a modular/blocky architecture (anisotropy ~2.27, PAE blockiness ~7.35) capable of mechanotransduction. However, its low pLDDT (~66.9) indicates potential structural instability or intrinsically disordered regions. This document outlines concrete experiments to rigorously test the hypothesis that LBX1's architecture acts as a mechanosensor.

## Data Provenance
- Date: 2026-02-16
- Reference file: `outputs/afcc/2026-02-16/metrics.csv`

## Explicit Falsification Criteria
The LBX1-mechanics link will be considered falsified if:
1. The protein does not undergo a measurable conformational change or stabilize under physiologically relevant mechanical loads.
2. The purported "blocky" architecture lacks functional independence when the disordered linker regions are removed or replaced.
3. Subcellular localization and functional activity are completely unperturbed by major disruptions to the mechanotransduction pathways (e.g., LINC complex ablation, substrate stiffness variation).

## Proposed Experiments

### Experiment 1: Single-Molecule Force Spectroscopy (SMFS) on LBX1 Domains
- **Hypothesis**: LBX1's blocky regions unfold in a force-dependent manner under physiological tension, acting as a mechanosensitive spring.
- **Assay Design**: Perform SMFS (e.g., optical or magnetic tweezers) on full-length recombinant LBX1.
- **Quantitative Readout**: Unfolding force (pN) and extension length (nm).
- **Expected Direction**: Distinct, measurable force peaks corresponding to the sequential unfolding of the structural blocks.
- **Falsification Threshold**: If the molecule behaves purely as a low-resistance unstructured polymer without defined unfolding force peaks (> 5 pN), the mechanosensitive structural architecture hypothesis is falsified.

### Experiment 2: LINC Complex Dependency for LBX1 Nuclear Localization
- **Hypothesis**: LBX1's activity and localization are dependent on intact mechanical force transmission to the nucleus via the LINC complex.
- **Assay Design**: Assess LBX1 nuclear-to-cytoplasmic ratio in wild-type vs. *LMNA*-null or *SUN1/2*-null cell lines grown on stiff vs. soft substrates.
- **Quantitative Readout**: Nuclear/cytoplasmic fluorescence intensity ratio of tagged LBX1.
- **Expected Direction**: LBX1 nuclear localization should be enhanced on stiff substrates in WT cells but disrupted in LINC-null cells.
- **Falsification Threshold**: If LBX1 localization remains constant regardless of substrate stiffness and LINC complex integrity (change in ratio < 10%), the mechanotransduction link is falsified.

### Experiment 3: SAXS Profiling of LBX1 under Crowding/Tension
- **Hypothesis**: The computationally predicted "intermediate/blocky" state of LBX1 reflects a biologically relevant conformation that compacts or extends under physiological conditions.
- **Assay Design**: Small-Angle X-ray Scattering (SAXS) on LBX1 in varying concentrations of crowding agents (e.g., PEG) to mimic nuclear environments.
- **Quantitative Readout**: Radius of gyration ($R_g$) and maximum particle dimension ($D_{max}$).
- **Expected Direction**: The $R_g$ and SAXS envelope should match the predicted compact blocky architecture rather than a random coil.
- **Falsification Threshold**: If the SAXS profile indicates a purely disordered random coil (e.g., Kratky plot lacks a clear peak and $R_g$ scales predictably with sequence length for IDPs), the specific structured modular architecture hypothesis is falsified.
