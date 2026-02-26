# Cluster Hypothesis: The Stiff-Axis Conservation

**Date:** 2026-03-12
**Source:** `scripts/structure_hypothesis_generator_v2.py` (K=3)
**Cluster ID:** 2 (High pLDDT, High Anisotropy)

## Cluster Members
- **Drivers (Anisotropy > 3.0):** PIEZO2 (4.44), LMNA (4.75), PLOD1 (3.40), ARNTL (3.32)
- **Core Members:** LBX1 (2.27), NTRK3 (1.94), NF1 (1.93), OTOP1 (1.75)
- **Outliers:** DMD (1.32, likely grouped due to high pLDDT/low disorder)

## Shared Properties
1.  **High Structural Confidence (pLDDT > 70):** Unlike the disordered signaling cluster (Cluster 1), these proteins form stable, well-defined 3D structures.
2.  **Significant Anisotropy (Mean ~2.8):** A subset of members exhibits extreme elongation, suggesting they act as physical "rods" or "stiffeners" rather than globular enzymes.
3.  **Mechanotransduction Focus:** The cluster is enriched for "Mechanotransduction" (4 hits) and "Proprioception" (3 hits).
4.  **Compartmental Spanning:** The top anisotropic members span the primary mechanical axis of the cell:
    -   **ECM:** PLOD1 (Collagen modifier)
    -   **Membrane:** PIEZO2 (Stretch-gated channel)
    -   **Nucleus:** LMNA (Nuclear lamina), ARNTL (Circadian clock)

## Hypothesized Mechanical Role: "Stiff-Axis Transducers"
We hypothesize that these high-anisotropy, high-confidence proteins function as **physical alignment sensors**. Their elongated morphology forces them to align with the principal stress vector of the tissue (e.g., gravity or muscle tension). This physical alignment is necessary for correct directional signaling.

-   **PIEZO2**: Its propeller arms align with membrane tension vectors to maximize sensitivity.
-   **LMNA**: The nuclear lamina stiffens along the stress axis to protect the genome.
-   **PLOD1**: Ensures collagen fibrils are crosslinked anisotropically.
-   **ARNTL**: May have a stiffness-dependent nuclear import or chromatin binding, linking circadian rhythm to mechanical load (The "Clock-Stiffness" link).

**Failure Mode:** Pathogenic variants reduce the anisotropy or structural rigidity of these proteins, causing them to "tumble" or randomize their orientation relative to the stress vector. This leads to **Directional Confusion** in growth signaling, resulting in scoliotic curvature.

## Proposed Concrete Test
**Experiment:** "The alignment Stress Test"
1.  **Model:** Human Dermal Fibroblasts (HDFs) or Osteoblasts.
2.  **Condition:** Subject cells to 1Hz cyclic uniaxial stretch (10% strain) for 24 hours (simulating postural loading).
3.  **Readout:** Immunofluorescence imaging of PIEZO2, LMNA, and ARNTL.
4.  **Metric:** Calculate the "Alignment Index" (Director Order Parameter, $S$) of protein aggregates relative to the stretch axis.
5.  **Prediction:**
    -   **Wildtype:** Proteins align significantly with the stretch axis ($S > 0.5$).
    -   **Scoliosis Variants (e.g., LMNA E145K, PIEZO2 E2727del):** Proteins show randomized orientation ($S \approx 0$), indicating a failure to sense or align with the stress vector.
