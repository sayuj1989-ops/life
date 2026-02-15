import csv
import os

MASTER_FILE = "data/candidates_master.csv"

new_candidates = [
    {
        "gene_symbol": "DAG1",
        "uniprot_id": "Q14118",
        "organism": "Homo sapiens",
        "pathway_tags": "Muscle,ECM,Mechanotransduction",
        "gravity_link": "Central component of Dystrophin-Glycoprotein Complex (DGC), linking laminin (ECM) to dystrophin (actin) to transmit gravity loads.",
        "spine_curvature_link": "Loss leads to muscular dystrophy with severe scoliosis. (DOI: 10.1016/j.ajhg.2011.02.008)",
        "priority_score": 90,
        "justification": "Core structural linker between ECM and cytoskeleton."
    },
    {
        "gene_symbol": "ALPL",
        "uniprot_id": "P05186",
        "organism": "Homo sapiens",
        "pathway_tags": "Bone,Mineralization,Enzyme",
        "gravity_link": "Essential for bone mineralization and stiffness to resist gravity.",
        "spine_curvature_link": "Mutations cause Hypophosphatasia (HPP) with rachitic deformities and scoliosis/kyphosis. (DOI: 10.1002/jbmr.322)",
        "priority_score": 88,
        "justification": "Key enzyme for bone stiffness."
    },
    {
        "gene_symbol": "TCF15",
        "uniprot_id": "Q12870",
        "organism": "Homo sapiens",
        "pathway_tags": "Segmentation,Somite,Transcription_Factor",
        "gravity_link": "Essential for epithelialization of somites, the building blocks of the spine.",
        "spine_curvature_link": "Essential for vertebral column formation; null mice have severe vertebral defects. (DOI: 10.1038/ng0595-39)",
        "priority_score": 85,
        "justification": "Essential for somite epithelialization and vertebral shape."
    },
    {
        "gene_symbol": "ENPP1",
        "uniprot_id": "P22413",
        "organism": "Homo sapiens",
        "pathway_tags": "Bone,Mineralization,Enzyme",
        "gravity_link": "Generates pyrophosphate, regulating tissue calcification and stiffness.",
        "spine_curvature_link": "Mutations cause Generalized Arterial Calcification of Infancy (GACI) and hypophosphatemic rickets with spinal deformities. (DOI: 10.1038/ng1191)",
        "priority_score": 85,
        "justification": "Regulator of mineralization balance."
    },
    {
        "gene_symbol": "XYLT2",
        "uniprot_id": "Q9H1B5",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Enzyme,Proteoglycan",
        "gravity_link": "Initiates GAG synthesis on proteoglycans, essential for compressive stiffness.",
        "spine_curvature_link": "Mutations cause Spondyloocular Syndrome with osteoporosis and scoliosis. (DOI: 10.1016/j.ajhg.2015.03.012)",
        "priority_score": 85,
        "justification": "Essential for proteoglycan synthesis and matrix mechanics."
    },
    {
        "gene_symbol": "B3GALT6",
        "uniprot_id": "Q96L61",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Enzyme,Proteoglycan",
        "gravity_link": "Essential for GAG linker region synthesis; proteoglycans resist gravity.",
        "spine_curvature_link": "Mutations cause Spondyloepimetaphyseal dysplasia with joint laxity (SEMD-JL1) and severe kyphoscoliosis. (DOI: 10.1016/j.ajhg.2013.04.018)",
        "priority_score": 85,
        "justification": "GAG synthesis enzyme linked to severe spinal dysplasia."
    },
    {
        "gene_symbol": "FAM20C",
        "uniprot_id": "Q8IXL6",
        "organism": "Homo sapiens",
        "pathway_tags": "Bone,Secretion,Kinase",
        "gravity_link": "Phosphorylates secreted phosphoproteins (DMP1, OPN) essential for bone formation under load.",
        "spine_curvature_link": "Mutations cause Raine Syndrome (osteosclerotic bone dysplasia) with spinal anomalies. (DOI: 10.1038/ng.224)",
        "priority_score": 85,
        "justification": "The 'Golgi Casein Kinase' essential for bone matrix phosphorylation."
    },
    {
        "gene_symbol": "CHSY1",
        "uniprot_id": "Q86X52",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Enzyme,Cartilage",
        "gravity_link": "Chondroitin synthase; synthesizes CS chains providing osmotic swelling pressure against gravity.",
        "spine_curvature_link": "Mutations cause Temtamy preaxial brachydactyly syndrome with spinal defects. (DOI: 10.1016/j.ajhg.2010.11.006)",
        "priority_score": 82,
        "justification": "Enzyme for chondroitin sulfate synthesis."
    },
    {
        "gene_symbol": "CANT1",
        "uniprot_id": "Q8WVQ1",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Enzyme,Cartilage",
        "gravity_link": "Calcium-activated nucleotidase; regulates proteoglycan synthesis.",
        "spine_curvature_link": "Mutations cause Desbuquois dysplasia with severe kyphoscoliosis. (DOI: 10.1016/j.ajhg.2010.05.014)",
        "priority_score": 85,
        "justification": "Critical for proteoglycan synthesis and cartilage integrity."
    },
    {
        "gene_symbol": "SLC35D1",
        "uniprot_id": "Q9NTN3",
        "organism": "Homo sapiens",
        "pathway_tags": "Transport,ECM,Cartilage",
        "gravity_link": "Transports UDP-glucuronic acid/UDP-N-acetylgalactosamine for chondroitin sulfate synthesis (stiffness).",
        "spine_curvature_link": "Mutations cause Schneckenbecken dysplasia with severe spinal defects. (DOI: 10.1086/339439)",
        "priority_score": 85,
        "justification": "Essential transporter for GAG synthesis components."
    },
    {
        "gene_symbol": "FKBP14",
        "uniprot_id": "Q9NWT1",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Chaperone,ER",
        "gravity_link": "Chaperone for collagen and ECM proteins.",
        "spine_curvature_link": "Mutations cause Ehlers-Danlos Syndrome with progressive kyphoscoliosis (FKBP14-kEDS). (DOI: 10.1016/j.ajhg.2012.01.003)",
        "priority_score": 88,
        "justification": "Defining gene for a kyphoscoliotic EDS subtype."
    },
    {
        "gene_symbol": "SLC39A13",
        "uniprot_id": "Q96H72",
        "organism": "Homo sapiens",
        "pathway_tags": "Ion_Transport,ECM,Bone",
        "gravity_link": "Zinc transporter; Zn is cofactor for lysyl hydroxylases (PLODs) - collagen crosslinking.",
        "spine_curvature_link": "Mutations cause Spondyloocheirodysplastic Ehlers-Danlos syndrome with spinal column defects. (DOI: 10.1038/ng.253)",
        "priority_score": 85,
        "justification": "Regulator of collagen crosslinking via zinc homeostasis."
    },
    {
        "gene_symbol": "MYMK",
        "uniprot_id": "Q96C59",
        "organism": "Homo sapiens",
        "pathway_tags": "Muscle,Development,Fusion",
        "gravity_link": "Essential for myoblast fusion to form multinucleated muscle fibers (force generation).",
        "spine_curvature_link": "Mutations cause Carey-Fineman-Ziter syndrome with scoliosis and myopathy. (DOI: 10.1038/s41467-017-00148-7)",
        "priority_score": 88,
        "justification": "Essential for muscle fiber formation and postural tone."
    },
    {
        "gene_symbol": "LEMD3",
        "uniprot_id": "Q9Y2U8",
        "organism": "Homo sapiens",
        "pathway_tags": "Nucleus,Signaling,Mechanotransduction",
        "gravity_link": "Inner nuclear membrane protein; antagonizes BMP/TGF-beta signaling (mechanosensitive).",
        "spine_curvature_link": "Mutations cause Osteopoikilosis and Buschke-Ollendorff syndrome with spinal involvement. (DOI: 10.1038/ng1455)",
        "priority_score": 82,
        "justification": "Nuclear membrane protein regulating bone density signaling."
    },
    {
        "gene_symbol": "COL22A1",
        "uniprot_id": "Q8NFW1",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Muscle,Adhesion",
        "gravity_link": "FACIT collagen localized to myotendinous junctions; transmits muscle force.",
        "spine_curvature_link": "Essential for myotendinous junction stability; zebrafish mutants show defects. (DOI: 10.1073/pnas.1002526107)",
        "priority_score": 80,
        "justification": "Structural component of the muscle-tendon interface."
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
