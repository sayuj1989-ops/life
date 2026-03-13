import re
from collections import OrderedDict

def deduplicate_bib(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    entries = re.split(r'\n(?=@)', content)

    unique_entries = OrderedDict()
    for entry in entries:
        if not entry.strip():
            continue

        match = re.search(r'@\w+\{([^,]+),', entry)
        if match:
            key = match.group(1).strip()
            if key not in unique_entries:
                unique_entries[key] = entry
        else:
            if 'header' not in unique_entries:
                unique_entries['header'] = entry
            else:
                unique_entries['header'] += '\n' + entry

    with open(filepath, 'w') as f:
        for val in unique_entries.values():
            f.write(val + '\n')

deduplicate_bib('manuscript/references.bib')
