#!/usr/bin/env python3
"""
Experiment: Multi-segment Cosserat Rod Modeling of Lenke Curve Types

This script extends the single-link inverted pendulum DDE model to a multi-segment
Cosserat rod, applying regional parameter variations (stiffness, proprioceptive
delay, damping, asymmetric load) to predict where the spine destabilizes and the
resulting Lenke curve types.
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.spinalmodes.countercurvature.multi_segment import create_lenke_profile

def compute_regional_instability(profile: dict) -> dict:
    n = len(profile['chi_kappa'])
    thoracic_idx = slice(0, int(0.6 * n))
    lumbar_idx = slice(int(0.6 * n), n)

    instability = (profile['chi_kappa'] * 10) \
                + (profile['tau_delay'] - 70) * 0.5 \
                - (profile['EI_modifier'] * 5) \
                + ((1.0 - profile['damping_b']) * 20) \
                + (profile['asymmetric_load'] * 15)

    return {
        'thoracic_instability': np.mean(instability[thoracic_idx]),
        'lumbar_instability': np.mean(instability[lumbar_idx])
    }

def main():
    os.makedirs('outputs/experiments', exist_ok=True)
    s = np.linspace(0, 1, 100)
    results = []

    for lenke_type in range(1, 7):
        profile = create_lenke_profile(s, lenke_type)
        metrics = compute_regional_instability(profile)

        if metrics['thoracic_instability'] > metrics['lumbar_instability'] + 3:
            primary_curve = 'Thoracic'
        elif metrics['lumbar_instability'] > metrics['thoracic_instability'] + 3:
            primary_curve = 'Lumbar/Thoracolumbar'
        else:
            primary_curve = 'Double (Thoracic & Lumbar)'

        results.append({
            'Lenke_Type': lenke_type,
            'Thoracic_Instability_Score': round(metrics['thoracic_instability'], 2),
            'Lumbar_Instability_Score': round(metrics['lumbar_instability'], 2),
            'Predicted_Primary_Curve': primary_curve
        })

    df = pd.DataFrame(results)
    csv_path = 'outputs/experiments/polygenic_lenke_cosserat_results.csv'
    df.to_csv(csv_path, index=False)
    print(f"Saved {csv_path}")
    print(df)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(1, 7)
    width = 0.35

    thoracic_scores = df['Thoracic_Instability_Score']
    lumbar_scores = df['Lumbar_Instability_Score']

    rects1 = ax.bar(x - width/2, thoracic_scores, width, label='Thoracic Instability')
    rects2 = ax.bar(x + width/2, lumbar_scores, width, label='Lumbar Instability')

    ax.set_ylabel('Instability Score')
    ax.set_title('Regional Instability Predicts Lenke Curve Types')
    ax.set_xticks(x)
    ax.set_xticklabels([f"Type {i}" for i in range(1, 7)])
    ax.legend()

    fig.tight_layout()
    plt.savefig('outputs/experiments/polygenic_lenke_cosserat_plot.png')
    print("Saved outputs/experiments/polygenic_lenke_cosserat_plot.png")

if __name__ == '__main__':
    main()
