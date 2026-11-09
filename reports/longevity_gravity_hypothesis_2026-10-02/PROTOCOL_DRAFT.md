# Proposed study sequence and decision rules

Version 0.2, 2026-10-02. Planning document only; not preregistered, powered, approved, or executed. Each stage requires its own finalized protocol, human-research approval, and consent before participant work. Timelines are planning estimates. The [executed material model and evidence update](MODEL_AND_DECISIONS.md) inform the mechanistic measurements; they do not validate the proposed human experiment.

The [countercurvature/information extension](COUNTERCURVATURE_INFORMATION.md) proposes secondary analyses of sensing, prediction, and the control-performance/energy relationship. The untrained functional primary endpoint remains the same. Information estimators and physical entropy production require different measurements and must not be conflated.

## Stage 0: Validate what is being measured

Over approximately 2–4 weeks, validate a wearable-plus-sampled-observation method against independently annotated floor, chair, squat, kneeling, and standing transitions. Assess classifier precision/recall, count agreement, support-use errors, wear-time gaps, and missed transitions in people with different body sizes and movement strategies. A trunk sensor alone must not be assumed to identify posture or vertebral shape accurately.

Recruit across customary floor-use levels rather than assigning exposure by nationality. Record floor sitting duration, transition frequency, inter-bout intervals, walking, chair rises, sleep, symptoms, and other exercise. Characterize both within-person day-to-day variation and between-person variation. State consent and privacy rules for any video; clinical imaging is not required to answer this initial question.

**Decision:** Proceed only if exposure categories can be separated with errors small relative to the planned dose difference. Set numerical acceptance thresholds after engineering feasibility but before examining intervention outcomes. If discrimination fails, use observed supervised sessions; do not transform generic activity counts into assumed floor-rise counts.

## Stage 1: Supervised feasibility and dose calibration

Approximately 20–30 adults could support feasibility estimates, not a lifespan or efficacy claim. Include older adults for whom a physiotherapist judges supported floor transfers acceptable. Record exclusions and reasons so the selected sample's limits are explicit. Use stable supports and individualized transfer strategies; unsupported rising is not a training requirement.

Measure center-of-mass excursion, joint movement, support use, bout duration, symptoms, perceived exertion, and heart-rate response. In a subset, use indirect calorimetry and motion/force measurements if available. Heart rate alone is not a precise estimate of energy cost for short resistance bouts; IMUs alone do not provide joint moments without additional assumptions.

Calibrate a chair-rise or low-step comparator to a prespecified target such as net metabolic dose, with similar session duration, contact, and distribution. Report positive mechanical work and muscle-specific demand separately. Equal repetition counts do not mean equal work; metabolic dose, joint loading, and movement complexity cannot all be perfectly matched. Select the primary matching variable before efficacy testing and report residual differences.

Measure adherence, measurement repeatability, reasons for missed sessions, pain, orthostatic symptoms, near falls, and adverse events. Choose dose from tolerability and observed task demands, not the historical 50–100/day assumption.

**Decision:** Stop or redesign if floor exposure is not feasible, comparator doses cannot be distinguished or matched as planned, or clinically important harms appear. Do not recruit only exceptionally capable elders and generalize the result to frailty.

## Stage 1b: Identify recoil and its energy source

Before making a chronic recoil claim, establish repeatability of selected-tendon force–deformation measurements in a controlled task, then validate them during dynamic transfers. Compare descent followed by prompt reversal, a brief standardized pause, and a longer supported seated pause. Include a rise from an already seated state and a chair-rise control. Randomize order, allow rest, and match support use and endpoints where possible. Test two tolerable standardized rising durations independently of sitting-pause duration, if feasible: unloading rate and a stationary hold are different manipulations. The participant population and movement sequence must be suitable for supervised testing; this is not a proposal for ballistic rebound or a jumping task.

Use force measurements, motion capture, selected muscle-tendon ultrasound, and EMG to estimate tissue deformation and joint work. Measure hand, knee, foot, and seat support as relevant; foot forces alone may omit substantial load. Standardize preload, preconditioning, joint angle, and rest in the controlled measurement; account for antagonist activity and uncertainty in moment arms and deformation. Observe any muscle-driven preload immediately before rising. Pair with indirect calorimetry over repeatable bouts and recovery; breath-by-breath oxygen use cannot precisely assign energy to one short rise. Account for the energy of holding a posture separately when pause durations differ.

Prespecify a mechanical primary endpoint, such as returned energy in a selected, measurable tendon during the rise, with an explicit force-estimation uncertainty model. It is a tissue-specific result, not a whole-body recoil fraction. A recoil estimate requires force and deformation; EMG or improved rise time alone is insufficient. A lower net metabolic cost at equal task demands is a separate outcome.

**Decision:** If meaningful passive energy from the preceding descent is absent after a habitual sitting interval, reject descent-stored recoil as the explanation for that interval. Muscle-generated spring loading may still operate during the subsequent rise. If performance differences reflect altered muscle activation, changed support, or posture, do not label them passive recoil. Continue the broader coordination hypothesis separately.

## Stage 2: Test whether floor rising adds general functional benefit

Use a 12–16-week, individually randomized, assessor-blinded, parallel trial. Compare supported floor-rise practice with the calibrated chair/step programme. Match schedule, contact, and the selected dose measure; continue and measure participants' background activity. Stratify randomization by important baseline limitations. Avoid participant-unblinded self-report as the only outcome.

**Primary outcome:** Baseline-adjusted between-arm difference in usual gait speed at the prespecified end point. Use standardized distances, practice trials, equipment, footwear, and aids. This is an untrained outcome; floor-rise time and SRT are secondary because participants directly practice them. Pilot baseline data must identify whether this population has a ceiling problem before the confirmatory protocol is frozen.

**Secondary outcomes:** Perturbation-recovery performance, balance, hip/ankle mobility, lower-limb strength/power, independent transfer ability, life-space mobility, and symptoms. A mechanistic subset can repeat the calibrated recoil and metabolic measurements from Stage 1b, including transfer to an untrained walking task. Do not make an omnibus reserve index by weighting measures after seeing results. Falls can be recorded, but a short modest-size trial is unlikely to establish a falls effect.

Estimate intention-to-treat effects with confidence intervals, adjusting for baseline primary outcome and prespecified stratification variables. Freeze handling of missing data and support changes; report exposure separation and attrition. Per-protocol estimates are supportive and subject to adherence selection.

Use 0.05 m/s only as an initial meaningful-change planning anchor from [Perera et al.](https://pubmed.ncbi.nlm.nih.gov/16696738/). Justify the eventual between-arm target in this population. Compute sample size from a defensible residual variance, chosen power, attrition estimate, and two-sided error rate before enrollment; feasibility sample size is not confirmatory power.

**Interpretation:** A clinically meaningful, adequately precise advantage on the untrained endpoint supports incremental functional benefit. Improvement only in floor-rise performance supports task learning. A confidence interval excluding the prespecified useful benefit weakens that specific incremental claim. A wide interval is inconclusive, and a nonsignificant difference does not establish equivalence. Neither favorable result proves the proposed biological mediator or increased survival.

## Stage 3: Test timing independently

A separate randomized crossover study can compare distributed versus clustered *identical* movements, with the same daily total dose and standardized meals/background activity. An optional fully powered factorial design could examine movement type and distribution together, but the interaction requires its own power assessment.

Choose one acute primary outcome, for example postprandial glucose incremental area under the curve over a fixed observation period. Fix sampling, medication handling, washout, period/order effects, and session eligibility in advance. Measure actual dose and sedentary intervals. Generalize cautiously beyond the chosen metabolic population.

This experiment tests an acute timing effect. It cannot identify a two-hour decay of whole-body structural coupling, or determine whether distributing bouts improves chronic adaptation. Chronic timing requires a longer randomized comparison.

## Stage 4: Investigate healthspan and survival

Establish individual-level prospective follow-up in a population containing a meaningful range of measured exposure. Okinawa is one possible site, contingent on access and collaboration; a comparable non-Okinawan cohort also tests the mechanism. A cross-sectional survey of surviving centenarians cannot reconstruct a causal lifelong dose.

Collect baseline and repeated health, function, activity, diet, smoking, socioeconomic and social variables, chronic conditions, medication, fall history, and exposure. Use validated birth/death records, attained-age methods with appropriate delayed entry, and explicit loss-to-follow-up rules. Disability-free survival and all-cause mortality answer different questions; define a multistate or competing-event analysis for disability rather than counting death as harmless censoring.

Prespecify lagged-exposure analyses, exclusion/sensitivity analyses for early deaths, and handling of time-varying illness that both changes movement and affects outcomes. Adjustment for a post-exposure mediator is not the same as adjustment for baseline confounding. If an intervention later changes mortality, mediation still requires additional assumptions and measurements.

**Decision:** Claim only associations from an observational cohort unless identification assumptions justify more. Do not convert an SRT hazard ratio into years gained, an expected benefit per rise, or an Okinawan attributable fraction.

## Molecular work: only after the functional comparison is informative

Klotho can be an exploratory repeated biomarker with standardized time, hydration, renal function, and assay conditions. Tissue-specific signaling requires a separate justified sampling plan. Multiple protein tests need an error-control or explicitly exploratory analysis. A biomarker change is not a surrogate for lifespan, and a negative biomarker result does not automatically refute a well-measured functional effect.

## Assumptions to resolve earliest

| Assumption | Type | Qualitative risk | Earliest useful resolution |
|---|---|---|---|
| Floor exposure can be distinguished from general activity | Technical | High until validated | Stage 0, weeks |
| Safe practice provides a separable, comparable dose | Technical/clinical | Moderate, population dependent | Stage 1, weeks |
| Floor practice transfers beyond trained task | Biological | High uncertainty; discriminating claim | Stage 2, months |
| Distribution adds a benefit at fixed dose | Biological | Uncertain and endpoint dependent | Stage 3 acute study; chronic claim needs longer study |
| Short-term function predicts intervention-mediated survival | Biological/causal | High uncertainty, long horizon | Stage 4 or extended randomized follow-up, years |

These are judgments about project uncertainty, not numerical probabilities. Prioritize the exposure and active-comparator tests over an expensive protein panel or another uncalibrated rod simulation.
