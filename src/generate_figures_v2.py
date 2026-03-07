#!/usr/bin/env python3
"""Generate publication figures for the Derivative Gain Trap manuscript."""

import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 10,
    'axes.labelsize': 11, 'axes.titlesize': 12,
    'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight'
})

with open('/sessions/gracious-relaxed-dirac/mnt/life/results/kd_trap_results.json') as f:
    D = json.load(f)

outdir = '/sessions/gracious-relaxed-dirac/mnt/life/figures_v2'
os.makedirs(outdir, exist_ok=True)

# ========== Figure 1: K_d vs τ* at multiple K_p (the core finding) ==========
fig, ax = plt.subplots(figsize=(7, 4.5))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
markers = ['o', 's', '^', 'D']

for idx, kp in enumerate(['90', '120', '150', '200']):
    data = D['sa'][kp]
    kds = [d['Kd'] for d in data]
    tcs = [(d['tc'] if d['tc'] else 0) for d in data]
    ax.plot(kds, [t*1000 for t in tcs], color=colors[idx], marker=markers[idx],
            markersize=5, label=f'$K_p$ = {kp}', linewidth=1.5)

ax.set_xlabel('Derivative Gain $K_d$ (N·m·s/rad)')
ax.set_ylabel('Critical Delay τ* (ms)')
ax.set_title('The Derivative Gain Trap: Non-Monotonic Stability Boundary')
ax.legend(frameon=True, fontsize=9)
ax.set_xlim(0, 55)
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3)

# Shade the "trap zone"
ax.axvspan(15, 50, alpha=0.08, color='red', label='_nolegend_')
ax.annotate('Over-correction\nzone', xy=(32, 20), fontsize=8, color='darkred',
            ha='center', style='italic')
ax.annotate('Optimal\nwindow', xy=(8, 80), fontsize=8, color='darkgreen',
            ha='center', style='italic')

ax.grid(True, alpha=0.3)
fig.savefig(f'{outdir}/fig1_kd_trap_curve.png')
fig.savefig(f'{outdir}/fig1_kd_trap_curve.pdf')
plt.close()
print("Fig 1 done")

# ========== Figure 2: K_d × τ stability heat map ==========
fig, ax = plt.subplots(figsize=(7, 5))
sb = D['sb']
Kd_arr = np.array(sb['Kd'])
tau_arr = np.array(sb['tau'])
tau_ms = tau_arr * 1000  # ms
Map = np.array(sb['map'])
Map = np.clip(Map, 1e-14, 100)

im = ax.pcolormesh(tau_ms, Kd_arr, Map, norm=LogNorm(vmin=1e-12, vmax=100),
                   cmap='RdYlGn_r', shading='auto')
cb = fig.colorbar(im, ax=ax, label='Amplitude Ratio (late/early RMS)')
ax.set_xlabel('Effective Adaptive Delay τ_eff (ms)')
ax.set_ylabel('Derivative Gain $K_d$ (N·m·s/rad)')
ax.set_title('Stability Phase Map: $K_d$ × τ Space')

# Overlay critical boundary
for i, kd in enumerate(Kd_arr):
    for j in range(len(tau_ms)):
        if j > 0 and Map[i, j] > 2.5 and Map[i, j-1] <= 2.5:
            ax.plot(tau_ms[j], kd, 'kx', markersize=4, markeredgewidth=1)
            break

fig.savefig(f'{outdir}/fig2_kd_tau_phasemap.png')
fig.savefig(f'{outdir}/fig2_kd_tau_phasemap.pdf')
plt.close()
print("Fig 2 done")

# ========== Figure 3: Growth-phase transient at different K_d ==========
fig, axes = plt.subplots(2, 2, figsize=(9, 7), sharex=True)
axes = axes.flatten()

kd_showcase = ['5', '10', '20', '30']
titles = ['$K_d$ = 5 (Under-damped)', '$K_d$ = 10 (Optimal)',
          '$K_d$ = 20 (Over-corrected)', '$K_d$ = 30 (Trap zone)']
colors_g = ['#d62728', '#2ca02c', '#ff7f0e', '#d62728']

for idx, (kd_str, title, col) in enumerate(zip(kd_showcase, titles, colors_g)):
    ax = axes[idx]
    data = D['sc'][kd_str]
    theta = np.array(data['theta'])
    t_arr = np.linspace(0, 8, len(theta))  # Duration was 8s in p3min
    theta_deg = np.degrees(theta)

    ax.plot(t_arr, theta_deg, color=col, linewidth=0.8)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel('θ (degrees)')
    ax.grid(True, alpha=0.3)

    # Add growth-spurt shading
    ax.axvspan(3.5, 6.5, alpha=0.1, color='blue')

    mx = data['max_deg']
    if abs(mx) > 50:
        ax.set_ylim(-60, 60)
        ax.annotate(f'RUNAWAY\n(max {mx:.0f}°)', xy=(0.5, 0.85),
                   xycoords='axes fraction', fontsize=8, color='red',
                   ha='center', fontweight='bold')
    else:
        yl = max(abs(mx) * 1.3, 5)
        ax.set_ylim(-yl, yl)
        ax.annotate(f'max = {mx:.1f}°', xy=(0.75, 0.85),
                   xycoords='axes fraction', fontsize=8, color=col)

axes[2].set_xlabel('Time (s)')
axes[3].set_xlabel('Time (s)')
fig.suptitle('Growth-Phase Transient Response Across $K_d$ Values\n(τ_eff = 60 ms, shaded = growth spurt)',
             fontsize=12, y=1.02)
fig.tight_layout()
fig.savefig(f'{outdir}/fig3_growth_kd_panels.png')
fig.savefig(f'{outdir}/fig3_growth_kd_panels.pdf')
plt.close()
print("Fig 3 done")

# ========== Figure 4: Optimal K_d envelope ==========
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

# Panel A: Optimal K_d vs K_p
kps = [d['Kp'] for d in D['sd']]
opt_kds = [d['opt_Kd'] for d in D['sd']]
max_tcs = [d['max_tc']*1000 for d in D['sd']]

ax1.plot(kps, opt_kds, 'ko-', markersize=5, linewidth=1.5)
ax1.set_xlabel('Proportional Gain $K_p$ (N·m/rad)')
ax1.set_ylabel('Optimal $K_d$ (N·m·s/rad)')
ax1.set_title('A. Optimal Derivative Gain')
ax1.grid(True, alpha=0.3)
ax1.axhline(y=8.0, color='red', linestyle='--', alpha=0.5, label='Default $K_d$=8')
ax1.legend(fontsize=8)

# Panel B: Max stability margin vs K_p
ax2.plot(kps, max_tcs, 'bs-', markersize=5, linewidth=1.5)
ax2.set_xlabel('Proportional Gain $K_p$ (N·m/rad)')
ax2.set_ylabel('Max Achievable τ* (ms)')
ax2.set_title('B. Maximum Stability Margin')
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(f'{outdir}/fig4_optimal_envelope.png')
fig.savefig(f'{outdir}/fig4_optimal_envelope.pdf')
plt.close()
print("Fig 4 done")

# ========== Figure 5: Trajectory comparison ==========
fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharex=True)
axes = axes.flatten()

for idx, kd_str in enumerate(['5', '10', '15', '25']):
    ax = axes[idx]
    data = D['sf'][kd_str]
    t_arr = np.array(data['t'])
    theta = np.degrees(np.array(data['theta']))

    col = '#d62728' if data['unstable'] else '#2ca02c'
    ax.plot(t_arr, theta, color=col, linewidth=0.6)

    status = 'UNSTABLE' if data['unstable'] else 'Stable'
    ax.set_title(f'$K_d$ = {kd_str}  ({status})', fontsize=10,
                 color='red' if data['unstable'] else 'green')
    ax.set_ylabel('θ (degrees)')
    ax.grid(True, alpha=0.3)

    if data['unstable']:
        ax.set_ylim(-60, 60)
    else:
        ax.set_ylim(-5, 5)

axes[2].set_xlabel('Time (s)')
axes[3].set_xlabel('Time (s)')
fig.suptitle('Time-Series at τ_eff = 70 ms: Both Low and High $K_d$ Destabilize',
             fontsize=11)
fig.tight_layout()
fig.savefig(f'{outdir}/fig5_trajectory_comparison.png')
fig.savefig(f'{outdir}/fig5_trajectory_comparison.pdf')
plt.close()
print("Fig 5 done")

print("\n✓ All 5 figures generated.")
