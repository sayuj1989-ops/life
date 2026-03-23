# Countercurvature Claims Matrix

This matrix categorizes claims related to the Biological Countercurvature hypothesis according to their evidentiary support, explicitly mapping them to source data.

| Claim | Tier | Source Evidence / Files | Notes |
|-------|------|-------------------------|-------|
| FBLN5, STOML3, PANX3, PIEZO2, ROCK1 are high-confidence, extended fibrous structures. | **Confirmed by metrics** | `outputs/afcc/2026-02-16/metrics.csv`; `reports/alphafold_data_assessment_2026-02-16.md` | Anisotropy > 3.0, pLDDT > 70. Reliable geometric inference. |
| LBX1 has a modular/blocky architecture with intermediate anisotropy. | **Confirmed by metrics** | `outputs/afcc/2026-02-16/metrics.csv` | Anisotropy ~2.27, pLDDT ~66.9, PAE Blockiness ~7.35. |
| Core candidates (LBX1, PIEZO2, LMNA) have static structural metrics across the trend window. | **Confirmed by metrics** | `scripts/analysis/evidence_freshness_audit.py`; `reports/evidence_freshness_audit.md` | Values are identical across all available runs; structural "evolution" claims are artifacts. |
| POC5 and GHR possess extreme fibrous/extended geometries. | **Supported but uncertain** | `outputs/afcc/2026-02-16/metrics.csv` | Extreme anisotropy (>5) but low confidence (pLDDT < 70). Could be highly flexible disordered tails rather than rigid rods. |
| LBX1 geometry changed over Jan-Feb, indicating evolving mechanistic state. | **Speculative narrative** | `reports/alphafold_data_assessment_2026-02-16.md`; `reports/evidence_freshness_audit.md` | **Falsified by data audit.** Metrics are completely static. Narrative cluster updates were hypothesis generation, not measurement. |
| LBX1 acts as a direct mechanical sensor or tension rod in the spine. | **Speculative narrative** | `outputs/afcc/2026-02-16/metrics.csv` | LBX1 lacks the high anisotropy and high confidence of bona fide structural rods (e.g., PIEZO2, LMNA). Needs functional validation (see `reports/lbx1_falsifiability_plan.md`). |
