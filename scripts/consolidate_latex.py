
import re
import os

def consolidate_tex(main_file_path, output_file_path):
    print(f"Consolidating {main_file_path} into {output_file_path}...")

    with open(main_file_path, 'r') as f:
        lines = f.readlines()

    consolidated_lines = []

    for line in lines:
        # Check for \input{...}
        match = re.search(r'^\s*\\input\{([^}]+)\}', line)
        comment_match = re.search(r'^\s*%.*\\input\{', line)

        if match and not comment_match:
            input_path = match.group(1)
            # Ensure extension .tex
            if not input_path.endswith('.tex'):
                input_path += '.tex'

            full_input_path = os.path.join(os.path.dirname(main_file_path), input_path)

            if os.path.exists(full_input_path):
                print(f"  Including {input_path}")
                consolidated_lines.append(f"% START INPUT: {input_path}\n")
                with open(full_input_path, 'r') as input_f:
                    consolidated_lines.extend(input_f.readlines())
                consolidated_lines.append(f"\n% END INPUT: {input_path}\n")
            else:
                print(f"  WARNING: File {full_input_path} not found. Keeping original line.")
                consolidated_lines.append(line)
        else:
            consolidated_lines.append(line)

    with open(output_file_path, 'w') as f:
        f.writelines(consolidated_lines)

    print(f"✅ Created {output_file_path}")

if __name__ == "__main__":
    consolidate_tex("manuscript/main.tex", "manuscript/submission_jor_spine.tex")
