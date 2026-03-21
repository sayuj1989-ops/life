import re
import os

def check_latex(filepath):
    print(f"Checking {filepath}...")
    with open(filepath, 'r') as f:
        content = f.read()

    # Check for unclosed environments
    env_begin = re.findall(r'\\begin{([^}]+)}', content)
    env_end = re.findall(r'\\end{([^}]+)}', content)

    begin_counts = {}
    end_counts = {}

    for env in env_begin:
        begin_counts[env] = begin_counts.get(env, 0) + 1
    for env in env_end:
        end_counts[env] = end_counts.get(env, 0) + 1

    errors = False
    for env, count in begin_counts.items():
        if count != end_counts.get(env, 0):
            print(f"ERROR: Mismatched \\begin{{{env}}} ({count}) and \\end{{{env}}} ({end_counts.get(env, 0)})")
            errors = True

    for env, count in end_counts.items():
        if count != begin_counts.get(env, 0):
             print(f"ERROR: Mismatched \\begin{{{env}}} ({begin_counts.get(env, 0)}) and \\end{{{env}}} ({count})")
             errors = True

    # Check for unclosed braces
    open_braces = content.count('{')
    close_braces = content.count('}')
    if open_braces != close_braces:
        print(f"ERROR: Mismatched braces. Open: {open_braces}, Close: {close_braces}")
        errors = True

    if not errors:
        print("OK: No basic LaTeX syntax errors found.")

check_latex('manuscript/sections/discussion.tex')
check_latex('manuscript/sections/figures.tex')
check_latex('manuscript/references.bib')
check_latex('manuscript/main.tex')
