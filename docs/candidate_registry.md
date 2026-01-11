# Candidate Registry

**Last Updated:** Week 2 Cycle - Gravity Expansion
**Focus:** Gravity, Mechanotransduction, and Spinal Curvature

This registry tracks high-priority gene and protein candidates identified as relevant to the "Biological Counter-Curvature" hypothesis. Candidates are scored based on their relevance to:
1.  **Gravity/Mechanotransduction**: Ability to sense or resist physical forces.
2.  **Spinal Curvature**: Genetic or experimental links to scoliosis or vertebral defects.
3.  **Developmental Role**: Involvement in key spinal formation pathways (Somites, PCP, Cilia).

## Top 30 Priority Candidates

| Rank | Gene Symbol | Score | Mechanism / Rationale | Gravity/Mechano Link |
|:----:|:-----------:|:-----:|:----------------------|:---------------------|
| 1 | **PIEZO2** | 95 | **Mechanotransduction**: Direct link between gravity sensing (proprioception) and spinal alignment. | Essential for proprioception, which provides the gravity reference frame for posture control. |
| 2 | **LBX1** | 95 | **Somite**: Major genetic driver of AIS with clear mechanistic link to postural tone. | Regulates migration of muscle precursors and formation of dorsal horn neurons involved in proprioception/gravity sensing. |
| 3 | **IFT88** | 92 | **Cilia**: Direct link via PIEZO1-cilia axis. | Linked to PIEZO1-Primary Cilia axis; essential for sensing flow/load. |
| 4 | **FBN1** | 92 | **ECM**: Major structural determinant of spine elasticity. | Microfibrils provide long-range elasticity and sequester TGF-beta, responding to tissue stretch. |
| 5 | **PIEZO1** | 92 | **Mechanotransduction**: Direct mechanistic link to growth plate asymmetry in scoliosis. | Senses mechanical overload; expression upregulates in compressed regions. |
| 6 | **YAP1** | 90 | **Mechanotransduction**: Central hub of cellular mechanotransduction. | Nuclear translocation is directly regulated by mechanical stiffness and gravity loading forces. |
| 7 | **POC5** | 90 | **Cilia**: Direct genetic cause of scoliosis linked to ciliary geometry. | Ciliary function is critical for detecting fluid flow and potentially gravity vectors (statocysts analogy). |
| 8 | **ITGB1** | 90 | **Mechanotransduction**: Primary gravity sensor at cell-ECM interface. | Integrins are the primary cellular gravity/load sensors via focal adhesions. |
| 9 | **KIF3A** | 88 | **Cilia**: Essential for ciliary structure and gravity sensing. | Required for ciliary formation and flow sensing (gravity proxy). |
| 10 | **ACAN** | 88 | **ECM**: Primary structural resistor of gravity load. | Major load-bearing proteoglycan in IVD/cartilage; resists gravity. |
| 11 | **WWTR1** | 88 | **Mechanotransduction**: Key partner of YAP in mechanosensing. | Paralog of YAP, acts as a mechanosensor of matrix stiffness and gravity-derived stress. |
| 12 | **ADGRG6** | 88 | **Mechanotransduction**: Mechanosensitive receptor directly linked to spine integrity. | GPR126 is a mechanosensitive GPCR; essential for intervertebral disc maintenance under mechanical load. |
| 13 | **FLNB** | 88 | **Cytoskeleton**: Structural integrator of stress and segmentation. | Actin cytoskeleton crosslinker, responds to mechanical stress. |
| 14 | **MESP2** | 88 | **Segmentation**: Critical for vertebral segmentation integrity. | Regulates somite boundary formation (the 'clock'), establishing structural units. |
| 15 | **UTS2R** | 88 | **Cilia**: Strong genetic link involving the CSF flow pathway. | Ciliary function detects fluid flow (gravity proxy). |
| 16 | **SOX9** | 85 | **Growth_Plate**: Master regulator of gravity-resisting tissue. | Regulates chondrogenesis under load; maintains IVD integrity against gravity. |
| 17 | **VANGL2** | 85 | **PCP**: PCP disruption directly links to vertebral defects. | Core PCP component aligning tissues against stress lines. |
| 18 | **NOTCH1** | 85 | **Segmentation**: Critical for vertebral segmentation timing. | Regulates somitogenesis timing; establishes axial pattern. |
| 19 | **VANGL1** | 85 | **PCP**: PCP pathway is fundamental to body axis linearity. | Planar Cell Polarity (PCP) aligns cells against tissue stress lines (gravity). |
| 20 | **PTK7** | 85 | **PCP**: Core PCP component linked to spinal curvature. | Regulates convergent extension movements, resisting gravity-induced spreading. |
| 21 | **COL2A1** | 85 | **ECM**: Primary gravity-resisting molecule in the spine. | Major structural component resisting compressive gravity loads in spine. |
| 22 | **TBX6** | 85 | **Segmentation**: Fundamental to vertebral segmentation symmetry. | Regulates somite segmentation clock; timing errors lead to hemivertebrae. |
| 23 | **PTK2** | 85 | **Mechanotransduction**: Key signal transducer for gravity sensing. | Central mediator of integrin mechanotransduction and gravity response. |
| 24 | **PKD2** | 85 | **Cilia**: Ciliary mechanosensor linked to asymmetry. | Mechanosensitive ion channel in cilia (flow/bending). |
| 25 | **DLL3** | 85 | **Segmentation**: Notch ligand essential for somite boundaries. | Notch signaling component for segmentation. |
| 26 | **CDH2** | 85 | **Adhesion**: Transmits mechanical information between cells. | Cell-cell adhesion, transmits tension across tissues. |
| 27 | **FGFR1** | 85 | **Signaling**: Key growth factor receptor linked to congenital spinal defects. | Regulates osteogenesis and limb development under load. |
| 28 | **HES7** | 85 | **Segmentation**: Proven segmentation defect link to spinal malformation. | Establishes structural units (somites) resisting gravity. |
| 29 | **PTH1R** | 82 | **Growth_Plate**: Key regulator of bone response to load. | Regulates bone turnover and chondrocyte differentiation under load. |
| 30 | **SCRIB** | 82 | **PCP**: PCP polarity defect links to neural tube/spine. | PCP component; localization affected by mutations. |

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
