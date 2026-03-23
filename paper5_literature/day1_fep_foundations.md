# Phase 1, Day 1: Free-Energy Principle Foundations

## Core Papers
1. Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138. DOI: [10.1038/nrn2787](https://doi.org/10.1038/nrn2787)
2. Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1-3), 70-87. DOI: [10.1016/j.jphysparis.2006.10.001](https://doi.org/10.1016/j.jphysparis.2006.10.001)

## Variational Free Energy and Surprise Minimisation
The Free-Energy Principle (FEP) posits that any self-organising system that resists a tendency to disorder must minimise its variational free energy. Variational free energy ($F$) is an upper bound on surprise (negative log-model evidence, $-\ln p(y|m)$). By minimising $F$, the system implicitly maximises the evidence for its own existence (its phenotype or generative model $m$).

Mathematically, free energy is defined as:
$$ F \approx \text{Surprise} + \text{D}_{KL}(q(x) || p(x|y)) $$
where $q(x)$ is an approximate posterior distribution over hidden states $x$, and $p(x|y)$ is the true posterior. Since the Kullback-Leibler (KL) divergence is always non-negative, $F$ bounds surprise.

## Generative Models and Predictive Coding
To minimise $F$, the brain maintains a generative model $p(y, x, v, \theta)$ of how sensory data $y$ is caused by hidden states $x$ and causes $v$, parameterized by $\theta$.
Under Gaussian assumptions, $F$ reduces to a precision-weighted sum of squared prediction errors:
$$ F = \frac{1}{2} \sum_i \varepsilon_i^T \Pi_i \varepsilon_i - \frac{1}{2} \ln |\Pi_i| + C $$
where $\varepsilon_i = y_i - g(x_i)$ is the prediction error, and $\Pi_i$ is the precision (inverse variance) matrix.

## Active Inference
Systems can minimise free energy in two ways:
1. **Perception**: Update the internal state $x$ to better predict the sensory input (changing the mind to match the world).
2. **Action**: Change the sensory input $y$ to match the prediction (changing the world to match the mind). This is active inference. Posture and movement are cast as the fulfilment of descending proprioceptive predictions.

## Relevance to Paper 5 (The Predictive Processing Bridge)
- **$K_p$ (Proportional Gain)**: Maps to the sensory precision on positional prediction errors ($\Pi_x$).
- **$K_d$ (Derivative Gain)**: Maps to the sensory precision on velocity prediction errors (generalised motion, $\Pi_v$).
- **$K_i$ (Integral Gain)**: Maps to the prior precision on persistent causes or slow hyperparameter updating.
- **$\tau$ (Delay)**: Requires temporal prediction over the interval, where the system relies entirely on its generative model.
- **Derivative Gain Gap**: A catastrophic drop in $\Pi_v$ (precision collapse) due to model misspecification during rapid growth, leading to over-reliance on inaccurate generative predictions.
