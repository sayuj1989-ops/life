import os
import re

TARGET_DIR = "/Users/mac/LIFE/countercurvature"

def fix_file_equations(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # regex for $$ block
    # Note: re.DOTALL makes . match newlines
    pattern = r'(\$\$)(.*?)(\$\$)'
    
    def replacer(match):
        raw_eq = match.group(2)
        
        # 1. Remove \label{...}
        cleaned_eq = re.sub(r'\\label\{[^}]+\}', '', raw_eq)
        
        # 2. Check for alignment characters '&' and newlines '\\'
        if '&' in cleaned_eq and '\\\\' in cleaned_eq:
            # It's an aligned block. Wrap in aligned if not already
            if 'begin{aligned}' not in cleaned_eq:
                cleaned_eq = f"\n\\begin{{aligned}}{cleaned_eq}\n\\end{{aligned}}\n"
        
        # 3. Clean up generic whitespace
        lines = [l.strip() for l in cleaned_eq.split('\n') if l.strip()]
        final_eq = '\n'.join(lines)
        
        # 4. Wrap back in $$
        return f"$$\n{final_eq}\n$$"

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Fixed {filepath}")

files = [f for f in os.listdir(TARGET_DIR) if f.endswith('.md')]
for f in files:
    fix_file_equations(os.path.join(TARGET_DIR, f))
