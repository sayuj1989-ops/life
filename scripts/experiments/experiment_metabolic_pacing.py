import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure output directory exists
os.makedirs('outputs/figures', exist_ok=True)

def simulate_metabolic_pacing(days=5, dt=0.01):
    """
    Simulates the "Metabolic Pacing" hypothesis:
    Aligning peak metabolic supply (e.g. via scheduled nutrition/activity) with
    peak gravitational loading (daytime upright posture) to prevent energy
    deficits from crossing the buckling threshold.
    """
    time = np.arange(0, days, dt)

    # Gravitational Loading Pattern (Upright during day, supine at night)
    # 0 = supine, 1 = upright. Modeled as a squarish wave.
    loading = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * time))
    # Smooth it out slightly
    loading = np.convolve(loading, np.ones(50)/50, mode='same')

    # Baseline metabolic supply (constant)
    baseline_supply = np.full_like(time, 0.6)

    # Paced metabolic supply (peaks during the day, optimized timing)
    # Peak slightly leads or coincides with loading
    paced_supply = 0.6 + 0.4 * np.sin(2 * np.pi * time + 0.2)

    # Base energy demand grows slowly over days (simulating adolescent spurt)
    base_demand = 0.4 + 0.1 * time

    # Total Demand = Base Demand + Loading Cost
    # If loading is high, demand spikes
    demand = base_demand + 0.5 * loading

    # Deficit = Demand - Supply
    # If Deficit > 0, the spine accumulates "error" (scoliotic drift)
    deficit_unpaced = np.maximum(0, demand - baseline_supply)
    deficit_paced = np.maximum(0, demand - paced_supply)

    # Accumulate error (buckling)
    error_unpaced = np.cumsum(deficit_unpaced) * dt
    error_paced = np.cumsum(deficit_paced) * dt

    # Plotting
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    # Plot 1: Loading & Demand
    ax1.plot(time, loading, 'k--', label='Gravitational Loading (Upright)', alpha=0.5)
    ax1.plot(time, demand, 'r-', label='Energy Demand', linewidth=2)
    ax1.set_ylabel('Normalized Units')
    ax1.set_title('Metabolic Pacing Hypothesis: Mitigating the Energy Deficit')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # Plot 2: Supply vs Demand
    ax2.plot(time, demand, 'r-', alpha=0.3)
    ax2.plot(time, baseline_supply, 'g--', label='Standard Supply (Constant)', linewidth=2)
    ax2.plot(time, paced_supply, 'b-', label='Paced Supply (Circadian Optimized)', linewidth=2)

    # Highlight deficit areas
    ax2.fill_between(time, baseline_supply, demand, where=(demand > baseline_supply), color='g', alpha=0.2, label='Unpaced Deficit')
    ax2.fill_between(time, paced_supply, demand, where=(demand > paced_supply), color='b', alpha=0.2, label='Paced Deficit')

    ax2.set_ylabel('Energy (Supply/Demand)')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    # Plot 3: Accumulated Deformity
    ax3.plot(time, error_unpaced, 'g--', label='Accumulated Deformity (Standard)', linewidth=2)
    ax3.plot(time, error_paced, 'b-', label='Accumulated Deformity (Paced)', linewidth=2)

    ax3.set_xlabel('Time (Days)')
    ax3.set_ylabel('Scoliotic Deformity')
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = 'outputs/figures/experiment_metabolic_pacing.png'
    plt.savefig(output_path, dpi=300)
    print(f"Figure saved to {output_path}")

if __name__ == "__main__":
    simulate_metabolic_pacing()
