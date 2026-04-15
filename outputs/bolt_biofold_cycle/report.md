# Bolt-BioFold Cycle Report
**Date**: 2026-04-15 19:46:24
**Seed List**: Default seed list (ECM/mechanobiology: MGP, DCN, LUM, FMOD, BMP2)

## Interpretations

### MGP
- **What we see**: Length 103, pLDDT mean 82.8, Anisotropy 6.14.
- **Why it matters**: Highly anisotropic (extended/fibrous). Mechanically plausible as a load-bearing or tension rod element in spinal ECM/countercurvature mechanics.
- **Confidence level**: High based on pLDDT (82.8).
- **Next test**: This protein has an extended architecture; test its role in curvature regulation under mechanical load by comparing orthologs or assessing interactions with known scoliosis genes.
### DCN
- **What we see**: Length 359, pLDDT mean 88.6, Anisotropy 2.54.
- **Why it matters**: Globular/intermediate structure. Likely acts as a signaling hub or cross-linking element in spinal mechanotransduction rather than a primary load-bearer.
- **Confidence level**: High based on pLDDT (88.6).
- **Next test**: Correlate its structural hinges and interaction surfaces with known mutations affecting spine development.
### LUM
- **What we see**: Length 338, pLDDT mean 90.4, Anisotropy 2.65.
- **Why it matters**: Globular/intermediate structure. Likely acts as a signaling hub or cross-linking element in spinal mechanotransduction rather than a primary load-bearer.
- **Confidence level**: High based on pLDDT (90.4).
- **Next test**: Correlate its structural hinges and interaction surfaces with known mutations affecting spine development.
### FMOD
- **What we see**: Length 376, pLDDT mean 86.4, Anisotropy 2.79.
- **Why it matters**: Globular/intermediate structure. Likely acts as a signaling hub or cross-linking element in spinal mechanotransduction rather than a primary load-bearer.
- **Confidence level**: High based on pLDDT (86.4).
- **Next test**: Correlate its structural hinges and interaction surfaces with known mutations affecting spine development.
### BMP2
- **What we see**: Length 396, pLDDT mean 79.6, Anisotropy 2.70.
- **Why it matters**: Globular/intermediate structure. Likely acts as a signaling hub or cross-linking element in spinal mechanotransduction rather than a primary load-bearer.
- **Confidence level**: Medium based on pLDDT (79.6).
- **Next test**: Correlate its structural hinges and interaction surfaces with known mutations affecting spine development.


## Best Next Move
- Prioritize high-confidence structured proteins (e.g., highly anisotropic tension rods) and cluster by geometry to identify novel shared structural motifs among scoliosis candidates.

## Quality & Reproducibility Checklist
- [x] **Data source**: AlphaFold DB (fetched via API, cached locally)
- [x] **Date/time of run**: 2026-04-15 19:46:24
- [x] **Code version**: Current repository state
- [x] **Parameters**: pLDDT threshold for geometry = 70, domain segmentation based on PAE blockiness heuristics
- [x] **Notes**: Computed exclusively on high-confidence backbone segments. Minimal plots generated in `figures/`.
