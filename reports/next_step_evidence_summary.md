# Next Step Evidence Summary

**Generated**: 2026-03-04
**Source Data**: `outputs/afcc/2026-02-16/metrics.csv`, `outputs/afcc/confidence_weighted_ranking.csv`, `reports/evidence_freshness_audit.md`

## 1. What is stronger now than baseline
* **Clear separation of Confidence vs. Shape**: We have explicitly separated candidates with high anisotropy into those with adequate confidence (`pLDDT >= 70`) versus those with low confidence. For instance, `PIEZO2` (anisotropy 4.44, pLDDT 79.4, per `outputs/afcc/2026-02-16/metrics.csv`), `CNNM2`, `FBLN5`, and `STOML3` are now confirmed as robust tension-rod models, whereas `POC5` and `GHR` are downgraded to speculative due to low pLDDT.
* **Refined understanding of LBX1**: LBX1's profile is now rigorously defined as an intermediate-anisotropy (2.27), highly blocky (PAE blockiness 7.35) structure with low confidence (pLDDT 66.9) per `outputs/afcc/2026-02-16/metrics.csv`. This falsifies simplistic "LBX1 is a rigid tension rod" narratives and properly bounds its hypothesized function to a modular or spring-like role.
* **Data Freshness and Narrative Discipline**: The audit (`reports/evidence_freshness_audit.md`) revealed that multiple daily and cluster reports had generated "new" narratives from completely static structural metrics (e.g., PIEZO2, LMNA, LBX1 metric vectors were unchanged over the trend window from `outputs/afcc/2026-01-09` to `outputs/afcc/2026-02-16`). We now have a clear claims matrix (`reports/countercurvature_claims_matrix.md`) that separates direct measurements from narrative inference.

## 2. What remains weak
* **Biological Validation of "Blocky" IDRs**: For candidates like LBX1, we rely heavily on AlphaFold's PAE blockiness to infer modular function. However, the low overall pLDDT means these hinges might simply be unstructured IDRs without any spring-like mechanical properties.
* **Causal Link Between Shape and Function**: High anisotropy, even with high confidence (like `FBLN5` or `PIEZO2`), is currently just a geometric property. We lack direct experimental evidence showing these specific structural features actively transduce tension in the spinal somite context.
* **Low-Confidence Outliers**: Extreme anisotropy candidates (like `POC5` at 24.69, per `outputs/afcc/2026-02-16/metrics.csv`) remain entirely speculative. Their high anisotropy might simply be an AlphaFold artifact for long, natively unstructured sequences.

## 3. Evidence AGAINST or weakening the current hypothesis
* **LBX1 is not a strong structural anchor (Direct Measurement)**: The data directly contradicts the hypothesis that LBX1 is a purely structural, fibrous tension rod. Its intermediate anisotropy (2.27) and low pLDDT (66.9) (per `outputs/afcc/2026-02-16/metrics.csv`) position it closer to a standard globular or modular protein, significantly weakening claims of its direct load-bearing capacity.
* **Static "Evolution" of Structural Narratives (Inference from Audit)**: The freshness audit (`reports/evidence_freshness_audit.md`) demonstrates that previously hypothesized "emerging structural classes" or "evolution" of candidate geometries over Jan-Feb 2026 were based on static, unchanged AlphaFold inputs. The narrative outpaced the measured evidence, meaning any temporal or causal inferences drawn during that period are unsupported by the underlying data.

## 4. Top 3 highest-leverage next experiments
1. **smFS of LBX1 and Modular Candidates**: Perform single-molecule force spectroscopy on recombinant LBX1 to test if its "blocky" domains exhibit discrete, force-dependent unfolding steps characteristic of a mechanical spring, thereby validating the PAE-based hypothesis.
2. **Nuclear Tension Perturbation (LINC complex)**: Modulate nuclear tension via LMNA knockdown or LINC complex disruption and measure the nuclear/chromatin localization of intermediate candidates like LBX1. This directly tests the core mechanotransduction hypothesis independent of AlphaFold predictions.
3. **Ensemble Modeling / MD of IDRs**: For low-confidence, high-anisotropy outliers (POC5, GHR), use ensemble modeling tools (e.g., AlphaFold-Multimer, Rosetta, or molecular dynamics relaxation) to determine if their extended structures represent stable physiological states or transient/artifactual conformations.