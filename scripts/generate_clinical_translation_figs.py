import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def generate_clinical_translation_fig():
    """
    Generates a comprehensive 2x2 Clinical Translation figure combining:
    1. Clinical Cohort Validation
    2. Peak Height Velocity (PHV) Timing
    3. Sexual Dimorphism
    4. Lenke Classifications
    """
    print("Generating comprehensive Clinical Translation figure...")

    output_dir = "figures/main"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "fig_clinical_translation.png")

    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25)

    # =========================================================
    # 1. Clinical Cohort Validation
    # =========================================================
    ax1 = fig.add_subplot(gs[0, 0])
    data_path = "data/clinical_cohort_targets.csv"
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        for source in df['source'].unique():
            subset = df[df['source'] == source]
            ax1.scatter(subset['age'], subset['cobb_angle'], label=source, s=100, alpha=0.7)

        L_crit_age = 11.67
        ax1.axvline(L_crit_age, color='r', linestyle='--', label=f'Model L_crit ~{L_crit_age} yrs')
        ax1.axvspan(11.0, 14.0, color='red', alpha=0.1, label='Energy Deficit Window')
        ax1.set_xlabel("Age (years)", fontsize=12)
        ax1.set_ylabel("Cobb Angle (degrees)", fontsize=12)
        ax1.set_title("A. Clinical Cohort Data vs Energy Deficit", fontsize=14, fontweight='bold', loc='left')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

    # =========================================================
    # 2. PHV Timing
    # =========================================================
    ax2 = fig.add_subplot(gs[0, 1])
    age = np.linspace(8, 18, 100)
    L_max = 0.45; L_min = 0.25; k_growth = 1.2; t_mid = 12.0
    L_t = L_min + (L_max - L_min) / (1 + np.exp(-k_growth * (age - t_mid)))
    dL_dt = np.gradient(L_t, age)
    c_scaling = 10.0
    R_t = c_scaling * L_t
    alpha = 5.0
    R_eff = R_t * (1 + alpha * dL_dt)
    R_crit = 3.5

    color = 'tab:blue'
    ax2.set_xlabel('Age (years)', fontsize=12)
    ax2.set_ylabel('Growth Velocity (cm/year)', color=color, fontsize=12)
    ax2.plot(age, dL_dt * 100, color=color, linewidth=2, label='Growth Velocity (PHV)')
    ax2.tick_params(axis='y', labelcolor=color)

    phv_indices = np.where(dL_dt * 100 > 1.5)[0]
    ax2.axvspan(age[phv_indices[0]], age[phv_indices[-1]], color='blue', alpha=0.1, label='PHV Window')

    ax2_twin = ax2.twinx()
    color2 = 'tab:red'
    ax2_twin.set_ylabel('Metabolic Deficit Ratio', color=color2, fontsize=12)
    ax2_twin.plot(age, R_eff, color=color2, linewidth=2, linestyle='--', label='Energy Deficit ($R_{eff}$)')
    ax2_twin.axhline(y=R_crit, color='black', linestyle=':', label='Critical Threshold ($R_{crit}$)')
    ax2_twin.tick_params(axis='y', labelcolor=color2)

    instability_indices = np.where(R_eff > R_crit)[0]
    if len(instability_indices) > 0:
        ax2_twin.axvspan(age[instability_indices[0]], age[instability_indices[-1]], color='red', alpha=0.2, label='Instability Window')

    ax2.set_title("B. Peak Height Velocity vs Instability Window", fontsize=14, fontweight='bold', loc='left')

    lines_1, labels_1 = ax2.get_legend_handles_labels()
    lines_2, labels_2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
    ax2.grid(True, alpha=0.3)

    # =========================================================
    # 3. Sexual Dimorphism
    # =========================================================
    ax3 = fig.add_subplot(gs[1, 0])
    t_mid_f = 11.5; t_mid_m = 13.5
    k_growth_f = 1.3; k_growth_m = 1.1
    L_max_f = 0.43; L_max_m = 0.48

    L_t_f = L_min + (L_max_f - L_min) / (1 + np.exp(-k_growth_f * (age - t_mid_f)))
    L_t_m = L_min + (L_max_m - L_min) / (1 + np.exp(-k_growth_m * (age - t_mid_m)))

    dL_dt_f = np.gradient(L_t_f, age)
    dL_dt_m = np.gradient(L_t_m, age)

    c_scaling_f = 2.7 / L_max_f
    c_scaling_m = 2.4 / L_max_m

    R_t_f = c_scaling_f * L_t_f
    R_t_m = c_scaling_m * L_t_m

    R_eff_f = R_t_f + dL_dt_f * (2.7 - np.max(R_t_f)) / np.max(dL_dt_f)
    R_eff_m = R_t_m + dL_dt_m * (2.4 - np.max(R_t_m)) / np.max(dL_dt_m)
    R_crit_dim = 2.5

    color_f = 'tab:pink'
    color_m = 'tab:blue'

    ax3.set_xlabel('Age (years)', fontsize=12)
    ax3.set_ylabel('Metabolic Deficit Ratio ($R$)', color='black', fontsize=12)
    ax3.plot(age, R_eff_f, color=color_f, linewidth=2.5, label='Female ($R_{peak} = 2.7$)')
    ax3.plot(age, R_eff_m, color=color_m, linewidth=2.5, label='Male ($R_{peak} = 2.4$)')
    ax3.axhline(y=R_crit_dim, color='black', linestyle='--', label='Critical Instability Threshold ($R_{crit} = 2.5$)')

    instability_f = np.where(R_eff_f > R_crit_dim)[0]
    if len(instability_f) > 0:
        ax3.axvspan(age[instability_f[0]], age[instability_f[-1]], color=color_f, alpha=0.2, label='Female Vulnerability Window')

    instability_m = np.where(R_eff_m > R_crit_dim)[0]
    if len(instability_m) > 0:
        ax3.axvspan(age[instability_m[0]], age[instability_m[-1]], color=color_m, alpha=0.2, label='Male Vulnerability Window')

    ax3.set_title("C. Sexual Dimorphism (10:1 Female-to-Male Ratio)", fontsize=14, fontweight='bold', loc='left')
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='upper right')

    # =========================================================
    # 4. Lenke Classifications
    # =========================================================
    ax4 = fig.add_subplot(gs[1, 1])
    # For a composite figure, we'll plot the three modes together in one panel
    s = np.linspace(0, 1, 100)
    kappa_1 = np.sin(np.pi * s)
    kappa_2 = np.sin(2 * np.pi * s)
    kappa_3 = np.sin(3 * np.pi * s)

    ax4.plot(kappa_1, s, color='darkorange', linewidth=2.5, label='Type 5 (n=1)')
    ax4.plot(kappa_2, s, color='royalblue', linewidth=2.5, label='Type 3 (n=2)')
    ax4.plot(kappa_3, s, color='forestgreen', linewidth=2.5, label='Type 4 (n=3)')

    ax4.set_xlabel('Lateral Curvature', fontsize=12)
    ax4.set_ylabel('Normalized Spine Length (s/L)', fontsize=12)
    ax4.invert_yaxis()
    ax4.grid(True, alpha=0.3)
    ax4.axvline(x=0, color='black', linestyle='--', alpha=0.5)
    ax4.legend(loc='upper left')
    ax4.set_title("D. Lenke Classifications as Rod Eigenmodes", fontsize=14, fontweight='bold', loc='left')

    plt.suptitle("Clinical Translation of the Metabolic Buckling Framework", fontsize=20, y=0.96)

    try:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\nSuccessfully generated comprehensive plot: {output_path}")
    except Exception as e:
        print(f"\nError saving plot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    generate_clinical_translation_fig()
