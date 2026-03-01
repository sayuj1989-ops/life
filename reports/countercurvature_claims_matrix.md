# Biological Countercurvature Claims Matrix

**Date:** 2026-03-01
**Goal:** Establish claim discipline for the manuscript by strictly separating quantitative measurement from speculative narrative, avoiding causal wording unless directly supported.

| Claim | Tier | Source/Data Support | Caveats/Weaknesses |
| :--- | :--- | :--- | :--- |
| **High Anisotropy Structural Classes Exist** | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv`. Genes like PIEZO2, LMNA, CNNM2, FBLN5 show quantitative anisotropy index > 3.0 and pLDDT mean > 70. | AlphaFold predictions represent single, unliganded states; true *in vivo* flexibility is not directly measured. |
| **Stable Structural Inputs Over Time** | Confirmed by metrics | `scripts/analysis/evidence_freshness_audit.py` demonstrates LBX1, PIEZO2, LMNA, POC5, and GHR metrics are identical from 2026-01-09 to 2026-02-28. | Indicates reuse of static AlphaFold snapshots, explicitly preventing claims of "newly emerging" structural geometries based on these runs. |
| **LBX1 Architecture is Intermediate/Blocky** | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv`. LBX1 shows intermediate anisotropy (2.27), high PAE blockiness (7.35), but low confidence (pLDDT 66.9). | This supports a modular/blocky architecture hypothesis but not high-confidence structural certainty. |
| **POC5 and GHR are Highly Extended** | Supported but uncertain | `outputs/afcc/2026-02-16/metrics.csv`. Extreme anisotropy outliers (POC5: 24.69, GHR: 5.13). | Both have low confidence (pLDDT < 70). High anisotropy may be an artifact of AlphaFold predicting intrinsically disordered regions (IDRs) in extended linear conformations. |
| **PIEZO2 and LMNA are "Tension Rods"** | Supported but uncertain | `outputs/afcc/2026-02-16/metrics.csv`. High anisotropy (>4.0) and adequate confidence (>76 pLDDT). Plausible load-bearing geometry. | While structure suggests load-bearing capacity, this is an inference; direct *in vivo* force transmission measurements are required. |
| **LBX1 acts as a "Tension-Gated Scaffold"** | Speculative narrative | Hypothesized in `reports/structure_clusters/2026-01-20__cluster_note.md` ("The Silenced Spring" model involving tension-dependent unfolding). | Extrapolated from static, low-confidence structural metrics. Lacks direct functional or biophysical evidence. |
| **Long-Range Strain Integration by POC5/MESP2** | Speculative narrative | Hypothesized in `reports/structure_clusters/2026-01-13__cluster_note.md` ("Anisotropic Patterning Axis"). | Relies heavily on the extreme (and low-confidence) anisotropy of POC5 to theorize they act as "strain antennas." Causal link to tissue patterning is untested. |

## Claim Guidance for Manuscript Use
1. **Rely entirely on Tier 1 ("Confirmed by metrics")** for establishing the baseline structural catalog of developmental and mechanosensory candidates.
2. **Present Tier 2 ("Supported but uncertain")** with explicit caveats regarding AlphaFold limitations (e.g., distinguishing extended rigid rods from disordered regions) and the need for orthogonal biophysical validation.
3. **Relegate Tier 3 ("Speculative narrative")** to the Discussion section as hypothesis generation or future directions. Do not frame these claims as findings derived from the current structural data snapshots. Avoid causal wording unless directly supported by functional assays.
