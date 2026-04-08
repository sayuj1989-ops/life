import urllib.request
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Default seed list: mechanobiology and spine morphogenesis
proteins = {
    "P29279": "CTGF",  # Connective tissue growth factor (ECM/Mechanobiology)
    "P12644": "BMP4",  # Bone morphogenetic protein 4 (Morphogen)
    "P46937": "YAP1"   # Yes-associated protein 1 (Mechanotransduction)
}

results = []

def download_af_data(uniprot_id):
    base_url = "https://alphafold.ebi.ac.uk/files/"
    pdb_url = f"{base_url}AF-{uniprot_id}-F1-model_v4.pdb"
    pae_url = f"{base_url}AF-{uniprot_id}-F1-predicted_aligned_error_v4.json"

    pdb_file = f"AF-{uniprot_id}.pdb"
    pae_file = f"AF-{uniprot_id}-pae.json"

    try:
        if not os.path.exists(pdb_file):
            urllib.request.urlretrieve(pdb_url, pdb_file)
        if not os.path.exists(pae_file):
            urllib.request.urlretrieve(pae_url, pae_file)
        return pdb_file, pae_file
    except Exception as e:
        print(f"Error downloading {uniprot_id}: {e}")
        return None, None

def parse_pdb(pdb_file):
    coords = []
    plddts = []
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                plddt = float(line[60:66])
                coords.append([x, y, z])
                plddts.append(plddt)
    return np.array(coords), np.array(plddts)

def compute_metrics(coords, plddts):
    n = len(plddts)
    if n == 0:
        return {}

    plddt_mean = np.mean(plddts)
    plddt_median = np.median(plddts)
    frac_high = np.sum(plddts >= 90) / n
    frac_ok = np.sum((plddts >= 70) & (plddts < 90)) / n
    frac_low = np.sum(plddts < 70) / n
    disorder_proxy = np.sum(plddts < 50) / n

    # High confidence subset
    high_conf_idx = np.where(plddts >= 70)[0]

    # Flags
    low_confidence_warning = plddt_mean < 70 or frac_low > 0.5
    likely_IDR_heavy = disorder_proxy > 0.3

    metrics = {
        "length": n,
        "pLDDT_mean": plddt_mean,
        "pLDDT_median": plddt_median,
        "pLDDT_fraction_high": frac_high,
        "pLDDT_fraction_ok": frac_ok,
        "pLDDT_fraction_low": frac_low,
        "disorder_fraction_proxy": disorder_proxy,
        "low_confidence_warning": low_confidence_warning,
        "likely_IDR_heavy": likely_IDR_heavy
    }

    # Geometry on high confidence backbone
    if len(high_conf_idx) > 10:
        hc_coords = coords[high_conf_idx]

        # Center coords
        center = np.mean(hc_coords, axis=0)
        centered_coords = hc_coords - center

        # PCA for principal axis & anisotropy
        cov = np.cov(centered_coords.T)
        evals, evecs = np.linalg.eigh(cov)
        evals = np.sort(evals)[::-1]

        anisotropy = evals[0] / evals[1] if evals[1] > 0 else 0
        rg = np.sqrt(np.sum(np.var(hc_coords, axis=0)))

        # End-to-end distance (of high conf stretches? Or just max distance?)
        e2e = np.linalg.norm(hc_coords[-1] - hc_coords[0])

        # Curvature approximation (window = 5 residues)
        curvatures = []
        for i in range(2, len(hc_coords)-2):
            p1, p2, p3 = hc_coords[i-2], hc_coords[i], hc_coords[i+2]
            v1 = p2 - p1
            v2 = p3 - p2
            # Use explicit squared summations for L2 norm to optimize performance per memory rule
            n1 = np.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
            n2 = np.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
            if n1 > 0 and n2 > 0:
                cos_theta = np.dot(v1, v2) / (n1 * n2)
                cos_theta = np.clip(cos_theta, -1.0, 1.0)
                angle = np.arccos(cos_theta)
                curvatures.append(angle)
            else:
                curvatures.append(0)

        curvatures = np.array(curvatures)
        mean_curv = np.mean(curvatures) if len(curvatures) > 0 else 0

        metrics.update({
            "radius_of_gyration": rg,
            "end_to_end_distance": e2e,
            "anisotropy_index": anisotropy,
            "curvature_summary": mean_curv
        })
    else:
        metrics.update({
            "radius_of_gyration": None,
            "end_to_end_distance": None,
            "anisotropy_index": None,
            "curvature_summary": None
        })

    return metrics, high_conf_idx

def analyze_all():
    for uid, name in proteins.items():
        print(f"Processing {name} ({uid})...")
        pdb_f, pae_f = download_af_data(uid)
        if not pdb_f:
            continue

        coords, plddts = parse_pdb(pdb_f)
        metrics, hc_idx = compute_metrics(coords, plddts)
        metrics['protein_id'] = f"{name}_{uid}"
        metrics['species'] = "Human"

        # Load PAE
        if os.path.exists(pae_f):
            with open(pae_f, 'r') as f:
                pae_data = json.load(f)
            pae_matrix = np.array(pae_data[0]['distance'])
            metrics['PAE_mean'] = np.mean(pae_matrix)

            # Plot PAE
            plt.figure(figsize=(6,5))
            plt.imshow(pae_matrix, cmap='viridis', aspect='auto')
            plt.colorbar(label='Expected Position Error (Å)')
            plt.title(f"{name} PAE Heatmap")
            plt.savefig(f"outputs/bolt_biofold_cycle/figures/{name}_PAE.png")
            plt.close()

        results.append(metrics)

        # Plot pLDDT
        plt.figure(figsize=(8,3))
        plt.plot(plddts, label='pLDDT', color='blue')
        plt.axhline(70, color='r', linestyle='--', label='Conf. threshold')
        plt.ylabel('pLDDT')
        plt.xlabel('Residue')
        plt.title(f"{name} pLDDT")
        plt.legend()
        plt.savefig(f"outputs/bolt_biofold_cycle/figures/{name}_pLDDT.png")
        plt.close()

    df = pd.DataFrame(results)
    df.to_csv("outputs/bolt_biofold_cycle/metrics.csv", index=False)
    print("Done generating outputs.")

if __name__ == "__main__":
    analyze_all()
