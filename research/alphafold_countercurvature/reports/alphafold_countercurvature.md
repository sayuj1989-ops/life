# AlphaFold Counter-Curvature Analysis Report (Bolt-BioFold ⚡)

**Date:** 2026-01-02
**Proteins Analyzed:** 21
**Code Version:** 20260102-AFCC

## 1. Scientific Framework
This pipeline explores the "Biological Countercurvature of Spacetime" hypothesis.
We analyze protein geometry (curvature, torsion, anisotropy) on high-confidence segments to identify load-bearing candidates in spine development.

## 2. Methodology
- **Selection:** User-defined or Default Seed List (Core Spine, ECM, Cytoskeleton, etc.).
- **Data Source:** AlphaFold Protein Structure Database (Official API).
- **Metrics:**
    - **Confidence:** pLDDT gated (≥70). PAE blockiness for domain estimation.
    - **Geometry:** Curvature & Torsion (discrete differential geometry on C-alpha), Anisotropy (Inertia Tensor), Radius of Gyration.
    - **Interaction:** Exposed Surface Proxy (Coordination Number), Charged Patch Score.

## 3. Key Findings

### Morphology Landscape
High anisotropy indicates fibrous/extended potential.

![Morphology Space](figures/morphology_space.png)

### Summary Results Table
Top candidates by Anisotropy:

| Gene | Category | Anisotropy | Rg (Å) | Curvature | pLDDT (Mean) | Exposed Frac |
|------|----------|------------|--------|-----------|--------------|--------------|
| MATN3 | seed_Growth_Plate | 4.98 | 53.9 | 0.308 | 79.3 | 0.47 |
| CDH2 | seed_Adhesion | 4.52 | 67.3 | 0.287 | 79.4 | 0.50 |
| ITGB1 | seed_Adhesion | 2.79 | 46.6 | 0.305 | 85.9 | 0.34 |
| BMP4 | seed_Morphogens | 2.69 | 27.8 | 0.297 | 78.5 | 0.47 |
| KIF3A | seed_Cilia | 2.43 | 37.7 | 0.328 | 75.4 | 0.54 |

### Confidence Overview
Distribution of model confidence. High pLDDT (>70) suggests well-ordered domains.

![pLDDT Distribution](figures/plddt_dist.png)

## 4. Interpretation & Predictions

### What We See
* **Fibrous Candidates:** Proteins like MATN3, CDH2, ITGB1 show high anisotropy (>2.5), consistent with load-bearing filaments or extended linkers.
* **Curvature Profiles:** Mean curvature values indicate the "bendiness" of the rigid segments.

### Why It Matters
For spine development, rigid rods (high anisotropy, low curvature) provide compression resistance (vertebral bodies), while flexible tethers (intermediate anisotropy, variable curvature) may mediate tension (ligaments/annulus).

### Next Test
* **Hypothesis:** MATN3 acts as a mechanical strut.
* **Experiment:** Compare persistence length in vitro vs orthologs with known skeletal defects.

## 5. Best Next Move
**Correlate curvature metrics with known phenotype genes?** (e.g. check if high curvature correlates with scoliosis-associated variants).

## Appendix: Full Metrics
See `data/processed/protein_metrics.csv` for the complete dataset.
