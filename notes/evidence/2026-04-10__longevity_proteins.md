# Evidence Note: Thermodynamic Cost & Longevity Proteins
Date: 2026-04-10

## Overview
This document maps 28 specific molecular targets (23 original + 5 longevity) onto the terms of the free energy dissipation functional:
`Ḟ = ∫ [ η_p |∂κ/∂t|² + η_a(κ−κ_passive)² + Γ_m ] ds`

## Proprioceptive Feedback Cost (η_p)
The cost of **sensing curvature error**. These proteins maintain the proprioceptive circuit that detects deviations from the information-prescribed shape. During the growth spurt, sensing density (sensors per unit length) must scale with L.

| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | Scaling | Role |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| **PIEZO2** | Q9H5I5 | 4.44 | Fibrous/Extended | 43.4 | 79.4 | 709 | 0 | L (sensor density per unit length) | Vector mechanosensor for proprioception; detects alignment error  |
| **EGR3** | Q06889 | 3.76 | Fibrous/Extended | 18.5 | 50.0 | 387 | 2 | L (innervation per segment) | Transcription factor maintaining muscle spindle innervation  |
| **RUNX3** | Q13761 | 2.06 | Intermediate | 15.8 | 60.6 | 415 | 12 | L (proprioceptive neuron count) | Master regulator of proprioceptive neuron development  |
| **NTRK3** | Q16288 | 1.94 | Intermediate | 32.5 | 76.8 | 839 | 9 | L (afferent neuron count) | TrkC receptor; proprioceptive neuron survival signal  |
| **PIEZO1** | Q92508 | 3.90 | Fibrous/Extended | 58.9 | 72.0 | 2521 | 3 | L^2 (membrane area) | Scalar mechanosensor; detects membrane tension (buckling threshold)  |

**Structural summary:** Mean anisotropy = **3.22**, Rg range = 16–59 Å, Mean pLDDT = 67.8, Total residues = 4871, Total hinges = 26

### Thermodynamic Predictions

- **PIEZO2** (L (sensor density per unit length)): High anisotropy (extended) = high metabolic cost to maintain orientation; channel density must scale with L during growth spurt
- **EGR3** (L (innervation per segment)): Extended structure despite being a TF; high disorder = energetically costly to fold; EGR3 expression must scale with L for spindle density
- **RUNX3** (L (proprioceptive neuron count)): Intermediate anisotropy, high disorder (56%); its expression level sets the proprioceptive gain; insufficient scaling during growth = reduced correction
- **NTRK3** (L (afferent neuron count)): Intermediate anisotropy, 9 hinge candidates = conformationally expensive; NT-3/TrkC signaling cost scales with spinal length
- **PIEZO1** (L^2 (membrane area)): Extended (3.9 aniso), massive (2521 res); scalar complement to PIEZO2; sets the stiffness floor below which buckling occurs

## Active Moment Maintenance (η_a)
The cost of **tonic muscle contraction and cytoskeletal tension** required to hold the counter-curvature against gravity. Scales with L³.

| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | Scaling | Role |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| **DMD** | P11532 | 1.32 | Globular | 22.8 | 76.3 | 525 | 1 | L^3 (muscle volume) | Dystrophin; cytoskeleton-ECM linker in paraspinal muscle  |
| **FLNA** | O75369 | 2.50 | Intermediate | 56.9 | 76.5 | 2647 | 116 | L^3 (muscle/fascia volume) | Filamin-A; cross-links actin filaments, mechanotransduction  |
| **MYH3** | P11055 | 1.79 | Intermediate | 50.2 | 74.2 | 1940 | 24 | L^3 (muscle volume) | Embryonic myosin heavy chain; active force generation  |
| **LMNA** | P02545 | 4.75 | Fibrous/Extended | 71.2 | 76.4 | 664 | 0 | L^3 (tissue volume) | Lamin-A/C; nuclear envelope scaffolding, protects against mechanical stress  |
| **VIM** | P08670 | 7.47 | Fibrous/Extended | 65.7 | 77.1 | 466 | 1 | L^3 (cellular volume) | Vimentin; intermediate filament, cellular strain gauge  |
| **CTGF** | P29279 | — | — | — | — | — | — | L^2 (loaded tissue area) | Connective tissue growth factor; matricellular signaling  *(no AFCC data)* |
| **CYR61** | O00622 | — | — | — | — | — | — | L^2 (loaded tissue area) | Matricellular protein; mechanically induced cell adhesion  *(no AFCC data)* |

**Structural summary:** Mean anisotropy = **3.56**, Rg range = 23–71 Å, Mean pLDDT = 76.1, Total residues = 6242, Total hinges = 142

### Thermodynamic Predictions

- **DMD** (L^3 (muscle volume)): Essential for maintenance of muscle tone against gravity; loss leads to collapse; connects contractile force to the load-bearing ECM.
- **FLNA** (L^3 (muscle/fascia volume)): High anisotropy, extended V-shape; acts as a shock absorber; cost scales with the volumetric mechanical demand of upright posture
- **MYH3** (L^3 (muscle volume)): Massive rod-like structure; extreme metabolic cost for synthesis and ATP consumption during continuous active maintenance of posture
- **LMNA** (L^3 (tissue volume)): High anisotropy (4.75); physical scaffold protecting the nucleus from gravity-induced deformation; failure leads to epigenetic changes
- **VIM** (L^3 (cellular volume)): Extended rod; forms a continuous tensegrity network transmitting gravity vector to nucleus; collapses under energy deficit
- **CTGF** (L^2 (loaded tissue area)): Moderate anisotropy; downstream effector of mechanical stress; scales with the area of mechanically loaded tissue
- **CYR61** (L^2 (loaded tissue area)): Compact but highly dynamic; secreted in response to eta_a strain; mediates cross-talk between mechanical load and ECM remodeling

## Basal Tissue Maintenance (Γ_m)
The cost of **matrix turnover, patterning, and metabolic supply**. This is the 'budget' that the other terms draw from.

| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | Scaling | Role |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| **SHH** | Q15465 | 2.12 | Intermediate | 24.5 | 78.4 | 462 | 6 | L (axial patterning) | Sonic hedgehog; morphogen patterning the neural tube and somites  |
| **HOXB7** | P09629 | — | — | — | — | — | — | L (axial patterning) | Homeobox protein; anteroposterior axis specification  *(no AFCC data)* |
| **PAX1** | P15863 | 4.41 | Fibrous/Extended | 24.1 | 54.6 | 534 | 1 | L (vertebral segmentation) | Paired box 1; sclerotome development, spine formation  |
| **COL1A1** | P02452 | 2.80 | Intermediate | 23.5 | 52.7 | 1464 | 16 | L^3 (tissue volume) | Type I collagen; primary load-bearing structural protein  |
| **COL2A1** | P02458 | 2.65 | Intermediate | 25.0 | 52.1 | 1487 | 16 | L^3 (disc volume) | Type II collagen; cartilage and intervertebral disc structure  |
| **LBX1** | P52954 | 2.27 | Intermediate | 22.7 | 66.9 | 281 | 0 | L (neural patterning) | Transcription factor; dorsal spinal cord patterning  |
| **GPR126** | Q86SQ4 | — | — | — | — | — | — | L (nerve length) | Adhesion GPCR; Schwann cell myelination, osteoblast function  *(no AFCC data)* |
| **BNC2** | Q6ZN30 | 1.96 | Intermediate | 30.9 | 53.5 | 1099 | 1 | L^3 (bone volume) | Basonuclin-2; zinc finger protein involved in craniofacial/skeletal development  |
| **MTNR1B** | P49286 | — | — | — | — | — | — | L^3 (systemic distribution) | Melatonin receptor 1B; circadian rhythm, metabolic regulation  *(no AFCC data)* |
| **SOX9** | P48436 | 2.19 | Intermediate | 16.6 | 56.0 | 509 | 2 | L (growth plates) | Master regulator of chondrogenesis; drives longitudinal bone growth  |
| **CDKN1A** | P38936 | 2.14 | Intermediate | 23.9 | 69.0 | 164 | 2 | 1 (systemic stress signal) | p21; cyclin-dependent kinase inhibitor, cell cycle arrest  |
| **SIRT1_Gamma** | Q96EB6 | 1.73 | Intermediate | 22.3 | 65.0 | 747 | 3 | 1 (systemic sensor) | NAD-dependent deacetylase; cellular energy sensor (supply side) **(DUAL-ROLE)** |
| **PPARGC1A_Gamma** | Q9UBK2 | 2.19 | Intermediate | 31.2 | 52.7 | 798 | 0 | L^3 (mitochondrial volume) | PGC-1alpha; master regulator of mitochondrial biogenesis **(DUAL-ROLE)** |

**Structural summary:** Mean anisotropy = **2.44**, Rg range = 17–31 Å, Mean pLDDT = 60.1, Total residues = 7545, Total hinges = 47

### Thermodynamic Predictions

- **SHH** (L (axial patterning)): Compact signaling molecule; establishes the initial coordinates (Information Field) that the mechanical system must follow
- **HOXB7** (L (axial patterning)): Small, highly disordered TF; sets the spatial gain for local growth rates along the spine
- **PAX1** (L (vertebral segmentation)): Disordered TF; defines the boundary conditions for the developing vertebrae; errors create intrinsic curvature (chi_kappa)
- **COL1A1** (L^3 (tissue volume)): Triple helix forming massive fibrils; the physical instantiation of the 'straight' energy functional; scales with body mass
- **COL2A1** (L^3 (disc volume)): Provides the compressive resistance (stiffness E0) in the disc; degrades if mechanical loading is highly asymmetric
- **LBX1** (L (neural patterning)): Disordered TF; implicated directly in AIS; likely regulates the left-right symmetry of proprioceptive neuron scaling
- **GPR126** (L (nerve length)): Large, multi-domain receptor; crucial for the signal conduction velocity in the eta_p proprioceptive loop
- **BNC2** (L^3 (bone volume)): Highly disordered (zinc fingers); maintains epigenetic state of osteoblasts during rapid longitudinal growth
- **MTNR1B** (L^3 (systemic distribution)): Compact 7-TM receptor; couples the mechanical growth rate to the circadian clock; disruption leads to temporal mismatch
- **SOX9** (L (growth plates)): Disordered TF; the 'gas pedal' for length (L); highly active during the adolescent growth spurt, creating the energy deficit
- **CDKN1A** (1 (systemic stress signal)): Small, highly disordered; acts as the emergency 'brake' on growth when energy supply fails; upregulated during deficit
- **SIRT1_Gamma** (1 (systemic sensor)): Compact, well-folded enzyme; detects declining NAD+/NADH ratio during peak growth velocity; acts as the supply-side sensor
- **PPARGC1A_Gamma** (L^3 (mitochondrial volume)): Highly disordered (73%); extremely vulnerable to energy deficit; bottleneck for increasing metabolic supply during growth spurt

## Longevity Effectors
Proteins directly implicated in human longevity that are activated by the cyclical mechanical and thermodynamic perturbations of squat-to-stand transitions.

| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | Scaling | Role |
| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| **FOXO3** | O43524 | 2.44 | Fibrous/Extended | 16.5 | 50.7 | 673 | 1 | 1 (systemic survival state) | Forkhead box O3; master longevity transcription factor  |
| **Klotho** | Q9UEF7 | 2.97 | Fibrous/Extended | 36.9 | 89.1 | 1012 | 1 | 1 (systemic hormone) | Anti-aging hormone; regulates phosphate, calcium, and vitamin D  |
| **YAP1** | P46937 | 1.99 | Intermediate | 23.6 | 57.4 | 504 | 2 | L^2 (loaded tissue area) | Transcriptional coactivator; mechanotransduction effector  |
| **SIRT1_L** | Q96EB6 | 1.73 | Intermediate | 22.3 | 65.0 | 747 | 3 | 1 (systemic survival state) | NAD-dependent deacetylase; extends lifespan via FOXO/PGC1a deacetylation **(DUAL-ROLE)** |
| **PPARGC1A_L** | Q9UBK2 | 2.19 | Intermediate | 31.2 | 52.7 | 798 | 0 | L^3 (mitochondrial volume) | PGC-1alpha; exercise-induced mitochondrial rejuvenation **(DUAL-ROLE)** |

**Structural summary:** Mean anisotropy = **2.26**, Rg range = 17–37 Å, Mean pLDDT = 63.0, Total residues = 3734, Total hinges = 7

### Thermodynamic Predictions

- **FOXO3** (1 (systemic survival state)): Activated by AMPK during energy depletion (squat/stand exertion); drives expression of anti-oxidant and DNA repair genes.
- **Klotho** (1 (systemic hormone)): Release stimulated by transient intracellular Ca2+ spikes from PIEZO1/2 during d(kappa)/dt (squat-to-stand transition).
- **YAP1** (L^2 (loaded tissue area)): Nuclear translocation driven directly by cytoskeletal tension (eta_a) via VIM/LMNA; promotes tissue repair; excluded in sedentary state.
- **SIRT1_L** (1 (systemic survival state)): Activated by cyclical mechanical loading that temporarily depletes ATP -> increases NAD+ -> SIRT1 activates longevity pathways.
- **PPARGC1A_L** (L^3 (mitochondrial volume)): Upregulated by AMPK during squat-to-stand thermodynamic cycling; prevents age-related mitochondrial decline.
