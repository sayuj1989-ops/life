# Countercurvature Claims Matrix: Evidence Status
**Date:** 2026-02-19
**Scope:** Structural and mechanosensitive claims derived from AFCC analysis.

| Claim ID | Claim Description | Evidence Status | Source Data | Confidence | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **C-001** | **"Tension Rods" Exist** | ✅ **Confirmed** | `metrics.csv`: PIEZO2 (4.44), LMNA (4.75), ADGRG6 (3.06) | **High** | Multiple high-confidence structures exceed Anisotropy > 3.0. |
| **C-002** | **PIEZO2 is a Linear Sensor** | ✅ **Confirmed** | `metrics.csv`: PIEZO2 (Anisotropy 4.44, pLDDT 79.4) | **High** | Strong structural evidence for extended geometry. |
| **C-003** | **LBX1 is a Structural Rod** | ❌ **Speculative / Weakened** | `metrics.csv`: LBX1 (Anisotropy 2.27, pLDDT 66.9) | **Low** | Anisotropy is moderate; structure is globular/intermediate. Unlikely to bear load. |
| **C-004** | **Metabolic Receptors are Anisotropic** | ⚠️ **Supported (with Caveats)** | `metrics.csv`: GHR (5.13), ARNTL (3.32) vs IGF1R (1.43) | **Medium** | GHR is highly anisotropic but low confidence (pLDDT 58.7). IGF1R is globular. The claim is not universal. |
| **C-005** | **Ciliary Proteins are Fibrous** | ⚠️ **Supported** | `metrics.csv`: POC5 (24.69) | **Low** | POC5 has extreme anisotropy but very low confidence (pLDDT 64.0) and high hinge count. Likely flexible. |
| **C-006** | **Collagen (COL1A1) is Anisotropic** | ⚠️ **Supported (Artifactual?)** | `metrics.csv`: COL1A1 (2.80) | **Low** | Low pLDDT (52.7) and high disorder. AlphaFold struggles with collagen triple helix. Result likely unreliable. |
| **C-007** | **Nuclear Envelope Stiffness (LMNA)** | ✅ **Confirmed** | `metrics.csv`: LMNA (4.75, pLDDT 76.4) | **High** | Consistent with known biology. Serves as a positive control. |

## Legend
- **Confirmed:** Supported by high-anisotropy (>3.0) and high-confidence (>70 pLDDT) metrics.
- **Supported:** Supported by metrics but limited by low confidence or mixed results.
- **Speculative:** Weak metric support or contradicts current data.

## Implications for Manuscript
- **Retain:** Claims C-001, C-002, C-007 as core pillars.
- **Refine:** Claim C-004 to be specific (GHR, not all metabolic receptors).
- **Reframe:** Claim C-003 (LBX1) should move from "Structural" to "Regulatory/Metabolic" or "Downstream Effector".
- **Discard/Caveat:** Claim C-006 (Collagen) should be cited with extreme caution or excluded due to model limitations.
