# Phase 1, Day 1: FEP Foundations

## Core Papers Reviewed
- Friston, K. J. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138. DOI: [10.1038/nrn2787](https://doi.org/10.1038/nrn2787)
- Friston, K., Kilner, J., & Harrison, L. (2006). A free energy principle for the brain. *Journal of Physiology-Paris*, 100(1-3), 70-87. DOI: [10.1016/j.jphysparis.2006.10.001](https://doi.org/10.1016/j.jphysparis.2006.10.001)

## Mathematical Formalism of the Free-Energy Principle

### 1. Surprise (Negative Log-Evidence)
Biological systems must minimize the dispersion of their sensory states to maintain homeostasis and resist entropy. Mathematically, they minimize the long-term average of surprise (self-information), denoted as $H(s)$:

$$ \text{Surprise} = -\ln p(\tilde{s} | m) $$

Where:
- $\tilde{s}$ represents the sensory states (e.g., proprioceptive feedback in the spine) and their generalized motion over time.
- $m$ is the agent's phenotype or model of the world.

### 2. Variational Free Energy ($F$)
Because biological systems cannot evaluate the true surprise directly (as it requires integrating over all possible hidden causes), they minimize an upper bound on surprise called variational free energy ($F$). This is formulated using a recognition density $q(\vartheta)$ over hidden states $\vartheta$ (including environmental causes $v$, internal states $x$, and parameters $\theta$):

$$ F(\tilde{s}, \mu) = -\langle \ln p(\tilde{s}, \vartheta | m) \rangle_q + \langle \ln q(\vartheta | \mu) \rangle_q $$

Alternatively, using the Kullback-Leibler (KL) divergence:

$$ F = \underbrace{D_{KL}[q(\vartheta | \mu) || p(\vartheta | \tilde{s}, m)]}_{\text{Divergence}} - \underbrace{\ln p(\tilde{s} | m)}_{\text{Log-evidence (negative surprise)}} $$

Since the KL divergence is always non-negative, $F \geq -\ln p(\tilde{s} | m)$. Minimizing $F$ implicitly minimizes surprise and provides an approximate posterior distribution over hidden causes.

### 3. The Generative Model $p(\tilde{s}, \vartheta | m)$
The free energy rests on a generative model, typically formulated in generalized coordinates of motion (position, velocity, acceleration, etc.), denoted by the tilde ($\tilde{x} = [x, x', x'', \dots]^T$). A continuous-time, non-linear generative model under Gaussian assumptions takes the form:

$$ \tilde{s} = g(\tilde{x}, \tilde{v}, \theta) + \tilde{z}_s $$
$$ \dot{\tilde{x}} = f(\tilde{x}, \tilde{v}, \theta) + \tilde{z}_x $$

Where:
- $g$ represents the sensory mapping.
- $f$ represents the equations of motion (the dynamics of the plant, such as the inverted pendulum model in Paper 2).
- $\tilde{z}_s$ and $\tilde{z}_x$ are random fluctuations (noise) with precision matrices $\Pi_s$ and $\Pi_x$.

Under the Laplace assumption (where $q(\vartheta)$ is Gaussian with mean $\mu$), free energy becomes a precision-weighted prediction error:

$$ F \approx \frac{1}{2} \tilde{\varepsilon}^T \Pi \tilde{\varepsilon} - \frac{1}{2} \ln |\Pi| $$

Where $\tilde{\varepsilon}$ is the prediction error vector:
$$ \tilde{\varepsilon}_s = \tilde{s} - g(\tilde{\mu}_x, \tilde{\mu}_v, \mu_\theta) $$
$$ \tilde{\varepsilon}_x = \dot{\tilde{\mu}}_x - f(\tilde{\mu}_x, \tilde{\mu}_v, \mu_\theta) $$

### 4. Active Inference and Minimization
Free energy is minimized with respect to both internal states (perception/learning) and action (motor control). The dynamics of the system follow a gradient descent on $F$:

**Perception (State estimation):**
$$ \dot{\tilde{\mu}} = D\tilde{\mu} - \partial_{\tilde{\mu}} F $$
Where $D$ is the temporal derivative operator shifting generalized coordinates.

**Action (Motor control):**
$$ \dot{a} = -\partial_a F = -\partial_a \tilde{s} \cdot \partial_{\tilde{s}} F $$

Crucially, in active inference, actions $a$ only change the sensory data $\tilde{s}$. Motor commands are not computed as optimal control signals to reach a target; rather, the agent holds a strong prior (prediction) about its desired trajectory, generating a proprioceptive prediction error. Action simply minimizes this prediction error at the peripheral reflex arc.

## Relevance to Paper 5: The Derivative Gain Gap
For the scoliosis model:
- The generative function $f$ is miscalibrated during rapid growth because the physical parameters (mass, length of the trunk) change faster than the model parameters $\theta$ can update.
- This creates persistent prediction errors on generalized motion (specifically velocity, mapping to the derivative gain $K_d$).
- The system recognizes this unreliability, leading to a collapse in the precision matrix $\Pi$ assigned to velocity prediction errors.
- As $\Pi$ drops, the gradient descent on $F$ becomes impaired. Neither perception (updating $\mu$) nor action (minimizing $\varepsilon_s$ through posture) can effectively resolve the free energy. The adolescent spine may settle into a local free-energy minimum corresponding to a stable, but structurally asymmetric, curvature.
