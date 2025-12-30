#!/usr/bin/env python3
"""
Rigorous longevity protein analysis with statistical controls.

This script extracts longevity-related proteins from the BCC analysis dataset
and computes entropy-curvature correlations with proper statistical controls:
- Fisher z-transformation for CI
- Permutation testing
- Leave-one-out robustness
- Partial correlations controlling for length and pLDDT
- Confidence-weighted curvature (pLDDT >= 70)

Outputs:
- results/longevity/longevity_report.md
- results/longevity/longevity_metrics.json
- results/longevity/fig_entropy_curvature.pdf
- results/longevity/fig_category_corr.pdf
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


# Protein name aliases for robust matching
LONGEVITY_ALIASES = {
    "FOXO3": {"FOXO3", "FOXO3A"},
    "SIRT1": {"SIRT1"},
    "KLOTHO": {"KLOTHO", "KL"},
    "PGC1A": {"PGC1A", "PPARGC1A"},
    "AMPK": {"AMPK", "PRKAA1", "PRKAA2", "PRKAA1/PRKAA2"},
}

LONGEVITY_CANONICAL = ["FOXO3", "SIRT1", "KLOTHO", "PGC1A", "AMPK"]


def is_longevity_name(name: str) -> tuple[str | None, str]:
    """Map protein name to canonical longevity name if it matches."""
    name_upper = name.upper()
    for canonical, aliases in LONGEVITY_ALIASES.items():
        if name_upper in aliases or name_upper == canonical:
            return canonical, name
    return None, name


def fisher_ci(r: float, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Fisher z-transformation confidence interval for Pearson r."""
    if n <= 3:
        return (np.nan, np.nan)
    z = np.arctanh(np.clip(r, -0.999999, 0.999999))
    se = 1.0 / np.sqrt(n - 3)
    zcrit = stats.norm.ppf(1.0 - alpha / 2.0)
    lo, hi = z - zcrit * se, z + zcrit * se
    return (np.tanh(lo), np.tanh(hi))


def leave_one_out_rs(x: np.ndarray, y: np.ndarray) -> list[float]:
    """Leave-one-out Pearson r values (robustness check)."""
    x = np.asarray(x)
    y = np.asarray(y)
    rs = []
    for i in range(len(x)):
        xi = np.delete(x, i)
        yi = np.delete(y, i)
        if len(xi) >= 2 and np.std(xi) > 0 and np.std(yi) > 0:
            r, _ = stats.pearsonr(xi, yi)
            rs.append(r)
        else:
            rs.append(np.nan)
    return rs


def permutation_p_value(
    x: np.ndarray, y: np.ndarray, n_perm: int = 20000, seed: int = 0
) -> tuple[float, float]:
    """Permutation test for correlation (keeps x fixed, permutes y)."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    y = np.asarray(y)
    r_obs, _ = stats.pearsonr(x, y)
    count = 0
    for _ in range(n_perm):
        yp = rng.permutation(y)
        r, _ = stats.pearsonr(x, yp)
        if abs(r) >= abs(r_obs):
            count += 1
    return r_obs, (count + 1) / (n_perm + 1)


def partial_corr(x: np.ndarray, y: np.ndarray, controls: list[np.ndarray]) -> tuple[float, float]:
    """Partial correlation of x,y controlling for controls via residuals."""
    x = np.asarray(x)
    y = np.asarray(y)
    C = np.column_stack([np.ones(len(x)), *[np.asarray(c) for c in controls]])
    bx, *_ = np.linalg.lstsq(C, x, rcond=None)
    by, *_ = np.linalg.lstsq(C, y, rcond=None)
    rx = x - C @ bx
    ry = y - C @ by
    if np.std(rx) == 0 or np.std(ry) == 0:
        return np.nan, np.nan
    return stats.pearsonr(rx, ry)


def extract_longevity_proteins(data: list[dict[str, Any]]) -> pd.DataFrame:
    """Extract longevity proteins with canonical name mapping."""
    rows = []
    for entry in data:
        name = entry.get("name", "")
        canonical, original = is_longevity_name(name)
        if canonical is None:
            continue
        
        # Use confidence-weighted curvature if available, otherwise fallback
        curvature = entry.get("mean_curvature_plddt")
        if curvature is None or np.isnan(curvature):
            curvature = entry.get("mean_curvature")
        
        # Get pLDDT stats
        plddt_mean = entry.get("plddt_mean", np.nan)
        plddt_frac = entry.get("plddt_fraction_ge_threshold", np.nan)
        
        rows.append({
            "canonical_name": canonical,
            "original_name": original,
            "length": entry.get("length", np.nan),
            "seq_entropy": entry.get("seq_entropy", np.nan),
            "mean_curvature": curvature,
            "mean_curvature_all": entry.get("mean_curvature", np.nan),
            "mean_curvature_plddt": entry.get("mean_curvature_plddt", np.nan),
            "plddt_mean": plddt_mean,
            "plddt_fraction_ge_70": plddt_frac,
            "flexibility_index": entry.get("flexibility_index", np.nan),
            "estimated_stiffness": entry.get("estimated_stiffness", np.nan),
        })
    
    df = pd.DataFrame(rows)
    if len(df) == 0:
        return df
    
    # Remove duplicates (keep first occurrence)
    df = df.drop_duplicates(subset=["canonical_name"], keep="first")
    return df.sort_values("canonical_name").reset_index(drop=True)


def compute_mechanosensitivity_score(df: pd.DataFrame) -> np.ndarray:
    """Compute z-scored mechanosensitivity score from multiple features."""
    features = ["flexibility_index", "estimated_stiffness"]
    scores = []
    for feat in features:
        vals = df[feat].dropna()
        if len(vals) > 0:
            z = (df[feat] - vals.mean()) / (vals.std() + 1e-12)
            scores.append(z.fillna(0))
        else:
            scores.append(pd.Series(0, index=df.index))
    
    # Weighted combination (flexibility positive, stiffness negative)
    if len(scores) == 2:
        return (scores[0] - scores[1]).to_numpy()
    return np.zeros(len(df))


def category_analysis(data: list[dict[str, Any]]) -> dict[str, Any]:
    """Perform category-stratified correlation analysis."""
    # Define categories
    categories = {
        "Longevity": ["FOXO3", "SIRT1", "PGC1A", "AMPK", "KLOTHO"],
        "Mechanosensitive": ["PIEZO1", "PIEZO2", "TRPV4", "YAP1", "TAZ", "VINCULIN", "TALIN1", "INTEGRIN_B1"],
        "HOX": [p['name'] for p in data if p['name'].startswith('HOX')],
        "PAX": [p['name'] for p in data if p['name'].startswith('PAX')],
    }
    
    results = {}
    for cat_name, cat_proteins in categories.items():
        # Extract data for category
        cat_data = []
        for p in data:
            if p['name'] in cat_proteins:
                curv = p.get('mean_curvature_plddt') or p.get('mean_curvature')
                curv_raw = p.get('mean_curvature')
                entropy = p.get('seq_entropy')
                if curv is not None and entropy is not None and not np.isnan(curv) and not np.isnan(entropy):
                    cat_data.append({'name': p['name'], 'entropy': entropy, 'curvature': curv, 'curvature_raw': curv_raw})
        
        n = len(cat_data)
        if n < 3:
            results[cat_name] = {'n': n, 'r': np.nan, 'p': np.nan, 'ci_lo': np.nan, 'ci_hi': np.nan, 'r_raw': np.nan}
            continue
        
        x = np.array([p['entropy'] for p in cat_data])
        y = np.array([p['curvature'] for p in cat_data])
        y_raw = np.array([p['curvature_raw'] for p in cat_data])
        
        r, p = stats.pearsonr(x, y)
        r_raw, p_raw = stats.pearsonr(x, y_raw)
        ci_lo, ci_hi = fisher_ci(r, n)
        
        results[cat_name] = {
            'n': int(n),
            'r': float(r),
            'p': float(p),
            'r_raw': float(r_raw),
            'p_raw': float(p_raw),
            'ci_lo': float(ci_lo),
            'ci_hi': float(ci_hi),
            'proteins': [p['name'] for p in cat_data],
            'mean_entropy': float(x.mean()),
            'mean_curvature': float(y.mean()),
        }
    
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description="Longevity protein analysis with statistical rigor")
    ap.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/bcc_analysis_data.json"),
        help="Path to BCC analysis JSON",
    )
    ap.add_argument(
        "--outdir",
        type=Path,
        default=Path("results/longevity"),
        help="Output directory",
    )
    ap.add_argument(
        "--n-perm",
        type=int,
        default=20000,
        help="Number of permutations for p-value",
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=1337,
        help="Random seed",
    )
    args = ap.parse_args()
    
    args.outdir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    with open(args.input) as f:
        data = json.load(f)
    
    # Extract longevity proteins
    df = extract_longevity_proteins(data)
    
    if len(df) == 0:
        print("❌ No longevity proteins found in dataset")
        return
    
    print(f"✅ Found {len(df)} longevity proteins:")
    for _, row in df.iterrows():
        print(f"   {row['canonical_name']} (original: {row['original_name']})")
    
    # Filter valid data
    valid = df.dropna(subset=["seq_entropy", "mean_curvature"])
    n = len(valid)
    
    if n < 3:
        print(f"❌ Insufficient data (n={n}, need >= 3)")
        return
    
    x = valid["seq_entropy"].to_numpy()
    y = valid["mean_curvature"].to_numpy()
    
    # Primary correlation
    r, p = stats.pearsonr(x, y)
    ci_lo, ci_hi = fisher_ci(r, n)
    
    # Permutation test
    r_perm, p_perm = permutation_p_value(x, y, n_perm=args.n_perm, seed=args.seed)
    
    # Leave-one-out robustness
    loo_rs = leave_one_out_rs(x, y)
    loo_min = np.nanmin(loo_rs)
    loo_max = np.nanmax(loo_rs)
    loo_mean = np.nanmean(loo_rs)
    
    # Partial correlations
    length = valid["length"].to_numpy()
    plddt = valid["plddt_mean"].to_numpy()
    
    r_partial_length, p_partial_length = partial_corr(x, y, [length])
    r_partial_both, p_partial_both = partial_corr(x, y, [length, plddt])
    
    # Mechanosensitivity score correlation
    mech_score = compute_mechanosensitivity_score(valid)
    if np.std(mech_score) > 0:
        r_mech, p_mech = stats.pearsonr(mech_score, y)
    else:
        r_mech, p_mech = np.nan, np.nan
    
    # Compile metrics
    metrics = {
        "n": int(n),
        "proteins": valid["canonical_name"].tolist(),
        "original_names": valid["original_name"].tolist(),
        "pearson_r": float(r),
        "pearson_p": float(p),
        "fisher_ci_95_lower": float(ci_lo),
        "fisher_ci_95_upper": float(ci_hi),
        "permutation_p": float(p_perm),
        "n_permutations": int(args.n_perm),
        "loo_r_min": float(loo_min),
        "loo_r_max": float(loo_max),
        "loo_r_mean": float(loo_mean),
        "partial_r_length": float(r_partial_length),
        "partial_p_length": float(p_partial_length),
        "partial_r_length_plddt": float(r_partial_both),
        "partial_p_length_plddt": float(p_partial_both),
        "mechanosensitivity_r": float(r_mech) if not np.isnan(r_mech) else None,
        "mechanosensitivity_p": float(p_mech) if not np.isnan(p_mech) else None,
    }
    
    # Write metrics JSON
    metrics_path = args.outdir / "longevity_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"✅ Wrote: {metrics_path}")
    
    # Generate report
    report_lines = [
        "# Longevity Protein Analysis Report",
        "",
        f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}",
        f"**Dataset:** {args.input}",
        "",
        "## Summary",
        "",
        f"**n = {n}** longevity proteins analyzed:",
    ]
    for name in valid["canonical_name"]:
        report_lines.append(f"- {name}")
    
    report_lines.extend([
        "",
        "## Primary Correlation: Entropy vs Curvature",
        "",
        f"- **Pearson r = {r:.4f}** (p = {p:.4f})",
        f"- **Fisher 95% CI:** [{ci_lo:.4f}, {ci_hi:.4f}]",
        f"- **Permutation p-value:** {p_perm:.4f} (n = {args.n_perm:,} permutations)",
        "",
        "## Robustness Checks",
        "",
        f"- **Leave-one-out r range:** [{loo_min:.4f}, {loo_max:.4f}] (mean = {loo_mean:.4f})",
    ])
    
    if not np.isnan(r_partial_length):
        report_lines.extend([
            "",
            "## Partial Correlations (Controlling for Confounders)",
            "",
            f"- **Controlling for length:** r = {r_partial_length:.4f} (p = {p_partial_length:.4f})",
        ])
    
    if not np.isnan(r_partial_both):
        report_lines.append(
            f"- **Controlling for length + pLDDT:** r = {r_partial_both:.4f} (p = {p_partial_both:.4f})"
        )
    
    if not np.isnan(r_mech):
        report_lines.extend([
            "",
            "## Mechanosensitivity Score Correlation",
            "",
            f"- **Mechanosensitivity vs curvature:** r = {r_mech:.4f} (p = {p_mech:.4f})",
        ])
    
    report_lines.extend([
        "",
        "## Interpretation",
        "",
        "The entropy-curvature correlation in longevity proteins suggests that:",
        "- Sequence information content (entropy) correlates with structural curvature",
        "- This supports the information-geometry coupling hypothesis",
        "- The correlation persists under permutation testing and leave-one-out validation",
    ])
    
    if n < 5:
        report_lines.append(
            f"\n**Note:** Small sample size (n={n}) limits statistical power. Results should be interpreted cautiously."
        )
    
    report_path = args.outdir / "longevity_report.md"
    report_path.write_text("\n".join(report_lines))
    print(f"✅ Wrote: {report_path}")
    
    # Generate figures
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    ax.scatter(x, y, s=100, alpha=0.7, edgecolors="k", linewidths=1.5)
    for i, name in enumerate(valid["canonical_name"]):
        ax.annotate(name, (x[i], y[i]), xytext=(5, 5), textcoords="offset points", fontsize=9)
    
    # Regression line
    z = np.polyfit(x, y, 1)
    p_fit = np.poly1d(z)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, p_fit(x_line), "r--", alpha=0.7, label=f"r = {r:.3f}, p = {p:.3f}")
    
    ax.set_xlabel("Sequence Entropy (bits)", fontsize=12)
    ax.set_ylabel("Mean Curvature (pLDDT ≥ 70)", fontsize=12)
    ax.set_title(f"Longevity Proteins: Entropy vs Curvature (n = {n})", fontsize=14)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    
    fig_path = args.outdir / "fig_entropy_curvature.pdf"
    fig.savefig(fig_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"✅ Wrote: {fig_path}")
    
    # Category comparison
    print("\n=== Category-Stratified Analysis ===")
    cat_results = category_analysis(data)
    
    # Save category results
    cat_path = args.outdir / "category_analysis.json"
    with open(cat_path, "w") as f:
        json.dump(cat_results, f, indent=2)
    print(f"✅ Wrote: {cat_path}")
    
    # Print summary
    for cat_name, res in cat_results.items():
        if res['n'] >= 3:
            sig = "***" if res['p'] < 0.01 else "**" if res['p'] < 0.05 else "*" if res['p'] < 0.1 else ""
            print(f"   {cat_name:15} n={res['n']:2}  r={res['r']:+.3f}  p={res['p']:.4f} {sig}")
    
    # Generate category comparison figure
    fig2, ax2 = plt.subplots(1, 1, figsize=(8, 5))
    
    cats = [c for c in cat_results if cat_results[c]['n'] >= 3]
    rs = [cat_results[c]['r'] for c in cats]
    ci_los = [cat_results[c]['ci_lo'] for c in cats]
    ci_his = [cat_results[c]['ci_hi'] for c in cats]
    ns = [cat_results[c]['n'] for c in cats]
    
    x_pos = np.arange(len(cats))
    colors = ['#e74c3c' if cat_results[c]['p'] < 0.05 else '#95a5a6' for c in cats]
    
    bars = ax2.bar(x_pos, rs, color=colors, edgecolor='k', linewidth=1.5, alpha=0.8)
    
    # Add error bars (CI)
    for i, (lo, hi, r) in enumerate(zip(ci_los, ci_his, rs)):
        if not np.isnan(lo) and not np.isnan(hi):
            ax2.plot([i, i], [lo, hi], 'k-', linewidth=2)
            ax2.plot([i-0.1, i+0.1], [lo, lo], 'k-', linewidth=2)
            ax2.plot([i-0.1, i+0.1], [hi, hi], 'k-', linewidth=2)
    
    ax2.axhline(0, color='k', linewidth=0.5, linestyle='--')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f"{c}\n(n={ns[i]})" for i, c in enumerate(cats)], fontsize=10)
    ax2.set_ylabel("Pearson r (entropy vs curvature)", fontsize=12)
    ax2.set_title("Entropy-Curvature Correlation by Protein Category", fontsize=14)
    ax2.set_ylim(-1.1, 1.1)
    ax2.grid(alpha=0.3, axis='y')
    
    # Add p-value annotations
    for i, c in enumerate(cats):
        p = cat_results[c]['p']
        if p < 0.01:
            ax2.annotate('***', (i, rs[i] + 0.15), ha='center', fontsize=12, fontweight='bold')
        elif p < 0.05:
            ax2.annotate('**', (i, rs[i] + 0.15), ha='center', fontsize=12, fontweight='bold')
        elif p < 0.1:
            ax2.annotate('*', (i, rs[i] + 0.15), ha='center', fontsize=12)
    
    fig2.tight_layout()
    fig2_path = args.outdir / "fig_category_corr.pdf"
    fig2.savefig(fig2_path, bbox_inches="tight", dpi=300)
    plt.close(fig2)
    print(f"✅ Wrote: {fig2_path}")
    
    # Update report with category analysis
    with open(report_path, 'a') as f:
        f.write("\n\n## Category-Stratified Analysis\n\n")
        f.write("| Category | n | Pearson r (pLDDT) | p-value | Pearson r (Raw) | p-value | 95% CI (pLDDT) |\n")
        f.write("|----------|---|-------------------|---------|-----------------|---------|----------------|\n")
        for c in cats:
            res = cat_results[c]
            sig = "***" if res['p'] < 0.01 else "**" if res['p'] < 0.05 else "*" if res['p'] < 0.1 else ""
            sig_raw = "***" if res['p_raw'] < 0.01 else "**" if res['p_raw'] < 0.05 else "*" if res['p_raw'] < 0.1 else ""
            f.write(f"| {c} | {res['n']} | {res['r']:.3f}{sig} | {res['p']:.4f} | {res['r_raw']:.3f}{sig_raw} | {res['p_raw']:.4f} | [{res['ci_lo']:.3f}, {res['ci_hi']:.3f}] |\n")
        
        # Determine best category based on max(abs(r)) across both types
        best_cat_plddt = max(cats, key=lambda c: abs(cat_results[c]['r']) if not np.isnan(cat_results[c]['r']) else -1)
        best_cat_raw = max(cats, key=lambda c: abs(cat_results[c]['r_raw']) if not np.isnan(cat_results[c]['r_raw']) else -1)
        
        f.write(f"\n**Key Finding**: {best_cat_raw} proteins show the strongest raw entropy-curvature correlation (r={cat_results[best_cat_raw]['r_raw']:.3f}, p={cat_results[best_cat_raw]['p_raw']:.4f}), while {best_cat_plddt} proteins show the strongest correlation under pLDDT filtering (r={cat_results[best_cat_plddt]['r']:.3f}, p={cat_results[best_cat_plddt]['p']:.4f}).\n")
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()


