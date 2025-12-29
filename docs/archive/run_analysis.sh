#!/bin/bash

# run_analysis.sh
# Orchestrate full manuscript analysis using LlamaIndex and LangChain

echo "🚀 Starting Full Manuscript Analysis..."
echo "======================================="

# 1. Indexing
echo -e "\n📚 Step 1: Indexing Manuscript (LlamaIndex)..."
./.venv/bin/python3 llamaindex_analyzer.py --action reindex

# 2. Structure Analysis
echo -e "\n🏗️  Step 2: Analyzing Structure..."
./.venv/bin/python3 llamaindex_analyzer.py --action structure > analysis/structure_report.txt
cat analysis/structure_report.txt

# 3. Cross-Reference Check
echo -e "\n🔗 Step 3: Checking Cross-References..."
./.venv/bin/python3 llamaindex_analyzer.py --action cross-ref > analysis/cross_ref_report.txt
cat analysis/cross_ref_report.txt

# 4. Consistency Checks (Key Terms)
echo -e "\n🔬 Step 4: Deep Consistency Checks..."
TERMS=("\\kappa" "I(s)" "counter-curvature" "information-elasticity")
for term in "${TERMS[@]}"; do
    echo "   - Checking: $term"
    ./.venv/bin/python3 llamaindex_analyzer.py --action consistency --topic "$term" >> analysis/consistency_report.txt
done

# 5. Citation Gaps (LangChain)
echo -e "\n📝 Step 5: Finding Citation Gaps..."
SECTIONS=("introduction" "theory" "methods" "results" "discussion")
for sec in "${SECTIONS[@]}"; do
    echo "   - Section: $sec"
    ./.venv/bin/python3 langchain_manuscript_analyzer.py --action citation-gaps --input "$sec" >> analysis/citation_gaps.txt
done

echo -e "\n✅ Analysis Complete. Reports saved in analysis/ directory."
