# Evidence Note: Metabolic Expansion of the Counter-Curvature Pipeline

**Date:** 2026-02-20
**Topic:** Gravity Spine Counter-Curvature
**Tags:** #Thermodynamic_Cost #Metabolism #Anisotropy #Gamma_m

## Overview

This note documents the expansion of the AlphaFold Counter-Curvature (AFCC) pipeline to include six critical metabolic and structural proteins linked to the "Thermodynamic Cost" hypothesis (Gamma_m) and muscle tone maintenance (eta_a). These proteins were identified as key supply-side constraints during the adolescent growth spurt.

## New Metric Computations

We successfully fetched structures and computed anisotropy metrics for the following candidates:

| Gene | UniProt | Term | Role | Anisotropy | Morphology | Residues | Status |
| :--- | :--- | :--- | :--- | ---: | :--- | ---: | :--- |
| **GHR** | P10912 | Gamma_m | Growth Hormone Receptor | **5.13** | Fibrous/Extended | 638 | Computed |
| **ARNTL** | O00327 | Gamma_m | BMAL1 (Circadian Clock) | **3.32** | Fibrous/Extended | 626 | Computed |
| **PPARGC1A** | Q9UBK2 | Gamma_m | PGC-1alpha (Mitochondrial) | 2.19 | Intermediate | 798 | Computed |
| **MYLK** | Q15746 | eta_a | Myosin Light Chain Kinase | 1.46 | Globular | 1914 | Computed |
| **IGF1R** | P08069 | Gamma_m | IGF-1 Receptor | 1.43 | Globular | 1367 | Computed |
| **DMD*** | P11532 | eta_a | Dystrophin (Fragment) | 1.32 | Globular | 525 | Computed |

*\*Note: DMD structure appears to be a fragment or specific domain construct available in AlphaFold DB (525 residues vs full length ~3685).*

## Key Findings

1.  **High Anisotropy in GHR (5.13):** The Growth Hormone Receptor exhibits significant structural anisotropy, consistent with the "Anisotropic Supply Hypothesis". This suggests its signaling efficiency may be highly sensitive to cytoplasmic crowding and compressive stress, potentially linking rapid growth (high GHR activity) to metabolic vulnerability in the spine.
2.  **Circadian Anisotropy (ARNTL):** BMAL1 (ARNTL) also shows elevated anisotropy (3.32), supporting the link between circadian rhythm disruption and spinal integrity (as seen in the "Spinal Jetlag" experiments).
3.  **Globular Nature of Kinases:** IGF1R and MYLK are relatively globular (Anisotropy < 1.5), which is typical for large enzymatic domains, though their large size (high residue count) contributes to their thermodynamic cost.

## Implication for "Energy Deficit Window"

The high anisotropy of GHR and ARNTL reinforces the concept that the **Basal Tissue Maintenance (Gamma_m)** term is not just a scalar cost but has geometric dependencies. The "Scaling Law Mismatch" identified in earlier research (Demand $L^{2.5}$ vs Supply $L^{1.3}$) may be exacerbated by the crowding sensitivity of these anisotropic supply proteins.

## Next Steps

*   Integrate these values into the "Protein Cost Landscape" visualization (`experiment_protein_physics.py`).
*   Investigate if the DMD fragment accurately represents the costamere's mechanical role or if full-length modeling is required.
