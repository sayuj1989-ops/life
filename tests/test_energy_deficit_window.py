
import os
import sys
import subprocess
import pandas as pd
import pytest

def test_energy_deficit_window_outputs():
    """
    Verify that the energy deficit window experiment produced the expected outputs.
    If outputs are missing, run the simulation script first.
    """
    csv_path = "outputs/thermodynamic_cost/energy_deficit_window.csv"
    png_path = "outputs/figures/energy_deficit_window.png"
    manuscript_png_path = "manuscript/figures/energy_deficit_window.png"
    script_path = "scripts/experiment_energy_deficit_window.py"

    # If outputs don't exist, run the script
    if not os.path.exists(csv_path) or not os.path.exists(png_path):
        print(f"Outputs missing. Running {script_path}...")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"
        print(result.stdout)

    # Check file existence again
    assert os.path.exists(csv_path), f"{csv_path} does not exist"
    assert os.path.exists(png_path), f"{png_path} does not exist"

    # Check manuscript figure existence (this one must be manually copied or handled by pipeline)
    # The test should pass if it exists. If not, maybe warn or fail depending on strictness.
    # Given I copied it manually, it should exist.
    assert os.path.exists(manuscript_png_path), f"{manuscript_png_path} does not exist"

    # Check CSV content
    df = pd.read_csv(csv_path)
    assert not df.empty, "CSV file is empty"
    required_cols = ["L", "P_counter", "S_proprio_alpha05"]
    for col in required_cols:
        assert col in df.columns, f"Column {col} missing in CSV"

    # Check critical logic (L_crit approx 0.35)
    # Find crossover
    deficit_mask = df['P_counter'] > df['S_proprio_alpha05']
    # It should be False for small L and True for large L
    assert not deficit_mask.iloc[0], "Should not be in deficit at small L"
    assert deficit_mask.iloc[-1], "Should be in deficit at large L"

    # Find first index where deficit is True
    crossover_idx = deficit_mask.idxmax()
    L_crit = df.iloc[crossover_idx]['L']

    # Allow some tolerance around 0.35
    assert 0.33 <= L_crit <= 0.37, f"L_crit {L_crit} is out of expected range [0.33, 0.37]"

if __name__ == "__main__":
    test_energy_deficit_window_outputs()
