# Cluster Analysis Note: 2026-01-22

## Analysis Context
- **Date:** 2026-01-22
- **Source Data:** AFCC Metrics (N=9 high-priority candidates)
- **Method:** K-Means Clustering (k=3) on Anisotropy vs. PAE Blockiness

## Cluster Definitions

### Cluster 0: "Tension Rods"
- **Members:** PIEZO2, LMNA, PIEZO1
- **Metrics:** High Anisotropy (~4.4), Low Blockiness (~3.7).
- **Properties:** Extended, fibrous structures.
- **Role:** Long-range force transmission and vector sensing.

### Cluster 1: "Blocky Scaffolds" (Selected)
- **Members:** CEP290, FLNA, COL1A1, LBX1
- **Metrics:** Moderate Anisotropy (~2.5), High Blockiness (~8.2).
- **Properties:** Proteins containing repetitive, folded domains (e.g., Ig repeats, Coiled-coils) separated by flexible linkers.
- **Hypothesized Role:** **"The Tensegrity Gate"**
  - High blockiness suggests these proteins exist in a compact "folded" state at rest but can undergo significant conformational extension (unfolding) under mechanical load.
  - This "Unfolding" is not just for elasticity but for **Gating**:
    - **FLNA:** Unfolds to expose cryptic integrin binding sites (Cytosolic).
    - **CEP290:** Unfolds to expand the ciliary transition zone pore (Ciliary).
  - **In Microgravity:** The lack of gravitational tension keeps these gates "Locked" (Hyper-Blocky), sequestering signals (FLNA) or blocking transport (CEP290).

### Cluster 2: "Globular Hubs"
- **Members:** IFT88, NF1
- **Metrics:** Low Anisotropy (~2.4), Low Blockiness (~2.4).
- **Properties:** Compact, globular.
- **Role:** Signaling payloads or transport machinery.

## Selected Hypothesis: The Ciliary Tension-Lock (CEP290)

**Observation:** CEP290 clusters with the known "spring" FLNA, suggesting it possesses similar tension-responsive mechanics. CEP290 forms the Y-links of the ciliary transition zone, the "gatekeeper" of the cilium.

**Hypothesis:** CEP290 functions as a **tension-gated sieve**. Under physiological load (gravity/flow tension on the membrane), CEP290's coiled-coil domains extend, increasing the effective pore size of the transition zone to allow entry of large ciliary cargoes (like the PKD1/2 mechanosensory complex). In microgravity/unloading, the gate remains collapsed (closed), leading to "Ciliary Blindness" (absence of sensors) despite the presence of the cilium itself.

**Test:** Compare the ciliary accumulation of PKD2 (Polycystin-2) in cells under:
1. Normal Gravity (1G)
2. Simulated Microgravity (RPM)
3. 1G + Osmotic swelling (artificial membrane tension)
*Prediction:* Microgravity reduces PKD2 ciliary entry; osmotic tension rescues it.
