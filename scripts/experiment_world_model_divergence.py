import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure output directory exists
OUTPUT_DIR = "outputs/world_model_divergence"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def simulate_world_model():
    t = np.linspace(0, 10, 500)
    g_true = 9.81
    # Simulated growth spurt: true physical sensitivity increases
    phys_sensitivity = 1.0 + 0.5 * (1 / (1 + np.exp(-2*(t-5))))
    # Internal model lags behind
    g_internal = 9.81 * (1.0 + 0.1 * (1 / (1 + np.exp(-1*(t-6)))))

    prediction_error = np.abs((phys_sensitivity * g_true) - g_internal)

    plt.figure(figsize=(10,6))
    plt.plot(t, phys_sensitivity * g_true, label='Physical Gravity Effect (Growth Spurt)')
    plt.plot(t, g_internal, label='Internal Model Prediction (Lagging)')
    plt.plot(t, prediction_error, label='Sensory Prediction Error (Cobb Angle Proxy)', linestyle='--')
    plt.xlabel('Adolescent Time (years)')
    plt.ylabel('Effective Force')
    plt.title('Latent Imagination: World Model Divergence in Scoliosis')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{OUTPUT_DIR}/divergence_plot.png")
    print(f"Plot saved to {OUTPUT_DIR}/divergence_plot.png")

if __name__ == '__main__':
    simulate_world_model()
