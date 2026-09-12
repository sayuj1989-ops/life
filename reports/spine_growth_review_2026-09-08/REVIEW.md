# Spine growth under gravity: research gap review

Reviewed 2026-09-08. Sources: the authoritative `~/life` manuscript, its compiled September 4 PDF, code and audit ledger; the `jupyterlab/scoliosis` working copy; publication-track audits; targeted primary-literature searches. This is a focused scientific audit, not a systematic review or patient validation.

**Assessment:** retain gravity as a load and growth as a period of changing geometry, tissue properties, and control demands. The promising core is competition between restoration and load-dependent remodeling. It currently illustrates a possible progression mechanism; it does not establish a general cause of AIS. The highest-value advance is a measurable, spatial, multiscale model that can fail against conventional growth-modulation models.

## 1. What happened to the derivative gain gap?

There are several different models being described under this name:

1. **Original growth-delay hypothesis:** withdrawn in `AUDIT_LEDGER.md`, R-2/R-4/H-1. The r=0.983 statistic compared deterministic functions of the same swept length grid. Removing the IEC coupling still gave r=0.9816. The original model's delay utilisation falls with growth: 0.806→0.655 at its assumed conduction velocity of 15 m/s; 0.546→0.324 at 55 m/s. Increasing absolute delay does not establish decreasing stability reserve: the mechanical timescale changes too. These numerical values are the existing ledger's re-derivation, not a new rerun here.
2. **Proposed loss of gain during growth:** a distinct, still-testable hypothesis. It needs independent measurements of gain, delay, inertia, stiffness and maturation. Putting a gain trough at peak height velocity and reproducing that timing is not independent evidence.
3. **New margin experiment in the working copy:** `experiment_derivative_gain_gap_margin.py` uses assumed gain maturation and six-second amplitude cutoffs. These are finite-duration response criteria, not an exact asymptotic stability boundary. It needs analytic boundary comparisons, time-step and horizon convergence, and both lower and upper gain limits. A positive lower gain gap alone does not ensure stability.
4. **Untracked `life/src/spine_growth_analysis.py`:** its advertised corrected Hopf formula is incorrect for its stated delayed-PD equation. Independently solving that equation gives a first boundary of 67.021 ms at Kd=8, compared with this file's 1491.041 ms. At Kd=12 the values are 78.852 ms versus 1938.610 ms. The independent roots have characteristic residuals below 1e-9. Its simulator also returns acceleration then velocity, but assigns those to position and velocity increments respectively; delayed states are held at the initial RK stage. Its blanket statement that Euler is unconditionally unstable for every positive delay is unsupported. Do not use its reassuring baseline-stability claim.

The new formula error does **not** reverse the original model's withdrawal: these are different parameterizations. Evidence and reproducible diagnostic code are in `check_equations.py` and `equation_checks.json`; original scripts were preserved.

## 2. The recovery ratchet still has load-bearing assumptions

The scalar implementation uses

`dκp/dt = kg(t) κe0 kg(t)/(kr + kg(t))`, with `κe0 > 0` fixed,

and reports flexibility as `F = κe0/(κe0 + κp)`.

**Progression and declining flexibility are imposed.** The derivative is positive and independent of the current permanent curvature. Consequently F must decrease. This is a useful toy example, but falling F in this simulation is not an independent discovery. It lacks a true onset bifurcation at kg=kr: the equation is smooth and any positive kg produces set even when kg<kr.

**The rate law needs a complete derivation.** For an isolated perturbation A, constant competing rates give `e(t)=A exp[-(kr+kg)t]`, `dp/dt=kg e`, and total permanent set `A kg/(kr+kg)`. That fraction is valid. To turn it into a continuous production rate one needs an event rate ν: `dp/dt = ν A kg/(kr+kg)`. The current code additionally assumes ν=kg. Alternatively, continuously maintained elastic deformation gives `dp/dt=kg e`; the event-rate multiplier should not be silently added again. Test these alternatives rather than treating the present equation as uniquely derived.

**The clocks are not yet linked.** Code runs in years: kr=0.3, 1, 6 corresponds to restoration times of about 3.3 years, 1 year, and 2 months. Those cannot directly represent a millisecond neural loop or immediate supine unloading. Define which slow process kr represents—habitual alignment, tissue adaptation, recovery of disc strain—and derive its connection to fast posture.

**The model supplies a signed seed.** Fixed positive κe0 assumes persistent asymmetric loading. Symmetric zero-mean fluctuations do not produce a preferred population handedness without rectification or bias. Random symmetry breaking can select individual curve direction, but right-thoracic predominance needs an independently specified asymmetry. Separate normal sagittal curvature from coronal deviation and axial twist.

**Restoration should remain possible.** The present growth function has a positive baseline at age 20; if extrapolated, set continues accumulating. It also excludes reverse remodeling. Specify maturation-dependent growth cessation and allow correction where biology permits, rather than making permanence universal.

## 3. Improvements ranked by scientific value

| Priority | Missing mechanism or distinction | Concrete improvement and discriminating test |
|---|---|---|
| 1 | **3D initiation versus progression** | Model sagittal alignment, coronal bending and torsion separately, with rib cage, pelvis, segmental stiffness and muscle load paths. Test mirrored perturbations, zero bias, reversed bias and no-growth controls. Predict axial rotation and location without prescribing the answer. |
| 2 | **Disc viscoelasticity versus vertebral growth** | Track reversible disc creep/hydration, vertebral wedging and a slow reference shape separately. Predict recovery under a standardized unloading protocol and the later spatial sequence of disc versus bone wedging. Supine residual Cobb is not a pure measurement of permanent bone deformation. |
| 3 | **Growth versus adaptation speed** | Use measured serial growth and an explicit adaptation timescale. A candidate dimensionless variable is `T_adapt × abs(d log L/dt)`. Test whether lagged recovery plus growth predicts subsequent change beyond maturity, baseline shape and conventional mechanics. Earlier sex-specific growth peaks alone do not predict an 8:1 disease ratio. |
| 4 | **Regional mechanics and load history** | Estimate segment-wise moments, directional stiffness and stress. Include co-contraction and brace forces; gravity magnitude alone is not tissue stress. Differentiate average compression, time under asymmetric load, and unloading/recovery. |
| 5 | **Physically defined metabolic supply** | Estimate actuator energy use and perfusion/oxygenation in the same tissue. Compare surface-limited, volume-limited and measured supply. An assumed supply exponent must not masquerade as demonstrated adolescent metabolic failure. |
| 6 | **Sensorimotor heterogeneity** | Retain proprioception, delay, feedback noise and recalibration as candidate modifiers. Perturbation-response identification is more informative than a sway-amplitude proxy; altered proprioception after a curve develops does not establish initiation. |
| 7 | **Developmental shape control beyond gravity** | Compare cilia–CSF–urotensin signaling, mechanosensation, ECM remodeling and anatomical patterning as separable upstream mechanisms. Require a tissue-level measurable intermediate instead of routing every gene through an unspecified information field. |
| 8 | **Non-progressors and correction** | Fit progressors, stable AIS, correcting curves and healthy adolescents jointly. Require the same parameterization to explain stability during normal growth and treatment-related correction. |

The first four should lead the next model. The later items are competing or modifying mechanisms, not a reason to add unlimited free parameters.

## 4. Gravity and energy: two remaining conceptual corrections

**Gravity does not specify an S-curve.** The current sinusoidal/HOX rest-curvature prescription encodes an alternating shape. Relaxing toward it is conditional on that prescription. Demonstrating emergence requires comparison with measured developmental anatomy and alternative rest shapes/boundary conditions. Gravity may amplify a susceptible structure's deformation without being a necessary origin of every scoliosis phenotype.

**Stored elastic energy is not metabolic power.** The prior scaling audit correctly rejected torque ∝L⁴ as a power law. But replacing it with strain energy `U∝L³` still needs a time or turnover rate before comparing it with metabolic supply in watts. If `P∝U/T(L)` and `T∝L^q`, the demand exponent is `3−q`, not necessarily 3. Static force maintenance can consume ATP without net external mechanical work; it needs an actuator cost model.

The reported 29% ratio rise is conditional on isometry, constant material/time factors, an L² supply assumption, and chosen endpoints 0.35 and 0.45 m. It is a scenario calculation, not an empirically established deficit. Disc diffusion limitations cannot automatically be assigned to vascular paraspinal muscle or sensory neurons. Nor does a whole-body allometric law directly determine local supply within a growing adolescent.

The dimensionless `Bg=EI/(MgL²)` is a useful descriptor. Its critical value depends on boundary conditions, load distribution, geometry and support. A universal human/quadruped threshold is unsupported by the project's own corrected cross-species table.

## 5. Literature that changes the next experiment

**Growth modulation is an established comparator.** Stokes' 2007 model already coupled loading asymmetry and growth sensitivity to simulate progression. Therefore the ratchet must add a measurable recovery process and outperform that comparator, not claim the entire curvature→load→growth feedback as new. [Primary model study](https://pubmed.ncbi.nlm.nih.gov/17653775/). Mechanical vertebral growth modulation also has experimental rat-tail evidence, which is distinct from proving human AIS initiation. [1996 experiment](https://pubmed.ncbi.nlm.nih.gov/8727190/).

**Flexibility is already prognostic in braced cohorts.** A 586-patient retrospective study and a 207-patient prospective study associated flexibility with brace outcomes. These support including flexibility, but do not establish that slow recovery causes untreated AIS or that the present ratchet uniquely explains the association. The proposed advance must be temporal prediction, a new measurable recovery parameter, and comparison against existing predictors. [Cheung 2020](https://pubmed.ncbi.nlm.nih.gov/32009436/), [Wong 2022](https://pubmed.ncbi.nlm.nih.gov/35360943/).

**Proprioception deserves a conditional role.** A recently indexed one-year cohort reports 166 baseline participants and 115 completing follow-up, with a finding concerning surgical correction and a cautious conclusion about prognostic significance. The retrieved abstract does not establish growth-related derivative-gain failure. Full-text access encountered a browser challenge, so this review does not infer unreported null estimates or causality. [Prospective study](https://pmc.ncbi.nlm.nih.gov/articles/PMC13285751/).

**CSF-linked axial control is a serious biological comparator.** Zebrafish experiments show that restoring Ptk7 in motile ciliated lineages prevents scoliosis, and restoration of ciliary motility after onset blocks progression. Reissner-fiber/urotensin work provides another experimentally manipulable path to axial shape control. These are animal mechanisms, not proof of human AIS, and challenge any universal requirement for human upright gravitational loading. [Grimes 2016](https://pubmed.ncbi.nlm.nih.gov/27284198/), [urotensin rescue study](https://pubmed.ncbi.nlm.nih.gov/32409296/).

## 6. What would actually test the refined theory?

**Model hierarchy:** conventional geometry/maturity prognosis → stress-modulated growth → added recovery dynamics → optional neural or metabolic modifier. Compare patient-held-out predictive performance and calibration, not correlations between formulas sharing the same inputs. Report uncertainty, missingness and treatment selection. The synthetic BrAIST success-rate match remains calibration; improved prediction alone would not uniquely establish causation.

**Minimum useful patient series:** serial height/spinal length and maturity; baseline and follow-up Cobb/3D morphology; standardized, clinically available flexibility assessment; curve pattern and regional wedging; brace exposure/adherence and other treatment. Flexibility measured with different unloading/bending protocols is not interchangeable. A future observational protocol needs prespecified timing and measurement reproducibility; no additional imaging is proposed here solely for this review.

**Primary discriminating prediction:** within-patient deterioration of independently measured recovery behavior precedes later structural wedging/progression, and interacts with measured growth after accounting for baseline curve and maturity. Prespecify the lag. Use existing flexibility as a comparator, not a newly invented discovery.

**Falsifiers:** (a) no added predictive value of recovery beyond conventional mechanics; (b) recovery changes only after structural progression; (c) the growth interaction disappears after maturity/treatment adjustment; (d) physiological rate ranges cannot generate the predicted window; (e) a symmetry-preserving model cannot produce the observed 3D phenotype without prescribing it. Each result should narrow or reject the relevant mechanism.

**Highest-value immediate computational step:** validate a signed two-state reduced model before adding biology:

`de/dt = u(load, geometry, time) − (kr+kg)e`

`dp/dt = kg e − kh p`

Here e is recoverable deviation, p is remodeled deviation, and kh is an optional restoration/remodeling term. This is a proposed comparator, not a validated replacement; parameter identification and a stress-to-growth law remain necessary. Its virtue is that forcing, recovery and conversion are explicit, and constant rates recover the impulse fraction without an unexplained event-rate multiplier. Extend it to segmental mechanics only after units, signed/noise controls and observations are defined.

## 7. Existing simulation and manuscript blockers

- **Newton rod result is not validation yet.** `results/newton_ratchet_rod/ratchet_rod.md` reports Gate C false at every tested Bg, and a purported Cobb angle of 15,628°. This is incompatible with a clinical Cobb measurement. Investigate quaternion/angle extraction, geometry, convergence, seed/shake sensitivity and units before biological interpretation. Code inspection suggests `joint_dtheta` applies `atan2` to the first two position columns of a body transform, rather than deriving adjacent rod-tangent angles. This is a likely measurement defect requiring a dedicated fix; it does not prove the biological mechanism false.
- **Current PDF contradicts its corrected abstract/discussion.** Its included `theory_summary.tex` still asserts a unique human position below a universal Bg≈0.1 threshold. Its conclusion claims a predictable boundary-crossing cause. These are not only obsolete unused drafts: the language was verified in PDF text. The abstract also overstates a clinically robust proxy despite acknowledging synthetic calibration.
- **Anatomical localization needs correction.** The included theory labels T8–T10 the thoracolumbar junction and asserts up to 80% directional stiffness loss without independently measured regional grounding. Directional anisotropy cannot by itself select right versus left.
- **Protein metrics remain exploratory.** The September 4 ledger resolves numerical provenance, but panel dependence, incomplete PIEZO2 coverage, sequence length, family/domain composition and confidence handling remain scientific limitations. Low pLDDT alone is not a mechanical hinge measurement; elongation does not establish ATP cost or vulnerability under physiological load. Structural-metric comparisons cannot substitute for tissue-specific functional measurements.
- **Unused alternate draft contains additional errors.** `sections/biophysical_origins.tex` claims two equal-amplitude growth oscillations with a fixed phase difference accumulate a lasting wedge. Their difference integrates to zero over full equal-frequency cycles unless another asymmetry/rectifier is added. Its antisymmetric bend–twist stiffness cannot arise from an ordinary conservative quadratic elastic energy; an active nonconservative mechanism would need explicit derivation. This file is not included by `main.tex` and should not be used as current theory.

## 8. Cleanup and next decision

Ten superseded root status documents were selected for reversible archival, with hashes and a restore script under `archive/status_cleanup_2026-09-08/`. The pre-cleanup README is preserved there. Two other obsolete status files referenced by `final_verification.sh` were retained to avoid breaking that script; the new root index marks legacy readiness material as historical. Active manuscript sources, data, experiments, pre-existing working changes and alternative drafts were preserved.

Recommended thesis: **During growth, some spines may fail to restore asymmetric deformation before load-dependent tissue remodeling consolidates it; anatomy and load paths determine where deformation develops, while sensorimotor and metabolic capacity may modify recovery.** Treat this as a falsifiable multiscale hypothesis. The next scientific milestone is a trustworthy mechanical model and independent longitudinal discrimination, not another simulated correlation or additional protein list.
