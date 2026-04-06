import time
import os

def parse_pdb_plddt_old(pdb_path):
    plddts = {}
    with open(pdb_path) as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                resnum = int(line[22:26].strip())
                bfactor = float(line[60:66].strip())
                plddts[resnum] = bfactor
    return plddts

def parse_pdb_plddt_new(pdb_path):
    plddts = {}
    with open(pdb_path, 'r') as f:
        # PDB lines are fixed format. We can just check specific characters.
        for line in f:
            if line.startswith('ATOM') and line[13:15] == 'CA':
                # Use slicing and int/float directly, strip is slow if called millions of times, but we can do it
                resnum = int(line[22:26])
                bfactor = float(line[60:66])
                plddts[resnum] = bfactor
    return plddts

def parse_pdb_plddt_newer(pdb_path):
    plddts = {}
    with open(pdb_path, 'r') as f:
        for line in f:
            # First check if it's ATOM
            if line[0:4] == 'ATOM':
                # Then check CA
                if line[13:15] == 'CA':
                    plddts[int(line[22:26])] = float(line[60:66])
    return plddts

pdb_files = [os.path.join("data/af_cache", f) for f in os.listdir("data/af_cache") if f.endswith(".pdb")]

if pdb_files:
    test_file = pdb_files[0]

    t0 = time.time()
    for _ in range(50):
        p1 = parse_pdb_plddt_old(test_file)
    print(f"Old: {time.time() - t0:.3f}s")

    t0 = time.time()
    for _ in range(50):
        p2 = parse_pdb_plddt_new(test_file)
    print(f"New: {time.time() - t0:.3f}s")

    t0 = time.time()
    for _ in range(50):
        p3 = parse_pdb_plddt_newer(test_file)
    print(f"Newer: {time.time() - t0:.3f}s")

    print("Same?", p1 == p3)
