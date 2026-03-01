import pandas as pd
import os

def run():
    print("Running Confidence-Weighted Structural Evidence Ranking...")
    input_file = "outputs/afcc/2026-02-16/metrics.csv"
    output_file = "outputs/afcc/confidence_weighted_ranking.csv"

    if not os.path.exists(input_file):
        print(f"Error: Could not find {input_file}")
        return

    df = pd.read_csv(input_file)

    # Classify confidence
    df['confidence_class'] = df['plddt_mean'].apply(lambda x: 'Adequate' if x >= 70 else 'Low')

    # Classify anisotropy
    df['anisotropy_class'] = df['anisotropy_index'].apply(lambda x: 'High' if x >= 3.0 else 'Intermediate/Low')

    # Sort for ranking: prioritize Adequate confidence, then sort by Anisotropy descending
    df_sorted = df.sort_values(by=['confidence_class', 'anisotropy_index'], ascending=[True, False])

    df_sorted.to_csv(output_file, index=False)
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    run()
