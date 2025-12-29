# Antigravity Mission: Instella Research Orchestrator for BCC Paper

**Mission ID:** `instella-bcc-orchestrator`  
**Target:** Biological Counter-Curvature & Spinal Modes Manuscript  
**Model:** AMD Instella-3B-Long-Instruct (128k context)  
**Status:** Ready for agent execution

---

## 🎯 Mission Overview

You are an **Antigravity agent** operating in this workspace. Your mission is to orchestrate the complete refinement of the Biological Counter-Curvature (BCC) manuscript using AMD's Instella-3B-Long-Instruct model.

**Core objectives:**

1. ✅ Set up and verify Instella infrastructure
2. 📊 Map and summarize the entire research repo
3. 📝 Build/refine target manuscript outline
4. ✍️ Rewrite all manuscript sections using Instella
5. 🔍 Run critical reviewer passes on each section
6. 🔄 Execute long-context consistency checks
7. 📋 Deliver polished manuscript with tracking documents

---

## 📂 Repository Context

**Workspace root:** `/Users/mac/LIFE`

**Key directories:**
- `life/` – Main research codebase (Python solvers, analysis scripts)
- `life-1/` – Alternative version or backup
- `manuscript/` – LaTeX sources (likely in subdirectories)
- Root-level markdown files – Draft sections, plans, outlines

**Draft sections (confirmed present):**
- `draft_intro_BCC.md`
- `draft_theory_BCC.md`
- `draft_methods_BCC.md`
- `draft_results_BCC.md`
- `draft_discussion_BCC.md`
- `draft_conclusion_BCC.md`

**Infrastructure files (already created):**
- ✅ `instella_client.py` – Long-context chat wrapper for Instella
- ✅ `instella_tasks.py` – Helper functions (summarize, rewrite, review)
- ✅ `rewrite_driver.py` – Section rewriting orchestration
- ✅ `reviewer_pass_driver.py` – Critical review orchestration

---

## 🚀 Mission Phases

### Phase 0: Verify Instella Setup

**Goal:** Ensure Instella model and dependencies are ready.

**Tasks:**

1. **Check Python environment**
   ```bash
   cd /Users/mac/LIFE
   python --version  # Should be 3.9+
   ```

2. **Verify dependencies**
   ```bash
   pip list | grep -E "transformers|torch|accelerate|sentencepiece"
   ```
   
   If missing:
   ```bash
   pip install --upgrade pip
   pip install "transformers>=4.47.0" accelerate torch sentencepiece
   ```

3. **Test Instella client**
   ```python
   # Quick test in Python REPL or create test_instella.py
   from instella_client import instella_chat
   
   response = instella_chat(
       system="You are a helpful assistant.",
       messages=[{"role": "user", "content": "Say hello in one sentence."}],
       max_new_tokens=50,
       temperature=0.3,
   )
   print(response)
   ```
   
   Expected: Model loads (may take 1-2 min first time), returns brief greeting.

4. **Document status**
   - Update `INSTELLA_STATUS.md` with:
     - Model ID: `amd/Instella-3B-Long-Instruct`
     - Load status: ✅ or ❌
     - Test result
     - GPU/CPU info
     - Estimated inference speed

**Deliverable:** `INSTELLA_STATUS.md` with setup verification

---

### Phase 1: Repository Mapping & Summarization

**Goal:** Create comprehensive map of repo and summarize key files using Instella's long context.

**Tasks:**

1. **Generate repository tree**
   ```bash
   cd /Users/mac/LIFE
   find . -type f -name "*.py" -o -name "*.md" -o -name "*.tex" | head -200 > repo_tree_snapshot.txt
   ```

2. **Identify key files to summarize**
   Priority targets:
   - All `draft_*_BCC.md` files
   - `TARGET_OUTLINE_BCC.md` (if exists)
   - `MANUSCRIPT_PLAN_BCC.md` (if exists)
   - Any large theory notes in `life/` or `manuscript/`
   - Main solver code (e.g., `life/src/life/solver.py` or similar)

3. **Run Instella summarization**
   ```python
   from instella_tasks import summarize_file
   
   files_to_summarize = [
       "draft_intro_BCC.md",
       "draft_theory_BCC.md",
       "draft_methods_BCC.md",
       "draft_results_BCC.md",
       "draft_discussion_BCC.md",
       "draft_conclusion_BCC.md",
       "TARGET_OUTLINE_BCC.md",
   ]
   
   summaries = {}
   for filepath in files_to_summarize:
       if Path(filepath).exists():
           print(f"Summarizing {filepath}...")
           summaries[filepath] = summarize_file(filepath, goal="scientific manuscript")
   
   # Save to MANUSCRIPT_PLAN_BCC_INSTELLA.md
   ```

4. **Create master planning document**
   - File: `MANUSCRIPT_PLAN_BCC_INSTELLA.md`
   - Structure:
     ```markdown
     # BCC Manuscript Plan (Instella-Enhanced)
     
     ## Repository Structure
     [Tree from repo_tree_snapshot.txt]
     
     ## Draft Sections Summary (via Instella)
     
     ### Introduction
     [Instella summary]
     
     ### Theory
     [Instella summary]
     
     ... [etc for all sections]
     
     ## Key Equations Inventory
     - IEC metric: [extracted from theory summary]
     - IEC energy: [...]
     - Cosserat balance: [...]
     - Mode eigenproblem: [...]
     
     ## Figures Inventory
     [List all figure references found in drafts]
     
     ## Next Steps
     [Agent notes on what needs work]
     ```

**Deliverable:** `MANUSCRIPT_PLAN_BCC_INSTELLA.md` with complete repo map and summaries

---

### Phase 2: Refine Target Outline

**Goal:** Use Instella to create/refine a publication-ready outline.

**Tasks:**

1. **Check for existing outline**
   - If `TARGET_OUTLINE_BCC.md` exists: read it
   - Else: create from draft summaries

2. **Use Instella to refine outline**
   ```python
   from instella_client import instella_chat
   
   system = """You are a structural editor for a theoretical biophysics paper on 
   Biological Counter-Curvature and Information-Elasticity Coupling in spinal systems.
   Your job is to create a clear, logical outline suitable for Nature Communications or 
   Physical Review X."""
   
   messages = [
       {
           "role": "user",
           "content": f"""
   Based on these section summaries:
   
   {summaries_combined}
   
   Create a detailed manuscript outline with:
   - Section titles and subsection structure
   - Key equations to include in each section (by name/description)
   - Figures needed (with placeholders if not yet generated)
   - Logical flow from motivation → theory → methods → results → implications
   
   Target length: 8-12 pages in 2-column format.
   """
       }
   ]
   
   refined_outline = instella_chat(system, messages, max_new_tokens=2048, temperature=0.3)
   ```

3. **Save refined outline**
   - File: `REFINED_OUTLINE_BCC.md`
   - Should include:
     - Clear section hierarchy
     - Equation placeholders with LaTeX names
     - Figure placeholders with descriptions
     - Word count targets per section
     - References to code/notebooks that generate data

**Deliverable:** `REFINED_OUTLINE_BCC.md` – publication-ready structure

---

### Phase 3: Section-by-Section Rewriting

**Goal:** Use Instella to rewrite each draft section for clarity, flow, and journal style.

**Target style:** Nature Communications (can be adjusted)

**Tasks:**

1. **Run rewrite_driver.py on each section**
   
   For each of: intro, theory, methods, results, discussion, conclusion
   
   ```bash
   # Single section
   python rewrite_driver.py draft_intro_BCC.md draft_intro_BCC_rewritten.md "Introduction" "Nature Communications"
   
   # Or batch mode (if you enhance the driver)
   for section in intro theory methods results discussion conclusion; do
       python rewrite_driver.py draft_${section}_BCC.md draft_${section}_BCC_rewritten.md "${section}" "Nature Communications"
   done
   ```

2. **Manual review of rewrites**
   - Check that equations are preserved
   - Verify citations/references are intact
   - Ensure technical terminology is correct
   - Look for any hallucinated content

3. **Flag issues for human review**
   - Add `[[QUESTION FOR AUTHOR]]` comments where Instella's rewrite is unclear
   - Add `[[TODO: VERIFY EQUATION]]` if any LaTeX looks wrong
   - Add `[[TODO: FIGURE X]]` for missing figure references

4. **Create integration checklist**
   - File: `REWRITE_INTEGRATION_CHECKLIST.md`
   - For each section, note:
     - Original file
     - Rewritten file
     - Key changes made by Instella
     - Issues requiring human attention
     - Integration status: [ ] Not started, [x] Integrated, [~] Partially integrated

**Deliverable:** 
- `draft_*_BCC_rewritten.md` for all sections
- `REWRITE_INTEGRATION_CHECKLIST.md`

---

### Phase 4: Reviewer Critique Pass

**Goal:** Run Instella as a critical journal reviewer on each rewritten section.

**Tasks:**

1. **Run reviewer_pass_driver.py on rewritten sections**
   
   ```bash
   # Single section
   python reviewer_pass_driver.py draft_intro_BCC_rewritten.md REVIEW_NOTES_INSTELLA.md "Introduction"
   
   # Batch mode
   for section in intro theory methods results discussion conclusion; do
       python reviewer_pass_driver.py draft_${section}_BCC_rewritten.md REVIEW_NOTES_INSTELLA.md "${section}"
   done
   ```

2. **Compile reviewer feedback**
   - All feedback appends to `REVIEW_NOTES_INSTELLA.md`
   - Structure by section
   - Categorize feedback:
     - 🔴 **Major issues** (must fix before submission)
     - 🟡 **Minor issues** (improve clarity)
     - 🔵 **Suggestions** (optional enhancements)

3. **Create action items from feedback**
   - For straightforward fixes (typos, minor clarifications), update files directly
   - For structural concerns, add to `REWRITE_INTEGRATION_CHECKLIST.md`
   - For scientific questions, flag with `[[AUTHOR EXPERTISE NEEDED]]`

**Deliverable:** `REVIEW_NOTES_INSTELLA.md` with section-by-section critique

---

### Phase 5: Long-Context Consistency Check

**Goal:** Leverage Instella's 128k context to check consistency across the entire manuscript.

**Tasks:**

1. **Concatenate all rewritten sections**
   ```python
   sections_order = [
       "draft_intro_BCC_rewritten.md",
       "draft_theory_BCC_rewritten.md",
       "draft_methods_BCC_rewritten.md",
       "draft_results_BCC_rewritten.md",
       "draft_discussion_BCC_rewritten.md",
       "draft_conclusion_BCC_rewritten.md",
   ]
   
   full_manuscript = ""
   for sec in sections_order:
       if Path(sec).exists():
           full_manuscript += f"\n\n# {sec}\n\n"
           full_manuscript += Path(sec).read_text()
   
   Path("full_manuscript_concatenated.md").write_text(full_manuscript)
   ```

2. **Run consistency check with Instella**
   ```python
   from instella_client import instella_chat
   
   system = """You are a meticulous technical editor for a biophysics journal.
   Check this complete manuscript draft for:
   1. Symbol consistency (are all variables defined before use?)
   2. Notation conflicts (same symbol used for different things?)
   3. Internal contradictions (theory vs results mismatch?)
   4. Missing transitions between sections
   5. Narrative coherence (does the story flow logically?)"""
   
   messages = [
       {
           "role": "user",
           "content": f"Analyze this full manuscript:\n\n{full_manuscript[:100000]}"  # Truncate if needed
       }
   ]
   
   consistency_report = instella_chat(system, messages, max_new_tokens=3000, temperature=0.2)
   Path("CONSISTENCY_REPORT_INSTELLA.md").write_text(consistency_report)
   ```

3. **Extract core narrative**
   ```python
   system = """You are a science communicator. Read this manuscript and distill
   the core narrative into 3-4 sentences suitable for:
   - The abstract
   - The introduction's final paragraph
   - The conclusion's opening paragraph"""
   
   messages = [
       {
           "role": "user",
           "content": f"Extract the core narrative from:\n\n{full_manuscript[:80000]}"
       }
   ]
   
   core_narrative = instella_chat(system, messages, max_new_tokens=500, temperature=0.3)
   ```

4. **Update planning document**
   - Add core narrative to `MANUSCRIPT_PLAN_BCC_INSTELLA.md`
   - Add consistency findings to same document

**Deliverable:** 
- `CONSISTENCY_REPORT_INSTELLA.md`
- Updated `MANUSCRIPT_PLAN_BCC_INSTELLA.md` with core narrative

---

### Phase 6: Abstract & Conclusion Polish

**Goal:** Use Instella to craft publication-ready abstract and conclusion based on refined content.

**Tasks:**

1. **Generate abstract**
   ```python
   from instella_client import instella_chat
   
   system = """You are writing an abstract for Nature Communications (150-200 words).
   The abstract must:
   - State the problem and motivation
   - Describe the approach (Information-Elasticity Coupling + Cosserat theory)
   - Highlight key findings (3D modes, phase diagrams, pathology predictions)
   - State broader implications"""
   
   messages = [
       {
           "role": "user",
           "content": f"""Based on this manuscript:
   
   Core narrative: {core_narrative}
   
   Introduction: {intro_summary}
   
   Results: {results_summary}
   
   Write a 150-200 word abstract."""
       }
   ]
   
   abstract = instella_chat(system, messages, max_new_tokens=400, temperature=0.3)
   Path("ABSTRACT_POLISHED_INSTELLA.md").write_text(abstract)
   ```

2. **Refine conclusion**
   ```python
   # Similar approach, 250-300 words
   # Should tie back to core narrative
   # Should suggest future directions
   ```

**Deliverable:** 
- `ABSTRACT_POLISHED_INSTELLA.md`
- Updated `draft_conclusion_BCC_rewritten.md`

---

### Phase 7: Final Integration & Deliverables

**Goal:** Compile all Instella-enhanced content into final manuscript and documentation.

**Tasks:**

1. **Create master manuscript file**
   - File: `MANUSCRIPT_FULL_BCC_INSTELLA.md`
   - Combine all rewritten sections in order
   - Include polished abstract
   - Add figure placeholders with captions
   - Include equation numbering guide

2. **Create changelog**
   - File: `CHANGELOG_INSTELLA.md`
   - Document major changes per section:
     - Introduction: [summary of improvements]
     - Theory: [...]
     - etc.
   - List equations verified
   - List figures referenced
   - List remaining TODOs

3. **Create author action items**
   - File: `AUTHOR_ACTION_ITEMS_BCC.md`
   - Extract all `[[QUESTION FOR AUTHOR]]` markers
   - Extract all `[[TODO: ...]]` markers
   - Prioritize by section and urgency

4. **Quality assurance checklist**
   - [ ] All sections rewritten and integrated
   - [ ] Reviewer feedback addressed or flagged
   - [ ] Consistency check completed
   - [ ] Equations preserved and numbered
   - [ ] Citations intact
   - [ ] Figures mapped to code/notebooks
   - [ ] Abstract polished
   - [ ] Conclusion ties to introduction
   - [ ] Core narrative present in abstract/intro/conclusion

**Deliverables:**
- `MANUSCRIPT_FULL_BCC_INSTELLA.md` – Complete draft
- `CHANGELOG_INSTELLA.md` – Record of improvements
- `AUTHOR_ACTION_ITEMS_BCC.md` – Human review needed

---

## 🎛️ Execution Guidelines

### For Antigravity Agents

**Operational rules:**

1. **Never delete original content**
   - Always work on `*_rewritten.md` or similar
   - Keep originals in place for comparison
   - If moving content, use `archive/` directory

2. **Preserve technical integrity**
   - Never modify equations without explicit instruction
   - Never invent data, results, or figures
   - Flag uncertainties with `[[VERIFY: ...]]`

3. **Stay scientific, not chatty**
   - Use formal academic tone in all Instella prompts
   - Avoid colloquialisms in generated text
   - Maintain consistent technical terminology

4. **Track progress explicitly**
   - Update `INSTELLA_STATUS.md` after each phase
   - Log errors and issues immediately
   - Provide ETA for long operations (model loading, inference)

5. **Human-in-the-loop for key decisions**
   - When Instella suggests major structural changes, flag for review
   - When encountering scientific ambiguity, ask rather than guess
   - When integration conflicts arise, document and request guidance

### Instella Usage Patterns

**For summarization:**
- Temperature: 0.2 (factual)
- Max tokens: 1024
- System prompt: Emphasize preservation of equations and notation

**For rewriting:**
- Temperature: 0.35 (creative but controlled)
- Max tokens: 2048
- System prompt: Specify target journal style explicitly

**For reviewing:**
- Temperature: 0.5 (critical thinking)
- Max tokens: 2048
- System prompt: "Act as Reviewer 2" (constructive but critical)

**For consistency checking:**
- Temperature: 0.2 (analytical)
- Max tokens: 3000
- System prompt: Focus on symbol definitions and logical flow

---

## 📊 Success Metrics

**Phase completion checklist:**

- ✅ Phase 0: Model loads successfully, test inference runs
- ✅ Phase 1: All key files summarized, planning doc created
- ✅ Phase 2: Refined outline approved (structurally sound)
- ✅ Phase 3: All 6 sections rewritten, integration checklist complete
- ✅ Phase 4: Reviewer notes compiled for all sections
- ✅ Phase 5: Consistency report generated, core narrative extracted
- ✅ Phase 6: Abstract + conclusion polished
- ✅ Phase 7: Full manuscript compiled, action items documented

**Quality indicators:**

- Zero equation formatting errors introduced
- Zero citation/reference losses
- Improved readability scores (Flesch-Kincaid) in rewritten sections
- Reduced redundancy between sections
- Clear logical flow from intro → conclusion
- All figures mapped to source code/notebooks

---

## 🆘 Troubleshooting

**Model loading issues:**
- If Instella fails to load: Check PyTorch/CUDA compatibility
- If OOM errors: Reduce `MAX_CONTEXT_TOKENS` in `instella_client.py`
- If slow inference: Consider using 4-bit quantization (advanced)

**Content quality issues:**
- If rewrites lose technical detail: Lower temperature, adjust system prompt
- If hallucinations occur: Add "Preserve all existing content" to prompt
- If style doesn't match target: Provide example paragraphs in prompt

**Integration conflicts:**
- If equation numbering breaks: Create equation inventory first
- If sections don't connect: Use Instella to generate transition paragraphs
- If narrative fragments: Run consistency check earlier in process

---

## 🎯 Final Output Structure

```
/Users/mac/LIFE/
├── INSTELLA_STATUS.md                    # Setup and model status
├── MANUSCRIPT_PLAN_BCC_INSTELLA.md       # Repo map + summaries + narrative
├── REFINED_OUTLINE_BCC.md                # Publication-ready outline
├── REVIEW_NOTES_INSTELLA.md              # Section-by-section critique
├── CONSISTENCY_REPORT_INSTELLA.md        # Cross-section analysis
├── REWRITE_INTEGRATION_CHECKLIST.md      # Integration tracking
├── CHANGELOG_INSTELLA.md                 # Summary of improvements
├── AUTHOR_ACTION_ITEMS_BCC.md            # Human review needed
├── ABSTRACT_POLISHED_INSTELLA.md         # Refined abstract
├── MANUSCRIPT_FULL_BCC_INSTELLA.md       # Complete draft manuscript
├── draft_*_BCC_rewritten.md              # Rewritten sections (6 files)
└── archive/                              # Original versions (backup)
```

---

## 🚀 Quick Start Commands

```bash
# Phase 0: Test Instella
python -c "from instella_client import instella_chat; print(instella_chat('You are helpful', [{'role':'user','content':'Hi'}], max_new_tokens=20))"

# Phase 1: Summarize all drafts
python -c "
from instella_tasks import summarize_file
from pathlib import Path
for f in Path('.').glob('draft_*_BCC.md'):
    print(f'Summarizing {f}...')
    summary = summarize_file(str(f))
    Path(f'{f.stem}_summary.txt').write_text(summary)
"

# Phase 3: Rewrite all sections
for sec in intro theory methods results discussion conclusion; do
    python rewrite_driver.py draft_${sec}_BCC.md draft_${sec}_BCC_rewritten.md "${sec}" "Nature Communications"
done

# Phase 4: Review all sections
for sec in intro theory methods results discussion conclusion; do
    python reviewer_pass_driver.py draft_${sec}_BCC_rewritten.md REVIEW_NOTES_INSTELLA.md "${sec}"
done
```

---

## 📝 Notes for Author

**Human oversight points:**

1. **After Phase 2:** Review `REFINED_OUTLINE_BCC.md` – does the structure make sense?
2. **After Phase 3:** Spot-check rewritten sections – are equations correct?
3. **After Phase 4:** Read `REVIEW_NOTES_INSTELLA.md` – any critical issues?
4. **After Phase 5:** Review `CONSISTENCY_REPORT_INSTELLA.md` – any contradictions?
5. **Before submission:** Process `AUTHOR_ACTION_ITEMS_BCC.md` – resolve all `[[QUESTION]]` markers

**Tips for best results:**

- Run phases sequentially; don't skip ahead
- Keep original drafts unchanged until rewrite is verified
- Use Instella's long context advantage: feed it entire sections at once
- Leverage the chat history: build context across multiple prompts when needed
- Trust the reviewer pass: Instella's critique is often insightful

---

## 🎓 Advanced: Extending the Mission

**Optional enhancements:**

1. **Figure generation integration**
   - Use Instella to analyze plot scripts
   - Generate captions based on code + data
   - Suggest additional plots for clarity

2. **Citation management**
   - Extract all `\cite{}` commands
   - Use Instella to suggest additional relevant papers
   - Check for missing citations in key claims

3. **Equation derivation documentation**
   - For each equation, generate a "derivation note"
   - Link equations to code implementations
   - Create supplementary material with full derivations

4. **Response to reviewers template**
   - After journal submission, use Instella to draft responses
   - Reference specific line numbers in manuscript
   - Maintain respectful, scientific tone

---

**Mission Status:** Ready for execution  
**Agent Authorization:** Autonomous operation within safety guidelines  
**Expected Completion Time:** 4-6 hours (mostly inference time)  
**Author Involvement Required:** ~1-2 hours review across all phases

---

*End of Mission Document*  
*Last Updated: 2025-11-27*  
*Prepared for: Antigravity Agent Execution*
