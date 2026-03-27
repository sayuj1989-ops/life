# Dream to Control: Learning Behaviors by Latent Imagination

**Authors**: Danijar Hafner, Timothy Lillicrap, Jimmy Ba, Mohammad Norouzi
**Citation**:
@article{hafner2019dreamer,
  title={Dream to Control: Learning Behaviors by Latent Imagination},
  author={Hafner, Danijar and Lillicrap, Timothy and Ba, Jimmy and Norouzi, Mohammad},
  journal={arXiv preprint arXiv:1912.01603},
  year={2019}
}

## Summary
Dreamer is a reinforcement learning agent that learns long-horizon behaviors from images purely by latent imagination. It learns a world model from past experience that can predict into the future. It then learns action and value models in its compact latent space. The value model optimizes Bellman consistency of imagined trajectories. The action model maximizes value estimates by propagating their analytic gradients back through imagined trajectories.

## Relevance to Paper 5 (The Predictive Processing Bridge)
Dreamer conceptually maps to active inference by utilizing latent imagination and learned world models. In the context of Paper 5, Dreamer's framework helps model delayed observations ($\tau$) and precision collapse dynamics. The learned world model predicting into the future aligns with the active inference mechanism of minimizing expected free energy through generative models and generalized motion.
