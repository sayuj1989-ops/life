# Phase 1, Day 1: FEP Foundations

## Core Papers
1. Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11, 127-138. DOI: 10.1038/nrn2787.
2. Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1-3), 70-87. DOI: 10.1016/j.jphysparis.2006.10.001.

## Key Concepts and Mathematical Formalism

### Variational Free Energy and Surprise
In the Free-Energy Principle (FEP), all self-organizing biological systems maintain their states within bounds by minimizing surprise. The surprise (or self-information) of sensory data $y$ is the negative log-probability $-\ln p(y)$. Since evaluating true surprise requires marginalizing over all hidden states and causes, the system instead minimizes an upper bound: the variational free energy $F$.

The free energy is defined as:
$$ F = \langle -\ln p(y, x, v, \theta) \rangle_q - H(q) $$

Alternatively, expressed via the Kullback-Leibler (KL) divergence:
$$ F = D_{KL}[q(x, v, \theta) || p(x, v, \theta | y)] - \ln p(y) $$

Because KL divergence is always non-negative, $F \ge -\ln p(y)$. By changing its internal states to minimize $F$, the system minimizes the surprise of its sensory data.

### Generative Models
The system embodies a generative model $p(y, x, v, \theta)$ mapping hidden states ($x$), hidden causes ($v$), and parameters ($\theta$) to sensory observations ($y$). The generative density is typically formulated as a hierarchical dynamic model, often using a linear Gaussian assumption. The dynamic evolution of the system can be expressed in generalized coordinates of motion (position, velocity, acceleration, etc.).

### Active Inference
The system minimizes free energy in two ways:
1. **Perception**: Changing the internal state (the approximate posterior $q$) to make it a better match for the true posterior, given the sensory data. This is typically implemented via predictive coding schemes (gradient descent on free energy).
2. **Action**: Changing the sensory data $y$ by acting on the world to make it conform to the predictions of the generative model.

In both perception and action, precision (inverse variance) plays a crucial role. Prediction errors are weighted by their precision. When precision is high, prediction errors have a stronger influence on updating the model or driving action.

## Relevance to PID Control
Baltieri & Buckley (2019) demonstrated that PID control can be formulated as active inference under a specific linear generative model. In our framework, we map:
- $K_p \leftrightarrow$ precision on position errors (sensory precision).
- $K_d \leftrightarrow$ precision on generalized motion (velocity prediction errors).
- $K_i \leftrightarrow$ prior precision on persistent causes.
- $\tau \leftrightarrow$ sensory delay requiring reliance on the forward model.

A key focus for this paper will be formalizing how rapid growth (the "plant" changing faster than the model parameters $\theta$ can update) systematically biases velocity predictions, leading to an adaptive down-weighting of $K_d$ (precision collapse).
