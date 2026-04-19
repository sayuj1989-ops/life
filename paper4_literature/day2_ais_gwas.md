# Phase 1, Day 2: AIS Genetics and GWAS Hits

## Overview
This document reviews the major Genome-Wide Association Study (GWAS) hits for Adolescent Idiopathic Scoliosis (AIS). The focus is on linking these genetic susceptibility loci to components of the proprioceptive delay ($\tau$) model or the mechanical plant, in preparation for the multi-component $\tau$ model.

## 1. GPR126 (ADGRG6)
* **Locus/Variant**: rs6570507, rs7755109, rs7774095
* **Population**: Validated in Chinese Han, Japanese, Caucasian, and multi-ethnic cohorts.
* **Risk Allele & Effect Size**: A multi-ethnic meta-analysis of rs6570507 (6,873 cases, 38,916 controls) yielded an Odds Ratio (OR) of 1.22 (P = 2.95 × 10^-20) (Kou et al., 2018, DOI: 10.1038/s41598-018-29011-7).
* **Biological Function**: GPR126 is an adhesion G-protein-coupled receptor that plays a critical role in the myelination of peripheral nerves by Schwann cells. Animal models (e.g., *Danio rerio* knockout) show delayed ossification and structural anomalies.
* **Hypothesized Role in $\tau$ Model**: Perturbations in GPR126 likely impair peripheral myelination efficiency, leading to thinner myelin sheaths. This would directly increase the afferent conduction delay ($\tau_{aff}$).

## 2. LBX1
* **Locus/Variant**: rs11190870, rs625039, rs11598564; functional variant rs678741 (antisense transcript LBX1AS1).
* **Population**: Widely replicated across Asian (Japanese, Chinese Han, Acehnese) and Caucasian populations.
* **Risk Allele & Effect Size**: Represents the strongest AIS GWAS signal. For rs11190870, Han Chinese populations show an OR of 1.70 (95% CI: 1.42–2.04, P = 3.26 × 10^-8) (Gao et al., 2013, DOI: 10.1371/journal.pone.0053234).
* **Biological Function**: LBX1 (ladybird homeobox 1) is a transcription factor essential for specifying distinct neuronal subtypes in the dorsal spinal cord and hindbrain. It is critically involved in the development of proprioceptive interneurons and somatosensory relay circuits.
* **Hypothesized Role in $\tau$ Model**: Variants may alter the developmental timing or wiring of spinal relay circuits, directly increasing the spinal relay delay ($\tau_{spin}$).

## 3. PAX1
* **Locus/Variant**: rs6137473, rs169311, and variants mapping to a female-specific enhancer locus.
* **Population**: Replicated in multiple cohorts (Chinese, Japanese, Caucasian); strong sexual dimorphism.
* **Risk Allele & Effect Size**: Allele G of rs6137473 and allele A of rs169311 add to the risk of AIS with an OR of 1.17 and 1.22 respectively in the Chinese population (Xu et al., 2018, DOI: 10.1097/BRS.0000000000002475).
* **Biological Function**: PAX1 is a transcription factor essential for vertebral column and sclerotome development. Knockout models (*Pax1-/-*) show distinct spinal deformities and kinked tails, suggesting a profound impact on bone and intervertebral disc formation (e.g., collagen $\alpha$1(XI) expression).
* **Hypothesized Role in $\tau$ Model**: Unlike LBX1 and GPR126, PAX1 likely alters the mechanical properties of the spine itself rather than the neural controller. In the PID model framework, PAX1 variants would modify the "plant" (geometry, stiffness) rather than increasing $\tau$.

## Summary and Next Steps
These major GWAS hits support a dual-etiology model for AIS:
1. **Controller defects (Delay $\tau$)**: LBX1 (spinal processing) and GPR126 (afferent conduction).
2. **Plant defects (Mechanical)**: PAX1 (vertebral geometry).

The next step is a deep dive into GPR126, focusing on its structural role in Schwann cell myelination, potential AlphaFold predictions for risk variants, and quantitative impacts on nerve conduction velocity.
