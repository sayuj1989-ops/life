#!/usr/bin/env python3
"""
Upload BCC Manuscript to RAGFlow Knowledge Base
"""
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ragflow_client import RAGFlowClient

def main():
    print("=" * 60)
    print("BCC Manuscript Upload to RAGFlow")
    print("=" * 60)
    print()
    
    # Initialize client
    print("🔌 Connecting to RAGFlow...")
    try:
        client = RAGFlowClient(
            base_url="http://localhost",
            email="researcher@ragflow.local",
            password="ragflow123"
        )
        print("✅ Connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check RAGFlow is running: docker ps | grep ragflow")
        print("2. Check user exists: docker exec <container> python create_user.py")
        return 1
    
    print()
    
    # Create knowledge base
    print("📚 Creating knowledge base...")
    try:
        kb = client.create_knowledge_base(
            name="BCC Manuscript",
            description="Biological Counter-Curvature: Information-Elasticity Coupling Framework for Spinal Geometry",
            language="English",
            chunk_method="naive"
        )
        kb_id = kb.get('id') or kb.get('data', {}).get('id')
        print(f"✅ Knowledge base created: {kb_id}")
    except Exception as e:
        # KB might already exist
        print(f"⚠️  KB creation note: {e}")
        print("Attempting to find existing KB...")
        try:
            kbs = client.list_knowledge_bases()
            bcc_kb = [k for k in kbs if 'BCC' in k.get('name', '')]
            if bcc_kb:
                kb_id = bcc_kb[0].get('id')
                print(f"✅ Using existing KB: {kb_id}")
            else:
                print("❌ No BCC knowledge base found")
                return 1
        except Exception as e2:
            print(f"❌ Failed to list KBs: {e2}")
            return 1
    
    print()
    
    # Define files to upload
    manuscript_dir = Path("/Users/mac/LIFE/life/manuscript")
    sections_dir = manuscript_dir / "sections"
    
    files_to_upload = [
        # LaTeX sections (priority)
        (sections_dir / "introduction.tex", "general"),
        (sections_dir / "theory.tex", "general"),
        (sections_dir / "methods.tex", "general"),
        (sections_dir / "results.tex", "general"),
        (sections_dir / "discussion.tex", "general"),
        (sections_dir / "conclusion.tex", "general"),
        (sections_dir / "abstract.tex", "general"),
        
        # Draft markdown files
        (Path("/Users/mac/LIFE/draft_intro_BCC.md"), "general"),
        (Path("/Users/mac/LIFE/draft_theory_BCC.md"), "general"),
        (Path("/Users/mac/LIFE/draft_methods_BCC.md"), "general"),
        (Path("/Users/mac/LIFE/draft_results_BCC.md"), "general"),
        (Path("/Users/mac/LIFE/draft_discussion_BCC.md"), "general"),
        
        # Planning documents
        (Path("/Users/mac/LIFE/TARGET_OUTLINE_BCC.md"), "general"),
        (Path("/Users/mac/LIFE/MANUSCRIPT_PLAN_BCC.md"), "general"),
    ]
    
    # Upload files
    print(f"📤 Uploading {len(files_to_upload)} files...")
    print()
    
    uploaded = 0
    failed = 0
    
    for file_path, parser_type in files_to_upload:
        if not file_path.exists():
            print(f"⏭️  Skipping (not found): {file_path.name}")
            continue
        
        try:
            print(f"📄 Uploading: {file_path.name}...", end=" ")
            result = client.upload_document(
                kb_id=kb_id,
                file_path=str(file_path),
                parser_type=parser_type,
                chunk_size=512,
                chunk_overlap=128
            )
            print("✅")
            uploaded += 1
        except Exception as e:
            print(f"❌ {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Upload Summary:")
    print(f"  ✅ Uploaded: {uploaded}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📚 Knowledge Base ID: {kb_id}")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"1. Access RAGFlow at: http://localhost")
    print(f"2. Login with: researcher@ragflow.local / ragflow123")
    print(f"3. View knowledge base: BCC Manuscript")
    print(f"4. Run analysis:")
    print(f"   python3 ragflow_manuscript_analyzer.py --kb-id {kb_id} --action check-equation --input 'I(s)'")
    print()
    
    # Save KB ID for future use
    kb_id_file = Path("/Users/mac/LIFE/.ragflow_kb_id")
    kb_id_file.write_text(kb_id)
    print(f"💾 KB ID saved to: {kb_id_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
