import csv
import os

MASTER_FILE = "data/candidates_master.csv"

new_candidates = [
    {
        "gene_symbol": "ITGA5",
        "uniprot_id": "P08648",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Adhesion",
        "gravity_link": "Forms the primary fibronectin receptor (with ITGB1) sensing gravity/stiffness.",
        "spine_curvature_link": "Null mice have truncated posterior axis; essential for somite boundaries. (DOI: 10.1242/dev.01257)",
        "priority_score": 88,
        "justification": "Primary integrin alpha subunit for fibronectin mechanosensing."
    },
    {
        "gene_symbol": "SDC4",
        "uniprot_id": "P31431",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,ECM",
        "gravity_link": "Cooperates with integrins in focal adhesion formation and mechanosensing.",
        "spine_curvature_link": "Deficiency leads to osteoarthritis-like cartilage degeneration; regulates aggrecanases. (DOI: 10.1073/pnas.1306422110)",
        "priority_score": 85,
        "justification": "Key proteoglycan regulator of focal adhesion signaling."
    },
    {
        "gene_symbol": "TRIP11",
        "uniprot_id": "Q15643",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Golgi,Secretion",
        "gravity_link": "Essential for secretion of ECM proteins that resist gravity; interacts with IFT20.",
        "spine_curvature_link": "Mutations cause Achondrogenesis 1A and Odontochondrodysplasia with severe spinal defects. (PMID: 20083543)",
        "priority_score": 88,
        "justification": "GMAP-210 is critical for Golgi structure and secretion of skeletal matrix."
    },
    {
        "gene_symbol": "SLC26A2",
        "uniprot_id": "P50443",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Transport",
        "gravity_link": "Essential for sulfation of GAGs, which provide compressive resistance (turgor) against gravity.",
        "spine_curvature_link": "Mutations cause Diastrophic Dysplasia (hitchhiker thumb + kyphoscoliosis). (DOI: 10.1038/ng0994-19)",
        "priority_score": 90,
        "justification": "Direct cause of kyphoscoliotic dysplasia via ECM sulfation."
    },
    {
        "gene_symbol": "DLL1",
        "uniprot_id": "O00548",
        "organism": "Homo sapiens",
        "pathway_tags": "Segmentation,Notch",
        "gravity_link": "Defines the boundaries of vertebral bodies (the gravity-resisting units).",
        "spine_curvature_link": "Mutations cause Spondylocostal Dysostosis (vertebral fusion/defects). (DOI: 10.1016/j.ajhg.2013.02.012)",
        "priority_score": 85,
        "justification": "Notch ligand essential for vertebral segmentation."
    },
    {
        "gene_symbol": "NEK9",
        "uniprot_id": "Q8TD19",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Kinase",
        "gravity_link": "Ciliary kinase; cilia are flow/gravity sensors.",
        "spine_curvature_link": "Mutations cause Nevo Syndrome (kyphosis/scoliosis). (DOI: 10.1016/j.ajhg.2015.12.010)",
        "priority_score": 85,
        "justification": "Ciliary kinase linked to skeletal dysplasia and spine curvature."
    },
    {
        "gene_symbol": "MAP3K7",
        "uniprot_id": "O43318",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Mechanotransduction",
        "gravity_link": "Central hub for BMP/TGF-beta signaling (load regulated).",
        "spine_curvature_link": "Mutations cause Frontometaphyseal Dysplasia with scoliosis. (DOI: 10.1016/j.ajhg.2016.10.012)",
        "priority_score": 85,
        "justification": "TAK1 is a master regulator of bone/cartilage signaling under load."
    },
    {
        "gene_symbol": "TTC21B",
        "uniprot_id": "Q7Z4L5",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Transport",
        "gravity_link": "Retrograde IFT component essential for ciliary signal transduction.",
        "spine_curvature_link": "Mutations cause Jeune Asphyxiating Thoracic Dystrophy (rib/spine). (DOI: 10.1038/ng.813)",
        "priority_score": 85,
        "justification": "IFT complex A component linked to thoracic dysplasia."
    },
    {
        "gene_symbol": "COL10A1",
        "uniprot_id": "Q03692",
        "organism": "Homo sapiens",
        "pathway_tags": "Growth_Plate,ECM",
        "gravity_link": "Marker of hypertrophic zone where calcification occurs to support load.",
        "spine_curvature_link": "Schmid Metaphyseal Chondrodysplasia involves spinal changes. (DOI: 10.1038/ng0695-177)",
        "priority_score": 82,
        "justification": "Hypertrophic chondrocyte collagen critical for growth plate structure."
    },
    {
        "gene_symbol": "TNC",
        "uniprot_id": "P24821",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Mechanotransduction",
        "gravity_link": "Mechanoregulated 'de-adhesion' protein; upregulated by mechanical stress.",
        "spine_curvature_link": "Highly expressed in the ligamentum flavum of scoliosis patients. (DOI: 10.1186/1471-2474-10-115)",
        "priority_score": 82,
        "justification": "Matricellular protein modulated by load and present in scoliotic tissues."
    },
    {
        "gene_symbol": "GDF11",
        "uniprot_id": "O95390",
        "organism": "Homo sapiens",
        "pathway_tags": "Development,Signaling",
        "gravity_link": "Determines anterior-posterior patterning (Hox regulator).",
        "spine_curvature_link": "Controls vertebral identity; knockout leads to transformation of vertebrae. (DOI: 10.1038/20235)",
        "priority_score": 80,
        "justification": "Growth differentiation factor crucial for axial patterning."
    },
    {
        "gene_symbol": "HOXC9",
        "uniprot_id": "P31256",
        "organism": "Homo sapiens",
        "pathway_tags": "Development,Segmentation",
        "gravity_link": "Specifies thoracic identity (rib bearing) vs lumbar.",
        "spine_curvature_link": "Upregulation associated with AIS; defines the rigid thoracic segment. (DOI: 10.1016/j.spinee.2008.08.003)",
        "priority_score": 80,
        "justification": "Hox gene defining the thoracic curvature segment."
    },
    {
        "gene_symbol": "SMARCA4",
        "uniprot_id": "P51532",
        "organism": "Homo sapiens",
        "pathway_tags": "Chromatin,Development",
        "gravity_link": "ATPase of SWI/SNF complex; remodels chromatin for mechano-response.",
        "spine_curvature_link": "Coffin-Siris syndrome and rhabdoid tumor predisposition syndrome (spinal tumors/scoliosis). (DOI: 10.1038/ng.2201)",
        "priority_score": 80,
        "justification": "Chromatin remodeler linked to syndromic spinal defects."
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
