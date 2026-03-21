import re

with open('manuscript/references.bib', 'r') as f:
    text = f.read()

# Fix duplicates
# Find all bib entries
entries = re.split(r'\n(?=@)', text)
unique_entries = {}
for entry in entries:
    if not entry.strip(): continue
    match = re.search(r'@\w+\{([^,]+),', entry)
    if match:
        key = match.group(1).strip()
        # if the key is already in unique_entries, we skip this to avoid duplicates
        if key not in unique_entries:
            unique_entries[key] = entry
    else:
        # if not match, just keep it (e.g. comments)
        unique_entries[len(unique_entries)] = entry

with open('manuscript/references.bib', 'w') as f:
    f.write('\n'.join(str(v) for v in unique_entries.values()) + '\n')
