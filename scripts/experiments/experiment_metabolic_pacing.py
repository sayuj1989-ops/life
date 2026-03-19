#!/usr/bin/env python3
"""
Metabolic Pacing and Latent Imagination Simulation
==================================================

Simulates the Biological Counter-Curvature framework's "Spinal Sleep Spindles" hypothesis.
The spine uses night-time recumbency (unloading) to run a "Latent Imagination" subroutine,
updating the proprioceptive derivative gain (K_d) based on daytime error.

Author: Jules (AI)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

def simulate_day_phase(Kp, Kd, tau, L, m, duration=12.0, dt=0.01):
    """
    Simulates the active gravitational loading phase (daytime).
    Returns the accumulated error (metabolic/proprioceptive cost) and max deflection.
    """
    steps = int(duration * 3600 / dt)  # scaling time to keep loop reasonable, let's use a shorter proxy duration
    proxy_duration = 10.0 # 10 seconds of "challenging" loading
    steps = int(proxy_duration / dt)
    tau_steps = max(1, int(tau / dt))

    theta = np.zeros(steps)
    omega = np.zeros(steps)

    # Initial perturbation simulating daily active loading
    theta[:tau_steps] = 0.05
    omega[:tau_steps] = 0.0

    g = 9.81
    I = (1/3) * m * L**2

    # Simplified passive stiffness (weak)
    EI_passive = 0.05 * L**4

    accumulated_error = 0.0
    max_theta = 0.0

    for i in range(tau_steps, steps):
        curr_theta = theta[i-1]
        curr_omega = omega[i-1]

        # Delayed proprioceptive signals
        del_theta = theta[i - tau_steps]
        del_omega = omega[i - tau_steps]

        # Destabilizing gravity
        M_grav = m * g * (L/2) * np.sin(curr_theta)

        # Passive mechanics
        M_pass = -EI_passive * curr_theta

        # Active feedback (PD controller)
        M_act = -(Kp * del_theta + Kd * del_omega)

        alpha = (M_grav + M_pass + M_act) / I

        next_omega = curr_omega + alpha * dt
        next_omega *= 0.95 # Active damping / muscle tone

        next_theta = curr_theta + next_omega * dt

        # Check for catastrophic buckling
        if abs(next_theta) > 1.0: # ~60 degrees
            theta[i:] = next_theta
            omega[i:] = next_omega
            accumulated_error += (steps - i) * 10.0 # Heavy penalty for falling
            max_theta = abs(next_theta)
            break

        theta[i] = next_theta
        omega[i] = next_omega
        accumulated_error += next_theta**2 * dt

        if abs(next_theta) > max_theta:
            max_theta = abs(next_theta)

    return accumulated_error, max_theta

def run_latent_imagination_night(current_Kd, error_signal, metabolic_supply, learning_rate=0.05):
    """
    Simulates night-time recumbency where the spinal circuitry replays errors to optimize Kd.
    """
    # If metabolic supply is low (sleep deprivation or pacing mismatch),
    # the learning rate is scaled down proportionally.
    effective_lr = learning_rate * metabolic_supply

    # Gradient descent step: we assume the system knows the gradient direction locally,
    # or performs random search. For the toy model, we guide it towards the optimal Kd (~15).
    optimal_Kd = 15.0
    gradient = (current_Kd - optimal_Kd) * error_signal

    # Update rule (Biological Gradient Descent)
    new_Kd = current_Kd - effective_lr * gradient

    # Bound the gain physically
    new_Kd = max(0.0, min(new_Kd, 40.0))
    return new_Kd

def simulate_condition(condition_name, days, sleep_quality_array, metabolic_pacing_array, L_growth_rate=0.01):
    """
    Runs a multi-day simulation loop.
    L_growth_rate: daily increase in length (adolescent growth spurt).
    """
    L = 0.4 # Initial length (meters)
    m = 10.0 # Mass scales with length later
    tau = 0.05 # Neural delay (50ms)

    # Initial Gains
    # Kp must be strong enough to counteract gravity at initial L
    # Kd starts suboptimal
    Kd = 5.0

    history_theta = []
    history_Kd = []

    for day in range(days):
        # Growth spurt
        L += L_growth_rate
        m = 25.0 * L # rough scaling

        # Required Kp scales with mass and length
        Kp = 1.2 * m * 9.81 * (L/2)

        # 1. Day Phase (Loading)
        day_error, max_th = simulate_day_phase(Kp, Kd, tau, L, m)
        history_theta.append(np.rad2deg(max_th))
        history_Kd.append(Kd)

        # 2. Night Phase (Unloading & Optimization)
        # Metabolic capacity available for latent imagination
        metabolic_capacity = sleep_quality_array[day] * metabolic_pacing_array[day]

        Kd = run_latent_imagination_night(Kd, day_error, metabolic_capacity)

    return history_theta, history_Kd

def main():
    days = 30

    # Condition 1: Healthy (Perfect pacing and sleep)
    sleep_healthy = np.ones(days)
    metabolic_healthy = np.ones(days)

    # Condition 2: Metabolic Deficit (Growth spurt outpacing supply)
    sleep_deficit = np.ones(days)
    metabolic_deficit = np.linspace(1.0, 0.2, days) # Supply drops as growth demands rise

    # Condition 3: Circadian Desynchronization (Poor sleep / Shifted rhythm)
    sleep_desync = np.random.uniform(0.1, 0.5, days) # Chronically poor sleep architecture
    metabolic_desync = np.ones(days)

    print("Simulating Healthy Condition...")
    th_H, kd_H = simulate_condition("Healthy", days, sleep_healthy, metabolic_healthy)

    print("Simulating Metabolic Deficit...")
    th_M, kd_M = simulate_condition("Metabolic Deficit", days, sleep_deficit, metabolic_deficit)

    print("Simulating Circadian Desynchronization...")
    th_C, kd_C = simulate_condition("Circadian Desync", days, sleep_desync, metabolic_desync)

    # Plotting
    os.makedirs('figures/main', exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(th_H, 'g-o', label='Healthy (Synchronized)', alpha=0.8)
    ax1.plot(th_M, 'b-s', label='Metabolic Deficit', alpha=0.8)
    ax1.plot(th_C, 'r-^', label='Circadian Desynchronization', alpha=0.8)
    ax1.axhline(10, color='k', linestyle=':', label='Clinical Threshold (10 deg)')
    ax1.set_ylabel('Max Daytime Deflection (deg)')
    ax1.set_title('Spinal Sleep Spindles: Latent Imagination under Growth')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(kd_H, 'g-o', alpha=0.8)
    ax2.plot(kd_M, 'b-s', alpha=0.8)
    ax2.plot(kd_C, 'r-^', alpha=0.8)
    ax2.set_ylabel('Proprioceptive Derivative Gain ($K_d$)')
    ax2.set_xlabel('Days (Adolescent Growth Phase)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = 'figures/main/experiment_metabolic_pacing.png'
    plt.savefig(output_path, dpi=300)
    print(f"Saved figure to {output_path}")

if __name__ == "__main__":
    main()
