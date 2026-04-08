# Phase 1, Day 3: Generalized Coordinates of Motion in Active Inference

## Goal
Understand Karl Friston's formalism for encoding velocity, acceleration, jerk etc., as "generalized coordinates of motion" and how precision on generalized motion relates to derivative control ($K_d$).

## Key Concepts from Literature
In Active Inference (e.g., Friston et al. 2010 "Action and behavior: a free-energy formulation", and subsequent robotics applications like Pio-Lopez et al. 2016), continuous dynamics are framed using "generalized coordinates of motion".

1. **Generalized Coordinates**: A state $x$ is expanded into a vector $\tilde{x} = [x, x', x'', \dots]^T$, where $x'$ is velocity, $x''$ is acceleration, etc.
2. **Generative Model in Generalized Coordinates**: The brain's generative model predicts not just the current sensory state, but its trajectory (derivatives).
3. **Prediction Errors**: Prediction errors are also calculated in generalized coordinates: $\tilde{\varepsilon} = [\varepsilon_x, \varepsilon_{x'}, \dots]^T$.
4. **Precision Weighting ($\Pi$)**: The precision matrix $\Pi$ weights these prediction errors. $\Pi$ is typically block-diagonal or structured, with different precisions assigned to different orders of motion (e.g., $\Pi_0$ for position, $\Pi_1$ for velocity).
5. **Gradient Descent on Free Energy ($F$)**: State estimation and action minimize free energy. The dynamics of internal states and action involve gradient descent. The contribution of the velocity prediction error $\varepsilon_{x'}$ to the gradient is weighted by its precision $\Pi_1$.
6. **Connection to PID Control**: Friston and colleagues (e.g., in robotic active inference papers like Baltieri and Buckley 2017, "An active inference implementation of phototaxis") have shown that active inference maps onto PID control. Specifically:
   - Precision of the 0th order prediction error ($\Pi_0$) maps to proportional gain ($K_p$).
   - Precision of the 1st order prediction error ($\Pi_1$) maps to derivative gain ($K_d$).
   - (Sometimes) integral gain relates to updating the baseline or higher-order states.

## Relevance to the "Derivative Gain Gap"
Our paper (Paper 3) proposes a "derivative gain gap" where rapid growth outpaces sensory adaptation, functionally degrading $K_d$.

Translated to Active Inference:
Rapid adolescent growth $\rightarrow$ systematically increased lag between predicted velocity and actual sensory velocity $\rightarrow$ persistent high velocity prediction errors ($\varepsilon_{x'}$) $\rightarrow$ the system infers that velocity sensory channels are "noisy" or unreliable $\rightarrow$ the precision of velocity prediction errors ($\Pi_1$) is down-weighted to minimize free energy.

Because $\Pi_1$ is functionally equivalent to $K_d$ in the motor reflex arc, a drop in $\Pi_1$ *is* the derivative gain gap.

## Falsifiable Tests / Mathematical Bridge
- The PID controller for posture from Paper 3 ($u = -K_p e - K_d \dot{e}$) can be re-derived as active inference on generalized coordinates where action $a = -\frac{\partial F}{\partial a} \approx -\Pi_0 \varepsilon_x - \Pi_1 \varepsilon_{x'}$.
- We can computationally model telomere-driven senescence as an inability to up-regulate $\Pi$ (precision) globally, while growth locally degrades $\Pi_1$.

## Citations
- Friston, K., Mattout, J., & Kilner, J. (2006). Action understanding and active inference. *Biological cybernetics*, 95(2), 137-160.
- Friston, K. J., Daunizeau, J., Kilner, J., & Kiebel, S. J. (2010). Action and behavior: a free-energy formulation. *Biological cybernetics*, 102(3), 227-260.
- Pio-Lopez, L., Nizard, A., Friston, K., & Pezzulo, G. (2016). Active inference and robot control: a case study. *Journal of The Royal Society Interface*, 13(122), 20160616.
- Baltieri, M., & Buckley, C. L. (2017). An active inference implementation of phototaxis.
