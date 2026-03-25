# Day 8: AlphaFold and Structural Impact Predictions

## Introduction
To understand how AIS-associated genetic variants impact the proteins mediating proprioceptive delay ($\tau$), we analyze their predicted three-dimensional structures using the AlphaFold Protein Structure Database. We then map the positions of known missense mutations and assess their likely functional consequences.

## Protein: GPR126 (ADGRG6)
- **Structure**: AlphaFold prediction (UniProt: Q86SQ4) reveals a massive extracellular domain (ECD) consisting of multiple modules (CUB, PTX, HormR, GAIN) tethered to a 7-transmembrane (7TM) region.
- **Variant Mapping**: Many AIS-associated variants (e.g., those linked to rs6570507, though this specific SNP is often intronic or regulatory) likely affect either the expression level of the receptor or subtly alter the structure of the ECD.
- **Functional Consequence**: The GAIN domain is essential for autoproteolysis and exposing the tethered agonistic "Stachel" sequence. Structural perturbations in the ECD (specifically regions with high predicted Local Distance Difference Test, pLDDT > 70) could alter the mechanical force required to activate the receptor or impair ligand binding (e.g., Laminin-211), leading to reduced cAMP signaling in Schwann cells and impaired myelination (increasing $\tau_{afferent}$).

## Protein: PIEZO2
- **Structure**: The human PIEZO2 structure (UniProt: Q9H5I5) forms a massive, three-bladed propeller trimer. Each subunit contains extensive transmembrane helices forming the blades and a central pore.
- **Variant Mapping**: Rare severe mutations (like those causing profound proprioceptive deficits) often map directly to the central pore or the inner helices controlling gating. Common variants might map to the extended blades.
- **Functional Consequence**: Variants in the mechanosensitive blades or the beam structure connecting the blades to the pore could alter the channel's activation threshold or inactivation kinetics. Even minor changes in the energy barrier for opening the pore would explicitly increase $\tau_{transduction}$ or impair high-frequency encoding ($K_d$).

## Protein: LBX1
- **Structure**: LBX1 (UniProt: P52954) is a transcription factor containing a homeobox DNA-binding domain.
- **Variant Mapping**: The AIS-associated SNP rs11190870 is located downstream of the LBX1 gene, in a putative enhancer region. Therefore, it likely affects the *expression level* or *timing* of LBX1 during spinal cord development rather than altering the protein's structure.
- **Functional Consequence**: Altered dosage of LBX1 during neural tube patterning could lead to subtle mis-specification or wiring deficits in dorsal horn interneurons, increasing synaptic integration time ($\tau_{spinal}$).

## Conclusion
While AlphaFold provides high-confidence models for the core domains of these proteins, the functional impact of AIS variants often seems to involve regulatory changes (expression levels) or subtle kinetic shifts rather than complete structural destabilization. This aligns perfectly with the hypothesis that AIS is caused by a polygenic accumulation of minor functional delays.
