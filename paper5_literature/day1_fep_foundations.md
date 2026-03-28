# Phase 1, Day 1: Free-Energy Principle Foundations

**References:**
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138. DOI: 10.1038/nrn2787
- Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1-3), 70-87. DOI: 10.1016/j.jphysparis.2006.10.001

## Core Concepts

The Free-Energy Principle (FEP) proposes that all self-organising biological systems maintain their states within narrow physiological bounds by minimising variational free energy, a bound on "surprise" (negative log-evidence).

### 1. Surprise and Free Energy
For a biological system to resist the natural tendency towards disorder (entropy), it must minimise the Shannon entropy of its sensory states. This entropy is the long-term average of surprise (negative log-probability of sensory states).
Because an organism cannot evaluate this directly (it does not know the true state of the world), it instead minimises variational free energy ($F$), which provides an upper bound on surprise.

$$ F \ge -\ln p(\tilde{y} \mid m) $$

where $\tilde{y}$ are the sensory observations and $m$ is the generative model.

### 2. The Generative Model
The brain maintains an internal generative model $p(\tilde{y}, \vartheta \mid m)$ of how sensory data $\tilde{y}$ are caused by hidden states and causes $\vartheta$ in the world.
The free energy is defined in terms of this generative model and an internal recognition density $q(\vartheta)$ (the brain's probabilistic representation of the causes of its sensations):

$$ F = D_{KL}[q(\vartheta) || p(\vartheta \mid \tilde{y})] - \ln p(\tilde{y}) $$

Since the Kullback-Leibler (KL) divergence is non-negative, free energy is strictly greater than or equal to surprise. By minimising free energy, the system makes $q(\vartheta)$ an approximate posterior estimate of the true causes, and simultaneously minimises surprise.

### 3. Active Inference
Under the FEP, there are two ways to minimise free energy:
1. **Perception**: Change internal states (update $q(\vartheta)$) to better match the sensory input.
2. **Action**: Change the world or the body's configuration (via motor output) to generate sensory input that matches prior expectations (the predictions).

This formulation unifying perception and action is termed **Active Inference**.

## Relevance to Postural Control (Paper 2 & 5)
In the context of the Paper 2 PID model for adolescent scoliosis:
- The system maintains an upright posture (a state of low surprise / low free energy).
- A generative model of the body's dynamics predicts proprioceptive feedback.
- If the body grows rapidly, the generative model becomes miscalibrated (model misspecification).
- Consequently, prediction errors rise, meaning free energy rises. If perception cannot update the model fast enough, active inference requires action (motor adjustments) to minimise the error.
- However, if the predictions guiding action are also compromised, the system may settle into a local free-energy minimum corresponding to an asymmetric curvature (scoliosis) rather than the global minimum (symmetric upright posture).
