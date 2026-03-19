import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "MYO1C",
            "uniprot_id": "O00159",
            "organism": "Homo sapiens",
            "pathway_tags": "Gravity_Sensing,Mechanotransduction,Motor_Protein",
            "gravity_link": "Myosin involved in adaptation of mechanosensitive hair cells in the inner ear.",
            "spine_curvature_link": "Variants in myosins associated with pathophysiology of human hearing loss and vestibular dysfunction. (DOI: 10.3389/fphys.2024.1374901)",
            "priority_score": "80",
            "justification": "Motor protein in hair cells relevant for gravity/vestibular sensing."
        },
        {
            "gene_symbol": "USH1G",
            "uniprot_id": "Q495M9",
            "organism": "Homo sapiens",
            "pathway_tags": "Gravity_Sensing,Scaffold,Mechanotransduction",
            "gravity_link": "Scaffold protein essential for maintaining the structure of hair cell stereocilia (gravity sensors).",
            "spine_curvature_link": "Mutations cause Usher Syndrome Type 1G, linking vestibular areflexia to potential postural defects. (DOI: 10.7705/biomedica.7498)",
            "priority_score": "85",
            "justification": "Essential structural component of vestibular gravity sensing apparatus."
        },
        {
            "gene_symbol": "CIB2",
            "uniprot_id": "O75838",
            "organism": "Homo sapiens",
            "pathway_tags": "Gravity_Sensing,Mechanotransduction,Calcium",
            "gravity_link": "Calcium- and integrin-binding protein required for mechanotransduction in hair cells.",
            "spine_curvature_link": "Role in sensorineural hearing loss; vestibular defects are strongly linked to scoliosis pathogenesis. (DOI: 10.7150/ijms.119492)",
            "priority_score": "82",
            "justification": "Regulates calcium signaling during mechanotransduction in gravity sensors."
        },
        {
            "gene_symbol": "GLI1",
            "uniprot_id": "P08151",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Development",
            "gravity_link": "Transcriptional effector of Hedgehog signaling, which is dependent on primary cilia (mechanosensors).",
            "spine_curvature_link": "Increased hedgehog signaling linked to cranial neural crest cell defects and dysplasia. (DOI: 10.3389/fphys.2026.1751758)",
            "priority_score": "85",
            "justification": "Key effector of ciliary Hedgehog signaling essential for skeletal patterning."
        },
        {
            "gene_symbol": "SMO",
            "uniprot_id": "Q9NWM0",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Cilia",
            "gravity_link": "G protein-coupled receptor that transduces Hedgehog signals at the primary cilium.",
            "spine_curvature_link": "Regulated by ciliary protein localization, essential for skeletal development and spine formation. (DOI: 10.1242/bio.062040)",
            "priority_score": "88",
            "justification": "Primary transducer of Hedgehog signaling at the mechanosensory cilium."
        },
        {
            "gene_symbol": "DISP1",
            "uniprot_id": "Q96F81",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Secretion",
            "gravity_link": "Essential for the release and diffusion of Hedgehog ligands, critical for morphogen gradients.",
            "spine_curvature_link": "Rare-variant aggregation highlights disease-linked genes associated with variations affecting the neural axis. (DOI: 10.1016/j.ajhg.2026.01.011)",
            "priority_score": "80",
            "justification": "Regulator of Hedgehog ligand distribution essential for axial patterning."
        },
        {
            "gene_symbol": "ROCK2",
            "uniprot_id": "O75116",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Signaling,Contractility",
            "gravity_link": "Regulates actin cytoskeleton and actomyosin contractility, essential for cellular response to tension.",
            "spine_curvature_link": "Regulation of cellular contractility by agonists present across loaded tissues. (DOI: 10.1182/bloodadvances.2025017995)",
            "priority_score": "82",
            "justification": "Key regulator of cytoskeletal tension and cellular contractility."
        },
        {
            "gene_symbol": "ACTN1",
            "uniprot_id": "P12814",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Mechanotransduction,Adhesion",
            "gravity_link": "Alpha-actinin linking actin filaments to focal adhesions, crucial for force transmission.",
            "spine_curvature_link": "Implications for cellular structure and interacting proteins under mechanical stress. (DOI: 10.3390/biomedicines13102479)",
            "priority_score": "85",
            "justification": "Core actin crosslinker essential for focal adhesion stability and force transmission."
        },
        {
            "gene_symbol": "ACTN4",
            "uniprot_id": "O43707",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Mechanotransduction,Somite",
            "gravity_link": "Non-muscle alpha-actinin that crosslinks actin filaments and regulates cell motility and adhesion.",
            "spine_curvature_link": "Links inactive integrin alpha 5 with actin in zebrafish somites, essential for proper segmentation. (DOI: 10.1016/j.mcpro.2025.101087)",
            "priority_score": "88",
            "justification": "Essential for somite integrity by linking integrins to the actin cytoskeleton."
        },
        {
            "gene_symbol": "MMP9",
            "uniprot_id": "P14780",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Remodeling,Mechanotransduction",
            "gravity_link": "Gelatinase B; degrades extracellular matrix, mechanically responsive in connective tissues.",
            "spine_curvature_link": "Involved in inflammatory feedback loops during intervertebral disc repair and degeneration under load. (DOI: 10.1002/advs.202521709)",
            "priority_score": "85",
            "justification": "Mechanosensitive MMP critical for disc matrix remodeling and inflammation."
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
