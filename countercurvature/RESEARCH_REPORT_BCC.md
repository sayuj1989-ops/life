# Biological Countercurvature Research Report

## Status
This document is a technical appendix to `countercurvature/MANUSCRIPT_COMPLETE.md` and retains expanded tables and workflow details.

## Executive Summary
- Unified framework: Normal sagittal curvature and scoliosis-like lateral deviations emerge from a single IEC-Cosserat model operating in different countercurvature regimes.
- Phase diagram: An intrinsic-geometry (incompatible elasticity) framing yields gravity-dominated, cooperative, and information-dominated regimes, with geodesic deviation as the order parameter.
- Microgravity persistence: Intrinsic geometry persists as gravitational loading decreases; expressed curvature may flatten if active feedback down-regulates (quantitative deltas pending).
- Scoliosis bifurcation: Small asymmetries are suppressed in gravity-dominated regimes but amplified into lateral deviations in information-dominated regimes.
- Molecular support: Raw entropy--curvature correlation across 53 proteins is modest (r = 0.405, p = 0.0026) but not significant under pLDDT filtering (r = -0.077, p = 0.5884); length-adjusted partial r = 0.441, while length + pLDDT partial r = 0.104.

## Abstract
Living systems routinely maintain structure against gravity, from plant stems to vertebrate spines. We propose a quantitative framework of biological countercurvature, where developmental information prescribes intrinsic geometry in the sense of incompatible elasticity and morphoelastic rods. By coupling an Information--Elasticity (IEC) model to Cosserat rod mechanics, we treat the spine as a rod with a prescribed reference metric and intrinsic curvature that minimizes elastic energy. In covariant form, the static minimizer can be interpreted as a geodesic of the reference metric without relying on a purely metaphorical spacetime analogy. We derive a mode selection principle showing that while gravity alone selects a C-shaped sag, the information-coupled system stabilizes an S-shaped counter-curvature mode. A normalized geodesic deviation metric $\widehat{D}_{\mathrm{geo}}$ quantifies this information-driven reshaping. Phase diagrams reveal distinct regimes: gravity-dominated, cooperative, and information-dominated, where the latter predicts the emergence of scoliosis-like lateral deformities as symmetry-broken modes. At the molecular scale, analysis of 53 AlphaFold structures shows a modest entropy--curvature correlation in the full dataset (r = 0.405, p = 0.0026) that weakens under pLDDT filtering and length/confidence controls (pLDDT $\ge$ 70: r = -0.077; partial r = 0.104), so the signal remains preliminary.

## Introduction

### The puzzle of spinal curvature under gravity
Living systems do not simply obey gravity; they negotiate with it. While a passive elastic beam clamped at one end and subject to gravity will sag into a monotonic C-shape, biological structures such as plant stems and vertebrate spines adopt complex, robust geometries that defy this passive tendency. The human spine, in particular, maintains a characteristic S-shaped sagittal profile (cervical and lumbar lordosis, thoracic kyphosis) that is critical for bipedal posture and shock absorption~(white_panjabi_spine, 1990). This shape is not merely a reaction to load but an intrinsic, actively maintained counter-curvature.

### Developmental genetic patterning
The blueprint for this geometry is laid down during embryogenesis. The paraxial mesoderm segments into somites, driven by the segmentation clock and oscillating gene expression (e.g., Notch, Wnt, FGF)~(pourquie2011vertebrate, 2011). These segments acquire distinct identities through the expression of HOX and PAX genes, which specify the morphological characteristics of the resulting vertebrae~(wellik2007hox, 2007). However, the mechanism by which these discrete genetic codes are translated into the continuous, mesoscale geometry of the adult spine remains a fundamental open question.

### Hypothesis: Information--Elasticity Coupling and intrinsic geometry
We propose that developmental information prescribes intrinsic strain and curvature in the reference configuration, consistent with incompatible elasticity and morphoelastic rod theory. The IEC framework treats the genetic information field $I(s)$ as a regulator of intrinsic curvature, stiffness, and active moments rather than as an external load. In this view, the spine does not fight gravity; it relaxes toward an intrinsic geometry set by development, with gravity selecting among the admissible equilibria.

### Contribution and overview
In this work, we:
(i) Define the IEC model and an intrinsic-geometry mapping that links genetic information to reference metric and intrinsic curvature fields.
(ii) Implement this framework in a 3D Cosserat rod simulation (using PyElastica) to model the spine under gravitational loading.
(iii) Demonstrate that the interplay between gravity and information selects specific spinal modes, shifting the ground state from a passive C-shape to an active S-shape.
(iv) Show that in information-dominated regimes, this same mechanism can amplify small asymmetries into pathological, scoliosis-like deformities.

## Theory: Information--Cosserat Model of Spinal Countercurvature

We propose that the robust S-shaped geometry of the spine arises not from passive mechanical equilibrium under gravity, but from an active counter-curvature mechanism driven by developmental information. We formalize this using an Information--Elasticity Coupling (IEC) framework, where a scalar information field $I(s)$ modifies the effective geometry and energetics of a Cosserat rod.

### Geometry and parameterization
Consider a slender rod parameterized by arc-length $s \in [0, L]$. The configuration is defined by a centerline curve $\mathbf{r}(s) \in \mathbb{R}^3$ and a director frame $\{\mathbf{d}_1, \mathbf{d}_2, \mathbf{d}_3\}(s)$ describing the orientation of cross-sections. The rod deforms under a gravitational field $\mathbf{g} = -g \hat{\mathbf{e}}_z$. In the absence of biological regulation, such a rod would sag into a C-shape (kyphosis) or buckle.

### Information field from developmental patterning
We introduce a scalar field $I(s)$ representing the spatial distribution of developmental identity along the axis. Rather than an arbitrary function, $I(s)$ is grounded in the well-characterized HOX gene expression boundaries that define spinal regionalization~(wellik2007hox). Specifically:
- Cervical-Thoracic Transition: Defined by the anterior expression limit of Hoxc6 (associated with T1).
- Thoracic-Lumbar Transition: Defined by the onset of Hoxc10 and Hoxd10 expression (associated with L1)~(burke1995hox).

We model $I(s)$ as a superposition of these collinear expression domains. The resultant field peaks in the cervical and lumbar regions where counter-curvature (lordosis) is required to resist the flexion moment of gravity, while the thoracic region (dominated by Hoxc6) retains a primary kyphotic curvature.

### Reference metric and intrinsic curvature (incompatible elasticity)
In an incompatible elasticity framing, information prescribes intrinsic strain and curvature rather than acting as an external load. We encode this by specifying an intrinsic axial stretch $\gamma(s)$ and an intrinsic curvature vector $\boldsymbol{\kappa}^0(s)$ as functions of $I(s)$:
$$
\gamma(s) = 1 + \chi_g \tilde{I}(s), \qquad \boldsymbol{\kappa}^0(s) = \boldsymbol{\kappa}_\mathrm{base} + \chi_\kappa \partial_s \tilde{I}(s).
$$
In 1D, the reference metric is $d\ell_{\mathrm{eff}}^2 = g_{\mathrm{eff}}(s)\,ds^2$ with $g_{\mathrm{eff}}(s) = \gamma(s)^2$.

The energetics of the rod are governed by an IEC-modified elastic energy functional:
$$
\mathcal{E} = \int_0^L \frac{1}{2} B(s) \left\|\boldsymbol{\kappa}(s) - \boldsymbol{\kappa}^0(s) \right\|^2 w(I(s)) \, ds,
$$
where $\boldsymbol{\kappa}(s)$ is the curvature, $\boldsymbol{\kappa}^0(s)$ is the intrinsic curvature prescribed by information, and $w(I) = 1 + \chi_E I(s)$ is a stiffness weighting function. When written in covariant form with $g_{\mathrm{eff}}(s)$, the static minimizer can be interpreted as a geodesic of the reference metric, providing a geometric reading without relying on the GR analogy for derivation.

In this framing, $\boldsymbol{\kappa}^0(s)$ is the primary constitutive field (intrinsic curvature), while the metric $g_{\mathrm{eff}}(s)$ is a geometrized view of the intrinsic stretch $\gamma(s)$. Conversely, a prescribed metric can be reduced to an equivalent intrinsic-curvature description in the 1D rod limit.

### Analogy note (optional)
The metric language admits a loose analogy to GR: information prescribes an intrinsic geometry, and the equilibrium centerline can be viewed as a geodesic of that geometry. This is an interpretation of the variational problem rather than a separate physical postulate.

### Cosserat force and moment balance
The equilibrium configuration is found by minimizing the total potential energy (elastic + gravitational). In the language of Cosserat rod theory, this yields the balance of linear and angular momentum. For a static rod subject to gravity $\mathbf{f}_g = \rho A \mathbf{g}$ and IEC-driven active moments, the equations are:

$$
\begin{aligned}
\mathbf{n}'(s) + \mathbf{f}_g &= \mathbf{0},  \\
\mathbf{m}'(s) + \mathbf{r}'(s) \times \mathbf{n}(s) + \mathbf{m}_{\mathrm{info}}'(s) &= \mathbf{0},
\end{aligned}
$$
where $\mathbf{n}$ is the internal force, $\mathbf{m}$ is the internal moment, and $\mathbf{m}_{\mathrm{info}}$ represents the active couple induced by the information field.

### Mode selection and spinal geometry
The interplay between the gravitational potential (favoring a C-shaped sag) and the IEC energy (favoring an S-shape) can be understood as a mode selection problem. In the linearized planar limit, small deflections $y(s)$ from the vertical satisfy an eigenvalue problem of the form:

$$
\mathcal{L}_{\mathrm{IEC}}[y(s)] = \frac{d^2}{ds^2} \left( B_{\mathrm{eff}}(s) \frac{d^2 y}{ds^2} \right) - \frac{d}{ds} \left( N(s) \frac{dy}{ds} \right) = \lambda_n y_n(s),
$$
where $N(s)$ is the axial tension due to gravity. The information field modifies the operator $\mathcal{L}_{\mathrm{IEC}}$ such that the lowest energy mode $\lambda_0$ shifts from a monotonic C-shape (passive buckling) to a higher-order S-shape (counter-curvature). This spectral shift explains the robustness of the spinal curve: the S-shape becomes the energetic ground state of the information-coupled system.

## Methods

### Deterministic IEC Beam Model
To explore the mode selection mechanism (Eq.~\ref{eq:mode_selection}), we discretize the linearized beam equations using a finite difference scheme on a 1D domain $s \in [0, L]$. The rod is divided into $N=100$ segments. The information field $I(s)$ is mapped to local stiffness $E_i$ and rest curvature $\kappa_{i}$ at each node. We solve the resulting boundary value problem (BVP) using a standard shooting method (or sparse matrix solver for the eigenproblem). This allows rapid exploration of the $(\chi_\kappa, g)$ parameter space to identify regions where S-modes become the ground state.

### 3D Cosserat Rod Implementation (PyElastica)
For full 3D simulations, we utilize PyElastica~(pyelastica_zenodo, 2023; gazzola2018forward, 2018), an open-source Python implementation of Cosserat rod theory. The spine is modeled as a Cosserat rod with the following specifications:

- Discretization: The rod is discretized into $n=50$--$100$ elements.
- IEC Coupling: A custom callback updates the local rest curvature vector $\bm{\kappa}^0(s)$ and bending stiffness matrix $\mathbf{B}(s)$ based on the information field $I(s)$.
- Boundary Conditions: The rod is clamped at the base (sacrum) and free at the top (cranium), simulating a cantilever column under gravity. For specific validation cases, clamped-clamped conditions are used.
- Boundary-condition caveat: This approximation ignores ribcage constraints, pelvis rotation, and active muscle stabilization, but captures global sagittal balance.
- Gravitational Loading: Gravity is applied as a uniform body force $\mathbf{f} = \rho A \mathbf{g}$.
- Damping: To find static equilibrium configurations, external damping ($\nu \sim 0.1$--$1.0$) is applied and the system is integrated until kinetic energy dissipates ($v_{\max} < 10^{-6}$ m/s).

### Parameter Sweeps and Mode Classification
We perform systematic parameter sweeps over coupling strength $\chi_\kappa$ (range $[0, 0.1]$) and gravitational acceleration $g$ (range $[0.01, 1.0]$ $g_{\mathrm{Earth}}$). For each simulation, we compute the equilibrium shape and evaluate:
- Geodesic Deviation $\widehat{D}_{\mathrm{geo}}$ (difference between realized shape and gravity-only geodesic).
- Lateral Deviation $S_{\mathrm{lat}}$ (symmetry breaking in the coronal plane).
- Cobb Angle (clinical proxy for scoliotic curves).

Regimes are classified as gravity-dominated ($\widehat{D}_{\mathrm{geo}} < 0.1$), cooperative ($0.1 < \widehat{D}_{\mathrm{geo}} < 0.3$), or information-dominated ($\widehat{D}_{\mathrm{geo}} > 0.3$).

We define the geodesic deviation explicitly as
$$
D_{\mathrm{geo}}^2 = \int_0^L g_{\mathrm{eff}}(s) \left[\kappa_{\mathrm{info}}(s) - \kappa_{\mathrm{passive}}(s)\right]^2 ds,
$$
with normalized form
$$
\widehat{D}_{\mathrm{geo}} = \frac{D_{\mathrm{geo}}}{\sqrt{\int_0^L g_{\mathrm{eff}}(s)\,\kappa_{\mathrm{passive}}(s)^2\,ds} + \epsilon},
$$
so the order parameter is dimensionless and comparable across simulations.

### Dimensionless control parameters
To generalize across size and material, we interpret the sweep parameters in terms of dimensionless groups:
$$
\Gamma = \frac{\rho A g L^3}{B_0}, \qquad \Lambda = \chi_\kappa \|\partial_s \tilde{I}\|_{\mathrm{rms}} L, \qquad \varepsilon = \text{coronal asymmetry amplitude}.
$$
Here $\Gamma$ measures gravity-to-bending strength, $\Lambda$ sets intrinsic curvature magnitude, and $\varepsilon$ captures left-right asymmetry. Our sweeps over $(g, \chi_\kappa)$ map onto $(\Gamma, \Lambda)$ for interpretation of regime boundaries.

### AlphaFold Protein Structure Analysis
A BCC protein database spans developmental patterning (HOX, PAX), mechanotransduction, segmentation clock components, longevity/stress response, ECM, and transcription factors. Structures are retrieved from the AlphaFold Protein Structure Database via the public API and cached under `results/alphafold/predictions/` (metadata under `results/alphafold/metadata/`) by `scripts/alphafold_reanalysis.py`.

Quality control excluded XML error responses, files smaller than 100 bytes, and files lacking ATOM/HETATM records. For each retained structure, we computed:
- Sequence entropy (Shannon entropy of amino-acid composition; a proxy for sequence heterogeneity rather than developmental information).
- Backbone curvature along the C-alpha trace using a sliding window of 7 residues and a centroid-based curvature proxy (inverse mean radius).
- Flexibility index from bend-angle variability.
- Compactness (radius of gyration and end-to-end distance).
- Mechanical proxies (proline/glycine ratio, instability index, GRAVY).

Curvature was computed on full chains and on pLDDT-filtered windows (pLDDT from CA B-factors; threshold 70). We report raw correlations, length-adjusted partial correlations, and partial correlations controlling for length and mean pLDDT, alongside category-stratified summaries.

## Data

### AlphaFold dataset status (current)
- Downloaded PDBs: 54
- Valid PDBs after QC: 53
- Invalid PDBs: 1 (Klotho)
- Not found in AlphaFold: 16 proteins
- Valid pLDDT-filtered metrics: 52 / 53 proteins

#### Coverage by category
| Category | Targets | Downloaded | Valid | Notes |
|----------|---------|------------|-------|-------|
| ECM | 4 | 2 | 2 | COL1A1, LAMININ_A1 not found |
| HOX | 32 | 22 | 22 | 10 not found |
| LONGEVITY | 5 | 4 | 4 | KLOTHO not found |
| MECHANOSENSITIVE | 8 | 8 | 8 | All retrieved |
| PAX | 5 | 4 | 4 | PAX6 not found |
| SEGMENTATION | 11 | 9 | 9 | NOTCH1, FGF4 not found |
| TRANSCRIPTION | 4 | 4 | 4 | All retrieved |

#### Not found in AlphaFold
COL1A1, FGF4, HOXA11, HOXA2, HOXA3, HOXB7, HOXB8, HOXC9, HOXD11, HOXD13, HOXD3, HOXD9, KLOTHO, LAMININ_A1, NOTCH1, PAX6.

### Data artifacts and locations
- AlphaFold summary report: alphafold_analysis/bcc_analysis_report.md
- AlphaFold data (JSON): alphafold_analysis/bcc_analysis_data.json
- AlphaFold correlation plot: ../alphafold_analysis/figures/entropy_curvature_correlation.png
- AlphaFold correlation plot (pLDDT >= 70): ../alphafold_analysis/figures/entropy_curvature_correlation_plddt70.png
- IEC/beam-surrogate figures: `figures/*.png`
- Manuscript figures: assets/*.png and assets/*.pdf

### Key numbers box (pending full sweeps)
The following metrics require completion once full sweeps are run:
- Microgravity persistence deltas.
- Phase regime anchor points.
- S-curve shape statistics.
- Scoliosis amplification factors.

## Tables

### AlphaFold summary statistics
- Total proteins analyzed: 53
- Mean sequence length: 618.0 aa
- Mean entropy: 4.033 bits
- Mean curvature: 0.1149
- Mean pLDDT (CA): 65.72
- Mean curvature (pLDDT >= 70): 0.1459
- Entropy-curvature correlation (all residues): r = 0.405 (p = 0.0026)
- Entropy-curvature correlation (pLDDT >= 70): r = -0.077 (p = 0.5884)
- Partial correlation (length-adjusted): r = 0.441 (p = 0.0010)
- Partial correlation (length + mean pLDDT, filtered): r = 0.104 (p = 0.4627)

### AlphaFold per-protein metrics

| Protein | Length | Entropy | Mean Curv | Mean Curv (pLDDT>=70) | Mean pLDDT | Frac pLDDT>=70 | Flex Index | Rg | Stiffness | Instability |
|---------|--------|---------|-----------|-----------------------|------------|----------------|------------|----|-----------|------------|
| HOXA4 | 320 | 3.956 | 0.1036 | 0.1578 | 61.82 | 0.24 | 0.358 | 42.33 | 0.016 | 76.11 |
| TBX6 | 295 | 4.127 | 0.1189 | 0.1202 | 72.93 | 0.60 | 0.235 | 24.70 | 0.011 | 48.30 |
| HOXB9 | 250 | 4.086 | 0.1079 | 0.1568 | 63.54 | 0.27 | 0.334 | 39.59 | 0.010 | 58.40 |
| PAX1 | 433 | 3.985 | 0.1069 | 0.1509 | 59.44 | 0.30 | 0.401 | 45.99 | 0.013 | 50.59 |
| HOXA5 | 270 | 4.023 | 0.1062 | 0.1578 | 61.69 | 0.26 | 0.342 | 41.14 | 0.007 | 65.61 |
| TAZ | 400 | 4.055 | 0.1080 | 0.1414 | 59.14 | 0.30 | 0.339 | 41.04 | 0.011 | 59.82 |
| PAX3 | 479 | 4.117 | 0.1194 | 0.1590 | 63.94 | 0.37 | 0.355 | 42.48 | 0.010 | 55.60 |
| HOXA7 | 230 | 4.069 | 0.1083 | 0.1577 | 63.13 | 0.30 | 0.332 | 33.94 | 0.005 | 56.05 |
| RUNX2 | 507 | 3.997 | 0.1024 | 0.1209 | 59.51 | 0.31 | 0.374 | 45.10 | 0.012 | 69.00 |
| TALIN1 | 2541 | 3.989 | 0.1502 | 0.1559 | 75.89 | 0.77 | 0.142 | 57.90 | 0.004 | 37.15 |
| PAX2 | 396 | 4.036 | 0.1151 | 0.1515 | 64.38 | 0.38 | 0.374 | 43.59 | 0.011 | 41.39 |
| HOXD10 | 340 | 4.101 | 0.1027 | 0.1570 | 58.89 | 0.22 | 0.363 | 40.67 | 0.008 | 71.70 |
| VINCULIN | 1134 | 4.037 | 0.1510 | 0.1577 | 86.59 | 0.89 | 0.139 | 36.18 | 0.006 | 42.20 |
| HOXA1 | 335 | 4.093 | 0.0998 | 0.1588 | 57.80 | 0.22 | 0.382 | 44.32 | 0.007 | 59.38 |
| SIRT1 | 747 | 4.086 | 0.1158 | 0.1396 | 65.02 | 0.50 | 0.345 | 40.25 | 0.009 | 53.88 |
| HOXD12 | 217 | 3.836 | 0.1008 | 0.0000 | 52.07 | 0.00 | 0.294 | 43.57 | 0.013 | 60.19 |
| HOXC8 | 242 | 4.105 | 0.1145 | 0.1592 | 64.14 | 0.30 | 0.303 | 34.35 | 0.006 | 63.34 |
| HES1 | 280 | 4.032 | 0.1244 | 0.1563 | 68.62 | 0.47 | 0.283 | 40.42 | 0.013 | 52.33 |
| FIBRONECTIN | 2477 | 4.131 | 0.1114 | 0.1106 | 69.65 | 0.61 | 0.307 | 52.46 | 0.008 | 40.12 |
| HOXA10 | 410 | 3.922 | 0.0989 | 0.1534 | 59.12 | 0.22 | 0.383 | 45.63 | 0.012 | 73.58 |
| HOXD8 | 290 | 4.054 | 0.1112 | 0.1553 | 61.71 | 0.29 | 0.315 | 38.03 | 0.013 | 70.57 |
| HOXC10 | 342 | 4.065 | 0.1003 | 0.1570 | 59.50 | 0.22 | 0.390 | 42.91 | 0.009 | 57.74 |
| HOXC11 | 304 | 4.076 | 0.1029 | 0.1571 | 59.39 | 0.24 | 0.386 | 38.43 | 0.009 | 60.04 |
| HES7 | 225 | 3.760 | 0.1258 | 0.1593 | 73.28 | 0.54 | 0.236 | 37.82 | 0.019 | 76.22 |
| INTEGRIN_B1 | 798 | 4.162 | 0.1332 | 0.1346 | 85.87 | 0.89 | 0.223 | 46.63 | 0.004 | 41.12 |
| YAP1 | 504 | 3.994 | 0.1110 | 0.1405 | 57.40 | 0.26 | 0.380 | 44.88 | 0.012 | 65.51 |
| AMPK | 559 | 4.184 | 0.1312 | 0.1393 | 79.55 | 0.76 | 0.222 | 31.29 | 0.005 | 49.43 |
| FOXO3 | 673 | 3.974 | 0.0961 | 0.1576 | 50.66 | 0.13 | 0.513 | 55.01 | 0.008 | 66.77 |
| DLL3 | 587 | 3.880 | 0.1233 | 0.1253 | 67.62 | 0.57 | 0.254 | 37.68 | 0.011 | 55.26 |
| WNT3A | 352 | 4.198 | 0.1353 | 0.1366 | 88.32 | 0.88 | 0.212 | 24.81 | 0.005 | 50.65 |
| SOX9 | 509 | 4.051 | 0.1025 | 0.1520 | 55.97 | 0.16 | 0.399 | 46.59 | 0.014 | 78.58 |
| HOXD1 | 328 | 3.954 | 0.1025 | 0.1589 | 59.56 | 0.24 | 0.398 | 46.72 | 0.011 | 66.82 |
| MESP2 | 397 | 3.825 | 0.1014 | 0.1557 | 54.17 | 0.18 | 0.336 | 43.54 | 0.012 | 73.92 |
| DLL1 | 247 | 4.089 | 0.1215 | 0.1202 | 86.16 | 0.81 | 0.250 | 31.63 | 0.007 | 43.96 |
| HOXD4 | 255 | 4.073 | 0.1106 | 0.1578 | 64.40 | 0.30 | 0.312 | 36.73 | 0.013 | 76.31 |
| FGF8 | 233 | 4.101 | 0.1264 | 0.1298 | 81.05 | 0.66 | 0.222 | 29.41 | 0.005 | 47.80 |
| HOXB1 | 301 | 3.965 | 0.1023 | 0.1587 | 60.65 | 0.24 | 0.399 | 41.58 | 0.013 | 69.02 |
| PAX9 | 341 | 4.068 | 0.1118 | 0.1510 | 63.44 | 0.37 | 0.401 | 41.95 | 0.010 | 50.19 |
| HOXC4 | 264 | 4.053 | 0.1094 | 0.1577 | 63.83 | 0.29 | 0.341 | 37.41 | 0.013 | 81.10 |
| WNT5A | 365 | 4.207 | 0.1383 | 0.1386 | 89.56 | 0.88 | 0.206 | 25.41 | 0.002 | 38.85 |
| HOXB2 | 356 | 3.906 | 0.1020 | 0.1570 | 60.15 | 0.26 | 0.400 | 45.16 | 0.015 | 85.76 |
| HOXC6 | 153 | 4.036 | 0.1256 | 0.1578 | 70.26 | 0.45 | 0.261 | 26.21 | 0.001 | 65.58 |
| COL2A1 | 1487 | 3.530 | 0.0965 | 0.1307 | 52.12 | 0.19 | 0.409 | 61.26 | 0.018 | 25.21 |
| PGC1A | 671 | 4.028 | 0.1002 | 0.1435 | 53.59 | 0.24 | 0.539 | 49.34 | 0.007 | 78.05 |
| NOTCH2 | 2471 | 4.150 | 0.1289 | 0.1533 | 59.40 | 0.35 | 0.325 | 58.07 | 0.007 | 45.58 |
| PIEZO1 | 2521 | 4.121 | 0.1390 | 0.1537 | 72.05 | 0.67 | 0.276 | 64.25 | 0.006 | 49.43 |
| HOXB6 | 224 | 4.084 | 0.1116 | 0.1577 | 64.61 | 0.32 | 0.342 | 34.50 | 0.008 | 74.74 |
| NOTCH3 | 2321 | 4.000 | 0.1291 | 0.1522 | 61.42 | 0.40 | 0.329 | 57.16 | 0.011 | 54.79 |
| TRPV4 | 871 | 4.162 | 0.1371 | 0.1532 | 71.60 | 0.67 | 0.245 | 42.41 | 0.006 | 43.23 |
| HOXB4 | 251 | 3.976 | 0.1120 | 0.1534 | 66.18 | 0.37 | 0.262 | 36.80 | 0.018 | 90.11 |
| PIEZO2 | 709 | 4.134 | 0.1336 | 0.1421 | 79.44 | 0.79 | 0.254 | 48.56 | 0.004 | 41.35 |
| HOXB5 | 269 | 4.005 | 0.1058 | 0.1577 | 61.11 | 0.26 | 0.388 | 41.73 | 0.007 | 62.08 |
| HOXA9 | 272 | 4.118 | 0.1046 | 0.1570 | 61.61 | 0.24 | 0.364 | 36.80 | 0.009 | 46.63 |

### Key numbers box (template)

Microgravity persistence:
- At g = 1.0: Dhat_geo = 6.54, E_total = 0.994
- At g = 0.01: Dhat_geo = 654, E_total = 1.01
- E_total reduction: -1.79% (g=1.0→0.01)
- Dhat_geo persistence ratio: 100

Phase diagram regimes (example anchors):
- Low Dhat_geo point: chi_kappa=0, g=0.01, Dhat_geo=0
- High Dhat_geo point: chi_kappa=0.1, g=0.01, Dhat_geo=1.09e+03

Mode transition (baseline gravity):
- First S-like (>=1 inflection) chi_kappa: 0.02

Microgravity persistence:
- At g = 1.0: Dhat_geo = 6.54, E_total = 0.994
- At g = 0.01: Dhat_geo = 654, E_total = 1.01
- E_total reduction: -1.79% (g=1.0→0.01)
- Dhat_geo persistence ratio: 100

Phase diagram regimes (example anchors):
- Low Dhat_geo point: chi_kappa=0, g=0.01, Dhat_geo=0
- High Dhat_geo point: chi_kappa=0.1, g=0.01, Dhat_geo=1.09e+03

Mode transition (baseline gravity):
- First S-like (>=1 inflection) chi_kappa: 0.02

Microgravity persistence:
- At g = 1.0: Dhat_geo = 6.54, E_total = 0.994
- At g = 0.01: Dhat_geo = 654, E_total = 1.01
- E_total reduction: -1.79% (g=1.0→0.01)
- Dhat_geo persistence ratio: 100

Phase diagram regimes (example anchors):
- Low Dhat_geo point: chi_kappa=0, g=0.01, Dhat_geo=0
- High Dhat_geo point: chi_kappa=0.1, g=0.01, Dhat_geo=1.09e+03

Mode transition (baseline gravity):
- First S-like (>=1 inflection) chi_kappa: 0.02

Microgravity persistence:
- At g = 1.0: Dhat_geo = 6.54, E_total = 0.994
- At g = 0.01: Dhat_geo = 654, E_total = 1.01
- E_total reduction: -1.79% (g=1.0→0.01)
- Dhat_geo persistence ratio: 100

Phase diagram regimes (example anchors):
- Low Dhat_geo point: chi_kappa=0, g=0.01, Dhat_geo=0
- High Dhat_geo point: chi_kappa=0.1, g=0.01, Dhat_geo=1.09e+03

Mode transition (baseline gravity):
- First S-like (>=1 inflection) chi_kappa: 0.02

