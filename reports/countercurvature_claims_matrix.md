# Countercurvature Claims Matrix

## Data Provenance
- Date: 2026-02-16
- Reference file: `outputs/afcc/2026-02-16/metrics.csv`

## Claims Classification

### Tier 1: Confirmed by Metrics
| Claim | Exact Source File | Source Row/Gene | Metric Value |
|-------|-------------------|-----------------|--------------|
| `CNNM2` possesses a highly extended, anisotropic structure. | `outputs/afcc/2026-02-16/metrics.csv` | CNNM2 | Anisotropy = 8.54, pLDDT = 70.4 |
| `PIEZO2` has a confirmed high-confidence extended architecture. | `outputs/afcc/2026-02-16/metrics.csv` | PIEZO2 | Anisotropy = 4.44, pLDDT = 79.4 |
| `ADGRG6` demonstrates strong structural signaling properties. | `outputs/afcc/2026-02-16/metrics.csv` | ADGRG6 | Anisotropy = 3.06, pLDDT = 73.7 |
| `LBX1` structurally registers as an intermediate/globular shape with low predictive confidence. | `outputs/afcc/2026-02-16/metrics.csv` | LBX1 | Anisotropy = 2.27, pLDDT = 66.9 |

### Tier 2: Supported but Uncertain
| Claim | Exact Source File | Source Row/Gene | Caveat / Uncertainty |
|-------|-------------------|-----------------|----------------------|
| Extremely high anisotropy candidates like `POC5` may act as tension rods. | `outputs/afcc/2026-02-16/metrics.csv` | POC5 | Very high anisotropy (24.69) but low confidence (pLDDT=64.0); could be an artifact of disorder. |
| `GHR`'s extended geometry couples with growth signaling mechanotransduction. | `outputs/afcc/2026-02-16/metrics.csv` | GHR | High anisotropy (5.13) but low confidence (pLDDT=58.7). Needs functional validation. |
| The metrics underlying core candidates (LBX1, PIEZO2) are stable across the measured window. | `reports/evidence_freshness_audit.md` | Audit script results | Identical vectors in output cache indicate stability, but means temporal changes cannot be inferred. |

### Tier 3: Speculative Narrative
| Claim | Exact Source File | Source Row/Gene | Falsification / Risk |
|-------|-------------------|-----------------|----------------------|
| `LBX1` acts as a direct mechanosensor through dynamic blocky domain rearrangement. | `reports/alphafold_data_assessment_2026-02-16.md` | LBX1 | High risk: Low pLDDT suggests disorder; "blocky" signal could just be uncoupled static domains. |
| Temporal evolution of structural predictions reveals emerging mechanosensitive traits over Jan-Feb. | `reports/afcc_latest.md` (historical versions) | Multiple | Falsified by audit: The underlying cached outputs did not change, meaning narrative updates were artifacts of human/agent interpretation, not data. |
