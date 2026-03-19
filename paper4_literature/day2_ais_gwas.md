# Phase 1, Day 2: AIS Genetics and GWAS Hits Review

## Introduction
Adolescent Idiopathic Scoliosis (AIS) has a strong genetic component, with heritability estimated at 38-89%. Over the last decade, Genome-Wide Association Studies (GWAS) have identified multiple susceptibility loci. This review connects the most robust GWAS hits to the components of proprioceptive delay ($\tau$).

## Key AIS GWAS Susceptibility Loci

### 1. LBX1 (Ladybird Homeobox 1)
* **Locus**: Chromosome 10q24.31 (e.g., rs11190870)
* **Significance**: The most consistently replicated AIS GWAS hit across multiple populations (Asian and Caucasian).
* **Biological Function**: LBX1 is a transcription factor expressed in the developing neural tube. It is essential for the specification and migration of dorsal spinal cord interneurons, particularly those in sensory pathways.
* **Connection to $\tau$ Model**: LBX1 mutations or altered expression could disrupt the formation or efficiency of proprioceptive relay circuits in the dorsal horn (e.g., Clarke's column). This directly impacts $\tau_{spinal}$, potentially slowing down synaptic transmission or integration of Ia afferent signals before they ascend the spinocerebellar tract.

### 2. GPR126 / ADGRG6 (Adhesion G Protein-Coupled Receptor G6)
* **Locus**: Chromosome 6q24.1 (e.g., rs6570507)
* **Significance**: Strongly associated with AIS and height.
* **Biological Function**: GPR126 is crucial for the myelination of peripheral nerves by Schwann cells. It acts via cAMP signaling to drive myelin basic protein expression.
* **Connection to $\tau$ Model**: Impaired GPR126 function could lead to subtly thinner myelin sheaths (reduced g-ratio) or delayed myelination during the rapid adolescent growth spurt. This would directly decrease nerve conduction velocity (NCV) along Ia afferents, significantly increasing $\tau_{afferent}$.

### 3. PAX1 (Paired Box 1)
* **Locus**: Chromosome 20p11.22
* **Significance**: Associated with AIS in female cohorts.
* **Biological Function**: PAX1 is a transcription factor involved in the development of the vertebral column (sclerotome differentiation).
* **Connection to $\tau$ Model**: Unlike LBX1 and GPR126, PAX1 likely affects the "plant" in the PID control model (the structural geometry and stiffness of the spine) rather than the controller delay $\tau$. Changes in vertebral morphology could alter the mechanical demands on the postural control system, making it more vulnerable to instability if $\tau$ is also elevated.

### 4. BNC2 (Basonuclin 2)
* **Locus**: Chromosome 9p22.2
* **Biological Function**: Zinc finger protein involved in multiplication of somatic cells. It has high expression in the uterus and is linked to adolescent development and potentially muscle/bone interactions.
* **Connection to $\tau$ Model**: May influence the timing of the pubertal growth spurt (the velocity term in the derivative gain gap model) rather than $\tau$ itself.

## Summary Mapping to $\tau$ Components
1. **$\tau_{afferent}$**: Governed by myelination genes (GPR126).
2. **$\tau_{spinal}$**: Governed by neural circuit development genes (LBX1).
3. **Plant/Geometry**: Governed by skeletal development genes (PAX1).

## Hypothesis for Paper 4
The polygenic architecture of AIS can be understood through the lens of control theory: risk alleles in genes like GPR126 and LBX1 incrementally add to different sub-components of the total proprioceptive delay $\tau$. When an individual inherits a high burden of these delay-increasing alleles, their $\tau_{total}$ crosses the critical threshold (>200ms) during the rapid skeletal elongation of puberty, triggering the derivative gain gap and subsequent spinal curvature.
