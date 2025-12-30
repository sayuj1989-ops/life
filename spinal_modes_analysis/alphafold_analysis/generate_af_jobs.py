"""
Generate AlphaFold Server Job Files (CORRECTED FORMAT)

Creates JSON job files in the correct AlphaFold Server format (list/array).
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict

def parse_fasta(fasta_file: str) -> List[Dict]:
    """Parse FASTA file and extract sequences"""
    sequences = []
    current_seq = None
    
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_seq:
                    sequences.append(current_seq)
                # Extract protein name from header
                parts = line.split('|')
                if len(parts) >= 2:
                    name = parts[1]
                    full_name = parts[2].split(' OS=')[0] if len(parts) > 2 else name
                else:
                    name = line[1:].split()[0]
                    full_name = name
                current_seq = {"id": name, "name": full_name, "sequence": ""}
            elif current_seq:
                current_seq["sequence"] += line
        
        if current_seq:
            sequences.append(current_seq)
    
    return sequences

def generate_alphafold_json(protein: Dict, output_dir: Path):
    """Generate AlphaFold Server JSON job file in CORRECT format"""
    # AlphaFold Server expects a LIST of jobs
    jobs = [
        {
            "name": f"{protein['id']}_{protein['name'][:30]}",  # Job name
            "modelSeeds": [1],
            "sequences": [
                {
                    "proteinChain": {
                        "sequence": protein["sequence"],
                        "count": 1
                    }
                }
            ]
        }
    ]
    
    output_file = output_dir / f"{protein['id']}.json"
    with open(output_file, 'w') as f:
        json.dump(jobs, f, indent=2)
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Generate AlphaFold Server job files (CORRECTED)")
    parser.add_argument("--sequences", default="alphafold_analysis/sequences.fasta",
                       help="Input FASTA file")
    parser.add_argument("--output-dir", default="alphafold_analysis/jobs",
                       help="Output directory for JSON files")
    
    args = parser.parse_args()
    
    sequences_path = Path(args.sequences)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔬 Generating AlphaFold Server Job Files (CORRECTED FORMAT)...")
    print("=" * 60)
    
    if not sequences_path.exists():
        print(f"❌ Sequences file not found: {sequences_path}")
        return
    
    proteins = parse_fasta(sequences_path)
    print(f"📊 Found {len(proteins)} proteins")
    
    for protein in proteins:
        output_file = generate_alphafold_json(protein, output_dir)
        print(f"✅ {protein['id']}: {output_file.name}")
    
    print(f"\n📁 Job files saved to: {output_dir}")
    print(f"\n📝 Format: AlphaFold Server expects JSON as LIST/ARRAY")
    print(f"✅ Files are now in correct format!")

if __name__ == "__main__":
    main()
