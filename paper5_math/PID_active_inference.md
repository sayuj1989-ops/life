# Mathematical Derivation: Active Inference and the Derivative Gain Gap

**Date**: 2026-04-03

## Formalism of Generalised Coordinates
Following Friston's formalism, let the hidden states in generalised coordinates be $\tilde{\mu} = [\mu, \mu', \mu'']^T$, and the sensory data be $\tilde{y} = [y, y', y'']^T$.

The prediction errors at the sensory level are defined as:
$$ \varepsilon_y = \tilde{y} - g(\tilde{\mu}) $$

Where $g(\cdot)$ is the generative mapping from hidden states to sensory consequences.

## The Baltieri-Buckley Mapping
As demonstrated by Baltieri & Buckley (2019), for a linear generative model $g(\mu) = \mu$, the gradient descent on free energy $F$ with respect to action $a$ yields a motor control signal.

Action minimizes sensory prediction errors:
$$ \dot{a} = -\frac{\partial F}{\partial a} \approx -\frac{\partial \tilde{y}}{\partial a} \cdot \Pi_y \cdot \varepsilon_y $$

Expanding the prediction error precision matrix $\Pi_y$ into position and velocity components (assuming diagonal):
$$ \Pi_y = \text{diag}(\Pi_{y_0}, \Pi_{y_1}, \dots) $$

The control signal effectively takes the form:
$$ u(t) = K_p e(t) + K_d \dot{e}(t) + K_i \int e(t) dt $$

Where:
- $K_p \propto \Pi_{y_0}$ (Precision of position error)
- $K_d \propto \Pi_{y_1}$ (Precision of velocity error) [VERIFY]

## The Predictive Processing Bridge to AIS
If Adolescent Idiopathic Scoliosis (AIS) is driven by a "Derivative Gain Gap" during rapid growth, this translates in the Active Inference framework to an uncoupling of the velocity precision $\Pi_{y_1}$. Rapid bone growth shifts the sensorimotor plant's dynamics faster than the internal generative model can update its priors. The resulting epistemic uncertainty leads the brain to down-weight $\Pi_{y_1}$ (i.e., $K_d \to 0$), which causes oscillatory instability and buckling of the spine under gravitational load.
