#!/usr/bin/env python3
"""
Thermodynamic Cost of Countercurvature: Extended Longevity Protein Analysis
===========================================================================

Extends the 23-protein thermodynamic cost analysis to include 5 longevity
proteins (FOXO3, Klotho, YAP1, SIRT1_L, PPARGC1A_L).

Output: Extended CSV with all 28 proteins (23 + 3 new + 2 flagged dual-role)

Author: Dr. Sayuj Krishnan S
"""

import csv
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd

# Ensure src is in path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from scripts.experiments.experiment_thermodynamic_cost_proteins import (
    load_all_metrics, TARGETS as BASE_TARGETS, ProteinTarget, generate_report
)

# Also import run_focused_cycle to get metrics if missing
try:
    from research.alphafold_countercurvature.scripts.bolt_focused_cycle import run_focused_cycle
except ImportError:
    pass

OUTPUT_DIR = Path("outputs/thermodynamic_cost")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


LONGEVITY_TARGETS: List[ProteinTarget] = [
    ProteinTarget(
        gene="FOXO3", uniprot="O43524", term="longevity",
        role="Downstream of eta_a (AMPK activation from muscle contraction)",
        prediction="Translates thermodynamic dissipation into longevity maintenance; upregulated by cyclic mechanical loading.",
        scaling="constant"
    ),
    ProteinTarget(
        gene="SIRT1_L", uniprot="Q96EB6", term="longevity",
        role="Dual-role: energy gauge + longevity effector via NAD+ cycling",
        prediction="Couples the metabolic cost of countercurvature directly to cellular lifespan and repair mechanisms.",
        scaling="constant"
    ),
    ProteinTarget(
        gene="Klotho", uniprot="Q9UEF7", term="longevity",
        role="Downstream of eta_p (Ca2+ from PIEZO1/2)",
        prediction="Acts as a systemic anti-aging hormone released in response to proprioceptive feedback dissipation.",
        scaling="constant"
    ),
    ProteinTarget(
        gene="YAP1", uniprot="P46937", term="longevity",
        role="Direct mechanosensor bridging eta_a to nuclear signaling",
        prediction="Mechanotransducer that responds to tension changes during thermodynamic cycling (squat-to-stand).",
        scaling="constant"
    ),
    ProteinTarget(
        gene="PPARGC1A_L", uniprot="Q9UBK2", term="longevity",
        role="Dual-role: mitochondrial supply + exercise-induced biogenesis",
        prediction="Drives mitochondrial biogenesis in response to active moment dissipation (eta_a), increasing energy supply.",
        scaling="constant"
    ),
]

def ensure_metrics(targets):
    """Ensure we have metrics for the longevity targets by using Bolt BioFold if necessary."""
    metrics = load_all_metrics()
    missing_targets = []

    dual_role_map = {"SIRT1_L": "SIRT1", "PPARGC1A_L": "PPARGC1A"}

    for t in targets:
        lookup_gene = dual_role_map.get(t.gene, t.gene)
        if lookup_gene not in metrics:
            missing_targets.append((t.uniprot, lookup_gene))

    if missing_targets:
        print(f"Fetching metrics for {missing_targets} using Bolt-BioFold...")
        # Since run_focused_cycle writes to research/alphafold_countercurvature/data/processed/bolt_biofold_results.csv
        # we can parse it and write out the required metrics.csv files.
        try:
            run_focused_cycle(missing_targets)

            df = pd.read_csv("research/alphafold_countercurvature/data/processed/bolt_biofold_results.csv")
            for _, row in df.iterrows():
                gene = row["protein_id"]
                out_dir = Path(f"outputs/afcc/{gene}")
                out_dir.mkdir(parents=True, exist_ok=True)

                out_dict = {
                    "gene_symbol": row["protein_id"],
                    "anisotropy_index": row["anisotropy_index"],
                    "morphology": "Extended" if row["anisotropy_index"] > 2.0 else "Globular",
                    "radius_of_gyration": row["radius_of_gyration"],
                    "plddt_mean": row["pLDDT_mean"],
                    "n_residues": row["length"],
                    "hinge_candidates": row["hinge_candidates"],
                    "disorder_fraction_proxy": row["disorder_fraction_proxy"],
                    "PAE_domain_blockiness_score": row["PAE_domain_blockiness_score"]
                }
                pd.DataFrame([out_dict]).to_csv(out_dir / "metrics.csv", index=False)

            metrics = load_all_metrics() # reload
        except Exception as e:
            print(f"Failed to fetch missing metrics automatically: {e}")

    return metrics

def main():
    print("=" * 70)
    print("  THERMODYNAMIC COST OF COUNTERCURVATURE: Extended Longevity Analysis")
    print("=" * 70)

    # 28 targets total
    all_targets = BASE_TARGETS + LONGEVITY_TARGETS

    # Check and Fetch metrics
    metrics = ensure_metrics(LONGEVITY_TARGETS)

    print(f"\n  Loaded metrics for {len(metrics)} proteins")

    # Save Extended CSV
    csv_path = OUTPUT_DIR / "thermodynamic_cost_proteins_extended.csv"
    rows = []
    dual_role_map = {"SIRT1_L": "SIRT1", "PPARGC1A_L": "PPARGC1A"}

    for t in all_targets:
        lookup_gene = dual_role_map.get(t.gene, t.gene)
        m = metrics.get(lookup_gene, {})

        dual_role_flag = "True" if t.gene in dual_role_map else "False"

        rows.append({
            "gene": t.gene,
            "uniprot": t.uniprot,
            "term": t.term,
            "role": t.role,
            "scaling": t.scaling,
            "anisotropy": m.get("anisotropy_index", ""),
            "morphology": m.get("morphology", ""),
            "rg": m.get("radius_of_gyration", ""),
            "plddt_mean": m.get("plddt_mean", ""),
            "n_residues": m.get("n_residues", ""),
            "hinge_candidates": m.get("hinge_candidates", ""),
            "disorder_fraction": m.get("disorder_fraction_proxy", ""),
            "PAE_blockiness": m.get("PAE_domain_blockiness_score", ""),
            "status": "matched" if lookup_gene in metrics else "missing",
            "dual_role": dual_role_flag
        })

    if rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  ✅ Extended CSV: {csv_path}")

if __name__ == "__main__":
    main()
