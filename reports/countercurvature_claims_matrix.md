# Countercurvature Claims Matrix

## Overview
This matrix categorizes current project claims into three tiers of certainty to enforce analytical discipline for the upcoming manuscript. Each claim is mapped to the exact evidence source and assessed for the distinction between direct measurement and hypothesis inference.

---

## Tier 1: Confirmed by Metrics
*These claims are directly derived from repeatable, quantitative analysis of available data with defined thresholds. They use measured evidence rather than causal wording.*

| Claim | Evidence Source / File Citation | Metric Support |
|-------|---------------------------------|----------------|
| **Some scoliosis-associated genes possess highly extended/fibrous architectures.** | `outputs/afcc/2026-02-16/metrics.csv` | PIEZO2, FBLN5, STOML3 show Anisotropy > 4.0 and pLDDT > 70. |
| **LBX1 is predicted to have an intermediate-shape, low-confidence structure with distinct "blocky" domains.** | `outputs/afcc/2026-02-16/metrics.csv`, `reports/alphafold_data_assessment_2026-02-16.md` | Anisotropy ~2.27, pLDDT ~66.9, PAE Blockiness ~7.35. |
| **Many highly anisotropic AlphaFold predictions for candidate genes lack structural confidence.** | `outputs/afcc/confidence_weighted_ranking.csv` | POC5 (Aniso 24.69) and GHR (Aniso 5.13) have mean pLDDT < 65. |
| **Longitudinal AlphaFold metrics for core genes (LBX1, PIEZO2, LMNA) are statically reused across consecutive analysis runs.** | `reports/evidence_freshness_audit.md` | Trend variance is 0 for these genes across 18 distinct runs (Jan-Feb). |

---

## Tier 2: Supported but Uncertain
*These claims have circumstantial data support or use valid proxies, but require orthogonal validation before being stated as fact. They are labeled as inferences.*

| Claim | Evidence Source / File Citation | Caveat / Uncertainty |
|-------|---------------------------------|----------------------|
| **Genes like POC5 and GHR may act as extended tension-rods in a mechanical network.** | `outputs/afcc/confidence_weighted_ranking.csv`, `outputs/afcc/2026-02-16/metrics.csv` | The extreme anisotropy is coupled with very low pLDDT, meaning the extended shape might be a modeling artifact of intrinsically disordered regions rather than a true load-bearing rod. |
| **Metabolic regulators (e.g., PPARGC1A) act as flexible hubs.** | `outputs/afcc/2026-02-16/metrics.csv` | Supported by low pLDDT and intermediate anisotropy, but "hub" function is inferred from generic lack of structure, not specific binding data. |
| **LBX1's high PAE blockiness indicates modular functional domains.** | `outputs/afcc/2026-02-16/metrics.csv` | While mathematically true in the matrix (PAE blockiness = 7.35), it is an inference that these blocks represent independent mechanical modules in vivo. |

---

## Tier 3: Speculative Narrative
*These are hypothesis-generating claims that currently lack direct, robust quantitative support in the repository, or over-interpret static structural models. They MUST NOT be presented as factual mechanisms in the manuscript.*

| Claim | Evidence Source / File Citation | Why it is Speculative / Evidence Against |
|-------|---------------------------------|------------------------------------------|
| **LBX1 structure exhibits shifting or newly emerging geometric classes over time.** | `reports/structure_clusters/2026-01-20__cluster_note.md` | **Directly falsified by audit:** The underlying AlphaFold outputs for LBX1 have remained mathematically identical across all recorded runs. Any narrative of structural "evolution" is artifactual. |
| **Low-confidence anisotropic proteins (POC5) serve as definitive mechanical sensors for spinal countercurvature.** | `reports/afcc_latest.md` | Lacks experimental perturbation data. AlphaFold predicts shape, not stiffness or force-transmission capability. Relying on POC5 for mechanical theory is highly risky given its pLDDT of 64.0. |
| **AlphaFold structural geometry directly predicts scoliotic phenotypic severity.** | General Project Hypothesis | No correlation has been established yet between the numerical value of anisotropy and the clinical Cobb angle or penetrance of the respective gene mutations. |
