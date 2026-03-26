# Phase 1, Day 1: FEP Foundations

## Core Papers Reviewed
1. Friston, K. J. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138. DOI: 10.1038/nrn2787
2. Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1-3), 70-87. DOI: 10.1016/j.jphysparis.2006.10.001

## Key Concepts
### Variational Free Energy & Surprise Minimization
- The Free Energy Principle (FEP) posits that biological systems maintain their states against the dispersing forces of the environment by minimizing variational free energy, an upper bound on surprise (negative log-evidence).
- Surprise, $-\ln p(y|m)$, bounds the improbability of sensory states $y$ given a model $m$. Because surprise itself cannot be evaluated directly, systems minimize free energy $F(s, y)$, which relies on internal states $s$.

### Generative Models
- The brain embodies a generative model of the world $p(y, \vartheta)$ mapping hidden causes $\vartheta$ to sensory inputs $y$.
- By continuously updating internal states (perception) to minimize prediction errors, the system effectively approximates the posterior distribution $p(\vartheta|y)$.

### Active Inference
- Free energy is minimized not only by updating internal models to match sensory data (perception) but also by acting on the world to change sensory data to match predictions (action).
- This unifies perception and motor control under a single imperative: prediction error minimization.
