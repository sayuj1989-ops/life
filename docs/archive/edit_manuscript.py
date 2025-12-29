"""
edit_manuscript.py

Streamlined manuscript editing using RAG-augmented rewriting.
Focuses on practical editing rather than exhaustive analysis.
"""

import sys
from pathlib import Path
from langchain_manuscript_analyzer import ManuscriptAnalyzer

def edit_section(analyzer, section_file: str, output_file: str):
    """Edit a single section with RAG augmentation"""
    section_path = Path(section_file)
    if not section_path.exists():
        print(f"❌ File not found: {section_file}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Editing: {section_path.name}")
    print(f"{'='*60}")
    
    content = section_path.read_text()
    section_name = section_path.stem
    
    print(f"📝 Running RAG-augmented rewrite...")
    rewritten = analyzer.rag_augmented_rewrite(
        section_name=section_name,
        section_content=content,
        style="Nature Communications"
    )
    
    output_path = Path(output_file)
    output_path.write_text(rewritten)
    print(f"✅ Saved to: {output_file}")
    return True

def main():
    print("🚀 Manuscript Editing with RAG")
    print("=" * 60)
    
    # Initialize analyzer (loads embeddings and vector store)
    print("\n📚 Initializing RAG Analyzer...")
    analyzer = ManuscriptAnalyzer()
    
    # Define sections to edit
    sections = [
        ("life/manuscript/sections/introduction.tex", "edited_sections/introduction_v2.tex"),
        ("life/manuscript/sections/theory.tex", "edited_sections/theory_v2.tex"),
        ("life/manuscript/sections/methods.tex", "edited_sections/methods_v2.tex"),
        ("life/manuscript/sections/results.tex", "edited_sections/results_v2.tex"),
        ("life/manuscript/sections/discussion.tex", "edited_sections/discussion_v2.tex"),
        ("life/manuscript/sections/conclusion.tex", "edited_sections/conclusion_v2.tex"),
    ]
    
    # Create output directory
    Path("edited_sections").mkdir(exist_ok=True)
    
    # Edit each section
    for section_file, output_file in sections:
        if not edit_section(analyzer, section_file, output_file):
            print(f"⚠️  Skipping {section_file}")
            continue
    
    print("\n" + "="*60)
    print("✅ All sections edited!")
    print("📁 Check edited_sections/ directory for results")

if __name__ == "__main__":
    main()
