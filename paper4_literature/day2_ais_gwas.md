# Phase 1, Day 2: AIS Genetics — Comprehensive Review of GWAS Hits

Adolescent Idiopathic Scoliosis (AIS) is a complex, polygenic trait. Large-scale Genome-Wide Association Studies (GWAS) have identified several key susceptibility loci that replicate across diverse ancestral populations. For Paper 4, we must map these genetic signals onto our control-theoretic decomposition of proprioceptive delay ($\tau$).

Below is a comprehensive review of the major GWAS hits to date, highlighting their risk alleles, effect sizes, and proposed biological functions.

## 1. GPR126 (ADGRG6) - Adhesion G Protein-Coupled Receptor G6
* **Original GWAS Discovery:** Kou et al., 2013 (*Nat Genet*, PMID: 23666238).
* **Locus:** Chromosome 6q24.1.
* **Top Variant / Risk Allele:** rs6570507.
* **Effect Size:** Odds Ratio (OR) $\approx 1.28$ in Japanese populations; replicated in Han Chinese and European-ancestry populations (OR $\approx 1.27$).
* **Biological Function:** *GPR126* is an adhesion GPCR critical for the differentiation of Schwann cells and the myelination of peripheral nerves. In zebrafish models, *gpr126* knockout causes delayed ossification and spine phenotypes.
* **Mapping to $\tau$:** **Afferent Conduction Delay ($\tau_{aff}$)**.
  * *Hypothesis:* The risk variant alters GPR126 expression or function, subtly impairing peripheral nerve myelination during the pubertal growth spurt. This thinning of the myelin sheath along Group Ia/II proprioceptive afferents decreases conduction velocity, thereby increasing $\tau_{aff}$.

## 2. LBX1 - Ladybird Homeobox 1
* **Original GWAS Discovery:** Takahashi et al., 2011 (*Nat Genet*, PMID: 22019779).
* **Locus:** Chromosome 10q24.31.
* **Top Variant / Risk Allele:** rs11190870.
* **Effect Size:** Odds Ratio (OR) $\approx 1.56$. This is consistently one of the strongest genetic signals for AIS susceptibility and progression across multi-ethnic populations.
* **Biological Function:** *LBX1* is a homeobox transcription factor essential for the dorsal-ventral patterning of the neural tube. It governs the specification and migration of dorsal spinal cord interneurons, particularly those involved in somatosensory and proprioceptive relay circuits (e.g., Clarke's column).
* **Mapping to $\tau$:** **Spinal Relay Delay ($\tau_{spin}$)**.
  * *Hypothesis:* Risk variants near *LBX1* alter the developmental timing or synaptic density of proprioceptive interneuron circuits within the spinal cord. Reduced synaptic efficiency or altered circuit architecture increases the processing time of the ascending proprioceptive signal, increasing $\tau_{spin}$.

## 3. PAX1 - Paired Box 1
* **Original GWAS Discovery:** Sharma et al., 2015 (*Nat Commun*, PMID: 25784220).
* **Locus:** Chromosome 20p11.22 (Enhancer locus distal to *PAX1*).
* **Top Variant / Risk Allele:** rs6137473.
* **Effect Size:** Odds Ratio (OR) $\approx 1.30$. Notably, this locus displays strong sexual dimorphism, conferring risk exclusively in females (consistent with the epidemiological female bias in severe AIS).
* **Biological Function:** *PAX1* is a transcription factor critical for sclerotome development and vertebral column formation. The risk variant resides in an enhancer region (PEC7) active in the spinal cord and intervertebral disc.
* **Mapping to $\tau$ Model:** **Not a controller delay, but a "Plant" modifier**.
  * *Context:* Unlike *GPR126* or *LBX1*, *PAX1* appears to dictate the structural geometry and mechanical properties of the spine itself. In our PID feedback model (Paper 2), *PAX1* governs the parameters of the physical plant (e.g., vertebral stiffness, initial asymmetry), not the proprioceptive controller ($\tau$). It may decrease the mechanical threshold required for the derivative gain gap to manifest as a structural curvature.

## 4. BNC2 - Basonuclin 2
* **Original GWAS Discovery:** Ogura et al., 2015 (*Am J Hum Genet*, PMID: 26211971).
* **Locus:** Chromosome 9p22.2.
* **Top Variant / Risk Allele:** rs10738445 (Functional SNP in an enhancer).
* **Effect Size:** Odds Ratio (OR) $\approx 1.21$.
* **Biological Function:** *BNC2* encodes a zinc finger transcription factor. The risk allele increases *BNC2* expression by enhancing YY1 transcription factor binding. Overexpression in zebrafish leads to body curvature in a gene-dosage-dependent manner.
* **Mapping to $\tau$:** **Pending / Plieotropic**.
  * *Context:* While its exact role in the sensory-motor loop is less established than *GPR126* or *LBX1*, *BNC2* is broadly involved in developmental processes. Its specific contribution to $\tau$ requires further literature mapping, but it may influence generalized tissue mechanics or neural crest cell migration.

## Summary
The major AIS GWAS loci strongly support a "neuro-mechanical" etiology, perfectly aligning with the derivative gain gap model. Specifically, the strongest polygenic risk signals hit distinct components of the proprioceptive feedback loop: *GPR126* (peripheral myelination/conduction, $\tau_{aff}$) and *LBX1* (spinal somatosensory circuit specification, $\tau_{spin}$). Other hits like *PAX1* modulate the mechanical vulnerability of the spinal plant itself.
