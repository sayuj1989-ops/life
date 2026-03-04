"""
Fetch AlphaFold v6 structural data for all 23 IEC framework proteins.
Uses API to get correct URLs, then downloads PDB for structural analysis.
"""
import json
import os
import time

import numpy as np
import requests
from scipy.spatial.distance import pdist

PROTEINS = {
    # DEMAND — Proprioceptive sensing (η_p)
    "PIEZO2":    {"uniprot": "Q9H5I5", "category": "Demand", "subcategory": "Proprioceptive", "role": "Phasic vector mechanosensor"},
    "LBX1":     {"uniprot": "P52951", "category": "Demand", "subcategory": "Proprioceptive", "role": "Proprioceptive specification TF"},
    "DSTYK":    {"uniprot": "Q6XUX3", "category": "Demand", "subcategory": "Proprioceptive", "role": "Mechanical antenna kinase"},
    "EGR3":     {"uniprot": "Q06889", "category": "Demand", "subcategory": "Proprioceptive", "role": "Muscle spindle development TF"},
    "RUNX3":    {"uniprot": "Q13761", "category": "Demand", "subcategory": "Proprioceptive", "role": "Proprioceptor differentiation TF"},
    # DEMAND — Cytoskeletal / muscle (η_a)
    "VIM":      {"uniprot": "P08670", "category": "Demand", "subcategory": "Cytoskeletal", "role": "Intermediate filament scaffold"},
    "LMNA":     {"uniprot": "P02545", "category": "Demand", "subcategory": "Cytoskeletal", "role": "Nuclear lamina / mechanotransduction"},
    "CAV1":     {"uniprot": "Q03135", "category": "Demand", "subcategory": "Cytoskeletal", "role": "Membrane mechanosensor"},
    "PIEZO1":   {"uniprot": "Q92508", "category": "Demand", "subcategory": "Cytoskeletal", "role": "Tonic scalar mechanosensor"},
    "ADGRG6":   {"uniprot": "Q86SQ4", "category": "Demand", "subcategory": "Cytoskeletal", "role": "Adhesion receptor (scoliosis-associated)"},
    "FBN2":     {"uniprot": "P35556", "category": "Demand", "subcategory": "Cytoskeletal", "role": "Fibrillin-2 / ECM mechanotransduction"},
    "PTK7":     {"uniprot": "Q13308", "category": "Demand", "subcategory": "Cytoskeletal", "role": "Planar cell polarity receptor"},
    # SUPPLY — Metabolic regulators (Γ_m)
    "GHR":      {"uniprot": "P10912", "category": "Supply", "subcategory": "Metabolic", "role": "Growth hormone receptor"},
    "IGF1R":    {"uniprot": "P08069", "category": "Supply", "subcategory": "Metabolic", "role": "IGF-1 receptor / growth signaling"},
    "PPARGC1A": {"uniprot": "Q9UBK2", "category": "Supply", "subcategory": "Metabolic", "role": "Mitochondrial biogenesis master regulator"},
    "ARNTL":    {"uniprot": "O00327", "category": "Supply", "subcategory": "Metabolic", "role": "BMAL1 / circadian clock"},
    "SIRT1":    {"uniprot": "Q96EB6", "category": "Supply", "subcategory": "Metabolic", "role": "NAD+ energy sensor / deacetylase"},
    "SOX9":     {"uniprot": "P48436", "category": "Supply", "subcategory": "Metabolic", "role": "Chondrogenesis TF"},
    "SHH":      {"uniprot": "Q15465", "category": "Supply", "subcategory": "Metabolic", "role": "Hedgehog morphogen"},
    "CDKN1A":   {"uniprot": "P38936", "category": "Supply", "subcategory": "Metabolic", "role": "p21 / cell cycle arrest sensor"},
    "COMP":     {"uniprot": "P49747", "category": "Supply", "subcategory": "Metabolic", "role": "Cartilage oligomeric matrix protein"},
    "COL1A1":   {"uniprot": "P02452", "category": "Supply", "subcategory": "Metabolic", "role": "Type I collagen alpha-1"},
    "PLOD1":    {"uniprot": "Q02809", "category": "Supply", "subcategory": "Metabolic", "role": "Collagen crosslinking enzyme"},
}

ALPHAFOLD_API = "https://alphafold.ebi.ac.uk/api"

def fetch_api_data(uniprot_id):
    """Fetch AlphaFold prediction metadata from API."""
    url = f"{ALPHAFOLD_API}/prediction/{uniprot_id}"
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        return data[0] if isinstance(data, list) else data
    return None

def compute_structural_metrics(pdb_text):
    """Parse PDB text and compute all structural metrics from CA atoms."""
    ca_coords = []
    plddt_scores = []

    for line in pdb_text.split('\n'):
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            bfactor = float(line[60:66])
            ca_coords.append([x, y, z])
            plddt_scores.append(bfactor)

    if len(ca_coords) < 10:
        return None

    coords = np.array(ca_coords)
    plddts = np.array(plddt_scores)
    centroid = coords.mean(axis=0)
    centered = coords - centroid

    # Gyration tensor
    gyration_tensor = np.einsum('ij,ik->jk', centered, centered) / len(centered)
    eigenvalues = np.sort(np.linalg.eigvalsh(gyration_tensor))[::-1]

    rg = np.sqrt(np.sum(eigenvalues))
    anisotropy = np.sqrt(eigenvalues[0] / eigenvalues[-1]) if eigenvalues[-1] > 0 else float('inf')

    trace = np.sum(eigenvalues)
    asphericity = 1.5 * np.sum((eigenvalues - trace/3)**2) / trace**2 if trace > 0 else 0

    disorder_frac = np.sum(plddts < 50) / len(plddts)
    end_to_end = np.linalg.norm(coords[-1] - coords[0])
    max_dim = np.max(pdist(coords))

    # Hinge candidates: residues where pLDDT dips below 60 flanked by confident regions
    hinge_count = 0
    window = 5
    for i in range(window, len(plddts) - window):
        if plddts[i] < 60:
            left_avg = np.mean(plddts[max(0,i-window):i])
            right_avg = np.mean(plddts[i+1:min(len(plddts),i+1+window)])
            if left_avg > 70 and right_avg > 70:
                hinge_count += 1

    return {
        "seq_length": len(ca_coords),
        "mean_plddt": float(np.mean(plddts)),
        "median_plddt": float(np.median(plddts)),
        "std_plddt": float(np.std(plddts)),
        "anisotropy": float(anisotropy),
        "asphericity": float(asphericity),
        "disorder_fraction": float(disorder_frac),
        "rg_angstrom": float(rg),
        "end_to_end_angstrom": float(end_to_end),
        "max_dimension_angstrom": float(max_dim),
        "hinge_candidates": int(hinge_count),
        "eigenvalues": [float(e) for e in eigenvalues],
        "confidence_bins": {
            "very_high_90plus": float(np.sum(plddts >= 90) / len(plddts)),
            "confident_70_90": float(np.sum((plddts >= 70) & (plddts < 90)) / len(plddts)),
            "low_50_70": float(np.sum((plddts >= 50) & (plddts < 70)) / len(plddts)),
            "very_low_below50": float(np.sum(plddts < 50) / len(plddts)),
        },
        "plddt_per_residue": [float(p) for p in plddts],
    }


def main():
    print("=" * 70)
    print("ALPHAFOLD v6 STRUCTURAL ANALYSIS — IEC FRAMEWORK (23 PROTEINS)")
    print("=" * 70)

    os.makedirs("/sessions/youthful-pensive-allen/alphafold_data", exist_ok=True)
    results = {}

    for gene, info in PROTEINS.items():
        uid = info["uniprot"]
        print(f"\n[{gene}] ({uid})...")

        # Step 1: Get metadata from API (includes correct PDB URL)
        api_data = fetch_api_data(uid)
        if not api_data:
            print("  ✗ API returned nothing")
            continue

        pdb_url = api_data.get("pdbUrl")
        if not pdb_url:
            print("  ✗ No PDB URL in API response")
            continue

        print(f"  PDB: {pdb_url}")

        # Step 2: Download PDB
        pdb_resp = requests.get(pdb_url, timeout=60)
        if pdb_resp.status_code != 200:
            print(f"  ✗ PDB download failed: {pdb_resp.status_code}")
            continue

        # Save PDB locally
        pdb_path = f"/sessions/youthful-pensive-allen/alphafold_data/{gene}_{uid}.pdb"
        with open(pdb_path, 'w') as f:
            f.write(pdb_resp.text)

        # Step 3: Compute metrics
        metrics = compute_structural_metrics(pdb_resp.text)
        if not metrics:
            print("  ✗ Metric computation failed")
            continue

        # Merge API-level data
        api_metrics = {
            "af_version": api_data.get("latestVersion"),
            "af_gene": api_data.get("gene"),
            "af_organism": api_data.get("organismScientificName"),
            "af_globalMetric": api_data.get("globalMetricValue"),
            "af_fractionVeryHigh": api_data.get("fractionPlddtVeryHigh"),
            "af_fractionConfident": api_data.get("fractionPlddtConfident"),
            "af_fractionLow": api_data.get("fractionPlddtLow"),
            "af_fractionVeryLow": api_data.get("fractionPlddtVeryLow"),
        }

        results[gene] = {**info, **metrics, **api_metrics}
        # Remove bulky per-residue data from printout
        print(f"  ✓ Len={metrics['seq_length']}, pLDDT={metrics['mean_plddt']:.1f}, "
              f"Anisotropy={metrics['anisotropy']:.2f}, Disorder={metrics['disorder_fraction']:.1%}, "
              f"Hinges={metrics['hinge_candidates']}")

        time.sleep(0.3)

    # Save results (without per-residue pLDDT to keep file small)
    save_results = {}
    for gene, data in results.items():
        save_results[gene] = {k: v for k, v in data.items() if k != "plddt_per_residue"}

    with open("/sessions/youthful-pensive-allen/alphafold_data/protein_metrics.json", "w") as f:
        json.dump(save_results, f, indent=2)

    # Also save full data including per-residue
    with open("/sessions/youthful-pensive-allen/alphafold_data/protein_metrics_full.json", "w") as f:
        json.dump(results, f, indent=2)

    # ===== SUMMARY STATISTICS =====
    demand = {k: v for k, v in results.items() if v["category"] == "Demand"}
    supply = {k: v for k, v in results.items() if v["category"] == "Supply"}
    proprio = {k: v for k, v in results.items() if v.get("subcategory") == "Proprioceptive"}
    cyto = {k: v for k, v in results.items() if v.get("subcategory") == "Cytoskeletal"}

    print(f"\n\n{'='*70}")
    print(f"SUMMARY STATISTICS ({len(results)}/{len(PROTEINS)} proteins fetched)")
    print(f"{'='*70}")

    for label, group in [("ALL DEMAND", demand), ("  Proprioceptive", proprio),
                          ("  Cytoskeletal", cyto), ("ALL SUPPLY", supply)]:
        if not group:
            continue
        anis = [v['anisotropy'] for v in group.values()]
        plddt = [v['mean_plddt'] for v in group.values()]
        dis = [v['disorder_fraction'] for v in group.values()]
        hinges = [v['hinge_candidates'] for v in group.values()]
        print(f"\n{label} (n={len(group)}):")
        print(f"  Anisotropy:  {np.mean(anis):.2f} ± {np.std(anis):.2f}  (range: {np.min(anis):.2f}–{np.max(anis):.2f})")
        print(f"  Mean pLDDT:  {np.mean(plddt):.1f} ± {np.std(plddt):.1f}")
        print(f"  Disorder:    {np.mean(dis):.1%} ± {np.std(dis):.1%}")
        print(f"  Hinges:      {np.mean(hinges):.1f} ± {np.std(hinges):.1f}")

    if demand and supply:
        d_anis = np.mean([v['anisotropy'] for v in demand.values()])
        s_anis = np.mean([v['anisotropy'] for v in supply.values()])
        gap = (d_anis - s_anis) / s_anis * 100
        print(f"\n{'='*70}")
        print(f"DEMAND–SUPPLY ANISOTROPY GAP: {gap:.1f}%")
        print(f"  Demand mean: {d_anis:.2f}")
        print(f"  Supply mean: {s_anis:.2f}")
        print(f"{'='*70}")

    # Print sorted table
    print(f"\n{'='*70}")
    print("PROTEIN TABLE (sorted by anisotropy, descending)")
    print(f"{'='*70}")
    print(f"{'Gene':<12} {'Cat':<8} {'SubCat':<15} {'Len':>5} {'pLDDT':>6} {'Anis':>6} {'Disord':>7} {'Hinges':>7} {'Rg(Å)':>7}")
    print("-" * 80)
    sorted_prots = sorted(results.items(), key=lambda x: x[1]['anisotropy'], reverse=True)
    for gene, v in sorted_prots:
        print(f"{gene:<12} {v['category']:<8} {v['subcategory']:<15} {v['seq_length']:>5} "
              f"{v['mean_plddt']:>6.1f} {v['anisotropy']:>6.2f} {v['disorder_fraction']:>6.1%} "
              f"{v['hinge_candidates']:>7} {v['rg_angstrom']:>7.1f}")

if __name__ == "__main__":
    main()
