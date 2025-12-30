import urllib.request
import json
import os
import sys

PROTEINS = {
    "YAP1": "P46937",
    "FOXO3": "O43524",
    "SIRT1": "Q96EB6",
    "Klotho": "Q9UEF7",
    "PGC1A": "Q9UBK2"
}

OUTPUT_DIR = "alphafold_analysis/predictions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_pdb(name, uniprot_id):
    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    print(f"Fetching metadata for {name} ({uniprot_id})...")
    
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            
        if not data:
            print(f"No data found for {name}")
            return
            
        # Get the first entry (usually canonical)
        entry = data[0]
        pdb_url = entry.get('pdbUrl')
        
        if not pdb_url:
            print(f"No PDB URL for {name}")
            return
            
        print(f"Downloading PDB from {pdb_url}...")
        dest_path = os.path.join(OUTPUT_DIR, f"{name}.pdb")
        
        with urllib.request.urlopen(pdb_url) as pdb_response, open(dest_path, 'wb') as f:
            f.write(pdb_response.read())
            
        print(f"Saved to {dest_path}")
        
    except Exception as e:
        print(f"Error fetching {name}: {e}")

if __name__ == "__main__":
    for name, uid in PROTEINS.items():
        fetch_pdb(name, uid)
