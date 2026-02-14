# Structure Cluster: Blocky Scaffolds (2026-02-16)

**Cluster Definition:** Proteins with High Blockiness (PAE Domain Blockiness Score > 5.0) and Moderate-to-High Anisotropy.
**Metrics Source:** `outputs/afcc/2026-02-13/metrics.csv`

## Cluster Members
Key candidates identified in this cluster:
- **GHR** (Anisotropy: 5.13, Blockiness: 5.31) - *Thermodynamic_Cost*
- **PIEZO1** (Anisotropy: 3.90, Blockiness: 5.74) - *Mechanotransduction*
- **TGFBR1** (Anisotropy: 3.65, Blockiness: 7.83) - *Signaling*
- **EMD** (Anisotropy: 4.29, Blockiness: 9.13) - *Nucleus*
- **FLNA** (Anisotropy: 2.50, Blockiness: 9.88) - *Cytoskeleton*
- **COL1A1** (Anisotropy: 2.80, Blockiness: 6.55) - *ECM*

## Shared Properties
The "Blocky Scaffolds" cluster is characterized by:
1.  **Multi-Domain Architecture:** High PAE blockiness indicates distinct, well-folded globular domains separated by flexible linkers or interfaces. This contrasts with "Tension Rods" (continuous extended structures) or "Globular" proteins (single domain).
2.  **Mechanosensitivity:** The cluster is enriched for known mechanosensors (PIEZO1, FLNA) and receptors (TGFBR, GHR).
3.  **Anisotropy:** Many members (GHR, EMD, PIEZO1) also exhibit high anisotropy, suggesting these multi-domain structures are arranged linearly or in planar arrays rather than spherical aggregates.

## Hypothesized Mechanical Role: "Tension-Gated Signalosomes"
We hypothesize that the "Blocky" architecture represents a **Tension-Gated Switch**.
- In the absence of tension (unloading), the domains may adopt a collapsed or sterically inhibited conformation ("Hyper-Blockiness").
- Mechanical tension (membrane stretch or cytoskeletal pull) aligns the anisotropic axis and separates the domains, exposing cryptic binding sites or enabling dimerization/activation.
- This creates a **Coincidence Detection** mechanism: Signaling = Ligand + Load.

## Specific Hypothesis: The GHR Tension Gate
**Candidate:** Growth Hormone Receptor (GHR)
**Observation:** GHR sits in the "Blocky Scaffold" cluster alongside PIEZO1, with high anisotropy (5.13). While typically viewed as a purely chemical receptor (ligand-gated), its structural similarity to mechanosensors suggests a mechanical component.

**Hypothesis (H_2026_02_16_GHR_Tension_Gate):**
The Growth Hormone Receptor (GHR) acts as a "Tension-Gated" switch due to its high-anisotropy, blocky architecture. In microgravity, loss of membrane tension prevents the active dimer alignment required for full signaling efficiency, uncoupling growth signaling from ligand availability. This explains the "Thermodynamic Cost" failure and growth defects in spaceflight despite normal or elevated GH levels.

**Proposed Test:**
- **System:** GHR-expressing cell line (e.g., Ba/F3-GHR or osteoblasts).
- **Condition:** Vary membrane tension using osmotic shock (hypotonic swelling) or fluid shear stress vs static control.
- **Readout:** Measure pSTAT5 levels in response to a fixed dose of Growth Hormone.
- **Prediction:** pSTAT5 response will be attenuated under low-tension conditions compared to high-tension conditions.
