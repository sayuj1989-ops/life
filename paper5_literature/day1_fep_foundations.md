# Phase 1, Day 1: Free-Energy Principle Foundations

## Core Papers
* Friston, K. J. (2010). The free-energy principle: a unified brain theory?. *Nature Reviews Neuroscience*, 11(2), 127-138. [DOI: 10.1038/nrn2787]
* Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1-3), 70-87. [DOI: 10.1016/j.jphysparis.2006.10.001]

## Summary of the Mathematical Formalism

### Variational Free Energy and Surprise Minimization
The free-energy principle (FEP) postulates that all self-organizing biological systems maintain their structural and functional integrity by minimizing variational free energy. Mathematically, free energy ($F$) provides a tractable upper bound on surprise (or negative log-evidence). Surprise is defined as $-\ln p(s|m)$, the negative log probability of observing sensory states $s$ given the agent's model $m$.

Since organisms cannot directly compute surprise (because it involves integrating over all possible hidden causes $v$ in the environment), they construct an internal generative model of how hidden states cause sensations. The brain approximates the true posterior distribution $p(v|s)$ with a recognition density $q(v)$. Variational free energy is then defined as:

$F = -\langle \ln p(s, v) \rangle_q + \langle \ln q(v) \rangle_q$

Alternatively, $F$ can be expressed as:
$F = \text{Surprise} + D_{KL}[q(v) || p(v|s)]$

Where $D_{KL}$ is the Kullback-Leibler divergence. Minimizing $F$ thus minimizes surprise while simultaneously making $q(v)$ a better approximation of the true posterior $p(v|s)$.

### Generative Models
A generative model $p(s, v)$ is the joint probability of sensory inputs and their hidden causes. It specifies how hidden states (e.g., body posture, environmental forces) generate sensory observations (e.g., proprioception, vision). For the brain, this involves a hierarchical mapping:
$s = g(v) + z$ (Sensory mapping)
$\dot{v} = f(v) + w$ (Dynamics)

Where $z$ and $w$ represent sensory noise and structural fluctuations. To minimize free energy, the brain uses this generative model to predict sensory inputs. The difference between predicted and actual sensory inputs constitutes prediction error.

### Active Inference
FEP suggests two ways to minimize free energy:
1. **Perceptual Inference**: Update the internal states $q(v)$ to make better predictions (minimize prediction error). This corresponds to perception and learning.
2. **Active Inference**: Change the sensory input $s$ to match the prediction by interacting with the environment. This corresponds to action (e.g., motor control). Action $a$ is selected to minimize free energy:
$a = \arg\min_a F(s(a), q)$

Under active inference, motor commands are not generated to achieve arbitrary goals but to fulfill prior beliefs about sensory trajectories (proprioceptive predictions). The reflex arc simply resolves proprioceptive prediction errors.
