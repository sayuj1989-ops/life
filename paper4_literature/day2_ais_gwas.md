# Phase 1, Day 2: AIS Genetics and GWAS Hits

## Overview
To link molecular variations to the macroscopic control-theoretic instability (the "derivative gain gap") observed in Adolescent Idiopathic Scoliosis (AIS), we must identify the specific genetic variants driving proprioceptive and structural changes. This document reviews the most robust Genome-Wide Association Study (GWAS) hits for AIS, detailing the risk alleles, their proposed biological functions, and their potential effect on the components of proprioceptive delay ($\tau$) and the biological "plant" (the spinal geometry itself).

## 1. LBX1 (Ladybird Homeobox 1)
* **Gene:** LBX1 (Chr 10q24.31)
* **Key SNPs:** rs11190870 (originally identified in Asian populations), rs11190878 (upstream of LBX1, identified in Caucasian populations).
* **Population Frequency & Effect Size:** Highly replicated across multiple ethnicities. The rs11190878 risk haplotype acts recessively (frequency ~0.52 in Caucasians) with an Odds Ratio (OR) of ~1.56. A co-dominant protective haplotype (frequency ~0.28) carries an OR of ~0.65. Overall, the locus explains ~1.4% of phenotypic variance (Takahashi et al., 2011; Londono et al.).
* **Proposed Biological Function:** LBX1 is a transcription factor critical for the specification of dorsal spinal cord interneurons. It is essential for the proper development and patterning of somatosensory circuits, specifically the proprioceptive relay interneurons in the spinal cord.
* **Component of $\tau$ Affected:** **Spinal relay delay ($\tau_{spin}$)**.
* **Hypothesis:** Aberrant LBX1 expression alters the synaptic wiring or developmental maturation of proprioceptive circuits in the spinal cord, introducing inefficiencies or slower processing times in the relay of sensory information.

## 2. GPR126 (ADGRG6 - Adhesion G-Protein-Coupled Receptor G6)
* **Gene:** GPR126 / ADGRG6 (Chr 6q24.1)
* **Key SNPs:** rs6570507 (intronic/regulatory variant).
* **Population Frequency & Effect Size:** Replicated across East Asian, Northern European, and US populations. A large multi-ethnic meta-analysis (6,873 cases / 38,916 controls) confirmed a combined $P$-value of $2.95 \times 10^{-20}$ and an OR of ~1.22 (Kou et al., 2013).
* **Proposed Biological Function:** GPR126 is an adhesion GPCR essential for Schwann cell myelination of peripheral nerves and is also involved in osteoblast differentiation and spinal column development.
* **Component of $\tau$ Affected:** **Afferent conduction delay ($\tau_{aff}$)** (and potentially the "Plant").
* **Hypothesis:** Variants in GPR126 reduce myelination efficiency or myelin thickness in the peripheral nervous system, particularly affecting the large, fast-conducting Group Ia/II proprioceptive afferents. Thinner myelin reduces nerve conduction velocity (NCV), directly increasing $\tau_{aff}$.

## 3. PAX1 (Paired Box 1)
* **Gene:** PAX1 (Chr 20p11.22)
* **Key SNPs:** rs2180439 (identified in an enhancer locus).
* **Population Frequency & Effect Size:** Strongly associated with susceptibility to idiopathic scoliosis, particularly in females (Sharma et al., 2015).
* **Proposed Biological Function:** PAX1 is a transcription factor that plays a crucial role in embryonic pattern formation, specifically in the development of the vertebral column (sclerotome differentiation).
* **Component of $\tau$ Affected:** **The "Plant" (Spinal geometry/mechanics)**.
* **Hypothesis:** Unlike LBX1 and GPR126, which likely affect the *controller* (by increasing delay), PAX1 variants likely alter the structural properties of the vertebral column itself. This may manifest as a pre-existing asymmetry, altered vertebral wedging, or differences in intervertebral disc mechanics, which lowers the threshold for mechanical instability once the derivative gain gap opens. It acts on the physical system being controlled, not the delay $\tau$.

## 4. Other Notable Loci
* **SCN11A / SCN9A (Nav1.5 / Nav1.7):** Voltage-gated sodium channels critical for action potential propagation in dorsal root ganglion (DRG) neurons. While less prominent in primary AIS GWAS than LBX1/GPR126, variants altering channel kinetics (activation/inactivation thresholds) directly impact afferent conduction velocity and thus $\tau_{aff}$.
* **BNC2, BCL2, AJAP1, MEIS1:** Additional loci identified in various GWAS and predictive models. Further deep-dive required to map them specifically to the control-theoretic framework, though they generally fall into categories of neurogenesis, apoptosis, or skeletal development.

## Synthesis and Control-Theoretic Mapping
The AIS GWAS data strongly supports the core thesis of Paper 2 and Paper 4: the etiology of AIS is a combination of neurological and structural factors.
1. **Controller Degradation (Increasing $\tau$):** GPR126 directly affects the transmission hardware (myelin) increasing $\tau_{aff}$. LBX1 affects the processing hardware (spinal interneurons) increasing $\tau_{spin}$.
2. **Plant Vulnerability:** PAX1 alters the physical structure of the spine, changing the baseline mechanics that the controller must stabilize.

When these genetic vulnerabilities coincide with the rapid pubertal growth spurt (rapidly shifting body geometry), the biological system crosses the instability threshold, initiating the scoliotic curve.

## References
* Takahashi, Y. et al. (2011). A genome-wide association study identifies common variants near LBX1 associated with adolescent idiopathic scoliosis. *Nature Genetics*. DOI: 10.1038/ng.974
* Kou, I. et al. (2013). Genetic variants in GPR126 are associated with adolescent idiopathic scoliosis. *Nature Genetics*. DOI: 10.1038/ng.2639
* Sharma, S. et al. (2015). A PAX1 enhancer locus is associated with susceptibility to idiopathic scoliosis in females. *Nature Communications*. DOI: 10.1038/ncomms7452
