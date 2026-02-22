#!/usr/bin/env python3
"""
bolt_biofold_analysis.py

Implements the "Bolt-BioFold" focused analysis cycle on a defined set of proteins.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

try:
    from tabulate import tabulate
except ImportError:
    print("⚠️ 'tabulate' not installed. Using pandas default output.")
    tabulate = None

# Setup paths
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_ROOT))

from research.alphafold_countercurvature.src.afcc.afdb import AlphaFoldFetcher
from research.alphafold_countercurvature.src.afcc.metrics import MetricsAnalyzer
from research.alphafold_countercurvature.src.afcc.structure import StructureParser

# Configuration
TARGETS = [
    {"gene_symbol": "PIEZO2", "uniprot_id": "Q9H5I5", "desc": "Proprioception/Gravity Sensing"},
    {"gene_symbol": "LBX1", "uniprot_id": "P52954", "desc": "AIS GWAS Hit / Muscle"},
    {"gene_symbol": "RUNX3", "uniprot_id": "Q13761", "desc": "Proprioception Transcription Factor"},
    {"gene_symbol": "HIF1A", "uniprot_id": "Q16665", "desc": "Metabolic / Hypoxic Response"},
    {"gene_symbol": "COL1A1", "uniprot_id": "P02452", "desc": "Structural / ECM"},
]

OUTPUT_DIR = REPO_ROOT / "outputs" / "bolt_biofold"
DATA_DIR = REPO_ROOT / "research" / "alphafold_countercurvature" / "data"
# IMPORTANT: Reuse existing raw data directory structure
RAW_DATA_DIR = DATA_DIR / "raw"
MANIFEST_PATH = DATA_DIR / "bolt_manifest.csv"

def interpret_protein(metrics, desc):
    """
    Generates interpretation bullets based on metrics.
    """
    bullets = []

    # Confidence
    conf_level = "High"
    if metrics['low_confidence_warning']:
        conf_level = "Low (Caution)"
    elif metrics['plddt_mean'] < 80:
        conf_level = "Medium"

    bullets.append(f"- **Confidence Level:** {conf_level} (Mean pLDDT: {metrics['plddt_mean']:.1f})")

    # Morphology
    morph = metrics['morphology']
    aniso = metrics['anisotropy_index']
    bullets.append(f"- **Morphology:** {morph} (Anisotropy: {aniso:.2f})")

    if aniso > 3.0:
        bullets.append("    - High anisotropy suggests fibrous or extended conformation, consistent with structural role or force transmission.")
    elif aniso < 1.5:
        bullets.append("    - Globular shape suggests enzymatic or binding domain function rather than structural span.")

    # Mechanics
    if metrics['hinge_candidates'] > 0:
        bullets.append(f"- **Hinge Detected:** {metrics['hinge_candidates']} potential hinge(s) found. May act as a flexible joint under load.")

    if metrics['likely_IDR_heavy']:
        bullets.append("- **IDR Heavy:** Significant disordered regions (>30%). May involve phase separation or flexible signaling tails.")

    # Context
    bullets.append(f"- **Context:** {desc}")

    # Next Test
    if aniso > 3.0:
        next_test = f"Test tensile strength or persistence length of {metrics['gene_symbol']} in vitro."
    elif metrics['hinge_candidates'] > 0:
        next_test = "Verify hinge flexibility using molecular dynamics or FRET under tension."
    elif metrics['likely_IDR_heavy']:
        next_test = "Test for liquid-liquid phase separation (LLPS) potential under crowding."
    else:
        next_test = "Investigate binding partners to understand mechanotransduction role."

    return bullets, next_test

def main():
    print("⚡ Bolt-BioFold: Starting Focused Analysis Cycle...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True) # Ensure raw dir exists

    # 1. Fetch Data
    print("\n📡 Fetching AlphaFold Structures...")
    # Initialize fetcher with RAW_DATA_DIR.
    # Note: AlphaFoldFetcher appends /afdb to this path internally for downloads.
    fetcher = AlphaFoldFetcher(data_dir=RAW_DATA_DIR, manifest_path=MANIFEST_PATH)

    # Reload targets from manifest if they exist to get paths
    manifest_df = pd.DataFrame()
    if MANIFEST_PATH.exists():
        manifest_df = pd.read_csv(MANIFEST_PATH)

    for t in TARGETS:
        # Check if already in manifest
        if not manifest_df.empty and t['uniprot_id'] in manifest_df['uniprot'].values:
            row = manifest_df[manifest_df['uniprot'] == t['uniprot_id']].iloc[0]
            t['status'] = row['status']
            t['pdb_path'] = row['pdb_path']
            t['pae_path'] = row['pae_path'] if 'pae_path' in row else None
            print(f"   Using cached info for {t['gene_symbol']}")
        else:
            res = fetcher.fetch_protein(t['uniprot_id'], t['gene_symbol'])
            t['status'] = res.get('status', 'unknown')
            t['pdb_path'] = res.get('pdb_path')
            t['pae_path'] = res.get('pae_path')

    # 2. Analyze
    print("\n🔬 Analyzing Structures...")
    parser = StructureParser()
    analyzer = MetricsAnalyzer()

    results = []

    for t in TARGETS:
        if t['status'] not in ['downloaded', 'cached']:
            print(f"⚠️ Skipping {t['gene_symbol']} (Status: {t['status']})")
            continue

        pdb_rel = t.get('pdb_path')
        if not pdb_rel:
             # Fallback: construct path manually if not in manifest return
             # fetcher uses RAW_DATA_DIR/afdb/{uniprot}/{uniprot}.pdb
             pdb_file = RAW_DATA_DIR / "afdb" / t['uniprot_id'] / f"{t['uniprot_id']}.pdb"
        else:
             # pdb_path in manifest is relative to REPO_ROOT
             pdb_file = REPO_ROOT / pdb_rel

        if not pdb_file.exists():
            print(f"❌ PDB file not found: {pdb_file}")
            continue

        print(f"   Processing {t['gene_symbol']}...")

        # Parse
        coords, plddt, resnames = parser.fast_parse_pdb_arrays(pdb_file)

        # PAE
        pae_matrix = None
        pae_rel = t.get('pae_path')
        if pae_rel and isinstance(pae_rel, str):
            pae_file = REPO_ROOT / pae_rel
            if pae_file.exists():
                pae_matrix = parser.parse_pae(pae_file)

        # Analyze
        metrics = analyzer.analyze_structure(plddt_scores=plddt, coords=coords, resnames=resnames, pae_matrix=pae_matrix)
        metrics['gene_symbol'] = t['gene_symbol']
        metrics['uniprot_id'] = t['uniprot_id']
        metrics['desc'] = t['desc']

        results.append(metrics)

    if not results:
        print("❌ No results generated.")
        return

    # 3. Generate Report
    print("\n📝 Generating Report...")
    df = pd.DataFrame(results)

    # Select columns for table
    cols_display = ['gene_symbol', 'uniprot_id', 'plddt_mean', 'anisotropy_index', 'radius_of_gyration', 'morphology', 'hinge_candidates', 'exposed_surface_proxy']

    if tabulate:
        table = tabulate(df[cols_display], headers='keys', tablefmt='pipe', floatfmt=".2f")
    else:
        table = df[cols_display].to_string(index=False)

    # Plots
    print("   Generating plots...")

    # pLDDT Plot
    plt.figure(figsize=(10, 6))
    for t in TARGETS:
         if t['gene_symbol'] not in df['gene_symbol'].values: continue

         pdb_rel = t.get('pdb_path')
         if pdb_rel:
             pdb_file = REPO_ROOT / pdb_rel
         else:
             pdb_file = RAW_DATA_DIR / "afdb" / t['uniprot_id'] / f"{t['uniprot_id']}.pdb"

         _, plddt, _ = parser.fast_parse_pdb_arrays(pdb_file)
         plt.plot(plddt, label=t['gene_symbol'], alpha=0.7)

    plt.title("AlphaFold Confidence (pLDDT) per Residue")
    plt.xlabel("Residue Index")
    plt.ylabel("pLDDT")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plddt_plot_path = OUTPUT_DIR / "plddt_plots.png"
    plt.savefig(plddt_plot_path)
    plt.close()

    # Curvature Plot
    plt.figure(figsize=(10, 6))
    for t in TARGETS:
         if t['gene_symbol'] not in df['gene_symbol'].values: continue

         pdb_rel = t.get('pdb_path')
         if pdb_rel:
             pdb_file = REPO_ROOT / pdb_rel
         else:
             pdb_file = RAW_DATA_DIR / "afdb" / t['uniprot_id'] / f"{t['uniprot_id']}.pdb"

         coords, plddt, _ = parser.fast_parse_pdb_arrays(pdb_file)

         # Calculate curvature again
         kappa = analyzer.calculate_curvature(coords)

         # Plot
         # Use a rolling mean to smooth noisy curvature
         kappa_series = pd.Series(kappa)
         kappa_smooth = kappa_series.rolling(window=5, center=True).mean()

         plt.plot(kappa_smooth, label=f"{t['gene_symbol']}", alpha=0.6)

    plt.title("Backbone Curvature (Kappa) - Smoothed")
    plt.xlabel("Residue Index")
    plt.ylabel("Curvature (1/A)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 0.5)
    curv_plot_path = OUTPUT_DIR / "curvature_plots.png"
    plt.savefig(curv_plot_path)
    plt.close()

    # Markdown Report
    report_content = f"""# Bolt-BioFold Analysis Report
**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
**Targets:** {', '.join([r['gene_symbol'] for r in results])}

## 1. Results Table
{table}

## 2. Key Plots
![pLDDT](plddt_plots.png)
![Curvature](curvature_plots.png)

## 3. Interpretation
"""

    best_next_moves = []

    for _, row in df.iterrows():
        bullets, next_move = interpret_protein(row, row['desc'])
        report_content += f"\n### {row['gene_symbol']}\n"
        for b in bullets:
            report_content += f"{b}\n"
        best_next_moves.append(f"{row['gene_symbol']}: {next_move}")

    report_content += "\n## 4. Best Next Move\n"

    # Logic to pick best move
    # Sort by anisotropy (descending)
    best_candidate = df.sort_values('anisotropy_index', ascending=False).iloc[0]
    best_move_text = f"Prioritize **{best_candidate['gene_symbol']}** for mechanical testing due to extreme anisotropy ({best_candidate['anisotropy_index']:.2f})."

    report_content += f"{best_move_text}\n"

    # Save Report
    report_path = OUTPUT_DIR / "report.md"
    with open(report_path, "w") as f:
        f.write(report_content)

    print(f"\n✅ Report saved to {report_path}")
    print(f"📊 Plots saved to {OUTPUT_DIR}")

    # Print summary to stdout
    print("\n--- REPORT SUMMARY ---")
    print(table)
    print(f"\nBest Next Move: {best_move_text}")

if __name__ == "__main__":
    main()
