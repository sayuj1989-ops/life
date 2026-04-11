# LBX1 Falsifiability Plan

## Introduction
The current AlphaFold Structural Clustering Pipeline (AFCC) data snapshot (outputs/afcc/2026-02-16/metrics.csv) describes LBX1 as having intermediate anisotropy (~2.27), low confidence (pLDDT ~66.9), and high domain blockiness (PAE ~7.35). Previous narratives have linked LBX1 to mechanosensing purely via geometric interpretation. To build a robust Biological Countercurvature model, this geometric hypothesis must be explicitly tested.

This plan details three experiments designed to *falsify* the hypothesis that LBX1's predicted "blocky" structure intrinsically links it to mechanical force sensing or countercurvature development.

## Experiment 1: The Domain Flexibility Test

- **Hypothesis**: LBX1's high PAE blockiness represents highly flexible disordered linkers between rigid binding domains, meaning it cannot act as a rigid tension rod.
- **Assay Design**: Single-molecule FRET (smFRET) or small-angle X-ray scattering (SAXS) on purified full-length LBX1 protein *in vitro* under varying mechanical loads/crowding environments to measure radius of gyration ($R_g$) variance.
- **Quantitative Readout**: Change in $R_g$ and FRET efficiency distribution spread across conditions.
- **Expected Direction**: $R_g$ will be highly variable and FRET populations will be broadly distributed or rapidly exchanging, characteristic of a flexible, multi-state intrinsically disordered protein (IDP).
- **Falsification Threshold**: If LBX1 adopts a single, rigid extended conformation with low $R_g$ variance (similar to LMNA), the flexibility hypothesis is falsified, supporting a rigid strut model. Conversely, if it is completely flexible, its role as a purely structural "tension sensor" is heavily weakened.

## Experiment 2: The Nuclear Tension Response Test

- **Hypothesis**: LBX1 acts downstream of nuclear mechanotransduction (e.g., LINC complex), rather than being the primary tension sensor itself.
- **Assay Design**: Perturb nuclear tension in cultured somitic mesoderm cells (using LINC complex inhibitors, e.g., dominant-negative KASH domains, or substrate stiffening). Monitor LBX1 nuclear localization and transcriptional activity (via reporter assay).
- **Quantitative Readout**: Nuclear/cytoplasmic ratio of LBX1 fluorescence; normalized luciferase reporter activity for known LBX1 target genes.
- **Expected Direction**: Reduced nuclear tension (LINC disruption) will decrease LBX1 nuclear localization and target transcription, while stiff substrates will increase it.
- **Falsification Threshold**: If LBX1 localization and transcriptional activity remain constant regardless of LINC disruption or extreme substrate stiffness changes (p > 0.05 vs control), the link between LBX1 and direct mechanical load/tension is falsified.

## Experiment 3: The Geometric Rescue Test in Vivo

- **Hypothesis**: The specific blocky architecture (high PAE blockiness) of LBX1 is required for its function in proper spinal alignment and countercurvature.
- **Assay Design**: In a zebrafish *lbx1* null mutant (which develops spinal curvature), perform genetic rescue using three constructs:
  1. Wild-type LBX1.
  2. A "rigidified" LBX1 (flexible linkers replaced by rigid alpha-helical linkers, reducing PAE blockiness).
  3. A "hyper-flexible" LBX1 (linkers expanded with Gly-Ser repeats).
- **Quantitative Readout**: Cobb angle (degree of spinal curvature) measured via microCT at standard developmental stages.
- **Expected Direction**: Wild-type will rescue. If the specific blocky flexibility is functionally required for mechanical integration, both rigid and hyper-flexible mutants will fail to rescue curvature.
- **Falsification Threshold**: If the "rigidified" construct perfectly rescues spinal geometry to wild-type levels (curvature difference < 5 degrees), the hypothesis that its specific "blocky, flexible" geometry (inferred from AFCC) is critical for countercurvature is falsified.
