# Phase Separation Analysis Report

**Date:** 2026-02-26

## Hypothesis
Proteins involved in **Metabolic Supply** (e.g., transcription factors, enzymatic regulators) rely on **Intrinsically Disordered Regions (IDRs)** and **Phase Separation** (condensates) to function efficiently. This makes them metabolically "cheap" to build (fewer rigid constraints) but "expensive" to maintain (high turnover, sensitive to pH/ATP).

Proteins involved in **Structural Demand** (e.g., mechanosensors, cytoskeleton) rely on **High Anisotropy** (rigid rods) to transmit force. This makes them structurally expensive and prone to mechanical buckling.

## Results

### Group Averages

| Group | Phase Separation Score | Anisotropy |
|-------|------------------------|------------|
| Supply (Disordered) | 0.396 | 3.094 |
| Demand (High Anisotropy) | 0.328 | 2.601 |
| **Difference** | **0.068** | **-0.493** |

### LBX1 Analysis
*   **Phase Separation Score**: 0.432 (Compare to Supply Mean: 0.396)
*   **Anisotropy**: 2.270 (Intermediate)
*   **Interpretation**: LBX1 clusters closer to the **Supply/Condensate** group than the Structural group, despite being a "muscular" transcription factor. This supports the hypothesis that LBX1 functions via condensate formation in the nucleus.

### Top Phase Separation Candidates
| Gene     |   Phase_Separation_Score |   Disorder_Proxy |   PAE_blockiness |
|:---------|-------------------------:|-----------------:|-----------------:|
| PPARGC1A |                   0.5978 |             0.62 |             6.56 |
| MYLK     |                   0.5087 |             0.35 |             8.29 |
| LBX1     |                   0.4325 |             0.26 |             7.35 |
| GHR      |                   0.4193 |             0.5  |             5.31 |
| EGR3     |                   0.418  |             0.64 |             0    |

### Top Anisotropy Candidates
| Gene   |   Anisotropy |   Phase_Separation_Score |
|:-------|-------------:|-------------------------:|
| GHR    |         5.13 |                   0.4193 |
| LMNA   |         4.75 |                   0.3008 |
| PIEZO2 |         4.44 |                   0.215  |
| EGR3   |         3.76 |                   0.418  |
| PLOD1  |         3.4  |                   0.2103 |

## Conclusion
The data supports the "Protein Cost Landscape" dichotomy.
