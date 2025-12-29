"""
Fix Invalid PDB Files
Detects and removes invalid PDB files (error responses, empty files, etc.)
"""

from pathlib import Path
import json

def is_valid_pdb(pdb_file: Path) -> bool:
    """Check if a file is a valid PDB structure"""
    try:
        # Check file size
        if pdb_file.stat().st_size < 100:
            return False
        
        # Check first line
        with open(pdb_file, 'r') as f:
            first_line = f.readline().strip()
            
            # XML error responses
            if first_line.startswith('<?xml') or first_line.startswith('<Error'):
                return False
            
            # Should start with PDB header keywords
            valid_starters = ['HEADER', 'TITLE', 'REMARK', 'ATOM', 'HETATM', 'MODEL']
            if not any(first_line.startswith(s) for s in valid_starters):
                # Might still be valid if it's a comment or empty line
                # Check if there are any ATOM records
                f.seek(0)
                has_atom = False
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    if 'ATOM' in chunk or 'HETATM' in chunk:
                        has_atom = True
                        break
                if not has_atom:
                    return False
        
        return True
    except Exception as e:
        print(f"   ⚠️  Error checking {pdb_file.name}: {e}")
        return False

def main():
    predictions_dir = Path("alphafold_analysis/predictions")
    
    print("🔍 Checking PDB Files for Validity")
    print("=" * 70)
    print()
    
    invalid_files = []
    valid_files = []
    
    for pdb_file in predictions_dir.glob("*.pdb"):
        if is_valid_pdb(pdb_file):
            valid_files.append(pdb_file.name)
        else:
            invalid_files.append(pdb_file)
            print(f"❌ Invalid: {pdb_file.name}")
    
    print()
    print("=" * 70)
    print(f"✅ Valid PDB files: {len(valid_files)}")
    print(f"❌ Invalid PDB files: {len(invalid_files)}")
    
    if invalid_files:
        print("\n💡 Invalid files detected:")
        for f in invalid_files:
            print(f"   - {f.name}")
        
        print("\n❓ Options:")
        print("   1. Delete invalid files (recommended)")
        print("   2. Keep for investigation")
        
        response = input("\nDelete invalid files? (y/n): ").strip().lower()
        if response == 'y':
            for f in invalid_files:
                f.unlink()
                print(f"   🗑️  Deleted: {f.name}")
            print(f"\n✅ Removed {len(invalid_files)} invalid files")
        else:
            print("\n📝 Keeping invalid files for investigation")
    
    # Save summary
    summary = {
        "valid": valid_files,
        "invalid": [f.name for f in invalid_files],
        "total_valid": len(valid_files),
        "total_invalid": len(invalid_files),
    }
    
    output_file = Path("alphafold_analysis/metadata/pdb_validation.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📝 Summary saved: {output_file}")

if __name__ == "__main__":
    main()





