import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

cache_dir = "data/afdb_cache"
proteins = {
    "Q9H5I5": "PIEZO2",
    "P11532": "DMD",
    "Q14118": "DAG1"
}

results = []
for uid, name in proteins.items():
    pdb_file = os.path.join(cache_dir, f"{uid}.pdb")
    pae_file = os.path.join(cache_dir, f"{uid}.json")

    if not os.path.exists(pdb_file):
        print(f"PDB not found for {uid}")
        continue

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

    coords = np.array(coords)
    plddts = np.array(plddts)

    n = len(plddts)
    if n == 0: continue

    plddt_mean = np.mean(plddts)
    plddt_median = np.median(plddts)
    frac_high = np.sum(plddts >= 90) / n
    frac_ok = np.sum((plddts >= 70) & (plddts < 90)) / n
    frac_low = np.sum(plddts < 70) / n
    disorder_proxy = np.sum(plddts < 50) / n

    metrics = {
        "protein_id": f"{name}_{uid}",
        "species": "Human",
        "length": n,
        "pLDDT_mean": round(plddt_mean, 2),
        "pLDDT_median": round(plddt_median, 2),
        "pLDDT_fraction_high": round(frac_high, 3),
        "pLDDT_fraction_ok": round(frac_ok, 3),
        "pLDDT_fraction_low": round(frac_low, 3),
        "disorder_fraction_proxy": round(disorder_proxy, 3),
        "low_confidence_warning": plddt_mean < 70 or frac_low > 0.5,
        "likely_IDR_heavy": disorder_proxy > 0.3
    }

    # Domains heuristic: stretches of pLDDT > 70
    is_high = plddts >= 70
    transitions = np.diff(is_high.astype(int))
    starts = np.where(transitions == 1)[0] + 1
    if is_high[0]:
        starts = np.insert(starts, 0, 0)
    ends = np.where(transitions == -1)[0]
    if is_high[-1]:
        ends = np.append(ends, len(is_high)-1)

    domains = [f"{s}-{e}" for s, e in zip(starts, ends) if e - s > 30]
    metrics["predicted_domain_segments"] = len(domains)

    metrics["hinge_candidates"] = "Not implemented" # Placeholder
    metrics["exposed_surface_proxy"] = "SASA not computed (requires external dep)"
    metrics["charged_patch_score"] = "Not implemented"

    hc_idx = np.where(is_high)[0]
    if len(hc_idx) > 10:
        hc_coords = coords[hc_idx]
        center = np.mean(hc_coords, axis=0)
        centered = hc_coords - center
        cov = np.cov(centered.T)
        evals, evecs = np.linalg.eigh(cov)
        evals = np.sort(evals)[::-1]
        evecs = evecs[:, np.argsort(evals)[::-1]]

        principal_axis = np.round(evecs[:, 0], 3).tolist()
        anisotropy = evals[0] / evals[1] if evals[1] > 0 else 0
        rg = np.sqrt(np.sum(np.var(hc_coords, axis=0)))
        e2e = np.linalg.norm(hc_coords[-1] - hc_coords[0])

        curvatures = []
        torsions = []
        for i in range(2, len(hc_coords)-2):
            p1, p2, p3 = hc_coords[i-2], hc_coords[i], hc_coords[i+2]
            v1 = p2 - p1
            v2 = p3 - p2
            n1 = np.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
            n2 = np.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
            if n1 > 0 and n2 > 0:
                cos_theta = np.dot(v1, v2) / (n1 * n2)
                cos_theta = np.clip(cos_theta, -1.0, 1.0)
                curvatures.append(np.arccos(cos_theta))
            else:
                curvatures.append(0)

            # Torsion approximation
            if i < len(hc_coords) - 3:
               p4 = hc_coords[i+3]
               v3 = p4 - p3
               n_v3 = np.sqrt(v3[0]**2 + v3[1]**2 + v3[2]**2)
               if n1 > 0 and n2 > 0 and n_v3 > 0:
                   b1 = np.cross(v1, v2)
                   b2 = np.cross(v2, v3)
                   n_b1 = np.linalg.norm(b1)
                   n_b2 = np.linalg.norm(b2)
                   if n_b1 > 0 and n_b2 > 0:
                       cos_phi = np.dot(b1, b2) / (n_b1 * n_b2)
                       cos_phi = np.clip(cos_phi, -1.0, 1.0)
                       sign = np.sign(np.dot(v1, b2))
                       torsions.append(sign * np.arccos(cos_phi))
                   else:
                       torsions.append(0)
               else:
                   torsions.append(0)
            else:
                torsions.append(0)


        mean_curv = np.mean(curvatures) if len(curvatures) > 0 else 0
        mean_tors = np.mean(torsions) if len(torsions) > 0 else 0

        # Bending hotspots
        sorted_curv_idx = np.argsort(curvatures)[::-1]
        hotspots = []
        for i in range(min(3, len(sorted_curv_idx))):
           idx = sorted_curv_idx[i]
           orig_idx = hc_idx[idx+2]
           hotspots.append(f"{orig_idx-2}-{orig_idx+2}")

        metrics.update({
            "backbone_principal_axis": principal_axis,
            "radius_of_gyration": round(rg, 2),
            "end_to_end_distance": round(e2e, 2),
            "anisotropy_index": round(anisotropy, 2),
            "curvature_summary": round(mean_curv, 3),
            "torsion_summary": round(mean_tors, 3),
            "bending_hotspots": ",".join(hotspots)
        })

        # Plot curvature
        plt.figure(figsize=(8,3))
        plt.plot(hc_idx[2:len(hc_coords)-2], curvatures, color='green')
        plt.ylabel('Curvature (rad)')
        plt.xlabel('Residue')
        plt.title(f"{name} Backbone Curvature (pLDDT >= 70)")
        plt.savefig(f"outputs/bolt_biofold_cycle/figures/{name}_curvature.png")
        plt.close()

    else:
        metrics.update({
            "backbone_principal_axis": None,
            "radius_of_gyration": None, "end_to_end_distance": None,
            "anisotropy_index": None, "curvature_summary": None,
            "torsion_summary": None, "bending_hotspots": None
        })

    if os.path.exists(pae_file):
        with open(pae_file, 'r') as f:
            pae_data = json.load(f)
        if isinstance(pae_data, list) and 'predicted_aligned_error' in pae_data[0]:
            pae_matrix = np.array(pae_data[0]['predicted_aligned_error'])
        elif isinstance(pae_data, list) and 'distance' in pae_data[0]:
            pae_matrix = np.array(pae_data[0]['distance'])
        else:
            pae_matrix = None

        if pae_matrix is not None:
            metrics['PAE_mean'] = round(np.mean(pae_matrix), 2)
            # blockiness score placeholder
            metrics['PAE_domain_blockiness_score'] = "Not implemented"
            plt.figure(figsize=(6,5))
            plt.imshow(pae_matrix, cmap='viridis', aspect='auto', vmax=30)
            plt.colorbar(label='Expected Position Error (Å)')
            plt.title(f"{name} PAE Heatmap")
            plt.savefig(f"outputs/bolt_biofold_cycle/figures/{name}_PAE.png")
            plt.close()
            metrics['multi_domain_uncertain'] = metrics['PAE_mean'] > 15
        else:
            metrics['PAE_mean'] = None
            metrics['PAE_domain_blockiness_score'] = None
            metrics['multi_domain_uncertain'] = None
    else:
        metrics['PAE_mean'] = None
        metrics['PAE_domain_blockiness_score'] = None
        metrics['multi_domain_uncertain'] = None

    results.append(metrics)

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
