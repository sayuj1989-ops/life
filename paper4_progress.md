# Paper 4 Progress: The Molecular Basis of τ

## Completed Sessions
* **Phase 1, Day 1 (Literature Review — Decomposing τ)** [2024-05-14]: Completed. Decomposed the total proprioceptive delay ($\tau$) into its constituent components (peripheral transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, and electromechanical delay). Identified initial molecular targets for each component. Incorporated PIEZO2 human mechanosensation literature (Chesler et al., 2016, DOI: 10.1056/NEJMoa1602812) and EMD values (Hopkins et al., 2009, DOI: 10.1002/jor.20934). Explicitly flagged numerical latency estimates requiring specific human paraspinal confirmation. Output generated in `paper4_literature/day1_tau_decomposition.md`.
* **Phase 1, Day 2 (Literature Review — AIS genetics)** [2024-05-15]: Completed. Reviewed GWAS hits for GPR126, LBX1, and PAX1. Detailed risk alleles, effect sizes, population frequencies, and proposed biological functions. Mapped GPR126 to afferent conduction ($\tau_{afferent}$) via myelination impairment, and LBX1 to spinal relay ($\tau_{spinal}$) via interneuron specification. Clarified that PAX1 likely impacts the mechanical plant rather than the neural controller. Output generated in `paper4_literature/day2_ais_gwas.md`.

## Key Findings/Decisions Made
* The total proprioceptive delay can be precisely modeled as a sum of 7 distinct physiological steps.
* Key molecular targets map cleanly onto different components: e.g., Piezo2 handles transduction ($\tau_{trans}$), GPR126 handles afferent conduction ($\tau_{aff}$), LBX1 handles spinal relay ($\tau_{spin}$).
* Most precise latency values in human electrophysiology literature are derived from appendicular (limb) muscles. Exact paraspinal values remain sparse and are flagged as "unverified — needs literature confirmation".
* GPR126 (Chromosome 6q24.1, OR $\approx$ 1.28) and LBX1 (Chromosome 10q24.31, OR $\approx$ 1.56 for TTA haplotype) variants directly map to the controller delay $\tau$.
* PAX1 variants (Chromosome 20p11.22) operate on the mechanical plant of the spine (vertebral development) rather than the proprioceptive delay $\tau$, representing a separate axis of AIS vulnerability.

## Issues / Questions for Dr. Sayuj
* Does Dr. Sayuj prefer to focus strictly on long-loop (transcortical/cerebellar) postural reflexes for the total $\tau$ budget (~100-200ms), or should we also model short-loop (spinal) stretch reflexes (~30-50ms) as a secondary control loop? The current decomposition applies to both, but $\tau_{cereb}$ is the dominant term for postural control.
* Does Dr. Sayuj want to include plant-altering variants (like PAX1) in the final polygenic simulation, or strictly restrict the model to controller delay ($\tau$) variants?

## Next Session
* **Phase 1, Day 3**: Literature Review — GPR126 deep dive. Investigate role in Schwann cell myelination, peripheral nerve development, knockout phenotypes, and conduction velocity data. Search for AlphaFold structure and AIS variant mapping. Output to `paper4_literature/day3_gpr126.md`.
