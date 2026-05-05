#!/bin/bash
# Final manuscript verification before submission

echo "═══════════════════════════════════════════════════════════════"
echo "FINAL MANUSCRIPT VERIFICATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

ERRORS=0
WARNINGS=0

# Check 1: Required files exist
echo "✓ Checking required files..."
FILES=(
    "manuscript/main.tex"
    "manuscript/sections/abstract.tex"
    "manuscript/sections/introduction.tex"
    "manuscript/sections/theory_summary.tex"
    "manuscript/sections/methods_summary.tex"
    "manuscript/sections/results.tex"
    "manuscript/sections/discussion.tex"
    "manuscript/sections/conclusion.tex"
    "manuscript/sections/statements.tex"
    "manuscript/sections/figures.tex"
    "manuscript/sections/availability.tex"
    "manuscript/references.bib"
    "manuscript_overleaf.zip"
    "submission_package/cover_letter_spine_deformity.tex"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ MISSING: $file"
        ((ERRORS++))
    fi
done
echo ""

# Check 2: Manuscript structure
echo "✓ Checking manuscript structure..."
if grep -q "\\input{sections/theory_summary}" manuscript/main.tex; then
    echo "  ✅ Using theory_summary (not full theory)"
else
    echo "  ⚠️  WARNING: May be using full theory section"
    ((WARNINGS++))
fi

if grep -q "\\input{sections/methods_summary}" manuscript/main.tex; then
    echo "  ✅ Using methods_summary (not full methods)"
else
    echo "  ⚠️  WARNING: May be using full methods section"
    ((WARNINGS++))
fi

if grep -q "\\input{sections/statements}" manuscript/main.tex; then
    echo "  ✅ Statements section included"
else
    echo "  ❌ ERROR: Statements section not included"
    ((ERRORS++))
fi
echo ""

# Check 3: Word count estimate
echo "✓ Estimating word count..."
TOTAL_WORDS=$(wc -w manuscript/sections/*.tex 2>/dev/null | tail -1 | awk '{print $1}')
echo "  Total: ~$TOTAL_WORDS words"

if [ "$TOTAL_WORDS" -lt 7000 ]; then
    echo "  ✅ Word count in acceptable range (~5,000-6,000)"
else
    echo "  ⚠️  WARNING: Word count may be high (target: ~5,000)"
    ((WARNINGS++))
fi
echo ""

# Check 4: Required statements present
echo "✓ Checking required statements..."
if grep -qi "ethics" manuscript/sections/statements.tex; then
    echo "  ✅ Ethics statement found"
else
    echo "  ❌ ERROR: Ethics statement missing"
    ((ERRORS++))
fi

if grep -qi "competing" manuscript/sections/statements.tex; then
    echo "  ✅ Competing interests statement found"
else
    echo "  ❌ ERROR: Competing interests missing"
    ((ERRORS++))
fi

if grep -qi "funding" manuscript/sections/statements.tex; then
    echo "  ✅ Funding statement found"
else
    echo "  ❌ ERROR: Funding statement missing"
    ((ERRORS++))
fi
echo ""

# Check 5: Figure files exist
echo "✓ Checking figure files..."
FIGURE_COUNT=$(find figures/main -type f \( -name "*.pdf" -o -name "*.png" \) 2>/dev/null | wc -l)
echo "  Found $FIGURE_COUNT figure files"

if [ "$FIGURE_COUNT" -ge 7 ]; then
    echo "  ✅ Sufficient figures (expected 7-8)"
else
    echo "  ⚠️  WARNING: Expected 7-8 figures, found $FIGURE_COUNT"
    ((WARNINGS++))
fi
echo ""

# Check 6: References
echo "✓ Checking references..."
REF_COUNT=$(grep -c "^@" manuscript/references.bib 2>/dev/null || echo 0)
echo "  Found $REF_COUNT references"

if [ "$REF_COUNT" -ge 200 ] && [ "$REF_COUNT" -le 300 ]; then
    echo "  ✅ Reference count acceptable (200-300)"
elif [ "$REF_COUNT" -gt 300 ]; then
    echo "  ⚠️  WARNING: High reference count ($REF_COUNT)"
    ((WARNINGS++))
else
    echo "  ⚠️  WARNING: Low reference count ($REF_COUNT)"
    ((WARNINGS++))
fi
echo ""

# Check 7: Git status
echo "✓ Checking git status..."
if git rev-parse --verify v1.0.0-submission >/dev/null 2>&1; then
    echo "  ✅ Tag v1.0.0-submission exists"
else
    echo "  ⚠️  WARNING: Tag v1.0.0-submission not found"
    ((WARNINGS++))
fi

if git diff --quiet 2>/dev/null; then
    echo "  ✅ No uncommitted changes"
else
    echo "  ⚠️  WARNING: Uncommitted changes present"
    ((WARNINGS++))
fi
echo ""

# Check 8: Overleaf ZIP
echo "✓ Checking Overleaf upload file..."
if [ -f "manuscript_overleaf.zip" ]; then
    SIZE=$(ls -lh manuscript_overleaf.zip | awk '{print $5}')
    echo "  ✅ manuscript_overleaf.zip exists ($SIZE)"
else
    echo "  ❌ ERROR: manuscript_overleaf.zip not found"
    ((ERRORS++))
fi
echo ""

# Check 9: Documentation
echo "✓ Checking documentation files..."
DOCS=(
    "DO_THIS_NOW.txt"
    "SUBMISSION_READY_FINAL.md"
    "FINAL_SUBMISSION_CHECKLIST.md"
    "ZENODO_SETUP_INSTRUCTIONS.md"
    "COMPILE_PDF_OPTIONS.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc"
    else
        echo "  ⚠️  Missing: $doc (optional)"
    fi
done
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════════"
echo "VERIFICATION SUMMARY"
echo "═══════════════════════════════════════════════════════════════"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ "$ERRORS" -eq 0 ]; then
    echo "✅ ✅ ✅ MANUSCRIPT IS PUBLICATION-READY! ✅ ✅ ✅"
    echo ""
    echo "Next steps:"
    echo "1. Go to https://www.overleaf.com"
    echo "2. Upload manuscript_overleaf.zip"
    echo "3. Compile → Download PDF"
    echo "4. Submit to https://www.editorialmanager.com/spde/"
    echo ""
    echo "See DO_THIS_NOW.txt for detailed instructions."
    echo ""
    exit 0
else
    echo "❌ ERRORS FOUND - MUST FIX BEFORE SUBMISSION"
    echo ""
    echo "Fix the errors listed above, then run this script again."
    echo ""
    exit 1
fi
