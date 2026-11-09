# Biological countercurvature, information, and postural thermodynamics

Prepared 2026-10-02. This develops the gravity and biological-organization motif in the user's earlier article, within ordinary biomechanics and information thermodynamics. Definitions and ideal theoretical results are separated from proposed human measurements. It supplies no new human data or longevity estimate.

## The connection to the earlier work

Sections 1.2 and 3 of the [earlier countercurvature article](https://quantumjournalofconsciousness.com/articles-3/) describe organisms maintaining or developing organized form under gravitational constraints. Those sections motivate the present question; they do not provide calibrated postural energetics or a floor-rise intervention result. The usable meaning of **biological countercurvature** here is the development, maintenance, and controlled deformation of body geometry under load.

The geometry in this study is the body's configuration and reference shape. Gravity enters through weight and its moments. Gene regulation, tissue remodeling, and sensorimotor control change material properties, reference geometry, or muscle forces. No additional gravitational field term is needed to formulate this research question.

Three timescales must remain separate:

| Process | Physical representation | Relevant information | Measurement |
|---|---|---|---|
| Development and slow remodeling | Reference curvature, joint geometry, stiffness, tissue mass | Regulatory signals influencing formation and maintenance | Longitudinal geometry and material measurements; a gene-to-parameter relationship requires independent identification |
| Immediate posture and movement control | Muscle forces acting on a loaded body with sensory feedback | Information about orientation, motion, contact, and perturbations | Controlled perturbations, kinematics, forces, activation and fitted response dynamics |
| Loading and recoil | Recoverable tissue deformation and dissipative history | The controller's selection and timing of loading/unloading | Tissue work and uncertainty, pause and speed conditions, metabolic bouts |

A stable anatomical curve can persist through passive material properties. Sustaining every component of that curve does not require continuous positive mechanical work. Conversely, an active isometric contraction can consume chemical energy while performing zero external work. The cost of formation, maintenance, force production, and movement must not be collapsed into one curvature-dependent energy term.

Human stance experiments support a concrete sensory-control component: Peterka used controlled visual/support-surface perturbations to study how orientation cues contribute to corrective responses. This supplies an experimental precedent for testing feedback, not a measurement of information-processing heat. [Peterka, 2002](https://pubmed.ncbi.nlm.nih.gov/12205132/).

## Information has a precise statistical definition

For a defined discrete variable X with probabilities p(x), Shannon entropy is

\[
H_2(X)=-\sum_x p(x)\log_2p(x).
\]

It measures uncertainty in bits. Mutual information is

\[
I_2(X;Y)=\sum_{x,y}p(x,y)\log_2\frac{p(x,y)}{p(x)p(y)}.
\]

It measures how much observing one variable reduces uncertainty about the other. The states, sampling conditions, and distribution must be specified. Entropy of a movement trace is not automatically useful information: noise can raise it. [Shannon, 1948, original paper](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

For probabilities over appropriately defined physical microstates, Gibbs entropy uses the corresponding natural-log expression multiplied by Boltzmann's constant. With coarse states, their internal entropy must also be included. A histogram of trunk angle does not enumerate the body's microstates, so multiplying its Shannon entropy by k_B does not yield whole-body thermodynamic entropy. [Jaynes, 1957](https://journals.aps.org/pr/abstract/10.1103/PhysRev.106.620).

\[
S_{Gibbs}=-k_B\sum_i p_i\ln p_i=k_B\ln2\,H_2,
\]

where the last equality uses the **same physical-state distribution** on both sides, not an arbitrary movement statistic.

The project's scalar patterning field I(s), amino-acid composition entropy, curvature-distribution entropy, and sensorimotor mutual information are different quantities. Each can be useful, but their names do not supply a common physical unit or an energy conversion.

## Where the thermodynamic connection becomes physical

### Erasing a physical memory

For a symmetric, initially unbiased one-bit memory, completely reset through a cyclic isothermal protocol without usable side information, the ideal Landauer heat bound is

\[
Q_{bath}\ge k_BT\ln2.
\]

At an illustrative 310 K this is approximately **2.97 × 10⁻²¹ J per erased bit**, using k_B = 1.380649 × 10⁻²³ J/K. It is an ideal erasure bound, not a measured cost per neural message, movement, or new bit learned. Biased states, errors and correlations require the appropriate generalized accounting. [Landauer, 1961](https://doi.org/10.1147/rd.53.0183).

Bérut and colleagues tested erasure using a colloidal-particle memory and approached the predicted limit with long erasure cycles. This verifies a physical information–heat connection in that apparatus; it does not calibrate human postural energetics. [Bérut et al., 2012](https://www.nature.com/articles/nature10872).

### Nonequilibrium free energy

For an ideal model with physical states i, fixed energies E_i, and a bath at temperature T, define

\[
\mathcal F[p]=\sum_i p_iE_i+k_BT\sum_i p_i\ln p_i.
\]

The canonical distribution is p_i^eq = exp(−E_i/k_BT)/Z. Direct substitution gives

\[
\mathcal F[p]-\mathcal F_{eq}
=k_BT D_{KL}(p\Vert p^{eq}),\qquad
D_{KL}=\sum_i p_i\ln\frac{p_i}{p_i^{eq}}\ge0.
\]

This is an explicit statistical-to-energetic bridge because the states, energies, and physical equilibrium distribution are specified. A distribution of body poses lacks those ingredients by itself. A statistical inference loss also does not become thermodynamic free energy by sharing its name. The whole body exchanges chemical species and heat and needs a richer open-system model. [Physical nonequilibrium framework: Still et al., 2012](https://arxiv.org/abs/1203.3271).

### Information used in feedback

For a specified isothermal measurement-and-feedback setup, Sagawa and Ueda derive the bound

\[
\langle W_{on}\rangle\ge\Delta F-k_BT I,
\]

where I is measurement mutual information in nats; information in bits introduces an additional factor ln 2. This permits improved work extraction/control relative to the system-only bound under the stated setup. The controller and memory must be accounted for in a complete cycle. Information guides the use of available physical resources; it does not supply a universally applicable −k_BT I term for a human movement. [Sagawa and Ueda, 2010](https://arxiv.org/abs/0907.4914).

Continuous information-flow formulations require explicit interacting stochastic subsystems and appropriate transition/thermodynamic assumptions. Correlation rates alone do not identify heat. Those conditions have not been established for this project's whole-body model. [Horowitz and Esposito, 2014](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.4.031015).

## The biological bridge is control under an energy budget

Lan and colleagues studied energy, speed and accuracy in a sensory-adaptation feedback network, with experiments in bacterial chemotaxis. Their result supports asking what energetic resources accurate adaptive control requires. Its numerical trade-off is not a human postural law. [Lan et al., 2012](https://pubmed.ncbi.nlm.nih.gov/22737175/).

Sartori and colleagues more directly formulated information-processing costs in sensory adaptation and applied them to bacterial sensing. This makes signaling networks a plausible later site for a physical information-thermodynamics experiment, after a defined signal, molecular state, and chemical budget are measurable. [Sartori et al., 2014](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003974).

The proposed human extension is an inference to test: repeated tolerable floor transfers may help maintain accurate estimates of body/load state and appropriately timed muscle action. Such coordination might reduce unnecessary activation at a given stability requirement, or preserve stability at a given available capacity. Either outcome could support independent activity. Neither implies that all extra activation is wasteful; co-contraction can provide useful stabilization.

Lower expenditure alone cannot distinguish efficient control from failed or insufficient control. The useful comparison is therefore a **performance–energy relationship**: recovery accuracy, support needs, and response speed evaluated together with task-specific metabolic cost. Mechanical recoil is one contributor to this relationship; sensing, muscle coordination, geometry, and external support are others.

In an explicit driven stochastic model, predictive and nonpredictive memory can have different relationships to dissipation. Applying that idea to posture is a proposed analogy until a physical model is validated; observational movement predictability is not a direct estimate of neuronal heat. [Still et al., 2012](https://arxiv.org/abs/1203.3271).

## Minimal extension of the mechanics

For illustration only, a single-link upright-body approximation can be written

\[
J\ddot\theta=mgh\sin\theta+
\tau_{passive}(\theta,z)+\tau_{active}(a)+\tau_{support}+\eta.
\]

Here θ is tilt from upright, J rotational inertia, h center-of-mass height, z passive material history, a activation/controller state, and η a disturbance. All terms on the right are torques. Positive mgh sin θ expresses destabilizing gravitational torque for this coordinate convention. A sensory observation y = h_obs(θ, θdot, contact) + noise informs a dynamic controller; h_obs is an observation function, not COM height h.

This model combines gravity, passive recovery and active feedback without declaring the body a literal helical spring. It is not yet solved, fitted, or validated and is only an initial approximation to stance, not a complete floor transfer or spine-growth model.

The mechanical balance from [the thermodynamic extension](THERMODYNAMIC_EXTENSION.md) still applies. An informational controller specifies how active forces respond to observations; it does not replace the measured muscle-work term or insert unmeasured information energy into it. Biological growth would require separate slow state variables and chemical/remodeling costs. Earlier withdrawn rod conclusions remain withdrawn.

## A discriminating research addition

Add a supervised, repeatable perturbation assessment to the existing dose-matched floor versus chair/step study. Keep untrained gait as the main functional endpoint. The following are mechanistic secondary outcomes, not a new unvalidated longevity index:

1. **Control performance:** held-out prediction of response kinematics/torque to prescribed perturbations, recovery time, error, and actual support use. Test sensory weighting in an appropriate supervised task. Define tolerable perturbations and reliability before an efficacy comparison.
2. **Mechanical performance:** measure the already specified recoil endpoints, pause and rise-speed conditions, and tissue-work uncertainty. Estimate new muscular preload separately where identifiable.
3. **Metabolic performance:** compare repeatable bouts with matched task conditions, recovery observation, and defined baseline subtraction. Single-event oxygen use cannot isolate the cost of sensing from actuation or assign it to one short correction.
4. **Information analysis, only if identifiable:** define X as a controlled input or future physical task state and Y as a specified response/observation history. Freeze sampling, lag, estimator and covariates. Use independent validation trials and appropriate surrogates accounting for autocorrelation. Account for shared task phase and common inputs; lagged dependence or transfer entropy alone does not establish neural causation. IMU and EMG variables remain proxies rather than direct measurements of the controller's internal information.

A useful positive finding would be improved untrained recovery at similar energetic demand, or reduced demand while preserving recovery performance and support conditions, beyond the active comparator. Greater trajectory entropy or mutual information alone is insufficient. If an apparently informative signal adds no held-out predictive value beyond ordinary kinematics/force/history, reject that addition. If training changes only the practiced transfer, retain task learning and withhold a generalized control claim.

The molecular route is separate: choose a defined mechanosensory pathway, controlled signal and measurable chemical transitions before applying information-thermodynamic bounds. Generic Klotho, YAP, or p21 changes cannot supply that calibration.

## Refined hypothesis for the paper

**Biological countercurvature can be studied as the formation and maintenance of functional body geometry under gravitational loading. Repeated low-to-upright transitions may preserve the coordination of sensory state estimation, active force, and reversible tissue deformation. Preserving useful control relative to available energetic and mechanical capacity may support sustained mobility and independence with age. Incremental benefit over comparable exercise, and any contribution to disability-free survival or lifespan, require separate tests.**

Proposed title: **“Biological countercurvature and the energetic cost of postural control: a testable framework for functional aging.”**
