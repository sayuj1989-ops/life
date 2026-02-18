import pandas as pd
import numpy as np
from pathlib import Path

# Input and Output paths
input_path = Path("outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv")
output_path = Path("outputs/thermodynamic_cost/phase_diagram_downsampled.csv")

# Read Data
if not input_path.exists():
    raise FileNotFoundError(f"Input file not found: {input_path}")

df = pd.read_csv(input_path)

# Filter for 3 distinct chi_kappa values (Low, Medium, High)
# The script generated 20 values between 0.01 and 0.10.
# We'll pick indices 0, 10, and 19 (approx 0.01, 0.05, 0.10).

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
# 3 curves * 10 steps = 30 rows.
df_filtered = df_filtered.iloc[::2]

# Keep only relevant columns
columns_to_keep = ["chi_kappa", "L", "R_deficit", "Cobb_angle"]
df_filtered = df_filtered[columns_to_keep]

# Save
df_filtered.to_csv(output_path, index=False)
print(f"Saved downsampled data to {output_path}")
print(f"Original rows: {len(df)}, Filtered rows: {len(df_filtered)}")
