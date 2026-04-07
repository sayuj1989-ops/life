# Phase 1, Day 2: Literature Review — AIS Genetics

## Introduction
Adolescent idiopathic scoliosis (AIS) is a highly heritable polygenic condition. Recent Genome-Wide Association Studies (GWAS) have identified multiple susceptibility loci. This document summarizes the key GWAS hits relevant to proprioceptive delay components and structural development of the spine.

## Key GWAS Hits

### 1. LBX1 (Ladybird homeobox 1)
* **Gene Function**: Transcription factor critical for the specification of dorsal spinal cord interneurons, particularly those involved in somatosensory and proprioceptive relay circuits.
* **Association**: LBX1 is one of the strongest and most consistently replicated GWAS signals for AIS.
* **Risk Variants**: Multiple SNPs near LBX1 have been implicated. For example:
    * rs11190870 (T allele increases susceptibility; OR ~ 1.17-1.22 depending on population; Minor Allele Frequency [MAF] ~ 0.49-0.62 in Asian populations, Takahashi et al., 2011, DOI: 10.1038/ng.974; Gao et al., 2013, DOI: 10.1371/journal.pone.0053234)
    * rs625039 (G allele increases susceptibility; OR ~ 1.14-1.49 depending on population; MAF ~ 0.62-0.71, Gao et al., 2013, DOI: 10.1371/journal.pone.0053234)

* **Proposed Mechanism in $\tau$**: Altered LBX1 expression may affect the development and synaptic organization of proprioceptive relay circuits in the dorsal spinal cord, potentially increasing the spinal relay delay ($\tau_{spin}$).

### 2. GPR126 (Adhesion G protein-coupled receptor G6 / ADGRG6)
* **Gene Function**: Encodes an adhesion GPCR essential for Schwann cell myelination of peripheral nerves and peripheral nerve development. Also plays a role in osteoblast differentiation and spine development.
* **Association**: Consistently associated with AIS across diverse populations (Asian, Caucasian).
* **Risk Variants**: E.g., rs6570507 (A/G, Minor allele frequency [MAF] ~ 0.31 based on 1000 Genomes). Combined meta-analysis yields significant association (OR = 1.22, P = 2.95x10^-20) across populations (Kou et al., 2018, DOI: 10.1038/s41598-018-29011-7).
* **Proposed Mechanism in $\tau$**: GPR126 variants might impair Schwann cell myelination of large-diameter group Ia/II proprioceptive afferents. Thinner or less efficient myelin sheaths would decrease conduction velocity, thereby increasing the afferent conduction delay ($\tau_{aff}$).

### 3. PAX1 (Paired box 1)
* **Gene Function**: Transcription factor involved in embryonic development of the vertebral column (sclerotome differentiation) and thymus.
* **Association**: GWAS and functional studies implicate PAX1 in AIS susceptibility, particularly in females.
* **Risk Variants**: Enhancer locus variants such as rs169311 (A allele) and rs6137473 (G allele). The rs6137473 G allele is associated with AIS specifically in females (OR ~ 1.30-1.67, P = 2.15x10^-10) but not males (Sharma et al., 2015, DOI: 10.1038/ncomms7452).
* **Proposed Mechanism in $\tau$**: PAX1 is more likely to affect vertebral column development and structural mechanics (the "plant" in the PID model) rather than the proprioceptive neural controller ($\tau$). However, structural changes could alter the mechanical demands placed on the proprioceptive system.

### 4. Other Genes (For Context)
* Studies have also linked other genes, such as those related to connective tissue or neuronal development, to AIS. We will focus our $\tau$ modeling efforts primarily on GPR126 (peripheral myelination/conduction) and LBX1 (spinal circuit development).

## Summary
The polygenic architecture of AIS supports the multi-component $\tau$ model. Variants in genes like GPR126 could independently increase $\tau_{aff}$, while LBX1 variants might increase $\tau_{spin}$. The combined effect of these small delays could push the total proprioceptive delay ($\tau$) beyond the critical threshold required for the "derivative gain gap" to manifest during the adolescent growth spurt.
