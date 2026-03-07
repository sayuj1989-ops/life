#!/usr/bin/env python3
"""
Thermodynamic Cost of Countercurvature: Extended Longevity Protein Analysis
====================================================================

Extends the 23-protein thermodynamic cost analysis to include 5 additional
longevity proteins (FOXO3, SIRT1, Klotho, YAP1, PGC-1α), mapping the three
terms of the free energy dissipation functional to specific molecular players.

  F_dot = integral[ eta_p |dkappa/dt|^2 + eta_a (kappa - kappa_passive)^2 + Gamma_m(s) ] ds

Uses pre-computed AFCC metrics from outputs/afcc/ (AlphaFold structures already
fetched and analyzed by the AFCC pipeline).

Author: Jules
Date: 2026-02-07
"""

import csv
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path("outputs/thermodynamic_cost")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Directories containing pre-computed AFCC metrics
METRICS_DIRS = [
    Path("outputs/afcc"),
    Path("research/alphafold_countercurvature/outputs/afcc"),
]

@dataclass
class ProteinTarget:
    gene: str
    uniprot: str
    term: str           # "eta_p", "eta_a", "Gamma_m", "longevity"
    role: str
    prediction: str
    scaling: str        # How cost scales with spinal length L
    dual_role: bool = False

# ---------------------------------------------------------------------------
# The Four Terms: Protein Targets (23 original + 5 longevity)
# ---------------------------------------------------------------------------

TARGETS: List[ProteinTarget] = [
    # ===== eta_p: Proprioceptive feedback dissipation =====
    ProteinTarget(
        gene="PIEZO2", uniprot="Q9H5I5", term="eta_p",
        role="Vector mechanosensor for proprioception; detects alignment error",
        prediction="High anisotropy (extended) = high metabolic cost to maintain orientation; "
                   "channel density must scale with L during growth spurt",
        scaling="L (sensor density per unit length)"
    ),
    ProteinTarget(
        gene="EGR3", uniprot="Q06889", term="eta_p",
        role="Transcription factor maintaining muscle spindle innervation",
        prediction="Extended structure despite being a TF; high disorder = energetically "
                   "costly to fold; EGR3 expression must scale with L for spindle density",
        scaling="L (innervation per segment)"
    ),
    ProteinTarget(
        gene="RUNX3", uniprot="Q13761", term="eta_p",
        role="Master regulator of proprioceptive neuron development",
        prediction="Intermediate anisotropy, high disorder (56%); its expression level sets "
                   "the proprioceptive gain; insufficient scaling during growth = reduced correction",
        scaling="L (proprioceptive neuron count)"
    ),
    ProteinTarget(
        gene="NTRK3", uniprot="Q16288", term="eta_p",
        role="TrkC receptor; proprioceptive neuron survival signal",
        prediction="Intermediate anisotropy, 9 hinge candidates = conformationally expensive; "
                   "NT-3/TrkC signaling cost scales with spinal length",
        scaling="L (afferent neuron count)"
    ),
    ProteinTarget(
        gene="PIEZO1", uniprot="Q92508", term="eta_p",
        role="Scalar mechanosensor; detects membrane tension (buckling threshold)",
        prediction="Extended (3.9 aniso), massive (2521 res); scalar complement to PIEZO2; "
                   "sets the stiffness floor below which buckling occurs",
        scaling="L^2 (membrane area)"
    ),

    # ===== eta_a: Active moment maintenance =====
    ProteinTarget(
        gene="DMD", uniprot="P11532", term="eta_a",
        role="Dystrophin; cytoskeleton-ECM linker in paraspinal muscle",
        prediction="Essential for maintenance of muscle tone against gravity; loss leads to collapse; "
                   "connects contractile force to the load-bearing ECM.",
        scaling="L^3 (muscle volume)"
    ),
    ProteinTarget(
        gene="MYLK", uniprot="Q15746", term="eta_a",
        role="Myosin light chain kinase; tonic contraction regulator",
        prediction="Regulator of myosin contractility; sets the gain of the active moment; "
                   "failure leads to inability to sustain postural tone.",
        scaling="L^2 (contractile force)"
    ),
    ProteinTarget(
        gene="LBX1", uniprot="P52954", term="eta_a",
        role="Paraspinal muscle specification TF; top GWAS hit for AIS",
        prediction="Intermediate anisotropy, high disorder (61%); blocky structure sensitive "
                   "to nuclear stiffness; during energy deficit, LBX1 program fails first",
        scaling="L^2 (muscle cross-section x length)"
    ),
    ProteinTarget(
        gene="FLNA", uniprot="P21333", term="eta_a",
        role="Filamin A; cytoskeletal mechanosensor and crosslinker",
        prediction="Tension-gated signal integrator; unfolding domains expose cryptic sites; "
                   "maintenance cost proportional to cytoskeletal volume",
        scaling="L^3 (muscle volume)"
    ),
    ProteinTarget(
        gene="VIM", uniprot="P08670", term="eta_a",
        role="Vimentin; gravitational strain gauge in cells",
        prediction="Intermediate filament; collapses in microgravity triggering ROS cascade; "
                   "the 'first domino' in energy deficit — its failure triggers metabolic switch",
        scaling="L^3 (cell volume)"
    ),
    ProteinTarget(
        gene="LMNA", uniprot="P02545", term="eta_a",
        role="Lamin A/C; nuclear mechanostat scaling with tissue stiffness",
        prediction="Highest anisotropy (4.75) among TFs; nuclear stiffness must scale with "
                   "gravitational load during growth; failure = Scalar Senescence",
        scaling="L^2 (load-bearing cross-section)"
    ),
    ProteinTarget(
        gene="CAV1", uniprot="Q03135", term="eta_a",
        role="Caveolin-1; membrane curvature sensor and mechanotransducer",
        prediction="Membrane-embedded sensor; cost of maintaining caveolar pits scales with "
                   "membrane area; connects to YAP/TAZ nuclear translocation",
        scaling="L^2 (membrane area)"
    ),

    # ===== Gamma_m: Basal tissue maintenance =====
    ProteinTarget(
        gene="COL1A1", uniprot="P02452", term="Gamma_m",
        role="Type I collagen; primary structural protein of vertebral bone/disc",
        prediction="Triple helix (high anisotropy expected); collagen turnover is the largest "
                   "single component of Gamma_m; cost scales with tissue volume",
        scaling="L^3 (bone/disc volume)"
    ),
    ProteinTarget(
        gene="COMP", uniprot="P49747", term="Gamma_m",
        role="Cartilage oligomeric matrix protein; disc ECM maintenance",
        prediction="ECM scaffold protein; turnover rate determines matrix maintenance cost; "
                   "disc height increases during growth requiring more COMP",
        scaling="L (disc height x number)"
    ),
    ProteinTarget(
        gene="SIRT1", uniprot="Q96EB6", term="Gamma_m",
        role="Sirtuin 1; NAD+-dependent metabolic sensor (energy gauge)",
        prediction="Compact enzyme; acts as the 'fuel gauge' detecting energy deficit; "
                   "low NAD+/NADH during rapid growth triggers metabolic switch to adipogenesis",
        scaling="constant (sensor, not structural)",
        dual_role=True
    ),
    ProteinTarget(
        gene="SOX9", uniprot="P48436", term="Gamma_m",
        role="Master chondrogenic TF; growth plate cartilage specification",
        prediction="SOX9 drives growth plate proliferation; its activity rate determines dL/dt; "
                   "higher SOX9 = faster growth = steeper metabolic demand curve",
        scaling="L (growth plate activity)"
    ),
    ProteinTarget(
        gene="SHH", uniprot="Q15465", term="Gamma_m",
        role="Sonic Hedgehog; morphogen gradient for vertebral patterning",
        prediction="Compact signaling molecule; maintains the information field I(s) itself; "
                   "gradient maintenance cost scales with rod length",
        scaling="L (gradient length)"
    ),
    ProteinTarget(
        gene="CDKN1A", uniprot="P38936", term="Gamma_m",
        role="p21; cell cycle inhibitor activated by mechanical unloading",
        prediction="Small, compact; upregulated in microgravity to halt proliferation; "
                   "its activation = signal that energy supply is insufficient for growth",
        scaling="threshold (binary switch)"
    ),
    ProteinTarget(
        gene="PPARGC1A", uniprot="Q9UBK2", term="Gamma_m",
        role="Mitochondrial biogenesis master regulator; determines energy SUPPLY capacity",
        prediction="Energy supply bottleneck during growth spurt contributes to AIS; failure to scale "
                   "mitochondrial biogenesis with L^3 leads to metabolic burnout.",
        scaling="L (mitochondrial volume)",
        dual_role=True
    ),
    ProteinTarget(
        gene="IGF1R", uniprot="P08069", term="Gamma_m",
        role="Insulin-like growth factor 1 receptor; mediates growth plate signaling",
        prediction="Signaling receptor for growth spurt rate; rapid growth linked to curve progression; "
                   "receptor density determines sensitivity to systemic growth signals.",
        scaling="L (receptor density)"
    ),
    ProteinTarget(
        gene="GHR", uniprot="P10912", term="Gamma_m",
        role="Growth hormone receptor; master regulator of adolescent growth spurt rate",
        prediction="Regulates the rate of spinal elongation; rapid growth is a risk factor for AIS; "
                   "dictates the pace of demand increase.",
        scaling="L (growth signal)"
    ),
    ProteinTarget(
        gene="ARNTL", uniprot="O00327", term="Gamma_m",
        role="BMAL1; circadian clock TF in intervertebral disc regulating metabolism",
        prediction="Circadian rhythm disruption linked to disc degeneration and scoliosis; essential "
                   "for temporal coordination of repair mechanisms.",
        scaling="L (circadian entrainment)"
    ),

    # ===== Longevity Beneficiaries (Downstream) =====
    ProteinTarget(
        gene="FOXO3", uniprot="O43524", term="longevity",
        role="Stress resistance, autophagy TF",
        prediction="Downstream of η_a (AMPK activation from muscle contraction)",
        scaling="Downstream effector"
    ),
    ProteinTarget(
        gene="SIRT1_L", uniprot="Q96EB6", term="longevity",
        role="Longevity effector via NAD+ cycling",
        prediction="IN Γ_m Dual-role: energy gauge + longevity effector via NAD+ cycling",
        scaling="Downstream effector"
    ),
    ProteinTarget(
        gene="KLOTHO", uniprot="Q9UEF7", term="longevity",
        role="Anti-oxidant, vascular health",
        prediction="Downstream of η_p (Ca²⁺ from PIEZO1/2)",
        scaling="Downstream effector"
    ),
    ProteinTarget(
        gene="YAP1", uniprot="P46937", term="longevity",
        role="Direct mechanosensor bridging η_a to nuclear signaling",
        prediction="Tissue repair, proliferation",
        scaling="Downstream effector"
    ),
    ProteinTarget(
        gene="PPARGC1A_L", uniprot="Q9UBK2", term="longevity",
        role="Mitochondrial supply + exercise-induced biogenesis",
        prediction="IN Γ_m Dual-role: mitochondrial supply + exercise-induced biogenesis",
        scaling="Downstream effector"
    ),
]

# ---------------------------------------------------------------------------
# Load pre-computed metrics
# ---------------------------------------------------------------------------

def load_all_metrics() -> Dict[str, Dict[str, Any]]:
    """Load all pre-computed AFCC metrics, preferring latest date."""
    all_proteins = {}

    for metrics_dir in METRICS_DIRS:
        if not metrics_dir.exists():
            continue
        # Sort by date (directory name) to get latest last (will overwrite)
        for metrics_file in sorted(metrics_dir.glob("*/metrics.csv")):
            with open(metrics_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    gene = row.get("gene_symbol", "")
                    if gene:
                        all_proteins[gene] = row
                        all_proteins[gene]["_source_file"] = str(metrics_file)

    return all_proteins


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("  THERMODYNAMIC COST OF COUNTERCURVATURE: Extended Longevity Analysis")
    print("  Using pre-computed AFCC metrics")
    print("=" * 70)

    # Load cached metrics
    metrics = load_all_metrics()
    print(f"\n  Loaded metrics for {len(metrics)} proteins")

    # Save CSV
    csv_path = OUTPUT_DIR / "thermodynamic_cost_proteins_extended.csv"
    rows = []
    for t in TARGETS:
        lookup_gene = t.gene.replace("_L", "") # Handle SIRT1_L and PPARGC1A_L
        m = metrics.get(lookup_gene, {})
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
            "PAE_blockiness": m.get("pae_blockiness", m.get("PAE_domain_blockiness_score", "")),
            "status": "matched" if lookup_gene in metrics else "missing",
            "dual_role": t.dual_role
        })

    if rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  ✅ CSV: {csv_path}")

    # Print summary
    print(f"\n{'='*70}")
    print("  SUMMARY BY DISSIPATION TERM")
    print(f"{'='*70}")

    for term, label in [("eta_p", "η_p (Sensing)"), ("eta_a", "η_a (Actuation)"), ("Gamma_m", "Γ_m (Maintenance)"), ("longevity", "Longevity Beneficiaries")]:
        term_targets = [t for t in TARGETS if t.term == term]

        term_targets_matched = [t for t in term_targets if t.gene.replace("_L", "") in metrics]

        if not term_targets_matched:
            print(f"\n  {label}: {len(term_targets)} proteins, NO AFCC METRICS MATCHED")
            continue

        anisos = [float(metrics[t.gene.replace("_L", "")]["anisotropy_index"]) for t in term_targets_matched if metrics[t.gene.replace("_L", "")].get("anisotropy_index")]
        rgs = [float(metrics[t.gene.replace("_L", "")]["radius_of_gyration"]) for t in term_targets_matched if metrics[t.gene.replace("_L", "")].get("radius_of_gyration")]

        mean_aniso = np.mean(anisos) if anisos else 0.0
        min_rg = min(rgs) if rgs else 0.0
        max_rg = max(rgs) if rgs else 0.0

        print(f"\n  {label}: {len(term_targets)} proteins, "
              f"mean aniso={mean_aniso:.2f}, Rg range={min_rg:.0f}–{max_rg:.0f} Å")

        for t in term_targets:
            lookup_gene = t.gene.replace("_L", "")
            if lookup_gene in metrics:
                m = metrics[lookup_gene]
                a = float(m.get("anisotropy_index", 0))
                rg = float(m.get("radius_of_gyration", 0))
                plddt = float(m.get("plddt_mean", 0))
                nres = int(m.get("n_residues", 0))
                hinges = int(m.get("hinge_candidates", 0))
                morph = m.get("morphology", "?")
                disorder = float(m.get("disorder_fraction_proxy", 0))

                print(f"    {t.gene:10s}  aniso={a:5.2f}  Rg={rg:6.1f}  "
                      f"pLDDT={plddt:5.1f}  res={nres:4d}  "
                      f"hinges={hinges}  disorder={disorder:.0%}  [{morph}]  "
                      f"scales:{t.scaling}")
            else:
                 print(f"    {t.gene:10s}  [MISSING IN AFCC]")


if __name__ == "__main__":
    main()
