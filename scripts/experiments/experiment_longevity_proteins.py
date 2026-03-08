#!/usr/bin/env python3
"""
Longevity Protein Analysis

Extends the 23-protein thermodynamic cost analysis to include 5 specific
longevity proteins, mapping them to the dissipation functional cascade:
FOXO3, SIRT1, Klotho, YAP1, PGC-1alpha.
"""

import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

# Add the src dir to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path("outputs/thermodynamic_cost")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

METRICS_DIRS = [
    Path("outputs/afcc"),
    Path("research/alphafold_countercurvature/outputs/afcc"),
]

@dataclass
class ProteinTarget:
    gene: str
    uniprot: str
    term: str           # "eta_p", "eta_a", "Gamma_m", or "longevity"
    role: str
    prediction: str
    scaling: str        # How cost scales with spinal length L
    dual_role: bool = False # Flag for SIRT1, PGC-1a

# ---------------------------------------------------------------------------
# The 23 Original Proteins + 5 Longevity Proteins
# ---------------------------------------------------------------------------

TARGETS: List[ProteinTarget] = [
    # ===== eta_p: Proprioceptive feedback dissipation =====
    ProteinTarget(gene="PIEZO2", uniprot="Q9H5I5", term="eta_p", role="Vector mechanosensor for proprioception; detects alignment error", prediction="High anisotropy; channel density must scale with L", scaling="L (sensor density)"),
    ProteinTarget(gene="EGR3", uniprot="Q06889", term="eta_p", role="TF maintaining muscle spindle innervation", prediction="Extended structure; EGR3 expression must scale with L", scaling="L (innervation)"),
    ProteinTarget(gene="RUNX3", uniprot="Q13761", term="eta_p", role="Master regulator of proprioceptive neuron development", prediction="Intermediate anisotropy; expression sets proprioceptive gain", scaling="L (proprioceptive neurons)"),
    ProteinTarget(gene="NTRK3", uniprot="Q16288", term="eta_p", role="TrkC receptor; proprioceptive neuron survival signal", prediction="Intermediate anisotropy; NT-3/TrkC signaling cost scales with L", scaling="L (afferent neurons)"),
    ProteinTarget(gene="PIEZO1", uniprot="Q92508", term="eta_p", role="Scalar mechanosensor; detects membrane tension", prediction="Extended, massive; scalar complement to PIEZO2", scaling="L^2 (membrane area)"),

    # ===== eta_a: Active moment maintenance =====
    ProteinTarget(gene="DMD", uniprot="P11532", term="eta_a", role="Dystrophin; cytoskeleton-ECM linker in paraspinal muscle", prediction="Essential for muscle tone against gravity", scaling="L^3 (muscle volume)"),
    ProteinTarget(gene="MYLK", uniprot="Q15746", term="eta_a", role="Myosin light chain kinase; tonic contraction regulator", prediction="Regulator of myosin contractility; sets the gain of the active moment", scaling="L^2 (contractile force)"),
    ProteinTarget(gene="LBX1", uniprot="P52954", term="eta_a", role="Paraspinal muscle specification TF", prediction="Blocky structure sensitive to nuclear stiffness", scaling="L^2 (muscle cross-section)"),
    ProteinTarget(gene="FLNA", uniprot="P21333", term="eta_a", role="Filamin A; cytoskeletal mechanosensor and crosslinker", prediction="Tension-gated signal integrator; maintenance cost proportional to volume", scaling="L^3 (muscle volume)"),
    ProteinTarget(gene="VIM", uniprot="P08670", term="eta_a", role="Vimentin; gravitational strain gauge in cells", prediction="Intermediate filament; collapses in microgravity triggering ROS", scaling="L^3 (cell volume)"),
    ProteinTarget(gene="LMNA", uniprot="P02545", term="eta_a", role="Lamin A/C; nuclear mechanostat scaling with tissue stiffness", prediction="Highest anisotropy TF; nuclear stiffness scales with gravitational load", scaling="L^2 (load-bearing section)"),
    ProteinTarget(gene="CAV1", uniprot="Q03135", term="eta_a", role="Caveolin-1; membrane curvature sensor", prediction="Cost of maintaining caveolar pits scales with membrane area", scaling="L^2 (membrane area)"),

    # ===== Gamma_m: Basal tissue maintenance =====
    ProteinTarget(gene="COL1A1", uniprot="P02452", term="Gamma_m", role="Type I collagen; primary structural protein", prediction="Triple helix; turnover is largest Gamma_m component", scaling="L^3 (bone/disc volume)"),
    ProteinTarget(gene="COMP", uniprot="P49747", term="Gamma_m", role="Cartilage oligomeric matrix protein; disc ECM maintenance", prediction="ECM scaffold protein; disc height increases during growth", scaling="L (disc height)"),
    ProteinTarget(gene="SIRT1", uniprot="Q96EB6", term="Gamma_m", role="Sirtuin 1; NAD+-dependent metabolic sensor (energy gauge)", prediction="Compact enzyme; acts as the 'fuel gauge' detecting energy deficit", scaling="constant (sensor, not structural)"),
    ProteinTarget(gene="SOX9", uniprot="P48436", term="Gamma_m", role="Master chondrogenic TF", prediction="Drives growth plate proliferation; higher SOX9 = steeper metabolic demand", scaling="L (growth plate activity)"),
    ProteinTarget(gene="SHH", uniprot="Q15465", term="Gamma_m", role="Sonic Hedgehog; morphogen gradient", prediction="Maintains information field I(s); cost scales with rod length", scaling="L (gradient length)"),
    ProteinTarget(gene="CDKN1A", uniprot="P38936", term="Gamma_m", role="p21; cell cycle inhibitor activated by mechanical unloading", prediction="Upregulated in microgravity to halt proliferation", scaling="threshold"),
    ProteinTarget(gene="PPARGC1A", uniprot="Q9UBK2", term="Gamma_m", role="Mitochondrial biogenesis master regulator", prediction="Energy supply bottleneck during growth spurt", scaling="L (mitochondrial volume)"),
    ProteinTarget(gene="IGF1R", uniprot="P08069", term="Gamma_m", role="Insulin-like growth factor 1 receptor", prediction="Receptor density determines sensitivity to systemic growth signals", scaling="L (receptor density)"),
    ProteinTarget(gene="GHR", uniprot="P10912", term="Gamma_m", role="Growth hormone receptor", prediction="Regulates rate of spinal elongation", scaling="L (growth signal)"),
    ProteinTarget(gene="ARNTL", uniprot="O00327", term="Gamma_m", role="BMAL1; circadian clock TF", prediction="Circadian entrainment; coordinates temporal repair", scaling="L (circadian entrainment)"),

    # ===== NEW: Longevity Downstream Proteins =====
    ProteinTarget(
        gene="FOXO3", uniprot="O43524", term="longevity",
        role="Master regulator of stress resistance, autophagy, and DNA repair",
        prediction="Downstream of eta_a (AMPK activation from muscle) and Gamma_m (SIRT1 deacetylation)",
        scaling="constant (downstream effector)"
    ),
    ProteinTarget(
        gene="KLOTHO", uniprot="Q9UEF7", term="longevity",
        role="Anti-aging hormone, protects against vascular and renal aging",
        prediction="Downstream of eta_p; secreted in response to PIEZO-mediated Ca2+ transients",
        scaling="L (systemic release)"
    ),
    ProteinTarget(
        gene="YAP1", uniprot="P46937", term="longevity",
        role="Master transcriptional regulator of tissue repair and proliferation",
        prediction="Downstream of eta_a; nuclear translocation is mechanically driven by VIM/LMNA cytoskeletal tension",
        scaling="L^3 (tissue volume)"
    ),
    ProteinTarget(
        gene="SIRT1_L", uniprot="Q96EB6", term="longevity",
        role="Sirtuin 1; NAD+-dependent metabolic sensor - Longevity Phase",
        prediction="Acts as the 'fuel gauge' detecting energy deficit AND a longevity effector via NAD+ cycling",
        scaling="constant (sensor, not structural)",
        dual_role=True
    ),
    ProteinTarget(
        gene="PPARGC1A_L", uniprot="Q9UBK2", term="longevity",
        role="Mitochondrial biogenesis master regulator (PGC-1a) - Longevity Phase",
        prediction="Energy supply bottleneck during growth, AND longevity effector upregulated by AMPK during cycling",
        scaling="L (mitochondrial volume)",
        dual_role=True
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

    return all_proteins


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("  LONGEVITY PROTEIN EXTENSION: Thermodynamic Cost Analysis")
    print("=" * 70)

    # Load cached metrics
    metrics = load_all_metrics()
    print(f"\n  Loaded metrics for {len(metrics)} proteins")

    # Check coverage
    found = []
    missing = []
    for t in TARGETS:
        search_gene = t.gene.replace("_L", "") # Handle dual role pseudo-genes
        if search_gene in metrics:
            found.append(t)
        else:
            missing.append(t)
            print(f"  ⚠ Missing: {t.gene} ({t.uniprot})")

    print(f"\n  Matched: {len(found)}/{len(TARGETS)} targets")

    # Save CSV
    csv_path = OUTPUT_DIR / "thermodynamic_cost_proteins_extended.csv"
    rows = []
    for t in TARGETS:
        search_gene = t.gene.replace("_L", "")
        m = metrics.get(search_gene, {})
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
            "disorder_fraction": m.get("disorder_fraction_proxy", ""),
            "PAE_blockiness": m.get("PAE_domain_blockiness_score", m.get("pae_blockiness", "")),
            "status": "matched" if t.gene in metrics else "missing",
        })

    if rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  ✅ Extended CSV written to: {csv_path}")


if __name__ == "__main__":
    main()
