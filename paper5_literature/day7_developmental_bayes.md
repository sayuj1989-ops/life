# Phase 2, Day 7: Bayesian models of sensorimotor development

## Core Concepts
How do children update their internal body models (body schema) during physical growth?
- **Continuous Calibration:** The sensorimotor system must constantly re-calibrate the mapping between motor commands (predictions) and sensory feedback.
- **Learning Rate vs. Growth Rate:** The generative model updates its parameters (e.g., limb lengths, mass, inertia) at a certain *learning rate*. If physical growth (e.g., peak height velocity during puberty) exceeds this learning rate, the model becomes misspecified.
- **Precision Weighting in Development:** As children grow, they must dynamically adjust how much they rely on priors vs. sensory evidence.

## Puberty and Prediction Error
- During the adolescent growth spurt, long bones elongate rapidly, and muscle mass changes. This significantly alters the biomechanics of the human plant (the body).
- The internal model predicts sensory consequences based on an *outdated* physical body. This generates persistent sensory prediction errors, particularly during movement (velocity, acceleration).
- In a Bayesian framework, persistent, unresolvable prediction errors are interpreted as "noise" or unreliability in that specific sensory channel. The optimal response is to down-weight the precision of those signals.

## Relevance to Adolescent Idiopathic Scoliosis (AIS)
1. **The "Adolescent Clumsiness" Phenomenon:** It is well-documented that adolescents experience a temporary decrease in motor coordination during peak growth. This is the behavioral manifestation of the generative model struggling to keep up with the changing plant.
2. **Postural Control Vulnerability:** Postural stability in the upright human requires a highly tuned model of the body's inverted pendulum dynamics. A mismatch in this model (especially regarding velocity predictions, leading to $\Pi_{y,1}$ drop) creates a specific vulnerability window.
3. **The Derivative Gain Gap:** The Bayesian formulation provides a principled reason *why* the derivative gain ($K_d$) degrades during rapid growth: the system optimally reduces reliance on unreliable velocity predictions.
