# Day 1: Free-Energy Principle Foundations

**Target Papers:**
- Friston K. (2010). The free-energy principle: a unified brain theory? *Nat Rev Neurosci* 11, 127–138. DOI: 10.1038/nrn2787
- Friston K., Kilner J., Harrison L. (2006). A free energy principle for the brain. *J Physiol Paris* 100(4), 70-87. DOI: 10.1016/j.jphysparis.2006.10.001

## Core Concepts

The Free-Energy Principle (FEP) dictates that any self-organising biological system that resists a tendency to disorder must minimise its variational free energy. Variational free energy represents an upper bound on surprise (or negative log-evidence).

1.  **Surprise (Surprisal):** The negative log probability of a sensory state $s$ given a model $m$: $- \ln p(s \mid m)$. The system aims to avoid surprising, non-viable states.
2.  **Variational Free Energy ($F$):** Since the system cannot directly evaluate the true surprise (because it involves integrating over all possible hidden causes), it evaluates a bound ($F$). Minimising $F$ implicitly minimises surprise.
3.  **Generative Model:** The system contains a statistical model mapping hidden causes in the world to sensory consequences. $p(s, \vartheta \mid m) = p(s \mid \vartheta) p(\vartheta)$ where $s$ are sensory states and $\vartheta$ are the hidden causes and parameters.
4.  **Recognition Density:** The system's internal representation or "best guess" about the hidden states, denoted by $q(\vartheta)$.
5.  **Active Inference:** The system can minimise $F$ in two ways:
    *   **Perceptual Inference:** Updating the internal model (the recognition density $q(\vartheta)$) to better match the sensory input.
    *   **Active Inference (Action):** Changing the world to make sensory input match the internal model's predictions. The system performs actions $a$ that change the sensory states $s$ to align with prior expectations.

## Mathematical Formalism

The free energy $F$ is defined with respect to sensory states $s$, an internal state $\mu$ (which parametrizes the recognition density $q$), and the generative model $m$:

$$F(s, \mu) = \mathbb{E}_q [-\ln p(s, \vartheta \mid m)] - H[q(\vartheta \mid \mu)]$$

Where:
*   $\mathbb{E}_q$ is the expectation under the recognition density $q$.
*   $p(s, \vartheta \mid m)$ is the generative model (joint probability of sensory data and hidden states).
*   $H[q]$ is the Shannon entropy of the recognition density.

Alternatively, $F$ can be decomposed into:

$$F(s, \mu) = D_{KL}[q(\vartheta \mid \mu) \parallel p(\vartheta \mid s, m)] - \ln p(s \mid m)$$
$$F(s, \mu) = \text{Complexity} - \text{Accuracy}$$

*   **Complexity:** The Kullback-Leibler (KL) divergence between the recognition density (posterior guess) and the true prior.
*   **Accuracy:** The expected log-likelihood of the data given the model.

**Gradient Descent:**
The system acts to minimise $F$ with respect to its internal states $\mu$ and actions $a$:

$$\dot{\mu} = - \frac{\partial F}{\partial \mu}$$
$$\dot{a} = - \frac{\partial F}{\partial a}$$

*Note: In future sections, we will map this to the PID controller from Paper 2, showing that PID parameters ($K_p, K_i, K_d$) emerge from specific precision structures in these gradient descent equations under a linear Gaussian generative model.*
