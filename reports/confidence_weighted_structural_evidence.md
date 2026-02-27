# Confidence-Weighted Structural Evidence

**Baseline Date:** 2026-02-27
**Source Data:** /app/research/alphafold_countercurvature/data/processed/protein_metrics.csv
**Metric:** Weighted Score = Anisotropy * (pLDDT / 100)

## Tier 1: Confirmed Structural Drivers (High Anisotropy, High Confidence)
These candidates have robust structural evidence supporting their role as anisotropic mechanical elements.

| gene_symbol | anisotropy_index | plddt_mean | weighted_score |
| --- | --- | --- | --- |
| LMNA | 4.751667397697646 | 76.37072289156627 | 3.6288827410245674 |
| PIEZO2 | 4.441176983762356 | 79.4436389280677 | 3.5282326071366135 |
| ADGRG6 | 3.0601126170353674 | 73.72809172809173 | 2.256162637270744 |

## Tier 2: Speculative Structural Drivers (High Anisotropy, Low Confidence)
High anisotropy detected but structure is low confidence (IDR or flexible). **Interpret with caution.**

| gene_symbol | anisotropy_index | plddt_mean | weighted_score |
| --- | --- | --- | --- |
| POC5 | 24.686435126462467 | 63.974834782608696 | 15.79310608587024 |
| GHR | 5.13247062540886 | 58.69753918495297 | 3.012633956505567 |
| ARNTL | 3.3192797281217827 | 65.52864217252394 | 2.1750789357460487 |

## LBX1 Comparative Analysis
Evaluating LBX1 against known mechanosensors and controls.

| gene_symbol | anisotropy_index | plddt_mean | PAE_domain_blockiness_score | confidence_tier | Comment |
| --- | --- | --- | --- | --- | --- |
| POC5 | 24.686435126462467 | 63.974834782608696 | 3.508112193042216 | Tier 2: High Anisotropy + Low Confidence | Extreme anisotropy, but check confidence (Ciliary). |
| GHR | 5.13247062540886 | 58.69753918495297 | 5.309022073672339 | Tier 2: High Anisotropy + Low Confidence | High anisotropy, low confidence (Membrane). |
| LMNA | 4.751667397697646 | 76.37072289156627 | 2.562202816305735 | Tier 1: High Anisotropy + High Confidence | Confirmed high-anisotropy sensor (Nuclear). |
| PIEZO2 | 4.441176983762356 | 79.4436389280677 | 2.799985883630068 | Tier 1: High Anisotropy + High Confidence | Confirmed high-anisotropy sensor (Vector). |
| ADGRG6 | 3.0601126170353674 | 73.72809172809173 | 6.778548436294672 | Tier 1: High Anisotropy + High Confidence | High anisotropy, good confidence (GPCR). |
| LBX1 | 2.266410666464284 | 66.86779359430605 | 7.354659843586591 | Tier 4: Low Anisotropy + Low Confidence | Baseline target. Moderate anisotropy, low confidence. Likely NOT a primary structural rod. |
| RUNX3 | 2.0611670656856456 | 60.564096385542165 | 0.0 | Tier 4: Low Anisotropy + Low Confidence | Comparator (Monolithic). |

### LBX1 Assessment
- **Anisotropy:** 2.27 (Moderate)
- **Confidence (pLDDT):** 66.87 (Low/Moderate)
- **Blockiness:** 7.35

**Conclusion:** LBX1's structural metrics do not support a "Tension Rod" hypothesis. It clusters with globular/intermediate proteins. Its role is likely regulatory rather than structural.
