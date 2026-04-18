# Phase 1, Day 2: AIS Genetics - Comprehensive Review of GWAS Hits

## Introduction
Adolescent idiopathic scoliosis (AIS) is a highly polygenic condition with an estimated heritability of ~38%. Large-scale genome-wide association studies (GWAS), primarily in East Asian and European-ancestry populations, have identified multiple susceptibility loci. These loci provide the critical molecular starting points for understanding the components of proprioceptive delay ($\tau$).

## Key Loci and Genetic Variants

### 1. LBX1 (Ladybird Homeobox 1)
* **Risk Allele / Locus:** `rs11190870` (and related SNPs in LD: `rs625039`, `rs11598564` at 10q24.31)
* **Effect Size:** Odds Ratio (OR) ~1.56 - 1.58
* **Population Frequency:** Risk allele frequency (RAF) varies, but often high in East Asian populations.
* **Proposed Biological Function:** `LBX1` encodes a transcription factor that is essential for the specification of distinct neuronal subtypes in the dorsal spinal cord, particularly somatosensory and proprioceptive interneurons, as well as hindbrain development and limb muscle migration.
* **Link to $\tau$ Model:** `LBX1` variants likely alter the development or connectivity of proprioceptive relay circuits in the spinal cord, directly increasing spinal relay delay ($\tau_{spin}$).

### 2. GPR126 (ADGRG6 - Adhesion G Protein-Coupled Receptor G6)
* **Risk Allele / Locus:** `rs6570507` (6q24.1)
* **Effect Size:** Odds Ratio (OR) ~1.23 - 1.28
* **Population Frequency:** Very common risk allele (RAF ~46-67% depending on Cobb angle severity in Japanese cohorts).
* **Proposed Biological Function:** `GPR126` is essential for the differentiation of Schwann cells and the myelination of peripheral nerves. In zebrafish, knockdown of *gpr126* delays ossification of the developing spine.
* **Link to $\tau$ Model:** `GPR126` variants likely impair peripheral nerve myelination, resulting in thinner myelin sheaths. This leads to reduced conduction velocity along Ia afferents, directly increasing afferent conduction delay ($\tau_{aff}$).

### 3. PAX1 (Paired Box 1)
* **Risk Allele / Locus:** Enhancer locus variants (e.g., associated with female susceptibility).
* **Effect Size:** Enhancer locus identified in Caucasian/Japanese cohorts.
* **Proposed Biological Function:** `PAX1` is a transcription factor critically involved in the development of the vertebral column (sclerotome differentiation).
* **Link to $\tau$ Model:** Unlike `LBX1` or `GPR126`, `PAX1` primarily acts on vertebral morphology—the "plant" geometry in the PID control model—rather than the neurological controller. Thus, it modifies the biomechanical load rather than the proprioceptive delay ($\tau$) itself.

## Synthesis
The most replicated AIS GWAS signals map beautifully to distinct anatomical components of the neuro-mechanical control loop:
* **The Controller (Delay $\tau$):** `LBX1` (spinal relay circuits, $\tau_{spin}$) and `GPR126` (peripheral myelination, $\tau_{aff}$).
* **The Plant (Biomechanics):** `PAX1` (vertebral column structure).

This supports the hypothesis that the pathogenesis of AIS involves both a vulnerable mechanical column and a lagging sensory-motor controller.

## References
1. Takahashi Y et al. (2011). *A genome-wide association study identifies common variants near LBX1 associated with adolescent idiopathic scoliosis*. Nat Genet. 43(12):1237-40. DOI: 10.1038/ng.974
2. Kou I et al. (2013). *Genetic variants in GPR126 are associated with adolescent idiopathic scoliosis*. Nat Genet. 45(6):676-9. DOI: 10.1038/ng.2639
3. Sharma S et al. (2015). *A PAX1 enhancer locus is associated with susceptibility to idiopathic scoliosis in females*. Nat Commun. 6:6452. DOI: 10.1038/ncomms7452
