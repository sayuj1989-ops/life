import pandas as pd
import os

def main():
    # Authoritative latest snapshot
    snapshot_file = "outputs/afcc/2026-02-16/metrics.csv"
    df = pd.read_csv(snapshot_file)

    # We also need LMNA and RUNX3 if not in 2026-02-16 snapshot
    # Let's search previous runs for missing comparators
    comparators = ["LBX1", "PIEZO2", "LMNA", "ADGRG6", "RUNX3", "POC5", "GHR"]
    all_genes_needed = comparators

    missing_genes = [g for g in all_genes_needed if g not in df['gene_symbol'].values]

    if missing_genes:
        # Search backward through runs
        base_dir = "outputs/afcc"
        folders = sorted([f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and f.startswith("2026-")], reverse=True)

        found_genes = []
        for folder in folders:
            if folder == "2026-02-16": continue
            past_file = os.path.join(base_dir, folder, "metrics.csv")
            if os.path.exists(past_file):
                try:
                    past_df = pd.read_csv(past_file)
                    col_name = "gene_symbol" if "gene_symbol" in past_df.columns else "Identity"
                    for g in missing_genes:
                        if g in found_genes: continue
                        # Find the gene
                        if col_name == "Identity":
                            row = past_df[past_df[col_name].str.startswith(g)]
                        else:
                            row = past_df[past_df[col_name] == g]

                        if not row.empty:
                            # Add to df
                            # map columns if needed
                            if col_name == "Identity":
                                # Very basic mapping for old format if it appears
                                pass
                            else:
                                df = pd.concat([df, row.iloc[[0]]], ignore_index=True)
                                found_genes.append(g)
                except Exception:
                    pass
            if len(found_genes) == len(missing_genes):
                break

    # Calculate confidence class
    # Confidence: Adequate = pLDDT >= 70, Low = pLDDT < 70
    # High Anisotropy: >= 3.0

    df['confidence_class'] = df['plddt_mean'].apply(lambda x: 'Adequate' if x >= 70 else 'Low')
    df['anisotropy_class'] = df['anisotropy_index'].apply(lambda x: 'High' if x >= 3.0 else 'Intermediate/Low')

    # 1. High-anisotropy + adequate-confidence
    high_adequate = df[(df['anisotropy_class'] == 'High') & (df['confidence_class'] == 'Adequate')].sort_values('anisotropy_index', ascending=False)

    # 2. High-anisotropy + low-confidence
    high_low = df[(df['anisotropy_class'] == 'High') & (df['confidence_class'] == 'Low')].sort_values('anisotropy_index', ascending=False)

    # Save the output CSV
    os.makedirs("outputs/afcc", exist_ok=True)
    df.to_csv("outputs/afcc/confidence_weighted_ranking.csv", index=False)

    # Generate the Markdown report
    with open("reports/confidence_weighted_structural_evidence.md", "w") as f:
        f.write("# Confidence-Weighted Structural Evidence Report\n\n")
        f.write("## Data Source\n")
        f.write("- **Primary Snapshot:** `outputs/afcc/2026-02-16/metrics.csv`\n")
        f.write("- **Methodology:** pLDDT >= 70 defines 'Adequate Confidence'. Anisotropy >= 3.0 defines 'High Anisotropy'.\n\n")

        f.write("## 1. High-Anisotropy + Adequate-Confidence (Strongest Evidence)\n")
        f.write("These candidates possess both extended geometries and high structural reliability.\n\n")
        f.write("| Gene | Anisotropy | pLDDT Mean | PAE Blockiness |\n")
        f.write("|---|---|---|---|\n")
        for _, row in high_adequate.iterrows():
            f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} |\n")

        f.write("\n## 2. High-Anisotropy + Low-Confidence (Exploratory Only)\n")
        f.write("These candidates show extended geometries but low structural reliability, often indicating intrinsic disorder. They should generate hypotheses, not conclusions.\n\n")
        f.write("| Gene | Anisotropy | pLDDT Mean | PAE Blockiness |\n")
        f.write("|---|---|---|---|\n")
        for _, row in high_low.iterrows():
            f.write(f"| {row['gene_symbol']} | {row['anisotropy_index']:.2f} | {row['plddt_mean']:.1f} | {row['PAE_domain_blockiness_score']:.2f} |\n")

        f.write("\n## 3. LBX1 Comparator Analysis\n")
        f.write("Comparing LBX1 against key anchor genes to contextualize its structural plausibility as a direct mechanosensor.\n\n")
        f.write("| Gene | Anisotropy | pLDDT Mean | PAE Blockiness | Confidence | Notes |\n")
        f.write("|---|---|---|---|---|---|\n")

        for g in comparators:
            row_data = df[df['gene_symbol'] == g]
            if not row_data.empty:
                r = row_data.iloc[0]
                conf = r['confidence_class']
                notes = "Strong tension rod" if (conf == "Adequate" and r['anisotropy_index'] >= 4) else "Low-confidence outlier" if r['anisotropy_index'] >= 20 else ""
                if g == "LBX1": notes = "Baseline, static, blocky"
                f.write(f"| {r['gene_symbol']} | {r['anisotropy_index']:.2f} | {r['plddt_mean']:.1f} | {r['PAE_domain_blockiness_score']:.2f} | {conf} | {notes} |\n")

if __name__ == "__main__":
    main()
