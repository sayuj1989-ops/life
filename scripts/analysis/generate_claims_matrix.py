from pathlib import Path

def generate_claims_matrix():
    report_content = """# Countercurvature Claims Matrix

**Date**: 2026-02-19

This matrix categorizes claims related to the Biological Countercurvature hypothesis into three tiers, mapping each to exact source rows/files to enforce claim discipline.

## Tier 1: Confirmed by Metrics

These claims are directly supported by measured quantitative data in the repository, primarily from the authoritative snapshot `outputs/afcc/2026-02-16/metrics.csv` and historical data tracking.

| Claim | Evidence Source | Exact Rows/Files |
|-------|----------------|------------------|
| **LBX1 is a low-confidence, intermediate-anisotropy structure.** | `metrics.csv` snapshot | `LBX1,P52954,... Intermediate, 2.266... 66.86...` in `outputs/afcc/2026-02-16/metrics.csv` |
| **LBX1 structural metrics are static across runs.** | Freshness audit history | See `reports/evidence_freshness_audit.md` (Runs present: 17, First Date: 2026-01-09) |
| **PIEZO2 is a high-anisotropy, adequate-confidence mechanosensor candidate.** | `metrics.csv` snapshot | `PIEZO2,Q9H5I5,... Fibrous/Extended, 4.441... 79.44...` in `outputs/afcc/2026-02-16/metrics.csv` |
| **POC5 and GHR exhibit extreme anisotropy but suffer from low pLDDT scores.** | `metrics.csv` snapshot | `POC5` (anisotropy=24.69, pLDDT=63.97), `GHR` (anisotropy=5.13, pLDDT=58.70) in `outputs/afcc/2026-02-16/metrics.csv` |

## Tier 2: Supported but Uncertain

These claims have directional support from data but rely on inferential leaps regarding biological function, or involve metrics near thresholds of reliability.

| Claim | Evidence Source | Exact Rows/Files |
|-------|----------------|------------------|
| **High-anisotropy, low-confidence genes represent flexible tension rods.** | AlphaFold geometry metrics and cluster notes | `POC5`, `GHR` in `outputs/afcc/2026-02-16/metrics.csv`; discussed in `reports/structure_clusters/2026-01-06__anisotropic_sensors.md` |
| **LBX1's high PAE blockiness implies a modular architecture.** | PAE domain blockiness score | `LBX1` (PAE blockiness=7.35) in `outputs/afcc/2026-02-16/metrics.csv` |
| **Circadian-mechanic coupling via ARNTL (extended geometry).** | Anisotropy metrics | `ARNTL` (anisotropy=3.32) in `outputs/afcc/2026-02-16/metrics.csv`; `reports/afcc_latest.md` (2026-03-05 entry) |

## Tier 3: Speculative Narrative

These claims over-interpret static inputs, rely on unverified structural states, or attribute dynamic biological function to static geometric proxies without direct measurement.

| Claim | Evidence Source | Exact Rows/Files |
|-------|----------------|------------------|
| **LBX1's structural state evolved over Jan-Feb, supporting new mechanistic interactions.** | Cluster narratives (refuted by static metrics) | `2026-01-20__cluster_note.md`, `2026-02-01__blocky_lbx1.md` flagged in `reports/alphafold_data_assessment_2026-02-16.md` |
| **POC5's extreme anisotropy directly translates to load-bearing mechanotransduction.** | Extrapolation from geometry | `POC5` (anisotropy=24.69, pLDDT=63.97) in `outputs/afcc/2026-02-16/metrics.csv` |
| **Changes in LMNA conformation actively drive proprioceptive delay.** | AlphaFold geometry metrics and speculative narrative | `LMNA` not present in 2026-02-16 snapshot; metrics were static from `2026-01-14` to `2026-02-26` |
"""
    report_path = Path('reports/countercurvature_claims_matrix.md')
    with open(report_path, 'w') as f:
        f.write(report_content)

    print(f"Report generated at {report_path}")

if __name__ == "__main__":
    generate_claims_matrix()
