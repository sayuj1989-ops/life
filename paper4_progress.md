# Paper 4 Progress: The Molecular Basis of τ

## Completed Sessions
* **Phase 1, Day 1 (Literature Review — Decomposing τ)** [2024-05-14]: Completed. Decomposed the total proprioceptive delay ($\tau$) into its constituent components (peripheral transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, and electromechanical delay). Identified initial molecular targets for each component. Incorporated PIEZO2 human mechanosensation literature (Chesler et al., 2016, DOI: 10.1056/NEJMoa1602812) and EMD values (Hopkins et al., 2009, DOI: 10.1002/jor.20934). Explicitly flagged numerical latency estimates requiring specific human paraspinal confirmation. Output generated in `paper4_literature/day1_tau_decomposition.md`.

## Key Findings/Decisions Made
* The total proprioceptive delay can be precisely modeled as a sum of 7 distinct physiological steps.
* Key molecular targets map cleanly onto different components: e.g., Piezo2 handles transduction ($\tau_{trans}$), GPR126 handles afferent conduction ($\tau_{aff}$), LBX1 handles spinal relay ($\tau_{spin}$).
* Most precise latency values in human electrophysiology literature are derived from appendicular (limb) muscles. Exact paraspinal values remain sparse and are flagged as "unverified — needs literature confirmation".

## Issues / Questions for Dr. Sayuj
* Does Dr. Sayuj prefer to focus strictly on long-loop (transcortical/cerebellar) postural reflexes for the total $\tau$ budget (~100-200ms), or should we also model short-loop (spinal) stretch reflexes (~30-50ms) as a secondary control loop? The current decomposition applies to both, but $\tau_{cereb}$ is the dominant term for postural control.

## Next Session
* **Phase 1, Day 2**: Literature Review — AIS genetics. Comprehensive review of GWAS hits (GPR126, LBX1, PAX1, and others). Detail risk allele, effect size, population frequency, and proposed biological function for each locus. Output to `paper4_literature/day2_ais_gwas.md`.
