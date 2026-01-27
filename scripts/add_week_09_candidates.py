import csv
import os

MASTER_FILE = "data/candidates_master.csv"

new_candidates = [
    {
        "gene_symbol": "ROBO3",
        "uniprot_id": "Q96MS0",
        "organism": "Homo sapiens",
        "pathway_tags": "Axon_Guidance,Proprioception",
        "gravity_link": "Essential for hindbrain axon crossing in somatosensory/proprioceptive pathways.",
        "spine_curvature_link": "Mutations cause Horizontal Gaze Palsy with Progressive Scoliosis (HGPPS). (DOI: 10.1038/ng1295)",
        "priority_score": 85,
        "justification": "Direct link between neural circuit formation (proprioception) and spinal curvature."
    },
    {
        "gene_symbol": "CNTNAP2",
        "uniprot_id": "Q9UHC6",
        "organism": "Homo sapiens",
        "pathway_tags": "Adhesion,Axon_Guidance",
        "gravity_link": "Interacts with L1 and Robo; involved in neural circuit formation (proprioception).",
        "spine_curvature_link": "GWAS association with Adolescent Idiopathic Scoliosis. (PubMed: 21216876)",
        "priority_score": 82,
        "justification": "Genetic association linking neural adhesion to AIS."
    },
    {
        "gene_symbol": "TTLL11",
        "uniprot_id": "Q8NHH1",
        "organism": "Homo sapiens",
        "pathway_tags": "Cytoskeleton,Cilia",
        "gravity_link": "Polyglutamylase essential for ciliary microtubule stability (gravity sensor structure).",
        "spine_curvature_link": "Variants associated with AIS; linked to ciliary defects. (PMC11470263)",
        "priority_score": 82,
        "justification": "Cytoskeletal modifier linked to ciliary stability and scoliosis."
    },
    {
        "gene_symbol": "TOR1A",
        "uniprot_id": "O14656",
        "organism": "Homo sapiens",
        "pathway_tags": "Nucleus,ER,Mechanotransduction",
        "gravity_link": "Interacts with LINC complex (Sun1/2, Lamin); essential for nuclear-cytoskeletal coupling.",
        "spine_curvature_link": "Mutations cause DYT1 Dystonia, frequently associated with scoliosis. (DOI: 10.1038/ng0997-101)",
        "priority_score": 85,
        "justification": "Nuclear envelope protein linking muscle tone (dystonia) to spinal curvature."
    },
    {
        "gene_symbol": "ARL13B",
        "uniprot_id": "Q3SXY8",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Signaling",
        "gravity_link": "Regulates ciliary signaling and structure; essential for sensing flow/gravity.",
        "spine_curvature_link": "Mutations cause Joubert Syndrome, characterized by cerebellar defects and scoliosis. (DOI: 10.1038/ng.180)",
        "priority_score": 88,
        "justification": "Key regulator of ciliary signaling with strong syndromic scoliosis link."
    },
    {
        "gene_symbol": "ADAMTS10",
        "uniprot_id": "Q9H324",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Mechanotransduction",
        "gravity_link": "Interacts with Fibrillin-1 (FBN1); essential for microfibril assembly and tissue stiffness.",
        "spine_curvature_link": "Mutations cause Weill-Marchesani syndrome (short stature, stiff joints, scoliosis). (DOI: 10.1086/423900)",
        "priority_score": 85,
        "justification": "Fibrillin-interacting protease essential for ECM mechanics."
    },
    {
        "gene_symbol": "PTHLH",
        "uniprot_id": "P12272",
        "organism": "Homo sapiens",
        "pathway_tags": "Growth_Plate,Signaling",
        "gravity_link": "PTHrP regulates chondrocyte differentiation under mechanical load (IHH loop).",
        "spine_curvature_link": "Essential for vertebral growth; disruption causes brachydactyly and spinal anomalies. (UniProt)",
        "priority_score": 82,
        "justification": "Central regulator of growth plate pacing under mechanical constraints."
    },
    {
        "gene_symbol": "STAT3",
        "uniprot_id": "P40763",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Bone",
        "gravity_link": "Mechanosensitive signaling hub; regulates osteoblast differentiation.",
        "spine_curvature_link": "Dominant-negative mutations cause Hyper-IgE (Job's) syndrome, with high scoliosis prevalence. (DOI: 10.1056/NEJMoa073618)",
        "priority_score": 82,
        "justification": "Signaling pathway linking immune dysfunction to severe skeletal/spinal defects."
    },
    {
        "gene_symbol": "CCDC39",
        "uniprot_id": "Q9UFE4",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Motility",
        "gravity_link": "Essential for dynein arm assembly in motile cilia (flow sensors).",
        "spine_curvature_link": "Mutations cause Primary Ciliary Dyskinesia (PCD) with situs inversus and scoliosis. (DOI: 10.1038/ng.718)",
        "priority_score": 88,
        "justification": "Essential component of the ciliary motility machinery linked to curvature."
    },
    {
        "gene_symbol": "POC1B",
        "uniprot_id": "Q8TC44",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Structure",
        "gravity_link": "Essential for basal body and ciliary integrity.",
        "spine_curvature_link": "Mutations cause PCD; linked to retinal degeneration and skeletal anomalies. (DOI: 10.1016/j.ajhg.2014.06.010)",
        "priority_score": 85,
        "justification": "Structural component of cilia essential for function."
    },
    {
        "gene_symbol": "CCDC103",
        "uniprot_id": "Q9Y2V0",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Motility",
        "gravity_link": "Dynein attachment factor essential for ciliary motility.",
        "spine_curvature_link": "Mutations cause PCD with situs inversus and scoliosis. (DOI: 10.1016/j.ajhg.2012.05.003)",
        "priority_score": 88,
        "justification": "Key factor for dynein arm attachment in motile cilia."
    },
    {
        "gene_symbol": "LTBP3",
        "uniprot_id": "Q9NS15",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Signaling",
        "gravity_link": "Regulates TGF-beta bioavailability in bone and ECM.",
        "spine_curvature_link": "Loss causes dental and spinal defects (scoliosis/kyphosis) in mice and humans. (PubMed: 10655536)",
        "priority_score": 85,
        "justification": "Regulator of TGF-beta signaling critical for spinal ossification."
    },
    {
        "gene_symbol": "SLC39A14",
        "uniprot_id": "Q15043",
        "organism": "Homo sapiens",
        "pathway_tags": "Ion_Transport,Bone,Mechanotransduction",
        "gravity_link": "Transports Manganese (Mn2+), required for integrin activation and mechanotransduction.",
        "spine_curvature_link": "Mutations cause severe progressive scoliosis and hyperostosis. (PubMed: 27153396)",
        "priority_score": 85,
        "justification": "Transporter providing co-factors for integrin-mediated gravity sensing."
    },
    {
        "gene_symbol": "KAT6B",
        "uniprot_id": "Q8WYB5",
        "organism": "Homo sapiens",
        "pathway_tags": "Chromatin,Development",
        "gravity_link": "Histone acetyltransferase regulating developmental gene expression.",
        "spine_curvature_link": "Mutations cause Genitopatellar and Ohdo syndromes, featuring severe scoliosis. (DOI: 10.1016/j.ajhg.2011.10.008)",
        "priority_score": 82,
        "justification": "Epigenetic regulator of vertebral development."
    },
    {
        "gene_symbol": "DYM",
        "uniprot_id": "Q7RTS9",
        "organism": "Homo sapiens",
        "pathway_tags": "Golgi,ECM,Transport",
        "gravity_link": "Regulates Golgi organization and ECM secretion.",
        "spine_curvature_link": "Mutations cause Dyggve-Melchior-Clausen disease (spondyloepimetaphyseal dysplasia). (DOI: 10.1086/367920)",
        "priority_score": 82,
        "justification": "Golgi protein affecting ECM quality and vertebral shape."
    },
    {
        "gene_symbol": "EVC",
        "uniprot_id": "P57679",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Hedgehog",
        "gravity_link": "Localizes to base of cilia; regulates Hedgehog signaling.",
        "spine_curvature_link": "Mutations cause Ellis-van Creveld syndrome (dwarfism, polydactyly, scoliosis). (DOI: 10.1038/73254)",
        "priority_score": 85,
        "justification": "Ciliary basal body protein regulating Hedgehog signaling."
    },
    {
        "gene_symbol": "EVC2",
        "uniprot_id": "Q86UK5",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Hedgehog",
        "gravity_link": "Forms complex with EVC at cilia base.",
        "spine_curvature_link": "Mutations cause Ellis-van Creveld syndrome and Weyers acrofacial dysostosis. (DOI: 10.1086/373931)",
        "priority_score": 85,
        "justification": "Partner of EVC in ciliary signaling."
    },
    {
        "gene_symbol": "IFT122",
        "uniprot_id": "Q9HBG6",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Transport",
        "gravity_link": "Component of IFT complex A; essential for retrograde ciliary transport.",
        "spine_curvature_link": "Mutations cause Sensenbrenner syndrome (Cranioectodermal dysplasia) with skeletal defects. (DOI: 10.1016/j.ajhg.2010.04.017)",
        "priority_score": 85,
        "justification": "IFT complex component essential for ciliary maintenance."
    },
    {
        "gene_symbol": "NEK1",
        "uniprot_id": "Q96PY6",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Signaling,Kinase",
        "gravity_link": "Kinase involved in ciliogenesis and DNA damage response.",
        "spine_curvature_link": "Mutations cause Short-Rib Polydactyly Syndrome (fatal skeletal dysplasia). (DOI: 10.1016/j.ajhg.2010.12.003)",
        "priority_score": 82,
        "justification": "Ciliary kinase regulating skeletal formation."
    },
    {
        "gene_symbol": "NEK8",
        "uniprot_id": "Q86SG6",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Signaling,Kinase",
        "gravity_link": "Localizes to cilia; regulates ciliary stability and signaling.",
        "spine_curvature_link": "Mutations cause Nephronophthisis with skeletal and spinal anomalies. (DOI: 10.1038/ng.258)",
        "priority_score": 82,
        "justification": "Ciliary kinase linked to fibrocystic/skeletal disease."
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
