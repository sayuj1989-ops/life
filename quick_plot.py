#!/usr/bin/env python3
"""Quick plot of eta_CC vs Bg."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('results/bg_validation_jax_quick/bg_validation_jax_results.csv')

print(f"Data shape: {df.shape}")
print(f"Bg range: [{df['Bg'].min():.2f}, {df['Bg'].max():.2f}]")
print(f"eta_CC range: [{df['eta_CC'].min():.2f}, {df['eta_CC'].max():.2f}]")
print(f"z_tip range: [{df['z_tip'].min():.2f}m, {df['z_tip'].max():.2f}m]")

# Plot eta_CC vs Bg
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Left: eta_CC vs Bg (all seeds)
for seed in df['seed'].unique():
    data = df[df['seed'] == seed]
    ax1.plot(data['Bg'], data['eta_CC'], 'o-', alpha=0.6, label=f'Seed {seed}')

ax1.axvline(x=1.0, color='r', linestyle='--', linewidth=2, label='Bg = 1 (hypothesis)')
ax1.axhline(y=0.0, color='k', linestyle='-', alpha=0.3)
ax1.set_xlabel('Bio-Gravitational Number (Bg)', fontsize=12)
ax1.set_ylabel('Counter-Curvature Efficiency (eta_CC)', fontsize=12)
ax1.set_title('Phase Transition Test: eta_CC vs Bg', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Right: z_tip vs chi_M (to understand physics)
for seed in df['seed'].unique():
    data = df[df['seed'] == seed]
    ax2.plot(data['chi_M'], data['z_tip'], 'o-', alpha=0.6, label=f'Seed {seed}')

ax2.axhline(y=df['z_tip_passive'].iloc[0], color='r', linestyle='--',
            linewidth=2, label=f'Passive (chi_M=0): {df["z_tip_passive"].iloc[0]:.2f}m')
ax2.set_xlabel('Active Moment Coupling (chi_M)', fontsize=12)
ax2.set_ylabel('Tip Deflection z_tip (m)', fontsize=12)
ax2.set_title('Physics Check: Tip Deflection vs chi_M', fontsize=14, fontweight='bold')
ax2.set_xscale('log')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/bg_validation_jax_quick/quick_plot.png', dpi=150)
print("\n✅ Plot saved: results/bg_validation_jax_quick/quick_plot.png")

# Summary statistics
print("\n" + "="*60)
print("QUICK ANALYSIS")
print("="*60)

grouped = df.groupby('Bg')['eta_CC'].agg(['mean', 'std']).reset_index()
print(f"\neta_CC at Bg=1 (hypothesis): {grouped[grouped['Bg'].between(0.9, 1.1)]['mean'].values}")

# Check if eta_CC increases with Bg (any trend?)
from scipy.stats import spearmanr
rho, p = spearmanr(df['Bg'], df['eta_CC'])
print(f"\nSpearman correlation (Bg vs eta_CC): ρ = {rho:.3f}, p = {p:.3e}")

if rho < -0.5:
    print("⚠️  NEGATIVE correlation — active moments make deflection WORSE (physics broken)")
elif abs(rho) < 0.3:
    print("⚠️  NO correlation — no phase transition detected (noise or physics issue)")
else:
    print("✅ Positive correlation — active moments improve counter-curvature")

# Check for sigmoid pattern (visual inspection needed)
print("\nTo check for sigmoid:")
print("  1. Open results/bg_validation_jax_quick/quick_plot.png")
print("  2. Look for S-curve in left panel")
print("  3. If eta_CC stays <0 everywhere → physics too broken")
print("  4. If eta_CC shows step-change near Bg=1 → hypothesis supported")
