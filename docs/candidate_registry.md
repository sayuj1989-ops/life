# Candidate Registry

**Last Updated:** Week 1 Cycle
**Focus:** Gravity, Mechanotransduction, and Spinal Curvature

This registry tracks high-priority gene and protein candidates identified as relevant to the "Biological Counter-Curvature" hypothesis. Candidates are scored based on their relevance to:
1.  **Gravity/Mechanotransduction**: Ability to sense or resist physical forces.
2.  **Spinal Curvature**: Genetic or experimental links to scoliosis or vertebral defects.
3.  **Developmental Role**: Involvement in key spinal formation pathways (Somites, PCP, Cilia).

## Top 30 Priority Candidates

| Rank | Gene Symbol | Score | Mechanism / Rationale | Gravity/Mechano Link |
|:----:|:-----------:|:-----:|:----------------------|:---------------------|
| 1 | **PIEZO2** | 95 | **Proprioception**: Essential for body schema and postural tone. Loss causes scoliosis. | Primary mechanoreceptor for proprioception (gravity sensing). |
| 2 | **LBX1** | 95 | **Muscle Tone**: Top AIS GWAS hit. Regulates dorsal horn interneurons and muscle migration. | Controls sensitivity of proprioceptive loops regulating posture against gravity. |
| 3 | **YAP1** | 90 | **Mechanotransduction**: Hippo pathway effector. Senses matrix stiffness. | Nuclear localization driven by mechanical load/gravity. |
| 4 | **POC5** | 90 | **Cilia**: Centriolar protein. Mutations cause ciliary defects and AIS. | Cilia act as cellular antennae/statocysts for fluid flow (gravity proxy). |
| 5 | **WWTR1 (TAZ)**| 88 | **Osteogenesis**: YAP paralog. Critical for bone formation and stem cell fate. | Mechano-responsive transcriptional co-activator. |
| 6 | **ADGRG6** | 88 | **Disc Health**: Mechanosensitive GPCR (GPR126) in chondrocytes/Schwann cells. | Required for maintenance of intervertebral discs under load. |
| 7 | **VANGL1** | 85 | **PCP**: Planar Cell Polarity gene. Aligns cells in tissue plane. | PCP systems align tissues against stress vectors. |
| 8 | **PTK7** | 85 | **PCP**: Regulator of convergent extension. | Loss leads to spinal curvature in models; resists buckling. |
| 9 | **COL2A1** | 85 | **ECM Integrity**: Main collagen of cartilage/discs. | Provides tensile/compressive strength against gravity. |
| 10 | **TBX6** | 85 | **Segmentation**: Controls somite clock timing. | Hemivertebrae (wedge deformities) cause local curvature. |
| 11 | **TRPV4** | 82 | **Ion Channel**: Osmotic/mechanical sensor in cartilage. | Activated by compressive loading (gravity). |
| 12 | **PKD1L1** | 80 | **Cilia/CSF**: Detects flow in spinal central canal. | CSF flow dynamics are potentially gravity-dependent. |
| 13 | **COMP** | 80 | **ECM Assembly**: Organizes collagen fibrils. | Mutations weaken matrix, leading to deformation under load. |
| 14 | **KIF6** | 78 | **Ciliary Motor**: Transport in cilia. | Linked to AIS; cilia function is key for symmetry. |
| 15 | **MATN1** | 75 | **ECM Network**: Cartilage stiffness. | Genetic link to scoliosis; structural role. |
| 16 | **HSPG2** | 75 | **Perlecan**: Mechanosensor in bone lacunae. | Transduces fluid shear stress in bone (gravity load). |
| 17 | **WNT3A** | 75 | **Bone Mass**: Wnt signaling. | Load-induced bone remodeling pathway. |
| 18 | **GREM1** | 72 | **Growth Plate**: BMP antagonist. | Regulates chondrocyte proliferation timing. |
| 19 | **SCUBE3** | 70 | **Morphogenesis**: Modulates BMP. | Emerging role in skeletal form. |
| 20 | **HOXB1** | 70 | **Patterning**: Axial identity. | Specifies "thoracic" vs "lumbar" properties. |

## Selection Methodology

Candidates were selected based on a "Gravity x Curvature" cross-referencing strategy:
*   **Seed Categories**: Mechanotransduction, Cilia/PCP, Somite Segmentation, Growth Plate.
*   **Expansion Criteria**: Direct literature evidence connecting the gene to both mechanical sensing/response and spinal alignment defects (Scoliosis, Kyphosis, AIS).
*   **Scoring**:
    *   **90-100**: Proven causative gene for Scoliosis with direct mechanotransduction role.
    *   **80-89**: Strong association with Scoliosis and clear mechanobiological function.
    *   **70-79**: Pathway member with experimental links to spine development or gravity response.

## Next Steps

1.  **AlphaFold Analysis**: Run the "Bolt-BioFold" pipeline on the top 10 candidates to assess structural anisotropy and mechanical robustness.
2.  **Simulation**: Incorporate PIEZO2 and LBX1 related parameters (neuromuscular tone) into `pyelastica` models.
3.  **Literature Review**: Deep dive into the "Proprioception as Gravity Sensing" mechanism for LBX1.
