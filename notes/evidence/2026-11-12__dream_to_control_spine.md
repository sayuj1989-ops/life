# Evidence Note: Spinal Control via Latent Imagination (Dream to Control)

**Date:** 2026-11-12
**Topic:** Reinforcement Learning / Latent Imagination / Active Inference
**References:** Hafner et al. (2019) "Dream to Control"

## 1. The Claim
The vertebrate spine, when modeled as an Active Inference agent, utilizes a mechanism analogous to "Latent Imagination" (as detailed in Dreamer) to predict and optimize long-horizon behaviors (e.g., maintaining upright posture against gravity over a lifetime). Instead of reacting purely to immediate sensory feedback (model-free), the spinal control system (e.g., via the cerebellum or local spinal circuits) learns a "world model" of spinal mechanics and gravity, allowing it to "dream" or simulate future trajectories to optimize muscle tone and counter-curvature.

## 2. Mechanism
*   **World Model:** The CNS maintains a compact, latent representation of the spine's Cosserat rod dynamics and the external gravitational field.
*   **Latent Imagination:** The system simulates future states (imagined trajectories) within this latent space to predict the consequences of different muscle activation patterns.
*   **Value and Action Models:** A value model evaluates the "goodness" (e.g., energetic efficiency, stability) of these imagined states, while an action model optimizes the motor commands (proprioceptive gains) by backpropagating gradients through the world model.

## 3. Relevance to Counter-Curvature
The "Dream to Control" framework provides a computational basis for how the CNS could solve the complex, high-dimensional control problem of maintaining the S-curve. The "Counter-Curvature" ($I$ term) might be the learned, optimal latent state that the action model strives to maintain. Scoliosis could represent a failure of this world model (e.g., due to noisy vestibular input or growth spurts), leading to erroneous "imagined" trajectories and maladaptive motor commands.

## 4. Hypothesis Integration
*   This aligns with **H_2025_02_20_Active_Inference** by offering a specific algorithmic mechanism (model-based RL via latent imagination) for how prediction errors are minimized and priors are formed.

## 5. Open Question & Proposed Test
**Question:** Does a model-based RL agent using latent imagination better capture the failure modes of human spinal control than a model-free agent?

**Proposed Test:**
*   **Protocol:** Implement a Dreamer-based agent to control a simulated Cosserat rod under noisy gravitational/vestibular input, and compare its performance (and failure modes) to a standard model-free PPO agent.
*   **Measure:** Divergence of the emergent scoliotic curvature pattern from clinical AIS progression curves.
*   **Prediction:** The latent imagination agent will exhibit 'geometric hallucinations' (smooth but structurally unstable curves) under sensory conflict, accurately mirroring idiopathic deformities, whereas the model-free agent will exhibit localized chaotic collapse.
