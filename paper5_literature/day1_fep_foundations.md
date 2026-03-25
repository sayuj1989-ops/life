# Day 1: Free-Energy Principle Foundations

## Core Papers
* Friston, K. J. (2010). The free-energy principle: a unified brain theory? Nature Reviews Neuroscience, 11(2), 127-138. DOI: 10.1038/nrn2787
* Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. Journal of Physiology-Paris, 100(1-3), 70-87. DOI: 10.1016/j.jphysparis.2006.10.001

## Key Concepts
1. **Variational Free Energy**: An upper bound on "surprise" (negative log marginal likelihood). By minimizing free energy, a biological system avoids phase transitions and maintains homeostasis.
2. **Surprise Minimization**: Formally defined as $-\ln p(y|m)$, where $y$ is sensory data and $m$ is the model (the agent). Agents minimize the Shannon entropy of their sensory states over time.
3. **Generative Models**: Formulated as $p(y, \vartheta|m)$, where $\vartheta$ includes hidden states $x$, causes $v$, and parameters $\theta$. The recognition density $q(\vartheta)$ approximates the true posterior $p(\vartheta|y,m)$.
4. **Active Inference**: The agent minimizes free energy by changing its internal states (perception, updating $q(\vartheta)$) or its sensory inputs (action, changing $y$).

## Mathematical Foundations
The free energy $\mathcal{F}$ is defined as:
$\mathcal{F} = \text{Surprise} + \text{D}_{KL}(q(\vartheta) || p(\vartheta|y))$
Since the Kullback-Leibler divergence is non-negative, free energy bounds surprise. Minimizing $\mathcal{F}$ with respect to internal states minimizes the divergence (approximate Bayesian inference), and minimizing it with respect to action minimizes surprise directly.

This forms the theoretical backbone for understanding the PID controller in Paper 2 as a system minimizing free energy under a specific generative model.
