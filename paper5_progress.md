# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 3 & Phase 3 Modeling**: Completed (Date: 2026-04-03)

## Key Findings
- **Literature**: Reviewed Baltieri & Buckley (2019) demonstrating that PID control maps perfectly onto active inference with linear generative models. Derivative gain ($K_d$) is proportional to the precision of velocity prediction errors ($\Pi_{y_1}$).
- **Math Formulation**: Documented the mapping in `paper5_math/PID_active_inference.md`. The "Derivative Gain Gap" in scoliosis can now be formalized as a rapid decay in velocity error precision ($\Pi_{y_1} \to 0$) due to generative model failure during rapid skeletal growth.
- **Dreamer Connection**: Conceptually linked the generative model of active inference to Hafner's Dreamer latent world models. When the internal world model fails to predict rapid morphological changes, it down-weights precision, leading to control failure.
- **Simulation**: Implemented a proof-of-concept active inference postural control model in `paper5_model/active_inference_posture.py`. The model successfully demonstrates that dropping $\Pi_v$ (velocity precision) replicates the oscillatory instability seen in the PyElastica Cosserat models. Outputs saved to `paper5_figures/active_inference_posture.png`.

## Decisions / Issues
- The analogy between precision and derivative gain holds robustly in simulation.
- The use of generalized coordinates of motion natively resolves the issue of representing temporal derivatives in the brain.

## Next Session Plan
- **Phase 4, Day 1:** Begin drafting the manuscript (`paper5_draft/sections/`). Outline the introduction, mapping the clinical observations of Adolescent Idiopathic Scoliosis (AIS) to the Predictive Processing framework. Integrate findings from the Dreamer world model analogy.
