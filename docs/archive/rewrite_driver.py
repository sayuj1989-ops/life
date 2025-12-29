import sys
import os
from instella_tasks import rewrite_section, read_text_file

def rewrite_file(input_path, output_path, title, style="Nature Communications"):
    print(f"Rewriting {input_path} as '{title}'...")
    content = read_text_file(input_path)
    rewritten = rewrite_section(title, content, style=style)
    
    with open(output_path, "w") as f:
        f.write(rewritten)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python rewrite_driver.py <input_file> <output_file> <title> [style]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    title = sys.argv[3]
    style = sys.argv[4] if len(sys.argv) > 4 else "Nature Communications"
    
    rewrite_file(input_file, output_file, title, style)
