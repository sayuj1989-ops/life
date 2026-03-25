# Dream to Control: Learning Behaviors by Latent Imagination

## Reference
**Title:** Dream to Control: Learning Behaviors by Latent Imagination
**Authors:** Danijar Hafner, Timothy Lillicrap, Jimmy Ba, Mohammad Norouzi
**Year:** 2019
**DOI:** 10.48550/arXiv.1912.01603
**URL:** https://arxiv.org/abs/1912.01603

## Abstract / Summary
Learned world models summarize an agent's experience to facilitate learning complex behaviors. While learning world models from high-dimensional sensory inputs is becoming feasible through deep learning, there are many potential ways for deriving behaviors from them. We present Dreamer, a reinforcement learning agent that solves long-horizon tasks from images purely by latent imagination. We efficiently learn behaviors by propagating analytic gradients of learned state values back through trajectories imagined in the compact state space of a learned world model. On 20 challenging visual control tasks, Dreamer exceeds existing approaches in data-efficiency, computation time, and final performance.

## BibTeX
```bibtex
@article{hafner2019dreamer,
  title={Dream to Control: Learning Behaviors by Latent Imagination},
  author={Hafner, Danijar and Lillicrap, Timothy and Ba, Jimmy and Norouzi, Mohammad},
  journal={arXiv preprint arXiv:1912.01603},
  year={2019}
}
```

## Relevance to Paper 5: The Predictive Processing Bridge
This paper introduces the "Dreamer" reinforcement learning agent, which solves long-horizon tasks from images purely by *latent imagination*. This is highly relevant to our work in Paper 5 ("The Predictive Processing Bridge"), where we explore predictive processing, active inference, and internal generative models.

**Key Connections:**
1. **Mapping Latent Imagination to Active Inference:** Dreamer's use of a learned world model to predict into the future and imagine trajectories in a compact latent space parallels the active inference framework, where agents maintain an internal generative model of their environment to predict and minimize surprise (variational free energy). Both rely on internal simulation to optimize behavior before acting.
2. **Delayed Observations & Latent State Representation:** By projecting high-dimensional images into a compact latent space, Dreamer creates a robust representation that can handle temporal dependencies. In biological systems (like the spinal proprioceptive network modeled in our work), delayed observations are a key challenge. A latent world model that can predict future states helps compensate for these sensory delays (e.g., the $\tau$ delay in proprioception).
3. **Precision Collapse Dynamics:** Dreamer optimizes value estimates by backpropagating analytic gradients through imagined trajectories. If the world model becomes inaccurate or decoupled from reality, the imagined trajectories degrade. This is conceptually similar to "precision collapse" in predictive processing, where a failure to properly weight sensory evidence versus prior predictions leads to maladaptive behavior or structural collapse (as proposed in our models of spinal deformity).
