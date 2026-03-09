# Counter-Curvature Claims Matrix

## Overview
This matrix categorizes key claims surrounding the Biological Counter-Curvature hypothesis according to their current level of empirical support within the repository's datasets.

| Claim | Support Tier | Exact Source File(s) / Rows | Justification |
|---|---|---|---|
| Strong structural signals for mechanosensory architecture exist in CNNM2, FBLN5, PIEZO2. | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` (Rows: CNNM2, FBLN5, PIEZO2) | These candidates meet both high anisotropy (>= 3.0) and adequate confidence (pLDDT >= 70.0) thresholds. |
| LBX1 has a stable, intermediate-anisotropy, highly blocky structure. | Confirmed by metrics | `outputs/afcc/2026-01-09` through `2026-02-16` `metrics.csv` | Metrics for LBX1 (Anisotropy: 2.27, pLDDT: 66.9, PAE Blockiness: 7.35) are identical across all 17 runs in the baseline window. |
| POC5 and GHR exhibit extreme tension-rod (highly anisotropic) morphologies. | Supported but uncertain | `outputs/afcc/2026-02-16/metrics.csv` (Rows: POC5, GHR) | Both have very high anisotropy (>5.0) but low confidence (pLDDT < 70.0), indicating potential IDRs rather than rigid rods. |
| LBX1 geometry evolved or emerged over the Jan-Feb 2026 period. | Speculative narrative | `reports/evidence_freshness_audit.md`, `reports/structure_clusters/2026-01-20__cluster_note.md` | The underlying AlphaFold metrics for LBX1 were strictly static during this period; narrative claims of 'emergence' lack new structural data backing. |
| The "Energy Deficit Window" causes structural failure. | Speculative narrative | `scripts/experiment_energy_deficit_window.py` (Simulation parameters) | Currently modeled theoretically; requires direct metabolic/stiffness measurements in vivo during the adolescent growth spurt for validation. |

