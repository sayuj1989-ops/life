# Phase 1, Day 2: AIS Genetics — GWAS Hits

## Abstract
Adolescent Idiopathic Scoliosis (AIS) is the most common pediatric skeletal disease, with a global pooled prevalence of approximately 1.34% to 3%. Its etiology is multi-factorial, and genetic factors have long been recognized as a primary driver. Over the past decade, large-scale Genome-Wide Association Studies (GWAS) and meta-analyses, particularly in Japanese, Chinese, and Caucasian populations, have successfully mapped several susceptibility loci.

The strongest associations observed to date implicate genes deeply involved in neural development, somatosensory pathways, myelin formation, and axial skeletal development. Here, we systematically review the primary GWAS loci, their risk alleles, odds ratios, and their hypothesized functional consequences.

---

## 1. LBX1 (Ladybird Homeobox 1)

**Locus / SNP:** `rs678741` (and `rs11190870`) on chromosome 10q24.31.
**Risk Allele:** The 'A' allele of `rs678741`.
**Effect Size:** Extremely strong and highly replicated (e.g., OR = 1.35 in a multi-ethnic meta-analysis, $P < 0.0001$).
**Population Frequency:** The risk allele 'A' is highly common, with a frequency of ~57% in Chinese AIS patients vs ~45% in controls, and ~42% globally in Europeans.
\*\*Citation:\*\* Takahashi et al., 2011 (DOI: 10.1038/ng.961); Zhu et al., 2015 (DOI: 10.1038/ncomms9597).
**Biological Function:** LBX1 is a transcription factor strictly required for the specification and differentiation of dorsal spinal cord interneurons, particularly the dI4, dI5, and dI6 classes. These interneurons are pivotal in the formation of somatosensory pathways, coordinating proprioceptive relay from peripheral afferents through the spinal cord.
**Mechanism for $\tau$ Decomposition:** Alterations in LBX1 activity could specifically extend $\tau_{spinal}$ (spinal relay delay) by altering the architecture or functional efficiency of proprioceptive interneuron circuitry during developmental critical periods.

---

## 2. GPR126 (ADGRG6)

**Locus / SNP:** `rs6570507` (also intronic variants like `rs41289839`) on chromosome 6q24.1.
**Risk Allele:** The 'A' allele for `rs6570507` (or 'A' for `rs41289839`).
**Effect Size:** Highly significant. A multi-population GWAS meta-analysis combining Japanese, Chinese, and European cohorts demonstrated $P = 1.27 \times 10^{-14}$ with an OR of 1.27.
**Population Frequency:** The risk allele frequency is approximately ~70% in Japanese and ~65% in Han Chinese AIS cohorts.
\*\*Citation:\*\* Kou et al., 2013 (DOI: 10.1038/ng.2639).
**Biological Function:** GPR126 encodes an Adhesion G-protein-coupled receptor (ADGRG6) that is critical for Schwann cell function. Specifically, it drives the elevation of cyclic AMP (cAMP) necessary to trigger the expression of myelin basic protein (MBP) and the transition to the myelination phase in peripheral nerves. Also expressed in cartilage.
**Mechanism for $\tau$ Decomposition:** As GPR126 is an absolute requirement for proper peripheral myelination, variants impairing its signaling or splicing (e.g., `rs41289839 G>A` which causes decreased inclusion of exon 6) may lead to transient hypomyelination during the adolescent growth spurt when axons undergo rapid stretch. This would directly reduce nerve conduction velocity, significantly elevating $\tau_{afferent}$.

---

## 3. PAX1 (Paired Box 1)

**Locus / SNP:** SNPs near the `PAX1` enhancer locus on chromosome 20p11.22.
**Risk Allele / Effect Size:** $P = 6.89 \times 10^{-9}$ in females; OR = 1.30. Notably, this is a strongly sexually dimorphic locus (no association found in males, $P = 0.71$).
**Population Frequency:** The minor allele frequency varies by population but the risk allele is consistently enriched in female AIS cohorts.
\*\*Citation:\*\* Sharma et al., 2015 (DOI: 10.1038/ncomms7643).
**Biological Function:** PAX1 is a transcription factor heavily involved in somite development, sclerotome differentiation, and vertebral column formation. The AIS-associated SNPs abolish an enhancer sequence active in zebrafish somitic muscle and the spinal cord.
**Mechanism for $\tau$ Decomposition vs. Plant Geometry:** Unlike GPR126 and LBX1, which map cleanly to the PID controller (the $\tau$ delay), PAX1 likely affects the properties of the "plant" (the vertebral column itself). Alterations here may change the mechanical stiffness or geometrical vulnerability of the spine to buckling, exacerbating the instability window caused by the derivative gain gap, rather than directly modulating $\tau$ itself.

---

## Other Notable Loci

* **BNC2:** SNP `rs10738445` or nearby SNPs. Associated with AIS.
* **COL11A1:** Related to cartilage and collagen formation.
* **HSPG2 / FBN1:** Rare variants identified via exome sequencing linked to severe familial forms of idiopathic scoliosis, affecting connective tissue integrity (matrix mechanics).

---

## Summary
The polygenic nature of AIS suggests a multi-hit pathogenesis. The most robust GWAS hits split cleanly into two functional categories:
1. **Controller / Proprioception Elements:** LBX1 (spinal circuit development) and GPR126 (peripheral nerve myelination), both of which will directly increase the components of total proprioceptive delay ($\tau_{spinal}$ and $\tau_{afferent}$).
2. **Plant / Mechanics Elements:** PAX1, COL11A1, FBN1, affecting vertebral geometry, biomechanics, and connective tissue properties.
