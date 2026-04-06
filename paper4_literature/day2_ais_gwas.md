# Phase 1, Day 2: Literature Review — AIS Genetics

## Overview
This document provides a comprehensive review of the primary Genome-Wide Association Study (GWAS) hits associated with Adolescent Idiopathic Scoliosis (AIS). We focus specifically on the genetic loci for GPR126, LBX1, and PAX1, detailing their risk alleles, effect sizes, population frequencies, and proposed biological functions.

## Key GWAS Hits

### 1. GPR126 (ADGRG6)
* **Locus:** Chromosome 6q24.1
* **Risk Allele:** The most significantly associated SNP is rs6570507.
* **Effect Size:** Odds Ratio (OR) $\approx$ 1.27 - 1.28.
* **Population Frequency:** Originally identified in a Japanese cohort and subsequently replicated in Han Chinese and European-ancestry populations (Kou et al., 2013, Nat Genet, DOI: 10.1038/ng.2639).
* **Proposed Biological Function:** GPR126 encodes an adhesion G-protein-coupled receptor that is highly expressed in cartilage. It is critical for Schwann cell myelination of peripheral nerves. Knockdown models in zebrafish demonstrate delayed ossification of the developing spine.
* **Hypothesis for $\tau$ model:** Variants in GPR126 may impair myelination of proprioceptive afferents, leading to thinner myelin sheaths, slower conduction velocities, and an increased afferent conduction delay ($\tau_{afferent}$).

### 2. LBX1
* **Locus:** Chromosome 10q24.31 (often cited around rs11190870 and rs11190878)
* **Risk Allele/Haplotype:**
  * In Asian populations, rs11190870 is a well-known risk variant.
  * In Caucasian populations, rs11190878 is strongly associated. A recessive risk haplotype (TTA) has an OR $\approx$ 1.56, while a co-dominant protective haplotype (CCG) has an OR $\approx$ 0.65.
* **Population Frequency:** Strongest susceptibility locus identified across multiple populations, including Asian and Caucasian cohorts. The TTA risk haplotype frequency in Caucasian controls is approximately 0.52.
* **Proposed Biological Function:** LBX1 (Ladybird homeobox 1) is a transcription factor playing a critical role in the specification of dorsal spinal cord interneurons.
* **Hypothesis for $\tau$ model:** Variants may alter the developmental trajectory of proprioceptive relay circuits within the spinal cord, potentially disrupting or delaying synaptic processing, thereby increasing the spinal relay delay ($\tau_{spinal}$).

### 3. PAX1
* **Locus:** Chromosome 20p11.22
* **Risk Allele:** Associated with a female-specific enhancer locus (e.g., overlapping the PEC7 sequence).
* **Proposed Biological Function:** PAX1 is a transcription factor essential for vertebral column development. Disruption of PAX1 regulatory elements (such as PEC7 and Xe1) in mouse models leads to kinky tail phenotypes, which are female-biased. Furthermore, an estrogen-sensitive Pax1-Col11a1-Mmp3 signaling axis has been implicated in AIS pathogenesis.
* **Hypothesis for $\tau$ model:** Unlike GPR126 or LBX1 which directly impact the neural controller (the $\tau$ components), PAX1 likely affects the mechanical properties of the spine (the "plant" in the PID model). This represents an important distinction: does a variant alter the controller's delay, or the mechanical system it must control?

## Summary
The major AIS GWAS hits map onto distinct aspects of the control-theoretic model. GPR126 and LBX1 directly influence the neural controller by potentially increasing specific components of the proprioceptive delay ($\tau_{afferent}$ and $\tau_{spinal}$, respectively). In contrast, PAX1 variants appear to influence the mechanical structure of the spine itself.

## References
* Kou I et al. (2013). Genetic variants in GPR126 are associated with adolescent idiopathic scoliosis. *Nature Genetics*. [DOI: 10.1038/ng.2639]
* Sharma S et al. (2015). A PAX1 enhancer locus is associated with susceptibility to idiopathic scoliosis in females. *Nature Communications*. [DOI: 10.1038/ncomms7452]
* Takahashi Y et al. (2011). A genome-wide association study identifies common variants near LBX1 associated with adolescent idiopathic scoliosis. *Nature Genetics*. [DOI: 10.1038/ng.974]
