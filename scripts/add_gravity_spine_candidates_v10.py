import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "IFT81",
            "uniprot_id": "Q8WYA0",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Transport,IFT",
            "gravity_link": "Core component of the IFT-B complex; essential for anterograde ciliary transport and ciliogenesis.",
            "spine_curvature_link": "Mutations cause Short-rib thoracic dysplasia with or without polydactyly, characterized by skeletal anomalies. (PMID: 24334769)",
            "priority_score": "85",
            "justification": "Essential IFT-B component with direct skeletal dysplasia links."
        },
        {
            "gene_symbol": "IFT27",
            "uniprot_id": "Q9NW79",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Transport,IFT",
            "gravity_link": "Component of the IFT-B complex; regulates ciliary transport and Hedgehog signaling.",
            "spine_curvature_link": "Mutations cause Bardet-Biedl syndrome, which features scoliosis and skeletal defects. (PMID: 24836450)",
            "priority_score": "85",
            "justification": "IFT-B component linked to BBS and Hedgehog signaling."
        },
        {
            "gene_symbol": "CHST12",
            "uniprot_id": "Q9P2D0",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Glycosylation,Cartilage",
            "gravity_link": "Chondroitin 4-O-sulfotransferase 2; transfers sulfate to chondroitin, essential for cartilage stiffness.",
            "spine_curvature_link": "Proteoglycan sulfation is critical for load-bearing in the spine; deficiencies lead to chondrodysplasia. (PMID: 20040404)",
            "priority_score": "82",
            "justification": "Key enzyme for chondroitin sulfation and ECM mechanical properties."
        },
        {
            "gene_symbol": "ANKH",
            "uniprot_id": "Q9HCJ1",
            "organism": "Homo sapiens",
            "pathway_tags": "Bone,Mineralization,Transport",
            "gravity_link": "Transmembrane protein regulating inorganic pyrophosphate (PPi) transport; crucial for preventing pathological calcification and regulating bone mineralization.",
            "spine_curvature_link": "Mutations cause Craniometaphyseal dysplasia and Chondrocalcinosis, directly affecting skeletal and joint mechanics. (PMID: 11326322)",
            "priority_score": "85",
            "justification": "Regulator of PPi transport and biomineralization balance."
        },
        {
            "gene_symbol": "RAB8A",
            "uniprot_id": "P61006",
            "organism": "Homo sapiens",
            "pathway_tags": "Trafficking,Cilia,Signaling",
            "gravity_link": "Rab GTPase essential for vesicular trafficking to the primary cilium; regulates ciliary membrane composition.",
            "spine_curvature_link": "Disruption impairs ciliogenesis and planar cell polarity, pathways closely linked to spinal alignment. (PMID: 17296717)",
            "priority_score": "82",
            "justification": "Key vesicular trafficking regulator for ciliary function."
        },
        {
            "gene_symbol": "BBS4",
            "uniprot_id": "Q96VK1",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Trafficking,Syndromic",
            "gravity_link": "Component of the BBSome; essential for ciliary protein trafficking and mechanosensing.",
            "spine_curvature_link": "Bardet-Biedl syndrome patients have a high prevalence of scoliosis and skeletal abnormalities. (PMID: 15124103)",
            "priority_score": "85",
            "justification": "BBSome component critical for ciliary signaling and skeletal form."
        },
        {
            "gene_symbol": "SLC26A3",
            "uniprot_id": "P40879",
            "organism": "Homo sapiens",
            "pathway_tags": "Ion_Transport,Cartilage",
            "gravity_link": "Chloride/sulfate exchanger; contributes to sulfate pool for proteoglycan synthesis in cartilage.",
            "spine_curvature_link": "Mutations cause Congenital Chloride Diarrhea; altered sulfate transport affects cartilage mechanics. (PMID: 8640232)",
            "priority_score": "75",
            "justification": "Sulfate transporter with indirect role in cartilage sulfation."
        },
        {
            "gene_symbol": "PHOSPHO1",
            "uniprot_id": "Q8TCT1",
            "organism": "Homo sapiens",
            "pathway_tags": "Bone,Mineralization,Enzyme",
            "gravity_link": "Phosphatase required for the initiation of matrix vesicle-mediated biomineralization.",
            "spine_curvature_link": "Knockout mice exhibit scoliosis, bowing of long bones, and hypomineralization. (PMID: 23625754)",
            "priority_score": "88",
            "justification": "Initiator of biomineralization; knockout directly leads to scoliosis."
        },
        {
            "gene_symbol": "ENPP3",
            "uniprot_id": "O14638",
            "organism": "Homo sapiens",
            "pathway_tags": "Bone,Mineralization,Enzyme",
            "gravity_link": "Generates inorganic pyrophosphate (PPi); works alongside ENPP1 to regulate mineralization.",
            "spine_curvature_link": "Regulates the balance of mineralization, which dictates the stiffness of the spinal column. (PMID: 19688177)",
            "priority_score": "80",
            "justification": "Regulator of pyrophosphate and biomineralization."
        },
        {
            "gene_symbol": "ARL6",
            "uniprot_id": "Q9H0F7",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Trafficking,Syndromic",
            "gravity_link": "Arf-like GTPase required for BBSome recruitment to the ciliary membrane.",
            "spine_curvature_link": "Mutations cause Bardet-Biedl syndrome, linking it to syndromic scoliosis. (PMID: 16428318)",
            "priority_score": "85",
            "justification": "Regulator of BBSome trafficking in primary cilia."
        },
        {
            "gene_symbol": "SEC24C",
            "uniprot_id": "P53622",
            "organism": "Homo sapiens",
            "pathway_tags": "Trafficking,ECM,Bone",
            "gravity_link": "COPII coat component essential for ER-to-Golgi transport of large ECM proteins like collagen.",
            "spine_curvature_link": "Proper collagen secretion is fundamental for maintaining spinal connective tissue integrity under load. (PMID: 24706913)",
            "priority_score": "82",
            "justification": "Essential COPII component for collagen trafficking."
        }
    ]

    existing_genes = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_genes.add(row['gene_symbol'].strip().upper())

    count = 0
    with open(MASTER_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"])
        for c in new_candidates:
            if c['gene_symbol'].strip().upper() not in existing_genes:
                c['priority_score'] = c['priority_score'].strip()
                writer.writerow(c)
                count += 1
                print(f"Added {c['gene_symbol']}")
            else:
                print(f"Skipped {c['gene_symbol']} (already exists)")

    print(f"Added {count} new candidates.")

if __name__ == "__main__":
    main()
