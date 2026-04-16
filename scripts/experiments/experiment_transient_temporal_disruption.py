import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def setup_directories():
    os.makedirs('outputs/embodied_time', exist_ok=True)

def dynamics(x, u, g=9.81, L=1.0, m=1.0):
    theta, omega = x
    dtheta = omega
    domega = (g / L) * np.sin(theta) + u / (m * L**2)
    return np.array([dtheta, domega])

def rk4(x, u, dt, L=1.0, m=1.0):
    k1 = dynamics(x, u, L=L, m=m)
    k2 = dynamics(x + 0.5 * dt * k1, u, L=L, m=m)
    k3 = dynamics(x + 0.5 * dt * k2, u, L=L, m=m)
    k4 = dynamics(x + dt * k3, u, L=L, m=m)
    return x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_agent_eval(tau, T_pred, L=1.0, m=1.0, Kp=20.0, Kd=8.0, T=2.0, dt=0.01):
    steps = int(T / dt)
    delay_steps = int(tau / dt)
    pred_steps = int(T_pred / dt)
    x = np.zeros((steps, 2))
    u = np.zeros(steps)
    x[0] = np.array([0.087, 0.0]) # 5 deg initial perturbation

    stable = True
    for i in range(steps - 1):
        obs_idx = max(0, i - delay_steps)
        x_obs = x[obs_idx]

        x_hat = np.copy(x_obs)
        if pred_steps > 0:
            for j in range(pred_steps):
                idx_u = obs_idx + j
                u_hat = u[idx_u] if idx_u < i else 0.0
                x_hat = rk4(x_hat, u_hat, dt, L=L, m=m)

        u[i] = -Kp * x_hat[0] - Kd * x_hat[1]
        x[i+1] = rk4(x[i], u[i], dt, L=L, m=m)

        if abs(x[i+1, 0]) > np.pi/2:
            stable = False
            break

    if not stable:
        return 1000.0, False

    effort = np.sum(np.abs(u)*dt)
    return effort, True

def run_developmental_simulation():
    t_months = np.linspace(0, 240, 100) # 0 to 20 years

    # Growth curve L(t)
    L_min = 0.5
    L_max = 1.8
    t_spurt = 156 # 13 years
    k_growth = 0.1
    L = L_min + (L_max - L_min) / (1 + np.exp(-k_growth * (t_months - t_spurt)))

    # Physical delay
    tau_0 = 0.05
    v_nerve = 15.0
    tau = tau_0 + L / v_nerve

    # Internal model adaptation
    T_pred = np.zeros_like(tau)
    T_pred[0] = tau[0]
    tau_adapt = 18.0 # adaptation time constant in months

    dt = t_months[1] - t_months[0]
    for i in range(1, len(t_months)):
        dT = (tau[i-1] - T_pred[i-1]) / tau_adapt
        T_pred[i] = T_pred[i-1] + dT * dt

    Delta_T = tau - T_pred

    F_active = np.zeros_like(t_months)
    stabilities = []

    for i in range(len(t_months)):
        Kp = 20.0 * (L[i]/1.0)
        Kd = 8.0 * (L[i]/1.0)
        f_cost, stable = simulate_agent_eval(tau[i], T_pred[i], L=L[i], Kp=Kp, Kd=Kd)
        F_active[i] = f_cost
        stabilities.append(stable)

    F_crit = 50.0

    F_actual = np.zeros_like(F_active)
    curvature = np.zeros_like(F_active)

    for i in range(len(t_months)):
        if F_active[i] > F_crit or not stabilities[i]:
            excess = F_active[i] - F_crit
            if not stabilities[i]:
                excess = 200.0
            F_actual[i] = F_crit + 0.1 * excess
            curvature[i] = excess * 0.2
        else:
            F_actual[i] = F_active[i]
            curvature[i] = 0.0

    for i in range(1, len(t_months)):
        if curvature[i] < curvature[i-1]:
            curvature[i] = curvature[i-1]

    df = pd.DataFrame({
        'Age_Years': t_months / 12.0,
        'Length_m': L,
        'Physical_Delay_tau': tau,
        'Predictive_Horizon_Tpred': T_pred,
        'Derivative_Gain_Gap': Delta_T,
        'Unbounded_Free_Energy': F_active,
        'Actual_Free_Energy': F_actual,
        'Structural_Curvature': curvature,
        'Stable_Sagittal': stabilities
    })
    df.to_csv('outputs/embodied_time/transient_temporal_disruption.csv', index=False)

    plt.figure(figsize=(12, 10))

    plt.subplot(3, 1, 1)
    plt.plot(df['Age_Years'], df['Physical_Delay_tau'], 'r-', linewidth=2, label=r'Physical Delay $\tau(t)$')
    plt.plot(df['Age_Years'], df['Predictive_Horizon_Tpred'], 'b--', linewidth=2, label=r'Internal Model $T_{pred}(t)$')
    plt.fill_between(df['Age_Years'], df['Predictive_Horizon_Tpred'], df['Physical_Delay_tau'],
                     where=(df['Physical_Delay_tau'] > df['Predictive_Horizon_Tpred']),
                     color='red', alpha=0.2, label='Derivative Gain Gap')
    plt.ylabel('Delay (s)')
    plt.title('The Derivative Gain Gap During Adolescent Growth Spurt', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(3, 1, 2)
    plt.plot(df['Age_Years'], df['Unbounded_Free_Energy'], 'k--', alpha=0.5, label='Unbounded Free Energy (Sagittal Posture)')
    plt.plot(df['Age_Years'], df['Actual_Free_Energy'], 'g-', linewidth=2, label='Bounded Free Energy (Buckled Posture)')
    plt.axhline(F_crit, color='r', linestyle=':', label='Metabolic Threshold $F_{crit}$')
    plt.ylabel('Thermodynamic Cost')
    plt.ylim(0, max(F_actual) * 1.5)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(3, 1, 3)
    plt.plot(df['Age_Years'], df['Structural_Curvature'], 'm-', linewidth=2, label='Structural Curvature (Scoliosis)')
    plt.xlabel('Age (Years)')
    plt.ylabel('Severity (Proxy)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('outputs/embodied_time/transient_temporal_disruption.png', dpi=300)
    plt.close()
    print("Simulation complete. Data saved to outputs/embodied_time/")

if __name__ == '__main__':
    setup_directories()
    run_developmental_simulation()
