import numpy as np
import matplotlib.pyplot as plt

def run_holographic_sim(fascial_tension_left, fascial_tension_right, D_holo=0.1, length=100):
    """
    Simulates the spinal curvature based on the Holographic Tension Hypothesis.
    """
    s = np.linspace(0, 1, length)

    # Boundary tensor simplified to scalar tension values on left and right
    H_left = fascial_tension_left
    H_right = fascial_tension_right

    # Bulk-Boundary Duality mapping (simplified kernel)
    # The curvature is proportional to the difference in boundary tensions
    kappa_rest = D_holo * (H_right - H_left) * np.ones_like(s)

    # Integrate curvature to get shape
    theta = np.cumsum(kappa_rest) / length
    x = np.cumsum(np.sin(theta)) / length
    y = np.cumsum(np.cos(theta)) / length

    return x, y, kappa_rest

def main():
    print("Running Holographic Tension Experiment...")

    # Case 1: Symmetric tension (healthy)
    x1, y1, k1 = run_holographic_sim(1.0, 1.0)

    # Case 2: Asymmetric tension (e.g., fascial slit on the left)
    # Left tension drops, creating an imbalance
    x2, y2, k2 = run_holographic_sim(0.2, 1.0)

    plt.figure(figsize=(8, 6))
    plt.plot(x1, y1, label='Symmetric Tension (Healthy)', linewidth=3)
    plt.plot(x2, y2, label='Asymmetric Tension (Fascial Defect)', linewidth=3, linestyle='--')

    plt.title('Holographic Tension Hypothesis: Fascial Defect Induces Curvature')
    plt.xlabel('Lateral Displacement')
    plt.ylabel('Spinal Axis')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')

    plt.savefig('outputs/holographic_tension_result.png')
    print("Simulation complete. Results saved to outputs/holographic_tension_result.png")

if __name__ == "__main__":
    import os
    os.makedirs('outputs', exist_ok=True)
    main()
