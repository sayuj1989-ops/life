# Floor rising as a recoil cycle: mechanical and thermodynamic hypothesis

Developed 2026-10-02 in response to the user's proposal to visualize floor sitting and getting up as recoiling. This extends the healthy-aging hypothesis; it does not establish a mechanism for Okinawan lifespan. Equations are first-principles balances and an illustrative material model, not fitted human simulations.

The subsequent [countercurvature and information extension](COUNTERCURVATURE_INFORMATION.md) connects the user's earlier gravity/body-geometry work to sensing and feedback. It defines informational quantities separately from mechanical energy and whole-body thermodynamic entropy.

## The useful interpretation of recoil

The body can be represented as a coordinated set of **muscle motors, elastic tissues, and dissipative elements**. During lowering, some gravitational potential energy may enter elastic storage while active muscles control descent. During rising, elastic return can assist muscular work. Tendons are plausible measurable reservoirs; muscle elastic elements and connective tissues may also contribute. The spine cannot be assumed to be the dominant reservoir or a literal helical spring.

Distinguish three phenomena:

1. **Descent-stored passive return:** energy remaining from the preceding lowering is returned during the rise.
2. **Muscle-generated preload:** muscle contraction stretches a tendon shortly before rising; its return changes power delivery and muscle operating conditions, but the stored energy was supplied by muscle.
3. **Recovery of posture and function:** the person returns to an upright configuration through active control. This can be valuable without substantial passive energy recycling.

They look similar in a video but make different energy predictions. “Recoiling” is useful only when its meaning is specified.

## What primary experiments support

An unusually relevant engineering experiment tested elastic knee-assist bands in 31 healthy adults. The bands stored energy during sitting and released it during standing. Measured metabolic power decreased by 3.2 ± 1.5% (mean ± SEM), while muscle activity did not differ significantly. This establishes that external elastic recycling can alter sit-to-stand energetics; it does not measure the native body's floor-rise recoil or show a longevity effect. [Lee, Kim, and Park, 2020](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2020.00966/full).

Ultrasound experiments in eight men observed tendon storage and release during squat jumps **without a preceding countermovement**. Muscle fascicles loaded the elastic tissues before push-off. Thus, finding recoil does not by itself prove recovery of gravitational energy from descent. Jumping is an adjacent mechanism, not a direct test of habitual floor transfers. [Kurokawa et al., 2001](https://pubmed.ncbi.nlm.nih.gov/11247934/).

A human hopping experiment linked tendon work and apparent energetic efficiency, with measurements depending on movement frequency. It supports measuring mechanics and metabolism together rather than inferring metabolic economy from movement shape. [Primary hopping study](https://doi.org/10.1242/jeb.242453).

Human muscle experiments also show that stretch-shortening performance can include activation and history-dependent force effects. Faster or stronger rising cannot be attributed entirely to stored elastic energy. [Seiberl et al., 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4463830/).

## Energy accounting

For a defined mechanical system, let `K` be kinetic energy, `U_g` gravitational potential energy, and `U_e` recoverable elastic energy. All are in joules. Let `P_active` be signed muscle mechanical power, `P_external` other external mechanical power, and `D` passive dissipation in watts:

\[
\frac{d}{dt}(K+U_g+U_e)=P_{active}+P_{external}-D,\qquad D\ge0.
\]

Elastic return appears as a decrease in `U_e`; it is not an additional energy source to add again to this balance. For identical starting and finishing mechanical states, the net changes of these energies vanish. The cycle still costs metabolic energy, including force generation, stabilization, negative-work control, and heat production. Negative muscle mechanical power during lowering does not mean negative metabolic expenditure.

Rising through center-of-mass height `Δh` requires approximately `m g Δh` of increased gravitational potential energy. A purely illustrative 70-kg body rising 0.70 m gains about 481 J. This is not measured floor-rise work, metabolic energy, or calories burned; actual joint work and tissue behavior require measurement. The corresponding descent reverses the potential-energy change, with only part potentially available for useful later return.

The open body obtains chemical energy from metabolism and exchanges heat and matter. Its entropy balance has the form:

\[
\frac{dS_{body}}{dt}=\dot S_{in}-\dot S_{out}+\dot S_{generated},
\qquad \dot S_{generated}\ge0.
\]

Maintaining organized tissues is compatible with exporting entropy. A rise does not reverse total entropy, and neither greater heat dissipation nor less heat per movement establishes slower aging. Measuring oxygen consumption is useful for metabolic cost; it is not a direct measurement of total entropy production or biological age.

## Why the sitting pause is a discriminator

A prompt lowering-and-rising sequence can exploit elastic return differently from sitting for minutes before standing. Some stored energy may dissipate or cease to be mechanically accessible. However, long-lived elastic storage, residual preload, and fresh muscle-generated loading are possible; there is no universal time after which all recoil disappears.

An illustrative **standard linear solid** makes the distinction explicit. Let an elastic spring `k∞` be in parallel with a Maxwell branch consisting of spring `k1` and dashpot `c`. Let `x` be total deformation and `z` deformation of the Maxwell spring, in metres:

\[
F=k_\infty x+k_1z,\qquad
\dot z=\dot x-\frac{z}{\tau},\qquad \tau=\frac{c}{k_1}.
\]

\[
U_e=\tfrac12k_\infty x^2+\tfrac12k_1z^2,\qquad
F\dot x=\dot U_e+\frac{k_1z^2}{\tau}.
\]

`k` has units N/m, `c` N·s/m, and `τ` seconds. At constant deformation, the Maxwell component relaxes as `z=z0 exp(−t/τ)` and its stored energy decreases as `exp(−2t/τ)`, while the parallel spring can retain energy. The dissipated portion becomes heat in this passive model. Actual tendons, discs, and muscles have different, often nonlinear and multiscale behavior. No parameter here is a measured human value or the historical draft's assumed two-hour reset.

An ex-vivo experiment on eight cervical disc segments measured stress relaxation under cyclic loading. It supports treating spinal tissues as viscoelastic, not assigning them a measured floor-rise energy return or a systemic anti-aging function. [Yoganandan et al., 2017](https://pubmed.ncbi.nlm.nih.gov/28033533/).

The companion implementation has now passed energy-balance and independent-integration checks across 225 normalized scenarios. Its [figure](recoil_sensitivity.png) and [model report](MODEL_AND_DECISIONS.md) retain negative net unloading return where prescribed deformation requires new work. A complete-cycle loss greater than the initial loading work is possible because unloading also supplies work in those scenarios; it is not energy creation. No relaxation time in seconds or human recoil fraction has been fitted.

## The refined longevity hypothesis

**Repeated tolerable loading-and-recovery cycles may preserve the capacity to coordinate active force generation with elastic storage and return. Preserved coordination may make daily movement less demanding relative to available capacity, supporting continued activity and independence. Whether this contributes to disability-free survival or lifespan must be tested separately.**

This separates an acute effect—energy and power redistribution in one movement—from adaptation over weeks and possible health effects over years. Improved economy could reduce fatigue and facilitate more activity; it could also reduce the stimulus per repetition. Therefore “more recoil means more longevity” is not a monotone prediction. Likewise, more stiffness can assist force transmission while limiting excursion; stiffness should not be maximized as a universal target.

The testable addition to the broader spine framework is preservation of **reversible, controlled deformation**, measured in specified tissues and tasks. Postural shape alone cannot identify this ability. Chronic training must show transfer beyond the practiced rise, rather than only faster execution.

## The first experiment

Compare prompt reversal, a short pause, and a longer supported sitting interval, plus a rise from an already seated state. Measure force, kinematics, selected tendon deformation, muscle activation, and metabolic cost over repeatable bouts. Separate the cost of holding a posture from the transition. Record support forces and actual movement strategy.

If returned energy originates mainly in new muscular preload after sitting, revise the mechanism to muscle-tendon power coordination. If native recoil is negligible but function improves, retain the coordination/training mechanism and reject passive recoil as its explanation. If floor practice fails to outperform an appropriate comparator on general function, do not use thermodynamic language to rescue a floor-specific longevity claim. Detailed proposals are in [Stage 1b of the protocol](PROTOCOL_DRAFT.md).
