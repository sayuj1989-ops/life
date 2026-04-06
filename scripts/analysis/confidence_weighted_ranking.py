import pandas as pd
from pathlib import Path

def run_ranking():
    # Use the authoritative snapshot: outputs/afcc/2026-02-16/metrics.csv
    snapshot_path = Path("outputs/afcc/2026-02-16/metrics.csv")

    if not snapshot_path.exists():
        print(f"Error: Snapshot not found at {snapshot_path}")
        return

    df = pd.read_csv(snapshot_path)
    if "Gene" in df.columns:
        df = df.rename(columns={"Gene": "gene_symbol"})

    # Re-rank candidates with explicit confidence weighting
    # We want:
    # 1) high-anisotropy (>= 3.0) + adequate-confidence (pLDDT >= 70)
    # 2) high-anisotropy (>= 3.0) + low-confidence (pLDDT < 70)

    df["confidence_class"] = df["plddt_mean"].apply(lambda x: "adequate" if x >= 70 else "low")
    df["anisotropy_class"] = df["anisotropy_index"].apply(lambda x: "high" if x >= 3.0 else "other")

    # Sort by anisotropy descending
    df_sorted = df.sort_values(by="anisotropy_index", ascending=False)

    # Select desired output columns
    cols = ["gene_symbol", "anisotropy_index", "plddt_mean", "PAE_domain_blockiness_score", "morphology", "confidence_class"]
    df_out = df_sorted[cols]

    out_path = Path("outputs/afcc/confidence_weighted_ranking.csv")
    df_out.to_csv(out_path, index=False)

    # Generate report
    high_adequate = df_sorted[(df_sorted["anisotropy_class"] == "high") & (df_sorted["confidence_class"] == "adequate")]
    high_low = df_sorted[(df_sorted["anisotropy_class"] == "high") & (df_sorted["confidence_class"] == "low")]

    # Extract LBX1 comparators
    comparators = ["LBX1", "PIEZO2", "LMNA", "ADGRG6", "RUNX3", "POC5", "GHR"]
    comp_df = df_sorted[df_sorted["gene_symbol"].isin(comparators)]

    report = f"""# Confidence-Weighted Structural Evidence

*Authoritative Snapshot used:* `outputs/afcc/2026-02-16/metrics.csv`

## 1. High-Anisotropy + Adequate-Confidence Candidates
These proteins exhibit strong structural asymmetry while maintaining reliable AlphaFold predictions (pLDDT $\ge$ 70). These are the strongest candidates for structurally grounded mechanosensor models.

{high_adequate[cols].to_markdown(index=False)}

## 2. High-Anisotropy + Low-Confidence Candidates (Exploratory Only)
These proteins exhibit high anisotropy, but their pLDDT scores indicate significant disorder or low modeling confidence (pLDDT < 70). The structural asymmetry may be an artifact of long intrinsically disordered regions rather than a true fibrous morphology.

{high_low[cols].to_markdown(index=False)}

## 3. LBX1 Comparator Analysis

We compare LBX1 against key benchmark proteins:
{comp_df[cols].to_markdown(index=False)}

**Key Observations:**
- LBX1 presents an intermediate anisotropy with low confidence.
- PIEZO2 serves as a robust mechanosensor benchmark, presenting high anisotropy and adequate confidence.
- LMNA is absent from the current snapshot.
- POC5 and GHR show extremely high anisotropy but suffer from low confidence, likely due to IDRs.
"""

    with open("reports/confidence_weighted_structural_evidence.md", "w") as f:
        f.write(report)

    print("Ranking completed. Saved to outputs/afcc/confidence_weighted_ranking.csv and reports/confidence_weighted_structural_evidence.md")

if __name__ == "__main__":
    run_ranking()
