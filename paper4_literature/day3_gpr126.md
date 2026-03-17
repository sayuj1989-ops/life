# Phase 1, Day 3: GPR126 (ADGRG6) Deep Dive

## Overview
GPR126 (also known as ADGRG6) is an Adhesion G Protein-Coupled Receptor and one of the most robust GWAS hits for Adolescent Idiopathic Scoliosis (AIS). Its established biological role is in the development of the peripheral nervous system (PNS), specifically the differentiation of Schwann cells and the myelination of peripheral nerves. This perfectly aligns with our hypothesis that genetic variants might modulate the afferent conduction delay ($\tau_{afferent}$) component of the total proprioceptive delay.

## Biological Role of GPR126
* **Function:** GPR126 is an essential regulator of Schwann cell development. It drives the elevation of intracellular cAMP levels, which activates the transcription factor EGR2 (Krox20), the master regulator of myelin gene expression (e.g., *MBP*, *MPZ*).
* **Expression:** Highly expressed in Schwann cell precursors and immature Schwann cells during the critical window of peripheral nerve development and myelination.
* **Knockout Phenotype:** As shown by Monk et al. (2009, *Science*, doi:10.1126/science.1173474) in zebrafish and Mogha et al. (2013, *Development*, doi:10.1242/dev.062224) in mice, complete loss of Gpr126 results in a severe congenital hypomyelinating peripheral neuropathy. Schwann cells arrest at the promyelinating stage, failing to wrap axons.
* **Relevant Phenotype for $\tau$:** Even subtle reductions in GPR126 function (hypomorphs or heterozygous states) can lead to thinner myelin sheaths (higher g-ratio). Because conduction velocity is directly proportional to myelin thickness and axon diameter, impaired GPR126 signalling directly translates to slower nerve conduction velocity (NCV).

## Link to Adolescent Idiopathic Scoliosis
* The AIS-associated variants in GPR126 (e.g., rs6570507) are typically intronic or regulatory, suggesting they modulate the *expression level* or splicing of the receptor rather than causing complete loss of function.
* **Hypothesis:** Individuals carrying the risk alleles have slightly reduced GPR126 expression or function. During the rapid adolescent growth spurt, when axons are physically lengthening at peak velocity (stretching the nerve), the demand on Schwann cells to remodel and extend the myelin sheath is at its highest. A subtle deficit in GPR126 signalling may cause myelination to "lag behind" bone growth, resulting in a transient relative hypomyelination of proprioceptive afferents.
* This lag slows conduction velocity, increasing $\tau_{afferent}$ precisely during the window of maximum skeletal growth, pushing total $\tau$ toward the $>200$ ms instability threshold identified in the PID model (Paper 2).

## Structural Considerations (AlphaFold & Variants)
* **Protein Structure:** GPR126 is a massive receptor characterized by a large extracellular domain (ECD) containing multiple adhesion motifs (CUB, PTX, HormR), a G-protein-coupled receptor proteolytic site (GPS) domain, a 7-transmembrane (7TM) domain, and an intracellular tail.
* **Activation Mechanism:** It is mechanically activated. The tethered agonist (Stachel sequence) is exposed upon mechanical shear or binding of the ECD to extracellular matrix (ECM) ligands like laminin or collagen IV.
* **AlphaFold Implications:** While the AIS GWAS SNPs are largely regulatory, any missense variants in the ECD or Stachel sequence would likely impair mechanotransduction or ECM binding, leading to the same downstream effect: reduced cAMP and impaired myelination.
* **Note on AlphaFold Database:** The full human GPR126 structure (UniProt Q86SQ4) can be retrieved from the AlphaFold database to visualize the massive extracellular stalk that acts as a mechanosensor. The pLDDT scores for the 7TM domain and structured ECD modules are generally high (>80), while the long linker regions show lower confidence, typical of flexible extracellular receptors.
* **Variant Mapping:** The primary GWAS risk allele (rs6570507) is intronic, meaning it primarily affects expression levels rather than protein structure directly. However, any missense variants in the high-confidence domains (like the GPS domain) would alter mechanosensitivity.

## Conclusion for the $\tau$ Budget
GPR126 provides the molecular mechanism for variations in **$\tau_{afferent}$**. If a genetic variant increases $\tau_{afferent}$ by even 10-15 ms (via a slight reduction in NCV from, say, 60 m/s to 50 m/s over a 1-meter path), it significantly narrows the safety margin against the derivative gain gap during the adolescent growth spurt.
