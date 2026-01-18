# Structural Cluster Analysis: The "Rod-Block" Dichotomy
**Date:** 2026-06-01
**Author:** Structure Hypothesis Generator (AFCC Pipeline)
**Cycle:** Week 7 - Gravity Expansion

## Overview
Analysis of AlphaFold-derived structural metrics (Anisotropy vs. PAE Domain Blockiness) for the latest candidate batch (N=9, `outputs/afcc/2026-01-14/metrics.csv`) reveals two distinct structural archetypes with divergent mechanical susceptibilities.

## Clusters

### Cluster 0: The "Tension Rods" (Vector Sensors)
*   **Members:** POC5, PIEZO2, IFT88, LMNA
*   **Structural Signature:** High Anisotropy (Mean: 9.17), Low Blockiness (Mean: 2.82).
*   **Properties:** Long, continuous fibrous structures with minimal domain segmentation.
*   **Hypothesized Role:** These proteins act as **"Structural Cantilevers"** or **"Tension Cables"**. Their lack of flexible linkers (low blockiness) means they transmit stress efficiently along their length. However, this geometric extension makes them structurally unstable in the absence of tension (e.g., buckling or slackening in microgravity).

### Cluster 1/2: The "Signaling Blocks" (Scalar Integrators)
*   **Members:** YAP1, LBX1, METTL3, ITGB1, PIEZO1
*   **Structural Signature:** Low Anisotropy (Mean: ~2.4), High Blockiness (Mean: ~7.5).
*   **Properties:** Globular domains connected by flexible linkers.
*   **Hypothesized Role:** These proteins act as **"Logic Gates"** or **"Hubs"**. Their modular "blocky" nature allows them to integrate chemical and metabolic signals (e.g., YAP1 nuclear translocation, METTL3 enzymatic activity) independently of long-range cytoskeletal tension.

## The Hypothesis: "Shape-Driven Signaling Mismatch"
**ID:** `H_2026_06_01_ShapeMismatch`

We hypothesize that **Microgravity acts as a selective filter that disables "Tension Rods" (Cluster 0) while leaving "Signaling Blocks" (Cluster 1/2) intact.**

1.  **Gravity Dependence:** The extreme anisotropy of Cluster 0 proteins (e.g., POC5, Aniso=24.7) implies they require a baseline gravitational/tensile load to maintain their aligned, functional conformation. In microgravity, they lose this "shape integrity" (becoming slack or misaligned).
2.  **Gravity Independence:** Cluster 1/2 proteins function based on local domain-domain interactions (chemical/steric) which are largely gravity-independent.
3.  **The Mismatch:** The cell enters a confused state where "Scalar" signals (Cluster 1/2: "We are healthy/metabolically active") persist, but "Vector" signals (Cluster 0: "We are upright and loaded") vanish. This discordance drives the aberrant remodeling seen in scoliosis (the "Blind Repair" mechanism).

## Proposed Verification
**Test:** Differential Stability Assay in Simulated Microgravity (Clinostat).
*   **Subject:** Human Paraspinal Myoblasts or Chondrocytes.
*   **Method:** Expose cells to 72h simulated microgravity.
*   **Readout:** Western Blot / IF for protein levels and localization.
*   **Prediction:**
    *   **Cluster 0 (POC5, IFT88):** Will show significant **degradation, aggregation, or mislocalization** (loss of tension = instability).
    *   **Cluster 1/2 (YAP1, METTL3):** Will remain **stable** (levels comparable to 1G control), though their signaling *output* (e.g. phosphorylation) may change.
*   **Falsification:** If both classes degrade equally, the hypothesis is false (general proteostatic stress). If neither degrades, the hypothesis is false (structures are robust).

## Implications for Counter-Curvature
If confirmed, this suggests that "Artificial Gravity" (e.g. centrifugation) or "Molecular Splinting" (stabilizing Cluster 0 rods) is the only viable countermeasure. Treating the chemical pathways (Cluster 1/2) without restoring the rod structure will be ineffective.
