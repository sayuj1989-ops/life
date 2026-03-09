import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    new_candidates = [
        {
            "gene_symbol": "BMP2",
            "uniprot_id": "P12643",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Bone,Mechanotransduction",
            "gravity_link": "Bone morphogenetic protein 2 expression is upregulated by mechanical strain and loading in osteoblasts.",
            "spine_curvature_link": "BMP signaling gradients dictate vertebral bone formation and asymmetry in spinal deformities. (PMID: 25484252)",
            "priority_score": "88",
            "justification": "Primary mechanosensitive bone growth factor essential for vertebral ossification."
        },
        {
            "gene_symbol": "ACTA2",
            "uniprot_id": "P62736",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Muscle,Mechanotransduction",
            "gravity_link": "Smooth muscle alpha-actin is a core component of cellular contractility and mechanosensing apparatus.",
            "spine_curvature_link": "Myofibroblast contractility mediated by ACTA2 contributes to the progressive tissue stiffening in scoliotic curves. (PMID: 32628468)",
            "priority_score": "85",
            "justification": "Core contractile filament for cellular tension generation."
        },
        {
            "gene_symbol": "FN1",
            "uniprot_id": "P02751",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Adhesion,Mechanotransduction",
            "gravity_link": "Fibronectin matrix assembly is strictly dependent on mechanical tension exerted by cells against their environment.",
            "spine_curvature_link": "Altered fibronectin deposition and matrix stiffness are found in the convex side of the scoliotic spine. (PMID: 17353683)",
            "priority_score": "90",
            "justification": "Primary tension-dependent ECM component bridging cells and physical environment."
        },
        {
            "gene_symbol": "ITGA1",
            "uniprot_id": "P56199",
            "organism": "Homo sapiens",
            "pathway_tags": "Adhesion,Mechanotransduction,ECM",
            "gravity_link": "Alpha-1 integrin binds collagen and laminin, transmitting mechanical load directly from ECM to the cytoskeleton.",
            "spine_curvature_link": "Integrin dysregulation impairs chondrocyte mechanotransduction, leading to abnormal growth plate loading in the spine. (PMID: 20560205)",
            "priority_score": "86",
            "justification": "Key integrin subunit for mechanotransduction of compressive forces in cartilage."
        },
        {
            "gene_symbol": "CTGF",
            "uniprot_id": "P29279",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Signaling,Mechanotransduction",
            "gravity_link": "Connective tissue growth factor (CCN2) is profoundly mechanosensitive and rapidly upregulated by stretch/tension.",
            "spine_curvature_link": "CTGF mediates stretch-induced proliferation of paraspinal muscle and ligament cells in asymmetrical spinal loading. (PMID: 21720235)",
            "priority_score": "87",
            "justification": "Matricellular protein directly activated by mechanical strain."
        },
        {
            "gene_symbol": "THBS1",
            "uniprot_id": "P07996",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction,Adhesion",
            "gravity_link": "Thrombospondin-1 senses and translates ECM tension, participating in transforming growth factor beta (TGF-beta) activation.",
            "spine_curvature_link": "Altered thrombospondin levels modify the structural integrity and mechanosensitivity of intervertebral discs. (PMID: 28919655)",
            "priority_score": "84",
            "justification": "Tension-activated regulator of TGF-beta in the extracellular matrix."
        },
        {
            "gene_symbol": "DSP",
            "uniprot_id": "P15924",
            "organism": "Homo sapiens",
            "pathway_tags": "Adhesion,Cytoskeleton,Mechanotransduction",
            "gravity_link": "Desmoplakin links the intermediate filament network to desmosomes, forming a continuous tissue-wide tension-bearing network.",
            "spine_curvature_link": "Mutations in intermediate filament networks decouple cellular mechanical responses, potentially contributing to loss of structural tone. (PMID: 30048689)",
            "priority_score": "82",
            "justification": "Essential linker for intermediate filament-based tissue integrity."
        },
        {
            "gene_symbol": "DNAI1",
            "uniprot_id": "Q9UI46",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Mechanotransduction,Motor_Protein",
            "gravity_link": "Dynein axonemal intermediate chain 1; critical for ciliary motility and flow sensing.",
            "spine_curvature_link": "Mutations cause Primary Ciliary Dyskinesia, strongly associated with idiopathic-like scoliosis due to lost CSF flow sensing. (PMID: 24391672)",
            "priority_score": "89",
            "justification": "Key structural motor component of flow-sensing cilia in the spine."
        },
        {
            "gene_symbol": "BBS4",
            "uniprot_id": "Q96RK4",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Scaffold,Mechanotransduction",
            "gravity_link": "Bardet-Biedl syndrome 4 protein localizes to the basal body and is required for primary cilia mechanosensory function.",
            "spine_curvature_link": "BBS mutations cause syndromic scoliosis due to impaired Wnt and Hedgehog signaling from the primary cilium. (PMID: 22695507)",
            "priority_score": "88",
            "justification": "Critical ciliary basal body component translating mechanics into signaling."
        },
        {
            "gene_symbol": "SP7",
            "uniprot_id": "Q8WI03",
            "organism": "Homo sapiens",
            "pathway_tags": "Transcription_Factor,Bone,Mechanotransduction",
            "gravity_link": "Osterix (SP7) is a master transcription factor for osteoblast differentiation, upregulated by mechanical loading.",
            "spine_curvature_link": "Mutations in SP7 cause Osteogenesis Imperfecta Type XII, which presents with severe spinal deformities and bone fragility. (PMID: 24706509)",
            "priority_score": "88",
            "justification": "Master transcriptional regulator of mechanically-driven bone formation."
        },
        {
            "gene_symbol": "DLX5",
            "uniprot_id": "P56178",
            "organism": "Homo sapiens",
            "pathway_tags": "Development,Bone,Transcription_Factor",
            "gravity_link": "Distal-less homeobox 5 acts downstream of mechanosensitive BMP pathways to regulate osteogenesis.",
            "spine_curvature_link": "Controls vertebral morphometry and chondrocyte hypertrophy; disruption causes axial skeleton defects. (PMID: 15159359)",
            "priority_score": "83",
            "justification": "Developmental regulator bridging mechanical cues to bone differentiation."
        },
        {
            "gene_symbol": "HOXA10",
            "uniprot_id": "P31260",
            "organism": "Homo sapiens",
            "pathway_tags": "Segmentation,Development,Transcription_Factor",
            "gravity_link": "Specifies lumbar vertebral identity, determining the morphology of the heavily loaded lower spine.",
            "spine_curvature_link": "Hox mutations cause homeotic transformations, altering spinal biomechanics and susceptibility to curvature. (PMID: 9550130)",
            "priority_score": "86",
            "justification": "Crucial for lumbar spine structural identity against gravity."
        },
        {
            "gene_symbol": "HOXD10",
            "uniprot_id": "P28358",
            "organism": "Homo sapiens",
            "pathway_tags": "Segmentation,Development,Transcription_Factor",
            "gravity_link": "Specifies lumbar and sacral vertebral identity, structuring the foundational weight-bearing segments of the spine.",
            "spine_curvature_link": "Loss of HOXD10 function alters the lumbo-sacral junction, a critical region for spinal stability and balance. (PMID: 9550130)",
            "priority_score": "85",
            "justification": "Determines the foundational weight-bearing structure of the spine."
        },
        {
            "gene_symbol": "CHSY1",
            "uniprot_id": "Q86X52",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Cartilage,Structure",
            "gravity_link": "Chondroitin sulfate synthase 1 synthesizes proteoglycans that provide the compressive resistance of the intervertebral discs.",
            "spine_curvature_link": "Mutations cause temtamy preaxial brachydactyly syndrome, accompanied by severe kyphoscoliosis due to disc and cartilage failure. (PMID: 21151125)",
            "priority_score": "89",
            "justification": "Synthesizes the primary water-binding, load-resisting molecules in discs."
        },
        {
            "gene_symbol": "TCOF1",
            "uniprot_id": "Q13428",
            "organism": "Homo sapiens",
            "pathway_tags": "Development,Transcription,Nucleus",
            "gravity_link": "Treacle protein mediates ribosomal DNA transcription, a heavily energy-dependent process sensitive to cellular metabolic supply.",
            "spine_curvature_link": "Treacher Collins syndrome features skeletal malformations; links to cellular stress responses in developing chondrocytes. (PMID: 15668252)",
            "priority_score": "80",
            "justification": "Links cellular metabolic capability to skeletal development."
        },
        {
            "gene_symbol": "NIPBL",
            "uniprot_id": "Q6NC26",
            "organism": "Homo sapiens",
            "pathway_tags": "Development,Transcription,Nucleus",
            "gravity_link": "Loads cohesin onto DNA, regulating global gene expression including mechanotransduction pathways during development.",
            "spine_curvature_link": "Mutations cause Cornelia de Lange syndrome, strongly associated with severe early-onset scoliosis and vertebral anomalies. (PMID: 15146185)",
            "priority_score": "87",
            "justification": "Master chromatin regulator driving developmental skeletal integrity."
        },
        {
            "gene_symbol": "SMC1A",
            "uniprot_id": "Q14683",
            "organism": "Homo sapiens",
            "pathway_tags": "Development,Transcription,Nucleus",
            "gravity_link": "Cohesin core component, mediating chromosome structure and influencing transcription of long mechanosensitive genes.",
            "spine_curvature_link": "SMC1A mutations lead to cohesinopathies with frequent skeletal and spinal deformities due to misregulated bone differentiation. (PMID: 16473305)",
            "priority_score": "85",
            "justification": "Cohesin component regulating large-scale structural gene expression."
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
