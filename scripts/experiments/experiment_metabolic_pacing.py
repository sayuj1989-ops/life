import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

def daytime_cost(Kd_val):
    """
    Computes a simplified daytime postural cost as a function of proprioceptive derivative gain (Kd).
    Using a proxy mapping:
    - High Kd reduces geometric error but increases high-frequency proprioceptive metabolic cost.
    - Too low Kd leads to large geometric error and mechanical instability.

    Returns a cost value based on:
    Cost = alpha * Kd + beta / (Kd + epsilon)
    """
    alpha = 0.5   # Cost of maintaining high derivative gain (e.g., neural/metabolic cost)
    beta = 2.0    # Cost of geometric error (instability due to low Kd)
    epsilon = 0.1 # Prevent division by zero

    return alpha * Kd_val + beta / (Kd_val + epsilon)

def nighttime_imagination_optimization(epochs=100, learning_rate=0.05):
    """
    Simulates Latent Imagination during "Spinal Sleep Spindles".
    The brain uses a forward model (tf.GradientTape) to optimize Kd
    by minimizing the predicted daytime postural cost.
    """
    # Initialize Kd as a trainable variable (start with a suboptimal value)
    Kd = tf.Variable(5.0, dtype=tf.float32)

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    Kd_history = []
    cost_history = []

    for epoch in range(epochs):
        with tf.GradientTape() as tape:
            cost = daytime_cost(Kd)

        # Backpropagate gradient through the "imagined" trajectory cost
        gradients = tape.gradient(cost, [Kd])
        optimizer.apply_gradients(zip(gradients, [Kd]))

        # Enforce non-negative Kd
        Kd.assign(tf.maximum(Kd, 0.0))

        Kd_history.append(Kd.numpy())
        cost_history.append(cost.numpy())

    return Kd_history, cost_history

def main():
    print("Simulating Metabolic Pacing and Latent Imagination...")

    # 1. Run optimization (Nighttime imagination)
    epochs = 150
    Kd_history, cost_history = nighttime_imagination_optimization(epochs=epochs)

    optimal_Kd = Kd_history[-1]
    final_cost = cost_history[-1]

    print(f"Optimization complete. Final Kd: {optimal_Kd:.3f}, Final Cost: {final_cost:.3f}")

    # 2. Plotting
    os.makedirs('figures/main', exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot Kd evolution
    ax1.plot(range(epochs), Kd_history, 'b-', linewidth=2, label='Derivative Gain ($K_d$)')
    ax1.set_xlabel('Nighttime Imagination Epoch')
    ax1.set_ylabel('Derivative Gain ($K_d$)')
    ax1.set_title('Optimization of $K_d$ via Latent Imagination')
    ax1.axhline(optimal_Kd, color='r', linestyle='--', label=f'Optimal $K_d$ ~ {optimal_Kd:.2f}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot Cost Landscape and Trajectory
    Kd_vals = np.linspace(0.1, 6.0, 100)
    costs = [daytime_cost(tf.constant(k, dtype=tf.float32)).numpy() for k in Kd_vals]

    ax2.plot(Kd_vals, costs, 'k--', label='Daytime Cost Landscape')
    ax2.plot(Kd_history, cost_history, 'ro-', markersize=4, alpha=0.6, label='Optimization Trajectory')
    ax2.plot(optimal_Kd, final_cost, 'g*', markersize=15, label='Converged Optimum')

    ax2.set_xlabel('Derivative Gain ($K_d$)')
    ax2.set_ylabel('Predicted Postural Cost')
    ax2.set_title('Gradient Descent on Internal World Model')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = 'figures/main/metabolic_pacing_latent_imagination.png'
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved figure to {output_path}")

if __name__ == "__main__":
    main()
