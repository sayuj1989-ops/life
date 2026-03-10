import csv

MASTER_FILE = "data/candidates_master.csv"

def main():
    new_candidates = [
        {
            "gene_symbol": "LOXL1",
            "uniprot_id": "Q08397",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction,Crosslinking",
            "gravity_link": "Lysyl oxidase-like 1; catalyzes the cross-linking of elastin and collagens, essential for tissue resilience against mechanical load.",
            "spine_curvature_link": "Loss alters ECM mechanics and structural stiffness; implicated in age-related and mechanical-load induced structural changes. (PMID: 15385959)",
            "priority_score": "86",
            "justification": "Essential for establishing mechanical stiffness and restoring elastic recoil in load-bearing connective tissues."
        },
        {
            "gene_symbol": "DPT",
            "uniprot_id": "Q07507",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction",
            "gravity_link": "Dermatopontin; interacts with fibronectin and TGF-beta, mediating extracellular matrix architecture in response to physical stress.",
            "spine_curvature_link": "Modulates collagen fibrillogenesis and ECM stiffness, factors critical for spinal stability. (PMID: 11110515)",
            "priority_score": "84",
            "justification": "Links collagen assembly to tension-dependent ECM architecture."
        },
        {
            "gene_symbol": "BMP2",
            "uniprot_id": "P12643",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Bone,Mechanotransduction",
            "gravity_link": "Bone morphogenetic protein 2; its expression is strictly regulated by mechanical loading and microgravity in osteoblasts.",
            "spine_curvature_link": "Drives osteoblast differentiation and spine ossification; asymmetrical expression implicated in scoliotic vertebral wedging. (PMID: 11520163)",
            "priority_score": "90",
            "justification": "Primary mechanosensitive driver of bone formation and structural remodeling."
        },
        {
            "gene_symbol": "FGF2",
            "uniprot_id": "P09038",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Mechanotransduction",
            "gravity_link": "Fibroblast growth factor 2; mechanically released from the ECM in response to loading to trigger repair and remodeling.",
            "spine_curvature_link": "Regulates chondrocyte proliferation in the growth plate; abnormal FGF signaling causes achondroplasia and spinal deformities. (PMID: 10452331)",
            "priority_score": "88",
            "justification": "A key load-released growth factor driving structural adaptation."
        },
        {
            "gene_symbol": "GLI1",
            "uniprot_id": "P08151",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Cilia",
            "gravity_link": "Effector of Hedgehog signaling, which is localized and modulated at the primary cilium (a critical mechanosensor).",
            "spine_curvature_link": "Essential for somite patterning and intervertebral disc formation; dysregulation alters vertebral segmentation. (PMID: 9006073)",
            "priority_score": "85",
            "justification": "Ciliary-dependent transcription factor driving spine development."
        },
        {
            "gene_symbol": "SMO",
            "uniprot_id": "Q99835",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Cilia",
            "gravity_link": "Smoothened; moves to the primary cilium upon activation, serving as the signal transducer for the mechanosensitive Hh pathway.",
            "spine_curvature_link": "Mutations disrupt somite formation and vertebral column integrity. (PMID: 12110168)",
            "priority_score": "86",
            "justification": "Obligate transducer of ciliary Hedgehog signaling."
        },
        {
            "gene_symbol": "HOXA1",
            "uniprot_id": "P49639",
            "organism": "Homo sapiens",
            "pathway_tags": "Somite,Development",
            "gravity_link": "HOX gene establishing the anterior-posterior axis, dictating where mechanical and gravity-resisting structures form.",
            "spine_curvature_link": "Sets up the cervical spine identity; disruptions lead to craniocervical anomalies and instability. (PMID: 16222686)",
            "priority_score": "82",
            "justification": "Master regulator of upper spine regional identity."
        },
        {
            "gene_symbol": "BAPX1",
            "uniprot_id": "P57073",
            "organism": "Homo sapiens",
            "pathway_tags": "Bone,Development,Somite",
            "gravity_link": "NKX3-2 (BAPX1); crucial for the differentiation of somitic sclerotome into mechanically functional axial skeleton.",
            "spine_curvature_link": "Essential for intervertebral disc and vertebral body formation; loss results in fused or malformed vertebrae. (PMID: 10508611)",
            "priority_score": "89",
            "justification": "Directly controls the fate of structural spine components."
        },
        {
            "gene_symbol": "TRPA1",
            "uniprot_id": "O75762",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Ion_Channel",
            "gravity_link": "Transient receptor potential ankyrin 1; mechanically gated ion channel that responds to stretch and cellular stress.",
            "spine_curvature_link": "Implicated in proprioceptive feedback and muscular tone control; potential role in sensing paraspinal mechanical asymmetry. (PMID: 14712238)",
            "priority_score": "84",
            "justification": "Candidate stretch sensor for muscular posture control."
        },
        {
            "gene_symbol": "ASIC1",
            "uniprot_id": "P78348",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Ion_Channel",
            "gravity_link": "Acid-sensing ion channel 1; involved in mechanosensation and touch, potentially contributing to load-sensing in the spine.",
            "spine_curvature_link": "Functions in bone remodeling and pain pathways; may transduce mechanical loading signals into osteocyte activity. (PMID: 19684112)",
            "priority_score": "82",
            "justification": "Modulates bone density in response to mechanical/chemical cues."
        },
        {
            "gene_symbol": "SANS",
            "uniprot_id": "Q495M9",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Mechanotransduction,Scaffold",
            "gravity_link": "USH1G (SANS); essential scaffold protein in hair cell stereocilia, anchoring the mechanotransduction complex for gravity sensing.",
            "spine_curvature_link": "Mutations cause Usher syndrome type 1G, characterized by profound deafness and vestibular areflexia (balance/posture defects). (PMID: 12592404)",
            "priority_score": "87",
            "justification": "Critical anchor for vestibular gravity sensors."
        },
        {
            "gene_symbol": "USH2A",
            "uniprot_id": "O75445",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Mechanotransduction,ECM",
            "gravity_link": "Usherin; forms the ankle links connecting stereocilia, essential for structural integrity under mechanical force.",
            "spine_curvature_link": "Mutations cause Usher syndrome type II; associated with mild vestibular dysfunction and potential postural compensation. (PMID: 9662395)",
            "priority_score": "85",
            "justification": "Structural component of mechanosensory cilia."
        },
        {
            "gene_symbol": "IFT20",
            "uniprot_id": "Q8IY31",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Trafficking,Mechanotransduction",
            "gravity_link": "Intraflagellar transport 20; couples the Golgi apparatus to the primary cilium, delivering mechanosensory receptors (like polycystin-2) to the ciliary membrane.",
            "spine_curvature_link": "Disruption of IFT causes severe skeletal dysplasias (e.g., Jeune syndrome) with spine deformities. (PMID: 16799062)",
            "priority_score": "88",
            "justification": "Essential for equipping cilia with mechanosensors."
        },
        {
            "gene_symbol": "IFT57",
            "uniprot_id": "Q9NWB7",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Trafficking",
            "gravity_link": "Component of the IFT complex B, necessary for anterograde transport and the assembly of the mechanical antenna (primary cilium).",
            "spine_curvature_link": "Mutations in IFT complex B proteins lead to short-rib polydactyly and other axial skeletal malformations. (PMID: 18025275)",
            "priority_score": "86",
            "justification": "Core builder of the primary cilium mechanosensor."
        },
        {
            "gene_symbol": "BBS4",
            "uniprot_id": "Q96VK1",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Trafficking",
            "gravity_link": "Bardet-Biedl syndrome 4; part of the BBSome complex mediating protein transport to the primary cilium, crucial for mechanosensor targeting.",
            "spine_curvature_link": "BBS features skeletal anomalies and obesity; defective ciliary signaling disrupts connective tissue homeostasis. (PMID: 11333244)",
            "priority_score": "85",
            "justification": "Key for ciliary receptor trafficking and function."
        },
        {
            "gene_symbol": "MKKS",
            "uniprot_id": "Q9NPJ1",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Chaperone",
            "gravity_link": "BBS6; a chaperonin required for the assembly of the BBSome, thereby regulating ciliary mechanosensory capacity.",
            "spine_curvature_link": "Mutations cause McKusick-Kaufman syndrome and BBS; impacts ciliary signaling necessary for proper musculoskeletal development. (PMID: 10835626)",
            "priority_score": "83",
            "justification": "Required for building functional mechanosensory cilia."
        },
        {
            "gene_symbol": "CEP41",
            "uniprot_id": "Q9BYV8",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Centrosome",
            "gravity_link": "Centrosomal protein 41; required for tubulin glutamylation, which stabilizes ciliary microtubules against mechanical stress.",
            "spine_curvature_link": "Mutations cause Joubert syndrome, marked by hypotonia, ataxia, and skeletal anomalies including scoliosis. (PMID: 22366787)",
            "priority_score": "86",
            "justification": "Stabilizes the structural core of the mechanosensory cilium."
        },
        {
            "gene_symbol": "WDR34",
            "uniprot_id": "Q96CG6",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Motor_Protein",
            "gravity_link": "Component of the dynein-2 complex (IFT retrograde transport), essential for ciliary turnover and remodeling during mechanoadaptation.",
            "spine_curvature_link": "Mutations cause short-rib thoracic dysplasia (Jeune syndrome) with profound vertebral defects. (PMID: 24183449)",
            "priority_score": "89",
            "justification": "Essential motor for ciliary mechanosensory function."
        },
        {
            "gene_symbol": "TUBG1",
            "uniprot_id": "P23258",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Centrosome",
            "gravity_link": "Gamma-tubulin; nucleates microtubules at the centrosome/basal body, anchoring the primary cilium and the cellular mechanical network.",
            "spine_curvature_link": "Mutations disrupt cortical development and microtubule organization, impacting cellular mechanics and potentially spine morphology. (PMID: 23260136)",
            "priority_score": "85",
            "justification": "Primary anchor for the cellular microtubule network."
        },
        {
            "gene_symbol": "NEDD1",
            "uniprot_id": "Q8NHV4",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Centrosome",
            "gravity_link": "Targets gamma-tubulin ring complexes to the centrosome, essential for establishing microtubule arrays that resist cellular deformation.",
            "spine_curvature_link": "Crucial for mitotic spindle formation and asymmetric cell division in tissue morphogenesis. (PMID: 16428859)",
            "priority_score": "82",
            "justification": "Organizer of the mechanoresistant microtubule network."
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
