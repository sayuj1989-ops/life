# Day 2: AIS Genetics - GWAS Review

## Introduction

Adolescent Idiopathic Scoliosis (AIS) is a highly heritable complex trait (heritability estimated around 38-89%). Genome-Wide Association Studies (GWAS) have identified several robust susceptibility loci. In this document, we map these GWAS hits to the specific biological processes, with a focus on how they might perturb the components of the proprioceptive delay $\tau$.

## Major GWAS Hits

### 1. LBX1 (Ladybird homeobox 1)
- **Genomic Locus**: 10q24.31
- **Key Variant(s)**: rs11190870, rs678741
- **Reported Effects**: Multiple studies across Asian and European populations show strong association (e.g., Cao et al., 2016, DOI: 10.1186/s12891-016-1139-z).
- **Biological Function**: Transcription factor essential for the specification and differentiation of sensory interneurons in the dorsal spinal cord, particularly the dI4-dI6 classes.
- **Mapping to $\tau$**: LBX1 specifically governs the development of the spinal relay circuitry. Variations could subtly alter synaptic connectivity or synaptic strength, potentially increasing **$\tau_{spinal}$**.

### 2. GPR126 (ADGRG6 - Adhesion G protein-coupled receptor G6)
- **Genomic Locus**: 6q24.1
- **Key Variant(s)**: rs6570507, rs7774095
- **Reported Effects**: Replicated across multiple populations (e.g., Qin et al., 2017, DOI: 10.1097/brs.0000000000002123).
- **Biological Function**: Essential for Schwann cell differentiation and peripheral nerve myelination. GPR126 signals through cAMP to drive myelin basic protein (MBP) expression.
- **Mapping to $\tau$**: Perturbations in GPR126 function would directly affect the thickness and quality of the myelin sheath on proprioceptive afferent and efferent fibers, reducing conduction velocity and increasing **$\tau_{afferent}$** and **$\tau_{efferent}$**.

### 3. PAX1 (Paired box 1)
- **Genomic Locus**: 20p11.22
- **Key Variant(s)**: rs6137473
- **Biological Function**: Transcription factor involved in pattern formation and development of the axial skeleton (somitogenesis and sclerotome development).
- **Mapping to Model**: Unlike LBX1 and GPR126, PAX1 likely affects the "plant" in our control-theoretic model—altering vertebral geometry, disc biomechanics, or baseline stiffness—rather than the controller's delay $\tau$. This helps differentiate structural susceptibility from sensorimotor susceptibility.

### 4. BNC2 (Basonuclin 2)
- **Genomic Locus**: 9p22.2
- **Key Variant(s)**: rs10738445
- **Biological Function**: Zinc finger protein implicated in diverse developmental processes, but specific role in AIS is less clear. May relate to muscle or connective tissue.

### 5. CHD7 (Chromodomain helicase DNA binding protein 7)
- **Genomic Locus**: 8q12.2
- **Key Variant(s)**: Evaluated in some populations (e.g., Bilgin et al., 2026, DOI: 10.1177/21925682251356933).
- **Biological Function**: Chromatin remodeling, implicated in neural crest and semicircular canal development (CHARGE syndrome).
- **Mapping to $\tau$**: Could influence inner ear vestibular function, contributing to overall postural control, potentially mapping to cerebellar/vestibular processing, a subset of **$\tau_{cerebellar}$**.

## Conclusion

The strongest GWAS signals for AIS map directly onto components of the proprioceptive reflex arc. LBX1 maps to spinal integration ($\tau_{spinal}$), while GPR126 maps to peripheral nerve conduction ($\tau_{afferent}$ and $\tau_{efferent}$). This provides a compelling molecular basis for the "Derivative Gain Gap" hypothesis, where cumulative minor genetic delays push total $\tau$ past the critical threshold during the rapid adolescent growth spurt.
