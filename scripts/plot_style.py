import matplotlib.pyplot as plt

def apply_nature_style():
    """Apply unified visual styling for Nature manuscript figures."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 8,
        'axes.labelsize': 8,
        'axes.titlesize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'legend.title_fontsize': 8,
        'figure.titlesize': 12,
        'lines.linewidth': 1.5,
        'axes.linewidth': 1.0,
        'axes.grid': False,
        'grid.alpha': 0.3,
        'axes.prop_cycle': plt.cycler('color', ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F', '#8491B4', '#91D1C2', '#DC0000', '#7E6148', '#B09C85']),
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,
        'figure.dpi': 300,
    })
