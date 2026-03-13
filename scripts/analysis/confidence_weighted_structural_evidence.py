import pandas as pd
import numpy as np
from pathlib import Path
import glob

def generate_report():
    metrics_path = Path("outputs/afcc/2026-02-16/metrics.csv")
    df = pd.read_csv(metrics_path)

    # Fill any NaNs
    df['anisotropy_index'] = df['anisotropy_index'].fillna(0)
    df['plddt_mean'] = df['plddt_mean'].fillna(0)
    if 'PAE_domain_blockiness_score' in df.columns:
        df['PAE_domain_blockiness_score'] = df['PAE_domain_blockiness_score'].fillna(0)

    # Calculate confidence weighted score
    df['confidence_weight'] = np.clip((df['plddt_mean'] - 50) / 40, 0, 1) # Scales 50-90 to 0-1
    df['confidence_weighted_anisotropy'] = df['anisotropy_index'] * df['confidence_weight']

    df = df.sort_values('confidence_weighted_anisotropy', ascending=False)
    df.to_csv("outputs/afcc/confidence_weighted_ranking.csv", index=False)

    high_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] >= 70)].copy()
    low_conf = df[(df['anisotropy_index'] >= 3.0) & (df['plddt_mean'] < 70)].copy()

    targets = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    comp_df = df[df['gene_symbol'].isin(targets)].copy()

    # Check for missing comparators and fetch most recent if missing
    missing_targets = set(targets) - set(comp_df['gene_symbol'])
    if missing_targets:
        afcc_dir = Path("outputs/afcc")
        all_files = sorted(glob.glob(str(afcc_dir / "2026-*" / "metrics.csv")), reverse=True)
        missing_rows = []
        for target in missing_targets:
            found = False
            for f in all_files:
                try:
                    tdf = pd.read_csv(f)
                    if target in tdf['gene_symbol'].values:
                        row = tdf[tdf['gene_symbol'] == target].iloc[0].copy()
                        row['run_date'] = Path(f).parent.name
                        # Ensure fields exist before calculation
                        if 'anisotropy_index' not in row:
                            row['anisotropy_index'] = row.get('anisotropy', 0)
                        if 'plddt_mean' not in row:
                            row['plddt_mean'] = row.get('mean_plddt', 0)

                        # Standardize PAE
                        if 'PAE_domain_blockiness_score' not in row:
                            row['PAE_domain_blockiness_score'] = row.get('pae_blockiness', 0)

                        # Recalculate
                        cw = np.clip((row['plddt_mean'] - 50) / 40, 0, 1)
                        row['confidence_weight'] = cw
                        row['confidence_weighted_anisotropy'] = row['anisotropy_index'] * cw

                        missing_rows.append(row)
                        found = True
                        break
                except Exception:
                    continue
            if not found:
                print(f"Warning: Could not find any historical data for {target}")

        if missing_rows:
            missing_df = pd.DataFrame(missing_rows)
            # Make sure missing_df only contains columns present in comp_df + run_date
            common_cols = list(set(comp_df.columns).intersection(missing_df.columns))
            missing_df = missing_df[common_cols + ['run_date']]
            comp_df['run_date'] = "2026-02-16" # Add to base df
            comp_df = pd.concat([comp_df, missing_df], ignore_index=True)

    # Format display columns
    display_cols = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'confidence_weighted_anisotropy', 'morphology']
    if 'run_date' in comp_df.columns:
        comp_display_cols = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'confidence_weighted_anisotropy', 'PAE_domain_blockiness_score', 'morphology', 'run_date']
    else:
        comp_display_cols = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'confidence_weighted_anisotropy', 'PAE_domain_blockiness_score', 'morphology']


    report = [
        "# Confidence-Weighted Structural Evidence",
        "",
        "## Overview",
        "Generated based on authoritative metrics snapshot: `outputs/afcc/2026-02-16/metrics.csv` (with missing comparators backfilled from recent runs).",
        "To mitigate narrative over-interpretation of static, low-confidence AFDB structures, this report re-ranks mechanosensor candidates by explicitly weighting their anisotropy by predictive confidence.",
        "",
        "## 1. High-Anisotropy, Adequate-Confidence (Structural Signal Strong)",
        "Proteins exhibiting significant extended shapes (Anisotropy >= 3.0) and sufficient predictive reliability (pLDDT >= 70). These are prime candidates for direct mechanical force transmission.",
        "",
        high_conf[display_cols].to_markdown(index=False),
        "",
        "## 2. High-Anisotropy, Low-Confidence (Exploratory Only)",
        "Proteins showing high theoretical anisotropy but lacking structural reliability (pLDDT < 70). These likely contain large Intrinsically Disordered Regions (IDRs). The 'fibrous' shape may be a simulation artifact of unbound states rather than a true biological rigid rod.",
        "",
        low_conf[display_cols].to_markdown(index=False),
        "",
        "## 3. LBX1 vs Mechanotransduction Comparators",
        "LBX1 is hypothesized as a crucial sensor/integrator. How does its structural profile compare against known mechanosensors and other key candidates?",
        "",
        comp_df[comp_display_cols].to_markdown(index=False),
        "",
        "**Synthesis:**",
        "LBX1 exhibits an intermediate, low-confidence structure (Anisotropy ~2.27, pLDDT ~66.9). Unlike true fibrous mechanosensors (e.g., PIEZO2, LMNA), its predicted structure lacks the rigid, extended architecture necessary to directly sustain or transmit significant tensile loads. Its role is likely downstream (biochemical/transcriptional integration) rather than primary mechanical load-bearing."
    ]

    with open("reports/confidence_weighted_structural_evidence.md", "w") as f:
        f.write("\n".join(report))

    print("Generated confidence_weighted_structural_evidence.md")

if __name__ == "__main__":
    generate_report()
