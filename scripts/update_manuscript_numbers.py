"""
Update Manuscript Numbers
Extracts quantitative results from analysis and saves them for LaTeX import
"""

import argparse
import json
import numpy as np
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stats", required=True, help="Path to stats summary JSON")
    parser.add_argument("--out", required=True, help="Output JSON file for manuscript")
    args = parser.parse_args()

    stats_path = Path(args.stats)
    out_path = Path(args.out)

    if not stats_path.exists():
        print(f"❌ Stats file not found: {stats_path}")
        return

    with open(stats_path, 'r') as f:
        data = json.load(f)

    # Extract key numbers
    # data is a list of protein results

    n_proteins = len(data)
    mean_curvature = np.mean([d['mean_curvature'] for d in data])
    mean_entropy = np.mean([d['seq_entropy'] for d in data])

    # Calculate correlation
    entropies = [d['seq_entropy'] for d in data]
    curvatures = [d['mean_curvature'] for d in data]
    correlation = np.corrcoef(entropies, curvatures)[0, 1]

    numbers = {
        "n_proteins": n_proteins,
        "mean_curvature": round(mean_curvature, 4),
        "mean_entropy": round(mean_entropy, 3),
        "entropy_curvature_correlation": round(correlation, 3)
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(numbers, f, indent=2)

    print(f"✅ Manuscript numbers updated: {out_path}")
    print(json.dumps(numbers, indent=2))

if __name__ == "__main__":
    main()
