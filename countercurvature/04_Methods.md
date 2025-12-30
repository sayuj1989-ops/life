# Methods: Deterministic IEC Beam Surrogate and AlphaFold Analysis

This repository makes the manuscript fully quantitative and reproducible using a deterministic Euler--Bernoulli surrogate (the small-deflection limit of a Cosserat rod) with IEC-prescribed intrinsic curvature.

## Deterministic IEC Beam Model

To explore the mode selection mechanism (Eq.~\ref{eq:mode_selection}), we discretize the linearized beam equations using a finite difference scheme on a 1D domain $s \in [0, L]$. The rod is divided into $N=100$ segments. The information field $I(s)$ is mapped to local stiffness $E_i$ and rest curvature $\kappa_{i}$ at each node. We solve the resulting boundary value problem (BVP) using a standard shooting method (or sparse matrix solver for the eigenproblem). This allows rapid exploration of the $(\chi_\kappa, g)$ parameter space to identify regions where S-modes become the ground state.

## Note on 3D Cosserat Rod Implementation (PyElastica)

The Cosserat rod formulation motivates the IEC intrinsic-geometry picture, but the reproducible computations in this repository use the linear Euler--Bernoulli limit (planar deflection with a prescribed intrinsic curvature field). A full PyElastica implementation is future work.

## Parameter Sweeps and Mode Classification

We perform systematic parameter sweeps over the coupling strength $\chi_\kappa$ (range $[0, 0.1]$) and gravitational acceleration $g$ (range $[0.01, 1.0]$ $g_{\mathrm{Earth}}$). For each simulation, we compute the equilibrium shape and evaluate the following metrics:
1.  \textbf{Geodesic Deviation} $\widehat{D}_{\mathrm{geo}}$: Quantifies the difference between the realized shape and the gravity-only geodesic.
2.  \textbf{Lateral Deviation} $S_{\mathrm{lat}}$: Measures symmetry breaking in the coronal plane.
3.  \textbf{Cobb Angle}: Standard clinical measure for scoliotic curves.

Regimes are classified as \emph{gravity-dominated} ($\widehat{D}_{\mathrm{geo}} < 0.1$), \emph{cooperative} ($0.1 < \widehat{D}_{\mathrm{geo}} < 0.3$), or \emph{information-dominated} ($\widehat{D}_{\mathrm{geo}} > 0.3$).

## AlphaFold Protein Structure Analysis

To investigate "counter-curvature" at the molecular scale, we retrieved predicted 3D structures for candidate mechanosensitive and longevity-associated proteins from the AlphaFold Protein Structure Database.
- **Targets**: YAP1 (P46937), FOXO3 (O43524), SIRT1 (Q96EB6), PGC1A (Q9UBK2).
- **Structure Retrieval**: High-confidence models (v6) were downloaded via the AlphaFold API.
- **Geometric Analysis**: For each protein, we computed the local backbone curvature $\kappa(s)$ along the C$\alpha$ trace using a sliding window of 5 residues.
- **Information Content**: Shannon entropy $H$ was calculated from the primary amino acid sequence distribution.
- **Correlation**: We computed the Pearson correlation coefficient between the mean backbone curvature and the sequence entropy to test the hypothesis that information-rich sequences encode more highly curved, structurally rigid geometries.

The reproducible AlphaFold reanalysis code is provided in `scripts/alphafold_reanalysis.py` and writes outputs to `results/` and `figures/`.

## Validation

The deterministic surrogate is validated against analytical expectations for small-deflection Euler--Bernoulli beams (cantilever under distributed load). All parameters and sweeps are defined in `config/default.yaml`.
