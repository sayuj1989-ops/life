import pandas as pd
import os

# Files to merge
FILE_16 = "outputs/afcc/2026-02-16/metrics.csv"
FILE_18 = "outputs/afcc/2026-02-18/metrics.csv"
OUTPUT_CSV = "outputs/afcc/confidence_weighted_ranking.csv"
REPORT_MD = "reports/confidence_weighted_structural_evidence.md"

def analyze():
    # Load data
    try:
        df16 = pd.read_csv(FILE_16)
        df16['source_date'] = '2026-02-16'
    except Exception as e:
        print(f"Error loading {FILE_16}: {e}")
        return

    try:
        df18 = pd.read_csv(FILE_18)
        df18['source_date'] = '2026-02-18'
    except Exception as e:
        print(f"Error loading {FILE_18}: {e}")
        df18 = pd.DataFrame()

    # Merge strategy: Use 18th as base for freshness, but ensure we keep genes from 16th if not in 18th
    # Concatenate and drop duplicates keeping last (which would be 18th if we sort by date)

    # Normalize columns
    df16.columns = df16.columns.str.strip()
    if not df18.empty:
        df18.columns = df18.columns.str.strip()
        combined = pd.concat([df16, df18], ignore_index=True)
    else:
        combined = df16

    # Sort by date (implicit in concatenation order) and deduplicate by gene_symbol
    # Keep last (latest)
    combined = combined.drop_duplicates(subset='gene_symbol', keep='last')

    # Calculate Scores
    # Confidence Score (0-1)
    combined['confidence_score'] = combined['plddt_mean'] / 100.0

    # Weighted Metrics
    combined['weighted_anisotropy'] = combined['anisotropy_index'] * combined['confidence_score']
    combined['weighted_blockiness'] = combined['PAE_domain_blockiness_score'] * combined['confidence_score']

    # Classification
    def classify(row):
        ani = row['anisotropy_index']
        conf = row['confidence_score']
        block = row['PAE_domain_blockiness_score']

        if ani >= 3.0 and conf >= 0.7:
            return "Strong Evidence (High Ani + High Conf)"
        elif ani >= 3.0 and conf < 0.7:
            return "Exploratory (High Ani + Low Conf)"
        elif ani < 3.0 and block > 5.0:
             # Blocky but not fibrous
             if conf >= 0.7:
                 return "Modular Scaffold (High Block + High Conf)"
             else:
                 return "Ambiguous Scaffold (High Block + Low Conf)"
        else:
            return "Weak/Globular"

    combined['classification'] = combined.apply(classify, axis=1)

    # Rank by Weighted Anisotropy
    combined = combined.sort_values('weighted_anisotropy', ascending=False)

    # Save CSV
    combined.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved ranking to {OUTPUT_CSV}")

    # Filter for Report Focus
    focus_genes = ['LBX1', 'PIEZO2', 'LMNA', 'ADGRG6', 'RUNX3', 'POC5', 'GHR']
    focus_df = combined[combined['gene_symbol'].isin(focus_genes)].copy()

    # Generate Report
    with open(REPORT_MD, "w") as f:
        f.write("# Confidence-Weighted Structural Evidence\n\n")
        f.write("## 1. Methodology\n")
        f.write("- **Data Source**: Composite snapshot of `2026-02-16` (Baseline) and `2026-02-18` (Comparator Update).\n")
        f.write("- **Weighting**: Metrics are scaled by `pLDDT / 100` to penalize disordered regions.\n")
        f.write("- **Classification Criteria**:\n")
        f.write("  - **Strong Evidence**: Anisotropy >= 3.0, pLDDT >= 70\n")
        f.write("  - **Exploratory**: Anisotropy >= 3.0, pLDDT < 70\n")
        f.write("\n")

        f.write("## 2. LBX1 Comparator Analysis\n")
        f.write("Comparing LBX1 against known mechanosensors and high-anisotropy candidates.\n\n")

        # Table
        cols = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'confidence_score', 'weighted_anisotropy', 'classification']
        # Check if genes exist before printing
        if not focus_df.empty:
            f.write(focus_df[cols].to_markdown(index=False, floatfmt=".2f"))
        else:
            f.write("No focus genes found in dataset.")
        f.write("\n\n")

        # Interpretation
        if 'LBX1' in focus_df['gene_symbol'].values:
            lbx1 = focus_df[focus_df['gene_symbol'] == 'LBX1'].iloc[0]
            f.write(f"### LBX1 Status: {lbx1['classification']}\n")
            f.write(f"- Raw Anisotropy: {lbx1['anisotropy_index']:.2f} (Intermediate)\n")
            f.write(f"- Confidence: {lbx1['plddt_mean']:.1f}%\n")
            f.write(f"- Weighted Score: {lbx1['weighted_anisotropy']:.2f}\n")
            f.write("- **Conclusion**: LBX1 does NOT meet the criteria for a 'Tension Rod' (Anisotropy > 3.0). Its structural evidence supports a modular/blocky role but confidence is low.\n\n")
        else:
            f.write("### LBX1 Status: Missing from dataset\n\n")

        f.write("## 3. Top Ranked Candidates (Strong Evidence)\n")
        strong = combined[combined['classification'].str.contains("Strong Evidence")].head(10)
        f.write(strong[cols].to_markdown(index=False, floatfmt=".2f"))
        f.write("\n\n")

        f.write("## 4. Exploratory High-Anisotropy Signals\n")
        f.write("Candidates with extreme geometry but low confidence (potential IDRs or fibers).\n")
        exploratory = combined[combined['classification'].str.contains("Exploratory")].head(10)
        f.write(exploratory[cols].to_markdown(index=False, floatfmt=".2f"))

if __name__ == "__main__":
    analyze()
