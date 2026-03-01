import re

with open('manuscript/submission_manuscript.tex', 'r') as f:
    text = f.read()

# Extract abstract
match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', text, re.DOTALL)
if match:
    abstract_text = match.group(1).strip()
    words = len(abstract_text.split())
    print(f"Abstract word count: {words}")
else:
    print("Abstract not found.")
