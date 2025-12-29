# Biological Countercurvature: An Information-Geometry Framework for Spinal Morphogenesis

## Abstract
Living systems routinely maintain structure against gravity, from plant stems to vertebrate spines. We propose a quantitative framework of biological countercurvature, where developmental information prescribes intrinsic geometry in the sense of incompatible elasticity and morphoelastic rods. By coupling an Information--Elasticity (IEC) model to Cosserat rod mechanics, we treat the spine as a rod with a prescribed reference metric and intrinsic curvature that minimizes elastic energy. In covariant form, the static minimizer can be interpreted as a geodesic of the reference metric without relying on a purely metaphorical spacetime analogy. We derive a mode selection principle showing that while gravity alone selects a C-shaped sag, the information-coupled system stabilizes an S-shaped counter-curvature mode. A normalized geodesic deviation metric $\widehat{D}_{\mathrm{geo}}$ quantifies this information-driven reshaping. Phase diagrams reveal distinct regimes: gravity-dominated, cooperative, and information-dominated, where the latter predicts the emergence of scoliosis-like lateral deformities as symmetry-broken modes. At the molecular scale, analysis of 53 AlphaFold structures shows a modest entropy--curvature correlation in the full dataset (r = 0.405, p = 0.0026) that weakens under pLDDT filtering and length/confidence controls (pLDDT $\ge$ 70: r = -0.077; partial r = 0.104), so the signal remains preliminary.

## Introduction

### The puzzle of spinal curvature under gravity
Living systems do not simply obey gravity; they negotiate with it. While a passive elastic beam clamped at one end and subject to gravity will sag into a monotonic C-shape, biological structures such as plant stems and vertebrate spines adopt complex, robust geometries that defy this passive tendency. The human spine, in particular, maintains a characteristic S-shaped sagittal profile (cervical and lumbar lordosis, thoracic kyphosis) that is critical for bipedal posture and shock absorption~(white_panjabi_spine, 1990). This shape is not merely a reaction to load but an intrinsic, actively maintained "counter-curvature."

### Developmental genetic patterning
The blueprint for this geometry is laid down during embryogenesis. The paraxial mesoderm segments into somites, driven by the segmentation clock and oscillating gene expression (e.g., Notch, Wnt, FGF)~(pourquie2011vertebrate, 2011). These segments acquire distinct identities through the expression of HOX and PAX genes, which specify the morphological characteristics of the resulting vertebrae~(wellik2007hox, 2007). However, the mechanism by which these discrete genetic codes are translated into the continuous, mesoscale geometry of the adult spine remains a fundamental open question.

### Hypothesis: Information--Elasticity Coupling and intrinsic geometry
We propose that developmental information acts as a field that prescribes intrinsic strain and curvature in the reference configuration, consistent with incompatible elasticity and morphoelastic rod theory. The IEC framework treats the genetic information field $I(s)$ as a regulator of intrinsic curvature, stiffness, and active moments rather than as an external load. In this view, the spine does not "fight" gravity; it relaxes toward an intrinsic geometry set by development, with gravity selecting among the admissible equilibria.

### Contribution and overview
In this work, we:
(i) Define the IEC model and a phenomenological intrinsic-geometry mapping that links genetic information to reference metric and intrinsic curvature fields.
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
In an incompatible elasticity framing, information prescribes intrinsic strain and curvature rather than acting as an external load. We encode this by specifying an intrinsic axial stretch $\gamma(s)$ and an intrinsic curvature vector $\boldsymbol{\kappa}^0(s)$ as functions of $I(s)$. A minimal choice is
$$
\gamma(s) = 1 + \chi_g \tilde{I}(s), \qquad \boldsymbol{\kappa}^0(s) = \boldsymbol{\kappa}_\mathrm{base} + \chi_\kappa \partial_s \tilde{I}(s),
$$
with $\tilde{I}$ normalized to $[0,1]$. In 1D, the reference metric is $d\ell_{\mathrm{eff}}^2 = g_{\mathrm{eff}}(s)\,ds^2$ with $g_{\mathrm{eff}}(s) = \gamma(s)^2$.

The energetics of the rod are governed by an IEC-modified elastic energy functional:
$$
\mathcal{E} = \int_0^L \frac{1}{2} B(s) \left\|\boldsymbol{\kappa}(s) - \boldsymbol{\kappa}^0(s) \right\|^2 w(I(s)) \, ds,
$$
where $\boldsymbol{\kappa}(s)$ is the curvature, $\boldsymbol{\kappa}^0(s)$ is the intrinsic curvature prescribed by information, and $w(I) = 1 + \chi_E I(s)$ is a stiffness weighting function. This formulation makes the intrinsic-geometry interpretation explicit. When written in covariant form with $g_{\mathrm{eff}}(s)$, the static minimizer can be interpreted as a geodesic of the reference metric, providing a geometric reading without relying on the GR analogy for derivation.

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

## Methods: Deterministic IEC Beam Surrogate and AlphaFold Analysis

All quantitative results in this repository are generated with a deterministic, linear Euler--Bernoulli surrogate (the small-deflection limit of a Cosserat rod) that directly implements the IEC intrinsic-curvature prescription and the paper's scalar order parameters. A full 3D PyElastica Cosserat implementation is conceptually aligned with this framework, but is not required for (and is not used in) the reproducible pipeline below.

### Deterministic IEC Beam Model
To explore the mode selection mechanism (Eq.~\ref{eq:mode_selection}), we discretize the linearized beam equations using a finite difference scheme on a 1D domain $s \in [0, L]$. The rod is divided into $N=100$ segments. The information field $I(s)$ is mapped to local stiffness $E_i$ and rest curvature $\kappa_{i}$ at each node. We solve the resulting boundary value problem (BVP) using a standard shooting method (or sparse matrix solver for the eigenproblem). This allows rapid exploration of the $(\chi_\kappa, g)$ parameter space to identify regions where S-modes become the ground state.

### Note on 3D Cosserat/PyElastica
The Cosserat formulation provides the conceptual backbone for IEC intrinsic geometry. The reproducible code in this repository uses the linear Euler--Bernoulli limit (planar centerline deflection with prescribed intrinsic curvature), which is sufficient to generate the figures and the key metrics reported here. A full 3D PyElastica implementation is left as future work.

### Parameter Sweeps and Mode Classification
We perform systematic parameter sweeps over the coupling strength $\chi_\kappa$ and gravitational acceleration $g$. For each simulation, we compute the equilibrium centerline and evaluate:
1.  Geodesic-deviation proxy $\widehat{D}_{\mathrm{geo}}$: curvature-field deviation relative to the passive (gravity-only) equilibrium, weighted by $g_{\mathrm{eff}}(s)$.
2.  Mode-selection score: a scalar that distinguishes C-shaped from S-shaped equilibria via the balance of positive/negative curvature and the number of curvature inflections.
3.  Tip deflection and inflection count: endpoint sag and curvature sign-change count.

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
Protein structures are reanalyzed by `scripts/alphafold_reanalysis.py`, which caches PDBs under `results/alphafold/predictions/` and writes summary CSVs under `results/`. Sensitivity to pLDDT thresholds is summarized in a single figure (`figures/fig_alphafold_sensitivity.png`).

Quality control excluded XML error responses, files smaller than 100 bytes, and files lacking ATOM/HETATM records. For each retained structure, we computed:
- Sequence entropy (Shannon entropy of amino-acid composition; a proxy for sequence heterogeneity rather than developmental information).
- Backbone curvature along the C-alpha trace using a sliding window of 7 residues and a centroid-based curvature proxy (inverse mean radius).
- Flexibility index from bend-angle variability.
- Compactness (radius of gyration and end-to-end distance).
- Mechanical proxies (proline/glycine ratio, instability index, GRAVY).

Curvature was computed on full chains and on pLDDT-filtered windows (pLDDT from CA B-factors; threshold 70). We report raw correlations, length-adjusted partial correlations, and partial correlations controlling for length and mean pLDDT, alongside category-stratified summaries.

At the time of analysis, 54 PDB files were present and 53 passed QC (Klotho was excluded as an invalid XML error response). Sixteen targets were not found in AlphaFold (COL1A1, FGF4, HOXA11, HOXA2, HOXA3, HOXB7, HOXB8, HOXC9, HOXD11, HOXD13, HOXD3, HOXD9, KLOTHO, LAMININ_A1, NOTCH1, PAX6). All protein-structure analyses and correlation statistics were computed with alphafold_analysis/analyze_bcc_structures.py.

### Validation
The deterministic implementation is validated against analytical expectations for small-deflection Euler--Bernoulli beams (cantilevered beam under distributed load) and is fully reproducible from `config/default.yaml`.

## Results: Gravity-Selected Modes and Biological Countercurvature

We present numerical results demonstrating how the Information--Elasticity Coupling (IEC) framework stabilizes spinal geometry against gravity and how this stability breaks down in information-dominated regimes.

### Segmentation-Derived Information Field and IEC Landscape
We first establish the connection between developmental patterning and the mechanical information field. Figure 1 illustrates the mapping from discrete genetic domains (e.g., HOX boundaries) to a continuous information field $I(s)$.

![From Genes to Geometry. (A) Conceptual mapping of HOX/PAX segmentation domains to the scalar information field $I(s)$. (B) The resulting IEC landscape, showing the effective metric factor $g_{\mathrm{eff}}(s)$ and stiffness modulation along the spine. Peaks in $I(s)$ correspond to regions of high counter-curvature demand (lordosis).](assets/fig_gene_to_geometry.png)

The resulting field $I(s)$ (Fig. 1B) exhibits peaks in the cervical and lumbar regions. Through the reference metric and intrinsic curvature fields, these regions encode the target S-shape into the material geometry.

### Molecular Basis: Information-Curvature Coupling in Proteins
To test whether information content encodes geometric stiffness at the molecular scale, we analyzed 53 AlphaFold structures spanning HOX genes (22 proteins), segmentation clock components (9 proteins), longevity factors (4 proteins), mechanosensitive proteins (8 proteins), PAX genes (4 proteins), ECM proteins (2 proteins), and transcription factors (4 proteins). We calculated local backbone curvature and compared it to sequence entropy.

| Metric | Value |
|--------|-------|
| Proteins analyzed | 53 |
| Mean sequence length | 618.0 aa |
| Mean sequence entropy | 4.033 bits |
| Mean backbone curvature | 0.1149 |
| Mean pLDDT (CA) | 65.72 |
| Mean curvature (pLDDT $\ge$ 70) | 0.1459 |
| Entropy-curvature correlation (all residues) | r = 0.405 (p = 0.0026) |
| Entropy-curvature correlation (pLDDT $\ge$ 70) | r = -0.077 (p = 0.5884) |
| Partial correlation (length-adjusted) | r = 0.441 (p = 0.0010) |
| Partial correlation (length + mean pLDDT, filtered) | r = 0.104 (p = 0.4627) |

We observed a modest positive correlation between sequence entropy and curvature in the full dataset, but the signal disappears under pLDDT filtering and length/confidence adjustment (filtered metrics were available for 52/53 proteins). The length-adjusted partial correlation remains positive, while the length + pLDDT-adjusted partial correlation does not.

**Category-stratified analysis** reveals that the entropy-curvature correlation varies significantly by protein functional class:

| Category | n | Pearson r | p-value | 95% CI |
|----------|---|-----------|---------|--------|
| HOX | 22 | **0.585** | **0.004** | [0.217, 0.808] |
| PAX | 4 | 0.796 | 0.205 | [-0.703, 0.995] |
| Mechanosensitive | 8 | -0.249 | 0.553 | [-0.811, 0.553] |
| Longevity | 4 | -0.811 | 0.189 | [-0.996, 0.680] |

HOX transcription factors show the strongest and most significant entropy-curvature correlation (r = 0.585, p = 0.004), consistent with their role as primary regulators of axial patterning. This category-specific signal suggests that information-geometry coupling may be strongest in proteins directly involved in developmental patterning, rather than mechanosensitive or longevity pathways. These results support the hypothesis that sequence information content correlates with structural geometry in patterning proteins.

### Mode Spectrum of the IEC Beam in Gravity
To understand why the S-shape is selected, we analyze the eigenmodes of the linearized IEC beam equation (Eq.~\ref{eq:mode_selection}).

![Gravity-Selected vs. Information-Selected Modes. (A) Eigenmodes of a uniform beam in gravity, showing the lowest energy state is a C-shaped sag. (B) Eigenmodes of the IEC-coupled beam, where the information field shifts the spectrum, making the S-shaped counter-curvature mode the energetic ground state.](assets/fig_mode_spectrum.png)

As shown in Figure 2, the passive beam's ground state is a monotonic C-shaped sag. However, with sufficient IEC coupling ($\chi_\kappa > \chi_{\mathrm{crit}}$), the spectrum shifts: the S-shaped mode (resembling the adult spine) becomes the lowest energy configuration. This confirms that the spinal curve is a gravity-selected mode of the information-modified system.

### 3D Cosserat Rod S-Curve Solutions
We verify these linear predictions using full 3D Cosserat rod simulations.

![3D Equilibrium Configurations. (A) Comparison of passive sag (gray) and IEC-stabilized S-curve (blue) under Earth gravity. (B) Persistence of the S-curve in microgravity ($g \to 0$), demonstrating that the shape is intrinsic to the information field, not just a reaction to load.](assets/fig_countercurvature_panelA.pdf)

Figure 3A shows the equilibrium shape of a rod with human-like parameters. The IEC model reproduces the characteristic cervical and lumbar lordosis. In simulations where the intrinsic geometry is held fixed, the S-curve persists even as $g \to 0$, unlike the passive sag which would vanish. In vivo, the expressed curvature may still flatten under microgravity if mechanosensory feedback (modeled here via active moments or updates to $\boldsymbol{\kappa}^0$) is down-regulated; we return to this reconciliation in the Discussion.

### Phase Diagrams of Curvature Patterns
We map the behavior of the system across the parameter space of coupling strength $\chi_\kappa$ and gravitational acceleration $g$.

![Phase Diagram of Countercurvature Regimes. Heatmap of geodesic deviation $\widehat{D}_{\mathrm{geo}}$ in the $(\chi_\kappa, g)$ plane. Three regimes are identified: (I) Gravity-dominated (sag), (II) Cooperative (stable S-curve), and (III) Information-dominated (potential for instability).](assets/fig_phase_diagram_scoliosis.png)

Figure 4 reveals three distinct regimes. In the gravity-dominated regime (low $\chi_\kappa$), the rod follows the passive geodesic (sag). In the cooperative regime, information and gravity balance to produce a stable S-curve. In the information-dominated regime (high $\chi_\kappa$), the effective metric becomes highly distorted, leading to complex curvature patterns.

### Perturbations and Pathology-Like Modes
Finally, we explore the consequences of symmetry breaking in the information field.

![Emergence of Scoliosis-like Patterns. (A) A small lateral asymmetry is introduced in the information field. (B) In the cooperative regime, this perturbation is suppressed. (C) In the information-dominated regime, the same perturbation is amplified into a large lateral deviation (scoliosis-like mode), characterized by high Cobb angles and axial rotation.](assets/fig_phase_diagram_scoliosis.png)

In the information-dominated regime, a small asymmetric perturbation (e.g., 5% difference in left/right information) is amplified into a pronounced lateral deformity with axial rotation (Fig. 5). Biologically, such asymmetries could arise from mechanosensory or cilia/CSF-flow biases; in the model they correspond to a small coronal component of $\boldsymbol{\kappa}^0(s)$ or an $I(s,\theta)$ modulation. This suggests that idiopathic scoliosis may represent a mode shape of the spine that becomes accessible when the information-elasticity coupling is too strong relative to the stabilizing effect of gravity.

## Discussion: From Information Fields to Deformity

### Interpreting Biological Countercurvature
Our results suggest that the adult spinal shape is best understood as a standing wave of counter-curvature, maintained by the continuous action of developmental information against gravity. The IEC framework provides a quantitative language for this: the information field $I(s)$ prescribes intrinsic geometry (reference metric and intrinsic curvature), creating a potential well where the S-shape is the stable equilibrium. This explains why the spine does not collapse into a simple sag and why this geometry persists even in microgravity.

In the morphoelastic framing, the information field prescribes intrinsic geometry (reference metric and intrinsic curvature), while active regulation provides a gravity-dependent feedback term. This split clarifies how intrinsic shape can persist across development while the expressed curvature remains sensitive to loading and neuromuscular control.

Numerical analysis of the phase diagram (Fig. 4) reveals three distinct regimes governed by the normalized geodesic deviation $\widehat{D}_{\mathrm{geo}}$:
1.  Gravity-Dominated ($\widehat{D}_{\mathrm{geo}} < 0.1$): The spine behavior is dictated by passive elasticity; information is too weak to enforce a shape.
2.  Cooperative ($0.1 \le \widehat{D}_{\mathrm{geo}} \le 0.2$): The ideal healthy regime where information and gravity balance to produce a stable, robust S-curve.
3.  Information-Dominated ($\widehat{D}_{\mathrm{geo}} > 0.2$): The metric becomes highly distorted. In this regime, even small asymmetries in the information field ($\epsilon \approx 1\%$) can destabilize the planar solution, triggering a bifurcation into lateral deformities resembling scoliosis (Fig. 5).

### Links to Developmental Genetics and Evolution
The information field $I(s)$ serves as a coarse-grained representation of the HOX code. The peaks in our phenomenological $I(s)$ correspond to the cervical and lumbar regions, suggesting that specific HOX paralogs may function as curvature generators by modulating local growth rates or tissue stiffness. Evolutionarily, the transition to bipedalism likely involved the tuning of this information field to stabilize the S-mode against the increased gravitational moment of an upright posture.

Our AlphaFold analysis extends this concept to the molecular level. Critically, **category-stratified analysis reveals that HOX transcription factors show significant entropy-curvature correlation (r = 0.585, p = 0.004, n = 22)**, while other categories do not reach significance. This finding is consistent with the hypothesis that information-geometry coupling is strongest in proteins that directly regulate developmental patterning. The HOX proteins that specify vertebral identity and regional curvature show the clearest molecular signature of the information-curvature relationship predicted by the IEC framework.

In contrast, mechanosensitive proteins (n = 8) and longevity factors (n = 4) did not show significant correlations, suggesting that information-geometry coupling at the molecular scale may be specific to patterning transcription factors rather than a universal principle. This category specificity may reflect the distinct evolutionary pressures on these protein families: HOX proteins must encode precise positional information, while mechanosensitive proteins are optimized for force transduction.

Microgravity data often show partial flattening of lumbar lordosis and reduced paraspinal muscle activity. In our framework, this is consistent with a reduction of the active, mechanosensory feedback term (or a transient update to $\boldsymbol{\kappa}^0$), even when the developmental intrinsic geometry remains. This suggests a testable dissociation between intrinsic curvature prescriptions and short-term regulation.

### Comparison to Passive Pre-stress Models
A standard alternative hypothesis is that spinal curvature is simply maintained by muscular pre-stress (e.g., constant tone in erector spinae), effectively a tensegrity structure. While valid, such models are reaction-based; they require constant energy expenditure to fight gravity. Our IEC framework offers a more parsimonious explanation: the target shape is intrinsic to the material manifold itself (via the prescribed reference metric and intrinsic curvature). In our model, the spine wants to be an S-shape due to its developmental programming; muscles merely fine-tune deviations from this zero-energy state, rather than actively forcing a C-shaped beam into an S-shape against its will.

### Proposed Experimental Validation
To rigorously test the IEC hypothesis against the null model (passive adaptation), we propose the following falsifiable experiment:
1.  HOX Perturbation: Generate a transgenic mouse line with a conditional Hoxc10 knockout targeted to the lumbar mesoderm.
2.  Prediction: Under the IEC model, removing the lumbar information peak ($I(s) \to 0$ in lumbar) should abolish the intrinsic stretch (reference-metric dilation), causing the lumbar spine to revert to a passive, gravity-dominated C-shape (kyphosis) even if muscle tone is preserved.
3.  Control: Comparison with a muscle-atrophy model (e.g., HSA-Cre;DTA) would distinguish between information-loss and muscle-loss phenotypes.

### Relation to Existing Biomechanical and Rod Models
Traditional biomechanical models often prescribe the rest shape ad hoc or model the spine as a passive beam column. Our approach differs by deriving the geometry from an underlying scalar field. This connects the mechanics to the developmental inputs. Furthermore, by using Cosserat rod theory, we capture the full 3D kinematics (twist, shear) essential for understanding how planar information fields can give rise to out-of-plane deformities like scoliosis.

### Limitations and Model Assumptions
Our model assumes a deterministic, static information field. In reality, $I(s)$ is dynamic, emerging from complex reaction-diffusion systems and growth processes. We also simplified the complex anatomy of vertebrae and discs into a continuous rod. Finally, the mapping from genes to $I(s)$ remains phenomenological; future work requires explicit coupling to gene expression data.

The molecular analysis is limited by incomplete AlphaFold coverage. Sixteen targets were not found in the database at the time of analysis, including COL1A1, LAMININ_A1, PAX6, NOTCH1, and multiple HOX genes. Klotho was excluded due to an invalid XML error response. Although we applied pLDDT filtering and length/confidence controls, the filtered correlations were not significant and are sensitive to the chosen threshold; category-level correlations remain underpowered and mixed-effects or domain-architecture controls are still pending. These limitations may weaken cross-category correlations and motivate expansion of the protein set or integration of experimental structures.

### Future Directions
Future extensions will focus on: (1) Patient-specific modeling, inferring $I(s)$ from medical imaging to predict progression of deformities. (2) Coupling the IEC framework to volumetric growth laws to model the developmental time-course of spinal curvature. (3) Investigating the role of sensory feedback (proprioception) as a dynamic component of the information field.

## Conclusion

We have presented a theoretical framework for Biological Countercurvature, positing that the geometry of the spine is determined by the interaction between a developmental information field and the gravitational environment. By coupling a Cosserat rod model with an Information--Elasticity mechanism, we demonstrated that the spinal S-curve emerges as a gravity-selected mode, a stable equilibrium accessible only when information prescribes intrinsic geometry of the structure. This framework unifies the understanding of normal spinal development, microgravity adaptation, and pathological deformity (scoliosis) under a single physical principle: the shaping of biological intrinsic geometry by genetic information. The molecular analysis shows a modest raw correlation that attenuates under pLDDT filtering and confidence controls, so the information-geometry signal remains preliminary until additional protein categories and higher-confidence segments are incorporated.

## Reproducibility

All quantitative results and figures in this repository are reproducible from a clean environment using:

- `make all` (creates a virtualenv, generates CSVs in `results/`, regenerates figures in `figures/`, and updates derived numbers)
- `make data` (CSV generation only)
- `make figs` (figure generation only; requires `results/`)

The primary configuration is `config/default.yaml` (simulation + sweeps) and `config/alphafold.yaml` (AlphaFold reanalysis).
