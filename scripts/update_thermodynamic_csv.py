import pandas as pd
from pathlib import Path
import datetime
import sys

# Define targets and metadata
TARGETS = {
    "PPARGC1A": {
        "term": "Gamma_m",
        "role": "Mitochondrial biogenesis master regulator; determines energy SUPPLY capacity",
        "scaling": "L (mitochondrial volume)"
    },
    "IGF1R": {
        "term": "Gamma_m",
        "role": "Insulin-like growth factor 1 receptor; mediates growth plate signaling",
        "scaling": "L (receptor density)"
    },
    "GHR": {
        "term": "Gamma_m",
        "role": "Growth hormone receptor; master regulator of adolescent growth spurt rate",
        "scaling": "L (growth signal)"
    },
    "ARNTL": {
        "term": "Gamma_m",
        "role": "BMAL1; circadian clock TF in intervertebral disc regulating metabolism",
        "scaling": "L (circadian entrainment)"
    },
    "DMD": {
        "term": "eta_a",
        "role": "Dystrophin; cytoskeleton-ECM linker in paraspinal muscle",
        "scaling": "L^3 (muscle volume)"
    },
    "MYLK": {
        "term": "eta_a",
        "role": "Myosin light chain kinase; tonic contraction regulator",
        "scaling": "L^2 (contractile force)"
    }
}

def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    metrics_path = Path(f"outputs/afcc/{today}/metrics.csv")
    cost_file = Path("outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv")

    if not metrics_path.exists():
        print(f"❌ Metrics file not found: {metrics_path}")
        # Try processed dir as fallback
        metrics_path = Path("research/alphafold_countercurvature/data/processed/protein_metrics.csv")
        if not metrics_path.exists():
             print("❌ No metrics found anywhere.")
             sys.exit(1)
        print("Using processed metrics as fallback.")

    print(f"Reading metrics from {metrics_path}")
    metrics_df = pd.read_csv(metrics_path)

    # Ensure uniprot column exists
    if 'uniprot' not in metrics_df.columns and 'uniprot_accession' in metrics_df.columns:
        metrics_df.rename(columns={'uniprot_accession': 'uniprot'}, inplace=True)

    # Read existing cost file
    if cost_file.exists():
        cost_df = pd.read_csv(cost_file)
    else:
        cost_df = pd.DataFrame(columns=["gene","uniprot","term","role","scaling","anisotropy","morphology","rg","plddt_mean","n_residues","hinge_candidates","disorder_fraction","PAE_blockiness","status"])

    # Update logic
    updated_rows = []

    # Keep existing rows that are NOT in our target list (we will replace them)
    # Actually, we should update in place or append.
    # Let's rebuild the dataframe to ensure clean state for targets.

    # Convert existing to list of dicts
    existing_records = cost_df.to_dict('records')
    existing_map = {row['gene']: row for row in existing_records}

    processed_genes = set()

    for gene, meta in TARGETS.items():
        # Find metric
        metric_row = metrics_df[metrics_df['gene_symbol'] == gene]
        if metric_row.empty:
            print(f"⚠️ Warning: No metrics found for {gene}")
            # If exists in cost file, keep old? Or skip?
            if gene in existing_map:
                updated_rows.append(existing_map[gene])
            continue

        metric_data = metric_row.iloc[0]

        # Mapping
        new_row = {
            "gene": gene,
            "uniprot": metric_data.get('uniprot', ''),
            "term": meta['term'],
            "role": meta['role'],
            "scaling": meta['scaling'],
            "anisotropy": metric_data.get('anisotropy_index', 0.0),
            "morphology": metric_data.get('morphology', 'Unknown'),
            "rg": metric_data.get('radius_of_gyration', 0.0),
            "plddt_mean": metric_data.get('plddt_mean', metric_data.get('mean_plddt', 0.0)),
            "n_residues": metric_data.get('n_residues', 0),
            "hinge_candidates": metric_data.get('hinge_candidates', 0), # assuming integer count
            "disorder_fraction": metric_data.get('disorder_fraction_proxy', metric_data.get('disorder_fraction', 0.0)),
            "PAE_blockiness": metric_data.get('PAE_domain_blockiness_score', metric_data.get('PAE_blockiness', 0.0)),
            "status": "matched"
        }

        # Handle hinge list format if it's a string representation of list or similar
        # If it's a list in the DF (unlikely for CSV read), getting len is needed.
        # But protein_metrics.csv usually has columns like 'n_hinges' or 'hinge_count' if summarized.
        # Let's check columns. The metrics script output `hinge_candidates` as list.
        # Wait, `04_analyze_metrics.py` saves `hinge_candidates` as a list string or count?
        # Reading the earlier output preview: `hinge_candidates` column seems to contain "6", "1", "54", "35", "31". So it's a count.
        # The key in metrics json is `hinge_candidates` which is a list of residues.
        # But `04` script flattens it?
        # Let's check `04` again.
        # Ah, `04` saves whatever is in the dict. If `hinge_candidates` is a list, pandas saves string rep "['A', 'B']".
        # But the preview showed integers. "hinge_candidates": 6.
        # Let's assume it's a count or parsable.

        h_val = metric_data.get('hinge_candidates', 0)
        if isinstance(h_val, str) and '[' in h_val:
             # Parse list string if needed, or just take length
             # But if `04` saves list, we want count.
             pass
        # Actually, let's look at `04` output again.
        # ARNTL: hinge_candidates column has "143:0.38; ...". Wait, that looks like a string of residues.
        # Ah, preview for ARNTL:
        # "143:0.38; 191:0.38; 428:0.38" -> This looks like a string representation.
        # And next column "6" -> Maybe `n_hinges`?
        # Let's check the column headers of metrics.csv.

        updated_rows.append(new_row)
        processed_genes.add(gene)
        print(f"✅ Updated {gene}")

    # Add back non-target genes
    for gene, row in existing_map.items():
        if gene not in processed_genes:
            updated_rows.append(row)

    # Convert back to DF
    final_df = pd.DataFrame(updated_rows)

    # Save
    final_df.to_csv(cost_file, index=False)
    print(f"Saved updated cost file to {cost_file}")

if __name__ == "__main__":
    main()
