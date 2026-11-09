# Recoil model, evidence update, and experimental decisions

Prepared 2026-10-02. The CPU material-model checks were executed successfully. They validate the equations and implementation under declared assumptions; they do not validate human floor-rise physiology or a longevity mechanism.

## The hypothesis now has three separate mechanisms

| Mechanism | Direct measurement | Claim requiring a separate experiment |
|---|---|---|
| Passive recovery of energy from descent | Tissue force–deformation history and returned work after a specified pause | Does a habitual floor-sitting interval preserve enough useful energy to assist rising? |
| Muscle-generated loading of elastic tissues | Fascicle shortening, tendon deformation, force and timing before/during rising | Does altered coordination improve economy or power at equal task demands? |
| Chronic adaptation of functional reserve | Change in strength, mobility, standardized tissue mechanics, and untrained function | Does floor practice outperform an appropriate activity comparator, and does any benefit persist? |

Short-term mechanical hysteresis, chronic structural adaptation, and lifelong survival must not share an assumed universal decay/reset constant. The current hypothesis does not require a helical centerline to be a mechanical energy reservoir.

## What the executed model establishes

`recoil_model.py` implements the standard linear solid already derived in the thermodynamic extension. Deformation is prescribed through loading, a hold, unloading, and complete passive relaxation at zero deformation. The material's total stiffness, deformation amplitude, and relaxation time define arbitrary reference units. No tissue constants were fitted.

The grid covers five equilibrium-stiffness fractions, three loading durations, five hold durations, and three unloading durations: **225 scenarios**. Segment solutions and integrated work/dissipation are analytic; an independent RK4 integration and refinement check compare internal state, work, and loss. Criteria were specified in the script before execution: segment and complete-cycle balance residuals below 1e-9, nonnegative losses within 1e-10 roundoff, independent integration and refinement differences below 1e-7. The purely elastic control must return all incoming work and lose none.

Executed results in `recoil_model_checks.json`:

- Maximum complete-cycle energy-balance residual: **4.61e-15** in normalized energy units.
- Maximum independent integration error: **9.50e-11**.
- Maximum coarse/fine integration difference: **1.43e-9**.
- **45 purely elastic control cases** passed.
- **58 scenarios had negative net unloading return**. Those prescribed paths need net external work during unloading; the sign was retained rather than clipped.

That last finding is an identifiability warning, not a biological prevalence estimate. The imposed deformation is a boundary condition. A free tissue's trajectory or a person's rising movement would also depend on inertia, muscle action, support, geometry, and control, which this material model does not solve.

The linear material also permits signed tensile/compressive force. A tendon can become slack and does not act as the same spring in compression. Translating this example to a tendon requires measured preload, tension-only behavior, and task geometry; negative-return scenarios must not be described as observed tendon behavior. The normalized endpoints test the accounting, not the anatomical suitability of this constitutive law.

Returned energy within part of the unloading phase differs from *net* unloading return if another part of that phase requires new input. The CSV records both positive outward work and injected work. Remaining internal energy at the end of unloading is included in the loss budget by taking the final zero-deformation relaxation to completion. An integral of force against displacement is work; EMG, posture, or instantaneous force alone does not identify it.

The [PNG figure](recoil_sensitivity.png) and [vector SVG](recoil_sensitivity.svg) plot these normalized scenarios. Ratios on their axes are not human efficiencies or a recommended rise cadence. Complete-cycle loss can exceed the initial loading work when the prescribed unloading also injects work; both inputs remain in the balance.

## Additional primary evidence

1. A study of 15 younger and 15 older adults found lower Achilles stiffness and higher walking metabolic power in the older group, with a modest stiffness–cost association (`r = −0.365`). This supplies an empirical bridge between tissue mechanics and functional energetics. Cross-sectional age differences do not identify a floor-rise effect or prove that changing stiffness will change metabolism. [Gray et al., 2024](https://pubmed.ncbi.nlm.nih.gov/39508895/).
2. A 12-month randomized tendon substudy recruited 36 older adults, with 33 analyzed. Heavy-load training maintained measured mechanical properties better than moderate-load training or control; tendon core collagen and measured cross-links did not change as hypothesized. Ordinary transitions cannot be assumed to reproduce this dose or molecular effect. [Eriksen et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6357404/).
3. A plantar-flexor experiment varied the duration of force relaxation. Measured hysteresis was greater at shorter relaxation durations below one second, with no significant difference among the tested one-to-five-second conditions. This concerns unloading duration, not a stationary sitting pause. It argues for controlling both variables independently. [Sasajima et al., 2023](https://pubmed.ncbi.nlm.nih.gov/36856103/).
4. A separate 14-participant Achilles study found similar stiffness at the tested fast/slow loading rates and about 5% mean hysteresis in its measurable fast condition. Its authors emphasized uncertainty and differences across measurement methods. There is no defensible universal tendon-loss fraction to assign to floor transfers. [Peltonen et al., 2013](https://pubmed.ncbi.nlm.nih.gov/23710431/).

These results support measurement, not a preferred material parameter. A tendon that is more compliant is not automatically healthier, and a stiffer vascular wall or disc is not equivalent to a stiffer tendon. Training load, tissue identity, force operating range, and measurement protocol all matter.

## A stronger mechanistic experiment

First establish repeatability of selected-tendon measurements in a controlled dynamometer task. Standardize loading and unloading rates, initial preload, joint angle, preconditioning, and rest. Estimate force using individualized moment arms where feasible, account for antagonist activity, and propagate uncertainty in force and ultrasound deformation into energy estimates. Tendon subregions and synergist contributions can prevent a single whole-tendon estimate from being identifiable.

Then validate the selected measurement during supervised floor and chair transfers. Treat the dynamic force/deformation estimate as unvalidated until synchronized sensor and model checks pass. Use all relevant supports and force measurements; a foot force plate alone can miss hand, knee, or seat support.

Separate two manipulations:

- **Pause:** prompt reversal, brief supported sitting, and a longer sitting interval. Prespecified example intervals are candidates for feasibility calibration, not validated physiological thresholds.
- **Unloading/rising duration:** two tolerable, standardized movement speeds where safe and feasible, independent of pause duration.

A speed change also affects muscle power, activation, and inertia. A pause changes possible relaxation, preload, fatigue and posture. Neither manipulation alone isolates passive recoil. Record actual kinematics and activation, and include a rise from an already seated state to help identify new muscle-generated loading.

Force–deformation measurements identify tissue work more directly than its energy source. Separating preceding-descent storage from contemporaneous muscle input may remain model-dependent even with ultrasound and EMG. If the source is not identifiable, report uncertainty bounds and total tissue work rather than assigning an unsupported passive fraction.

Do not import jumping or ballistic protocols into frail participants. Begin with the simplest supervised transfer that supports valid measurement. Metabolic comparisons require repeated bouts and a defined recovery observation period; include the different holding costs instead of confusing them with transition cost.

## Decisions to freeze before an efficacy trial

**Primary mechanistic decision:** Does measured passive return from descent remain materially useful after the observed habitual sitting interval? Choose a useful-effect threshold above the independently established measurement error before analyzing the intervention. An imprecise near-zero estimate is inconclusive.

**Transfer decision:** Does the training preserve or improve untrained walking/perturbation performance relative to an active comparator? Floor-rise speed alone is insufficient. Compare effects with uncertainty and the prespecified useful functional target.

**Dose decision:** Is the loading actually strong and frequent enough to produce the proposed adaptation? If the measured force/strain exposure is below an effective dose and no adaptation occurs, retain that negative finding. Do not retrospectively redefine habitual sitting as equivalent to heavy resistance training.

**Thermodynamic decision:** Does any economy improvement reflect reduced muscle work, changed activation, passive recovery, or an external assistance effect? Lower oxygen cost does not determine entropy production or an aging rate. Mechanical savings and chronic stimulus can oppose each other, so measure both rather than assuming a monotone longevity benefit.

**Longevity decision:** A later cohort or extended trial must independently address disability-free survival and mortality. The energy model generates no conversion from joules saved to years gained.

## Reproduction

From the report directory, execute `python3 validate_models.py`. This recreates the assumption-check JSON and the material-model CSV/JSON. To produce the Matplotlib PNG/SVG figure, execute `render_recoil.py` afterward in an environment containing Matplotlib. Both stages are CPU only. The figure was rendered successfully using `/home/sayuj/life/.venv/bin/python` and visually checked for readable labels and unclipped curves.

The previous unexecuted reset arithmetic is now independently verified in `assumption_checks.json`; its biological assumptions remain unidentified. No withdrawn rod conclusion, frozen human protocol, or manuscript is reinstated by these checks.
