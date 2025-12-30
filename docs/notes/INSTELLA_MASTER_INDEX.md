# 📚 Instella System - Master Index

**Quick navigation for all Instella-related files**

---

## 🎯 Start Here

| File | Purpose | When to Use |
|------|---------|-------------|
| **`INSTELLA_INTEGRATION_COMPLETE.md`** | **Overall summary** | Read first to understand what's been built |
| **`INSTELLA_QUICKSTART.md`** | **5-minute guide** | When you want to test/run tasks immediately |
| **`INSTELLA_ANTIGRAVITY_MISSION.md`** | **Complete mission** | For autonomous agent execution or full workflow |
| **`INSTELLA_STATUS.md`** | **Current status** | Check setup status, troubleshoot issues |

---

## 📖 Documentation (4 files, ~52KB)

### 1. `INSTELLA_INTEGRATION_COMPLETE.md` (14KB)
**What it is:** High-level summary of the entire system  
**Contains:**
- What's been created
- 7-phase mission overview
- How to use the system (human vs. agent)
- Expected deliverables
- Next steps and pro tips

**Read when:** Starting fresh, want big picture

---

### 2. `INSTELLA_QUICKSTART.md` (8.1KB)
**What it is:** Hands-on getting started guide  
**Contains:**
- 5-minute setup verification
- Common workflows (summarize/rewrite/review)
- Quick commands for immediate use
- Troubleshooting tips
- Performance reference tables

**Read when:** Ready to run tasks, need quick commands

---

### 3. `INSTELLA_ANTIGRAVITY_MISSION.md` (21KB)
**What it is:** Detailed 7-phase execution plan  
**Contains:**
- Phase 0: Setup verification
- Phase 1: Repo mapping & summarization
- Phase 2: Outline refinement
- Phase 3: Section rewrites
- Phase 4: Reviewer passes
- Phase 5: Consistency checks
- Phase 6: Abstract/conclusion polish
- Phase 7: Final integration
- Execution guidelines, success metrics, troubleshooting

**Read when:** Running full workflow, autonomous agent execution

---

### 4. `INSTELLA_STATUS.md` (8.4KB)
**What it is:** Current system status and diagnostics  
**Contains:**
- Setup completion checklist
- Phase 0 verification instructions
- Performance expectations
- Troubleshooting diagnostics
- Mission execution checklist
- Alternative approaches (API-based LLMs)

**Read when:** Checking if setup is ready, troubleshooting, updating status

---

## 🔧 Core Infrastructure (2 files, ~6KB)

### 5. `instella_client.py` (4.0KB)
**What it is:** Low-level Instella wrapper  
**Key functions:**
- `instella_chat(system, messages, ...)` – Main chat interface
- `_build_prompt(system, messages)` – Chat template builder
- `summarize_text(text, goal)` – Quick summarization helper

**Modify when:** Need to change model settings, context limits, or add streaming features  
**Don't modify if:** You just want to use Instella (use `instella_tasks.py` instead)

---

### 6. `instella_tasks.py` (2.3KB)
**What it is:** High-level task helpers  
**Key functions:**
- `summarize_file(path, goal)` – Summarize files with auto-chunking
- `rewrite_section(title, content, style)` – Journal-style rewrites
- `reviewer_pass(section_title, content)` – Critical reviewer feedback
- `read_text_file(path)` – Safe file reading

**Modify when:** Adding new task types (e.g., citation extraction, equation validation)  
**Use directly:** Import and call these functions in scripts/notebooks

---

## 🚀 Driver Scripts (2+ files, see project root)

### 7. `rewrite_driver.py`
**What it is:** CLI for section rewrites  
**Usage:**
```bash
python rewrite_driver.py <input> <output> <title> [style]
```
**Example:**
```bash
python rewrite_driver.py draft_intro_BCC.md draft_intro_BCC_rewritten.md "Introduction" "Nature Communications"
```

---

### 8. `reviewer_pass_driver.py`
**What it is:** CLI for reviewer passes  
**Usage:**
```bash
python reviewer_pass_driver.py <input> <output_report> <title>
```
**Example:**
```bash
python reviewer_pass_driver.py draft_intro_BCC.md REVIEW_NOTES_INSTELLA.md "Introduction"
```

---

### 9. `summarize_manuscript.py`
**What it is:** Batch summarization of all sections  
**Usage:**
```bash
python summarize_manuscript.py
```
**Output:** Summaries appended to `MANUSCRIPT_PLAN_BCC_INSTELLA.md`

---

### 10. `refine_outline.py`
**What it is:** Outline refinement with Instella  
**Usage:**
```bash
python refine_outline.py
```
**Input:** `TARGET_OUTLINE_BCC.md` (or creates from scratch)  
**Output:** `REFINED_OUTLINE_BCC.md`

---

### 11. `consistency_check.py`
**What it is:** Full manuscript consistency analysis  
**Usage:**
```bash
python consistency_check.py
```
**Output:** `CONSISTENCY_REPORT_INSTELLA.md`

---

### 12. `run_rewrites.sh`
**What it is:** Batch script to rewrite all sections  
**Usage:**
```bash
bash run_rewrites.sh
```
**Output:** All `draft_*_BCC_rewritten.md` files

---

## 📊 Planning & Tracking (2 files)

### 13. `MANUSCRIPT_PLAN_BCC_INSTELLA.md` (922B)
**What it is:** Repo map + section summaries + core narrative  
**Updated by:** Phase 1 (summarization), Phase 5 (consistency check)  
**Contains:**
- Directory structure
- Section summaries (via Instella)
- Equation inventory
- Figure inventory
- Core narrative

---

### 14. `PROJECT_TREE_INSTELLA.txt` (15KB)
**What it is:** Full repository file tree  
**Generated by:** `find` command or manual tree snapshot  
**Use for:** Understanding repo structure, finding files

---

## 🎯 Usage Patterns

### Pattern 1: Quick Test (5 minutes)
```bash
# Read quickstart
cat INSTELLA_QUICKSTART.md

# Test Instella
python -c "from instella_client import instella_chat; print(instella_chat('helpful', [{'role':'user','content':'hi'}], max_new_tokens=10))"

# Summarize one file
python -c "from instella_tasks import summarize_file; print(summarize_file('draft_intro_BCC.md'))"
```

**Files needed:** `instella_client.py`, `instella_tasks.py`, `INSTELLA_QUICKSTART.md`

---

### Pattern 2: Single Section Workflow (30 minutes)
```bash
# Summarize
python -c "from instella_tasks import summarize_file; print(summarize_file('draft_intro_BCC.md'))" > intro_summary.txt

# Rewrite
python rewrite_driver.py draft_intro_BCC.md draft_intro_BCC_rewritten.md "Introduction" "Nature Communications"

# Review
python reviewer_pass_driver.py draft_intro_BCC_rewritten.md REVIEW_NOTES_INSTELLA.md "Introduction"
```

**Files needed:** Core infrastructure + driver scripts

---

### Pattern 3: Full Manuscript Workflow (4-6 hours)
```bash
# Follow the mission
cat INSTELLA_ANTIGRAVITY_MISSION.md

# Execute phases 0-7 sequentially
# See mission document for detailed steps
```

**Files needed:** All documentation + infrastructure + driver scripts

---

### Pattern 4: Antigravity Agent (Autonomous)
```
Mission prompt:
"Execute INSTELLA_ANTIGRAVITY_MISSION.md for BCC paper refinement. 
Run all 7 phases sequentially. Update INSTELLA_STATUS.md after each phase."
```

**Files needed:** `INSTELLA_ANTIGRAVITY_MISSION.md` (agent reads others as needed)

---

## 🔍 File Dependency Graph

```
INSTELLA_INTEGRATION_COMPLETE.md (start here)
    ├─ INSTELLA_QUICKSTART.md (quick tasks)
    │   └─ instella_client.py (core model wrapper)
    │   └─ instella_tasks.py (helper functions)
    │       ├─ rewrite_driver.py
    │       ├─ reviewer_pass_driver.py
    │       ├─ summarize_manuscript.py
    │       ├─ refine_outline.py
    │       └─ consistency_check.py
    │
    ├─ INSTELLA_ANTIGRAVITY_MISSION.md (full workflow)
    │   └─ Uses all driver scripts above
    │   └─ Produces: MANUSCRIPT_PLAN_BCC_INSTELLA.md
    │                 REFINED_OUTLINE_BCC.md
    │                 REVIEW_NOTES_INSTELLA.md
    │                 CONSISTENCY_REPORT_INSTELLA.md
    │                 ... (many outputs)
    │
    └─ INSTELLA_STATUS.md (status tracking)
        └─ Updated after each phase
```

---

## 📦 Expected Outputs (After Full Mission)

### Documentation Outputs
- `MANUSCRIPT_PLAN_BCC_INSTELLA.md` – Enhanced with summaries
- `REFINED_OUTLINE_BCC.md` – Publication-ready structure
- `REVIEW_NOTES_INSTELLA.md` – Critical feedback
- `CONSISTENCY_REPORT_INSTELLA.md` – Cross-section analysis
- `CHANGELOG_INSTELLA.md` – Improvement summary
- `AUTHOR_ACTION_ITEMS_BCC.md` – Human review needed

### Content Outputs
- `draft_intro_BCC_rewritten.md`
- `draft_theory_BCC_rewritten.md`
- `draft_methods_BCC_rewritten.md`
- `draft_results_BCC_rewritten.md`
- `draft_discussion_BCC_rewritten.md`
- `draft_conclusion_BCC_rewritten.md`
- `ABSTRACT_POLISHED_INSTELLA.md`
- `MANUSCRIPT_FULL_BCC_INSTELLA.md` – Complete integrated draft

---

## 🎓 Learning Path

**If you're new to this system:**

1. **Day 1:** Read `INSTELLA_INTEGRATION_COMPLETE.md` (20 min)
2. **Day 1:** Follow `INSTELLA_QUICKSTART.md` (30 min)
3. **Day 1:** Test on one section (intro) using Pattern 2 above (30 min)
4. **Day 2:** Review outputs, adjust if needed (1 hour)
5. **Day 2:** Run batch rewrite (Phases 3-4) (2-3 hours)
6. **Day 3:** Consistency check and integration (Phases 5-7) (2-3 hours)

**If you're an Antigravity agent:**

1. Read `INSTELLA_ANTIGRAVITY_MISSION.md`
2. Execute phases 0-7 sequentially
3. Update `INSTELLA_STATUS.md` after each phase
4. Flag uncertainties for human review

---

## 🆘 Troubleshooting Index

| Problem | See This File | Section |
|---------|--------------|---------|
| Model won't load | `INSTELLA_STATUS.md` | "Next Steps: Phase 0 Verification" |
| Import errors | `INSTELLA_QUICKSTART.md` | "Troubleshooting" |
| Slow inference | `INSTELLA_STATUS.md` | "Performance Expectations" |
| Poor output quality | `INSTELLA_ANTIGRAVITY_MISSION.md` | "Instella Usage Patterns" |
| OOM errors | `INSTELLA_STATUS.md` | "If Test Fails" |
| Equation mangling | `INSTELLA_QUICKSTART.md` | "Tips for Best Results" |
| General setup | `INSTELLA_INTEGRATION_COMPLETE.md` | "Next Steps → Immediate" |

---

## 📞 Quick Reference Commands

### Setup
```bash
cd /Users/mac/LIFE
source .venv/bin/activate
pip list | grep -E "transformers|torch"
```

### Test
```bash
python -c "from instella_client import instella_chat; print(instella_chat('helpful', [{'role':'user','content':'hi'}], max_new_tokens=10))"
```

### Summarize
```bash
python -c "from instella_tasks import summarize_file; print(summarize_file('draft_intro_BCC.md'))"
```

### Rewrite
```bash
python rewrite_driver.py draft_intro_BCC.md draft_intro_BCC_rewritten.md "Introduction"
```

### Review
```bash
python reviewer_pass_driver.py draft_intro_BCC.md REVIEW_NOTES_INSTELLA.md "Introduction"
```

### Batch (all sections)
```bash
bash run_rewrites.sh
```

---

## ✅ System Status

| Component | Status | Location |
|-----------|--------|----------|
| Documentation | ✅ Complete | 4 files, 52KB |
| Core infrastructure | ✅ Ready | 2 files, 6KB |
| Driver scripts | ✅ Ready | 6+ files |
| Mission plan | ✅ Ready | `INSTELLA_ANTIGRAVITY_MISSION.md` |
| Dependencies | ⏸️ Pending test | Run Phase 0 |
| Model | ⏸️ Not tested | Run Phase 0 |

**Next action:** Follow `INSTELLA_QUICKSTART.md` to test setup (Phase 0)

---

## 🎯 Success Checklist

- [x] All documentation created
- [x] Core infrastructure present
- [x] Driver scripts available
- [x] Mission plan ready
- [x] Quick start guide written
- [x] Master index created (this file)
- [ ] Virtual environment activated
- [ ] Dependencies verified
- [ ] Instella model tested
- [ ] At least one task completed
- [ ] Ready for full mission

**Once all boxes checked, system is fully operational.**

---

## 📚 File Size Reference

| File | Size | Type |
|------|------|------|
| `INSTELLA_ANTIGRAVITY_MISSION.md` | 21KB | Documentation |
| `INSTELLA_INTEGRATION_COMPLETE.md` | 14KB | Documentation |
| `INSTELLA_QUICKSTART.md` | 8.1KB | Documentation |
| `INSTELLA_STATUS.md` | 8.4KB | Documentation |
| `instella_client.py` | 4.0KB | Code |
| `instella_tasks.py` | 2.3KB | Code |
| `MANUSCRIPT_PLAN_BCC_INSTELLA.md` | 922B | Planning |
| `PROJECT_TREE_INSTELLA.txt` | 15KB | Planning |
| **Total** | **~73KB** | **8 core files** |

*Plus driver scripts (rewrite_driver.py, etc.) in project root*

---

**Master Index Version:** 1.0  
**Last Updated:** 2025-11-27  
**Status:** Complete and ready for use  
**Total Setup Time:** ~1 hour for full system creation  
**Next Step:** Read `INSTELLA_INTEGRATION_COMPLETE.md` or `INSTELLA_QUICKSTART.md`

---

*End of Master Index*
