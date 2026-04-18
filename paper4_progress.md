# Paper 4 Progress: The Molecular Basis of τ

## Completed Sessions
* **Phase 1, Day 1 (Literature Review — Decomposing τ)** [2024-05-14]: Completed. Decomposed the total proprioceptive delay ($\tau$) into its constituent components (peripheral transduction, afferent conduction, spinal relay, cerebellar processing, efferent conduction, NMJ, and electromechanical delay). Identified initial molecular targets for each component. Incorporated PIEZO2 human mechanosensation literature (Chesler et al., 2016, DOI: 10.1056/NEJMoa1602812) and EMD values (Hopkins et al., 2009, DOI: 10.1002/jor.20934). Explicitly flagged numerical latency estimates requiring specific human paraspinal confirmation. Output generated in `paper4_literature/day1_tau_decomposition.md`.
* **Phase 1, Day 2 (Literature Review — AIS Genetics)** [Today]: Completed. Conducted a comprehensive review of major AIS GWAS hits (*GPR126*, *LBX1*, *PAX1*, *BNC2*). Extracted risk alleles, effect sizes (Odds Ratios ranging 1.21-1.56), and biological functions. Mapped each locus to the control-theoretic model: *GPR126* to afferent delay ($\tau_{aff}$), *LBX1* to spinal relay delay ($\tau_{spin}$), and *PAX1* as a structural "plant" modifier. Output generated in `paper4_literature/day2_ais_gwas.md`.

## Key Findings/Decisions Made
* **GPR126 (rs6570507, OR 1.28):** Strongly links to Schwann cell myelination, directly supporting the hypothesis that delayed/impaired afferent conduction velocity ($\tau_{aff}$) contributes to AIS.
* **LBX1 (rs11190870, OR 1.56):** The most significant genetic risk factor. As a key specifier of dorsal interneurons, it maps cleanly to the spinal relay processing delay ($\tau_{spin}$).
* **PAX1 (rs6137473, OR 1.30):** Notable for strong female-specific risk. Modulates spinal cord/disc enhancers. Decided to classify *PAX1* not as a controller delay ($\tau$) gene, but as a modifier of the physical spine (the "plant" in the PID model) that increases structural vulnerability to the derivative gain gap.

## Issues / Questions for Dr. Sayuj
* Does Dr. Sayuj agree with the classification of *PAX1* as a "plant" parameter rather than a controller/$\tau$ parameter? This helps maintain the purity of the $\tau$ budget while acknowledging the strongest GWAS hits.

## Next Session
* **Phase 1, Day 3**: GPR126 deep dive — role in Schwann cell myelination, peripheral nerve development, knockout phenotypes, any conduction velocity data. Search for AlphaFold structure and AIS variant mapping. Output to `paper4_literature/day3_gpr126.md`.
