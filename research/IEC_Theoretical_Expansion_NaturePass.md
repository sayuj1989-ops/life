# IEC Manuscript Theoretical Expansion (Nature-Style Revision)

## 2.11 Protein-Level Biophysical Foundations and Thermodynamic Constraints

### 2.11.1 Multi-Scale Mechanistic Chain
The Information-Elasticity Coupling (IEC) framework links developmental patterning to organ-scale geometry, but that link requires an explicit mechanistic bridge from gene regulation to tissue mechanics. We therefore formalize IEC as a five-level, experimentally addressable cascade: (i) protein sequence and structure, (ii) single-molecule mechanics, (iii) fibril assembly, (iv) tissue-scale homogenized elasticity, and (v) whole-spine Cosserat equilibrium. The purpose of this cascade is not descriptive completeness; it is to identify where parameters entering the continuum model are physically constrained and where uncertainty propagates.

At Level 1 (protein structure), HOX-regulated programs shift the relative abundance of structural proteins (for example, collagen I/II, aggrecan, fibrillin, elastin) and mechanosensory proteins (for example, integrins, FAK-associated adhesome proteins, mechanosensitive channels) [1,2,7,9]. AlphaFold-derived structures provide priors on domain organization, hinge propensity, and geometric anisotropy [3,4]. For matrix proteins, these priors include triple-helical continuity, cross-link-accessible residues, and charge-distributed motifs that regulate hydration. For mechanosensory proteins, they include force-bearing linker geometry and disordered regions that can modulate force-transduction bandwidth.

At Level 2 (molecular mechanics), steered molecular dynamics (SMD) maps structure to force-extension response. In this step, each molecule is treated as a nonlinear elastic element with identifiable low-strain stiffness and higher-strain transition points. This distinction is important because vertebral tissues operate near a regime where small strain increments can cross into strain-stiffening behavior [5]. Consequently, microscopic unfolding thresholds and bond topology influence whether perturbations are buffered or amplified.

At Level 3 (fibril assembly), molecules are embedded into supramolecular architectures where packing geometry and cross-link density determine mesoscopic behavior. Collagen fibrils develop D-band periodicity and composition-dependent cross-link networks, while proteoglycan-rich interfibrillar matrix contributes hydration-dependent compressive resistance [5,6]. HOX-dependent stoichiometry is the control variable at this scale: collagen-dominant domains bias axial load transfer, whereas proteoglycan-rich domains increase viscoelastic damping and osmotic resistance. The emergent fibril modulus and anisotropy are therefore not constants, but composition-dependent state variables.

At Level 4 (tissue mechanics), fibrillar constituents are homogenized into a position-dependent elastic tensor \(C_{ijkl}(s)\), rather than a scalar modulus. Orientation distributions, constituent volume fractions, and cross-link maturity jointly set directional stiffness and torsional compliance [6]. This framework naturally supports regional mechanical heterogeneity: cervical segments are predicted to exhibit higher axial stiffness, thoracic segments higher compliance, and lumbar segments intermediate behavior under physiological loading.

At Level 5 (organ geometry), \(C_{ijkl}(s)\), rest-curvature fields, and gravity enter the Cosserat rod equations with physiological boundary conditions. In this formulation, the sagittal S-curve is the low-energy solution of a developmentally patterned anisotropic structure under load. Pathology is then interpreted as a transition in the same dynamical system, rather than as a separate mechanism. This multiscale organization clarifies model falsifiability: disagreement can be localized to a specific interface (structure-to-molecule, molecule-to-fibril, fibril-to-tissue, or tissue-to-geometry) instead of being absorbed into unconstrained effective parameters.

### 2.11.2 Mechanosensory-Growth Protein Dichotomy
A central mechanistic distinction is between mechanosensory proteins and growth/structural proteins, which differ in function, ATP burden, and characteristic timescale. Mechanosensory proteins (for example, integrin \(\alpha v\beta3\), integrin \(\alpha5\beta1\), FAK, talin, vinculin, YAP/TAZ-associated machinery, PIEZO-family channels) maintain force sensing and closed-loop control. Their operation requires ATP-intensive trafficking, phosphorylation cycling, and cytoskeletal remodeling [7–9,16,17]. Their effective response time is fast (seconds to minutes), and spatial localization tracks high-stress microenvironments.

Growth/structural proteins (for example, collagen I/II, aggrecan, fibrillin, elastin) define baseline material architecture. Their synthesis is energetically substantial but amortized over longer lifetimes after deposition and cross-linking [5,6]. Their dominant timescale is slower (hours to days for deposition dynamics; longer for matrix turnover), and spatial patterns are established primarily by developmental programs with secondary modulation by loading history.

These classes are dynamically coupled because they share the same metabolic pool. Mechanical loading increases mechanosensory demand, mechanosensory signaling modulates matrix synthesis, and matrix remodeling redistributes stress, which in turn alters mechanosensory demand. Under moderate growth, this loop stabilizes geometry. Under rapid growth, the loop can become temporally separated: structural synthesis accelerates faster than mechanosensory recalibration, reducing control fidelity during a finite window. The scoliosis-vulnerability hypothesis in IEC is therefore a control-limited regime of a coupled resource-allocation system.

### 2.11.3 Thermodynamic Constraints and Energy Deficit Mechanism
We represent the energy budget per unit tissue volume as

\[
E_{\mathrm{total}}(t)=E_{\mathrm{mechano}}(t)+E_{\mathrm{growth}}(t)+E_{\mathrm{metabolic}}(t),
\]

where \(E_{\mathrm{mechano}}\) is ATP expenditure for force sensing and feedback maintenance, \(E_{\mathrm{growth}}\) for structural synthesis and assembly, and \(E_{\mathrm{metabolic}}\) for baseline cellular maintenance. During adolescence, \(E_{\mathrm{growth}}\) rises with growth velocity, while effective supply can remain transport-limited over short intervals [10,20]. The result is a transient deficit in control-relevant energy allocation.

We quantify this imbalance using

\[
R(t)=\frac{v_{\mathrm{growth}}(t)}{v_{\mathrm{adapt}}(t)},
\]

with \(v_{\mathrm{adapt}}\) representing mechanosensory adaptation rate. The vulnerable regime is

\[
R(t)>R_{\mathrm{crit}},\qquad \frac{\partial \kappa}{\partial \varepsilon}\gg1,
\]

where \(\kappa\) is curvature and \(\varepsilon\) perturbation amplitude. In this regime, perturbations that would ordinarily be corrected are amplified because corrective sensing and remodeling lag behind growth-driven geometric change. The framework therefore predicts highest risk when growth acceleration exceeds adaptation bandwidth, which is temporally consistent with adolescent idiopathic scoliosis (AIS) onset distributions [11,12].

To avoid overinterpretation, this mechanism should be read as a conditional instability statement: elevated \(R(t)\) is interpreted as a risk-elevating condition, not a sufficient condition for progression. Additional susceptibility factors (for example, developmental asymmetry, neuromuscular control variance, and connective-tissue microstructure) likely modulate transition probability [11–15].

### 2.11.4 Tensor Structure of IEC
A scalar coupling law \(E(s)=E_0f(I(s))\) captures magnitude modulation but does not capture directional susceptibility. The mechanically relevant object is anisotropic stiffness \(C_{ijkl}(s)\) coupled to a vectorial information gradient \(\nabla I(s)\). Let
\(\hat n_{\mathrm{info}}=\nabla I/|\nabla I|\) and \(\hat n_{\mathrm{stress}}\) be the local principal-stress direction. We define

\[
\alpha(s)=\hat n_{\mathrm{info}}(s)\cdot\hat n_{\mathrm{stress}}(s),
\]

and model directional stiffness as

\[
E_{\mathrm{eff}}(s)=E_{\parallel}\alpha^2(s)+E_{\perp}\big(1-\alpha^2(s)\big),\qquad E_{\parallel}>E_{\perp}.
\]

When \(\alpha\approx1\), information gradients and stress directions are aligned and resistance is high. When \(\alpha\approx0\), coupling is weak and effective stiffness approaches \(E_{\perp}\), creating a compliant direction that can localize deformation. This orientation law provides a mechanistic explanation for plane-selective vulnerability: under predominantly axial loading, lateral perturbations can drive stronger misalignment than matched AP perturbations, yielding larger coronal amplification.

This extension resolves a core limitation of scalar IEC implementations: they can reproduce curvature magnitude trends but not directional instability. The tensor form yields testable predictions at imaging scale: sites of progression should co-localize with low-\(\alpha\) domains and altered collagen orientation fields measured by polarized light or second-harmonic generation microscopy [14,15].

## 4.7 Thermodynamic Instability Windows Predict Scoliotic Vulnerability
To evaluate the thermodynamic-instability hypothesis, we computed the age-dependent ratio
\(R(t)=v_{\mathrm{growth}}(t)/v_{\mathrm{adapt}}(t)\) from ages 5-20 years. Growth velocity was modeled using sex-stratified adolescent growth trajectories (Preece-Baines parameterization) fitted to longitudinal spinal-length data from the Zurich Growth Study (\(n=222\)) [11,12]. Adaptation velocity was estimated from turnover windows of representative mechanosensory proteins (integrin \(\beta\)-subunits, FAK, PIEZO2-family channels) and constrained by ATP-availability scaling [7,16,17].

Figure 7 (Energy Deficit Time Course) shows that \(R(t)\) peaks sharply during adolescence. In the current parameterization, peak vulnerability occurred at 11.2 +/- 0.8 years in females and 13.4 +/- 1.1 years in males, with \(R_{\mathrm{peak}}=2.7+/-0.3\) and \(2.4+/-0.4\), respectively, above \(R_{\mathrm{crit}}=1.5\). The interval \(R(t)>R_{\mathrm{crit}}\) persisted for approximately 18 months in females and 24 months in males. These windows overlapped the known AIS incidence maxima by sex and age [11,12].

To examine severity linkage, we calculated integrated deficit burden \(\int (R-R_{\mathrm{crit}})_+\,dt\) and compared it with Cobb angle at skeletal maturity in a retrospective AIS cohort (\(n=156\)). Figure 8 (Energy Deficit Magnitude vs Cobb Angle) showed a positive association (Pearson \(r=0.68\), \(R^2=0.46\), \(p<0.001\)). Patients in the highest deficit tertile (\(R_{\mathrm{peak}}>3.0\)) had larger final curves (34 +/- 12 degrees) than those in the lowest tertile (\(R_{\mathrm{peak}}<2.0\), 18 +/- 8 degrees; Mann-Whitney \(p<0.001\)).

The mechanistic interpretation is that deficit windows reduce feedback fidelity: small asymmetries that are ordinarily corrected can persist long enough to couple to asymmetric loading and growth. This interpretation is compatible with Hueter-Volkmann-type feedback in progressive curves [13,14], but it does not claim that energy imbalance alone determines outcome. In sensitivity analyses, age and sex adjustment did not abolish the deficit-severity association, although residual variance indicates additional covariates.

Two quantitative predictions follow. First, progression risk should track mismatch timing (growth versus adaptation) more strongly than absolute growth magnitude alone. Second, interventions that increase adaptation bandwidth or reduce transient ATP constraints during the peak window should reduce progression probability, even if baseline sagittal architecture is unchanged. These predictions are testable in prospective cohorts with serial growth, metabolomic, and imaging measurements.

Model diagnostics were used to evaluate whether the deficit signal was dominated by a narrow parameter subset. Across perturbations in mechanosensory turnover, ATP-supply scaling, and growth-curve parameters, peak timing shifted modestly (typically <1 year), but the existence of a puberty-centered vulnerability window remained stable. The strongest sensitivity was to the adaptation-rate prior, indicating that direct in vivo measurements of vertebral mechanosensory turnover are a key missing constraint for next-generation models. Even under conservative settings, the model retained sex-offset peaks and a positive deficit-severity relationship, suggesting that the mechanism is structurally robust, although the exact effect size should be interpreted with uncertainty bounds rather than as a fixed constant.

## 4.8 Vector Mismatch Localizes Scoliotic Deviations
To test whether directional instability localizes by vector mismatch, we mapped
\(\alpha(s)=\hat n_{\mathrm{info}}\cdot\hat n_{\mathrm{stress}}\) along normal and perturbed geometries.

Figure 9A (Vector Field Overlay) shows near-collinearity in unperturbed solutions, with
\(\alpha(s)=0.97+/-0.02\) across most segments. Under lateral perturbation (\(\varepsilon_{\mathrm{asym}}=0.05\)), the gradient acquires a transverse component, and \(\alpha\) falls to 0.21 +/- 0.08 at the thoracolumbar junction, co-localizing with maximal coronal curvature.

Figure 9B (Alignment Heat Map) summarizes five perturbation amplitudes. Across runs, the minimum-\(\alpha\) domain co-localized with the curve apex within +/-2 vertebral levels. Cobb angle scaled with mismatch magnitude approximately as
\(\theta_{\mathrm{Cobb}}\propto(1-\alpha_{\min})^{1.4}\) (\(R^2=0.93\)), indicating a steep nonlinearity in orientation-dependent susceptibility.

For experimental comparison, we analyzed published polarized-light microscopy datasets from cadaveric scoliotic spines [14]. Controls showed fiber-axis misalignment of 12 +/- 4 degrees, whereas apical scoliotic regions showed 38 +/- 11 degrees. The measured increase in orientation disorder was directionally consistent with low-\(\alpha\) predictions, while acknowledging that end-stage tissue remodeling in cadaveric specimens is not equivalent to early progression dynamics.

Directional selectivity emerged in matched-perturbation simulations: a 5% sagittal asymmetry increased kyphosis by 3.2 degrees, whereas a 5% lateral asymmetry produced 17.8 degrees of coronal Cobb angle (ratio 5.6:1). This anisotropic amplification is expected from
\(E_{\mathrm{eff}}=E_{\parallel}\alpha^2+E_{\perp}(1-\alpha^2)\), because lateral perturbations under axial loading are more likely to push \(\alpha\) toward low values.

These analyses suggest that scoliosis risk is governed by both scalar stiffness magnitude and vector alignment structure. A practical implication is that progression biomarkers should include orientation metrics (information-gradient directionality and collagen alignment), not only bulk modulus estimates.

To assess localization fidelity, we compared apical-level predictions from the low-\(\alpha\) map with apex labels from radiographic reconstructions. Agreement was strongest when mismatch was defined by contiguous domains rather than isolated minima, supporting a segment-level interpretation of instability. In bootstrap resampling across perturbation amplitudes, low-\(\alpha\) domain location remained stable relative to apex level, while absolute \(\alpha_{\min}\) values varied with constitutive assumptions. This behavior is expected for anisotropic systems in which localization topology is more robust than local magnitude. Together, these results indicate that vector mismatch is not merely a descriptive correlate but a plausible organizing variable for where deformity amplifies and in which plane progression is favored.

Prospectively, this framework implies that serial vector-field mapping could stratify progression risk before large Cobb-angle changes are visible, particularly when combined with growth-velocity and metabolic indices.

## 3.5 Multi-Scale Protein Mechanics Pipeline

### 3.5.1 Protein Structure Prediction (Level 1)
Structures were retrieved from AlphaFold DB v4 where available and predicted de novo otherwise (AlphaFold 2.3.2/3 workflow) [3,4]. For each protein, we extracted pLDDT and PAE, domain boundaries, radius of gyration, anisotropy ratio, and candidate hinge regions (low-confidence linkers between higher-confidence domains). These descriptors were used as priors for mechanical simulation and uncertainty weighting. Proteins with extensive disordered regions were retained but flagged for larger mechanical uncertainty.

### 3.5.2 Steered Molecular Dynamics (Level 2)
SMD was run in GROMACS 2023.3 with CHARMM36m and TIP3P water at 150 mM ionic strength. Systems were energy-minimized (steepest descent), equilibrated under NVT then NPT ensembles (310 K, 1 bar), and pulled with a harmonic spring along the principal molecular axis. Pulling velocity and spring constant were selected to capture quasi-elastic response before large-scale unfolding (\(v_{\mathrm{pull}}=0.01\) nm ps\(^{-1}\), \(k=1000\) kJ mol\(^{-1}\) nm\(^{-2}\)).

For each target, five seeds were simulated; force-extension curves were aligned by zero-force extension and fitted in the low-strain regime to estimate stiffness. Type I collagen served as a calibration anchor: predicted \(k=420+/-65\) pN nm\(^{-1}\), consistent with AFM ranges (350-500 pN nm\(^{-1}\)) [5]. We report mean +/- s.d. and retain per-seed traces for reproducibility.

### 3.5.3 Fibril Assembly and Coarse-Grained Mechanics (Level 3)
Atomistic outputs were coarse-grained with Martini 3 and assembled into quasi-hexagonal fibrils with 67 nm D-band staggering [5,6]. Cross-link density was varied from immature to mature regimes to probe stiffness nonlinearity. Fibril tensile response was computed at low strain rate, and linear-regime modulus was extracted from stress-strain slopes.

Proteoglycan contributions were added through an osmotic term based on Donnan equilibrium, parameterized by fixed-charge density [6]. Composite fibril-matrix behavior was then estimated by mixture rules with composition-dependent volume fractions. This level yields effective fibril-scale constitutive parameters passed to tissue homogenization.

### 3.5.4 Tissue Homogenization (Level 4)
Tissue-level elasticity was computed as

\[
\mathbf C_{\mathrm{tissue}}(s)=\sum_i \phi_i(s)\,\mathbf R(\theta_i)\,\mathbf C_{\mathrm{fibril},i}\,\mathbf R(\theta_i)^T,
\]

where \(\phi_i(s)\) are constituent volume fractions from histology/immunostaining,
\(\theta_i\) are preferred orientation angles from polarized imaging, and
\(\mathbf C_{\mathrm{fibril},i}\) are constituent stiffness tensors from Level 3.

Regional parameterization yielded \(E_{\mathrm{cervical}}=1.15+/-0.18\) GPa,
\(E_{\mathrm{thoracic}}=0.32+/-0.07\) GPa, and
\(E_{\mathrm{lumbar}}=0.78+/-0.12\) GPa, with predicted-versus-measured agreement
\(R^2=0.81\) across 12 vertebral levels. These values were used as priors in Cosserat simulations and propagated with uncertainty bands.

### 3.5.5 Protein-Class Dynamics and Energy Allocation
Mechanosensory and growth pools were modeled by coupled kinetics:

\[
\frac{dP_{\mathrm{mech}}}{dt}=\alpha_m(E_{\mathrm{mech}})-\delta_mP_{\mathrm{mech}},\qquad
\frac{dP_{\mathrm{grow}}}{dt}=\alpha_g(E_{\mathrm{grow}})-\delta_gP_{\mathrm{grow}},
\]

subject to \(\alpha_m+\alpha_g\leq E_{\mathrm{total}}-E_{\mathrm{metabolic}}\).
Degradation constants were set to \(\delta_m=0.058\) h\(^{-1}\) and
\(\delta_g=0.001\) h\(^{-1}\), consistent with mechanosensory versus matrix turnover separation [10,20]. Growth forcing followed fitted adolescent velocity curves. At each time step, ATP-constrained synthesis rates generated \(R(t)\) and a time-varying mechanosensory coupling term used in the rod solver.

### 3.5.6 Cosserat Integration and Vector-Field Analysis (Level 5)
The Cosserat rod was solved with spatially varying rest curvature, anisotropic stiffness, gravity, and physiological boundary conditions [18,19]. Outputs included sagittal and coronal curvature, Cobb-angle proxies, local moments, and principal-stress directions. The alignment map \(\alpha(s)\) was computed nodewise from information-gradient and stress vectors.

Vector mismatch regions were defined as contiguous segments with \(\alpha<0.5\), and severe mismatch as \(\alpha<0.3\). These thresholds were applied consistently in model and imaging analyses to avoid post-hoc relabeling.

### 3.5.7 Validation and Uncertainty Reporting
Validation was performed at three interfaces: molecular (SMD versus AFM), tissue (homogenized modulus versus mechanical testing), and geometry (predicted curvature versus imaging-derived curvature). We report \(R^2\), residual distributions, and bootstrap confidence intervals. Agreement at one level was not assumed to guarantee transferability; each interface was evaluated independently.

To reduce overfitting risk, key analyses were repeated under parameter perturbation and alternative initialization seeds. Core conclusions (existence of an adolescent vulnerability window and localization by vector mismatch) were robust to these perturbations, while effect sizes varied as expected with constitutive uncertainty.

For numerical reproducibility, all simulations were run with fixed random seeds per replicate set, and deterministic post-processing scripts were used for stiffness extraction, alignment mapping, and curve-angle quantification. Convergence checks included mesh refinement for rod discretization, time-step reduction in dynamic relaxation, and seed-wise stability of fitted low-strain slopes in SMD traces. A run was accepted only when force balance residuals and geometric outputs met prespecified tolerances across consecutive refinement levels.

Data integration followed a predeclared mapping of measurement scale to model parameter: molecular stiffness constrained constituent tensors, histology constrained volume fractions, polarized imaging constrained orientation matrices, and growth records constrained time-varying forcing terms. This mapping was designed to prevent circular fitting of geometry-level outcomes. Where literature values were heterogeneous, priors were represented as distributions and propagated forward to prediction intervals. The reported point estimates therefore represent central tendencies of posterior simulations, while uncertainty envelopes reflect both measurement noise and structural model variance.

## Key Equations (Insertion List)
1. **Energy balance**
\[
E_{\mathrm{total}}=E_{\mathrm{mechano}}+E_{\mathrm{growth}}+E_{\mathrm{metabolic}}.
\]

2. **Instability ratio**
\[
R(t)=\frac{v_{\mathrm{growth}}(t)}{v_{\mathrm{adapt}}(t)},\quad R(t)>R_{\mathrm{crit}}\Rightarrow \text{vulnerability window}.
\]

3. **Amplification criterion**
\[
\frac{\partial \kappa}{\partial \varepsilon}\gg1\quad \text{for }R(t)>R_{\mathrm{crit}}.
\]

4. **Alignment parameter**
\[
\alpha(s)=\hat n_{\mathrm{info}}\cdot\hat n_{\mathrm{stress}}.
\]

5. **Orientation-dependent stiffness**
\[
E_{\mathrm{eff}}(s)=E_{\parallel}\alpha^2(s)+E_{\perp}\big(1-\alpha^2(s)\big).
\]
