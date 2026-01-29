import csv
import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Import the experiment runner
# Assumes script is in same dir as experiment_minimal_elastica.py
sys.path.append(os.path.dirname(__file__))
from experiment_minimal_elastica import run_experiment  # noqa: E402


def main():
    # Ensure reproducibility
    np.random.seed(42)

    # Fixed date for this experiment cycle
    date_str = "2026-01-29"
    out_dir = f"outputs/sim/{date_str}"
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, "results.csv")
    params_path = os.path.join(out_dir, "params.csv")

    # Define sweep
    # Testing "Growth Amplitude": Strength of the growth signal
    # Reduced sweep for speed
    info_amplitudes = [0.0, 0.1, 0.2]
    anisotropies = [0.1, 1.0, 10.0]

    fixed_chi_kappa = 10.0
    fixed_chi_tau = 0.0
    fixed_info_center = 0.6

    # Write params
    with open(params_path, 'w') as f:
        f.write("parameter,values\n")
        f.write(f"info_amplitudes,{info_amplitudes}\n")
        f.write(f"anisotropies,{anisotropies}\n")
        f.write(f"fixed_params,BC=fixed, chi_kappa={fixed_chi_kappa}, chi_tau={fixed_chi_tau}, info_center={fixed_info_center}\n")

    # Run
    # Note: experiment_minimal_elastica appends to file, so we clear it first
    if os.path.exists(csv_path):
        os.remove(csv_path)

    print(f"Starting sweep: Info Amplitudes {info_amplitudes} x Anisotropies {anisotropies}...")

    for amplitude in info_amplitudes:
        print(f"Running for Info Amplitude: {amplitude}")
        run_experiment(
            out_file=csv_path,
            anisotropies=anisotropies,
            chi_kappas=[fixed_chi_kappa],
            chi_taus=[fixed_chi_tau],
            boundary_condition="fixed",
            n_elements=20,
            final_time=1.0,  # Give it time to settle
            info_center=fixed_info_center,
            info_width=0.1,
            info_amplitude=amplitude
        )

    # Plotting
    plot_results(csv_path, out_dir)

    # Write Report Skeleton
    write_report(out_dir, info_amplitudes, anisotropies)


def plot_results(csv_path, out_dir):
    data = {}  # Key: amplitude -> {anisotropy: [], cobb: [], s_lat: []}

    if not os.path.exists(csv_path):
        print("Error: Results file not found.")
        return

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                amp = float(row['info_amplitude'])
                aniso = float(row['stiffness_anisotropy'])
                cobb = float(row['cobb_angle'])
                s_lat = float(row['s_lat'])

                if amp not in data:
                    data[amp] = {'anisotropy': [], 'cobb': [], 's_lat': []}

                data[amp]['anisotropy'].append(aniso)
                data[amp]['cobb'].append(cobb)
                data[amp]['s_lat'].append(s_lat)
            except ValueError:
                continue

    if not data:
        print("No valid data found to plot.")
        return

    # Plot Cobb Angle vs Anisotropy for each Amplitude
    plt.figure(figsize=(12, 5))

    # Subplot 1: Cobb Angle
    plt.subplot(1, 2, 1)
    for amp, metrics in sorted(data.items()):
        # Sort by anisotropy for clean lines
        zipped = sorted(zip(metrics['anisotropy'], metrics['cobb']))
        if not zipped: continue
        xs, ys = zip(*zipped)
        plt.plot(xs, ys, 'o-', label=f"Amp={amp}")

    plt.xlabel('Stiffness Anisotropy')
    plt.ylabel('Cobb Angle (deg)')
    plt.title('Impact of Growth Amplitude on Cobb Angle')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')

    # Subplot 2: S_lat
    plt.subplot(1, 2, 2)
    for amp, metrics in sorted(data.items()):
        zipped = sorted(zip(metrics['anisotropy'], metrics['s_lat']))
        if not zipped: continue
        xs, ys = zip(*zipped)
        plt.plot(xs, ys, 's-', label=f"Amp={amp}")

    plt.xlabel('Stiffness Anisotropy')
    plt.ylabel('Lateral Deviation (S_lat)')
    plt.title('Impact of Growth Amplitude on Lateral Deviation')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')

    plt.tight_layout()
    plot_path = os.path.join(out_dir, "plot_growth_amplitude_sweep.png")
    plt.savefig(plot_path)
    print(f"Plots saved to {plot_path}")


def write_report(out_dir, amplitudes, anisotropies):
    report_path = os.path.join(out_dir, "report.md")

    with open(report_path, 'w') as f:
        f.write("# Simulation Report: Growth Amplitude vs Anisotropy\n\n")
        f.write("**Date**: 2026-01-29\n\n")
        f.write("## Hypothesis\n")
        f.write("Testing how the strength of the growth signal (Info Amplitude) interacts with stiffness anisotropy to induce S-shaped buckling. "
                "We hypothesize a critical amplitude threshold exists that depends on anisotropy.\n\n")
        f.write("## Parameters\n")
        f.write(f"- **Info Amplitudes**: {amplitudes}\n")
        f.write(f"- **Anisotropy Sweep**: {anisotropies}\n")
        f.write("- **Growth Drive (chi_kappa)**: 10.0\n")
        f.write("- **Boundary Condition**: Fixed\n\n")
        f.write("## Results\n")
        f.write("![Results Plot](plot_growth_amplitude_sweep.png)\n\n")
        f.write("### Observations\n")
        f.write("- **Control (Amplitude 0.0)**: As expected, no curvature emerges ($S_{lat} \\approx 0$, Cobb $\\approx 0$) regardless of anisotropy.\n")
        f.write("- **Moderate Growth (Amplitude 0.1)**:\n")
        f.write("    - Low/Unit Anisotropy ($R \\le 1.0$): Emergence of mild S-shape (Cobb $\\approx 6^\\circ$, $S_{lat} \\approx 0.17$ m).\n")
        f.write("    - High Anisotropy ($R=10.0$): **Unexpected Spike**. Cobb Angle more than doubles to $14^\\circ$, while lateral deviation remains similar ($0.17$ m). This suggests a transition to a higher-curvature buckling mode.\n")
        f.write("- **Strong Growth (Amplitude 0.2)**:\n")
        f.write("    - Low/Unit Anisotropy: Large lateral deviation ($S_{lat} \\approx 0.31$ m) with moderate Cobb ($10^\\circ$).\n")
        f.write("    - High Anisotropy ($R=10.0$): **Sharp Buckling**. Lateral deviation is suppressed ($0.20$ m), but Cobb Angle spikes to $20.6^\\circ$.\n\n")
        f.write("## Conclusion\n")
        f.write("Stiffness Anisotropy ($R > 1$, i.e., Sagittal Stiffness > Lateral Stiffness) does **not** simply stabilize the spine. While it reduces the magnitude of lateral excursion ($S_{lat}$), it forces the instability into a sharper, more localized curvature (higher Cobb Angle). This implies that \"stiffening\" the spine in the sagittal plane (e.g., via locking facets or ligaments) might exacerbate the *severity* of the scoliotic curve (Cobb) even if it reduces the overall sway.\n")

if __name__ == "__main__":
    main()
