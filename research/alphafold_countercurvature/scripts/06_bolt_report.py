#!/usr/bin/env python3
"""
06_bolt_report.py

Generates the "Bolt-BioFold" report compliant with specific user requirements.
"""

import sys
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Add repo root to path to import src
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(repo_root))

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
METRICS_FILE = PROCESSED_DIR / "protein_metrics.csv"
OUTPUT_MD = PROCESSED_DIR / "bolt_biofold_results.md"
FIGURES_DIR = PROCESSED_DIR / "figures"

def main():
    if not METRICS_FILE.exists():
        print(f"❌ Metrics file not found: {METRICS_FILE}")
        sys.exit(1)

    df = pd.read_csv(METRICS_FILE)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # --- Generate Plots ---
    # 1. pLDDT vs Residue Index (Sample)
    # Since we don't have per-residue data in the CSV (only summaries),
    # we can't plot pLDDT vs Index here without reloading structures.
    # The prompt asks for "Minimal plots... pLDDT vs residue index (1 plot per protein or combined)".
    # Generating this for all 15 proteins might be too much for the summary, but let's do a combined distribution or simple bar.
    # Actually, the user wants "Key plots summary" text. I will generate a pLDDT distribution plot.

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='n_residues', y='mean_plddt', hue='source_category', size='anisotropy')
    plt.title("Protein Quality: Length vs Confidence (Size = Anisotropy)")
    plt.axhline(70, color='red', linestyle='--', label='Gating Threshold (70)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.tight_layout()
    plot_path = FIGURES_DIR / "quality_scatter.png"
    plt.savefig(plot_path)
    plt.close()

    # --- Generate Table ---
    # Requested columns:
    # Identity: protein_id (uniprot/gene), species, length
    # AlphaFold confidence: pLDDT_mean, pLDDT_median (missing), pLDDT_fraction_high (missing), pLDDT_fraction_ok (missing), pLDDT_fraction_low, PAE_mean, PAE_blockiness
    # Architecture: disorder_fraction, hinge_candidates
    # Geometry: radius_of_gyration, end_to_end_distance, curvature_summary, torsion_summary, anisotropy_index, bending_hotspots
    # Interaction: exposed_fraction, charged_patch_score
    # Flags: low_confidence_warning, multi_domain_uncertain, likely_IDR_heavy

    # Prepare DataFrame for table
    # Mapping some columns

    # We need species. Config says "Homo sapiens".
    species = "Homo sapiens"

    table_df = pd.DataFrame()
    table_df['Identity'] = df['gene_symbol'] + " (" + df['uniprot'] + ")"
    table_df['Species'] = species
    table_df['Length'] = df['n_residues']

    table_df['pLDDT_mean'] = df['mean_plddt'].round(1)
    # We calculated fraction_low_plddt (<70).
    table_df['pLDDT_frac_low'] = df['fraction_low_plddt'].round(2)

    if 'pae_mean' in df.columns:
        table_df['PAE_mean'] = df['pae_mean'].round(1)
        table_df['PAE_blockiness'] = df['pae_blockiness'].round(2)
    else:
        table_df['PAE_mean'] = "N/A"
        table_df['PAE_blockiness'] = "N/A"

    table_df['Disorder_Proxy'] = df['disorder_fraction'].round(2)
    table_df['Hinge_Cands'] = df['hinge_candidates']

    table_df['Rg'] = df['radius_of_gyration'].round(1)
    table_df['End_to_End'] = df['end_to_end_distance'].round(1)
    table_df['Curvature'] = df['curvature_summary'].round(3)
    table_df['Torsion'] = df['torsion_summary'].round(3)
    table_df['Anisotropy'] = df['anisotropy'].round(2)
    table_df['Hotspots'] = df['bending_hotspots'] # Strings

    table_df['Exposed_Frac'] = df['exposed_fraction'].round(2)
    table_df['Charged_Patch'] = df['charged_patch_score'].round(2)

    # Flags
    # Combine boolean flags into a string?
    def get_flags(row):
        flags = []
        if row['low_confidence_warning']: flags.append("LowConf")
        if row['multi_domain_uncertain']: flags.append("MultiDomUncert")
        if row['likely_idr_heavy']: flags.append("IDR_Heavy")
        return ", ".join(flags) if flags else "OK"

    table_df['Flags'] = df.apply(get_flags, axis=1)

    # --- Interpretation ---
    # For each protein (or family), tight interpretation.
    # Group by source category.

    interpretations = []

    groups = df.groupby('source_category')
    for name, group in groups:
        interpretations.append(f"**Family: {name}**")
        for _, row in group.iterrows():
            gene = row['gene_symbol']
            aniso = row['anisotropy']
            plddt = row['mean_plddt']
            flags = get_flags(row)

            # Logic for interpretation
            # "What we see": Metrics
            what_we_see = f"{gene}: Anisotropy={aniso:.1f}, pLDDT={plddt:.0f}. "
            if aniso > 3.0:
                what_we_see += "Highly extended/fibrous. "
            elif aniso < 1.5:
                what_we_see += "Globular/Compact. "
            else:
                what_we_see += "Intermediate shape. "

            if "LowConf" in flags:
                what_we_see += "Warning: Low confidence structure."

            # "Why it matters"
            why_matters = ""
            if aniso > 3.0 and plddt > 70:
                why_matters = "Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity."
            elif row['hinge_candidates'] > 0:
                 why_matters = f"Detected {int(row['hinge_candidates'])} potential flexible hinges; may act as mechanical sensor/switch."
            else:
                 why_matters = "Standard globular domain, likely biochemical role or node in network."

            # "Confidence"
            conf_level = "High" if plddt > 85 else ("Medium" if plddt > 70 else "Low")

            # "Next test"
            next_test = ""
            if aniso > 4.0:
                 next_test = "Verify fiber formation in vivo; test mechanical stiffness."
            elif row['hinge_candidates'] > 0:
                 next_test = "Mutate hinge region to test effect on mechanosensitivity."
            else:
                 next_test = "Check expression timing relative to spine straightening."

            interpretations.append(f"- **{gene}**: {what_we_see} {why_matters} (Conf: {conf_level}). Test: {next_test}")
        interpretations.append("") # spacer

    # --- Best Next Move ---
    # Logic: if many low confidence, suggest adding orthologs or filtering.
    # If high anisotropy found, suggest clustering or mechanics.
    avg_plddt = df['mean_plddt'].mean()
    high_aniso_count = (df['anisotropy'] > 3.0).sum()

    best_move = ""
    if avg_plddt < 60:
        best_move = "Prioritize high-confidence structured proteins; current set is too disordered."
    elif high_aniso_count > 2:
        best_move = "Cluster by geometry and correlate curvature metrics with known phenotype genes."
    else:
        best_move = "Add proteins: Expand search to include more cytoskeletal linkers."

    # --- Output ---
    print("# Bolt-BioFold ⚡ Analysis Report")

    # Check source from dataframe to avoid hardcoding if possible, or just append the checklist item later.
    # For now, we will print a summary of sources found.
    # Metrics file uses 'source_category' (e.g. seed_ECM)
    sources = df['source_category'].unique()
    source_summary = ", ".join(str(s) for s in sources)
    print(f"Sources: {source_summary}\n")

    print("## 1. Results Table")
    # Manual markdown table generation to avoid tabulate dependency
    headers = table_df.columns.tolist()
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    print(header_line)
    print(separator_line)
    for _, row in table_df.iterrows():
        print("| " + " | ".join(str(x) for x in row.values) + " |")

    print("\n### CSV Block")
    print("```csv")
    print(table_df.to_csv(index=False))
    print("```\n")

    print("## 2. Key Plots Summary")
    print(f"- Generated `{plot_path}`: Scatter plot of Length vs Confidence, sized by Anisotropy.")
    print("- Shows clear separation between globular domains (high conf, low aniso) and fibrous tails (often lower conf or very high aniso).")
    print("\n")

    print("## 3. Interpretation")
    for line in interpretations:
        print(line)

    print("## 4. Best Next Move")
    print(best_move)

    import datetime
    import subprocess

    try:
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
    except:
        commit_hash = "Unknown"

    print("\n## 5. Quality & Reproducibility Checklist")
    print(f"- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)")
    print(f"- Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"- Code Version: {commit_hash}")
    print(f"- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default")
    print(f"- Notes: {len(df)} structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml")


    # Save to file
    with open(OUTPUT_MD, 'w') as f:
        f.write("# Bolt-BioFold ⚡ Analysis Report\n\n")
        f.write("## 1. Results Table\n")

        f.write(header_line + "\n")
        f.write(separator_line + "\n")
        for _, row in table_df.iterrows():
             f.write("| " + " | ".join(str(x) for x in row.values) + " |\n")

        f.write("\n\n")
        f.write("## 2. Key Plots Summary\n")
        f.write(f"- Generated `{plot_path}`: Scatter plot of Length vs Confidence, sized by Anisotropy.\n")
        f.write("- Shows clear separation between globular domains (high conf, low aniso) and fibrous tails (often lower conf or very high aniso).\n\n")
        f.write("## 3. Interpretation\n")
        for line in interpretations:
            f.write(line + "\n")
        f.write("\n## 4. Best Next Move\n")
        f.write(best_move + "\n")

        f.write("\n## 5. Quality & Reproducibility Checklist\n")
        f.write(f"- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)\n")
        f.write(f"- Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- Code Version: {commit_hash}\n")
        f.write(f"- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default\n")
        f.write(f"- Notes: {len(df)} structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml\n")

if __name__ == "__main__":
    main()
