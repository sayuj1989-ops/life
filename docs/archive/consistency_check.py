import os
from instella_client import instella_chat
from instella_tasks import read_text_file

def run_consistency_check(manuscript_dir, output_file):
    print("Running consistency check...")
    
    # Concatenate key sections
    sections = ["abstract.tex", "introduction.tex", "theory.tex", "methods.tex", "results.tex", "discussion.tex", "conclusion.tex"]
    full_text = ""
    for sec in sections:
        path = os.path.join(manuscript_dir, "sections", sec)
        if os.path.exists(path):
            full_text += f"\n\n--- {sec} ---\n\n"
            full_text += read_text_file(path)
            
    system_prompt = (
        "You are a meticulous scientific editor. Your job is to check the manuscript for internal consistency. "
        "Focus on: 1) Defined symbols (e.g. is I(s) defined before use?), 2) Consistent terminology (e.g. 'counter-curvature' vs 'countercurvature'), "
        "3) Agreement between Theory equations and Results figures."
    )
    
    user_msg = {
        "role": "user",
        "content": (
            f"Analyze the following manuscript text for consistency issues.\n"
            f"Provide a list of: \n"
            f"1. Undefined symbols.\n"
            f"2. Terminology inconsistencies.\n"
            f"3. Logic gaps between Theory and Results.\n"
            f"4. A suggested 3-4 sentence 'Core Narrative' summary.\n\n"
            f"Text:\n{full_text[:100000]}" # Truncate to be safe, though model is 128k
        )
    }
    
    report = instella_chat(system_prompt, [user_msg], max_new_tokens=4096, temperature=0.2)
    
    with open(output_file, "w") as f:
        f.write("# Consistency Check Report\n\n")
        f.write(report)
    print(f"Saved consistency report to {output_file}")

if __name__ == "__main__":
    run_consistency_check("life/manuscript", "CONSISTENCY_REPORT.md")
