# LBX1 Falsifiability Plan

This plan outlines explicit experiments designed to falsify the hypothesis linking LBX1 strictly to structural mechanotransduction in the biological countercurvature model.

## Rationale
Current AlphaFold metrics (outputs/afcc/2026-02-16/metrics.csv) indicate LBX1 possesses low structural confidence (pLDDT ~66.9) and high PAE blockiness (~7.35). High anisotropy alone is insufficient to establish it as a core mechanosensor like PIEZO2. This requires experimental falsification.

## Experiment 1: In Vitro Nuclear Tension Perturbation

- **Hypothesis**: If LBX1's blocky/extended geometry is a functional mechanosensor, altering local nuclear tension will modify its localization or transcriptional activity.
- **Assay Design**: Subject somite/neural crest-derived cells expressing tagged LBX1 to cyclic stretch or modify the LINC complex (e.g., LMNA knockdown) to reduce nuclear mechanical coupling.
- **Quantitative Readout**: Ratio of nucleoplasmic to chromatin-bound LBX1 via fractionation, and target gene expression (e.g., downstream proprioceptive markers).
- **Expected Direction**: Reduced tension leads to delocalization or altered activity if it's purely a structural sensor.
- **Falsification Threshold**: If nuclear tension perturbation yields less than a 10% change in LBX1 localization or target activity compared to static controls, the direct mechanosensor geometry hypothesis is falsified.

## Experiment 2: Truncation/Disorder Domain Deletion

- **Hypothesis**: The high PAE blockiness and low pLDDT regions of LBX1 are intrinsically disordered and mechanically irrelevant to its primary function.
- **Assay Design**: Construct LBX1 mutants lacking the lowest-confidence, high-blockiness domains identified by AlphaFold. Compare binding kinetics and transcriptional rescue in a knockout background against wild-type.
- **Quantitative Readout**: Transcription factor binding affinity (via ChIP-qPCR) and phenotypic rescue in cellular models.
- **Expected Direction**: Deletion of purely structural 'spring' regions should alter mechanically-induced signaling but preserve basal transcription.
- **Falsification Threshold**: If the deletion mutant perfectly rescues wild-type function under all mechanical loading conditions, the extended 'spring' geometry is not required for mechanotransduction.

## Experiment 3: Biophysical Stiffness Measurement (AFM)

- **Hypothesis**: Purified LBX1 protein exhibits anisotropic stiffness consistent with a load-bearing mechanosensor or 'tension rod'.
- **Assay Design**: Perform single-molecule Atomic Force Microscopy (AFM) on purified full-length LBX1 to measure unfolding force and stiffness.
- **Quantitative Readout**: Unfolding force (pN) and contour length extension compared to canonical mechanosensors like Talin or PIEZO2 fragments.
- **Expected Direction**: LBX1 should exhibit a distinct force-extension curve typical of modular 'blocky' springs.
- **Falsification Threshold**: If the unfolding force is identical to globular null-controls or lacks the characteristic stepwise unfolding of a blocky spring, the 'tension rod' structural hypothesis is falsified.
