# Confidence-Weighted Structural Evidence

**Baseline Date:** 2026-02-16
**Metric:** Weighted Score = Anisotropy * (pLDDT / 100)

## Tier 1: Confirmed Structural Drivers (High Anisotropy, High Confidence)
These candidates have robust structural evidence supporting their role as anisotropic mechanical elements.

| gene_symbol | anisotropy_index | plddt_mean | weighted_score |
| --- | --- | --- | --- |
| CNNM2 | 8.540535839977684 | 70.37298285714286 | 6.010229822575638 |
| FBLN5 | 7.054480619949517 | 83.33808035714287 | 5.8790687278326 |
| STOML3 | 5.559834719858973 | 84.32628865979382 | 4.688402274875716 |
| PANX3 | 5.075360561640713 | 81.7247193877551 | 4.147824176917664 |
| PIEZO2 | 4.441176983762356 | 79.4436389280677 | 3.5282326071366135 |
| ROCK1 | 3.2921885930351955 | 76.13419497784342 | 2.5064812824597356 |
| ADGRG6 | 3.0601126170353674 | 73.72809172809173 | 2.256162637270744 |

## Tier 2: Speculative Structural Drivers (High Anisotropy, Low Confidence)
High anisotropy detected but structure is low confidence (IDR or flexible). **Interpret with caution.**

| gene_symbol | anisotropy_index | plddt_mean | weighted_score |
| --- | --- | --- | --- |
| POC5 | 24.686435126462467 | 63.974834782608696 | 15.79310608587024 |
| GHR | 5.13247062540886 | 58.69753918495297 | 3.012633956505567 |
| EMD | 4.288514695460691 | 60.25062992125985 | 2.5838571182808647 |
| MESP2 | 4.029817350768749 | 54.17438287153653 | 2.183128680629072 |
| ARNTL | 3.3192797281217827 | 65.52864217252394 | 2.1750789357460487 |

## LBX1 Comparative Analysis
Evaluating LBX1 against known mechanosensors and controls.

| gene_symbol | anisotropy_index | plddt_mean | PAE_domain_blockiness_score | confidence_tier | Comment |
| --- | --- | --- | --- | --- | --- |
| POC5 | 24.686435126462467 | 63.974834782608696 | 3.508112193042216 | Tier 2: High Anisotropy + Low Confidence | Extreme anisotropy, but check confidence. |
| GHR | 5.13247062540886 | 58.69753918495297 | 5.309022073672339 | Tier 2: High Anisotropy + Low Confidence |  |
| PIEZO2 | 4.441176983762356 | 79.4436389280677 | 2.799985883630068 | Tier 1: High Anisotropy + High Confidence | Confirmed high-anisotropy sensors. |
| ADGRG6 | 3.0601126170353674 | 73.72809172809173 | 6.778548436294672 | Tier 1: High Anisotropy + High Confidence |  |
| LBX1 | 2.266410666464284 | 66.86779359430605 | 7.354659843586591 | Tier 4: Low Anisotropy + Low Confidence | Baseline target. Moderate anisotropy, low confidence. Likely NOT a primary structural rod. |

### LBX1 Assessment
- **Anisotropy:** 2.27 (Moderate)
- **Confidence (pLDDT):** 66.87 (Low/Moderate)
- **Blockiness:** 7.35

**Conclusion:** LBX1's structural metrics do not support a "Tension Rod" hypothesis. It clusters with globular/intermediate proteins. Its role is likely regulatory rather than structural.
