# AlphaFold Counter-Curvature Analysis Report

**Date:** 2026-01-01
**Proteins Analyzed:** 23

## 1. Scientific Framework
This pipeline explores the "Biological Countercurvature of Spacetime" hypothesis by identifying structural proteins that may contribute to axial mechanical robustness.
While gravity is negligible at the molecular scale, we assume that organism-level loads select for specific protein architectures (fibrous, anisotropic, stiff) in load-bearing tissues.

## 2. Methodology
- **Selection:** DISECTRIOE scoring (HOX/PAX seeds).
- **Data Source:** AlphaFold Protein Structure Database (Official API).
- **Metrics:** Anisotropy (Principal Moments of Inertia), Radius of Gyration, pLDDT Confidence.

## 3. Key Findings

### Morphology Landscape
The plot below maps proteins based on their extension (Anisotropy) vs size (Rg).
High anisotropy indicates fibrous/extended potential.

![Morphology Space](figures/morphology_space.png)

### Top Anisotropic Candidates (Fibrous Potential)
| Gene | Anisotropy | Rg (Å) | pLDDT | Morphology |
|------|------------|--------|-------|------------|
| HOXB9 | 2.58 | 39.6 | 63.5 | Intermediate |
| ACTB | 2.16 | 21.6 | 95.2 | Intermediate |
| HOXD13 | 2.07 | 43.3 | 55.4 | Intermediate |
| ALB | 1.82 | 27.1 | 92.7 | Intermediate |
| HOXA1 | 1.82 | 44.3 | 57.8 | Intermediate |

### Confidence Overview
Distribution of model confidence. High pLDDT (>70) suggests well-ordered domains.

![pLDDT Distribution](figures/plddt_dist.png)

## 4. Testable Predictions
Based on these metrics, we predict:
1. **High Anisotropy Candidates:** Proteins like HOXB9, ACTB, HOXD13 likely form extended cytoskeletal or ECM networks essential for resisting compression.
2. **Compact/Globular Candidates:** Proteins with low anisotropy likely function as soluble regulators or globular domains.

## 5. Next Steps
- Validate extended candidates in vivo (staining/KO).
- Expand search using the 'Expansion Modules' in `targets.yaml`.
- Correlate with tissue stiffness data.
