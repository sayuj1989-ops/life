# Candidate Registry

****Last Updated:** Week 2 Cycle - Gravity Expansion (Added LMNA, PAX1, NKX3-2, etc.)
**Focus:** Gravity, Mechanotransduction, and Spinal Curvature

This registry tracks high-priority gene and protein candidates identified as relevant to the "Biological Counter-Curvature" hypothesis. Candidates are scored based on their relevance to:
1.  **Gravity/Mechanotransduction**: Ability to sense or resist physical forces.
2.  **Spinal Curvature**: Genetic or experimental links to scoliosis or vertebral defects.
3.  **Developmental Role**: Involvement in key spinal formation pathways (Somites, PCP, Cilia).

## Top 30 Priority Candidates

| Rank | Gene Symbol | Score | Mechanism / Rationale | Gravity/Mechano Link |
|:----:|:-----------:|:-----:|:----------------------|:---------------------|
| 1 | **LBX1** | 95 | **Somite**: Major genetic driver of AIS with clear mechanistic link to postural tone. | Regulates migration of muscle precursors and formation of dorsal horn neurons involved in proprioception/gravity sensing. |
| 2 | **PIEZO2** | 95 | **Mechanotransduction**: Direct link between gravity sensing (proprioception) and spinal alignment. | Essential for proprioception, which provides the gravity reference frame for posture control. |
| 3 | **FBN1** | 92 | **ECM**: Major structural determinant of spine elasticity. | Microfibrils provide long-range elasticity and sequester TGF-beta, responding to tissue stretch. |
| 4 | **IFT88** | 92 | **Cilia**: Direct link via PIEZO1-cilia axis. | Linked to PIEZO1-Primary Cilia axis; essential for sensing flow/load. |
| 5 | **LMNA** | 92 | **Mechanotransduction**: Direct link between nuclear mechanotransduction and spinal stability. | Nuclear lamina scales with tissue stiffness; central mechanotransducer (Swift et al., 2013). |
| 6 | **PIEZO1** | 92 | **Mechanotransduction**: Direct mechanistic link to growth plate asymmetry in scoliosis. | Senses mechanical overload; expression upregulates in compressed regions. |
| 7 | **ITGB1** | 90 | **Mechanotransduction**: Primary gravity sensor at cell-ECM interface. | Integrins are the primary cellular gravity/load sensors via focal adhesions. |
| 8 | **POC5** | 90 | **Cilia**: Direct genetic cause of scoliosis linked to ciliary geometry. | Ciliary function is critical for detecting fluid flow and potentially gravity vectors (statocysts analogy). |
| 9 | **YAP1** | 90 | **Mechanotransduction**: Central hub of cellular mechanotransduction. | Nuclear translocation is directly regulated by mechanical stiffness and gravity loading forces. |
| 10 | **ACAN** | 88 | **ECM**: Primary structural resistor of gravity load. | Major load-bearing proteoglycan in IVD/cartilage; resists gravity. |
| 11 | **ADGRG6** | 88 | **Mechanotransduction**: Mechanosensitive receptor directly linked to spine integrity. | GPR126 is a mechanosensitive GPCR; essential for intervertebral disc maintenance under mechanical load. |
| 12 | **FLNB** | 88 | **Cytoskeleton**: Structural integrator of stress and segmentation. | Actin cytoskeleton crosslinker, responds to mechanical stress. |
| 13 | **KIF3A** | 88 | **Cilia**: Essential for ciliary structure and gravity sensing. | Required for ciliary formation and flow sensing (gravity proxy). |
| 14 | **MESP2** | 88 | **Segmentation**: Critical for vertebral segmentation integrity. | Regulates somite boundary formation (the 'clock'), establishing structural units. |
| 15 | **PAX1** | 88 | **Segmentation**: Essential for vertebral structural integrity. | Required for sclerotome differentiation and vertebral body formation (gravity resisting units). |
| 16 | **UTS2R** | 88 | **Cilia**: Strong genetic link involving the CSF flow pathway. | Ciliary function detects fluid flow (gravity proxy). |
| 17 | **WWTR1** | 88 | **Mechanotransduction**: Key partner of YAP in mechanosensing. | Paralog of YAP, acts as a mechanosensor of matrix stiffness and gravity-derived stress. |
| 18 | **CDH2** | 85 | **Adhesion**: Transmits mechanical information between cells. | Cell-cell adhesion, transmits tension across tissues. |
| 19 | **COL2A1** | 85 | **ECM**: Primary gravity-resisting molecule in the spine. | Major structural component resisting compressive gravity loads in spine. |
| 20 | **COL6A1** | 85 | **ECM**: Key for muscle-matrix mechanical coupling. | Interface between muscle and ECM; critical for force transmission. |
| 21 | **DLL3** | 85 | **Segmentation**: Notch ligand essential for somite boundaries. | Notch signaling component for segmentation. |
| 22 | **DVL1** | 85 | **PCP**: PCP mediator linked to segmentation defects. | Mediator of Wnt/PCP signaling; establishes tissue polarity against stress. |
| 23 | **FGFR1** | 85 | **Signaling**: Key growth factor receptor linked to congenital spinal defects. | Regulates osteogenesis and limb development under load. |
| 24 | **FHL1** | 85 | **Mechanotransduction**: Muscle mechanosensor linked to spinal rigidity. | LIM domains act as mechanosensors; mutations cause Reducing Body Myopathy. |
| 25 | **GDF6** | 85 | **Development**: Direct cause of vertebral fusion defects. | BMP family member regulating vertebral segmentation and fusion. |
| 26 | **HES7** | 85 | **Segmentation**: Proven segmentation defect link to spinal malformation. | Establishes structural units (somites) resisting gravity. |
| 27 | **LRP5** | 85 | **Signaling**: Key regulator of bone mechanoadaptation. | Wnt co-receptor regulating bone mass in response to load. |
| 28 | **NKX3-2** | 85 | **Growth_Plate**: Regulates cartilage growth under load. | Inhibits chondrocyte maturation; modulates stress response in cartilage. |
| 29 | **NOTCH1** | 85 | **Segmentation**: Critical for vertebral segmentation timing. | Regulates somitogenesis timing; establishes axial pattern. |
| 30 | **PKD2** | 85 | **Cilia**: Ciliary mechanosensor linked to asymmetry. | Mechanosensitive ion channel in cilia (flow/bending). |

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
