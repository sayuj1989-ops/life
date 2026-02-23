
import os
import sys
import subprocess
import pandas as pd
import pytest

def test_energy_deficit_window_outputs():
    """
    Verify that the updated energy deficit window experiment produced the expected outputs.
    Checks for the new file format (v2) with Demand_IntegratedMoment and Supply_L2.
    """
    csv_path = "outputs/thermodynamic_cost/energy_deficit_window_v2.csv"
    png_path = "outputs/figures/energy_deficit_window.png"
    script_path = "scripts/experiment_energy_deficit_window.py"

    # If outputs don't exist, run the script
    if not os.path.exists(csv_path) or not os.path.exists(png_path):
        print(f"Outputs missing. Running {script_path}...")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Script failed with error:\n{result.stderr}")
            assert False, "Script execution failed"
        print(result.stdout)

    # Check file existence again
    assert os.path.exists(csv_path), f"{csv_path} does not exist"
    assert os.path.exists(png_path), f"{png_path} does not exist"

    # Check CSV content
    df = pd.read_csv(csv_path)
    assert not df.empty, "CSV file is empty"

    # Updated column names for v2
    required_cols = ["L", "Demand_IntegratedMoment", "Supply_L2"]
    for col in required_cols:
        assert col in df.columns, f"Column {col} missing in CSV. Available: {df.columns}"

    # Check critical logic (L_crit approx 0.35)
    # Find crossover: Demand > Supply
    deficit_mask = df['Demand_IntegratedMoment'] > df['Supply_L2']

    # It should be False for small L and True for large L
    # Check L=0.25 (should be safe)
    safe_idx = df['L'].searchsorted(0.26) # Approx index
    if safe_idx < len(df):
        assert not deficit_mask.iloc[safe_idx], "Should not be in deficit at small L (0.25m)"

    # Check L=0.45 (should be in deficit)
    danger_idx = df['L'].searchsorted(0.44)
    if danger_idx < len(df):
        assert deficit_mask.iloc[danger_idx], "Should be in deficit at large L (0.45m)"

    # Find first index where deficit is True
    # If the mask starts with False and becomes True
    if deficit_mask.any():
        crossover_idx = deficit_mask.idxmax()
        L_crit = df.iloc[crossover_idx]['L']

        # Allow some tolerance around 0.35
        # The simulation is calibrated to cross at 0.35 exactly
        assert 0.33 <= L_crit <= 0.37, f"L_crit {L_crit} is out of expected range [0.33, 0.37]"
    else:
        assert False, "No deficit crossover found (Demand never exceeds Supply)"

if __name__ == "__main__":
    test_energy_deficit_window_outputs()
