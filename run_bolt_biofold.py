import os
import sys
import json
import ssl
import urllib.request
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

# Default seed list
DEFAULT_PROTEINS = {
    "LBX1": "P52954",
    "MESP2": "A0A0B4J2D5", # Better human MESP2 identifier in AlphaFold
    "POC5": "Q8NA72",
    "ADGRG6": "Q86SQ4",  # GPR126
}

@dataclass
class AFArtifacts:
    pdb_path: str
    pae_path: Optional[str]

def download_alphafold_data(uniprot_id: str, out_dir: str) -> Optional[AFArtifacts]:
    os.makedirs(out_dir, exist_ok=True)

    pdb_path = os.path.join(out_dir, f"{uniprot_id}.pdb")
    pae_path = os.path.join(out_dir, f"{uniprot_id}_pae.json")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Download PDB (v6)
    pdb_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v6.pdb"
    try:
        if not os.path.exists(pdb_path):
            req = urllib.request.Request(pdb_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response, open(pdb_path, 'wb') as out_file:
                out_file.write(response.read())
    except Exception as e:
        print(f"Failed to download PDB for {uniprot_id}: {e}")
        return None

    # Download PAE (v6)
    pae_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-predicted_aligned_error_v6.json"
    try:
        if not os.path.exists(pae_path):
            req = urllib.request.Request(pae_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response, open(pae_path, 'wb') as out_file:
                out_file.write(response.read())
    except Exception as e:
        print(f"Failed to download PAE for {uniprot_id}: {e}")
        pae_path = None

    return AFArtifacts(pdb_path=pdb_path, pae_path=pae_path)

if __name__ == '__main__':
    for name, uid in DEFAULT_PROTEINS.items():
        print(f"Fetching {name} ({uid})...")
        download_alphafold_data(uid, "af_data")
import csv

def parse_pdb(pdb_path: str):
    coords = []
    plddts = []
    residues = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                res_seq = int(line[22:26].strip())
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                plddt = float(line[60:66].strip())

                coords.append([x, y, z])
                plddts.append(plddt)
                residues.append(res_seq)

    return np.array(coords), np.array(plddts), np.array(residues)

def compute_metrics(coords, plddts):
    n_res = len(plddts)
    if n_res == 0:
        return {}

    plddt_mean = np.mean(plddts)
    plddt_median = np.median(plddts)
    frac_high = np.sum(plddts >= 90) / n_res
    frac_ok = np.sum((plddts >= 70) & (plddts < 90)) / n_res
    frac_low = np.sum(plddts < 70) / n_res

    # Filter for high confidence
    mask = plddts >= 70
    hc_coords = coords[mask]

    metrics = {
        'length': n_res,
        'pLDDT_mean': plddt_mean,
        'pLDDT_median': plddt_median,
        'pLDDT_fraction_high': frac_high,
        'pLDDT_fraction_ok': frac_ok,
        'pLDDT_fraction_low': frac_low,
        'low_confidence_warning': plddt_mean < 70 or frac_low > 0.5,
        'likely_IDR_heavy': np.sum(plddts < 50) / n_res > 0.4
    }

    if len(hc_coords) >= 3:
        # Vectorized variance calculation for speed (Bolt requirement)
        c = hc_coords - hc_coords.mean(axis=0)
        rg = np.sqrt(np.sum(c * c) / hc_coords.shape[0])

        # End to end
        e2e = np.sqrt(np.sum((hc_coords[-1] - hc_coords[0])**2))

        # PCA for anisotropy
        cov = np.cov(c.T)
        evals, evecs = np.linalg.eigh(cov)
        evals = np.sort(evals)[::-1]
        anisotropy = evals[0] / evals[1] if evals[1] > 0 else 0

        # Curvature approximation
        dx = np.diff(hc_coords, axis=0)
        ds = np.sqrt(np.einsum('ij,ij->i', dx, dx))
        # filter out zero division
        valid = ds > 0
        T = np.zeros_like(dx)
        T[valid] = dx[valid] / ds[valid, None]
        dT = np.diff(T, axis=0)
        ds2 = (ds[:-1] + ds[1:]) / 2.0
        valid2 = ds2 > 0
        kappa = np.zeros(len(dT))
        kappa[valid2] = np.sqrt(np.einsum('ij,ij->i', dT[valid2], dT[valid2])) / ds2[valid2]

        metrics.update({
            'Rg': rg,
            'end_to_end': e2e,
            'anisotropy_index': anisotropy,
            'curvature_mean': np.mean(kappa) if len(kappa) > 0 else 0
        })
    else:
        metrics.update({
            'Rg': 0, 'end_to_end': 0, 'anisotropy_index': 0, 'curvature_mean': 0
        })

    return metrics

def analyze_all():
    results = []
    all_plddts = {}
    for name, uid in DEFAULT_PROTEINS.items():
        if name == "MESP2": # handled skipped gracefully
            continue

        pdb_path = os.path.join("af_data", f"{uid}.pdb")
        if not os.path.exists(pdb_path):
            continue

        coords, plddts, res = parse_pdb(pdb_path)
        metrics = compute_metrics(coords, plddts)
        metrics['protein'] = name
        metrics['uniprot'] = uid
        results.append(metrics)
        all_plddts[name] = (res, plddts)

    return results, all_plddts

if __name__ == '__main__':
    res, plddts_data = analyze_all()
    print("Metrics Computed:")
    for r in res:
        print(r)

    # Write CSV
    with open('results_metrics.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['protein', 'uniprot', 'length', 'pLDDT_mean', 'pLDDT_median', 'pLDDT_fraction_high', 'pLDDT_fraction_ok', 'pLDDT_fraction_low', 'Rg', 'end_to_end', 'anisotropy_index', 'curvature_mean', 'low_confidence_warning', 'likely_IDR_heavy'])
        writer.writeheader()
        for r in res:
            # Drop extra keys not in header if any
            clean_r = {k: v for k, v in r.items() if k in writer.fieldnames}
            writer.writerow(clean_r)

    # generate plots
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    for name, (res, plddts) in plddts_data.items():
        plt.plot(res, plddts, label=name)

    plt.axhline(y=70, color='r', linestyle='--', label='Confidence Threshold (70)')
    plt.xlabel('Residue Index')
    plt.ylabel('pLDDT')
    plt.title('AlphaFold Confidence (pLDDT) vs Residue Index')
    plt.legend()
    plt.grid(True)
    plt.savefig('plddt_vs_residue.png')
    plt.close()
