import numpy as np
import matplotlib.pyplot as plt

def calculate_tau_trajectory(age, gpr126_variant=False, lbx1_variant=False, piezo2_variant=False):
    # Base delays (ms)
    tau_transduction_base = 2.0
    tau_spinal_base = 3.0
    tau_cerebellar_base = 25.0
    tau_nmj_base = 1.0
    tau_em_base = 50.0

    # Growth model (Height in meters)
    # Simple sigmoid for adolescent growth spurt centered around 12 years
    h_max = 1.65
    h_min = 1.20
    k = 1.5 # growth rate
    age_mid = 12.0
    height = h_min + (h_max - h_min) / (1 + np.exp(-k * (age - age_mid)))

    # Growth velocity (cm/yr)
    dh_dt = (h_max - h_min) * k * np.exp(-k * (age - age_mid)) / (1 + np.exp(-k * (age - age_mid)))**2 * 100

    # NCV model (m/s)
    ncv_base = 60.0
    # Transient NCV drop during peak growth (myelination lag)
    ncv_lag = 0.5 * dh_dt

    # Genetic perturbations
    ncv_penalty = 5.0 if gpr126_variant else 0.0
    tau_spinal_penalty = 5.0 if lbx1_variant else 0.0
    tau_transduction_penalty = 2.0 if piezo2_variant else 0.0

    ncv_actual = ncv_base - ncv_lag - ncv_penalty

    # Path length is roughly proportional to height (e.g. 60% of height)
    path_length = height * 0.6

    # Calculate conduction delays
    tau_afferent = (path_length / ncv_actual) * 1000 # convert to ms
    tau_efferent = (path_length / ncv_actual) * 1000

    # Total tau
    tau_total = (tau_transduction_base + tau_transduction_penalty +
                 tau_afferent +
                 tau_spinal_base + tau_spinal_penalty +
                 tau_cerebellar_base +
                 tau_efferent +
                 tau_nmj_base +
                 tau_em_base)

    return tau_total, dh_dt

if __name__ == "__main__":
    ages = np.linspace(8, 16, 100)

    tau_wt, vel = calculate_tau_trajectory(ages)
    tau_gpr126, _ = calculate_tau_trajectory(ages, gpr126_variant=True)
    tau_lbx1, _ = calculate_tau_trajectory(ages, lbx1_variant=True)
    tau_poly, _ = calculate_tau_trajectory(ages, gpr126_variant=True, lbx1_variant=True, piezo2_variant=True)

    plt.figure(figsize=(10, 6))
    plt.plot(ages, tau_wt, label="Wild Type", color='blue')
    plt.plot(ages, tau_gpr126, label="GPR126 Variant", color='orange', linestyle='--')
    plt.plot(ages, tau_lbx1, label="LBX1 Variant", color='green', linestyle='-.')
    plt.plot(ages, tau_poly, label="Polygenic (GPR126 + LBX1 + PIEZO2)", color='red', linewidth=2)

    plt.axhline(y=200, color='black', linestyle=':', label='Instability Threshold (200 ms)')

    plt.title("Proprioceptive Delay ($\\tau$) Trajectory During Puberty")
    plt.xlabel("Age (Years)")
    plt.ylabel("Total Proprioceptive Delay $\\tau$ (ms)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../paper4_figures/tau_trajectory.png", dpi=300)
    print("Saved tau_trajectory.png")
