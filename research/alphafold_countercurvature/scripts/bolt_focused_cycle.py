#!/usr/bin/env python3
"""
Bolt-BioFold ⚡ - Focused Analysis Cycle
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Setup path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

from research.alphafold_countercurvature.src.afcc.afdb import AlphaFoldFetcher
from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer
from research.alphafold_countercurvature.src.afcc.structure import StructureParser

# Constants
DEFAULT_SEED_LIST = [
    ("Q9H5I5", "PIEZO2"),
    ("P02452", "COL1A1"),
    ("P18206", "VCL"),
    ("Q13418", "ILK"),
    ("P21810", "BGN")
]

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_FILE = DATA_DIR / "manifest.csv"

def df_to_markdown(df):
    """Converts a DataFrame to a Markdown table string."""
    columns = df.columns.tolist()
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for _, row in df.iterrows():
        # format floats
        vals = []
        for v in row.values:
            if isinstance(v, float):
                vals.append(f"{v:.2f}")
            else:
                vals.append(str(v))
        row_str = "| " + " | ".join(vals) + " |"
        rows.append(row_str)
    return "\n".join([header, separator] + rows)

def get_interpretation(metrics, gene):
    """Generates a tight interpretation based on metrics."""
    # Confidence
    if metrics['low_confidence_warning']:
        confidence = "Low"
        what = f"pLDDT mean {metrics['plddt_mean']:.1f} indicates mostly low-confidence regions."
    elif metrics['plddt_mean'] > 85:
        confidence = "High"
        what = f"High pLDDT mean ({metrics['plddt_mean']:.1f}) suggests well-structured regions."
    else:
        confidence = "Medium"
        what = f"Moderate pLDDT mean ({metrics['plddt_mean']:.1f})."

    # Morphology
    aniso = metrics['anisotropy_index']
    if not np.isnan(aniso):
        what += f" Anisotropy index is {aniso:.2f}."
        if aniso > 3.0:
            why = "High aspect ratio supports tension transmission or structural scaffolding."
        elif aniso > 2.0:
            why = "Moderate anisotropy suggests a structural element."
        else:
            why = "Globular domain likely involved in signaling or binding."
    else:
        why = "No high-confidence structured domains detected."

    # Mechanics
    curv = metrics['curvature_summary']
    if curv > 0.5:
        what += f" High mean curvature ({curv:.2f})."

    hinges = metrics['hinge_candidates']
    if hinges > 0:
        what += f" Detected {hinges} potential hinge(s)."
        next_test = "Compare curvature under stress in simulation."
    else:
        next_test = "Check expression gradients in developing spine."

    return {
        'what': what,
        'why': why,
        'confidence': confidence,
        'next_test': next_test
    }

def plot_plddt(plddt_scores, gene, output_path):
    plt.figure(figsize=(8, 4))
    plt.plot(plddt_scores, label='pLDDT', color='blue', linewidth=1)
    plt.axhline(70, color='orange', linestyle='--', label='Confidence Threshold (70)')
    plt.axhline(90, color='green', linestyle=':', label='High Confidence (90)')
    plt.title(f"pLDDT Profile: {gene}")
    plt.xlabel("Residue Index")
    plt.ylabel("pLDDT")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_pae(pae_matrix, gene, output_path):
    plt.figure(figsize=(6, 6))
    # PAE typically 0-30+ Angstroms
    plt.imshow(pae_matrix, cmap='Greens_r', vmin=0, vmax=30, origin='upper')
    plt.colorbar(label='Predicted Aligned Error (Å)')
    plt.title(f"PAE Matrix: {gene}")
    plt.xlabel("Residue Index")
    plt.ylabel("Residue Index")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def run_focused_cycle(targets=None):
    print("⚡ Bolt-BioFold: Starting Focused Analysis Cycle")

    if not targets:
        print("   No input provided. Using Default Seed List.")
        targets = DEFAULT_SEED_LIST
        is_default = True
    else:
        is_default = False

    # 1. Fetch
    fetcher = AlphaFoldFetcher(data_dir=DATA_DIR / "raw", manifest_path=MANIFEST_FILE)

    analyzed_data = []

    parser = StructureParser()
    analyzer = MetricsAnalyzer()

    for uniprot, gene in targets:
        print(f"\n   Processing {gene} ({uniprot})...")
        res = fetcher.fetch_protein(uniprot, gene)

        if res['status'] not in ['downloaded', 'cached']:
            print(f"   ❌ Failed to fetch {gene}. Skipping.")
            continue

        # Handle API inconsistency (cached returns full dict, downloaded returns status only)
        if 'pdb_path' in res:
            pdb_path = Path(res['pdb_path'])
            pae_path = Path(res['pae_path']) if res.get('pae_path') and pd.notna(res.get('pae_path')) else None
        else:
            # Retrieve from updated manifest in fetcher
            try:
                row = fetcher.manifest[fetcher.manifest['uniprot'] == uniprot].iloc[0]
                pdb_path = Path(row['pdb_path'])
                pae_val = row['pae_path']
                pae_path = Path(pae_val) if pae_val and pd.notna(pae_val) else None
            except Exception as e:
                print(f"      ⚠️ Error retrieving path from manifest: {e}")
                # Fallback to standard path construction
                protein_dir = DATA_DIR / "raw" / "afdb" / uniprot
                pdb_path = protein_dir / f"{uniprot}.pdb"
                pae_path = protein_dir / f"{uniprot}_pae.json"

        # 2. Parse & Analyze
        print("      Parsing and analyzing...")
        # Use fast parser for speed/caching
        coords, plddt, resnames = parser.fast_parse_pdb_arrays(pdb_path)

        if coords is None:
            print("      ❌ Failed to parse structure.")
            continue

        pae_matrix = None
        if pae_path and pae_path.exists():
            pae_matrix = parser.parse_pae(pae_path)
        elif pae_path:
             print(f"      ⚠️ PAE path set but file missing: {pae_path}")

        metrics = analyzer.analyze_structure(
            plddt_scores=plddt,
            coords=coords,
            resnames=resnames,
            pae_matrix=pae_matrix
        )

        # Add flags for missing artifacts
        metrics['missing_pae'] = pae_matrix is None

        # 3. Interpret
        interpretation = get_interpretation(metrics, gene)

        # 4. Plots
        plot_plddt_path = OUTPUT_DIR / f"plot_{gene}_plddt.png"
        plot_plddt(plddt, gene, plot_plddt_path)

        plot_pae_path = None
        if pae_matrix is not None:
             plot_pae_path = OUTPUT_DIR / f"plot_{gene}_pae.png"
             plot_pae(pae_matrix, gene, plot_pae_path)

        # Construct Row (Full Schema)
        row = {
            # Identity
            'protein_id': gene,
            'uniprot': uniprot,
            'species': 'human', # Default per prompt
            'length': metrics['n_residues'],

            # Confidence
            'pLDDT_mean': metrics['plddt_mean'],
            'pLDDT_median': metrics['plddt_median'],
            'pLDDT_fraction_high': metrics['plddt_fraction_high'],
            'pLDDT_fraction_ok': metrics['plddt_fraction_ok'],
            'pLDDT_fraction_low': metrics['plddt_fraction_low'],
            'PAE_mean': metrics['PAE_mean'],
            'PAE_domain_blockiness_score': metrics['PAE_domain_blockiness_score'],

            # Architecture
            'predicted_domain_segments': metrics['predicted_domain_segments'],
            'disorder_fraction_proxy': metrics['disorder_fraction_proxy'],
            'hinge_candidates': metrics['hinge_candidates'],

            # Geometry
            'backbone_principal_axis': metrics['backbone_principal_axis'],
            'radius_of_gyration': metrics['radius_of_gyration'],
            'end_to_end_distance': metrics['end_to_end_distance'],
            'curvature_summary': metrics['curvature_summary'],
            'torsion_summary': metrics['torsion_summary'],
            'anisotropy_index': metrics['anisotropy_index'],
            'bending_hotspots': metrics['bending_hotspots'],

            # Interaction
            'exposed_surface_proxy': metrics['exposed_surface_proxy'],
            'charged_patch_score': metrics['charged_patch_score'],

            # Flags
            'low_confidence_warning': metrics['low_confidence_warning'],
            'multi_domain_uncertain': metrics['multi_domain_uncertain'],
            'likely_IDR_heavy': metrics['likely_IDR_heavy'],
            'missing_pae': metrics['missing_pae'],

            # Interpretation
            'confidence_level': interpretation['confidence'],
            'what': interpretation['what'],
            'why': interpretation['why'],
            'next_test': interpretation['next_test']
        }
        analyzed_data.append(row)

    # Output Generation
    if not analyzed_data:
        print("❌ No data analyzed.")
        return

    df = pd.DataFrame(analyzed_data)

    # Save CSV
    csv_path = OUTPUT_DIR / "bolt_biofold_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n   💾 Results saved to {csv_path}")

    # Save Markdown Report
    md_path = OUTPUT_DIR / "bolt_biofold_results.md"

    # Determine Best Next Move
    high_aniso = df[df['anisotropy_index'] > 3.0]
    if not high_aniso.empty:
        best_move = f"Simulate mechanical load on high-anisotropy candidates: {', '.join(high_aniso['protein_id'].tolist())}"
    else:
        best_move = "Expand candidate list to include more cytoskeletal cross-linkers."

    with open(md_path, 'w') as f:
        f.write("# Bolt-BioFold ⚡ Analysis Report\n\n")

        f.write("## Reproducibility Checklist\n")
        f.write(f"- **Source:** {'Default Seed List (AlphaFold DB)' if is_default else 'User Input (AlphaFold DB)'}\n")
        f.write(f"- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("- **Commit:** (Not checked dynamically in this script)\n")
        f.write("- **Params:** pLDDT threshold=70, smoothing_window=N/A, Segmentation rule=Consistent high pLDDT + PAE blockiness\n")

        missing_pae_genes = df[df['missing_pae']]['protein_id'].tolist()
        if missing_pae_genes:
             f.write(f"- **Notes:** PAE JSON missing for: {', '.join(missing_pae_genes)}\n\n")
        else:
             f.write("- **Notes:** All requested artifacts successfully loaded.\n\n")

        # Stop condition: If geometry is meaningless due to low confidence
        if df['pLDDT_mean'].mean() < 55.0 and len(df) <= 2:
            f.write("## BLOCKED REPORT\n")
            f.write("Analysis blocked. Results are dominated by low-confidence regions such that geometry is meaningless.\n")
            f.write("Please run on different targets or orthologs with higher confidence structures.\n")
            return

        f.write("## Results Table\n\n")

        # Drop internal flag before markdown/csv
        df_out = df.drop(columns=['missing_pae'])
        f.write(df_to_markdown(df_out))

        f.write("\n\n### CSV-Ready Block\n")
        f.write("```csv\n")
        f.write(df_out.to_csv(index=False))
        f.write("```\n")

        f.write("\n\n## Key Plots Summary\n")
        f.write("*   Generated pLDDT profiles for all proteins.\n")
        f.write("*   Generated PAE heatmaps for proteins with available PAE data.\n")

        f.write("\n## Interpretations\n")
        for _, row in df.iterrows():
            f.write(f"\n### {row['protein_id']} ({row['uniprot']})\n")
            f.write(f"- **What we see:** {row['what']}\n")
            f.write(f"- **Why it matters:** {row['why']}\n")
            f.write(f"- **Confidence level:** {row['confidence_level']}\n")
            f.write(f"- **Next test:** {row['next_test']}\n")

        f.write("\n## Best Next Move\n")
        f.write(f"🚀 **{best_move}**\n")

    print(f"   📄 Report saved to {md_path}")
    print(f"\n   🚀 Best Next Move: {best_move}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    run_focused_cycle()
