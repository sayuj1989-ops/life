# Countercurvature Claims Matrix

This matrix evaluates claims related to the Biological Countercurvature hypothesis, categorizing them based on explicit metric support.

| Claim | Evidence Tier | Source Citation | Notes |
|-------|---------------|-----------------|-------|
| CNNM2, FBLN5, PIEZO2 possess extended, high-confidence structures. | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` | Anisotropy > 3.0, pLDDT > 70. |
| LBX1 is an intermediate-anisotropy, low-confidence structure. | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` | Anisotropy 2.27, pLDDT 66.9. |
| LBX1 geometry has evolved/changed significantly across recent runs. | Speculative narrative (Falsified) | `reports/evidence_freshness_audit.md` | Audit shows identical per-gene values for LBX1 across 22 runs. |
| POC5 and GHR are extremely anisotropic, potential tension rods. | Supported but uncertain | `outputs/afcc/2026-02-16/metrics.csv` | High anisotropy (> 5), but low confidence (pLDDT < 70). |
| Structural clustering reveals novel mechanical pathways. | Speculative narrative | `reports/structure_clusters/*.md` | Relies on low-confidence models and static inputs; high risk of over-interpretation. |
