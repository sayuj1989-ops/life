# Audit of the earlier longevity draft

Reviewed 2026-10-02. Sources: `research/longevity_squat_stand_feasibility.md` and `scripts/experiments/experiment_squat_stand_cycle.py`, in `/home/sayuj/life`. Historical files were read and preserved. This report supersedes their stronger statements for this research proposal, without changing a manuscript or a frozen simulation protocol.

| Earlier assumption | Current assessment | Required correction or test |
|---|---|---|
| Habitual floor rising correlates with exceptional Okinawan lifespan | No directly measured prospective exposure estimate identified in this targeted search | Present as a motivating observation to investigate; obtain individual-level exposure and outcome data |
| Okinawan elders perform 50–100 rises/day; chair users perform about three | Neither population estimate is sourced in the draft | Measure both floor and chair transitions with a validated classifier and sampled observation; do not assign counts by nationality |
| A rise resets coupling completely | This is an imposed model rule, not a measured response | Test partial, saturating, and no-reset alternatives against repeated measurements |
| Coupling decays with a two-hour constant inferred from bed rest or microgravity | No traceable parameter derivation in the draft or code | Keep unidentified; fast signaling and chronic disuse cannot be treated as one timescale |
| Both 50 and 100 rises maintain more than 90% coupling | Inconsistent with the stated 24-hour equation at 50 rises | Analytic evaluation gives approximately 88.9% at 50 and 94.2% at 100; these are conditional model outputs, not measured biology |
| Greater modeled dissipation establishes molecular adaptation | No measured calibration to metabolic energy or a molecular response | Treat model cost as illustrative until units, discretization, physiology, and observables are validated |
| PIEZO activation causes a floor-rise-specific Klotho spike | No direct causal evidence supplied | A separate exploratory mechanism question, not an asserted cascade |
| Higher YAP and lower p21 establish anti-aging benefit | Sign and interpretation depend on tissue and context | Prespecify tissue-specific assays; avoid a universal desirable direction |
| Coupling should correlate with lifespan above 0.6 | No empirical effect-size basis | Remove the numerical expectation; estimate uncertainty from prospective data |
| Protein structures establish whole-body coupling | Structure is not a kinetic, mechanical, or clinical calibration | Protein-level work cannot substitute for physiological measurements |

## Mathematical interpretation of the reset model

For evenly spaced full resets over a period `T`, with decay time `τ` and `N` resets:

`average / peak = (τ N / T) × [1 − exp(−T / (N τ))]`.

The companion CPU script was executed on 2026-10-02 and independently integrated the exponential over the declared sensitivity grid. The maximum analytic–numerical difference was `6.67e-11`; results are recorded in [assumption_checks.json](assumption_checks.json). Under `T=24 h`, `τ=2 h`, the verified conditional outputs are approximately `24.5%, 88.9%, 94.2%` for `N=3, 50, 100`. Changing to a 16-hour waking window changes them. The 24-hour calculation assumes evenly spaced resets through sleep; a daytime pattern needs an explicit overnight segment and a stated baseline. Replacing 24 by 16 is only a sensitivity scenario, not a repair or a measured model.

This expression is monotone by construction. Its shape cannot prove a dose response, optimal frequency, or a population survival difference. The two-hour constant, complete-reset rule, and initial condition require identification before biological interpretation.

## Simulation limitations identified directly in the source

`compute_cycle_dissipation` assigns coefficients `1e-2`, `1e-3`, and `5.0` without a physiological calibration or unit derivation. Curvature costs use node sums without spatial quadrature weights. Those sums can depend on mesh count instead of approximating a fixed physical integral. Every posture step creates a fresh rod and relaxes it for 0.1 seconds; equilibrium and path-dependent physiological history are not established by that construction. A comment about SIRT1/PGC-1α supplies no modeled or measured molecular response.

Positive dissipation should be represented as a loss rate in an explicit balance, for example `dF/dt = P_supply − P_loss`, rather than identifying a positive sum with free-energy decay without a sign convention. Static muscle activation can consume energy despite unchanged height, but its cost is not identified by curvature squared alone.

## Computation boundary

`check_assumptions.py` checks arithmetic and gives hypothetical `m g Δh` examples only. It loads no trained model, runs no rod simulation, collects no clinical data, and estimates no lifespan or protein effect. Its executed output records hashes of the historical draft and script so the reviewed inputs can be identified. Numerical verification does not identify the reset rule or decay time biologically. The separate [passive recoil model and decisions](MODEL_AND_DECISIONS.md) also passed its declared numerical checks; human parameters remain uncalibrated.
