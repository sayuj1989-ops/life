"""
Create publication-quality figures for the IEC manuscript AlphaFold analysis.
"""
import json

import matplotlib
import numpy as np

matplotlib.use('Agg')
import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

# Load data
with open("/sessions/youthful-pensive-allen/alphafold_data/protein_metrics.json") as f:
    data = json.load(f)

OUTDIR = "/sessions/youthful-pensive-allen/mnt/life/alphafold_figures"
os.makedirs(OUTDIR, exist_ok=True)

# Color scheme
DEMAND_COLOR = "#C0392B"    # Deep red
SUPPLY_COLOR = "#2980B9"    # Blue
PROPRIO_COLOR = "#E74C3C"   # Light red
CYTO_COLOR = "#C0392B"      # Dark red
BG_COLOR = "#FAFAFA"
GRID_COLOR = "#E0E0E0"

# Sort proteins
demand_prots = {k: v for k, v in data.items() if v["category"] == "Demand"}
supply_prots = {k: v for k, v in data.items() if v["category"] == "Supply"}

# ================================================================
# FIGURE 1: Demand vs Supply Anisotropy Bar Chart (Main Figure)
# ================================================================
def fig1_anisotropy_bar():
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(BG_COLOR)

    # Sort all proteins by anisotropy
    sorted_all = sorted(data.items(), key=lambda x: x[1]['anisotropy'], reverse=True)
    genes = [g for g, _ in sorted_all]
    anisotropies = [v['anisotropy'] for _, v in sorted_all]
    categories = [v['category'] for _, v in sorted_all]
    subcats = [v.get('subcategory', '') for _, v in sorted_all]

    colors = []
    for cat, sub in zip(categories, subcats):
        if cat == "Demand" and sub == "Proprioceptive":
            colors.append(PROPRIO_COLOR)
        elif cat == "Demand":
            colors.append(CYTO_COLOR)
        else:
            colors.append(SUPPLY_COLOR)

    bars = ax.bar(range(len(genes)), anisotropies, color=colors, edgecolor='white', linewidth=0.5, width=0.75)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, anisotropies)):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                f'{val:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Demarcation line between demand and supply
    demand_count = sum(1 for c in categories if c == "Demand")
    # Actually draw the mean lines
    demand_mean = np.mean([v['anisotropy'] for v in demand_prots.values()])
    supply_mean = np.mean([v['anisotropy'] for v in supply_prots.values()])

    ax.axhline(y=demand_mean, color=DEMAND_COLOR, linestyle='--', alpha=0.7, linewidth=1.5,
               label=f'Demand mean = {demand_mean:.2f}')
    ax.axhline(y=supply_mean, color=SUPPLY_COLOR, linestyle='--', alpha=0.7, linewidth=1.5,
               label=f'Supply mean = {supply_mean:.2f}')

    # Annotate the gap
    gap_pct = (demand_mean - supply_mean) / supply_mean * 100
    mid_y = (demand_mean + supply_mean) / 2
    ax.annotate(f'Anisotropy Gap\n{gap_pct:.0f}%',
                xy=(len(genes)-1.5, mid_y), fontsize=12, fontweight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3CD', edgecolor='#856404', alpha=0.9))

    ax.set_xticks(range(len(genes)))
    ax.set_xticklabels(genes, rotation=45, ha='right', fontsize=10, fontweight='bold')
    ax.set_ylabel('Anisotropy Ratio (√λ₁/λ₃)', fontsize=13, fontweight='bold')
    ax.set_title('AlphaFold Structural Anisotropy: Demand vs Supply Proteins\n'
                 '(IEC Framework — 23 Key Mechanotransduction Proteins)',
                 fontsize=14, fontweight='bold', pad=15)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=PROPRIO_COLOR, label='Demand — Proprioceptive (ηₚ)'),
        mpatches.Patch(facecolor=CYTO_COLOR, label='Demand — Cytoskeletal (ηₐ)'),
        mpatches.Patch(facecolor=SUPPLY_COLOR, label='Supply — Metabolic (Γₘ)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.9)

    ax.set_ylim(0, max(anisotropies) * 1.15)
    ax.grid(axis='y', alpha=0.3, color=GRID_COLOR)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(f"{OUTDIR}/fig_anisotropy_bar.pdf", dpi=300, bbox_inches='tight')
    plt.savefig(f"{OUTDIR}/fig_anisotropy_bar.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 1: Anisotropy bar chart")


# ================================================================
# FIGURE 2: Multi-panel (Anisotropy vs Disorder vs pLDDT)
# ================================================================
def fig2_scatter_panels():
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor('white')

    for ax in axes:
        ax.set_facecolor(BG_COLOR)
        ax.grid(alpha=0.3, color=GRID_COLOR)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Panel A: Anisotropy vs Disorder Fraction
    ax = axes[0]
    for gene, v in data.items():
        color = DEMAND_COLOR if v['category'] == 'Demand' else SUPPLY_COLOR
        marker = 's' if v.get('subcategory') == 'Proprioceptive' else 'o'
        size = max(30, min(200, v['seq_length'] / 10))
        ax.scatter(v['disorder_fraction']*100, v['anisotropy'], c=color, s=size,
                   marker=marker, alpha=0.8, edgecolors='white', linewidth=0.5, zorder=5)
        # Label high-anisotropy and outlier proteins
        if v['anisotropy'] > 3.5 or v['disorder_fraction'] > 0.6 or gene in ['PPARGC1A', 'VIM', 'LMNA', 'PIEZO2', 'COL1A1']:
            ax.annotate(gene, (v['disorder_fraction']*100, v['anisotropy']),
                       fontsize=8, fontweight='bold', ha='left', va='bottom',
                       xytext=(3, 3), textcoords='offset points')

    ax.set_xlabel('Disorder Fraction (%)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Anisotropy Ratio', fontsize=11, fontweight='bold')
    ax.set_title('A. Structure vs Disorder', fontsize=12, fontweight='bold')

    # Panel B: pLDDT vs Anisotropy
    ax = axes[1]
    for gene, v in data.items():
        color = DEMAND_COLOR if v['category'] == 'Demand' else SUPPLY_COLOR
        marker = 's' if v.get('subcategory') == 'Proprioceptive' else 'o'
        size = max(30, min(200, v['seq_length'] / 10))
        ax.scatter(v['mean_plddt'], v['anisotropy'], c=color, s=size,
                   marker=marker, alpha=0.8, edgecolors='white', linewidth=0.5, zorder=5)
        if v['anisotropy'] > 3.5 or v['mean_plddt'] < 55 or gene in ['PPARGC1A', 'VIM', 'PLOD1', 'PTK7']:
            ax.annotate(gene, (v['mean_plddt'], v['anisotropy']),
                       fontsize=8, fontweight='bold', ha='left', va='bottom',
                       xytext=(3, 3), textcoords='offset points')

    ax.set_xlabel('Mean pLDDT Score', fontsize=11, fontweight='bold')
    ax.set_ylabel('Anisotropy Ratio', fontsize=11, fontweight='bold')
    ax.set_title('B. Confidence vs Structure', fontsize=12, fontweight='bold')

    # Panel C: Box plot comparison
    ax = axes[2]
    demand_anis = [v['anisotropy'] for v in demand_prots.values()]
    supply_anis = [v['anisotropy'] for v in supply_prots.values()]

    bp = ax.boxplot([demand_anis, supply_anis],
                    labels=['Demand\n(n=12)', 'Supply\n(n=11)'],
                    patch_artist=True, widths=0.5,
                    medianprops=dict(color='black', linewidth=2))
    bp['boxes'][0].set_facecolor(DEMAND_COLOR)
    bp['boxes'][0].set_alpha(0.6)
    bp['boxes'][1].set_facecolor(SUPPLY_COLOR)
    bp['boxes'][1].set_alpha(0.6)

    # Add individual points
    for i, (vals, color) in enumerate([(demand_anis, DEMAND_COLOR), (supply_anis, SUPPLY_COLOR)]):
        x = np.random.normal(i+1, 0.04, size=len(vals))
        ax.scatter(x, vals, c=color, s=40, alpha=0.8, edgecolors='white', linewidth=0.5, zorder=5)

    # Statistical annotation
    from scipy import stats
    t_stat, p_val = stats.ttest_ind(demand_anis, supply_anis)
    u_stat, u_pval = stats.mannwhitneyu(demand_anis, supply_anis, alternative='greater')

    ax.text(1.5, max(max(demand_anis), max(supply_anis)) * 0.95,
            f'Mann-Whitney U\np = {u_pval:.4f}\n(one-sided)',
            ha='center', va='top', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray'))

    ax.set_ylabel('Anisotropy Ratio', fontsize=11, fontweight='bold')
    ax.set_title('C. Demand vs Supply', fontsize=12, fontweight='bold')

    # Global legend
    legend_elements = [
        mpatches.Patch(facecolor=DEMAND_COLOR, alpha=0.6, label='Demand (mechanosensors)'),
        mpatches.Patch(facecolor=SUPPLY_COLOR, alpha=0.6, label='Supply (metabolic regulators)'),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', label='Proprioceptive', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', label='Other', markersize=8),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=10,
               bbox_to_anchor=(0.5, -0.02), framealpha=0.9)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)
    plt.savefig(f"{OUTDIR}/fig_scatter_panels.pdf", dpi=300, bbox_inches='tight')
    plt.savefig(f"{OUTDIR}/fig_scatter_panels.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 2: Scatter panels (Anisotropy vs Disorder vs pLDDT)")


# ================================================================
# FIGURE 3: VIM Cascade / Vulnerability Waterfall
# ================================================================
def fig3_vim_cascade():
    """Show the predicted failure cascade ordered by anisotropy."""
    # Cascade order from manuscript
    cascade_genes = ['VIM', 'LMNA', 'PIEZO2', 'CAV1', 'PIEZO1', 'EGR3', 'LBX1']
    cascade_data = [(g, data[g]) for g in cascade_genes if g in data]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(BG_COLOR)

    x = range(len(cascade_data))
    anis = [v['anisotropy'] for _, v in cascade_data]
    plddt = [v['mean_plddt'] for _, v in cascade_data]
    disorder = [v['disorder_fraction'] * 100 for _, v in cascade_data]
    genes = [g for g, _ in cascade_data]

    # Bar for anisotropy
    bars = ax.bar(x, anis, color=[DEMAND_COLOR]*len(x), alpha=0.7, width=0.5, label='Anisotropy Ratio')

    # Overlay disorder fraction as secondary y
    ax2 = ax.twinx()
    ax2.plot(x, disorder, 'o-', color='#F39C12', linewidth=2.5, markersize=10,
             markerfacecolor='#F39C12', markeredgecolor='white', label='Disorder %', zorder=5)

    # Add arrows between bars to show cascade direction
    for i in range(len(x) - 1):
        ax.annotate('', xy=(x[i+1], anis[i+1] + 0.1),
                    xytext=(x[i], anis[i] + 0.1),
                    arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2))

    # Labels
    for i, (gene, val) in enumerate(zip(genes, anis)):
        ax.text(i, val + 0.15, f'{val:.2f}', ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=DEMAND_COLOR)

    # Vulnerability index annotation for VIM
    vim_vi = data['VIM']['anisotropy'] / np.mean([v['anisotropy'] for v in supply_prots.values()])
    ax.annotate(f'VIM Vulnerability Index\n= {vim_vi:.1f}× supply mean',
                xy=(0, anis[0]), xytext=(1.5, anis[0] + 0.8),
                fontsize=10, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FADBD8', edgecolor=DEMAND_COLOR))

    ax.set_xticks(x)
    ax.set_xticklabels(genes, fontsize=12, fontweight='bold')
    ax.set_ylabel('Anisotropy Ratio (Structural Cost)', fontsize=12, fontweight='bold', color=DEMAND_COLOR)
    ax2.set_ylabel('Disorder Fraction (%)', fontsize=12, fontweight='bold', color='#F39C12')

    ax.set_title('VIM Cascade: Predicted Failure Sequence During Energy Deficit\n'
                 '(Proteins ordered by vulnerability — highest anisotropy fails first)',
                 fontsize=13, fontweight='bold', pad=15)

    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax.grid(axis='y', alpha=0.2)

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{OUTDIR}/fig_vim_cascade.pdf", dpi=300, bbox_inches='tight')
    plt.savefig(f"{OUTDIR}/fig_vim_cascade.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 3: VIM Cascade")


# ================================================================
# FIGURE 4: Supply-Side Disorder Paradox
# ================================================================
def fig4_supply_paradox():
    """Show that supply proteins are cheaper (low anisotropy) but more fragile (high disorder)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('white')

    # Panel A: Grouped comparison
    ax = axes[0]
    ax.set_facecolor(BG_COLOR)

    categories = ['Anisotropy\n(Structural Cost)', 'Disorder %\n(Fragility)', 'Mean pLDDT\n(Confidence)']
    demand_vals = [
        np.mean([v['anisotropy'] for v in demand_prots.values()]),
        np.mean([v['disorder_fraction'] for v in demand_prots.values()]) * 100,
        np.mean([v['mean_plddt'] for v in demand_prots.values()]),
    ]
    supply_vals = [
        np.mean([v['anisotropy'] for v in supply_prots.values()]),
        np.mean([v['disorder_fraction'] for v in supply_prots.values()]) * 100,
        np.mean([v['mean_plddt'] for v in supply_prots.values()]),
    ]

    # Normalize for visual comparison
    demand_norm = [demand_vals[i] / max(demand_vals[i], supply_vals[i]) * 100 for i in range(3)]
    supply_norm = [supply_vals[i] / max(demand_vals[i], supply_vals[i]) * 100 for i in range(3)]

    x = np.arange(3)
    width = 0.35
    bars1 = ax.bar(x - width/2, demand_norm, width, color=DEMAND_COLOR, alpha=0.7, label='Demand')
    bars2 = ax.bar(x + width/2, supply_norm, width, color=SUPPLY_COLOR, alpha=0.7, label='Supply')

    # Add actual values
    for bar, val in zip(bars1, demand_vals):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold', color=DEMAND_COLOR)
    for bar, val in zip(bars2, supply_vals):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold', color=SUPPLY_COLOR)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
    ax.set_ylabel('Normalized Value (%)', fontsize=11, fontweight='bold')
    ax.set_title('A. The Supply-Side Disorder Paradox', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.2)

    # Highlight the paradox
    ax.annotate('PARADOX: Supply is cheaper\nbut MORE disordered',
                xy=(1, supply_norm[1] + 5), fontsize=10, fontweight='bold',
                ha='center', color='#856404',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3CD', edgecolor='#856404'))

    # Panel B: PPARGC1A spotlight
    ax = axes[1]
    ax.set_facecolor(BG_COLOR)

    # Show PPARGC1A as the fragile bottleneck
    ppargc1a = data['PPARGC1A']
    spotlight_genes = ['PPARGC1A', 'COL1A1', 'SOX9', 'GHR', 'SIRT1']
    spotlight_data = [(g, data[g]) for g in spotlight_genes]

    x_pos = range(len(spotlight_data))
    disorder_vals = [v['disorder_fraction'] * 100 for _, v in spotlight_data]
    plddt_vals = [v['mean_plddt'] for _, v in spotlight_data]

    ax.bar(x_pos, disorder_vals, color=SUPPLY_COLOR, alpha=0.6, width=0.5, label='Disorder %')
    ax2 = ax.twinx()
    ax2.plot(x_pos, plddt_vals, 'D-', color='#27AE60', linewidth=2, markersize=10,
             markerfacecolor='#27AE60', markeredgecolor='white', label='pLDDT')

    ax.set_xticks(x_pos)
    ax.set_xticklabels([g for g, _ in spotlight_data], fontsize=11, fontweight='bold')
    ax.set_ylabel('Disorder Fraction (%)', fontsize=11, fontweight='bold', color=SUPPLY_COLOR)
    ax2.set_ylabel('Mean pLDDT', fontsize=11, fontweight='bold', color='#27AE60')
    ax.set_title('B. Supply Protein Fragility\n(PPARGC1A = metabolic bottleneck)', fontsize=12, fontweight='bold')

    # Annotate PPARGC1A
    ax.annotate(f'pLDDT = {ppargc1a["mean_plddt"]:.1f}\n{ppargc1a["disorder_fraction"]*100:.0f}% disordered\n→ Positive feedback trap',
                xy=(0, disorder_vals[0]),
                xytext=(1.5, disorder_vals[0] + 5),
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black'),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FADBD8', edgecolor='#C0392B'))

    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9)

    plt.tight_layout()
    plt.savefig(f"{OUTDIR}/fig_supply_paradox.pdf", dpi=300, bbox_inches='tight')
    plt.savefig(f"{OUTDIR}/fig_supply_paradox.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 4: Supply-Side Disorder Paradox")


# ================================================================
# FIGURE 5: Comprehensive Heatmap
# ================================================================
def fig5_heatmap():
    """Create a heatmap of all structural metrics across 23 proteins."""
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor('white')

    # Sort: Demand first (by anisotropy desc), then Supply (by anisotropy desc)
    demand_sorted = sorted(demand_prots.items(), key=lambda x: x[1]['anisotropy'], reverse=True)
    supply_sorted = sorted(supply_prots.items(), key=lambda x: x[1]['anisotropy'], reverse=True)
    all_sorted = demand_sorted + supply_sorted
    genes = [g for g, _ in all_sorted]

    metrics = ['anisotropy', 'mean_plddt', 'disorder_fraction', 'rg_angstrom', 'hinge_candidates', 'asphericity']
    metric_labels = ['Anisotropy\nRatio', 'Mean\npLDDT', 'Disorder\nFraction', 'Rg\n(Å)', 'Hinge\nCandidates', 'Asphericity']

    # Build matrix and normalize per column
    matrix = np.zeros((len(genes), len(metrics)))
    for i, (gene, _) in enumerate(all_sorted):
        for j, m in enumerate(metrics):
            val = data[gene][m]
            if m == 'disorder_fraction':
                val *= 100
            matrix[i, j] = val

    # Z-score normalize per column
    z_matrix = np.zeros_like(matrix)
    for j in range(matrix.shape[1]):
        col = matrix[:, j]
        z_matrix[:, j] = (col - np.mean(col)) / (np.std(col) + 1e-10)

    im = ax.imshow(z_matrix, cmap='RdBu_r', aspect='auto', vmin=-2, vmax=2)

    ax.set_xticks(range(len(metrics)))
    ax.set_xticklabels(metric_labels, fontsize=10, fontweight='bold')
    ax.set_yticks(range(len(genes)))

    # Color gene labels by category
    ytick_labels = ax.set_yticklabels(genes, fontsize=10, fontweight='bold')
    for i, (gene, v) in enumerate(all_sorted):
        color = DEMAND_COLOR if v['category'] == 'Demand' else SUPPLY_COLOR
        ytick_labels[i].set_color(color)

    # Add actual values as text
    for i in range(len(genes)):
        for j in range(len(metrics)):
            val = matrix[i, j]
            if metrics[j] == 'disorder_fraction':
                text = f'{val:.0f}%'
            elif metrics[j] in ['hinge_candidates']:
                text = f'{val:.0f}'
            elif metrics[j] == 'mean_plddt':
                text = f'{val:.0f}'
            elif metrics[j] == 'rg_angstrom':
                text = f'{val:.0f}'
            else:
                text = f'{val:.2f}'
            color = 'white' if abs(z_matrix[i, j]) > 1.2 else 'black'
            ax.text(j, i, text, ha='center', va='center', fontsize=8, color=color, fontweight='bold')

    # Separator line between Demand and Supply
    sep = len(demand_sorted) - 0.5
    ax.axhline(y=sep, color='black', linewidth=2, linestyle='-')
    ax.text(-0.8, sep/2, 'DEMAND', ha='center', va='center', fontsize=11, fontweight='bold',
            color=DEMAND_COLOR, rotation=90)
    ax.text(-0.8, sep + (len(supply_sorted)/2), 'SUPPLY', ha='center', va='center', fontsize=11,
            fontweight='bold', color=SUPPLY_COLOR, rotation=90)

    cbar = plt.colorbar(im, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label('Z-score (column-normalized)', fontsize=10)

    ax.set_title('AlphaFold Structural Metrics Heatmap — 23 IEC Framework Proteins\n'
                 '(Red = high relative value, Blue = low relative value)',
                 fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.savefig(f"{OUTDIR}/fig_heatmap.pdf", dpi=300, bbox_inches='tight')
    plt.savefig(f"{OUTDIR}/fig_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 5: Comprehensive heatmap")


# ================================================================
# FIGURE 6: pLDDT per-residue profiles for key proteins
# ================================================================
def fig6_plddt_profiles():
    """Show per-residue pLDDT profiles for key demand vs supply proteins."""
    # Load full data with per-residue
    with open("/sessions/youthful-pensive-allen/alphafold_data/protein_metrics_full.json") as f:
        full_data = json.load(f)

    key_prots = [('VIM', DEMAND_COLOR), ('LMNA', DEMAND_COLOR), ('PIEZO2', DEMAND_COLOR),
                 ('PPARGC1A', SUPPLY_COLOR), ('COL1A1', SUPPLY_COLOR), ('PLOD1', SUPPLY_COLOR)]

    fig, axes = plt.subplots(3, 2, figsize=(16, 12), sharex=False)
    fig.patch.set_facecolor('white')

    for idx, ((gene, color), ax) in enumerate(zip(key_prots, axes.flat)):
        plddt = full_data[gene]['plddt_per_residue']
        residues = np.arange(1, len(plddt) + 1)

        ax.set_facecolor(BG_COLOR)
        ax.fill_between(residues, plddt, alpha=0.3, color=color)
        ax.plot(residues, plddt, color=color, linewidth=0.8)

        # Confidence thresholds
        ax.axhline(y=90, color='green', alpha=0.3, linestyle=':', linewidth=1)
        ax.axhline(y=70, color='orange', alpha=0.3, linestyle=':', linewidth=1)
        ax.axhline(y=50, color='red', alpha=0.3, linestyle=':', linewidth=1)

        # Background coloring
        ax.axhspan(90, 100, alpha=0.05, color='green')
        ax.axhspan(70, 90, alpha=0.05, color='blue')
        ax.axhspan(50, 70, alpha=0.05, color='yellow')
        ax.axhspan(0, 50, alpha=0.05, color='red')

        cat = full_data[gene]['category']
        mean_plddt = np.mean(plddt)
        disorder = sum(1 for p in plddt if p < 50) / len(plddt) * 100
        anis = full_data[gene]['anisotropy']

        ax.set_title(f'{gene} ({cat}) — pLDDT={mean_plddt:.1f}, Anis={anis:.2f}, Disorder={disorder:.0f}%',
                     fontsize=11, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.set_ylabel('pLDDT', fontsize=10)
        ax.set_xlabel('Residue', fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.suptitle('Per-Residue AlphaFold Confidence (pLDDT) — Key Demand vs Supply Proteins',
                 fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(f"{OUTDIR}/fig_plddt_profiles.pdf", dpi=300, bbox_inches='tight')
    plt.savefig(f"{OUTDIR}/fig_plddt_profiles.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 6: pLDDT per-residue profiles")


# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Creating publication figures...")
    print(f"Output directory: {OUTDIR}\n")
    fig1_anisotropy_bar()
    fig2_scatter_panels()
    fig3_vim_cascade()
    fig4_supply_paradox()
    fig5_heatmap()
    fig6_plddt_profiles()
    print(f"\n✓ All figures saved to {OUTDIR}/")
