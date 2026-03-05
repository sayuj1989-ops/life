import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "SDC4",
            "uniprot_id": "P31431",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,ECM,Adhesion",
            "gravity_link": "Focal adhesion coreceptor translating extracellular tension to the cytoskeleton.",
            "spine_curvature_link": "Crucial for intervertebral disc maintenance and transduces mechanical loads in cartilage. (DOI: 10.1016/j.matbio.2018.04.011)",
            "priority_score": "86",
            "justification": "Key mechanotransducer linking ECM to intracellular tension."
        },
        {
            "gene_symbol": "LUM",
            "uniprot_id": "P51884",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Growth_Plate,Collagen",
            "gravity_link": "Major ECM proteoglycan regulating collagen fibril assembly for tensile strength against gravity.",
            "spine_curvature_link": "Deficiency disrupts collagen network, leading to kyphoscoliosis in mouse models. (DOI: 10.1074/jbc.M309783200)",
            "priority_score": "87",
            "justification": "Directly implicated in structural integrity of the spine via collagen regulation."
        },
        {
            "gene_symbol": "DCN",
            "uniprot_id": "P07585",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Growth_Plate,Collagen",
            "gravity_link": "Binds type I collagen fibrils, essential for transmitting and distributing mechanical loads.",
            "spine_curvature_link": "Deficiency causes connective tissue weakness and spinal curvature abnormalities. (DOI: 10.1038/srep15623)",
            "priority_score": "86",
            "justification": "Crucial for mechanical load distribution in connective tissues."
        },
        {
            "gene_symbol": "MFNG",
            "uniprot_id": "O00587",
            "organism": "Homo sapiens",
            "pathway_tags": "Segmentation,Notch,Somite",
            "gravity_link": "Modulates Notch receptor signaling during the somite segmentation clock.",
            "spine_curvature_link": "Essential for proper vertebral segmentation; defects lead to congenital scoliosis. (DOI: 10.1093/hmg/ddg036)",
            "priority_score": "89",
            "justification": "Core component of the somite clock essential for vertebral patterning."
        },
        {
            "gene_symbol": "BBS4",
            "uniprot_id": "Q96IZ7",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Mechanotransduction",
            "gravity_link": "Core component of the BBSome in primary cilia, cellular mechanosensors of fluid flow/strain.",
            "spine_curvature_link": "Ciliopathy mutations cause skeletal defects and scoliosis. (DOI: 10.1371/journal.pgen.1000326)",
            "priority_score": "85",
            "justification": "Ciliary component strongly linked to skeletal ciliopathies."
        },
        {
            "gene_symbol": "GPR161",
            "uniprot_id": "Q8N6U8",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Signaling,Hedgehog",
            "gravity_link": "Localizes to primary cilia, regulating Hedgehog signaling in response to mechanical/ciliary cues.",
            "spine_curvature_link": "Mutants display neural tube and skeletal patterning defects including spinal column malformations. (DOI: 10.1016/j.cell.2013.01.020)",
            "priority_score": "85",
            "justification": "Key receptor in ciliary Hedgehog signaling essential for skeletal patterning."
        },
        {
            "gene_symbol": "AMOT",
            "uniprot_id": "Q4VCS5",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Cell_Polarity,Hippo",
            "gravity_link": "Mechanosensitive scaffold binding F-actin and YAP/TAZ; regulates shape under physical force.",
            "spine_curvature_link": "Bridges actin cytoskeleton with Hippo signaling to control tissue growth patterns. (DOI: 10.1038/ncb2271)",
            "priority_score": "86",
            "justification": "Important YAP/TAZ regulator bridging cytoskeletal tension and growth."
        },
        {
            "gene_symbol": "MYH10",
            "uniprot_id": "P35580",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Motor_Protein,Mechanotransduction",
            "gravity_link": "Non-muscle myosin IIB provides cellular contractility and tension generation against physical forces.",
            "spine_curvature_link": "Required for mechanical feedback during tissue morphogenesis and spinal cord development. (DOI: 10.1016/j.devcel.2007.12.007)",
            "priority_score": "85",
            "justification": "Provides the contractility required for mechanosensing and tissue stiffness."
        },
        {
            "gene_symbol": "STK3",
            "uniprot_id": "Q13188",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Hippo,Signaling",
            "gravity_link": "Core kinase in the Hippo pathway, sensitive to mechanical stress and cytoskeletal tension.",
            "spine_curvature_link": "Regulates YAP/TAZ activity crucial for bone development and mechanosensing in growth plates. (DOI: 10.1038/nrm.2016.118)",
            "priority_score": "87",
            "justification": "Upstream regulator of the key mechanotransducer YAP1 in skeletal tissues."
        },
        {
            "gene_symbol": "STK4",
            "uniprot_id": "Q13043",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Hippo,Signaling",
            "gravity_link": "Paralog of STK3, core Hippo kinase inhibiting YAP/TAZ under low mechanical tension.",
            "spine_curvature_link": "Cooperates with STK3 in skeletal development and growth plate regulation. (DOI: 10.1038/nrm.2016.118)",
            "priority_score": "87",
            "justification": "Core kinase for sensing lack of tension in mechanotransduction pathways."
        }
    ]

    existing_genes = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_genes.add(row['gene_symbol'])

    count = 0
    with open(MASTER_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"])
        # No header write, appending
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
