# Paper 4 Progress: The Molecular Basis of τ

## Completed Sessions
* **Phase 1, Day 1 (Literature Review — Decomposing τ)** [2024-05-14]: Completed. Decomposed the total proprioceptive delay ($\tau$) into its constituent components (peripheral transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, and electromechanical delay). Identified initial molecular targets for each component. Incorporated PIEZO2 human mechanosensation literature (Chesler et al., 2016, DOI: 10.1056/NEJMoa1602812) and EMD values (Hopkins et al., 2009, DOI: 10.1002/jor.20934). Explicitly flagged numerical latency estimates requiring specific human paraspinal confirmation. Output generated in `paper4_literature/day1_tau_decomposition.md`.
* **Phase 1, Day 2 (Literature Review — AIS genetics)** [2024-05-15]: Completed. Reviewed the top GWAS hits for AIS, including GPR126 (rs6570507, rs41289839), LBX1 (rs678741), and PAX1. Detailed their risk alleles, odds ratios, and biological functions. Mapped GPR126 to $\tau_{afferent}$ (myelination), LBX1 to $\tau_{spinal}$ (spinal relay), and PAX1 to the mechanical "plant" (vertebral geometry). Output generated in `paper4_literature/day2_ais_gwas.md`.

## Key Findings/Decisions Made
* The top AIS GWAS hits map beautifully to our control theory framework. GPR126 (peripheral myelination) directly influences $\tau_{afferent}$. LBX1 (dorsal spinal interneuron specification) directly influences $\tau_{spinal}$.
* PAX1 and connective tissue genes (COL11A1, FBN1) likely affect the mechanical "plant" rather than the neurological controller. This distinction is crucial for Paper 4.
* The GPR126 variant `rs41289839 G>A` is known to alter splicing (decreased inclusion of exon 6), offering a very concrete molecular mechanism for how a common variant could cause a subtle physiological change (mild reduction in myelination efficiency) rather than a severe disease phenotype.

## Issues / Questions for Dr. Sayuj
* For the polygenic risk model later in Phase 3, should we model PAX1 as a modifier of the critical buckling threshold in the PID equation, while GPR126 and LBX1 directly increase $\tau$?

## Next Session
* **Phase 1, Day 3**: GPR126 deep dive — role in Schwann cell myelination, peripheral nerve development, knockout phenotypes, and any available nerve conduction velocity data. Search for AlphaFold structural data and AIS variant mapping. Output to `paper4_literature/day3_gpr126.md`.
