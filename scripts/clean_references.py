
import re
from pathlib import Path

def main():
    bib_path = Path("manuscript/references.bib")
    if not bib_path.exists():
        print(f"Error: {bib_path} not found.")
        return

    with open(bib_path, 'r') as f:
        content = f.read()

    # Split into entries
    # Assume entries start with @
    entries = re.split(r'\n@', content)

    cleaned_entries = []
    removed_count = 0

    # Handle first entry split artifact
    if entries[0].strip() == "":
        entries = entries[1:]
    else:
        # If file doesn't start with newline@, just process.
        # But typically bib files do.
        # Actually split removes the delimiter. So we need to add @ back.
        pass

    # Better approach: Iterate lines, identify blocks.
    # But regex split is okay if we re-add @.

    # Let's try a line-based parser to be safer with comments.

    lines = content.splitlines()
    new_lines = []
    current_entry = []
    skip_entry = False

    for line in lines:
        if line.strip().startswith("@"):
            # Start of new entry
            if current_entry:
                if not skip_entry:
                    new_lines.extend(current_entry)

            current_entry = [line]
            skip_entry = False
        else:
            current_entry.append(line)
            if "year" in line.lower() and "2026" in line:
                skip_entry = True
                removed_count += 1
                # Check if it's the specific forbidden ones
                if "mader" in "".join(current_entry).lower() or "gerwin" in "".join(current_entry).lower():
                     print(f"Removing specific forbidden ref: {''.join(current_entry)[:50]}...")

    # Flush last entry
    if current_entry and not skip_entry:
        new_lines.extend(current_entry)

    with open(bib_path, 'w') as f:
        f.write("\n".join(new_lines))

    print(f"Removed {removed_count} entries with year 2026.")

if __name__ == "__main__":
    main()
