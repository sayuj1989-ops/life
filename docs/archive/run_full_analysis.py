"""
run_full_analysis.py

Optimized script to run all manuscript analysis tasks in a single session
to avoid reloading the LLM multiple times.
"""

import sys
import os
from pathlib import Path
from llamaindex_analyzer import LlamaIndexAnalyzer
from langchain_manuscript_analyzer import ManuscriptAnalyzer as LangChainAnalyzer

def main():
    print("🚀 Starting Optimized Full Manuscript Analysis...")
    print("===============================================")

    # Ensure output directory exists
    os.makedirs("analysis", exist_ok=True)

    # Initialize LlamaIndex Analyzer (Loads LLM once)
    print("\n📚 Initializing LlamaIndex Analyzer (Loading Model)...")
    llama_analyzer = LlamaIndexAnalyzer()

    # 1. Structure Analysis
    print("\n🏗️  Running Structure Analysis...")
    structure_report = llama_analyzer.analyze_structure()
    Path("analysis/structure_report.txt").write_text(structure_report)
    print("   ✅ Saved to analysis/structure_report.txt")

    # 2. Cross-Reference Check
    print("\n🔗 Running Cross-Reference Check...")
    cross_ref_report = llama_analyzer.cross_reference_check()
    Path("analysis/cross_ref_report.txt").write_text(cross_ref_report)
    print("   ✅ Saved to analysis/cross_ref_report.txt")

    # 3. Consistency Checks
    print("\n🔬 Running Deep Consistency Checks...")
    terms = ["\\kappa", "I(s)", "counter-curvature", "information-elasticity"]
    consistency_results = []
    for term in terms:
        print(f"   - Checking: {term}")
        result = llama_analyzer.deep_consistency_check(term)
        consistency_results.append(f"### Term: {term}\n{result}\n")
    
    Path("analysis/consistency_report.txt").write_text("\n".join(consistency_results))
    print("   ✅ Saved to analysis/consistency_report.txt")

    # 4. Citation Gaps (Using LangChain Analyzer for variety/legacy support or switch to LlamaIndex if preferred)
    # Since we have LlamaIndex loaded, maybe we should use it? 
    # But LangChainAnalyzer has specific logic. Let's use LangChainAnalyzer but we need to be careful about memory.
    # If we load another LLM it might OOM.
    # Let's try to use LlamaIndex for citation gaps too if possible, or just use the LangChain one.
    # The LangChain one uses Instella via `instella_chat` which loads the model via `instella_client`.
    # `instella_client` uses a global `model` variable.
    # So both analyzers actually share the SAME model instance in memory if they import from `instella_client`!
    # So it IS safe to use both.
    
    print("\n📝 Running Citation Gap Analysis (LangChain)...")
    langchain_analyzer = LangChainAnalyzer() # This re-inits embeddings but reuses LLM
    
    sections = ["introduction", "theory", "methods", "results", "discussion"]
    citation_results = []
    for sec in sections:
        print(f"   - Section: {sec}")
        gaps = langchain_analyzer.find_citation_gaps(sec)
        if gaps:
            citation_results.append(f"### Section: {sec}\n" + "\n".join([f"- {g}" for g in gaps]) + "\n")
        else:
            citation_results.append(f"### Section: {sec}\nNo gaps found.\n")

    Path("analysis/citation_gaps.txt").write_text("\n".join(citation_results))
    print("   ✅ Saved to analysis/citation_gaps.txt")

    print("\n✅ All Analysis Complete!")

if __name__ == "__main__":
    main()
