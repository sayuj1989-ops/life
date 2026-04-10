# Paper 4 Progress: The Molecular Basis of τ

## Completed Sessions
* **Phase 1, Day 1 (Literature Review — Decomposing τ)** [2024-05-14]: Completed. Decomposed the total proprioceptive delay ($\tau$) into its constituent components (peripheral transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, and electromechanical delay). Identified initial molecular targets for each component. Incorporated PIEZO2 human mechanosensation literature (Chesler et al., 2016, DOI: 10.1056/NEJMoa1602812) and EMD values (Hopkins et al., 2009, DOI: 10.1002/jor.20934). Explicitly flagged numerical latency estimates requiring specific human paraspinal confirmation. Output generated in `paper4_literature/day1_tau_decomposition.md`.

## Key Findings/Decisions Made
* The total proprioceptive delay can be precisely modeled as a sum of 7 distinct physiological steps.
* Key molecular targets map cleanly onto different components: e.g., Piezo2 handles transduction ($\tau_{trans}$), GPR126 handles afferent conduction ($\tau_{aff}$), LBX1 handles spinal relay ($\tau_{spin}$).
* Most precise latency values in human electrophysiology literature are derived from appendicular (limb) muscles. Exact paraspinal values remain sparse and are flagged as "unverified — needs literature confirmation".

## Issues / Questions for Dr. Sayuj
* Does Dr. Sayuj prefer to focus strictly on long-loop (transcortical/cerebellar) postural reflexes for the total $\tau$ budget (~100-200ms), or should we also model short-loop (spinal) stretch reflexes (~30-50ms) as a secondary control loop? The current decomposition applies to both, but $\tau_{cereb}$ is the dominant term for postural control.

* **Phase 1, Day 2 (Literature Review — AIS genetics)** [2024-05-15]: Completed. Conducted a comprehensive review of AIS GWAS hits including GPR126, LBX1, and PAX1. Detailed risk alleles, population frequencies (Asian and Caucasian cohorts), and proposed biological functions. Mapped these loci onto the $\tau$ model, distinguishing between "controller defects" (GPR126 affecting $\tau_{aff}$, LBX1 affecting $\tau_{spin}$) and "plant defects" (PAX1 altering vertebral geometry). Output generated in `paper4_literature/day2_ais_gwas.md`.

## Key Findings/Decisions Made (Day 2)
* GPR126 variants (e.g., rs225694, rs7774095) have a strong biological rationale for impairing Schwann cell myelination, thereby increasing afferent conduction delay ($\tau_{aff}$).
* LBX1 variants (e.g., rs11190870) influence dorsal interneuron specification, strongly supporting an increase in spinal relay delay ($\tau_{spin}$).
* PAX1 variants are recognized as altering the mechanical "plant" (vertebral development) rather than the proprioceptive controller.

## Issues / Questions for Dr. Sayuj
* How deeply should we model the PAX1 "plant" alterations in the Python simulations? Should we focus strictly on the $\tau$ increases (controller), or should we also perturb the inertia/length parameters in the PID inverted pendulum model to reflect PAX1-driven geometry changes?

## Next Session
* **Phase 1, Day 3**: GPR126 deep dive — role in Schwann cell myelination, peripheral nerve development, knockout phenotypes, any conduction velocity data. Search for AlphaFold structure and AIS variant mapping. Output to `paper4_literature/day3_gpr126.md`.
