# Literature Review: Dream to Control & Active Inference

**Source:** Hafner et al., 2019, "Dream to Control: Learning Behaviors by Latent Imagination"

## Relevance to Paper 5 ("The Predictive Processing Bridge")

The Dreamer architecture offers a mathematically rigorous implementation of learning behaviors via a compact latent space. In the context of postural control and the biological countercurvature hypothesis, we conceptualize "Latent Imagination" as the central nervous system's capacity to simulate the consequences of motor commands on spinal alignment before execution.

### Key Components & Biological Analogues

1.  **World Model:** Dreamer learns a transition model ($p(s_t | s_{t-1}, a_{t-1})$), an observation model ($q(o_t | s_t)$), and a reward model ($q(r_t | s_t)$).
    *   *Biological Analogue:* This is the internal forward model of the spine's structural dynamics. The latent state $s_t$ represents the abstract postural configuration (e.g., aggregated spinal modes, orientation), while $o_t$ represents the raw proprioceptive and vestibular input.
2.  **Action Model:** Maximizes expected value by propagating analytic gradients through imagined trajectories.
    *   *Biological Analogue:* This represents higher-order motor planning (e.g., brainstem/cortical descending pathways) adjusting the setpoints of the lower-level spinal PID controllers to minimize long-term alignment errors (represented as "value").
3.  **Latent Imagination:** The agent optimizes behavior strictly within the learned latent space without interacting with the environment.
    *   *Biological Analogue:* The critical feature of predictive processing in complex motor control. The controller anticipates the destabilizing effects of growth or gravity and pre-emptively adjusts control gains (or "precisions") to maintain stability.
