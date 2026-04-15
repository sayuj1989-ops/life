"""
Statistical analysis of the Demand-Supply Anisotropy Gap (WP4).

Tests:
1. Mann-Whitney U test: Demand vs Supply structural anisotropy
2. Fisher's exact test: AIS GWAS loci × high-anisotropy Demand proteins
3. Effect sizes: Cohen's d, rank-biserial correlation, Cliff's delta
4. Multiple comparison correction: Bonferroni

Input: protein_metrics.json from fetch_alphafold_v6.py
Output: statistical_results_v7.json, statistical_report_v7.txt
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

# Use scipy for stats
from scipy import stats


def load_metrics(json_path: str) -> dict:
    """Load protein metrics from JSON."""
    with open(json_path) as f:
        return json.load(f)


def classify_groups(data: dict) -> tuple[dict, dict]:
    """Split proteins into Demand and Supply groups."""
    demand = {k: v for k, v in data.items() if v["category"] == "Demand"}
    supply = {k: v for k, v in data.items() if v["category"] == "Supply"}
    return demand, supply


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Compute Cohen's d effect size (pooled SD)."""
    n1, n2 = len(group1), len(group2)
    s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return (np.mean(group1) - np.mean(group2)) / pooled_sd


def cliffs_delta(group1: np.ndarray, group2: np.ndarray) -> float:
    """Compute Cliff's delta (non-parametric effect size)."""
    n1, n2 = len(group1), len(group2)
    dominance = 0
    for x in group1:
        for y in group2:
            if x > y:
                dominance += 1
            elif x < y:
                dominance -= 1
    return dominance / (n1 * n2)


def rank_biserial_from_u(u_stat: float, n1: int, n2: int) -> float:
    """Compute rank-biserial correlation from Mann-Whitney U statistic."""
    return 1 - (2 * u_stat) / (n1 * n2)


# AIS GWAS loci (from published GWAS: Sharma et al. 2011, Kou et al. 2018,
# Ogura et al. 2015, Zhu et al. 2015, Khanshour et al. 2018)
AIS_GWAS_GENES = {
    "PAX1", "LBX1", "ADGRG6", "BNC2", "SCUBE3", "FBN2",
    "SOX9",   # GWAS-proximal locus
    "SHH",    # 7q36 region GWAS hit
}


def run_analysis(metrics_path: str, output_dir: str):
    """Run full statistical analysis."""
    data = load_metrics(metrics_path)

    demand, supply = classify_groups(data)
    print(f"Loaded {len(data)} proteins: {len(demand)} Demand, {len(supply)} Supply")
    print()

    # ======== 1. Mann-Whitney U Test: Anisotropy ========
    d_anis = np.array([v["anisotropy"] for v in demand.values()])
    s_anis = np.array([v["anisotropy"] for v in supply.values()])

    u_stat, mwu_p = stats.mannwhitneyu(d_anis, s_anis, alternative="greater")
    rbc = rank_biserial_from_u(u_stat, len(d_anis), len(s_anis))
    cd = cohens_d(d_anis, s_anis)
    cliff = cliffs_delta(d_anis, s_anis)

    print("=" * 70)
    print("TEST 1: Mann-Whitney U — Demand vs Supply Anisotropy")
    print("=" * 70)
    print(f"  Demand:  n={len(d_anis)}, mean={np.mean(d_anis):.3f} ± {np.std(d_anis, ddof=1):.3f}")
    print(f"           median={np.median(d_anis):.3f}, range=[{np.min(d_anis):.3f}, {np.max(d_anis):.3f}]")
    print(f"  Supply:  n={len(s_anis)}, mean={np.mean(s_anis):.3f} ± {np.std(s_anis, ddof=1):.3f}")
    print(f"           median={np.median(s_anis):.3f}, range=[{np.min(s_anis):.3f}, {np.max(s_anis):.3f}]")
    print(f"  U-statistic: {u_stat:.1f}")
    print(f"  p-value (one-sided, Demand > Supply): {mwu_p:.6f}")
    print(f"  Effect sizes:")
    print(f"    Cohen's d:            {cd:.3f}  ({'large' if abs(cd)>0.8 else 'medium' if abs(cd)>0.5 else 'small'})")
    print(f"    Rank-biserial corr:   {rbc:.3f}")
    print(f"    Cliff's delta:        {cliff:.3f}  ({'large' if abs(cliff)>0.474 else 'medium' if abs(cliff)>0.33 else 'small'})")
    gap_pct = (np.mean(d_anis) - np.mean(s_anis)) / np.mean(s_anis) * 100
    print(f"  Anisotropy gap: {gap_pct:.1f}%")
    print()

    # ======== 2. Mann-Whitney U Test: Disorder Fraction ========
    d_dis = np.array([v["disorder_fraction"] for v in demand.values()])
    s_dis = np.array([v["disorder_fraction"] for v in supply.values()])

    u_dis, mwu_dis_p = stats.mannwhitneyu(d_dis, s_dis, alternative="less")
    cd_dis = cohens_d(d_dis, s_dis)

    print("=" * 70)
    print("TEST 2: Mann-Whitney U — Demand vs Supply Disorder Fraction")
    print("=" * 70)
    print(f"  Demand disorder:  mean={np.mean(d_dis):.3f} ± {np.std(d_dis, ddof=1):.3f}")
    print(f"  Supply disorder:  mean={np.mean(s_dis):.3f} ± {np.std(s_dis, ddof=1):.3f}")
    print(f"  U-statistic: {u_dis:.1f}")
    print(f"  p-value (one-sided, Demand < Supply): {mwu_dis_p:.6f}")
    print(f"  Cohen's d: {cd_dis:.3f}")
    print()

    # ======== 3. Fisher's Exact Test: GWAS × Anisotropy ========
    median_anis = np.median([v["anisotropy"] for v in data.values()])
    print(f"Median anisotropy threshold: {median_anis:.3f}")

    # 2×2 contingency table:
    # High anisotropy + GWAS | High anisotropy + non-GWAS
    # Low anisotropy + GWAS  | Low anisotropy + non-GWAS
    high_gwas = 0
    high_non_gwas = 0
    low_gwas = 0
    low_non_gwas = 0

    for gene, v in data.items():
        is_gwas = gene in AIS_GWAS_GENES
        is_high = v["anisotropy"] > median_anis
        if is_high and is_gwas:
            high_gwas += 1
        elif is_high and not is_gwas:
            high_non_gwas += 1
        elif not is_high and is_gwas:
            low_gwas += 1
        else:
            low_non_gwas += 1

    table = [[high_gwas, high_non_gwas], [low_gwas, low_non_gwas]]
    odds_ratio, fisher_p = stats.fisher_exact(table, alternative="two-sided")

    print("=" * 70)
    print("TEST 3: Fisher's Exact Test — AIS GWAS loci × High Anisotropy")
    print("=" * 70)
    print(f"  Contingency table:")
    print(f"                    GWAS    non-GWAS")
    print(f"  High anisotropy:   {high_gwas}        {high_non_gwas}")
    print(f"  Low anisotropy:    {low_gwas}        {low_non_gwas}")
    print(f"  Odds ratio: {odds_ratio:.3f}")
    print(f"  p-value (two-sided): {fisher_p:.6f}")
    print(f"  GWAS genes in dataset: {[g for g in data if g in AIS_GWAS_GENES]}")
    print()

    # ======== 4. Bonferroni Correction ========
    n_tests = 3
    bonferroni_threshold = 0.05 / n_tests
    print("=" * 70)
    print(f"BONFERRONI CORRECTION ({n_tests} tests, threshold = {bonferroni_threshold:.4f})")
    print("=" * 70)
    tests = [
        ("Anisotropy (MWU)", mwu_p, mwu_p < bonferroni_threshold),
        ("Disorder (MWU)", mwu_dis_p, mwu_dis_p < bonferroni_threshold),
        ("GWAS×Anisotropy (Fisher)", fisher_p, fisher_p < bonferroni_threshold),
    ]
    for name, p, sig in tests:
        status = "✅ SIGNIFICANT" if sig else "❌ not significant"
        print(f"  {name}: p={p:.6f}  {status}")
    print()

    # ======== 5. Summary Table ========
    print("=" * 70)
    print("FULL PROTEIN TABLE (sorted by anisotropy, descending)")
    print("=" * 70)
    header = f"{'Gene':<12} {'Cat':<8} {'SubCat':<15} {'Len':>5} {'pLDDT':>6} {'Anis':>6} {'Disord':>7} {'GWAS':>5}"
    print(header)
    print("-" * len(header))
    sorted_prots = sorted(data.items(), key=lambda x: x[1]["anisotropy"], reverse=True)
    for gene, v in sorted_prots:
        gwas_flag = "✓" if gene in AIS_GWAS_GENES else ""
        print(f"{gene:<12} {v['category']:<8} {v['subcategory']:<15} {v['seq_length']:>5} "
              f"{v['mean_plddt']:>6.1f} {v['anisotropy']:>6.2f} {v['disorder_fraction']:>6.1%} "
              f"{gwas_flag:>5}")
    print()

    # ======== Save Results ========
    results = {
        "n_total": len(data),
        "n_demand": len(demand),
        "n_supply": len(supply),
        "anisotropy_mwu": {
            "demand_mean": float(np.mean(d_anis)),
            "demand_std": float(np.std(d_anis, ddof=1)),
            "demand_median": float(np.median(d_anis)),
            "supply_mean": float(np.mean(s_anis)),
            "supply_std": float(np.std(s_anis, ddof=1)),
            "supply_median": float(np.median(s_anis)),
            "U_statistic": float(u_stat),
            "p_value_one_sided": float(mwu_p),
            "cohens_d": float(cd),
            "rank_biserial": float(rbc),
            "cliffs_delta": float(cliff),
            "gap_percent": float(gap_pct),
        },
        "disorder_mwu": {
            "demand_mean": float(np.mean(d_dis)),
            "supply_mean": float(np.mean(s_dis)),
            "U_statistic": float(u_dis),
            "p_value_one_sided": float(mwu_dis_p),
            "cohens_d": float(cd_dis),
        },
        "fisher_exact": {
            "contingency_table": table,
            "odds_ratio": float(odds_ratio),
            "p_value_two_sided": float(fisher_p),
            "gwas_genes_found": [g for g in data if g in AIS_GWAS_GENES],
        },
        "bonferroni_threshold": bonferroni_threshold,
        "per_protein": {
            gene: {
                "category": v["category"],
                "subcategory": v["subcategory"],
                "anisotropy": v["anisotropy"],
                "disorder_fraction": v["disorder_fraction"],
                "seq_length": v["seq_length"],
                "mean_plddt": v["mean_plddt"],
                "is_gwas": gene in AIS_GWAS_GENES,
            }
            for gene, v in data.items()
        },
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "statistical_results_v7.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Saved statistical results to {out_path}")

    return results


if __name__ == "__main__":
    # Find metrics file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    # Try expanded data first, fall back to existing
    expanded_path = os.path.join(repo_root, "data", "processed", "alphafold_data", "protein_metrics.json")
    existing_path = os.path.join(script_dir, "protein_metrics.json")

    if os.path.exists(expanded_path):
        metrics_path = expanded_path
        print(f"Using expanded dataset: {metrics_path}")
    elif os.path.exists(existing_path):
        metrics_path = existing_path
        print(f"Using existing dataset: {metrics_path}")
    else:
        print("ERROR: No protein_metrics.json found.")
        sys.exit(1)

    output_dir = os.path.join(repo_root, "data", "processed", "alphafold_data")
    run_analysis(metrics_path, output_dir)
