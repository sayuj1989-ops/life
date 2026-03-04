import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "PKD2L1",
            "uniprot_id": "Q9P0L9",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Ion_Channel,Fluid_Flow",
            "gravity_link": "PKD2L1 forms mechanosensitive ion channels in primary cilia and detects fluid flow in the spinal cord central canal (Reissner fiber complex), proxy for gravity/posture.",
            "spine_curvature_link": "Pkd2l1 mutant zebrafish exhibit spine curvature (scoliosis) due to defects in central canal fluid flow sensing. (DOI: 10.1038/s41467-018-06283-3)",
            "priority_score": "88",
            "justification": "Strong functional link between CSF flow sensing (cilia) and spinal alignment."
        },
        {
            "gene_symbol": "ZMPSTE24",
            "uniprot_id": "O75844",
            "organism": "Homo sapiens",
            "pathway_tags": "Nucleus,Mechanotransduction,LINC",
            "gravity_link": "Essential for processing prelamin A to mature lamin A; Lamin A is a key nuclear mechanosensor scaling with tissue stiffness and gravity loading.",
            "spine_curvature_link": "Mutations cause Restrictive Dermopathy and Mandibuloacral Dysplasia, featuring skeletal abnormalities and spinal deformities. (DOI: 10.1093/hmg/ddg065)",
            "priority_score": "85",
            "justification": "Nuclear mechanics link via Lamin A maturation, critical for tissue stiffness response."
        },
        {
            "gene_symbol": "JAG2",
            "uniprot_id": "Q9Y219",
            "organism": "Homo sapiens",
            "pathway_tags": "Segmentation,Notch,Signaling",
            "gravity_link": "Notch ligand required for somite boundary formation and segmentation, establishing the structural units resisting gravity.",
            "spine_curvature_link": "Jag2 null mice exhibit fused vertebrae and severe segmentation defects. (PMID: 10330172)",
            "priority_score": "88",
            "justification": "Core Notch ligand for establishing vertebral structural units."
        },
        {
            "gene_symbol": "RBPJ",
            "uniprot_id": "Q06330",
            "organism": "Homo sapiens",
            "pathway_tags": "Segmentation,Notch,Signaling",
            "gravity_link": "Central transcriptional effector of Notch signaling, translating segmentation clock signals into somite boundaries.",
            "spine_curvature_link": "Mutations cause Spondylocostal Dysostosis and Adams-Oliver syndrome with vertebral fusions. (DOI: 10.1016/j.ajhg.2016.03.003)",
            "priority_score": "85",
            "justification": "Master transcriptional effector of Notch-mediated vertebral segmentation."
        },
        {
            "gene_symbol": "SOX8",
            "uniprot_id": "P57073",
            "organism": "Homo sapiens",
            "pathway_tags": "Growth_Plate,Transcription_Factor",
            "gravity_link": "Paralog of SOX9; redundant role in chondrogenesis and maintaining growth plate / intervertebral disc against compressive load.",
            "spine_curvature_link": "Sox8 null mice show mild skeletal phenotypes but exacerbate Sox9 deficiency defects in cartilage. (PMID: 11520164)",
            "priority_score": "80",
            "justification": "Chondrogenic factor supporting structural integrity of the spine."
        },
        {
            "gene_symbol": "SIX1",
            "uniprot_id": "Q15475",
            "organism": "Homo sapiens",
            "pathway_tags": "Development,Transcription_Factor,Muscle",
            "gravity_link": "Regulates myogenesis and epaxial muscle development, essential for the paraspinal musculature supporting the spine against gravity.",
            "spine_curvature_link": "Six1/Six4 double mutants lack epaxial muscles, leading to severe skeletal and spinal anomalies. (PMID: 15159398)",
            "priority_score": "85",
            "justification": "Essential for paraspinal muscle formation."
        },
        {
            "gene_symbol": "EYA1",
            "uniprot_id": "Q99502",
            "organism": "Homo sapiens",
            "pathway_tags": "Development,Transcription_Factor,Organogenesis",
            "gravity_link": "Coactivator for SIX1 in paraxial mesoderm and muscle development.",
            "spine_curvature_link": "Mutations cause Branchiootorenal (BOR) syndrome, which can include cervical vertebral anomalies. (PMID: 9843981)",
            "priority_score": "82",
            "justification": "Cofactor for SIX1 in developing posture-supporting structures."
        },
        {
            "gene_symbol": "FUT8",
            "uniprot_id": "Q16128",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Glycosylation,Mechanotransduction",
            "gravity_link": "Core fucosylates receptors (like TGF-beta receptor and integrins), tuning their mechanosensitivity and signaling output in loaded tissues.",
            "spine_curvature_link": "Fut8 knockout mice exhibit severe growth retardation, emphysema, and kyphoscoliosis due to altered TGF-beta signaling. (PMID: 16223707)",
            "priority_score": "85",
            "justification": "Tuning of mechanosensitive signaling pathways via glycosylation."
        },
        {
            "gene_symbol": "PKD1L2",
            "uniprot_id": "Q7Z442",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Ion_Channel,Fluid_Flow",
            "gravity_link": "Putative mechanosensor in primary cilia, potentially partnering with PKD2 family channels to sense fluid flow.",
            "spine_curvature_link": "Related to PKD1L1 which is firmly linked to scoliosis in zebrafish; human variants linked to skeletal phenotypes.",
            "priority_score": "80",
            "justification": "Ciliary mechanosensor paralog with potential role in flow sensing."
        },
        {
            "gene_symbol": "LMX1A",
            "uniprot_id": "Q8TE12",
            "organism": "Homo sapiens",
            "pathway_tags": "Development,Cytoskeleton,Dorsal_Ventral",
            "gravity_link": "Regulates roof plate development in the spinal cord; critical for dorsal-ventral patterning of the neural tube.",
            "spine_curvature_link": "The dreher mouse mutant (Lmx1a mutation) exhibits vertebral anomalies and scoliosis. (PMID: 11181829)",
            "priority_score": "85",
            "justification": "Essential for neural tube and vertebral patterning."
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
