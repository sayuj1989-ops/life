
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import json

# Define paths
REPO_ROOT = Path(".").resolve()
sys.path.append(str(REPO_ROOT))

from research.alphafold_countercurvature.src.afcc.structure import StructureParser
from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer

AFCC_DIR = REPO_ROOT / "research" / "alphafold_countercurvature"
DATA_DIR = AFCC_DIR / "data"
OUTPUT_DIR = DATA_DIR / "plots"
MANIFEST_FILE = DATA_DIR / "manifest.csv"
METRICS_FILE = DATA_DIR / "processed" / "protein_metrics.csv"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def plot_plddt(structures_info, output_path):
    n = len(structures_info)
    cols = 4
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(cols*4, rows*3), constrained_layout=True)
    axes = axes.flatten()

    parser = StructureParser()

    for i, row in enumerate(structures_info):
        ax = axes[i]
        pdb_path = Path(row['pdb_path'])
        gene = row['gene_symbol']

        _, plddt, _ = parser.fast_parse_pdb_arrays(pdb_path)

        if len(plddt) > 0:
            ax.plot(plddt, linewidth=1)
            ax.set_title(f"{gene} (Mean: {np.mean(plddt):.1f})")
            ax.set_ylim(0, 100)
            ax.axhline(70, color='orange', linestyle='--', alpha=0.5)
            ax.axhline(90, color='green', linestyle='--', alpha=0.5)
            if i % cols == 0:
                ax.set_ylabel("pLDDT")
            if i >= n - cols:
                ax.set_xlabel("Residue")
        else:
            ax.text(0.5, 0.5, "No Data", ha='center')

    # Hide unused axes
    for j in range(i+1, len(axes)):
        axes[j].axis('off')

    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"📊 Saved {output_path}")

def plot_pae(structures_info, output_path):
    # Select top interesting ones
    # For now, let's pick based on Anisotropy from metrics if available

    targets = ['POC5', 'LMNA', 'PIEZO2']
    selected = [row for row in structures_info if row['gene_symbol'] in targets]

    if not selected:
        selected = structures_info[:3]

    n = len(selected)
    if n == 0: return

    fig, axes = plt.subplots(1, n, figsize=(n*5, 4), constrained_layout=True)
    if n == 1: axes = [axes]

    parser = StructureParser()

    for i, row in enumerate(selected):
        ax = axes[i]
        pae_path = row.get('pae_path')
        gene = row['gene_symbol']

        if pae_path and isinstance(pae_path, str) and Path(pae_path).exists():
            pae = parser.parse_pae(Path(pae_path))
            if pae is not None:
                im = ax.imshow(pae, cmap='Greens_r', vmin=0, vmax=30)
                ax.set_title(f"{gene} PAE")
                if i == 0:
                    ax.set_ylabel("Residue")
                ax.set_xlabel("Residue")
                # plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            else:
                 ax.text(0.5, 0.5, "PAE Load Failed", ha='center')
        else:
            ax.text(0.5, 0.5, "No PAE", ha='center')

    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"📊 Saved {output_path}")

def plot_curvature(structures_info, output_path):
    targets = ['POC5', 'LMNA', 'PIEZO2']
    selected = [row for row in structures_info if row['gene_symbol'] in targets]

    if not selected:
        selected = structures_info[:3]

    n = len(selected)
    if n == 0: return

    fig, axes = plt.subplots(n, 1, figsize=(10, n*3), constrained_layout=True)
    if n == 1: axes = [axes]

    parser = StructureParser()
    analyzer = MetricsAnalyzer()

    for i, row in enumerate(selected):
        ax = axes[i]
        pdb_path = Path(row['pdb_path'])
        gene = row['gene_symbol']

        coords, plddt, _ = parser.fast_parse_pdb_arrays(pdb_path)

        if len(coords) > 0:
            kappa = analyzer.calculate_curvature(coords)

            # Mask low confidence
            mask = plddt >= 70
            kappa_clean = kappa.copy()
            # We can't easily mask the line plot with NaNs without breaking lines,
            # but we can color it.

            # Plot raw curvature in grey
            ax.plot(kappa, color='lightgrey', alpha=0.5, label='Raw Curvature')

            # Plot high confidence segments
            # Create a masked array
            kappa_masked = np.where(mask, kappa, np.nan)
            ax.plot(kappa_masked, color='blue', label='High Confidence (>70)')

            ax.set_title(f"{gene} Backbone Curvature")
            ax.set_ylabel("Kappa (1/A)")
            if i == n-1:
                ax.set_xlabel("Residue")
            ax.legend()
            ax.set_ylim(0, 1.0) # Cap at 1.0 for readability

    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"📊 Saved {output_path}")

def main():
    if not MANIFEST_FILE.exists():
        print("No manifest found.")
        sys.exit(1)

    manifest = pd.read_csv(MANIFEST_FILE)
    # Filter only downloaded
    downloaded = manifest[manifest['status'].isin(['downloaded', 'cached'])]

    # Check if we should filter by seed list
    # The metrics file might have more, but manifest has everything.
    # We'll use manifest rows that are in our seed list if possible.
    # Or just all downloaded since we cleaned the environment (mostly).

    # Convert dataframe to list of dicts
    structures = downloaded.to_dict('records')

    print(f"Generating plots for {len(structures)} structures...")

    plot_plddt(structures, OUTPUT_DIR / "plddt_summary.png")
    plot_pae(structures, OUTPUT_DIR / "pae_summary.png")
    plot_curvature(structures, OUTPUT_DIR / "curvature_summary.png")

if __name__ == "__main__":
    main()
