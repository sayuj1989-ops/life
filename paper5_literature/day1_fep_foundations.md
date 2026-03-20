# Day 1: Free-Energy Principle Foundations

## Core Concepts from Friston (2006, 2010)

This document synthesises the mathematical formalism of the free-energy principle (FEP) as established in Karl Friston's foundational papers: "A free energy principle for the brain" (2006, *J Physiol Paris*) and "The free-energy principle: a unified brain theory?" (2010, *Nat Rev Neurosci*). The goal is to lay the groundwork for bridging FEP with the delayed PID control model of postural stability developed in Paper 2.

### 1. The Imperative of Self-Organisation: Minimising Surprise

The FEP begins with a fundamental thermodynamic question: how do biological systems resist the natural tendency towards disorder (entropy) and maintain themselves in a restricted set of states?

Friston posits that biological systems must minimise the long-term average of *surprise* (or self-information) associated with their sensory states. If an organism maintains states that are highly probable (low surprise) given its phenotype, it survives.

Mathematically, let $y$ be the sensory states of the organism, and $m$ be the model (the organism's phenotype). Surprise is the negative log-evidence:

$$ \text{Surprise} = -\ln p(y \mid m) $$

However, the organism cannot evaluate $p(y \mid m)$ directly, as it requires marginalising over all possible hidden states of the world (causes), $x$, that could have generated the sensory data.

### 2. Variational Free Energy as a Tractable Bound

To solve this, the organism maintains an internal *generative model* of how hidden states $x$ cause sensory states $y$, denoted as $p(y, x \mid m)$. Furthermore, it maintains a *recognition density* or approximate posterior, $q(x)$, which represents its beliefs about the current hidden states given the sensory data.

The variational free energy, $F$, is defined as:

$$ F = -\langle \ln p(y, x \mid m) \rangle_q + \langle \ln q(x) \rangle_q $$
$$ F = \mathbb{E}_q[-\ln p(y, x \mid m)] - \mathcal{H}[q(x)] $$

Where $\mathcal{H}[q(x)]$ is the entropy of the recognition density.

Crucially, $F$ can be rearranged into two illuminating forms:

**Form 1: Surprise + Divergence**
$$ F = -\ln p(y \mid m) + D_{KL}[q(x) \parallel p(x \mid y, m)] $$
Since the Kullback-Leibler (KL) divergence is always non-negative, the free energy $F$ acts as an upper bound on surprise ($-\ln p(y \mid m)$). By minimising $F$, the organism implicitly minimises surprise. Additionally, minimising $F$ drives the recognition density $q(x)$ to approximate the true posterior $p(x \mid y, m)$.

**Form 2: Complexity - Accuracy**
$$ F = D_{KL}[q(x) \parallel p(x \mid m)] - \langle \ln p(y \mid x, m) \rangle_q $$
Here, the first term (complexity) measures how much the prior beliefs $p(x \mid m)$ must be updated to form the posterior $q(x)$. The second term (accuracy) measures the expected log-likelihood of the sensory data given the inferred states. Minimising $F$ therefore entails finding states that accurately explain the sensory data while minimising the complexity of the explanation (Occam's razor).

### 3. The Generative Model

The generative model $p(y, x \mid m)$ is central to the FEP. It factorises into a likelihood $p(y \mid x, m)$ and a prior $p(x \mid m)$. In continuous state-space models typical of motor control, this is often expressed using hierarchical dynamic models.

For a linear Gaussian generative model, the relationships are often expressed as:
$$ y = g(x) + z_y $$
$$ \dot{x} = f(x) + z_x $$
Where $z_y$ and $z_x$ are zero-mean Gaussian fluctuations (noise) with specific precisions (inverse variances) $\Pi_y$ and $\Pi_x$.

Under the Laplace assumption, the recognition density $q(x)$ is assumed to be Gaussian, fully parameterised by its mean $\mu$, meaning $q(x) = \mathcal{N}(\mu, \Sigma)$. The free energy then becomes a function of the sufficient statistics (the mean $\mu$):
$$ F(\mu, y) \approx \frac{1}{2} \epsilon_y^T \Pi_y \epsilon_y + \frac{1}{2} \epsilon_x^T \Pi_x \epsilon_x + \frac{1}{2} \ln |\Pi_y| + \frac{1}{2} \ln |\Pi_x| + C $$
Where $\epsilon_y = y - g(\mu)$ is the sensory prediction error, and $\epsilon_x = \dot{\mu} - f(\mu)$ is the state prediction error (or dynamics prediction error).

### 4. Active Inference: Minimising F through Action and Perception

The FEP states that the brain minimises free energy with respect to both internal states (perception) and sensory inputs (action). Let $a$ be action.

**Perception (Optimising $\mu$):**
The brain changes its internal representations to better predict sensory inputs.
$$ \dot{\mu} = -\frac{\partial F}{\partial \mu} $$
This gradient descent on free energy yields predictive coding schemes, where updating $\mu$ is driven by precision-weighted prediction errors.

**Action (Optimising $a$):**
The brain acts on the environment to change sensory inputs so they align with its predictions.
$$ \dot{a} = -\frac{\partial F}{\partial a} = -\frac{\partial F}{\partial y} \frac{\partial y}{\partial a} $$
Action does not change the internal model; it changes the world ($y$) to make the sensory data expected under the current model. This is the essence of *active inference*, replacing the classical notion of motor commands computing optimal trajectories with reflexes that suppress proprioceptive prediction errors.

### 5. The Role of Precision

Precision ($\Pi$) in these models is crucial. It acts as a gain factor on prediction errors. High precision means the error is heavily weighted (trusted); low precision means it is ignored. In the brain, precision is thought to be mediated by neuromodulators (like dopamine or acetylcholine) and relates to attention and uncertainty.

When bridging to the PID controller in Paper 2:
*   **Prediction error $\epsilon$** corresponds to the error signal (e.g., target angle - current angle).
*   **Precision $\Pi$** corresponds to the controller gains ($K_p$, $K_d$). A collapse in precision on velocity errors would mathematically equate to a degradation of the derivative gain ($K_d$).

### 6. Summary for Paper 5

To formally demonstrate that the delayed PID controller of Paper 2 is a special case of active inference:
1.  We must define the specific generative model $p(y, x, v \mid m)$ for the inverted pendulum trunk model.
2.  We must define the free energy functional for this model.
3.  We must show that the Euler-Lagrange equations for active inference ($\dot{a} = -\partial F / \partial a$) and perceptual inference ($\dot{\mu} = -\partial F / \partial \mu$) reduce to the PID control law, specifically highlighting the mapping between precision weights and PID gains ($K_p, K_d, K_i$).
4.  We must frame the "derivative gain gap" as a dynamic collapse in the precision assigned to generalised motion (velocity) due to the model becoming misspecified during rapid adolescent growth.

---
**References:**
*   Friston, K. J., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1-3), 70-87. https://doi.org/10.1016/j.jphysparis.2006.10.001
*   Friston, K. J. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138. https://doi.org/10.1038/nrn2787
