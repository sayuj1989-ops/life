# Countercurvature Claims Matrix

This document maps claims relating to the Biological Countercurvature hypothesis to their exact supporting evidence and assigns an epistemological confidence tier.

| Claim | Tier | Exact Source / File | Metric Support / Caveat |
|-------|------|---------------------|--------------------------|
| **PIEZO2 represents a strong mechanosensor candidate.** | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` | Anisotropy=4.44, pLDDT=79.4. Reliable extended structure. |
| **CNNM2 and FBLN5 show the highest reliable anisotropy.** | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` | CNNM2 (8.54, pLDDT 70.4), FBLN5 (7.05, pLDDT 83.3). |
| **LBX1 structure is highly dynamic/evolving.** | Speculative narrative | `reports/evidence_freshness_audit.md` | Falsified by audit. Metrics are entirely static across all runs. |
| **LBX1 possesses an intermediate, blocky structure.** | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` | Anisotropy=2.27, PAE_blockiness=7.35. |
| **LBX1 is a reliable, high-confidence mechanosensor.** | Speculative narrative | `outputs/afcc/2026-02-16/metrics.csv` | Weakened by low pLDDT (66.9) and intermediate anisotropy (2.27). |
| **POC5 and GHR are extreme fibrous tension rods.** | Supported but uncertain | `outputs/afcc/2026-02-16/metrics.csv` | High anisotropy but low pLDDT. May simply be disordered regions. |
| **Narrative updates reflect real-time structural discoveries.** | Speculative narrative | `reports/evidence_freshness_audit.md` | Audit shows reused static vectors trigger false "discovery" narratives. |

## Tiers:
- **Confirmed by metrics:** Directly observable, high-confidence data in the authoritative snapshot.
- **Supported but uncertain:** Observable metric trends, but constrained by high uncertainty (e.g., low pLDDT).
- **Speculative narrative:** Claims that extrapolate beyond the data, infer causality without experiments, or rely on static reused inputs.
