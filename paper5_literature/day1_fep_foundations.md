# Phase 1, Day 1: Free-Energy Principle Foundations

**Objective:** Review core papers establishing Friston's free-energy principle, focusing on the mathematical formalism of variational free energy, surprise minimisation, generative models, and active inference.

## Key Papers

1. **Friston, K. J. (2010). The free-energy principle: a unified brain theory?**
   *Nature Reviews Neuroscience, 11*(2), 127-138.
   DOI: 10.1038/nrn2787
   *   **Core Concepts:** Optimization of value (expected reward) or surprise (prediction error, negative log-evidence). Unification of brain theories (neural Darwinism, optimal control, etc.) under the FEP framework.
   *   **Relevance:** Establishes the foundation that all self-organising systems minimise variational free energy.

2. **Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain.**
   *Journal of Physiology-Paris, 100*(1-3), 70-87.
   DOI: 10.1016/j.jphysparis.2006.10.001
   *   **Core Concepts:** Mathematical formulation of Helmholtz's ideas about perception. Explains perceptual inference and learning using constructs from statistical physics.
   *   **Relevance:** The foundational mathematical text for FEP, defining the generative model and the free-energy bound on surprise.

## Mathematical Formalism

The Free Energy Principle (FEP) posits that biological systems maintain their integrity by minimising the Shannon entropy of their sensory states, which is equivalent to minimising surprise (or negative log-evidence, $-\ln p(\tilde{y} | m)$). Since surprise cannot be evaluated directly, systems minimise a variational upper bound called *free energy* ($\mathcal{F}$).

$$ \mathcal{F} = \mathbb{E}_q [-\ln p(\tilde{y}, \tilde{x})] - \mathcal{H}[q(\tilde{x})] $$
$$ \mathcal{F} = D_{KL}[q(\tilde{x}) || p(\tilde{x} | \tilde{y})] - \ln p(\tilde{y}) $$

Where:
*   $\tilde{y}$ represents sensory observations (and their generalised motion).
*   $\tilde{x}$ represents hidden states in the world causing the observations.
*   $p(\tilde{y}, \tilde{x})$ is the *generative model*, detailing how hidden states cause sensory inputs.
*   $q(\tilde{x})$ is the *recognition density* (the brain's internal representation or posterior belief about the hidden states).
*   $D_{KL}$ is the Kullback-Leibler divergence.

Because $D_{KL} \geq 0$, free energy $\mathcal{F}$ is always an upper bound on surprise $-\ln p(\tilde{y})$. Minimising $\mathcal{F}$ achieves two things:
1.  **Perceptual Inference:** It makes the recognition density $q(\tilde{x})$ a better approximation of the true posterior $p(\tilde{x} | \tilde{y})$ (minimising the KL divergence).
2.  **Active Inference:** It minimises the surprise of the sensory data itself by changing the sensory data via action (changing $\tilde{y}$).

## Implications for Paper 5

*   The PID controller developed in Paper 2 must be shown to perform the equivalent of minimising $\mathcal{F}$.
*   The "plant" (human trunk) and its dynamics constitute the generative model $p$.
*   The controller state corresponds to the recognition density $q$.
*   Crucially, the generative model must be linear Gaussian to yield standard PID-like equations, where prediction errors correspond to the difference between predicted and actual states, precision-weighted.
