# Structure-Derived Hypothesis: The Rigid-Body Integrator
**Date:** 2026-02-21
**Cluster ID:** 0 (from `structure_hypothesis_generator.py`)
**Source Data:** `outputs/afcc/2026-02-20/metrics.csv`

## Cluster Members
- **PIEZO2** (Anisotropy: 4.44, Disorder: 0.14)
- **ACVR1** (Anisotropy: 3.41, Disorder: 0.12)

## Shared Structural Properties
This cluster is uniquely defined by:
1.  **High Anisotropy (> 3.4):** These proteins are structurally extended, functioning as "rods" rather than "spheres".
2.  **Low Disorder (< 0.15):** Unlike other anisotropic proteins (e.g., those with long disordered tails), these are rigid, structured assemblies.
3.  **Mechanotransduction Function:** Both members are critical mechanosensors (Proprioception for PIEZO2, Bone formation for ACVR1).

## Hypothesized Mechanical Role: Rigid-Body Integrators
Developmental symmetry requires the detection of weak, consistent global signals (e.g., gravity vector, tissue-level stress fields) amidst a noisy environment of local thermal fluctuations and transient cellular collisions.

We hypothesize that **Cluster 0 proteins function as 'Rigid-Body Integrators'**. Their high flexural rigidity and extended length allow them to span multiple cytoskeletal or ECM elements, mechanically coupling distant points. This geometry forces the protein to respond only to **coordinated, long-wavelength stress fields** (which can bend or torque the entire rigid assembly) while filtering out short-wavelength, high-frequency noise (which effectively cancels out over a rigid rod).

**Failure Modes:**
- **Loss of Anisotropy (Truncation):** The sensor becomes a local, scalar sensor (pressure only), losing directional sensitivity.
- **Loss of Rigidity (Disorder):** If the rigid stalk is replaced by a flexible linker, the protein becomes an "entropic sensor," responding to local thermal fluctuations. This creates "signaling noise," leading to stochastic developmental errors such as Heterotopic Ossification (FOP, *ACVR1*) or Idiopathic Scoliosis (*PIEZO2*).

## Proposed Test (Falsifiability)
**Experiment:** Noise-Sensitivity Assay in Engineered Variants.

1.  **Constructs:**
    - `WT-ACVR1`: Wild-type (Rigid).
    - `Flex-ACVR1`: Variant where the rigid juxtamembrane/kinase interface is replaced by a flexible Gly-Ser linker of equivalent length.
2.  **System:** Chondrogenic cell line (ATDC5) under static equilibrium (no load).
3.  **Measurement:** Single-cell imaging of SMAD1/5/8 nuclear translocation (FRET or fluctuating intensity) over time.
4.  **Prediction:**
    - `WT-ACVR1` will show a stable baseline signal (low variance).
    - `Flex-ACVR1` will show high-variance "flickering" signaling due to susceptibility to local thermal/cytoskeletal noise, mimicking the "constitutive activity" seen in FOP (where the 'lock' is broken).

## Hypothesis Register Entry
> **H_2026_02_21_RigidIntegration**
> High-anisotropy mechanosensors (Cluster 0: PIEZO2, ACVR1) act as 'Rigid-Body Integrators' that average mechanical noise over large spatial scales; replacing their rigid domains with flexible linkers will increase signaling noise and disrupt developmental symmetry.
