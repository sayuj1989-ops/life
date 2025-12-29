import sys
import os
from instella_tasks import reviewer_pass, read_text_file

def review_file(input_path, output_path, title):
    print(f"Reviewing {input_path} as '{title}'...")
    content = read_text_file(input_path)
    review = reviewer_pass(title, content)
    
    with open(output_path, "a") as f:
        f.write(f"\n\n## Review: {title}\n\n")
        f.write(review)
    print(f"Appended review to {output_path}")

if __name__ == "__main__":
    # Usage: python reviewer_pass_driver.py <input_file> <output_report_file> <section_title>
    if len(sys.argv) < 4:
        print("Usage: python reviewer_pass_driver.py <input_file> <output_report_file> <section_title>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    title = sys.argv[3]
    
    review_file(input_file, output_file, title)
