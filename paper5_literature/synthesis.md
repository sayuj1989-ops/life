# Phase 2, Day 10: Synthesis and Mapping

## Formal Correspondence Table
This table maps the biomechanical/control engineering components of our Adolescent Idiopathic Scoliosis (AIS) model (Paper 2) directly onto the Free-Energy Principle (FEP) and Active Inference formalism (building on Baltieri & Buckley 2019).

| Paper 2 (PID / Biomechanics) | FEP / Active Inference Formalism | Mathematical Variable / Expression |
| :--- | :--- | :--- |
| Target Posture (Upright) | High-level Prior / Expected State | $\mu$ (or $v$ in hierarchical models) |
| Actual Posture (Angle) | Hidden State (Position) | $x$ (zeroth-order generalized coordinate) |
| Actual Postural Velocity | Hidden State (Velocity) | $x'$ (first-order generalized coordinate) |
| Proprioceptive Signal | Sensory Observation | $y = g(x) + \omega$ |
| Position Error | Sensory Prediction Error (Position) | $\varepsilon_{y,0} = y - \mu_y$ |
| Velocity Error | Sensory Prediction Error (Velocity) | $\varepsilon_{y,1} = y' - \mu_{y'}$ |
| **Proportional Gain ($K_p$)** | **Precision on Position Error** | **$\Pi_{y,0}$** |
| **Derivative Gain ($K_d$)** | **Precision on Velocity Error** | **$\Pi_{y,1}$** |
| **Integral Gain ($K_i$)** | **Precision on Prior / Learning Rate** | **$\Pi_{v,0}$** |
| Proprioceptive Delay ($\tau$) | Temporal Prediction Horizon | Time difference $(t)$ vs $(t-\tau)$ requiring forward integration: $y(t) \approx y(t-\tau) + \tau y'(t-\tau)$ |
| Growth Spurt ($v_g > 6$ cm/yr) | Fast Plant Parameter Change | $\dot{\theta}_{plant} > \text{Learning Rate}(\dot{\theta}_{model})$ |
| Model Misspecification | High Variance of Prediction Error | $\Sigma_{y,1} \uparrow$ |
| **Derivative Gain Gap** | **Velocity Precision Collapse** | **$\Pi_{y,1} \downarrow$ due to $\Sigma_{y,1} \uparrow$** |
| Postural Instability | Free-Energy Landscape Flattening | Loss of a deep global minimum at $x=0$ |
| Scoliotic Curvature | Local Free-Energy Minimum | A new stable attractor state $x \neq 0$ minimizing free energy under degraded precision |

## Mathematical Gaps to Fill in Phase 3
Baltieri & Buckley (2019) establish the mapping for $K_p$, $K_d$, and $K_i$ under a linear generative model. However, their base model does not explicitly account for:
1.  **Delay ($\tau$):** We must formally incorporate the proprioceptive delay $\tau$ into the generative model's observation equation $y(t)$. The brain must predict $x(t)$ given delayed observations $y(t-\tau)$. This is where the generalized coordinates (specifically the Taylor series expansion $y(t) \approx y(t-\tau) + \tau y'(t-\tau)$) become critical, emphasizing why velocity precision ($\Pi_{y,1}$) is so vital for stability.
2.  **Growth ($\dot{\theta}_{plant}$):** We need a specific formal term for the plant's parameters (e.g., mass $m$, length $l$, inertia $I$) changing continuously over time.
3.  **Precision Dynamics ($\dot{\Pi}_{y,1}$):** We must write the differential equation governing the precision update. When the prediction error $\varepsilon_{y,1}$ is persistently large (due to growth outpacing model updates), the estimated variance $\Sigma_{y,1}$ increases, causing $\Pi_{y,1}$ (and thus effective $K_d$) to drop.
