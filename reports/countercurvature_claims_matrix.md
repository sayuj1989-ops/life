# Countercurvature Claims Matrix

This matrix details the evidence base for the Biological Countercurvature hypothesis, carefully separating direct measurement from inference.

| Claim | Tier | Source/Reference | Notes/Caveats |
|-------|------|------------------|---------------|
| PIEZO2 possesses a highly extended, anisotropic structure consistent with a mechanosensor. | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` (Anisotropy 4.44, pLDDT 79.4) | Directly derived from high-confidence AlphaFold predictions. |
| CNNM2 and FBLN5 display strong anisotropic geometry. | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` (CNNM2 Anis. 8.54, FBLN5 Anis. 7.05) | High pLDDT (>70) confirms geometry reliability. |
| LBX1 has an intermediate, high-blockiness structure. | Confirmed by metrics | `outputs/afcc/2026-02-16/metrics.csv` (Anisotropy 2.27, PAE 7.35, pLDDT 66.9) | Low confidence limits structural interpretation; must be verified experimentally. |
| POC5 and GHR possess extremely anisotropic structures. | Supported but uncertain | `outputs/afcc/2026-02-16/metrics.csv` (POC5 Anis. 24.69, pLDDT 64.0) | Values are driven by low-confidence regions (IDRs); could be artifacts of modeling disorder. |
| Repeated AFCC runs reveal dynamic conformational shifts in core candidates. | Speculative narrative | `reports/evidence_freshness_audit.md` | Audit shows core metrics (LBX1, PIEZO2) are perfectly static across Jan-Feb runs. Trend claims are ungrounded. |
| LBX1 acts as a pure mechanical 'tension rod' to relay curvature stress to the nucleus. | Speculative narrative | `reports/structure_clusters/` notes | Falsifiable experiments are pending (`reports/lbx1_falsifiability_plan.md`); current structural data is too low-confidence (pLDDT < 70) to fully support this. |
