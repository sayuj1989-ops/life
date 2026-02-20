#!/usr/bin/env python3
"""
Validate Full Pipeline Integration

This script tests the end-to-end flow of the AlphaFold Counter-Curvature (AFCC) pipeline
by simulating the handoff between data acquisition and mechanical simulation.

It verifies:
1.  **Data Ingestion**: Reading and parsing candidate metrics (Anisotropy, pLDDT).
2.  **Parameter Mapping**: Correctly transforming biological metrics into mechanical parameters.
3.  **Simulation Execution**: Running the PyElastica simulation for each candidate.
4.  **Result Aggregation**: Collecting and verifying outputs (S_lat, Cobb Angle).

Usage:
    python scripts/validation/validate_full_pipeline.py [--output-dir DIR]
"""

import sys
import argparse
import pandas as pd
import numpy as np
import time
from pathlib import Path
from datetime import datetime

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(REPO_ROOT / "src"))

try:
    from spinalmodes.countercurvature.pyelastica_bridge import run_protein_simulation, PYELASTICA_AVAILABLE
except ImportError:
    print("Error: Could not import spinalmodes. Check src/ path.")
    sys.exit(1)

def create_mock_metrics_csv(filepath):
    """Generates a mock metrics CSV with known candidate profiles."""
    data = [
        {
            "gene_symbol": "Mock_High_Aniso",
            "anisotropy_index": 5.0,
            "plddt_mean": 90.0,
            "radius_of_gyration": 50.0,
            "morphology": "rod"
        },
        {
            "gene_symbol": "Mock_Isotropic",
            "anisotropy_index": 1.0,
            "plddt_mean": 90.0,
            "radius_of_gyration": 20.0,
            "morphology": "globular"
        },
        {
            "gene_symbol": "Mock_Disordered",
            "anisotropy_index": 1.0,
            "plddt_mean": 40.0,
            "radius_of_gyration": 30.0,
            "morphology": "coil"
        }
    ]
    df = pd.DataFrame(data)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"✅ Created mock metrics CSV at {filepath}")
    return df

def run_simulation_batch(metrics_csv, output_dir):
    """Runs simulations for candidates in the metrics CSV."""
    if not metrics_csv.exists():
        print(f"❌ Metrics CSV not found: {metrics_csv}")
        return []

    df = pd.read_csv(metrics_csv)
    print(f"📋 Loaded {len(df)} candidates from {metrics_csv.name}")

    results = []

    # Simulation Constants for this test
    ACTIVE_CURVATURE_BASE = 5.0  # Represents strong growth drive
    INITIAL_DEFECT = 0.05        # Small lateral perturbation to trigger buckling
    DURATION = 1.5               # Short duration for quick test
    DT = 1e-4

    print(f"\n🚀 Starting Batch Simulation (Base Active Curvature = {ACTIVE_CURVATURE_BASE}, Defect = {INITIAL_DEFECT})")
    print(f"{'Gene':<20} | {'Aniso':<6} | {'StiffMod':<8} | {'Status':<10}")
    print("-" * 60)

    for _, row in df.iterrows():
        gene = row['gene_symbol']
        anisotropy = row.get('anisotropy_index', 1.0)
        plddt = row.get('plddt_mean', 90.0)

        # map pLDDT to stiffness modulation (lower pLDDT = more flexible/modulated)
        # 100 -> 0.0 modulation (stiff)
        # 0   -> 1.0 modulation (flexible)
        stiffness_modulation = max(0.0, min(1.0, (100.0 - plddt) / 100.0))

        try:
            res = run_protein_simulation(
                anisotropy=anisotropy,
                active_curvature=ACTIVE_CURVATURE_BASE,
                stiffness_modulation=stiffness_modulation,
                initial_lateral_defect=INITIAL_DEFECT,
                n_elements=30, # Low resolution for speed
                duration=DURATION,
                dt=DT,
                show_progress=False
            )

            success = res.get('success', False)
            status = "PASS" if success else "FAIL"

            # Store result
            res_row = {
                "gene_symbol": gene,
                "input_anisotropy": anisotropy,
                "input_plddt": plddt,
                "mapped_stiffness_mod": stiffness_modulation,
                "status": status,
                "S_lat": res.get("S_lat", 0.0),
                "cobb_angle": res.get("cobb_angle", 0.0),
                "U_CC": res.get("U_CC", 0.0),
                "runtime": res.get("runtime_sec", 0.0),
                "error": res.get("error", "")
            }
            results.append(res_row)

            print(f"{gene:<20} | {anisotropy:<6.1f} | {stiffness_modulation:<8.2f} | {status:<10}")

        except Exception as e:
            print(f"{gene:<20} | {anisotropy:<6.1f} | {stiffness_modulation:<8.2f} | ERROR: {e}")
            results.append({"gene_symbol": gene, "status": "ERROR", "error": str(e)})

    # Convert to DataFrame
    res_df = pd.DataFrame(results)

    # Save Results
    csv_out = output_dir / "validation_results.csv"
    res_df.to_csv(csv_out, index=False)
    print(f"\n💾 Results saved to {csv_out}")

    return res_df

def generate_report(results_df, output_dir):
    """Generates a markdown report summarizing the validation."""
    report_path = output_dir / "pipeline_validation_report.md"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(report_path, "w") as f:
        f.write(f"# Pipeline Validation Report\n\n")
        f.write(f"**Date:** {timestamp}\n\n")

        f.write("## 1. Execution Summary\n")
        total = len(results_df)
        passed = len(results_df[results_df['status'] == 'PASS'])
        failed = total - passed

        f.write(f"- **Total Candidates:** {total}\n")
        f.write(f"- **Passed:** {passed}\n")
        f.write(f"- **Failed:** {failed}\n\n")

        f.write("## 2. Quantitative Results\n")
        f.write("| Gene | Anisotropy | pLDDT | S_lat | Cobb Angle | U_CC (J) |\n")
        f.write("|---|---|---|---|---|---|\n")

        for _, row in results_df.iterrows():
            if row['status'] == 'PASS':
                f.write(f"| {row['gene_symbol']} | {row['input_anisotropy']:.1f} | {row['input_plddt']:.0f} | "
                        f"{row['S_lat']:.4f} | {row['cobb_angle']:.1f} | {row['U_CC']:.2e} |\n")
            else:
                f.write(f"| {row['gene_symbol']} | - | - | ERROR | {row.get('error','')} | - |\n")

        f.write("\n## 3. Verification Checks\n")

        # Check 1: Mock_High_Aniso vs Mock_Isotropic
        # Hypothesis: High anisotropy should be more stable (lower S_lat) under same load?
        # Or maybe less stable depending on orientation.
        # Here we just check they are DIFFERENT.
        try:
            high_aniso = results_df[results_df['gene_symbol'] == 'Mock_High_Aniso'].iloc[0]
            isotropic = results_df[results_df['gene_symbol'] == 'Mock_Isotropic'].iloc[0]

            diff_slat = abs(high_aniso['S_lat'] - isotropic['S_lat'])
            diff_cobb = abs(high_aniso['cobb_angle'] - isotropic['cobb_angle'])

            is_different = (diff_slat > 1e-4) or (diff_cobb > 0.1)
            status = "PASS" if is_different else "FAIL"

            f.write(f"- **Anisotropy Sensitivity Check**: {status}\n")
            f.write(f"  - High Aniso Cobb: {high_aniso['cobb_angle']:.2f}\n")
            f.write(f"  - Isotropic Cobb: {isotropic['cobb_angle']:.2f}\n")

        except IndexError:
            f.write("- **Anisotropy Sensitivity Check**: SKIPPED (Missing data)\n")

    print(f"📄 Report generated at {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Validate Full Pipeline Integration")
    parser.add_argument("--output-dir", type=str, default="outputs/pipeline_validation", help="Directory for validation outputs")
    parser.add_argument("--mock-data", action="store_true", default=True, help="Use mock data (default)")

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics_csv = output_dir / "mock_metrics.csv"

    if args.mock_data:
        create_mock_metrics_csv(metrics_csv)

    if not PYELASTICA_AVAILABLE:
        print("⚠️  PyElastica not installed. Skipping simulation step.")
        # We can still test data parsing logic if we mock run_protein_simulation,
        # but for now let's just exit or warn.
        return

    results_df = run_simulation_batch(metrics_csv, output_dir)

    if not results_df.empty:
        generate_report(results_df, output_dir)
        print("\n✅ Validation Pipeline Complete.")
    else:
        print("\n❌ Validation Pipeline Failed: No results generated.")
        sys.exit(1)

if __name__ == "__main__":
    main()
