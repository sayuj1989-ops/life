# Adolescent Idiopathic Scoliosis GWAS: Mapping the Molecular Architecture of Proprioceptive Delay

This document systematically reviews the major loci identified in Genome-Wide Association Studies (GWAS) for Adolescent Idiopathic Scoliosis (AIS). Our goal is to assess these genetic variants not just as statistical markers, but as specific molecular mechanisms perturbing the proprioceptive delay ($\tau$) in the derivative gain gap model.

## 1. Major AIS GWAS Loci

### 1.1 LBX1 (Ladybird Homeobox 1)
- **Chromosomal Locus:** 10q24.31 (e.g., rs11190870)
- **GWAS Discovery:** Takahashi et al., 2011 (Nat Genet. 2011;43:1237-1240. DOI: 10.1038/ng.974)
- **Effect Size / Frequency:** High replication across ethnic groups (Asian, Caucasian).
- **Biological Function:** Transcription factor crucial for the specification of distinct neuronal subtypes in the dorsal spinal cord, particularly the somatosensory and proprioceptive interneurons (class dI4-dI6).
- **Proposed Role in $\tau$:** $\tau_{spinal}$ (Spinal Relay Delay). Aberrant expression or function of LBX1 during neural development could lead to subtle miswiring or altered synaptic connectivity in proprioceptive relay circuits within the spinal cord, increasing processing time or decreasing signal-to-noise ratio in ascending tracts.

### 1.2 GPR126 (ADGRG6)
- **Chromosomal Locus:** 6q24.1 (e.g., rs6570507)
- **GWAS Discovery:** Kou et al., 2013 (Nat Genet. 2013;45:676-679. DOI: 10.1038/ng.2639)
- **Effect Size / Frequency:** Significant associations observed across multiple cohorts. Often associated with curve progression.
- **Biological Function:** GPR126 (Adhesion G protein-coupled receptor G6) is critical for Schwann cell development and myelination of peripheral nerves. GPR126 signalling elevates cAMP levels, driving the myelination program.
- **Proposed Role in $\tau$:** $\tau_{afferent}$ (Afferent Conduction Delay). Variants that decrease GPR126 expression or function may lead to thinner myelin sheaths (lower g-ratio) or delayed myelination during periods of rapid pubertal bone growth, directly slowing conduction velocity in large diameter Group Ia/II afferents.

### 1.3 PAX1 (Paired Box 1)
- **Chromosomal Locus:** 20p11.22 (Enhancer locus)
- **GWAS Discovery:** Sharma et al., 2015 (Nat Commun. 2015;6:6452. DOI: 10.1038/ncomms7452)
- **Effect Size / Frequency:** Female-specific association with susceptibility.
- **Biological Function:** Transcription factor essential for the development of the vertebral column and patterning of the sclerotome.
- **Proposed Role in $\tau$:** *Differentiating Controller vs. Plant*. PAX1 primarily affects the *plant* (vertebral geometry, biomechanical flexibility) rather than the neural *controller* ($\tau$). However, altered vertebral geometry changes the effective stiffness and mass distribution, thereby altering the critical stability boundary which the delayed PID controller must navigate.

### 1.4 BNC2 (Basonuclin-2)
- **Chromosomal Locus:** 9p22.3
- **GWAS Discovery:** Ogura et al., 2015 (Am J Hum Genet. 2015;97:437-446. DOI: 10.1016/j.ajhg.2015.07.016)
- **Biological Function:** Zinc finger protein with widespread expression, proposed roles in bone and cartilage development or potentially neural crest derivatives.

### 1.5 Additional Loci (e.g., CHL1, SCN11A)
- **CHL1 (Cell Adhesion Molecule L1 Like):** Implicated in neuronal migration and axon guidance. Could influence both $\tau_{afferent}$ and central connectivity.
- **Nav Channels (e.g., SCN11A):** While specific AIS GWAS hits in Nav channels are less prominent, common variations in voltage-gated sodium channel kinetics (Nav1.5/Nav1.7) in DRG neurons represent strong biological candidates for modulating intrinsic $\tau_{afferent}$.

## 2. Synthesis: The Polygenic Landscape of $\tau$

AIS is highly polygenic. No single variant explains more than a small fraction of the heritability (~1-2% per locus). The derivative gain gap model naturally accommodates this polygenicity:
* **Genetic Risk Score:** Instead of one catastrophic failure (like Charcot-Marie-Tooth), an AIS patient inherits a collection of common alleles that subtly slow multiple points in the proprioceptive reflex arc.
* **Component Stacking:** A patient might have a $\tau_{afferent}$ slowed by +5ms (GPR126 variant) and a $\tau_{spinal}$ slowed by +8ms (LBX1 variant). The *total* $\tau$ pushes them past the critical >200ms threshold during the pubertal growth spurt.

## 3. Literature Gaps & Next Steps
- We need to quantify the exact reduction in nerve conduction velocity (NCV) associated with GPR126 hypofunction (to be explored in Day 3).
- We need to determine if LBX1 variants functionally alter synapse number or signal latency in spinal interneurons.
- We must distinguish genetic effects on the *biomechanical plant* (PAX1) from effects on the *neuromotor controller* (GPR126, LBX1).
