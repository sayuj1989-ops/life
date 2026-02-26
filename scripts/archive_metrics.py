import shutil
import datetime
from pathlib import Path
import os

def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    output_dir = Path(f"outputs/afcc/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)

    source = Path("research/alphafold_countercurvature/data/processed/protein_metrics.csv")
    dest = output_dir / "metrics.csv"

    if source.exists():
        shutil.copy(source, dest)
        print(f"✅ Archived metrics to {dest}")
    else:
        print(f"❌ Source metrics file not found at {source}")
        sys.exit(1)

if __name__ == "__main__":
    main()
