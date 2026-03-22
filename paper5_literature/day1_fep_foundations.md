# Day 1: Friston's Free-Energy Principle — Core Foundations

## Overview
This document reviews the foundational mathematical formalism of Karl Friston's Free-Energy Principle (FEP), focusing on variational free energy, surprise minimisation, generative models, and active inference. These concepts serve as the theoretical bedrock for "The Predictive Processing Bridge: Reframing Adolescent Scoliosis as a Free-Energy Catastrophe" (Paper 5).

## Core Concepts

### 1. Surprise and Variational Free Energy
The Free-Energy Principle postulates that self-organising biological systems must resist a natural tendency to disorder by minimising the entropy of their sensory and physiological states. In information-theoretic terms, this is equivalent to minimising **surprise** (or self-information), defined as the negative log-probability of sensory states $y$:
$$ -\ln p(y) $$
However, calculating true surprise directly is intractable, as it requires marginalising over all possible hidden states and causes $x$ in the environment:
$$ p(y) = \int p(y, x) dx $$
To circumvent this, the brain instead minimises a tractable upper bound on surprise called **variational free energy** ($F$). This is achieved by introducing an internal generative model $p(y, x)$ and a recognition density (or approximate posterior) $q(x)$ representing the brain's "best guess" about the hidden states.

The variational free energy is defined as:
$$ F = \mathbb{E}_{q(x)}[\ln q(x) - \ln p(y, x)] $$
Because $F = -\ln p(y) + D_{KL}[q(x) || p(x|y)]$, and the Kullback-Leibler (KL) divergence is always non-negative, $F$ is strictly an upper bound on surprise. By minimising $F$, the system implicitly minimises surprise and makes $q(x)$ a better approximation of the true posterior $p(x|y)$.

### 2. The Generative Model
The generative model represents the joint probability of sensory outcomes $y$ and hidden states $x$. Under the Laplace assumption, the recognition density $q(x)$ is assumed to be a Gaussian distribution parameterized by its mode $\mu$.
$$ p(y, x) = p(y | x) p(x) $$
The process of perception involves updating the internal states $\mu$ to minimise $F$, which can be achieved via gradient descent:
$$ \dot{\mu} = - \frac{\partial F}{\partial \mu} $$
This yields predictive processing: the brain generates top-down predictions of sensory input based on its generative model, compares them against actual bottom-up sensory input, and uses the resulting **prediction errors** to update $\mu$.

### 3. Active Inference
While perception updates internal states to match the world, **active inference** posits that the system can also change the world to match its predictions. This is done by performing actions $a$ that change the sensory outcomes $y$.
Crucially, motor control is cast not as the computation of optimal motor commands to achieve a goal, but as the fulfilment of descending proprioceptive predictions. The spinal cord executes reflexes to minimise proprioceptive prediction errors:
$$ \dot{a} = - \frac{\partial F}{\partial a} $$
Thus, both perception and action serve the single imperative of minimising variational free energy.

### 4. Precision
A critical component in this framework is **precision** ($\Pi$, the inverse variance of a distribution). Precision weights prediction errors based on their reliability. If a sensory signal is deemed noisy or unreliable, its precision is low, and the associated prediction error is down-weighted. Conversely, highly reliable predictions or observations carry high precision and strongly drive inference and action.
In the context of the derivative gain gap, we will show that precision collapse on generalised motion (velocity) corresponds to the degradation of the derivative gain $K_d$.

## Key References

### Friston 2010 (Nature Reviews Neuroscience)
This paper provides a comprehensive, accessible overview of the FEP as a unified brain theory, linking the information-theoretic formulation of free energy to brain structure and function, including predictive coding and active inference.

```bibtex
@article{Friston_2010,
  title={The free-energy principle: a unified brain theory?},
  volume={11},
  ISSN={1471-0048},
  url={http://dx.doi.org/10.1038/nrn2787},
  DOI={10.1038/nrn2787},
  number={2},
  journal={Nature Reviews Neuroscience},
  publisher={Springer Science and Business Media LLC},
  author={Friston, Karl},
  year={2010},
  month=jan,
  pages={127–138}
}
```

### Friston 2006 (Journal of Physiology-Paris)
This earlier work lays the rigorous mathematical foundation for the FEP, defining the formal relationships between surprise, variational free energy, and the updating equations for the recognition density under the Laplace assumption.

```bibtex
@article{Friston_2006,
  title={A free energy principle for the brain},
  volume={100},
  ISSN={0928-4257},
  url={http://dx.doi.org/10.1016/j.jphysparis.2006.10.001},
  DOI={10.1016/j.jphysparis.2006.10.001},
  number={1–3},
  journal={Journal of Physiology-Paris},
  publisher={Elsevier BV},
  author={Friston, Karl and Kilner, James and Harrison, Lee},
  year={2006},
  month=jul,
  pages={70–87}
}
```
