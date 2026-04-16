# AlphaFold Counter-Curvature Analysis Report (Bolt-BioFold ⚡)

## Quality & Reproducibility Checklist
- **Data source:** AlphaFold DB API (fallback to local cache)
- **Date/time of run:** 2026-04-16 20:54:51
- **Code version:** local (untracked)
- **Parameters:** pLDDT ≥ 70 threshold for geometry, default domain heuristics.

## Interpretation

### DCN (P07585)
- **What we see:** Length 359, Anisotropy 2.54, Rg 22.85. Conf: 88.6 mean pLDDT.
- **Why it matters:** Compact structure suggests a regulatory/globular role rather than direct tension/compression resistance. Contributes to mechanical properties of spinal ligaments/cartilage.
- **Confidence level:** High
- **Next test:** Compare orthologs to see if DCN anisotropy is conserved in species with different gravitational loads.

### LUM (P51884)
- **What we see:** Length 338, Anisotropy 2.65, Rg 23.48. Conf: 90.4 mean pLDDT.
- **Why it matters:** Compact structure suggests a regulatory/globular role rather than direct tension/compression resistance. Contributes to mechanical properties of spinal ligaments/cartilage.
- **Confidence level:** High
- **Next test:** Compare orthologs to see if LUM anisotropy is conserved in species with different gravitational loads.

### FMOD (Q06828)
- **What we see:** Length 376, Anisotropy 2.79, Rg 23.56. Conf: 86.4 mean pLDDT.
- **Why it matters:** Compact structure suggests a regulatory/globular role rather than direct tension/compression resistance. Contributes to mechanical properties of spinal ligaments/cartilage.
- **Confidence level:** High
- **Next test:** Compare orthologs to see if FMOD anisotropy is conserved in species with different gravitational loads.

## Best Next Move
- correlate curvature metrics with known phenotype genes
