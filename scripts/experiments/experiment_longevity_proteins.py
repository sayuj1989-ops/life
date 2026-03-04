#!/usr/bin/env python3
"""
Thermodynamic Cost of Countercurvature: Longevity Protein Extension
====================================================================

Extends the 23-protein thermodynamic cost analysis to include 5 longevity proteins:
FOXO3, SIRT1 (dual-role), Klotho, YAP1, PGC-1α (dual-role).

This maps the core dissipation terms (eta_p, eta_a, Gamma_m) to downstream
longevity effector networks, establishing the molecular basis for why
frequent thermodynamic cycling (e.g., squat-to-stand) preserves biological
coupling and promotes healthy aging.

Author: Dr. Sayuj Krishnan S
Date: 2026-02-07
"""

import csv
import time
from pathlib import Path
import os
import sys
from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path("outputs/thermodynamic_cost")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

METRICS_DIRS = [
    Path("outputs/afcc"),
    Path("research/alphafold_countercurvature/outputs/afcc"),
]
from scripts.experiments.experiment_thermodynamic_cost_proteins import (
    OUTPUT_DIR,
    TARGETS,
    load_all_metrics,
)


@dataclass
class ProteinTarget:
    gene: str
    uniprot: str
    term: str           # "eta_p", "eta_a", "Gamma_m", or "longevity"
    role: str
    prediction: str
    scaling: str
    dual_role: bool = False
    upstream: str = ""  # which term activates this longevity protein

# ---------------------------------------------------------------------------
# The 28 Proteins: Core 23 + 5 Longevity
# ---------------------------------------------------------------------------

TARGETS: List[ProteinTarget] = [
    # ===== eta_p: Proprioceptive feedback dissipation =====
    ProteinTarget(
        gene="PIEZO2", uniprot="Q9H5I5", term="eta_p",
        role="Vector mechanosensor for proprioception; detects alignment error",
        prediction="High anisotropy (extended) = high metabolic cost to maintain orientation",
        scaling="L"
    ),
    ProteinTarget(
        gene="EGR3", uniprot="Q06889", term="eta_p",
        role="Transcription factor maintaining muscle spindle innervation",
        prediction="Extended structure despite being a TF; high disorder",
        scaling="L"
    ),
    ProteinTarget(
        gene="RUNX3", uniprot="Q13761", term="eta_p",
        role="Master regulator of proprioceptive neuron development",
        prediction="Intermediate anisotropy, high disorder",
        scaling="L"
    ),
    ProteinTarget(
        gene="NTRK3", uniprot="Q16288", term="eta_p",
        role="TrkC receptor; proprioceptive neuron survival signal",
        prediction="Intermediate anisotropy, conformationally expensive",
        scaling="L"
    ),
    ProteinTarget(
        gene="PIEZO1", uniprot="Q92508", term="eta_p",
        role="Scalar mechanosensor; detects membrane tension",
        prediction="Extended (3.9 aniso), massive (2521 res)",
        scaling="L^2"
    ),

    # ===== eta_a: Active moment maintenance =====
    ProteinTarget(
        gene="DMD", uniprot="P11532", term="eta_a",
        role="Dystrophin; cytoskeleton-ECM linker in paraspinal muscle",
        prediction="Essential for maintenance of muscle tone against gravity",
        scaling="L^3"
    ),
    ProteinTarget(
        gene="MYLK", uniprot="Q15746", term="eta_a",
        role="Myosin light chain kinase; tonic contraction regulator",
        prediction="Regulator of myosin contractility",
        scaling="L^2"
    ),
    ProteinTarget(
        gene="LBX1", uniprot="P52954", term="eta_a",
        role="Paraspinal muscle specification TF",
        prediction="Intermediate anisotropy, high disorder",
        scaling="L^2"
    ),
    ProteinTarget(
        gene="FLNA", uniprot="P21333", term="eta_a",
        role="Filamin A; cytoskeletal mechanosensor and crosslinker",
        prediction="Tension-gated signal integrator",
        scaling="L^3"
    ),
    ProteinTarget(
        gene="VIM", uniprot="P08670", term="eta_a",
        role="Vimentin; gravitational strain gauge in cells",
        prediction="Intermediate filament; collapses in microgravity",
        scaling="L^3"
    ),
    ProteinTarget(
        gene="LMNA", uniprot="P02545", term="eta_a",
        role="Lamin A/C; nuclear mechanostat",
        prediction="Highest anisotropy among TFs",
        scaling="L^2"
    ),
    ProteinTarget(
        gene="CAV1", uniprot="Q03135", term="eta_a",
        role="Caveolin-1; membrane curvature sensor",
        prediction="Membrane-embedded sensor",
        scaling="L^2"
    ),

    # ===== Gamma_m: Basal tissue maintenance =====
    ProteinTarget(
        gene="COL1A1", uniprot="P02452", term="Gamma_m",
        role="Type I collagen; primary structural protein",
        prediction="Triple helix; turnover is largest component of Gamma_m",
        scaling="L^3"
    ),
    ProteinTarget(
        gene="COMP", uniprot="P49747", term="Gamma_m",
        role="Cartilage oligomeric matrix protein",
        prediction="ECM scaffold protein",
        scaling="L"
    ),
    ProteinTarget(
        gene="SIRT1", uniprot="Q96EB6", term="Gamma_m",
        role="Sirtuin 1; NAD+-dependent metabolic sensor",
        prediction="Compact enzyme; energy gauge",
        scaling="constant",
        dual_role=True,
        upstream="Gamma_m (NAD+ cycling)"
    ),
    ProteinTarget(
        gene="SOX9", uniprot="P48436", term="Gamma_m",
        role="Master chondrogenic TF",
        prediction="Drives growth plate proliferation",
        scaling="L"
    ),
    ProteinTarget(
        gene="SHH", uniprot="Q15465", term="Gamma_m",
        role="Sonic Hedgehog; morphogen gradient",
        prediction="Compact signaling molecule",
        scaling="L"
    ),
    ProteinTarget(
        gene="CDKN1A", uniprot="P38936", term="Gamma_m",
        role="p21; cell cycle inhibitor",
        prediction="Upregulated in microgravity",
        scaling="threshold"
    ),
    ProteinTarget(
        gene="PPARGC1A", uniprot="Q9UBK2", term="Gamma_m",
        role="PGC-1a; Mitochondrial biogenesis master regulator",
        prediction="Energy supply bottleneck during growth",
        scaling="L",
        dual_role=True,
        upstream="Gamma_m (AMPK activation)"
    ),
    ProteinTarget(
        gene="IGF1R", uniprot="P08069", term="Gamma_m",
        role="Insulin-like growth factor 1 receptor",
        prediction="Signaling receptor for growth spurt rate",
        scaling="L"
    ),
    ProteinTarget(
        gene="GHR", uniprot="P10912", term="Gamma_m",
        role="Growth hormone receptor",
        prediction="Regulates the rate of spinal elongation",
        scaling="L"
    ),
    ProteinTarget(
        gene="ARNTL", uniprot="O00327", term="Gamma_m",
        role="BMAL1; circadian clock TF",
        prediction="Circadian rhythm disruption linked to scoliosis",
        scaling="L"
    ),

    # ===== Longevity Extensions =====
    ProteinTarget(
        gene="FOXO3", uniprot="O43524", term="longevity",
        role="Stress resistance, autophagy, DNA repair",
        prediction="Activated by AMPK (from muscle contraction) and deacetylated by SIRT1",
        scaling="activity level",
        upstream="eta_a + Gamma_m"
    ),
    ProteinTarget(
        gene="KLOTHO", uniprot="Q9UEF7", term="longevity",
        role="Anti-aging hormone, Ca2+ homeostasis",
        prediction="Secreted in response to proprioceptive Ca2+ transients",
        scaling="activity level",
        upstream="eta_p (PIEZO -> Ca2+)"
    ),
    ProteinTarget(
        gene="YAP1", uniprot="P46937", term="longevity",
        role="Tissue repair and proliferation",
        prediction="Nuclear translocation driven by cytoskeletal tension",
        scaling="activity level",
        upstream="eta_a (VIM/LMNA tension)"
    ),
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
                        all_proteins[gene]["_source_file"] = str(metrics_file)
    return all_proteins

def main():
    print("=" * 70)
    print("  THERMODYNAMIC COST: Longevity Protein Extension")
    print("=" * 70)

    metrics = load_all_metrics()
    print(f"\n  Loaded pre-computed metrics for {len(metrics)} proteins")

    csv_path = OUTPUT_DIR / "thermodynamic_cost_proteins_extended.csv"
    rows = []

    for t in TARGETS:
        m = metrics.get(t.gene, {})
        # Note: pae_blockiness is the correct key per codebase memory
        rows.append({
            "gene": t.gene,
            "uniprot": t.uniprot,
            "term": t.term,
            "dual_role": str(t.dual_role),
            "upstream_activator": t.upstream,
            "role": t.role,
            "scaling": t.scaling,
            "anisotropy": m.get("anisotropy_index", ""),
            "morphology": m.get("morphology", ""),
            "rg": m.get("radius_of_gyration", ""),
            "plddt_mean": m.get("plddt_mean", ""),
            "n_residues": m.get("n_residues", ""),
            "hinge_candidates": m.get("hinge_candidates", ""),
            "disorder_fraction": m.get("disorder_fraction_proxy", ""),
            "PAE_blockiness": m.get("pae_blockiness", ""),
            "status": "matched" if t.gene in metrics else "missing",
        })

    if rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  ✅ Extended CSV: {csv_path}")

    print(f"\n  Mapped {len(TARGETS)} proteins total:")
    print(f"  - core framework: 23 proteins")
    print(f"  - longevity new : 3 proteins")
    print(f"  - dual-role     : 2 proteins (SIRT1, PPARGC1A)")

if __name__ == "__main__":
    main()
