# Dreamer Integration Roadmap for Spinal Modeling

**Concept:** Based on "Dream to Control" (Hafner et al., 2020), this integration maps Latent Imagination to the active inference of spinal counter-curvature.

1.  **Objective:** Expand `experiment_latent_imagination.py` to use a lightweight neural transition model (similar to PlaNet/Dreamer) instead of a simple linear state predictor. This model will learn to predict the delayed postural state under gravitational loading.
2.  **Simulation Environment:** Create a PyElastica-based OpenAI Gym environment where an agent controls muscle moments to maintain an S-shape despite a growing length ($L$) and increasing sensorimotor delays ($\tau$).
3.  **The "Dreamer" Agent:** The agent will learn a latent transition model of the spine. The "Derivative Gain Trap" will be simulated by physically increasing $L$, which delays the observation stream. If the world model adapts quickly enough, latent imagination will stabilize the spine. If $L$ grows too fast, the agent will suffer precision collapse and trigger scoliotic buckling.
4.  **Requirements:** This will require TensorFlow 2 as per the original prompt's recommendation: "we recommend the newer implementation of Dreamer in TensorFlow 2".
