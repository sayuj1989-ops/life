#!/usr/bin/env python3
"""
Longevity Protein Analysis

Extends the thermodynamic cost analysis to include longevity proteins.
Maps longevity proteins to the dissipation cascade.
"""

import csv
import os
import sys
from dataclasses import dataclass

sys.path.append(os.getcwd())

from scripts.experiments.experiment_thermodynamic_cost_proteins import (
    OUTPUT_DIR,
    TARGETS,
    load_all_metrics,
)


@dataclass
class LongevityTarget:
    gene: str
    uniprot: str
    term: str
    role: str
    prediction: str
    scaling: str
    dual_role: bool = False
    upstream: str = ""

def run_longevity_analysis():
    print("=" * 70)
    print("  THERMODYNAMIC COST OF COUNTERCURVATURE: Longevity Extension")
    print("=" * 70)

    # Base targets from original file
    base_targets = list(TARGETS)

    # We will extend the targets with new longevity ones, or update existing ones
    new_targets = [
        LongevityTarget(
            gene="FOXO3", uniprot="O43524", term="longevity",
            role="Stress resistance, autophagy",
            prediction="Downstream of η_a (AMPK activation from muscle contraction)",
            scaling="downstream",
            dual_role=False,
            upstream="η_a -> AMPK + Γ_m -> SIRT1"
        ),
        LongevityTarget(
            gene="KLOTHO", uniprot="Q9UEF7", term="longevity",
            role="Anti-oxidant, vascular health",
            prediction="Downstream of η_p (Ca2+ from PIEZO1/2)",
            scaling="downstream",
            dual_role=False,
            upstream="η_p -> PIEZO -> Ca2+"
        ),
        LongevityTarget(
            gene="YAP1", uniprot="P46937", term="longevity",
            role="Tissue repair, proliferation",
            prediction="Direct mechanosensor bridging η_a to nuclear signaling",
            scaling="downstream",
            dual_role=False,
            upstream="η_a -> VIM/LMNA tension"
        )
    ]

    # We also update SIRT1 and PPARGC1A to flag dual_role=True
    all_targets = []
    for t in base_targets:
        dual_role = False
        upstream = ""
        if t.gene == "SIRT1":
            dual_role = True
            upstream = "Γ_m (NAD+ cycling)"
        elif t.gene == "PPARGC1A":
            dual_role = True
            upstream = "Γ_m (AMPK activation)"

        all_targets.append(LongevityTarget(
            gene=t.gene,
            uniprot=t.uniprot,
            term=t.term,
            role=t.role,
            prediction=t.prediction,
            scaling=t.scaling,
            dual_role=dual_role,
            upstream=upstream
        ))

    all_targets.extend(new_targets)

    # Load cached metrics
    metrics = load_all_metrics()
    print(f"\n  Loaded metrics for {len(metrics)} proteins")

    # Save extended CSV
    csv_path = OUTPUT_DIR / "thermodynamic_cost_proteins_extended.csv"
    rows = []
    for t in all_targets:
        # Support case-insensitive lookup
        m = metrics.get(t.gene, metrics.get(t.gene.capitalize(), metrics.get(t.gene.upper(), {})))
        rows.append({
            "gene": t.gene,
            "uniprot": t.uniprot,
            "term": t.term,
            "role": t.role,
            "scaling": t.scaling,
            "dual_role": "True" if t.dual_role else "False",
            "upstream": t.upstream,
            "anisotropy": m.get("anisotropy_index", ""),
            "morphology": m.get("morphology", ""),
            "rg": m.get("radius_of_gyration", ""),
            "plddt_mean": m.get("plddt_mean", ""),
            "n_residues": m.get("n_residues", ""),
            "hinge_candidates": m.get("hinge_candidates", ""),
            "disorder_fraction": m.get("disorder_fraction_proxy", ""),
            "PAE_blockiness": m.get("pae_blockiness", m.get("PAE_domain_blockiness_score", "")),
            "status": "matched" if m else "missing",
        })

    if rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  ✅ CSV: {csv_path}")

if __name__ == "__main__":
    run_longevity_analysis()
