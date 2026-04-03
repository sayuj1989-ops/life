import numpy as np
import pandas as pd
import os

os.makedirs('outputs/figures', exist_ok=True)

def main():
    """
    Validates L_crit = 0.35m against standard growth charts.
    Sitting height (which includes head, neck, and spine) at age 11 is roughly 0.75m.
    Spine length is approximately 45% of sitting height.
    """
    # CDC/WHO approximate sitting height for 50th percentile females
    ages = np.array([8, 9, 10, 11, 12, 13, 14, 15])
    sitting_heights_m = np.array([0.65, 0.68, 0.71, 0.74, 0.78, 0.81, 0.83, 0.84])

    # Spine is ~45% of sitting height
    spine_ratio = 0.45
    spine_lengths = sitting_heights_m * spine_ratio

    # Find age where spine length crosses L_crit = 0.35m
    L_crit = 0.35
    age_interp = np.interp(L_crit, spine_lengths, ages)

    print(f"Predicted Age for L_crit={L_crit}m: {age_interp:.2f} years")

    df = pd.DataFrame({
        'Age_Years': ages,
        'Sitting_Height_m': sitting_heights_m,
        'Estimated_Spine_Length_m': spine_lengths
    })

    # Mark the vulnerability window (L > 0.35)
    df['In_Vulnerability_Window'] = df['Estimated_Spine_Length_m'] >= L_crit

    df.to_csv('outputs/figures/lcrit_validation.csv', index=False)
    print("Saved validation to outputs/figures/lcrit_validation.csv")

if __name__ == "__main__":
    main()
