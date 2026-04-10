# Bolt-BioFold Analysis Report

## Interpretation
### Q9UBK2
**What we see:** Mean pLDDT = 52.7, 7 predicted domains. Disordered fraction: 0.62. Anisotropy: 1.90 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Low
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### O00327
**What we see:** Mean pLDDT = 65.5, 7 predicted domains. Disordered fraction: 0.40. Anisotropy: 5.12 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Low
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### Q9H5I5
**What we see:** Mean pLDDT = 79.4, 8 predicted domains. Disordered fraction: 0.14. Anisotropy: 4.43 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Medium
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### Q14118
**What we see:** Mean pLDDT = 68.2, 7 predicted domains. Disordered fraction: 0.38. Anisotropy: 2.90 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Low
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### P52954
**What we see:** Mean pLDDT = 66.9, 7 predicted domains. Disordered fraction: 0.26. Anisotropy: 2.71 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Low
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### P10912
**What we see:** Mean pLDDT = 58.7, 6 predicted domains. Disordered fraction: 0.50. Anisotropy: 12.04 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Low
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### Q16288
**What we see:** Mean pLDDT = 76.8, 14 predicted domains. Disordered fraction: 0.20. Anisotropy: 1.53 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Medium
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### Q15746
**What we see:** Mean pLDDT = 65.8, 31 predicted domains. Disordered fraction: 0.35. Anisotropy: 1.57 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Low
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### P08069
**What we see:** Mean pLDDT = 78.0, 18 predicted domains. Disordered fraction: 0.16. Anisotropy: 1.41 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Medium
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

### P11532
**What we see:** Mean pLDDT = 76.3, 8 predicted domains. Disordered fraction: 0.18. Anisotropy: 1.32 if computed.
**Why it matters:** Structural properties define mechanical capabilities within the ECM/cytoskeleton linking to countercurvature.
**Confidence level:** Medium
**Next test:** Check orthologs or associated scoliosis mutants in domain boundaries.

## Best Next Move
Cluster proteins by geometry and correlate curvature metrics with known phenotype genes to prioritize high-confidence structured candidates.

## Quality & Reproducibility Checklist
- Data source: Local AlphaFold DB cache (`data/afdb_cache/`)
- Date/time: Runtime execution
- Parameters: pLDDT >= 70 for geometry, smoothing window=5
- Notes: SASA and charged patch score not computed (no extra dependencies). PAE domain blockiness is a simplified proxy.