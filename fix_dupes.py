import re

with open('manuscript/references.bib', 'r') as f:
    content = f.read()

# Find the first index of the duplicated section added in the previous step
dupe_start = content.rfind("@article{bastien2013unifying,")
if dupe_start != -1:
    content = content[:dupe_start]

with open('manuscript/references.bib', 'w') as f:
    f.write(content)
