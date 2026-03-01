# Metabolic Proteins in AFCC Pipeline

### Claim
The incorporation of metabolic and signaling proteins (PPARGC1A, IGF1R, GHR, ARNTL, DMD, MYLK) into the AlphaFold Counter-Curvature (AFCC) analysis pipeline reveals unexpected structural features, particularly high regions of low confidence and extended morphologies. These findings link their biological roles in energy supply and mechanotransduction to specific structural architectures.

### Mechanism
Structural analysis indicates that these proteins utilize varying degrees of structural disorder and high hinge density (e.g., GHR with 54 potential hinges) to function effectively. Their low-confidence (pLDDT) regions likely correspond to Intrinsically Disordered Regions (IDRs) that facilitate dynamic interactions or phase separation, essential for their roles as metabolic-mechanical integrators.

### Why it matters
Understanding the specific geometry and flexibility of these proteins provides a mechanistic link between the physical forces acting on the spine (mechanotransduction) and the metabolic cost of maintaining those forces. For example, GHR's highly elongated and hinged structure might allow it to respond to mechanical gating or strain, modulating growth rates during adolescent growth spurts.

### How it constrains or supports the counter-curvature hypothesis
These results support Hypothesis `H_2026_05_25_IDM_Metabolic_Integrator`, which proposes that Intrinsically Disordered Mechanotransducers (IDMs) act as Metabolic-Mechanical Integrators. The structural features identified (disorder and hinges) in proteins like PPARGC1A and ARNTL provide a physical basis for how metabolic capacity can be coupled to mechanical demand, a core tenant of the counter-curvature hypothesis where energy supply dictates spinal stability.

### Open question + proposed test
**Open Question:** Do the identified hinge regions in these metabolic proteins exhibit force-dependent unfolding or gating that directly modulates their signaling activity?
**Proposed Test:** Conduct Steered Molecular Dynamics (SMD) simulations or single-molecule force spectroscopy on the specific hinge domains of GHR and MYLK to quantify their force-extension behavior and determine if physiological strains induce functional conformational changes.
