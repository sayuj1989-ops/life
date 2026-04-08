# Paper 5: The Predictive Processing Bridge - Progress Tracker

## Current Status
**Phase 1, Day 3: Generalized Coordinates of Motion in Active Inference** - Completed (Date: 2026-04-03)

## Key Findings
- Reviewed core FEP papers (Friston 2010, Friston 2006) on Day 1.
- Day 2: Active inference reframes motor control (Adams et al. 2013). Motor commands are descending proprioceptive predictions, and movement occurs via classical reflex arcs suppressing proprioceptive prediction errors.
- The equilibrium-point hypothesis aligns with active inference: descending signals specify an equilibrium state (a prediction).
- Day 3: Understood Karl Friston's formalism for encoding velocity, acceleration, jerk etc., as "generalized coordinates of motion".
- The brain's generative model predicts trajectories $\tilde{x} = [x, x', x'', \dots]^T$ and calculates prediction errors in these coordinates $\tilde{\varepsilon} = [\varepsilon_x, \varepsilon_{x'}, \dots]^T$.
- The precision matrix $\Pi$ weights these errors. The precision of the 0th order error ($\Pi_0$) maps to proportional gain ($K_p$), and the precision of the 1st order error ($\Pi_1$) maps to derivative gain ($K_d$) (Baltieri & Buckley, 2017).
- Rapid adolescent growth causes systematic mismatches in velocity predictions, leading the system to down-weight $\Pi_1$ to minimize free energy. This is the Active Inference equivalent of the "derivative gain gap".

## Decisions / Issues
- The mathematical bridge is now solid: $K_d$ degradation $\equiv$ precision down-weighting of velocity prediction errors ($\Pi_1$).
- Next phase is to formalize this connection and write the mathematical methods bridging Paper 3 (PID control) and Paper 5 (Active Inference).

## Next Session Plan
- **Phase 2, Day 1:** Start math formalization in `paper5_math/`. Write down the PID equations from Paper 3 and re-derive them from the Free Energy gradient descent with respect to action, explicitly showing the $\Pi_0$ and $\Pi_1$ mappings.
