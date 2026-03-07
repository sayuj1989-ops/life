import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "SMAD6",
            "uniprot_id": "O43541",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,BMP,Development",
            "gravity_link": "Inhibitory SMAD that acts as a negative regulator of BMP signaling, which is modulated by mechanical load in skeletal tissues.",
            "spine_curvature_link": "Mutations in SMAD6 are associated with craniosynostosis and radioulnar synostosis, with potential broader skeletal and spinal involvement via BMP regulation. (PMID: 32058062)",
            "priority_score": "82",
            "justification": "Negative regulator of the mechanically-responsive BMP pathway."
        },
        {
            "gene_symbol": "FOXA2",
            "uniprot_id": "Q9Y261",
            "organism": "Homo sapiens",
            "pathway_tags": "Transcription_Factor,Notochord,Development",
            "gravity_link": "Master regulator of notochord development (hydrostatic skeleton), crucial for establishing the embryonic gravity-resisting structure.",
            "spine_curvature_link": "Essential for midline patterning and notochord formation; defects lead to severe axial/spinal anomalies. (PMID: 9814704)",
            "priority_score": "88",
            "justification": "Fundamental transcription factor defining the primitive structural axis."
        },
        {
            "gene_symbol": "IFT81",
            "uniprot_id": "Q8WYA0",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Transport,Mechanotransduction",
            "gravity_link": "Core component of the IFT-B complex essential for ciliary assembly and mechanosensory fluid flow detection.",
            "spine_curvature_link": "Mutations cause Short-rib thoracic dysplasia (Jeune syndrome) with severe skeletal and thoracic/spinal deformities. (PMID: 24334766)",
            "priority_score": "85",
            "justification": "Ciliopathy gene with a direct link to skeletal dysplasia."
        },
        {
            "gene_symbol": "P0CG48",
            "uniprot_id": "P0CG48",
            "organism": "Homo sapiens",
            "pathway_tags": "Ubiquitin,Signaling",
            "gravity_link": "Ubiquitin-B (UBB); involved in protein degradation pathways activated during cellular mechanical stress and remodeling.",
            "spine_curvature_link": "Proteostasis failure is implicated in paraspinal muscle asymmetry and disc degeneration, though UBB mutations directly causing scoliosis are rare.",
            "priority_score": "75",
            "justification": "General marker of protein turnover under mechanical load."
        },
        {
            "gene_symbol": "GLI1",
            "uniprot_id": "P08151",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Development",
            "gravity_link": "Transcriptional effector of Hedgehog signaling, which is dependent on the primary cilium (a primary cellular mechanosensor).",
            "spine_curvature_link": "Hedgehog signaling is essential for somite patterning and vertebral development; mutations disrupt axial patterning. (PMID: 9814707)",
            "priority_score": "85",
            "justification": "Key transcriptional effector of the ciliary-Hedgehog signaling axis."
        },
        {
            "gene_symbol": "ROCK2",
            "uniprot_id": "O15146",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Signaling,Contraction",
            "gravity_link": "Rho-associated kinase; major driver of actomyosin contractility, generating the cellular forces required to resist gravity.",
            "spine_curvature_link": "Hyperactivity of the RhoA/ROCK pathway is observed in scoliotic models; modulation can rescue certain spinal defects. (PMID: 30065020 context)",
            "priority_score": "82",
            "justification": "Primary kinase executing the cytoskeletal response to mechanical tension."
        },
        {
            "gene_symbol": "BMP2",
            "uniprot_id": "P12643",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Bone,Mechanotransduction",
            "gravity_link": "Potent osteogenic factor whose expression and signaling are highly upregulated by mechanical loading in bone.",
            "spine_curvature_link": "Essential for vertebral ossification and growth; variants may influence spinal curve severity. (PMID: 15630473 context)",
            "priority_score": "85",
            "justification": "Major mechanosensitive growth factor driving spinal bone formation."
        },
        {
            "gene_symbol": "NOTCH3",
            "uniprot_id": "Q9UM47",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Segmentation,Development",
            "gravity_link": "Receptor in the Notch signaling pathway, which is sensitive to mechanical forces such as fluid shear stress.",
            "spine_curvature_link": "Mutations cause CADASIL; while primarily vascular, Notch signaling broadly regulates somite segmentation and vertebral boundaries. (PMID: 8900270)",
            "priority_score": "78",
            "justification": "Notch receptor contributing to segmentation and mechanosignaling."
        },
        {
            "gene_symbol": "IFT57",
            "uniprot_id": "Q9NWB7",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Transport,Mechanotransduction",
            "gravity_link": "Component of the IFT-B complex required for anterograde transport in primary cilia, enabling fluid flow/gravity sensing.",
            "spine_curvature_link": "Mutations cause orofaciodigital syndrome and skeletal anomalies due to defective ciliary signaling. (PMID: 25447326)",
            "priority_score": "85",
            "justification": "Ciliopathy gene essential for mechanosensory ciliary integrity."
        },
        {
            "gene_symbol": "CDC42EP3",
            "uniprot_id": "Q9UKI2",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Signaling,Adhesion",
            "gravity_link": "Effector of CDC42 that regulates actin filament reorganization and cell shape changes in response to mechanical stimuli.",
            "spine_curvature_link": "Involved in septin-mediated cytoskeletal regulation; crucial for cellular tensegrity and polarity in loaded tissues. (PMID: 26158630)",
            "priority_score": "80",
            "justification": "Cytoskeletal regulator coupling small GTPase signaling to mechanical structural changes."
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
