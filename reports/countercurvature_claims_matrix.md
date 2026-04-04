# Countercurvature Claims Matrix

**Date:** 2026-04-04

## Overview
This matrix categorizes claims related to the Biological Countercurvature hypothesis based on the strength of structural evidence derived from AlphaFold data.

### Tier 1: Confirmed by Metrics
Claims directly supported by quantitative structural metrics with high confidence.

| Claim | Source / Evidence | Confidence |
|-------|-------------------|------------|
| PIEZO2 exhibits a highly anisotropic, extended architecture consistent with a tension-sensing role. | `outputs/afcc/2026-02-16/metrics.csv` (Anisotropy: 4.44, pLDDT: 79.4) | High |
| FBLN5 and STOML3 are high-anisotropy, structurally confident proteins. | `outputs/afcc/2026-02-16/metrics.csv` (FBLN5 Anisotropy: 7.05, pLDDT: 83.3; STOML3 Anisotropy: 5.56, pLDDT: 84.3) | High |

### Tier 2: Supported but Uncertain
Claims supported by metrics but requiring caution due to low confidence scores (pLDDT < 70).

| Claim | Source / Evidence | Confidence |
|-------|-------------------|------------|
| POC5 is highly anisotropic, potentially forming extended structures. | `outputs/afcc/2026-02-16/metrics.csv` (Anisotropy: 24.69, pLDDT: 64.0) | Low (Likely disordered) |
| GHR possesses extended fibrous architecture that could be mechanically sensitive. | `outputs/afcc/2026-02-16/metrics.csv` (Anisotropy: 5.13, pLDDT: 58.7) | Low (Potential artifact of disorder) |

### Tier 3: Speculative Narrative
Claims that over-interpret the data or rely on structurally uncertain candidates.

| Claim | Source / Evidence | Confidence |
|-------|-------------------|------------|
| LBX1 acts as a rigid, anisotropic structural scaffold for mechanotransduction. | `outputs/afcc/2026-02-16/metrics.csv` (Anisotropy: 2.27, pLDDT: 66.9) | Very Low (Inadequate anisotropy, high disorder) |
| The "Blocky Scaffolds" cluster represents a distinct functional class of mechanically active proteins. | `reports/structure_clusters/*.md` | Low (Cluster membership driven by low-confidence regions rather than verified domains) |
