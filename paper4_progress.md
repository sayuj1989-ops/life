# Paper 4 Progress: The Molecular Basis of τ

## Completed Sessions
* **Phase 1, Day 1 (Literature Review — Decomposing τ)** [2024-05-14]: Completed. Decomposed the total proprioceptive delay ($\tau$) into its constituent components (peripheral transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, and electromechanical delay). Identified initial molecular targets for each component. Incorporated PIEZO2 human mechanosensation literature (Chesler et al., 2016, DOI: 10.1056/NEJMoa1602812) and EMD values (Hopkins et al., 2009, DOI: 10.1002/jor.20934). Explicitly flagged numerical latency estimates requiring specific human paraspinal confirmation. Output generated in `paper4_literature/day1_tau_decomposition.md`.
* **Phase 1, Day 2 (Literature Review — AIS genetics)** [Current Session]: Completed. Conducted a comprehensive review of AIS GWAS hits, focusing on LBX1, GPR126 (ADGRG6), and PAX1. Detailed risk alleles, effect sizes, population frequencies, and proposed biological functions. Linked GPR126 to afferent conduction delay ($\tau_{aff}$) and LBX1 to spinal relay delay ($\tau_{spin}$). Output generated in `paper4_literature/day2_ais_gwas.md`.

## Key Findings/Decisions Made
* **LBX1**: Strongest GWAS signal. Plays a role in dorsal interneuron specification. Proposed to alter spinal relay delay ($\tau_{spin}$).
* **GPR126**: Critical for Schwann cell myelination. Proposed to alter afferent conduction delay ($\tau_{aff}$) due to thinner myelin sheaths.
* **PAX1**: Involved in vertebral column development. Likely affects the mechanical "plant" rather than the neural controller ($\tau$), but important context.
* The combined small delays from variants like GPR126 and LBX1 support the multi-component $\tau$ model, potentially pushing $\tau_{total}$ over the threshold during the growth spurt.

## Issues / Questions for Dr. Sayuj
* Does Dr. Sayuj prefer to focus strictly on long-loop (transcortical/cerebellar) postural reflexes for the total $\tau$ budget (~100-200ms), or should we also model short-loop (spinal) stretch reflexes (~30-50ms) as a secondary control loop? The current decomposition applies to both, but $\tau_{cereb}$ is the dominant term for postural control.

## Next Session
* **Phase 1, Day 3**: GPR126 deep dive — role in Schwann cell myelination, peripheral nerve development, knockout phenotypes, any conduction velocity data. Search for AlphaFold structure and AIS variant mapping. Output to `paper4_literature/day3_gpr126.md`.
