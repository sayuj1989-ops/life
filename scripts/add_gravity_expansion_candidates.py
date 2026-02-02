import csv
import os

MASTER_FILE = "data/candidates_master.csv"

new_candidates = [
    {
        "gene_symbol": "TNS1",
        "uniprot_id": "Q9HBL0",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Adhesion",
        "gravity_link": "Focal adhesion protein linking integrins to actin; essential for sensing matrix stiffness.",
        "spine_curvature_link": "Top GWAS hit for Adolescent Idiopathic Scoliosis (AIS). (DOI: 10.1038/ncomms8644)",
        "priority_score": 92,
        "justification": "GWAS confirmed candidate involved in primary cell-ECM mechanotransduction."
    },
    {
        "gene_symbol": "FERMT2",
        "uniprot_id": "Q96AC1",
        "organism": "Homo sapiens",
        "pathway_tags": "Adhesion,Mechanotransduction",
        "gravity_link": "Kindlin-2; co-activator of integrins essential for chondrocyte mechanosensing.",
        "spine_curvature_link": "Conditional knockout in chondrocytes causes severe dwarfism and spinal deformity. (DOI: 10.1371/journal.pgen.1005384)",
        "priority_score": 88,
        "justification": "Essential activator of integrins in cartilage."
    },
    {
        "gene_symbol": "KMT2D",
        "uniprot_id": "O14686",
        "organism": "Homo sapiens",
        "pathway_tags": "Chromatin,Development",
        "gravity_link": "Histone methyltransferase (MLL2); regulates open chromatin for developmental gene expression.",
        "spine_curvature_link": "Mutations cause Kabuki Syndrome; scoliosis is present in ~50% of patients. (DOI: 10.1038/ng.641)",
        "priority_score": 88,
        "justification": "Major syndromic cause of scoliosis linked to epigenetic regulation."
    },
    {
        "gene_symbol": "CHD7",
        "uniprot_id": "Q9P2D1",
        "organism": "Homo sapiens",
        "pathway_tags": "Chromatin,Development",
        "gravity_link": "Chromatin remodeler; essential for neural crest migration and patterning.",
        "spine_curvature_link": "Mutations cause CHARGE syndrome; scoliosis is a major feature. (DOI: 10.1038/ng1404)",
        "priority_score": 85,
        "justification": "Chromatin remodeling factor linked to syndromic spinal defects."
    },
    {
        "gene_symbol": "ZIC3",
        "uniprot_id": "O60481",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Development",
        "gravity_link": "Zinc finger transcription factor regulating Left-Right asymmetry (nodal flow).",
        "spine_curvature_link": "Mutations cause Heterotaxy and VACTERL association with vertebral anomalies. (DOI: 10.1038/ng0998-90)",
        "priority_score": 88,
        "justification": "Key determinant of body axis symmetry and vertebral patterning."
    },
    {
        "gene_symbol": "CHST3",
        "uniprot_id": "Q7LGC8",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Enzyme",
        "gravity_link": "Sulfates chondroitin 6; determines osmotic pressure (swelling) of cartilage to resist gravity.",
        "spine_curvature_link": "Mutations cause Spondyloepiphyseal Dysplasia Omani Type with severe kyphoscoliosis. (DOI: 10.1086/521257)",
        "priority_score": 85,
        "justification": "Enzyme defining the osmotic stiffness of cartilage."
    },
    {
        "gene_symbol": "IFT172",
        "uniprot_id": "Q9UG01",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Transport",
        "gravity_link": "Intraflagellar transport protein; essential for ciliary assembly and signaling (flow/gravity sensing).",
        "spine_curvature_link": "Mutations cause Jeune and Mainzer-Saldino syndromes with skeletal defects. (DOI: 10.1016/j.ajhg.2013.10.023)",
        "priority_score": 88,
        "justification": "Essential component of the ciliary transport machinery."
    },
    {
        "gene_symbol": "COL9A3",
        "uniprot_id": "Q14050",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Cartilage",
        "gravity_link": "FACIT collagen stabilizing cartilage fibrils against compressive load.",
        "spine_curvature_link": "Mutations cause Stickler Syndrome and Multiple Epiphyseal Dysplasia with spinal defects. (DOI: 10.1086/301772)",
        "priority_score": 85,
        "justification": "Structural component of cartilage matrix."
    },
    {
        "gene_symbol": "SOX5",
        "uniprot_id": "P35711",
        "organism": "Homo sapiens",
        "pathway_tags": "Transcription_Factor,Development",
        "gravity_link": "Regulates chondrogenesis and notochord sheath formation.",
        "spine_curvature_link": "Mutations cause Lamb-Shaffer Syndrome; scoliosis is a cardinal feature. (DOI: 10.1016/j.ajhg.2012.08.028)",
        "priority_score": 85,
        "justification": "Master regulator of cartilage development."
    },
    {
        "gene_symbol": "TBX1",
        "uniprot_id": "O43435",
        "organism": "Homo sapiens",
        "pathway_tags": "Development,Transcription_Factor",
        "gravity_link": "T-box transcription factor; regulates pharyngeal and vertebral segmentation.",
        "spine_curvature_link": "Central gene in 22q11.2 deletion (DiGeorge); scoliosis is highly prevalent. (DOI: 10.1302/0301-620X.97B2.34685)",
        "priority_score": 85,
        "justification": "Key developmental factor with strong syndromic link to scoliosis."
    }
]

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    # Read existing
    existing_symbols = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            existing_symbols.add(row['gene_symbol'])

    # Append new
    with open(MASTER_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        count = 0
        for cand in new_candidates:
            if cand['gene_symbol'] in existing_symbols:
                print(f"Skipping {cand['gene_symbol']} (already exists)")
                continue

            writer.writerow(cand)
            print(f"Added {cand['gene_symbol']}")
            count += 1

    print(f"Successfully added {count} new candidates.")

if __name__ == "__main__":
    main()
