# Cluster Report: 0 - Tension Rods (High Anisotropy)

**Date**: 2026-02-27
**Cluster**: 0 (Tension Rods)
**Source**: `outputs/afcc/current_metrics.csv`

## Members
- **LMNA** (Anisotropy: 4.75) - Nuclear Lamin A/C
- **PIEZO2** (Anisotropy: 4.44) - Mechanosensitive Ion Channel
- **EGR3** (Anisotropy: 3.76) - Transcription Factor (Muscle Spindle)

## Shared Structural Properties
This cluster is defined by **High Anisotropy (> 3.5)** and **Low Blockiness (< 4.0)**.
These proteins are characterized by extended, rod-like, or filamentous structures rather than compact globular domains. They act as "molecular calipers" or "tension cables" capable of integrating mechanical stress over long distances (relative to cell size).

## Hypothesized Mechanical Role: The "Anisotropic Caliper"
Gravity is a weak force at the cellular scale. To sense it, a cell must integrate this weak signal over a large spatial area or through a long lever arm.
We hypothesize that **High Anisotropy is a functional requirement for gravity sensing**.
- **LMNA**: Acts as a "stiffness gauge" for the nucleus, scaling its resistance with tissue stress. Its rod-like structure allows it to buckle or unfold under specific load thresholds, signaling changes in nuclear shape.
- **PIEZO2**: The "Proprioceptive Caliper". Its long lever arms (propeller blades) amplify membrane tension, allowing it to detect minute changes in curvature associated with posture.
- **EGR3**: While a TF, its high anisotropy suggests it may be part of a larger mechanosensitive complex or have a structural role in organizing the muscle spindle's sensing apparatus.

**Hypothesis**: *The Anisotropic Caliper Hypothesis*.
Loss of anisotropy (e.g., truncation, globular variants) in these proteins leads to a "Sensory Gain Failure," where the cell cannot distinguish gravity vectors from thermal noise.

## Proposed Test: The Differential Buckling Assay
**Objective**: To determine if the anisotropic structure is essential for force sensitivity.

**Method**:
1.  **Construct**: Create FRET-based tension sensor variants of PIEZO2 and LMNA:
    -   Wild Type (High Anisotropy)
    -   "Globularized" Mutant (Linker deletions or domain packing to reduce anisotropy to < 2.0).
2.  **System**: Express in HEK293T cells (mechanically neutral background).
3.  **Assay**: Apply controlled shear stress (fluid flow) or substrate strain.
4.  **Readout**: Measure FRET efficiency (tension) vs. Strain.
    -   **Prediction**: Wild Type will show a sharp, non-linear activation threshold (buckling/unfolding). The Globular Mutant will show a linear, blunted response, failing to amplify the signal.

## Implications for Scoliosis
If this hypothesis holds, it suggests that AIS may be a disease of **Molecular Geometry**. Variants that subtly reduce the aspect ratio (anisotropy) of these sensors could raise the threshold for proprioceptive feedback, causing the "silent" accumulation of spinal error until a curve develops.
