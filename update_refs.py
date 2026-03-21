import re

with open('manuscript/references.bib', 'r') as f:
    content = f.read()

# Replace any 2025 references to explicitly mark them as "in preparation"
# For example, replace `year = {2025},` with `year = {2025}, \n  note = {Manuscript in preparation},`
content = re.sub(r'(year\s*=\s*\{202[56]\},)', r'\1\n  note    = {Manuscript in preparation},', content)

with open('manuscript/references.bib', 'w') as f:
    f.write(content)
