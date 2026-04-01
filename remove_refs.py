import re

with open('manuscript/references.bib', 'r') as f:
    content = f.read()

# Remove Tosi_2026 entry
content = re.sub(r'@article\{Tosi_2026,[\s\S]*?\}\n', '', content)

# Remove Qin_2025 entry
content = re.sub(r'@article\{Qin_2025,[\s\S]*?\}\n', '', content)

with open('manuscript/references.bib', 'w') as f:
    f.write(content)
