import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib

matplotlib.use('Agg')

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def exp_embodied_time_milestones():
    print("Running comprehensive Embodied Temporal Cognition computational model...")

    years = np.linspace(0, 20, 200)

    # 1. Developmental Length Model (Logistic)
    L_min = 0.5   # Birth length proxy
    L_max = 1.7   # Adult length proxy
    k_growth = 1.5
    t_mid = 12.0  # Spurt around 12 years old

    L_t = L_min + (L_max - L_min) / (1 + np.exp(-k_growth * (years - t_mid)))
    dL_dt = np.gradient(L_t, years)

    # 2. Delay and Prediction Model
    tau_0 = 0.05
    v = 15.0
    tau_t = tau_0 + L_t / v

    T_pred_t = np.zeros_like(years)
    T_pred_t[0] = tau_t[0]
    tau_adapt = 2.0  # Plasticity time constant

    for i in range(1, len(years)):
        dt_yr = years[i] - years[i-1]
        dT_pred = (1.0 / tau_adapt) * (tau_t[i-1] - T_pred_t[i-1]) * dt_yr
        T_pred_t[i] = T_pred_t[i-1] + dT_pred

    gap_t = tau_t - T_pred_t
    gap_t[gap_t < 0] = 0 # No negative gap

    # 3. Thermodynamic Free Energy Proxy
    # F scales with mass (proxy for volume ~ L^3) and exponentially with the derivative gain gap
    m_t = 10.0 * (L_t / L_min)**3
    F_t = m_t * np.exp(50 * gap_t)
    F_baseline = m_t * 1.0 # Base cost without temporal mismatch

    # Save data
    df = pd.DataFrame({
        'Age_Years': years,
        'Length_m': L_t,
        'Growth_Velocity': dL_dt,
        'Mass_kg_proxy': m_t,
        'Neural_Delay_tau': tau_t,
        'Cognitive_Horizon_Tpred': T_pred_t,
        'Derivative_Gain_Gap': gap_t,
        'Free_Energy_F': F_t,
        'Baseline_Energy': F_baseline
    })
    df.to_csv('outputs/embodied_time/embodied_cognition_timeline.csv', index=False)

    # Plotting the three fundamental pillars mentioned in the prompt
    fig = plt.figure(figsize=(12, 14))

    # --- Pillar 1: Biomechanical Necessity (The Milestones) ---
    ax1 = plt.subplot(3, 1, 1)

    # Milestones overlay (Age, Name, L)
    milestones = [
        (0.25, 'Head Control', 0.6),
        (0.5, 'Sitting', 0.65),
        (1.0, 'Standing', 0.75),
        (1.5, 'Walking', 0.85)
    ]

    ax1.plot(years[years <= 5], tau_t[years <= 5] * 1000, 'k-', lw=2, label=r'Physical Delay $\tau$')
    ax1.plot(years[years <= 5], T_pred_t[years <= 5] * 1000, 'b--', lw=2, label=r'Cognitive Horizon $T_{pred}$')

    for age, name, l in milestones:
        idx = np.abs(years - age).argmin()
        ax1.plot(age, T_pred_t[idx]*1000, 'ro')
        ax1.annotate(name, (age, T_pred_t[idx]*1000 + 2), fontsize=10, ha='center')

    ax1.set_xlim([0, 5])
    ax1.set_ylim([70, 120])
    ax1.set_ylabel('Time (ms)', fontsize=12)
    ax1.set_title('Ontogeny of Time Perception: Cognitive Horizon tracks Postural Necessity', fontsize=14)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)

    # --- Pillar 2: Life as a Dissipative Structure (Adolescent Spurt) ---
    ax2 = plt.subplot(3, 1, 2)
    color1 = 'tab:blue'
    ax2.plot(years, L_t, color=color1, lw=2, label='Somatic Scale $L(t)$')
    ax2.set_ylabel('Body Length $L$ (m)', color=color1, fontsize=12)
    ax2.tick_params(axis='y', labelcolor=color1)

    ax2b = ax2.twinx()
    color2 = 'tab:red'
    ax2b.plot(years, gap_t * 1000, color=color2, lw=2, label=r'Derivative Gain Gap $\Delta T$')
    ax2b.set_ylabel('Temporal Mismatch (ms)', color=color2, fontsize=12)
    ax2b.tick_params(axis='y', labelcolor=color2)

    ax2.set_title('The Allometric Trap: Growth outpaces Cognitive Adaptation', fontsize=14)
    ax2.grid(True, alpha=0.3)

    # --- Pillar 3: Friston's Free Energy Principle & The Resolution ---
    ax3 = plt.subplot(3, 1, 3)
    ax3.plot(years, F_baseline, 'g--', lw=2, label='Baseline Free Energy (No Mismatch)')
    ax3.plot(years, F_t, 'r-', lw=2.5, label='Actual Free Energy (with Mismatch)')

    # Annotate the scoliosis bifurcation
    peak_idx = np.argmax(gap_t)
    peak_age = years[peak_idx]
    ax3.axvline(peak_age, color='k', linestyle=':', lw=2)
    ax3.annotate('Metabolic Buckling\n(Scoliosis breaks symmetry to bound Free Energy)',
                 xy=(peak_age, F_t[peak_idx]*0.8), xytext=(peak_age+1, F_t[peak_idx]*0.6),
                 arrowprops=dict(facecolor='black', shrink=0.05), fontsize=11)

    ax3.set_yscale('log')
    ax3.set_xlabel('Age (Years)', fontsize=12)
    ax3.set_ylabel(r'Thermodynamic Cost $\mathcal{F}$', fontsize=12)
    ax3.set_title('The Resolution: Breaking Symmetry to Bound Free Energy', fontsize=14)
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/embodied_cognition_synthesis.png', dpi=300)
    plt.close()
    print("Saved outputs to outputs/embodied_time/")

if __name__ == "__main__":
    setup_directories()
    exp_embodied_time_milestones()
