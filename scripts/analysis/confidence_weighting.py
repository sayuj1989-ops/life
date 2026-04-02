import pandas as pd
import numpy as np

def run_ranking():
    # Load authoritative metrics
    df = pd.read_csv('outputs/afcc/2026-02-16/metrics.csv')

    # Define thresholds
    HIGH_CONF_THRESH = 70.0
    HIGH_ANISO_THRESH = 3.0

    # Add confidence and category labels
    df['confidence_tier'] = np.where(df['plddt_mean'] >= HIGH_CONF_THRESH, 'Adequate', 'Low')

    # Categorize
    df['evidence_category'] = 'Other'

    # High anisotropy + adequate confidence
    mask_high_aniso_conf = (df['anisotropy_index'] >= HIGH_ANISO_THRESH) & (df['plddt_mean'] >= HIGH_CONF_THRESH)
    df.loc[mask_high_aniso_conf, 'evidence_category'] = 'High Anisotropy + Adequate Confidence'

    # High anisotropy + low confidence
    mask_high_aniso_low_conf = (df['anisotropy_index'] >= HIGH_ANISO_THRESH) & (df['plddt_mean'] < HIGH_CONF_THRESH)
    df.loc[mask_high_aniso_low_conf, 'evidence_category'] = 'High Anisotropy + Low Confidence'

    # Sort
    df = df.sort_values(['evidence_category', 'anisotropy_index'], ascending=[True, False])

    # Save output
    df.to_csv('outputs/afcc/confidence_weighted_ranking.csv', index=False)

    print(df[['gene_symbol', 'anisotropy_index', 'plddt_mean', 'evidence_category']].head(15))

run_ranking()
