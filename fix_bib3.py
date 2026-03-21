import re

with open('manuscript/references.bib', 'r') as f:
    text = f.read()

# Make lowercase key comparisons
entries = re.split(r'\n(?=@)', text)
unique_entries = {}
for entry in entries:
    if not entry.strip(): continue
    match = re.search(r'@\w+\{([^,]+),', entry)
    if match:
        key = match.group(1).strip().lower() # LOWERCASE key comparison
        if key not in unique_entries:
            unique_entries[key] = entry
    else:
        unique_entries[len(unique_entries)] = entry

with open('manuscript/references.bib', 'w') as f:
    f.write('\n'.join(str(v) for v in unique_entries.values()) + '\n')
