#!/usr/bin/env python3
"""
WP4 Independent Reconfirmation: Demand-Supply Structural Anisotropy Gap
========================================================================
Fetches 31 AlphaFold structures, computes gyration-tensor anisotropy,
and tests whether DEMAND proteins are more anisotropic than SUPPLY proteins.

Author: Independent reconfirmation agent
"""

import json
import io
import sys
import time
import numpy as np
from scipy import stats
import requests

# ── Protein lists ──────────────────────────────────────────────────────
DEMAND = {
    "PIEZO2": "Q9H5I5", "LBX1": "P52951", "DSTYK": "Q6XUX3",
    "EGR3": "Q06889", "RUNX3": "Q13761", "ASIC3": "Q9UHC3",
    "KCNK2": "O95069", "TMC1": "Q8TDI8", "PAX1": "P15858",
    "VIM": "P08670", "LMNA": "P02545", "CAV1": "Q03135",
    "PIEZO1": "Q92508", "ADGRG6": "Q86SQ4", "FBN2": "P35556",
    "PTK7": "Q13308", "TRPV4": "Q9HBA0", "DPYSL4": "O14531",
    "SCUBE3": "Q8IX30",
}

SUPPLY = {
    "GHR": "P10912", "IGF1R": "P08069", "PPARGC1A": "Q9UBK2",
    "ARNTL": "O00327", "SIRT1": "Q96EB6", "SOX9": "P48436",
    "SHH": "Q15465", "CDKN1A": "P38936", "COMP": "P49747",
    "COL1A1": "P02452", "PLOD1": "Q02809", "BNC2": "Q6ZN30",
}

AF_API = "https://alphafold.ebi.ac.uk/api/prediction/{uid}"

# ── Helper functions ───────────────────────────────────────────────────

def fetch_pdb_url(uniprot_id: str) -> str:
    """Query AlphaFold API to get the PDB download URL."""
    url = AF_API.format(uid=uniprot_id)
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                data = r.json()
                # API returns a list; take first entry
                if isinstance(data, list):
                    data = data[0]
                return data["pdbUrl"]
            elif r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            else:
                print(f"  WARNING: API returned {r.status_code} for {uniprot_id}")
                return None
        except Exception as e:
            print(f"  WARNING: request error for {uniprot_id}: {e}")
            time.sleep(2 ** attempt)
    return None


def download_pdb(pdb_url: str) -> str:
    """Download PDB text from the given URL."""
    for attempt in range(4):
        try:
            r = requests.get(pdb_url, timeout=60)
            if r.status_code == 200:
                return r.text
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"  WARNING: download error: {e}")
            time.sleep(2 ** attempt)
    return None


def parse_ca_coords(pdb_text: str) -> np.ndarray:
    """Extract Cα atom coordinates from PDB text."""
    coords = []
    for line in pdb_text.splitlines():
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            coords.append([x, y, z])
    return np.array(coords)


def compute_anisotropy(coords: np.ndarray) -> dict:
    """
    Compute gyration tensor eigenvalues and anisotropy ratio.
    G_jk = (1/N) sum_i (r_i - r_bar)_j * (r_i - r_bar)_k
    Anisotropy = sqrt(lambda_1 / lambda_3)  where lambda_1 >= lambda_2 >= lambda_3
    """
    N = coords.shape[0]
    centroid = coords.mean(axis=0)
    delta = coords - centroid  # (N, 3)
    G = (delta.T @ delta) / N  # (3, 3) gyration tensor
    eigvals = np.linalg.eigvalsh(G)  # sorted ascending
    lam1, lam2, lam3 = eigvals[2], eigvals[1], eigvals[0]  # descending
    anisotropy = np.sqrt(lam1 / lam3) if lam3 > 0 else np.inf
    return {
        "n_ca": N,
        "lam1": lam1, "lam2": lam2, "lam3": lam3,
        "anisotropy": anisotropy,
        "Rg": np.sqrt(eigvals.sum()),
    }


def cohens_d(group1, group2):
    """Cohen's d with pooled standard deviation."""
    n1, n2 = len(group1), len(group2)
    m1, m2 = np.mean(group1), np.mean(group2)
    s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
    sp = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    return (m1 - m2) / sp if sp > 0 else 0.0


def cliffs_delta(group1, group2):
    """Cliff's delta: non-parametric effect size."""
    n1, n2 = len(group1), len(group2)
    count = 0
    for x in group1:
        for y in group2:
            if x > y:
                count += 1
            elif x < y:
                count -= 1
    return count / (n1 * n2)


# ── Main pipeline ──────────────────────────────────────────────────────

def process_group(name_to_uid: dict, group_label: str) -> list:
    results = []
    for gene, uid in name_to_uid.items():
        print(f"  [{group_label}] {gene} ({uid})...", end=" ", flush=True)
        pdb_url = fetch_pdb_url(uid)
        if pdb_url is None:
            print("SKIPPED (no PDB URL)")
            continue
        pdb_text = download_pdb(pdb_url)
        if pdb_text is None:
            print("SKIPPED (download failed)")
            continue
        coords = parse_ca_coords(pdb_text)
        if len(coords) < 10:
            print(f"SKIPPED (only {len(coords)} Cα atoms)")
            continue
        metrics = compute_anisotropy(coords)
        metrics["gene"] = gene
        metrics["uniprot"] = uid
        metrics["group"] = group_label
        results.append(metrics)
        print(f"Cα={metrics['n_ca']}, aniso={metrics['anisotropy']:.3f}")
    return results


def main():
    print("=" * 70)
    print("WP4 INDEPENDENT RECONFIRMATION — Structural Anisotropy Analysis")
    print("=" * 70)

    print("\n── Fetching DEMAND proteins (n=19) ──")
    demand_results = process_group(DEMAND, "DEMAND")

    print("\n── Fetching SUPPLY proteins (n=12) ──")
    supply_results = process_group(SUPPLY, "SUPPLY")

    all_results = demand_results + supply_results
    if not all_results:
        print("ERROR: No proteins processed successfully!")
        sys.exit(1)

    # Sort by anisotropy descending
    all_results.sort(key=lambda x: -x["anisotropy"])

    # Extract anisotropy arrays
    demand_aniso = np.array([r["anisotropy"] for r in demand_results])
    supply_aniso = np.array([r["anisotropy"] for r in supply_results])

    # ── Statistics ──
    U_stat, p_value = stats.mannwhitneyu(demand_aniso, supply_aniso, alternative="greater")
    d = cohens_d(demand_aniso, supply_aniso)
    cliff = cliffs_delta(demand_aniso, supply_aniso)

    demand_median = np.median(demand_aniso)
    supply_median = np.median(supply_aniso)
    gap_pct = ((demand_median - supply_median) / supply_median) * 100

    # ── Print results ──
    print("\n" + "=" * 70)
    print("RESULTS TABLE — Sorted by Anisotropy (descending)")
    print("=" * 70)
    header = f"{'Rank':<5} {'Gene':<12} {'UniProt':<10} {'Group':<8} {'Cα':<6} {'λ1':<12} {'λ2':<12} {'λ3':<12} {'Aniso':<8} {'Rg(Å)':<8}"
    print(header)
    print("-" * len(header))
    for i, r in enumerate(all_results, 1):
        print(f"{i:<5} {r['gene']:<12} {r['uniprot']:<10} {r['group']:<8} "
              f"{r['n_ca']:<6} {r['lam1']:<12.2f} {r['lam2']:<12.2f} {r['lam3']:<12.2f} "
              f"{r['anisotropy']:<8.3f} {r['Rg']:<8.2f}")

    print("\n" + "=" * 70)
    print("GROUP SUMMARIES")
    print("=" * 70)
    print(f"  DEMAND (n={len(demand_aniso)}): mean={np.mean(demand_aniso):.3f}, "
          f"median={demand_median:.3f}, SD={np.std(demand_aniso, ddof=1):.3f}")
    print(f"  SUPPLY (n={len(supply_aniso)}): mean={np.mean(supply_aniso):.3f}, "
          f"median={supply_median:.3f}, SD={np.std(supply_aniso, ddof=1):.3f}")
    print(f"  Median gap: {gap_pct:+.1f}%")

    print("\n" + "=" * 70)
    print("STATISTICAL TESTS")
    print("=" * 70)
    print(f"  Mann-Whitney U statistic: {U_stat:.1f}")
    print(f"  p-value (one-sided, greater): {p_value:.6f}")
    print(f"  Cohen's d (pooled SD):        {d:.3f}")
    print(f"  Cliff's delta:                {cliff:.3f}")
    bonferroni_threshold = 0.0167
    print(f"  Bonferroni threshold:         {bonferroni_threshold}")

    print("\n" + "=" * 70)
    verdict_pass = p_value < bonferroni_threshold
    if verdict_pass:
        verdict = (f"✅ CONFIRMED: Demand-Supply anisotropy gap SURVIVES Bonferroni correction.\n"
                   f"   p = {p_value:.6f} < {bonferroni_threshold}")
    else:
        verdict = (f"❌ NOT CONFIRMED: Demand-Supply anisotropy gap does NOT survive Bonferroni.\n"
                   f"   p = {p_value:.6f} >= {bonferroni_threshold}")
    print("VERDICT:", verdict)
    print("=" * 70)

    # ── Check against expected values ──
    print("\n── Discrepancy check vs. expected values ──")
    exp_gap, exp_p, exp_d = 70.0, 0.002, 1.1
    gap_disc = abs(gap_pct - exp_gap)
    d_disc = abs(d - exp_d)
    print(f"  Gap:     computed={gap_pct:.1f}%, expected~{exp_gap}%, Δ={gap_disc:.1f}pp "
          f"{'⚠️  >5%' if gap_disc > 5 else '✓'}")
    print(f"  Cohen d: computed={d:.3f}, expected~{exp_d}, Δ={d_disc:.3f} "
          f"{'⚠️  >5% relative' if d_disc/exp_d > 0.05 else '✓'}")
    p_order_match = (p_value < 0.01) == (exp_p < 0.01)
    print(f"  p-value: computed={p_value:.6f}, expected~{exp_p}, same order? {p_order_match} "
          f"{'✓' if p_order_match else '⚠️'}")

    # ── Write Markdown report ──
    md_path = "/workspace/life/research/managed_agent/wp4_reconfirmation_results.md"
    with open(md_path, "w") as f:
        f.write("# WP4 Independent Reconfirmation: Demand-Supply Structural Anisotropy Gap\n\n")
        f.write("## Method\n\n")
        f.write("1. Fetched AlphaFold-predicted structures for 31 proteins via the AlphaFold EBI API.\n")
        f.write("2. Parsed Cα coordinates from each PDB file.\n")
        f.write("3. Computed the gyration tensor: G_jk = (1/N) Σ_i (r_i - r̄)_j (r_i - r̄)_k\n")
        f.write("4. Extracted eigenvalues λ₁ ≥ λ₂ ≥ λ₃ and computed anisotropy = √(λ₁/λ₃).\n")
        f.write("5. Ran one-sided Mann-Whitney U test (DEMAND > SUPPLY).\n")
        f.write("6. Computed Cohen's d (pooled SD) and Cliff's delta effect sizes.\n\n")

        f.write("## Protein Table (sorted by anisotropy, descending)\n\n")
        f.write("| Rank | Gene | UniProt | Group | Cα | λ₁ | λ₂ | λ₃ | Anisotropy | Rg (Å) |\n")
        f.write("|------|------|---------|-------|----|-----|-----|-----|------------|--------|\n")
        for i, r in enumerate(all_results, 1):
            f.write(f"| {i} | {r['gene']} | {r['uniprot']} | {r['group']} | "
                    f"{r['n_ca']} | {r['lam1']:.1f} | {r['lam2']:.1f} | {r['lam3']:.1f} | "
                    f"{r['anisotropy']:.3f} | {r['Rg']:.1f} |\n")

        f.write("\n## Group Summaries\n\n")
        f.write(f"| Group | n | Mean Aniso | Median Aniso | SD |\n")
        f.write(f"|-------|---|-----------|-------------|----|\n")
        f.write(f"| DEMAND | {len(demand_aniso)} | {np.mean(demand_aniso):.3f} | "
                f"{demand_median:.3f} | {np.std(demand_aniso, ddof=1):.3f} |\n")
        f.write(f"| SUPPLY | {len(supply_aniso)} | {np.mean(supply_aniso):.3f} | "
                f"{supply_median:.3f} | {np.std(supply_aniso, ddof=1):.3f} |\n")
        f.write(f"\n**Median gap: {gap_pct:+.1f}%**\n\n")

        f.write("## Statistical Tests\n\n")
        f.write(f"| Test | Value |\n")
        f.write(f"|------|-------|\n")
        f.write(f"| Mann-Whitney U | {U_stat:.1f} |\n")
        f.write(f"| p-value (one-sided) | {p_value:.6f} |\n")
        f.write(f"| Cohen's d | {d:.3f} |\n")
        f.write(f"| Cliff's delta | {cliff:.3f} |\n")
        f.write(f"| Bonferroni threshold | {bonferroni_threshold} |\n")

        f.write(f"\n## Verdict\n\n")
        f.write(f"{verdict}\n\n")

        f.write("## Discrepancy Check vs. Expected Values\n\n")
        f.write(f"| Metric | Computed | Expected | Δ | Status |\n")
        f.write(f"|--------|----------|----------|---|--------|\n")
        f.write(f"| Median gap | {gap_pct:.1f}% | ~70% | {gap_disc:.1f}pp | "
                f"{'⚠️ >5pp' if gap_disc > 5 else '✓ OK'} |\n")
        f.write(f"| Cohen's d | {d:.3f} | ~1.1 | {d_disc:.3f} | "
                f"{'⚠️ >5% relative' if d_disc/exp_d > 0.05 else '✓ OK'} |\n")
        f.write(f"| p-value | {p_value:.6f} | ~0.002 | — | "
                f"{'✓ same order' if p_order_match else '⚠️ different order'} |\n")

        f.write(f"\n---\n*Generated by wp4_reconfirm_scratch.py — independent reconfirmation*\n")

    print(f"\n✅ Report saved to {md_path}")


if __name__ == "__main__":
    main()
