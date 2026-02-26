import pandas as pd
import os

def generate_confidence_ranking(input_path="outputs/afcc/2026-02-16/metrics.csv", output_path="outputs/afcc/confidence_weighted_ranking.csv"):
    """
    Generates a confidence-weighted ranking of structural candidates.
    """

    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return

    df = pd.read_csv(input_path)

    # Normalize column names just in case
    df.columns = [c.lower() for c in df.columns]

    # Map essential columns
    col_map = {
        'anisotropy': 'anisotropy_index',
        'mean_plddt': 'plddt_mean',
        'pae_blockiness': 'pae_domain_blockiness_score'
    }
    df.rename(columns=col_map, inplace=True)

    required = ['gene_symbol', 'anisotropy_index', 'plddt_mean', 'pae_domain_blockiness_score']
    missing = [c for c in required if c not in df.columns]

    if missing:
        # Fallback for identity column
        if 'identity' in df.columns and 'gene_symbol' not in df.columns:
             df['gene_symbol'] = df['identity'].apply(lambda x: x.split(' ')[0] if '(' in str(x) else str(x))
        elif 'gene_symbol' not in df.columns:
            print(f"Error: Missing columns {missing} and no identity column found.")
            return

    # Calculate weighted metrics
    # Weighted Anisotropy: We value anisotropy more if the structure is confident.
    # Formula: Anisotropy * (pLDDT / 100)
    # We penalize low confidence heavily.

    df['weighted_anisotropy'] = df['anisotropy_index'] * (df['plddt_mean'] / 100.0)

    # Define Confidence Tiers
    def get_tier(plddt):
        if plddt >= 80: return "High"
        if plddt >= 70: return "Medium"
        return "Low"

    df['confidence_tier'] = df['plddt_mean'].apply(get_tier)

    # Sort by weighted anisotropy descending
    df_sorted = df.sort_values('weighted_anisotropy', ascending=False)

    # Select output columns
    out_cols = [
        'gene_symbol',
        'weighted_anisotropy',
        'anisotropy_index',
        'plddt_mean',
        'confidence_tier',
        'pae_domain_blockiness_score',
        'morphology'
    ]

    # Handle optional morphology column
    if 'morphology' not in df.columns:
        out_cols.remove('morphology')

    final_df = df_sorted[out_cols]

    # Save
    final_df.to_csv(output_path, index=False)
    print(f"Ranking saved to {output_path}")

    # Print top 5 for verification
    print("\nTop 5 Confidence-Weighted Candidates:")
    print(final_df.head(5).to_markdown(index=False))

if __name__ == "__main__":
    generate_confidence_ranking()
