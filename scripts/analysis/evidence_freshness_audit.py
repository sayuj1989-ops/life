import os
import pandas as pd
import glob
from pathlib import Path

def audit_freshness():
    afcc_dir = Path("outputs/afcc")
    all_files = sorted(glob.glob(str(afcc_dir / "2026-*" / "metrics.csv")))

    if not all_files:
        print("No metrics files found.")
        return

    history = []
    canonical_columns = None
    schema_drifts = []
    missing_outputs = []

    for f in all_files:
        date_str = Path(f).parent.name
        run_dir = Path(f).parent

        try:
            df = pd.read_csv(f)
            df['run_date'] = date_str
            history.append(df)

            # Check schema drift
            if canonical_columns is None:
                canonical_columns = set(df.columns) - {'run_date'}
            else:
                current_columns = set(df.columns) - {'run_date'}
                missing_cols = canonical_columns - current_columns
                extra_cols = current_columns - canonical_columns
                if missing_cols or extra_cols:
                    schema_drifts.append({
                        'date': date_str,
                        'missing_from_canonical': list(missing_cols),
                        'extra_over_canonical': list(extra_cols)
                    })

            # Check missing linked outputs (assuming PDBs should exist if n_residues > 0 or similar,
            # or check if specific expected files are missing in the run directory)
            # A common missing output is the metrics file itself if it was empty, but we're reading it.
            # We'll check if the corresponding report file exists in reports/afcc_YYYY-MM-DD.md
            # Or if standard outputs like PDBs are missing. Since we don't know the exact structure,
            # we'll look for a generic "metadata.json" or similar that might be missing, or just note
            # if the directory is surprisingly empty compared to the CSV rows.

            num_structures = len(df)
            # In a real scenario, we might check for `outputs/afcc/{date}/pdb/`
            pdb_dir = run_dir / "pdb"
            if pdb_dir.exists():
                pdb_count = len(list(pdb_dir.glob("*.pdb")))
                if pdb_count < num_structures:
                    missing_outputs.append({
                        'date': date_str,
                        'expected_structures': num_structures,
                        'found_pdbs': pdb_count
                    })
            else:
                # If the directory doesn't exist but we have rows, flag it.
                missing_outputs.append({
                    'date': date_str,
                    'issue': "No 'pdb' directory found, but metrics exist."
                })

        except Exception as e:
            print(f"Error reading {f}: {e}")

    if not history:
        return

    full_df = pd.concat(history, ignore_index=True)

    # Check for static values across runs
    print("Finding static proteins...")
    static_summary = []

    genes = full_df['gene_symbol'].unique()
    for gene in genes:
        gene_data = full_df[full_df['gene_symbol'] == gene].sort_values('run_date')
        if len(gene_data) > 1:
            # Check if key metrics are exactly identical across all appearances
            key_cols = ['anisotropy_index', 'plddt_mean']
            is_static = True
            for col in key_cols:
                if gene_data[col].nunique() > 1:
                    is_static = False
                    break
            if is_static:
                static_summary.append({
                    'gene_symbol': gene,
                    'appearances': len(gene_data),
                    'first_seen': gene_data['run_date'].iloc[0],
                    'last_seen': gene_data['run_date'].iloc[-1],
                    'anisotropy': gene_data['anisotropy_index'].iloc[0],
                    'plddt': gene_data['plddt_mean'].iloc[0]
                })

    static_df = pd.DataFrame(static_summary)
    print(f"Found {len(static_df)} proteins with completely static metrics across multiple runs.")

    report_content = [
        "# Evidence Freshness Audit",
        "",
        "## Overview",
        f"Analyzed {len(all_files)} runs from {all_files[0].split('/')[-2]} to {all_files[-1].split('/')[-2]}.",
        "",
        "## Schema Drifts",
    ]

    if schema_drifts:
        report_content.append("The following runs exhibited schema deviations from the canonical (first observed) structure:")
        for drift in schema_drifts:
            report_content.append(f"- **{drift['date']}**: Missing {drift['missing_from_canonical']}, Extra {drift['extra_over_canonical']}")
    else:
        report_content.append("No schema drifts detected across all analyzed runs.")

    report_content.extend([
        "",
        "## Missing Linked Outputs",
    ])

    if missing_outputs:
        report_content.append("The following runs have missing linked outputs (e.g., PDB files not matching metrics count):")
        for mo in missing_outputs:
            if 'issue' in mo:
                report_content.append(f"- **{mo['date']}**: {mo['issue']}")
            else:
                report_content.append(f"- **{mo['date']}**: Expected {mo['expected_structures']} structures, but found {mo['found_pdbs']} PDBs.")
    else:
        report_content.append("All expected linked outputs are present.")

    report_content.extend([
        "",
        "## Static Metrics Warning",
        "The following proteins show identical structural metrics across multiple historical runs, indicating the underlying AFDB structures have not been updated or are being reused from cache:",
        ""
    ])

    if not static_df.empty:
        static_df = static_df.sort_values('appearances', ascending=False)
        report_content.append(static_df.to_markdown(index=False))
    else:
        report_content.append("No completely static proteins found.")

    with open("reports/evidence_freshness_audit.md", "w") as f:
        f.write("\n".join(report_content))

    print("Generated reports/evidence_freshness_audit.md")

if __name__ == "__main__":
    audit_freshness()
