# Paper 4 Progress: The Molecular Basis of τ

## Completed Sessions
* **Phase 1, Day 1 (Literature Review — Decomposing τ)** [2024-05-14]: Completed. Decomposed the total proprioceptive delay ($\tau$) into its constituent components (peripheral transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, and electromechanical delay). Identified initial molecular targets for each component. Incorporated PIEZO2 human mechanosensation literature (Chesler et al., 2016, DOI: 10.1056/NEJMoa1602812) and EMD values (Hopkins et al., 2009, DOI: 10.1002/jor.20934). Explicitly flagged numerical latency estimates requiring specific human paraspinal confirmation. Output generated in `paper4_literature/day1_tau_decomposition.md`.
* **Phase 1, Day 2 (Literature Review — AIS GWAS)** [Current]: Completed. Comprehensive review of GWAS hits (GPR126, LBX1, PAX1, and others). Detailed risk allele, effect size, and proposed biological function for each locus mapping them to specific components of the proprioceptive delay ($\tau$). GPR126 mapped to $\tau_{afferent}$, LBX1 mapped to $\tau_{spinal}$, and PAX1 distinguished as affecting the biomechanical plant rather than the neural controller. Output generated in `paper4_literature/day2_ais_gwas.md`.

## Key Findings/Decisions Made
* AIS is highly polygenic, and the derivative gain gap model accommodates this via a "polygenic stack" where multiple variants (e.g., GPR126, LBX1) add small incremental delays to the total proprioceptive delay ($\tau$).
* GPR126 (ADGRG6) variants are hypothesized to increase afferent conduction delay ($\tau_{afferent}$) via impaired Schwann cell myelination.
* LBX1 variants are hypothesized to increase spinal relay delay ($\tau_{spinal}$) via altered development of somatosensory interneurons.
* PAX1 primarily affects vertebral development (the "plant") rather than the proprioceptive delay (the "controller").

## Issues / Questions for Dr. Sayuj
* We need to determine the specific effect size of GPR126 variants on nerve conduction velocity (NCV) in humans to quantify the $\tau_{afferent}$ delay accurately. If human data is sparse, is it acceptable to extrapolate from animal knockout models (e.g., zebrafish/mouse) for the initial simulation?

## Next Session
* **Phase 1, Day 3**: GPR126 deep dive — role in Schwann cell myelination, peripheral nerve development, knockout phenotypes, any conduction velocity data. Search for AlphaFold structure and AIS variant mapping. Output to `paper4_literature/day3_gpr126.md`.
