import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "PKD2L2",
            "uniprot_id": "Q9NZM6",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Mechanotransduction,Ion_Channel",
            "gravity_link": "Forms mechanosensitive channel complexes in primary cilia; senses fluid flow and mechanical stress.",
            "spine_curvature_link": "Polycystin channels are critical for left-right asymmetry; defects in related channels cause spinal anomalies. (Extrapolated from PKD family)",
            "priority_score": "80",
            "justification": "Ciliary mechanosensor potentially compensating or interacting with other PKD channels."
        },
        {
            "gene_symbol": "FBN3",
            "uniprot_id": "Q7Z5A9",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction",
            "gravity_link": "Microfibril component providing elasticity and sequestering TGF-beta; responds to tissue stretch.",
            "spine_curvature_link": "Fibrillin family members (e.g., FBN1, FBN2) are strongly linked to Marfan and Beals syndromes featuring scoliosis.",
            "priority_score": "82",
            "justification": "Structural determinant of elasticity, homologous to FBN1."
        },
        {
            "gene_symbol": "WNT4",
            "uniprot_id": "P56705",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Bone,Mechanotransduction",
            "gravity_link": "Wnt ligand regulating bone mass and osteoblast differentiation; expression is mechanically regulated.",
            "spine_curvature_link": "Wnt signaling is critical for vertebral bone mass and structural integrity.",
            "priority_score": "80",
            "justification": "Key regulator of bone mass under Wnt control."
        },
        {
            "gene_symbol": "COL5A2",
            "uniprot_id": "P05997",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Structure",
            "gravity_link": "Regulates collagen fibril diameter and tissue tensile strength against gravity.",
            "spine_curvature_link": "Classical Ehlers-Danlos syndrome, associated with spinal laxity and scoliosis, is linked to COL5A mutations. (DOI: 10.1002/humu.23594)",
            "priority_score": "85",
            "justification": "Structural determinant of tissue stiffness and joint stability."
        },
        {
            "gene_symbol": "NOTCH3",
            "uniprot_id": "Q9UM47",
            "organism": "Homo sapiens",
            "pathway_tags": "Segmentation,Signaling",
            "gravity_link": "Notch signaling is sensitive to mechanical forces and fluid shear stress.",
            "spine_curvature_link": "Notch pathway is essential for somitogenesis and vertebral segmentation.",
            "priority_score": "82",
            "justification": "Linked to vertebral segmentation."
        },
        {
            "gene_symbol": "TRPV1",
            "uniprot_id": "Q8NER1",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Ion_Channel,Inflammation",
            "gravity_link": "Mechanosensitive ion channel responding to mechanical and osmotic stress.",
            "spine_curvature_link": "Implicated in intervertebral disc degeneration and nociception. (PMID: 30890250)",
            "priority_score": "78",
            "justification": "Mechanosensor in loaded tissues and discs."
        }
    ]

    existing_genes = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_genes.add(row['gene_symbol'])

    with open(MASTER_FILE, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"])
        # No header write, appending
        count = 0
        for c in new_candidates:
            if c['gene_symbol'] not in existing_genes:
                writer.writerow(c)
                count += 1
                print(f"Added {c['gene_symbol']}")
            else:
                print(f"Skipped {c['gene_symbol']} (already exists)")

    print(f"Added {count} new candidates.")

if __name__ == "__main__":
    main()
