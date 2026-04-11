# Confidence-Weighted Structural Evidence

## Methodology
To prevent over-interpretation of intrinsically disordered or highly flexible regions, candidates are stratified by their structural confidence (pLDDT mean). High-anisotropy values computed on low-confidence regions reflect extended random coils rather than rigid mechanical sensors.

## 1. High-Anisotropy, Adequate Confidence (Mechanosensor Candidates)
These proteins exhibit both extended shapes and rigid structural predictions, making them the most defensible candidates for load-bearing or geometric sensing roles.
Threshold: Anisotropy >= 3.0, pLDDT >= 70.0

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|------|------------|-------|----------------|------------|
| CNNM2 | 8.54 | 70.4 | 4.83 | Fibrous/Extended |
| FBLN5 | 7.05 | 83.3 | 3.55 | Fibrous/Extended |
| STOML3 | 5.56 | 84.3 | 0.00 | Fibrous/Extended |
| PANX3 | 5.08 | 81.7 | 2.77 | Fibrous/Extended |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Fibrous/Extended |
| ROCK1 | 3.29 | 76.1 | 4.95 | Fibrous/Extended |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Fibrous/Extended |

## 2. High-Anisotropy, Low Confidence (Exploratory Only)
These proteins have extended predictions but low structural confidence. Their high anisotropy likely reflects disordered states, unfoldase activity, or missing binding partners. Structural inferences here are strictly hypothesis-generating.
Threshold: Anisotropy >= 3.0, pLDDT < 70.0

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|------|------------|-------|----------------|------------|
| POC5 | 24.69 | 64.0 | 3.51 | Fibrous/Extended |
| GHR | 5.13 | 58.7 | 5.31 | Fibrous/Extended |
| EMD | 4.29 | 60.3 | 9.13 | Fibrous/Extended |
| MESP2 | 4.03 | 54.2 | 0.00 | Fibrous/Extended |
| ARNTL | 3.32 | 65.5 | 3.59 | Fibrous/Extended |

## LBX1 Comparator Analysis
LBX1's predicted structure is contextualized against known mechanosensors and other candidates to evaluate its plausibility as a purely geometric driver.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology | Role in Context |
|------|------------|-------|----------------|------------|-----------------|
| POC5 | 24.69 | 64.0 | 3.51 | Fibrous/Extended | Centriolar scaffold; extreme anisotropy, low confidence (disordered). |
| GHR | 5.13 | 58.7 | 5.31 | Fibrous/Extended | Growth receptor; high anisotropy, low confidence. |
| LMNA | 4.75 | 76.4 | 2.56 | Fibrous/Extended | Nuclear tension element; extended, high confidence. |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Fibrous/Extended | Validated mechanosensor; extended, high confidence. |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Fibrous/Extended | Scoliosis-linked receptor; extended, adequate confidence. |
| LBX1 | 2.27 | 66.9 | 7.35 | Intermediate | Target of interest; intermediate shape, low confidence. |
| RUNX3 | 2.06 | 60.6 | 0.00 | Intermediate | Transcription factor; globular/intermediate, low confidence. |

### Conclusion on LBX1
Based on explicit confidence weighting:
- **LBX1 is not an extended mechanosensor**: Its anisotropy (2.27) falls below the threshold for tension rods, and its low pLDDT (66.9) suggests flexibility rather than a rigid structural element.
- **LBX1 vs Known Sensors**: Unlike `PIEZO2` or `LMNA`, which maintain high confidence across their extended geometries, LBX1 resembles flexible transcription factors (`RUNX3`).
- **Path Forward**: LBX1's high PAE blockiness (7.35) remains its most distinctive feature, suggesting a 'beads-on-a-string' multi-domain architecture. Its role in scoliosis is more likely related to complex assembly or tension-modulated binding rather than intrinsic cytoskeletal strut function.
