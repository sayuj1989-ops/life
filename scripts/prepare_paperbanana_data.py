import pandas as pd
import numpy as np
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Prepare simulation data for PaperBanana plotting.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv"),
        help="Path to the raw simulation CSV file."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/thermodynamic_cost/phase_diagram_downsampled.csv"),
        help="Path to save the downsampled CSV file."
    )

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    # Check if input file exists
    if not input_path.exists():
        print(f"Error: Input file not found at {input_path}", file=sys.stderr)
        print("Please run the simulation script first to generate the data:", file=sys.stderr)
        print("  python3 scripts/weekly_sim_energy_deficit_bifurcation.py", file=sys.stderr)
        sys.exit(1)

    # Read Data
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)

    # Filter for 3 distinct chi_kappa values (Low, Medium, High)
    if "chi_kappa" not in df.columns:
        print("Error: Column 'chi_kappa' not found in input CSV.", file=sys.stderr)
        sys.exit(1)

    unique_chis = np.sort(df["chi_kappa"].unique())
    if len(unique_chis) < 3:
        print("Warning: Less than 3 unique chi_kappa values found. Using all.")
        selected_chis = unique_chis
    else:
        # Select min, median-ish, and max
        selected_chis = [unique_chis[0], unique_chis[len(unique_chis)//2], unique_chis[-1]]

    print(f"Selected chi_kappa values: {selected_chis}")

    # Filter DataFrame
    df_filtered = df[df["chi_kappa"].isin(selected_chis)].copy()

    # Further downsample: select every 2nd row to reduce token count for VLM
    # Original simulation has 20 L steps. Taking every 2nd gives 10 steps.
    df_filtered = df_filtered.iloc[::2]

    # Keep only relevant columns
    columns_to_keep = ["chi_kappa", "L", "R_deficit", "Cobb_angle"]
    # Verify columns exist
    missing_cols = [col for col in columns_to_keep if col not in df_filtered.columns]
    if missing_cols:
        print(f"Error: Missing columns in input data: {missing_cols}", file=sys.stderr)
        sys.exit(1)

    df_filtered = df_filtered[columns_to_keep]

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save
    df_filtered.to_csv(output_path, index=False)
    print(f"Saved downsampled data to {output_path}")
    print(f"Original rows: {len(df)}, Filtered rows: {len(df_filtered)}")

if __name__ == "__main__":
    main()
