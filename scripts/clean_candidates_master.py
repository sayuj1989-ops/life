import csv
import sys
from pathlib import Path

MASTER_FILE = Path("data/candidates_master.csv")

TARGETS = {
    "PPARGC1A": {
        "uniprot_id": "Q9UBK2",
        "pathway_tags": "Thermodynamic_Cost",
        "gravity_link": "Mitochondrial biogenesis master regulator; determines energy SUPPLY capacity.",
        "spine_curvature_link": "Energy supply bottleneck during growth spurt contributes to AIS.",
        "priority_score": "100",
        "justification": "Essential for Gamma_m supply side."
    },
    "IGF1R": {
        "uniprot_id": "P08069",
        "pathway_tags": "Thermodynamic_Cost",
        "gravity_link": "Insulin-like growth factor 1 receptor; mediates growth plate signaling.",
        "spine_curvature_link": "Signaling receptor for growth spurt rate; rapid growth linked to curve progression.",
        "priority_score": "100",
        "justification": "Essential for Gamma_m supply side."
    },
    "GHR": {
        "uniprot_id": "P10912",
        "pathway_tags": "Thermodynamic_Cost",
        "gravity_link": "Growth hormone receptor; master regulator of adolescent growth spurt rate.",
        "spine_curvature_link": "Regulates the rate of spinal elongation; rapid growth is a risk factor for AIS.",
        "priority_score": "100",
        "justification": "Essential for Gamma_m supply side."
    },
    "ARNTL": {
        "uniprot_id": "O00327",
        "pathway_tags": "Thermodynamic_Cost",
        "gravity_link": "BMAL1; circadian clock TF in intervertebral disc.",
        "spine_curvature_link": "Circadian rhythm disruption linked to disc degeneration and scoliosis.",
        "priority_score": "100",
        "justification": "Essential for Gamma_m supply side."
    },
    "DMD": {
        "uniprot_id": "P11532",
        "pathway_tags": "Thermodynamic_Cost",
        "gravity_link": "Dystrophin; cytoskeleton-ECM linker in paraspinal muscle (eta_a term).",
        "spine_curvature_link": "Duchenne Muscular Dystrophy patients have very high prevalence of severe, progressive scoliosis. (SciELO)",
        "priority_score": "100",
        "justification": "Essential for maintenance of muscle tone against gravity; loss leads to collapse."
    },
    "MYLK": {
        "uniprot_id": "Q15746",
        "pathway_tags": "Thermodynamic_Cost",
        "gravity_link": "Myosin light chain kinase; tonic contraction regulator (eta_a term).",
        "spine_curvature_link": "Genetic variants associated with AIS susceptibility. (DOI: 10.1007/s00586-011-2067-7)",
        "priority_score": "100",
        "justification": "Regulator of myosin contractility."
    }
}

def main():
    if not MASTER_FILE.exists():
        print(f"Error: {MASTER_FILE} not found.")
        sys.exit(1)

    rows = []
    seen_genes = set()

    # Read existing
    try:
        with open(MASTER_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                gene = row['gene_symbol']

                # If it's one of our targets, skip it for now (we'll add the correct version later)
                # unless we want to keep existing entries that might have different info?
                # The user wants duplicates removed.
                if gene in TARGETS:
                    continue

                if gene not in seen_genes:
                    rows.append(row)
                    seen_genes.add(gene)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    # Add our targets
    for gene, data in TARGETS.items():
        new_row = {
            "gene_symbol": gene,
            "uniprot_id": data["uniprot_id"],
            "organism": "Homo sapiens",
            "pathway_tags": data["pathway_tags"],
            "gravity_link": data["gravity_link"],
            "spine_curvature_link": data["spine_curvature_link"],
            "priority_score": data["priority_score"],
            "justification": data["justification"]
        }
        # Ensure all fields are present
        for field in fieldnames:
            if field not in new_row:
                new_row[field] = ""

        rows.append(new_row)
        print(f"Added/Updated {gene}")

    # Write back
    try:
        with open(MASTER_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Successfully cleaned and updated {MASTER_FILE}")
    except Exception as e:
        print(f"Error writing CSV: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
