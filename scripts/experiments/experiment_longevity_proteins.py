#!/usr/bin/env python3
"""
Thermodynamic Cost of Countercurvature: Extended Longevity Protein Analysis
===========================================================================

Extends the 23-protein structural analysis to include 5 specific longevity
targets, mapping them onto the free energy dissipation cascade.

  F_dot = integral[ eta_p |dkappa/dt|^2 + eta_a (kappa - kappa_passive)^2 + Gamma_m(s) ] ds

Longevity Targets Added:
  FOXO3     : Downstream of eta_a (AMPK activation from muscle contraction)
  SIRT1     : IN Gamma_m (Dual-role: energy gauge + longevity effector)
  Klotho    : Downstream of eta_p (Ca2+ from PIEZO1/2)
  YAP1      : Downstream of eta_a (Mechanosensor bridging tension to nucleus)
  PGC-1alpha: IN Gamma_m (Dual-role: mitochondrial supply + biogenesis)

Author: Dr. Sayuj Krishnan S (Extended)
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
    dual_role: bool = False # Is it both a basal target and a longevity target?

# ---------------------------------------------------------------------------
# The Three Terms + Longevity: Protein Targets
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
        gene="FLNA", uniprot="O75369", term="eta_a",
        role="Filamin-A; cross-links actin filaments, mechanotransduction",
        prediction="High anisotropy, extended V-shape; acts as a shock absorber; "
                   "cost scales with the volumetric mechanical demand of upright posture",
        scaling="L^3 (muscle/fascia volume)"
    ),
    ProteinTarget(
        gene="MYH3", uniprot="P11055", term="eta_a",
        role="Embryonic myosin heavy chain; active force generation",
        prediction="Massive rod-like structure; extreme metabolic cost for synthesis and "
                   "ATP consumption during continuous active maintenance of posture",
        scaling="L^3 (muscle volume)"
    ),
    ProteinTarget(
        gene="LMNA", uniprot="P02545", term="eta_a",
        role="Lamin-A/C; nuclear envelope scaffolding, protects against mechanical stress",
        prediction="High anisotropy (4.75); physical scaffold protecting the nucleus "
                   "from gravity-induced deformation; failure leads to epigenetic changes",
        scaling="L^3 (tissue volume)"
    ),
    ProteinTarget(
        gene="VIM", uniprot="P08670", term="eta_a",
        role="Vimentin; intermediate filament, cellular strain gauge",
        prediction="Extended rod; forms a continuous tensegrity network transmitting "
                   "gravity vector to nucleus; collapses under energy deficit",
        scaling="L^3 (cellular volume)"
    ),
    ProteinTarget(
        gene="CTGF", uniprot="P29279", term="eta_a",
        role="Connective tissue growth factor; matricellular signaling",
        prediction="Moderate anisotropy; downstream effector of mechanical stress; "
                   "scales with the area of mechanically loaded tissue",
        scaling="L^2 (loaded tissue area)"
    ),
    ProteinTarget(
        gene="CYR61", uniprot="O00622", term="eta_a",
        role="Matricellular protein; mechanically induced cell adhesion",
        prediction="Compact but highly dynamic; secreted in response to eta_a strain; "
                   "mediates cross-talk between mechanical load and ECM remodeling",
        scaling="L^2 (loaded tissue area)"
    ),

    # ===== Gamma_m: Basal maintenance =====
    ProteinTarget(
        gene="SHH", uniprot="Q15465", term="Gamma_m",
        role="Sonic hedgehog; morphogen patterning the neural tube and somites",
        prediction="Compact signaling molecule; establishes the initial coordinates "
                   "(Information Field) that the mechanical system must follow",
        scaling="L (axial patterning)"
    ),
    ProteinTarget(
        gene="HOXB7", uniprot="P09629", term="Gamma_m",
        role="Homeobox protein; anteroposterior axis specification",
        prediction="Small, highly disordered TF; sets the spatial gain for local "
                   "growth rates along the spine",
        scaling="L (axial patterning)"
    ),
    ProteinTarget(
        gene="PAX1", uniprot="P15863", term="Gamma_m",
        role="Paired box 1; sclerotome development, spine formation",
        prediction="Disordered TF; defines the boundary conditions for the developing "
                   "vertebrae; errors create intrinsic curvature (chi_kappa)",
        scaling="L (vertebral segmentation)"
    ),
    ProteinTarget(
        gene="COL1A1", uniprot="P02452", term="Gamma_m",
        role="Type I collagen; primary load-bearing structural protein",
        prediction="Triple helix forming massive fibrils; the physical instantiation "
                   "of the 'straight' energy functional; scales with body mass",
        scaling="L^3 (tissue volume)"
    ),
    ProteinTarget(
        gene="COL2A1", uniprot="P02458", term="Gamma_m",
        role="Type II collagen; cartilage and intervertebral disc structure",
        prediction="Provides the compressive resistance (stiffness E0) in the disc; "
                   "degrades if mechanical loading is highly asymmetric",
        scaling="L^3 (disc volume)"
    ),
    ProteinTarget(
        gene="LBX1", uniprot="P52954", term="Gamma_m",
        role="Transcription factor; dorsal spinal cord patterning",
        prediction="Disordered TF; implicated directly in AIS; likely regulates the "
                   "left-right symmetry of proprioceptive neuron scaling",
        scaling="L (neural patterning)"
    ),
    ProteinTarget(
        gene="GPR126", uniprot="Q86SQ4", term="Gamma_m",
        role="Adhesion GPCR; Schwann cell myelination, osteoblast function",
        prediction="Large, multi-domain receptor; crucial for the signal conduction "
                   "velocity in the eta_p proprioceptive loop",
        scaling="L (nerve length)"
    ),
    ProteinTarget(
        gene="BNC2", uniprot="Q6ZN30", term="Gamma_m",
        role="Basonuclin-2; zinc finger protein involved in craniofacial/skeletal development",
        prediction="Highly disordered (zinc fingers); maintains epigenetic state of "
                   "osteoblasts during rapid longitudinal growth",
        scaling="L^3 (bone volume)"
    ),
    ProteinTarget(
        gene="MTNR1B", uniprot="P49286", term="Gamma_m",
        role="Melatonin receptor 1B; circadian rhythm, metabolic regulation",
        prediction="Compact 7-TM receptor; couples the mechanical growth rate to the "
                   "circadian clock; disruption leads to temporal mismatch",
        scaling="L^3 (systemic distribution)"
    ),
    ProteinTarget(
        gene="SOX9", uniprot="P48436", term="Gamma_m",
        role="Master regulator of chondrogenesis; drives longitudinal bone growth",
        prediction="Disordered TF; the 'gas pedal' for length (L); highly active "
                   "during the adolescent growth spurt, creating the energy deficit",
        scaling="L (growth plates)"
    ),
    ProteinTarget(
        gene="CDKN1A", uniprot="P38936", term="Gamma_m",
        role="p21; cyclin-dependent kinase inhibitor, cell cycle arrest",
        prediction="Small, highly disordered; acts as the emergency 'brake' on growth "
                   "when energy supply fails; upregulated during deficit",
        scaling="1 (systemic stress signal)"
    ),

    # ===== NEW LONGEVITY TARGETS =====
    # Note: For dual-role proteins, we create two separate entries to appear properly in the output
    ProteinTarget(
        gene="FOXO3", uniprot="O43524", term="longevity",
        role="Forkhead box O3; master longevity transcription factor",
        prediction="Activated by AMPK during energy depletion (squat/stand exertion); "
                   "drives expression of anti-oxidant and DNA repair genes.",
        scaling="1 (systemic survival state)"
    ),
    ProteinTarget(
        gene="Klotho", uniprot="Q9UEF7", term="longevity",
        role="Anti-aging hormone; regulates phosphate, calcium, and vitamin D",
        prediction="Release stimulated by transient intracellular Ca2+ spikes from "
                   "PIEZO1/2 during d(kappa)/dt (squat-to-stand transition).",
        scaling="1 (systemic hormone)"
    ),
    ProteinTarget(
        gene="YAP1", uniprot="P46937", term="longevity",
        role="Transcriptional coactivator; mechanotransduction effector",
        prediction="Nuclear translocation driven directly by cytoskeletal tension (eta_a) "
                   "via VIM/LMNA; promotes tissue repair; excluded in sedentary state.",
        scaling="L^2 (loaded tissue area)"
    ),

    # SIRT1 original role as Gamma_m (Energy gauge)
    ProteinTarget(
        gene="SIRT1_Gamma", uniprot="Q96EB6", term="Gamma_m",
        role="NAD-dependent deacetylase; cellular energy sensor (supply side)",
        prediction="Compact, well-folded enzyme; detects declining NAD+/NADH ratio "
                   "during peak growth velocity; acts as the supply-side sensor",
        scaling="1 (systemic sensor)",
        dual_role=True
    ),
    # SIRT1 role as Longevity effector
    ProteinTarget(
        gene="SIRT1_L", uniprot="Q96EB6", term="longevity",
        role="NAD-dependent deacetylase; extends lifespan via FOXO/PGC1a deacetylation",
        prediction="Activated by cyclical mechanical loading that temporarily depletes "
                   "ATP -> increases NAD+ -> SIRT1 activates longevity pathways.",
        scaling="1 (systemic survival state)",
        dual_role=True
    ),

    # PGC-1alpha original role as Gamma_m (Mitochondrial supply)
    ProteinTarget(
        gene="PPARGC1A_Gamma", uniprot="Q9UBK2", term="Gamma_m",
        role="PGC-1alpha; master regulator of mitochondrial biogenesis",
        prediction="Highly disordered (73%); extremely vulnerable to energy deficit; "
                   "bottleneck for increasing metabolic supply during growth spurt",
        scaling="L^3 (mitochondrial volume)",
        dual_role=True
    ),
    # PGC-1alpha role as Longevity effector
    ProteinTarget(
        gene="PPARGC1A_L", uniprot="Q9UBK2", term="longevity",
        role="PGC-1alpha; exercise-induced mitochondrial rejuvenation",
        prediction="Upregulated by AMPK during squat-to-stand thermodynamic cycling; "
                   "prevents age-related mitochondrial decline.",
        scaling="L^3 (mitochondrial volume)",
        dual_role=True
    ),
]


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
                    gene = row["gene_symbol"]
                    all_proteins[gene] = row

                    # We need to map the actual gene names to the dual role entries we created
                    if gene == "SIRT1":
                        all_proteins["SIRT1_Gamma"] = row
                        all_proteins["SIRT1_L"] = row
                    if gene == "PPARGC1A" or gene == "PGC-1alpha":
                        all_proteins["PPARGC1A_Gamma"] = row
                        all_proteins["PPARGC1A_L"] = row
                    if gene == "KL": # Klotho is often KL
                        all_proteins["Klotho"] = row

    return all_proteins


def generate_report(targets: List[ProteinTarget], metrics: Dict) -> str:
    """Generate evidence note mapping proteins to dissipation terms."""

    terms = {
        "eta_p": ("Proprioceptive Feedback Cost (η_p)",
                  "The cost of **sensing curvature error**. These proteins maintain "
                  "the proprioceptive circuit that detects deviations from the "
                  "information-prescribed shape. During the growth spurt, sensing "
                  "density (sensors per unit length) must scale with L."),
        "eta_a": ("Active Moment Maintenance (η_a)",
                  "The cost of **tonic muscle contraction and cytoskeletal tension** "
                  "required to hold the counter-curvature against gravity. Scales with L³."),
        "Gamma_m": ("Basal Tissue Maintenance (Γ_m)",
                    "The cost of **matrix turnover, patterning, and metabolic supply**. "
                    "This is the 'budget' that the other terms draw from."),
        "longevity": ("Longevity Effectors",
                      "Proteins directly implicated in human longevity that are activated "
                      "by the cyclical mechanical and thermodynamic perturbations of "
                      "squat-to-stand transitions.")
    }

    lines = []
    lines.append("# Evidence Note: Thermodynamic Cost & Longevity Proteins")
    lines.append(f"Date: {time.strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("## Overview")
    lines.append("This document maps 28 specific molecular targets (23 original + 5 longevity) "
                 "onto the terms of the free energy dissipation functional:")
    lines.append("`Ḟ = ∫ [ η_p |∂κ/∂t|² + η_a(κ−κ_passive)² + Γ_m ] ds`")
    lines.append("")

    for term_id, (term_title, term_desc) in terms.items():
        lines.append(f"## {term_title}")
        lines.append(term_desc)
        lines.append("")

        term_targets = [t for t in targets if t.term == term_id]

        # Table Header
        lines.append("| Gene | UniProt | Anisotropy | Morphology | Rg (Å) | pLDDT | Res | Hinges | Scaling | Role |")
        lines.append("| :--- | :--- | ---: | :--- | ---: | ---: | ---: | ---: | :--- | :--- |")

        for t in term_targets:
            # Map back to original gene name for lookup if it's a split entry
            lookup_gene = t.gene
            if lookup_gene in ["SIRT1_Gamma", "SIRT1_L"]:
                lookup_gene = "SIRT1"
            elif lookup_gene in ["PPARGC1A_Gamma", "PPARGC1A_L"]:
                lookup_gene = "PPARGC1A"
            elif lookup_gene == "Klotho" and lookup_gene not in metrics and "KL" in metrics:
                lookup_gene = "KL"

            m = metrics.get(lookup_gene)
            if m:
                aniso = float(m.get("anisotropy_index", 0))
                morph = m.get("morphology", "?")
                rg = float(m.get("radius_of_gyration", 0))
                plddt = float(m.get("plddt_mean", 0))
                nres = int(m.get("n_residues", 0))
                hinges = int(m.get("hinge_candidates", 0))

                role_str = f"{t.role} {'**(DUAL-ROLE)**' if t.dual_role else ''}"

                lines.append(
                    f"| **{t.gene}** | {t.uniprot} | {aniso:.2f} | "
                    f"{morph} | {rg:.1f} | {plddt:.1f} | {nres} | "
                    f"{hinges} | {t.scaling} | {role_str} |"
                )
            else:
                role_str = f"{t.role} {'**(DUAL-ROLE)**' if t.dual_role else ''}"
                lines.append(
                    f"| **{t.gene}** | {t.uniprot} | — | — | — | — | — | — | "
                    f"{t.scaling} | {role_str} *(no AFCC data)* |"
                )
        lines.append("")

        # Compute term-level statistics
        available = []
        for t in term_targets:
            lookup = t.gene
            if lookup in ["SIRT1_Gamma", "SIRT1_L"]: lookup = "SIRT1"
            elif lookup in ["PPARGC1A_Gamma", "PPARGC1A_L"]: lookup = "PPARGC1A"
            elif lookup == "Klotho" and "KL" in metrics: lookup = "KL"

            if lookup in metrics:
                available.append(metrics[lookup])

        if available:
            anisos = [float(m.get("anisotropy_index", 0)) for m in available]
            rgs = [float(m.get("radius_of_gyration", 0)) for m in available]
            plddts = [float(m.get("plddt_mean", 0)) for m in available]
            total_res = sum(int(m.get("n_residues", 0)) for m in available)
            total_hinges = sum(int(m.get("hinge_candidates", 0)) for m in available)

            lines.append(f"**Structural summary:** Mean anisotropy = **{np.mean(anisos):.2f}**, "
                        f"Rg range = {min(rgs):.0f}–{max(rgs):.0f} Å, "
                        f"Mean pLDDT = {np.mean(plddts):.1f}, "
                        f"Total residues = {total_res}, "
                        f"Total hinges = {total_hinges}")
            lines.append("")

        # Per-protein predictions
        lines.append("### Thermodynamic Predictions")
        lines.append("")
        for t in term_targets:
            lines.append(f"- **{t.gene}** ({t.scaling}): {t.prediction}")
        lines.append("")

    return "\n".join(lines)


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

    # Check coverage
    found = []
    missing = []
    for t in TARGETS:
        lookup = t.gene
        if lookup in ["SIRT1_Gamma", "SIRT1_L"]: lookup = "SIRT1"
        elif lookup in ["PPARGC1A_Gamma", "PPARGC1A_L"]: lookup = "PPARGC1A"
        elif lookup == "Klotho" and "KL" in metrics: lookup = "KL"

        if lookup in metrics:
            found.append(t)
        else:
            missing.append(t)
            print(f"  ⚠ Missing: {t.gene} ({t.uniprot}) - searched for {lookup}")

    print(f"  Matched: {len(found)}/{len(TARGETS)} targets")
    print()

    # Save CSV
    csv_path = OUTPUT_DIR / "thermodynamic_cost_proteins_extended.csv"
    rows = []
    for t in TARGETS:
        lookup = t.gene
        if lookup in ["SIRT1_Gamma", "SIRT1_L"]: lookup = "SIRT1"
        elif lookup in ["PPARGC1A_Gamma", "PPARGC1A_L"]: lookup = "PPARGC1A"
        elif lookup == "Klotho" and "KL" in metrics: lookup = "KL"

        m = metrics.get(lookup, {})
        rows.append({
            "gene": t.gene,
            "uniprot": t.uniprot,
            "term": t.term,
            "role": t.role,
            "scaling": t.scaling,
            "dual_role": t.dual_role,
            "anisotropy": m.get("anisotropy_index", ""),
            "morphology": m.get("morphology", ""),
            "rg": m.get("radius_of_gyration", ""),
            "plddt_mean": m.get("plddt_mean", ""),
            "n_residues": m.get("n_residues", ""),
            "hinge_candidates": m.get("hinge_candidates", ""),
            "disorder_fraction": m.get("disorder_fraction_proxy", ""),
            "PAE_blockiness": m.get("PAE_domain_blockiness_score", ""),
            "status": "matched" if lookup in metrics else "missing",
        })

    if rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  ✅ CSV: {csv_path}")

    # Generate evidence note
    report = generate_report(TARGETS, metrics)
    note_path = Path("notes/evidence") / f"{time.strftime('%Y-%m-%d')}__longevity_proteins.md"
    note_path.parent.mkdir(parents=True, exist_ok=True)
    with open(note_path, "w") as f:
        f.write(report)
    print(f"  ✅ Evidence note: {note_path}")

if __name__ == "__main__":
    main()
