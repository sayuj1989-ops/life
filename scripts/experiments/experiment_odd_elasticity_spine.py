import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_eigenvalues(EI, GJ, K_odd):
    term1 = (EI + GJ) / 2.0
    term2_inner = ((EI - GJ) / 2.0)**2 - K_odd**2

    # Using complex math to handle negative square roots
    term2 = np.sqrt(np.complex128(term2_inner))

    lambda1 = term1 + term2
    lambda2 = term1 - term2

    return lambda1, lambda2

def run_simulation():
    days = 1000  # ~3 years of adolescent growth
    time = np.linspace(0, days, days)

    # Baseline stiffnesses (decreasing slightly due to structural demands of rapid growth)
    EI = 100.0 - 0.02 * time
    GJ = 80.0 - 0.01 * time

    # Odd elasticity builds up as metabolic mismatch / neural delay increases during peak height velocity
    # Peaks around day 600
    K_odd = 5.0 + 20.0 * np.exp(-((time - 600)/200)**2)

    results = []

    for t, ei, gj, k_odd in zip(time, EI, GJ, K_odd):
        l1, l2 = calculate_eigenvalues(ei, gj, k_odd)

        # Check if imaginary part is non-zero
        is_complex = abs(l1.imag) > 1e-6

        # Cobb angle surrogate: grows if system is in complex eigenvalue regime
        cobb_rate = abs(l1.imag) * 0.1 if is_complex else 0.0

        results.append({
            'time_days': t,
            'EI': ei,
            'GJ': gj,
            'K_odd': k_odd,
            'Lambda1_real': l1.real,
            'Lambda1_imag': l1.imag,
            'Lambda2_real': l2.real,
            'Lambda2_imag': l2.imag,
            'cobb_rate': cobb_rate,
            'is_complex': is_complex
        })

    df = pd.DataFrame(results)

    # Integrate Cobb angle
    df['cobb_angle'] = df['cobb_rate'].cumsum()

    # Output directory
    out_dir = "outputs/sim/odd_elasticity"
    os.makedirs(out_dir, exist_ok=True)

    df.to_csv(os.path.join(out_dir, "odd_elastic_transition.csv"), index=False)

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(df['time_days'], df['EI'], 'b-', label='Bending Stiffness (EI)')
    ax1.plot(df['time_days'], df['GJ'], 'g-', label='Torsional Stiffness (GJ)')
    ax1.plot(df['time_days'], df['K_odd'], 'r-', linewidth=2, label='Odd Elasticity ($K_{odd}$)')

    # Highlight critical region
    critical_mask = df['is_complex']
    if critical_mask.any():
        ax1.fill_between(df['time_days'], 0, 100, where=critical_mask,
                         color='red', alpha=0.2, label='Complex Eigenvalues (Instability)')

    ax1.set_ylabel("Stiffness Moduli")
    ax1.set_title("Active Odd Elasticity During Adolescent Growth Spurt")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(df['time_days'], df['cobb_angle'], 'k-', linewidth=2, label='Progression (Cobb Angle Surrogate)')
    ax2.set_xlabel("Time (Days)")
    ax2.set_ylabel("Deformity Magnitude")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "odd_elastic_buckling.png"), dpi=300)
    print("Simulation complete.")

if __name__ == "__main__":
    run_simulation()
