# Day 1: Free-Energy Principle Foundations

## Core Concepts
The Free-Energy Principle (FEP), primarily developed by Karl Friston, asserts that all self-organising biological systems must minimise variational free energy to resist the second law of thermodynamics (entropy) and maintain their structural and functional integrity over time.

### Key Papers
1. **Friston, K. J. (2010). The free-energy principle: a unified brain theory? Nature Reviews Neuroscience, 11(2), 127-138. DOI: 10.1038/nrn2787**
   - Unifies action, perception, and learning under one imperative: minimising variational free energy, which is equivalent to minimising surprise (or negative log-evidence).
   - The brain maintains an internal **generative model** of the world and acts to make the sensory data it receives fit this model.

2. **Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. Journal of Physiology-Paris, 100(1-3), 70-87. DOI: 10.1016/j.jphysparis.2006.10.001**
   - Formulates perception as inference, building on Helmholtz's ideas.
   - Variational free energy represents an upper bound on surprise. By minimising it, the brain effectively performs approximate Bayesian inference on the hidden states of the world causing sensory input.

### Key Mathematical Formalism
Let $o$ be observations (sensory states), $s$ be hidden states, and $\mu$ be internal states of the brain (the parameters of the recognition density).

The surprise (or self-information) of sensory states is $-\ln p(o)$.
Variational free energy $F(o, \mu)$ is defined as:
$$ F(o, \mu) = E_q[-\ln p(o, s)] - H[q(s|\mu)] $$
Where:
- $q(s|\mu)$ is the recognition density (the brain's probabilistic representation of hidden states).
- $p(o, s)$ is the generative model mapping hidden states to observations.
- $H$ is the entropy of the recognition density.

Because $F \ge -\ln p(o)$, minimising $F$ with respect to $\mu$ (perception) and $o$ (action) ensures that the system avoids surprising states.

### Connection to Paper 5 (Predictive Processing Bridge)
- The PID controller for the trunk (Paper 2) is a mechanism for maintaining a target state (upright posture).
- Under FEP, this target state corresponds to the prior beliefs in the generative model.
- The control gains ($K_p$, $K_d$) must correspond to the precision (inverse variance) of the error signals in a hierarchical predictive coding architecture.
- Specifically, the derivative gain $K_d$ will relate to the precision of prediction errors on the temporal derivative of the hidden state (generalised motion).
