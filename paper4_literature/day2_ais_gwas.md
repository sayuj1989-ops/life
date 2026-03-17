# Phase 1, Day 2: Comprehensive Review of AIS GWAS Hits

## Overview
Adolescent Idiopathic Scoliosis (AIS) is a complex multifactorial disorder with a strong genetic component. Genome-wide association studies (GWAS) over the past decade have identified several key susceptibility loci. This document summarizes the most prominent hits, focusing on their potential connection to the proprioceptive delay ($\tau$) budget established in Day 1.

## Key GWAS Loci

### 1. GPR126 (ADGRG6)
* **Locus:** Chromosome 6q24.1
* **Key SNPs:** rs6570507, rs7755109
* **Original Discovery:** Kou et al. (2013, *Nature Genetics*, doi:10.1038/ng.2639)
* **Risk Allele & Effect Size:** The risk allele (e.g., rs6570507-A) is associated with an increased odds ratio of approximately 1.22 to 1.28 across multiple populations (East Asian, European, North American).
* **Proposed Biological Function:** GPR126 is an adhesion G-protein-coupled receptor that is essential for the development and myelination of peripheral nerves. It regulates the differentiation of Schwann cells.
* **Link to $\tau$ Budget:** Defects or variations in GPR126 function could lead to hypomyelination or altered myelin structure in peripheral nerves. Because afferent and efferent conduction velocity is highly dependent on myelination, GPR126 variants likely impact **$\tau_{afferent}$** and **$\tau_{efferent}$**.

### 2. LBX1 (Ladybird Homeobox 1)
* **Locus:** Chromosome 10q24.31
* **Key SNPs:** rs11190870, rs678741
* **Original Discovery:** Takahashi et al. (2011, *Nature Genetics*, doi:10.1038/ng.961)
* **Risk Allele & Effect Size:** The risk allele at rs11190870 is one of the strongest and most consistently replicated signals in AIS genetics, with an odds ratio often > 1.3 to 1.5 in Asian populations and strongly replicated in other ancestries.
* **Proposed Biological Function:** LBX1 is a transcription factor critical for the specification of dorsal spinal cord interneurons during embryonic development, specifically those involved in integrating and processing somatosensory and proprioceptive inputs.
* **Link to $\tau$ Budget:** Altered expression of LBX1 could subtly change the wiring, synaptic density, or processing efficiency of spinal sensory relay circuits (such as those in Clarke's column). This directly implicates **$\tau_{spinal}$**.

### 3. PAX1 (Paired Box 1)
* **Locus:** Chromosome 20p11.22
* **Key SNPs:** rs6137473, various enhancer variants
* **Original Discovery:** Sharma et al. (2015, *Nature Communications*, doi:10.1038/ncomms7452)
* **Risk Allele & Effect Size:** Significantly associated with AIS susceptibility, particularly in females.
* **Proposed Biological Function:** PAX1 is a transcription factor essential for the proper formation of the vertebral column and intervertebral discs.
* **Link to $\tau$ Budget:** PAX1 is primarily involved in skeletal development rather than neurophysiology. Therefore, it is likely that PAX1 variants alter the **"plant"** (the mechanical properties of the spine, its stiffness, and susceptibility to buckling) rather than the "controller" (the nervous system). It does not directly map to a $\tau$ component but modulates the threshold at which the $\tau$ gap causes catastrophic failure.

### 4. Other Notable Loci
* **BNC2 (Chromosome 9p22.2):** Often associated with pigmentation, but strongly linked to AIS. Function in AIS remains unclear, potentially related to connective tissue or neural crest derivatives.
* **SOX9 / KCNJ2 (Chromosome 17q24.3):** SOX9 is critical for chondrogenesis. KCNJ2 encodes an inwardly rectifying potassium channel (Kir2.1) involved in maintaining resting membrane potential in excitable tissues. KCNJ2 variants could potentially influence neuronal excitability and thus **$\tau_{transduction}$** or synaptic delays.
* **SCN9A/SCN11A (Chromosome 2q24):** While not top-tier GWAS hits for AIS broadly, variants in voltage-gated sodium channels (Nav1.7, Nav1.9) expressed in DRG neurons can directly modulate sensory nerve conduction velocity (**$\tau_{afferent}$**) and are prime candidate modifiers for polygenic risk.

## Summary
The major AIS GWAS loci map elegantly onto distinct components of our control-theoretic model:
1. **LBX1** $\rightarrow$ Spinal relay processing ($\tau_{spinal}$)
2. **GPR126** $\rightarrow$ Peripheral nerve myelination ($\tau_{afferent}$, $\tau_{efferent}$)
3. **PAX1** $\rightarrow$ Mechanical plant properties (vertebral geometry)

In the subsequent days, we will dive deeper into GPR126 and Piezo2 (the primary mechanotransducer) to understand exactly how common genetic variation might slow conduction and transduction.
