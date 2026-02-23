import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def run_vim_cascade():
    print("Running VIM Cascade Simulation...")

    # Load Energy Deficit Data
    df_energy = pd.read_csv("outputs/thermodynamic_cost/energy_deficit_window_v2.csv")

    # Calculate Deficit Ratio R = Demand / Supply
    # Avoid division by zero at very small L (Supply ~ 0)
    # But Supply ~ L^2, Demand ~ L^4. Limit L->0 is 0.
    # We focus on the range L > 0.25

    # Recalculate Supply_L2 here to be sure (it's in the CSV but let's be explicit)
    # The CSV has Supply_L2 calibrated to cross at 0.35m.

    df_energy['Deficit_Ratio'] = df_energy['Demand_IntegratedMoment'] / df_energy['Supply_L2']

    # Define Protein Cascade Parameters
    # Anisotropy scores from AlphaFold analysis
    proteins = [
        {'name': 'VIM', 'anisotropy': 7.47, 'role': 'Cytoskeletal Stiffness', 'cobb_impact': 8.0, 'color': 'purple'},
        {'name': 'GHR', 'anisotropy': 5.13, 'role': 'Growth Signaling', 'cobb_impact': 0.0, 'color': 'gray'}, # GHR failure -> stop growth?
        {'name': 'LMNA', 'anisotropy': 4.75, 'role': 'Nuclear Stiffness', 'cobb_impact': 5.0, 'color': 'magenta'},
        {'name': 'PIEZO2', 'anisotropy': 4.44, 'role': 'Proprioception (Vector)', 'cobb_impact': 15.0, 'color': 'red'},
        {'name': 'PIEZO1', 'anisotropy': 3.90, 'role': 'Proprioception (Scalar)', 'cobb_impact': 5.0, 'color': 'orange'},
        {'name': 'LBX1', 'anisotropy': 2.27, 'role': 'Muscle Symmetry', 'cobb_impact': 20.0, 'color': 'blue'},
        {'name': 'SIRT1', 'anisotropy': 1.73, 'role': 'Energy Sensor', 'cobb_impact': 0.0, 'color': 'green'}
    ]

    # Failure Threshold Model
    # A protein fails when the System Stress > Its Robustness
    # System Stress ~ Deficit_Ratio (Energy Starvation)
    # Robustness ~ 1 / Anisotropy (High anisotropy = fragile)
    # Failure Condition: Deficit_Ratio > (Threshold_Constant / Anisotropy)
    # We calibrate Threshold_Constant so VIM fails exactly when Deficit > 1.0 (at L_crit = 0.35)
    # Actually, VIM is the most sensitive. It should fail AT the crossover.
    # So Threshold_Constant = 1.0 * VIM.Anisotropy = 7.47

    # Wait, if Deficit = 1.0, VIM fails.
    # If Deficit = 1.5, stronger proteins fail.
    # Condition: Deficit_Ratio * Anisotropy > K_fail
    # Let K_fail = 7.5 (So VIM fails at R=1.0)

    K_fail = 7.5

    results = []

    for i, row in df_energy.iterrows():
        L = row['L']
        R = row['Deficit_Ratio']

        current_cobb = 5.0 # Baseline physiological Cobb (normal spine is straight but has measurement error)
        failed_proteins = []

        for p in proteins:
            # Check Failure
            stress = R * p['anisotropy']
            is_failed = stress > K_fail

            if is_failed:
                current_cobb += p['cobb_impact']
                failed_proteins.append(p['name'])

        results.append({
            'L': L,
            'Deficit_Ratio': R,
            'Cobb_Angle': current_cobb,
            'Failed_Proteins': ", ".join(failed_proteins),
            'Failure_Count': len(failed_proteins)
        })

    df_res = pd.DataFrame(results)

    # Detect onset L for each protein
    onset_points = {}
    for p in proteins:
        # Find first L where this protein is in Failed_Proteins
        failed_rows = df_res[df_res['Failed_Proteins'].str.contains(p['name'])]
        if not failed_rows.empty:
            onset_L = failed_rows.iloc[0]['L']
            onset_points[p['name']] = onset_L
            print(f"Protein {p['name']} fails at L = {onset_L:.3f} m")

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot Cobb Angle Surge
    color = 'tab:red'
    ax1.set_xlabel('Spinal Length (m)', fontsize=14)
    ax1.set_ylabel('Projected Cobb Angle (°)', color=color, fontsize=14)
    ax1.plot(df_res['L'], df_res['Cobb_Angle'], color=color, linewidth=3, label='Cobb Angle')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 100)

    # Plot Deficit Ratio on secondary axis
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Metabolic Deficit Ratio (Demand/Supply)', color=color, fontsize=14)
    ax2.plot(df_res['L'], df_res['Deficit_Ratio'], color=color, linestyle='--', label='Deficit Ratio')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.axhline(1.0, color='gray', linestyle=':', label='Deficit Threshold (R=1)')

    # Add Failure Zones
    # Shade regions based on dominant failure?
    # Or just vertical lines for onset

    # Sort onsets
    sorted_onsets = sorted(onset_points.items(), key=lambda x: x[1])

    for name, L_fail in sorted_onsets:
        p_info = next(p for p in proteins if p['name'] == name)
        if p_info['cobb_impact'] > 0: # Only plot structural failures
            ax1.axvline(L_fail, color=p_info['color'], linestyle='-', alpha=0.5)
            ax1.text(L_fail + 0.002, 80 if name=='VIM' else (60 if name=='PIEZO2' else 40),
                     f"{name} FAIL\n(A={p_info['anisotropy']})",
                     color=p_info['color'], fontweight='bold', rotation=90)

    # Title and Layout
    plt.title('The VIM Cascade: Sequential Protein Failure Driving Scoliosis', fontsize=16)

    # Create custom legend for proteins
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color=p['color'], lw=2) for p in proteins if p['name'] in onset_points and p['cobb_impact'] > 0]
    custom_labels = [f"{p['name']} (Anisotropy {p['anisotropy']})" for p in proteins if p['name'] in onset_points and p['cobb_impact'] > 0]

    ax1.legend(custom_lines, custom_labels, loc='upper left', title='Failure Sequence')

    plt.tight_layout()
    out_path = Path("outputs/figures/vim_cascade.png")
    plt.savefig(out_path, dpi=300)
    print(f"Saved Figure to {out_path}")

    # Save CSV Results
    df_res.to_csv("outputs/thermodynamic_cost/vim_cascade_results.csv", index=False)

if __name__ == "__main__":
    run_vim_cascade()
