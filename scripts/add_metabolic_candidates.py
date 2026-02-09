import csv
import os
from pathlib import Path

MASTER_FILE = Path("data/candidates_master.csv")

new_candidates = [
    {
        "gene_symbol": "PPARGC1A",
        "uniprot_id": "Q9UBK2",
        "organism": "Homo sapiens",
        "pathway_tags": "Metabolism,Mitochondria,Signaling",
        "gravity_link": "Master regulator of mitochondrial biogenesis; determines ATP supply capacity.",
        "spine_curvature_link": "Supply-side failure in Energy Deficit Window; reduced expression in AIS muscle.",
        "priority_score": 96,
        "justification": "Key metabolic regulator defining the energy supply limit."
    },
    {
        "gene_symbol": "IGF1R",
        "uniprot_id": "P08069",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Growth,Receptor",
        "gravity_link": "Growth factor receptor; sets the metabolic pace of growth against gravity.",
        "spine_curvature_link": "Essential for vertebral growth velocity; signaling intensity defines demand.",
        "priority_score": 96,
        "justification": "Primary growth regulator determining the rate of structure formation."
    },
    {
        "gene_symbol": "GHR",
        "uniprot_id": "P10912",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Growth,Receptor",
        "gravity_link": "Growth hormone receptor; systemic regulator of growth velocity.",
        "spine_curvature_link": "GH/IGF-1 axis drives the adolescent growth spurt, the risk window for AIS.",
        "priority_score": 96,
        "justification": "Systemic driver of the growth spurt."
    },
    {
        "gene_symbol": "ARNTL",
        "uniprot_id": "O00327",
        "organism": "Homo sapiens",
        "pathway_tags": "Circadian,Metabolism,Signaling",
        "gravity_link": "Circadian clock (BMAL1); regulates temporal gating of repair.",
        "spine_curvature_link": "Loss of circadian rhythm exacerbates metabolic stress; potential 'Spinal Jetlag'.",
        "priority_score": 96,
        "justification": "Core clock component linking time to metabolic capacity."
    }
]

update_candidates = {
    "DMD": 96,
    "MYLK": 96
}

def main():
    if not MASTER_FILE.exists():
        print(f"Error: {MASTER_FILE} not found.")
        return

    # Read existing
    rows = []
    fieldnames = []
    existing_symbols = set()

    with open(MASTER_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            gene = row['gene_symbol']
            existing_symbols.add(gene)

            # Update priority if in update list
            if gene in update_candidates:
                print(f"Updating priority for {gene} from {row['priority_score']} to {update_candidates[gene]}")
                row['priority_score'] = update_candidates[gene]

            rows.append(row)

    # Append new
    added_count = 0
    for cand in new_candidates:
        if cand['gene_symbol'] in existing_symbols:
            print(f"Skipping {cand['gene_symbol']} (already exists)")
            continue

        # Ensure all fields are present
        row = {col: cand.get(col, "") for col in fieldnames}
        rows.append(row)
        print(f"Added {cand['gene_symbol']}")
        added_count += 1

    # Write back
    with open(MASTER_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully added {added_count} new candidates and updated {len(update_candidates)} priorities.")

if __name__ == "__main__":
    main()
