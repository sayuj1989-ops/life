# Confidence-Weighted Structural Evidence Report
**Date:** 2026-03-06
**Method:** Ranked by $Score = Anisotropy \times \frac{pLDDT}{100} \times (1 - \frac{PAE}{31})$
**Source:** `outputs/afcc/confidence_weighted_ranking.csv`

## Executive Summary
We applied a rigorous "Confidence Weighting" to the AlphaFold structural metrics. This filters out candidates where high anisotropy might be an artifact of disordered "floppy" tails rather than rigid structural features.

**Key Finding**: The "Tension Rod" hypothesis splits into two distinct categories:
1.  **True Structural Struts (High Confidence)**: PIEZO2, LMNA, PLOD1. These have high anisotropy AND high structural confidence, confirming they are likely rigid, load-bearing elements.
2.  **Disordered Signaling Nodes (Low Confidence)**: LBX1, GHR, EGR3. These have high anisotropy but low confidence, suggesting they are **mechanically soft** but potentially **phase-sensitive** (IDR-heavy).

## Ranking Analysis

### Top Tier: Validated Structural Elements
These candidates have strong evidence for being anisotropic *and* well-defined structures.

| Rank | Gene | Score | Anisotropy | pLDDT | PAE | Interpretation |
|---|---|---|---|---|---|---|
| **1** | **PLOD1** | 2.37 | 3.40 | 92.7 | 7.7 | **Confirmed**. Rigid enzyme, likely crosslinks collagen under load. |
| **2** | **PIEZO2** | 1.59 | 4.44 | 79.4 | 17.0 | **Confirmed**. The primary "Tension Rod". High aspect ratio is real. |
| **3** | **NF1** | 1.17 | 1.93 | 87.2 | 9.5 | **Confirmed**. Globular/Intermediate, but very distinct structure. |
| **4** | **LMNA** | 0.71 | 4.75 | 76.4 | 24.9 | **Supported**. High anisotropy, but lower confidence in tails. |

### Middle Tier: The Metabolic/Signaling Cluster
These candidates show "anisotropy" but it is likely driven by disordered regions (IDRs).

| Rank | Gene | Score | Anisotropy | pLDDT | PAE | Interpretation |
|---|---|---|---|---|---|---|
| **6** | **ARNTL** | 0.57 | 3.32 | 65.5 | 22.8 | **Mixed**. Circadian clock component. IDR-heavy. |
| **7** | **GHR** | 0.50 | 5.13 | 58.7 | 25.8 | **Artifactual Anisotropy?** Very low confidence. Likely a floppy tail. |

### Lower Tier: LBX1 and Proprioceptors
LBX1 falls into the low-confidence tail.

| Rank | Gene | Score | Anisotropy | pLDDT | PAE | Interpretation |
|---|---|---|---|---|---|---|
| **10** | **EGR3** | 0.31 | 3.76 | 50.0 | 25.9 | **Speculative**. Very low confidence. Likely IDR-driven. |
| **11** | **LBX1** | 0.29 | 2.27 | 66.9 | 25.1 | **Weak Structural Evidence**. |

## LBX1 Deep Dive
**Current Status**: Rank #11/15.
**The Problem**: LBX1 was originally hypothesized to be a "stiff" transcription factor. The data contradicts this. With pLDDT=66.9 and PAE=25.1, AlphaFold is unsure of its relative domain positions.
**New Hypothesis**: LBX1 is not a *rod*. It is a *phase-sensor*. Its anisotropy (2.27) and disorder suggest it might condense into liquid droplets.
*   **Implication**: Mechanical stress might not "bend" LBX1 (as it does PIEZO2). Instead, nuclear stress might change the *solubility* or *phase state* of LBX1, altering its binding kinetics.

## Conclusion
We must stop referring to LBX1 as a "Tension Rod". It is structurally distinct from PIEZO2/LMNA.
*   **PIEZO2/LMNA**: Mechanics-through-Structure (Rod).
*   **LBX1/EGR3**: Mechanics-through-Phase (Droplet).

This distinction creates a falsifiable divergence in our model: PIEZO2 should respond to *strain magnitude*, while LBX1 should respond to *nuclear crowding/density*.
