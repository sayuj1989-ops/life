#!/usr/bin/env python3
"""
Cloud-optimized manuscript editor with checkpointing support.
Designed for SkyPilot deployment on GPU instances.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List
import time

# Import the appropriate client based on availability
try:
    from qwen_client import qwen_chat as qwen_llm_chat
    QWEN_AVAILABLE = True
except ImportError:
    QWEN_AVAILABLE = False

try:
    from instella_client import instella_chat as instella_llm_chat
    INSTELLA_AVAILABLE = True
except ImportError:
    INSTELLA_AVAILABLE = False

try:
    from lmstudio_client import lmstudio_chat as lmstudio_llm_chat
    LMSTUDIO_AVAILABLE = True
except ImportError:
    LMSTUDIO_AVAILABLE = False

# Default will be set in main() or via CLI
llm_chat = None 
MODEL_NAME = "Unknown"

if not (QWEN_AVAILABLE or INSTELLA_AVAILABLE or LMSTUDIO_AVAILABLE):
    print("❌ Error: No LLM clients found (qwen, instella, or lmstudio)!")
    sys.exit(1)

# Import RAG analyzer if available
try:
    from langchain_manuscript_analyzer import ManuscriptAnalyzer
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("⚠️  RAG analyzer not available, proceeding without RAG enhancement")


class CloudManuscriptEditor:
    """Cloud-optimized manuscript editor with progress tracking"""
    
    def __init__(self, checkpoint_dir: str = None):
        self.checkpoint_dir = Path(checkpoint_dir) if checkpoint_dir else None
        self.progress_file = self.checkpoint_dir / "progress.json" if self.checkpoint_dir else None
        self.output_dir = Path("edited_sections")
        self.output_dir.mkdir(exist_ok=True)
        
        # Load progress if resuming
        self.completed_sections = self._load_progress()
        
        # Initialize RAG if available
        self.rag_analyzer = None
        if RAG_AVAILABLE and Path("chroma_db").exists():
            try:
                self.rag_analyzer = ManuscriptAnalyzer()
                print("✅ RAG analyzer initialized")
            except Exception as e:
                print(f"⚠️  RAG initialization failed: {e}")
    
    def _load_progress(self) -> List[str]:
        """Load checkpoint progress"""
        if self.progress_file and self.progress_file.exists():
            with open(self.progress_file) as f:
                data = json.load(f)
                return data.get("completed_sections", [])
        return []
    
    def _save_progress(self, section: str):
        """Save checkpoint progress"""
        if self.checkpoint_dir:
            self.checkpoint_dir.mkdir(exist_ok=True)
            self.completed_sections.append(section)
            with open(self.progress_file, "w") as f:
                json.dump({
                    "completed_sections": self.completed_sections,
                    "timestamp": time.time()
                }, f)
    
    def edit_section(self, section_name: str, content: str, style: str = "Nature Communications") -> str:
        """Edit a single section using LLM"""
        
        system_prompt = f"""You are an expert scientific editor for {style}.
Your task is to refine and improve the following manuscript section while:
- Maintaining technical accuracy
- Preserving all equations and notation
- Improving clarity and flow
- Following {style} style guidelines
- Keeping the same section structure"""
        
        user_message = {
            "role": "user",
            "content": f"Please refine this {section_name} section:\n\n{content}"
        }
        
        print(f"  Editing {section_name} with {MODEL_NAME}...")
        edited = llm_chat(system_prompt, [user_message], max_new_tokens=4096, temperature=0.3)
        
        return edited
    
    def process_manuscript(self, manuscript_dir: Path, style: str = "Nature Communications"):
        """Process all manuscript sections"""
        
        sections = [
            "introduction",
            "theory", 
            "methods",
            "results",
            "discussion",
            "conclusion"
        ]
        
        total_sections = len(sections)
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"Cloud Manuscript Editor - {MODEL_NAME}")
        print(f"{'='*60}\n")
        
        for idx, section in enumerate(sections, 1):
            # Skip if already completed
            if section in self.completed_sections:
                print(f"[{idx}/{total_sections}] ✅ {section} (already completed, skipping)")
                continue
            
            # Find section file
            section_files = list(manuscript_dir.glob(f"**/{section}.tex"))
            if not section_files:
                section_files = list(manuscript_dir.glob(f"**/draft_{section}_*.md"))
            
            if not section_files:
                print(f"[{idx}/{total_sections}] ⚠️  {section}.tex not found, skipping")
                continue
            
            section_file = section_files[0]
            
            print(f"\n[{idx}/{total_sections}] Processing: {section}")
            print(f"  Input: {section_file}")
            
            # Read content
            with open(section_file) as f:
                content = f.read()
            
            # Edit section
            try:
                edited_content = self.edit_section(section, content, style)
                
                # Save output
                output_file = self.output_dir / f"{section}_v2.tex"
                with open(output_file, "w") as f:
                    f.write(edited_content)
                
                print(f"  Output: {output_file}")
                print(f"  ✅ Complete ({len(edited_content)} chars)")
                
                # Save checkpoint
                self._save_progress(section)
                
            except Exception as e:
                print(f"  ❌ Error editing {section}: {e}")
                continue
        
        # Summary
        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"✅ Manuscript editing complete!")
        print(f"   Time: {elapsed/60:.1f} minutes")
        print(f"   Sections: {len(self.completed_sections)}/{total_sections}")
        print(f"   Output: {self.output_dir}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Cloud-optimized manuscript editor")
    parser.add_argument(
        "--manuscript-dir",
        type=str,
        default="manuscript",
        help="Directory containing manuscript sections"
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=str,
        default=None,
        help="Directory for checkpoints (for spot instance recovery)"
    )
    parser.add_argument(
        "--style",
        type=str,
        default="Nature Communications",
        help="Journal style"
    )
    
    parser.add_argument(
        "--backend",
        type=str,
        choices=["qwen-cloud", "instella", "lmstudio"],
        default="lmstudio",
        help="LLM backend to use (default: lmstudio)"
    )
    
    args = parser.parse_args()

    # Setup Backend
    global llm_chat, MODEL_NAME
    
    if args.backend == "lmstudio":
        if not LMSTUDIO_AVAILABLE:
            print("❌ Error: lmstudio_client not found.")
            sys.exit(1)
        llm_chat = lmstudio_llm_chat
        MODEL_NAME = "LMStudio (Qwen3-8B)"
        print(f"🚀 Using Backend: {MODEL_NAME}")
        
    elif args.backend == "qwen-cloud":
        if not QWEN_AVAILABLE:
            print("❌ Error: qwen_client not found.")
            sys.exit(1)
        llm_chat = qwen_llm_chat
        MODEL_NAME = "Qwen2.5-32B (Cloud)"
        print(f"🚀 Using Backend: {MODEL_NAME}")
        
    elif args.backend == "instella":
        if not INSTELLA_AVAILABLE:
            print("❌ Error: instella_client not found.")
            sys.exit(1)
        llm_chat = instella_llm_chat
        MODEL_NAME = "Instella-3B (Local)"
        print(f"🚀 Using Backend: {MODEL_NAME}")

    # Initialize editor
    editor = CloudManuscriptEditor(checkpoint_dir=args.checkpoint_dir)
    
    # Process manuscript
    manuscript_dir = Path(args.manuscript_dir)
    if not manuscript_dir.exists():
        print(f"❌ Error: Manuscript directory not found: {manuscript_dir}")
        sys.exit(1)
    
    editor.process_manuscript(manuscript_dir, style=args.style)


if __name__ == "__main__":
    main()
