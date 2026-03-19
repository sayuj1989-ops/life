import re
import sys
import glob

def check_latex():
    # Read the bibliography file to get all defined keys
    bib_keys = set()
    try:
        with open('manuscript/references.bib', 'r') as f:
            bib_content = f.read()
            # Extract keys from @article{key, @book{key, etc.
            matches = re.findall(r'@\w+\{([^,]+),', bib_content)
            bib_keys.update([m.strip() for m in matches])
    except FileNotFoundError:
        print("Error: references.bib not found.")
        sys.exit(1)

    print(f"Found {len(bib_keys)} entries in references.bib")

    # Check all .tex files for \cite{} commands
    tex_files = glob.glob('manuscript/**/*.tex', recursive=True)
    missing_refs = []

    for tf in tex_files:
        with open(tf, 'r') as f:
            content = f.read()

            # Find \cite{key1, key2}
            cites = re.findall(r'\\cite\{([^\}]+)\}', content)
            for cite in cites:
                # Handle comma separated lists
                keys = [k.strip() for k in cite.split(',')]
                for key in keys:
                    if key not in bib_keys:
                        missing_refs.append((tf, key))

    if missing_refs:
        print("ERROR: Unresolved references found:")
        for tf, key in missing_refs:
            print(f"  {tf}: {key}")
        sys.exit(1)

    print("SUCCESS: All citations are resolved!")

if __name__ == '__main__':
    check_latex()
