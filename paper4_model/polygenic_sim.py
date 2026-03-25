import numpy as np
import matplotlib.pyplot as plt

def run_polygenic_sim(n_individuals=10000):
    # Frequencies of risk alleles
    # GPR126 (e.g., rs6570507, minor allele freq ~0.3)
    # LBX1 (e.g., rs11190870, MAF ~0.4)
    # PIEZO2 (Hypothetical subtle variant, MAF ~0.1)

    np.random.seed(42)

    gpr126_alleles = np.random.binomial(2, 0.3, n_individuals)
    lbx1_alleles = np.random.binomial(2, 0.4, n_individuals)
    piezo2_alleles = np.random.binomial(2, 0.1, n_individuals)

    # Calculate tau at peak growth (Age = 12)
    # Using the math from day 11

    tau_transduction_base = 2.0
    tau_spinal_base = 3.0
    tau_cerebellar_base = 25.0
    tau_nmj_base = 1.0
    tau_em_base = 65.0

    height = 1.425 # height at age 12
    dh_dt = 9.28 # peak velocity
    path_length = height * 0.6

    ncv_base = 55.0
    ncv_lag = 0.5 * dh_dt

    tau_totals = []

    # Add some biological noise
    noise = np.random.normal(0, 15.0, n_individuals)
    tau_spinal_base = 5.0
    ncv_base = 35.0

    for i in range(n_individuals):
        # Additive effects
        ncv_penalty = 4.0 * gpr126_alleles[i]
        tau_spinal_penalty = 4.0 * lbx1_alleles[i]
        tau_trans_penalty = 3.0 * piezo2_alleles[i]

        ncv_actual = ncv_base - ncv_lag - ncv_penalty

        tau_afferent = (path_length / ncv_actual) * 1000
        tau_efferent = (path_length / ncv_actual) * 1000

        tau = (tau_transduction_base + tau_trans_penalty +
               tau_afferent +
               tau_spinal_base + tau_spinal_penalty +
               tau_cerebellar_base +
               tau_efferent +
               tau_nmj_base +
               tau_em_base +
               noise[i])

        tau_totals.append(tau)

    tau_totals = np.array(tau_totals)

    # Calculate scoliosis risk (tau > 200)
    ais_cases = np.sum(tau_totals > 200)
    prevalence = (ais_cases / n_individuals) * 100

    print(f"Simulated AIS Prevalence: {prevalence:.2f}%")

    plt.figure(figsize=(10, 6))
    plt.hist(tau_totals, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(x=200, color='red', linestyle='--', linewidth=2, label='Instability Threshold')

    # Highlight the tail
    tail = tau_totals[tau_totals > 200]
    plt.hist(tail, bins=10, color='red', edgecolor='black', alpha=0.7, label='AIS Cases')

    plt.title("Population Distribution of Proprioceptive Delay ($\\tau$) at Peak Growth")
    plt.xlabel("Total Proprioceptive Delay $\\tau$ (ms)")
    plt.ylabel("Number of Individuals")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../paper4_figures/polygenic_distribution.png", dpi=300)
    print("Saved polygenic_distribution.png")

if __name__ == "__main__":
    run_polygenic_sim()
