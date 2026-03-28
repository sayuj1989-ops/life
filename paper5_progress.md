# Paper 5 Progress: The Predictive Processing Bridge

## Date: 2026-03-28
**Phase Completed:** Phase 1, Day 1 (Literature Review — Free-Energy Principle Foundations)

### Key Findings & Mathematical Insights
- Successfully retrieved verifiable DOIs for the foundational FEP papers by Friston (2006, 2010) using the Crossref API.
- Documented the core mathematical formalism of variational free energy: $F \ge -\ln p(\tilde{y} \mid m)$ and $F = D_{KL}[q(\vartheta) || p(\vartheta \mid \tilde{y})] - \ln p(\tilde{y})$.
- Outlined the "Generative Model" and "Active Inference" core concepts, bridging the theory of perception/action to maintaining posture within narrow physiological bounds.
- Developed the preliminary conceptual link to Paper 2: a rapid growth spurt causes generative model misspecification, raising prediction errors. If action (postural adjustments) attempts to minimise these errors using compromised predictions, the system may get stuck in a local free-energy minimum corresponding to scoliosis.

### Issues, Open Questions, or Points for Dr. Sayuj K.S.
- Dr. Sayuj, the mathematical formulation for the generative model of postural control (Day 11) will require mapping the specific terms of the delayed PID model (from Paper 2) to the variables ($\tilde{y}$, $\vartheta$, $m$) outlined in the FEP formalism today. I will focus on Baltieri & Buckley (2019) in Day 4 to ensure the mapping is robust.
- Are there specific variables from the Peterka (2002) PID model you would like prioritised in the mapping beyond $K_p$, $K_d$, $K_i$, and $\tau$?

### Next Session Plan
- **Phase 1, Day 2:** Active inference and motor control. I will review how FEP explains movement, posture, and reflexes, focusing on key papers by Friston et al. (active inference for motor control) and Adams et al. (optimal motor control under FEP, equilibrium-point hypothesis). Output to `paper5_literature/day2_active_inference_motor.md`.
