#!/usr/bin/env python3
"""
Longevity Protein Analysis Extension
====================================

Extends the base thermodynamic cost analysis to include 5 specific longevity proteins
(FOXO3, SIRT1, Klotho, YAP1, PGC-1α) to support the longevity squat-stand study.
It maps the full 28-protein cascade representing the biophysical pathways through which
dynamic structural perturbation is transduced into extended physiological resilience.

Author: Dr. Sayuj Krishnan S
Date: 2026-02-07
"""

import csv
import time
from pathlib import Path
from typing import Any, Dict, List
import numpy as np

OUTPUT_DIR = Path("outputs/thermodynamic_cost")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
METRICS_DIRS = [
    Path("outputs/afcc"),
    Path("research/alphafold_countercurvature/outputs/afcc"),
]

class ProteinTarget:
    def __init__(self, gene: str, uniprot: str, term: str, role: str, prediction: str, scaling: str, dual_role: bool = False):
        self.gene = gene
        self.uniprot = uniprot
        self.term = term
        self.role = role
        self.prediction = prediction
        self.scaling = scaling
        self.dual_role = dual_role

TARGETS = [
    # ===== Original 23 Proteins =====
    ProteinTarget("PIEZO2", "Q9H5I5", "eta_p", "Vector mechanosensor", "High anisotropy", "L"),
    ProteinTarget("EGR3", "Q06889", "eta_p", "Muscle spindle TF", "High disorder", "L"),
    ProteinTarget("RUNX3", "Q13761", "eta_p", "Proprioceptive TF", "High disorder", "L"),
    ProteinTarget("NTRK3", "Q16288", "eta_p", "Survival signal", "Cost scales with L", "L"),
    ProteinTarget("PIEZO1", "Q92508", "eta_p", "Scalar mechanosensor", "Extended", "L^2"),

    ProteinTarget("DMD", "P11532", "eta_a", "ECM linker", "Essential for tone", "L^3"),
    ProteinTarget("MYLK", "Q15746", "eta_a", "Tonic contraction", "Regulator", "L^2"),
    ProteinTarget("LBX1", "P52954", "eta_a", "Paraspinal TF", "Sensitive to stiffness", "L^2"),
    ProteinTarget("FLNA", "P21333", "eta_a", "Crosslinker", "Tension-gated", "L^3"),
    ProteinTarget("VIM", "P08670", "eta_a", "Strain gauge", "Collapses in microgravity", "L^3"),
    ProteinTarget("LMNA", "P02545", "eta_a", "Nuclear mechanostat", "Highest TF anisotropy", "L^2"),
    ProteinTarget("CAV1", "Q03135", "eta_a", "Curvature sensor", "Membrane-embedded", "L^2"),

    ProteinTarget("COL1A1", "P02452", "Gamma_m", "Primary structural", "Turnover cost", "L^3"),
    ProteinTarget("COMP", "P49747", "Gamma_m", "Disc ECM", "Scaffold", "L"),
    ProteinTarget("SIRT1", "Q96EB6", "Gamma_m", "Metabolic sensor", "Fuel gauge", "constant"),
    ProteinTarget("SOX9", "P48436", "Gamma_m", "Chondrogenic TF", "Drives growth", "L"),
    ProteinTarget("SHH", "Q15465", "Gamma_m", "Morphogen", "Gradient maintenance", "L"),
    ProteinTarget("CDKN1A", "P38936", "Gamma_m", "Cell cycle inhibitor", "Unloading signal", "threshold"),
    ProteinTarget("PPARGC1A", "Q9UBK2", "Gamma_m", "Mitochondrial supply", "Supply bottleneck", "L"),
    ProteinTarget("IGF1R", "P08069", "Gamma_m", "Growth factor receptor", "Signaling", "L"),
    ProteinTarget("GHR", "P10912", "Gamma_m", "Growth hormone receptor", "Rate regulator", "L"),
    ProteinTarget("ARNTL", "O00327", "Gamma_m", "Circadian clock", "Rhythm", "L"),

    # ===== Longevity Specific Targets (New + Explicit Dual Roles) =====
    ProteinTarget("FOXO3", "O43524", "longevity", "Stress resistance TF", "Downstream of AMPK/SIRT1", "longevity"),
    ProteinTarget("KLOTHO", "Q9UEF7", "longevity", "Anti-aging hormone", "Downstream of PIEZO2 Ca2+ influx", "longevity"),
    ProteinTarget("YAP1", "P46937", "longevity", "Tissue repair TF", "Nuclear translocation requires cytoskeletal tension", "longevity"),

    ProteinTarget("SIRT1_L", "Q96EB6", "longevity", "FOXO3 deacetylase", "Dual-role: metabolic gauge + longevity effector", "longevity", dual_role=True),
    ProteinTarget("PPARGC1A_L", "Q9UBK2", "longevity", "Mitochondrial biogenesis", "Dual-role: developmental bottleneck + exercise-induced supply", "longevity", dual_role=True),
]

def load_all_metrics() -> Dict[str, Dict[str, Any]]:
    all_proteins = {}
    for metrics_dir in METRICS_DIRS:
        if not metrics_dir.exists():
            continue
        for metrics_file in sorted(metrics_dir.glob("*/metrics.csv")):
            with open(metrics_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    gene = row.get("gene_symbol", "")
                    if gene:
                        all_proteins[gene] = row
    return all_proteins


def main():
    print("=" * 70)
    print("  LONGEVITY PROTEIN EXTENSION: Thermodynamic Cost Analysis")
    print("=" * 70)

    metrics = load_all_metrics()
    print(f"\n  Loaded metrics for {len(metrics)} proteins")

    csv_path = OUTPUT_DIR / "thermodynamic_cost_proteins_extended.csv"
    rows = []

    matched_count = 0
    for t in TARGETS:
        lookup_gene = t.gene.replace("_L", "")
        m = metrics.get(lookup_gene, {})

        if lookup_gene in metrics:
            matched_count += 1

        rows.append({
            "gene": t.gene,
            "uniprot": t.uniprot,
            "term": t.term,
            "role": t.role,
            "scaling": t.scaling,
            "dual_role": "True" if t.dual_role else "False",
            "anisotropy": m.get("anisotropy_index", ""),
            "morphology": m.get("morphology", ""),
            "rg": m.get("radius_of_gyration", ""),
            "plddt_mean": m.get("plddt_mean", ""),
            "n_residues": m.get("n_residues", ""),
            "hinge_candidates": m.get("hinge_candidates", ""),
            "disorder_fraction": m.get("disorder_fraction_proxy", m.get("disorder_fraction", "")),
            "PAE_blockiness": m.get("pae_blockiness", m.get("PAE_domain_blockiness_score", "")),
            "status": "matched" if lookup_gene in metrics else "missing",
        })

    print(f"\n  Matched: {matched_count}/{len(TARGETS)} targets")

    if rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  ✅ Extended CSV written to: {csv_path}")

if __name__ == "__main__":
    main()
