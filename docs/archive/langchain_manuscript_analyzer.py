"""
LangChain + Instella Manuscript Analyzer

Replacement for RAGFlow-based analyzer using local LangChain + ChromaDB.
"""

import os
import sys
import argparse
from typing import List, Dict, Optional
from pathlib import Path

# LangChain imports
from langchain_community.document_loaders import DirectoryLoader, TextLoader
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Import Instella client (assumes it's in the same directory)
try:
    from instella_client import instella_chat
    INSTELLA_AVAILABLE = True
except ImportError:
    INSTELLA_AVAILABLE = False
    print("⚠️  Instella client not available. Check instella_client.py and dependencies")

class ManuscriptAnalyzer:
    """Analyze manuscript using LangChain retrieval and Instella generation"""
    
    def __init__(
        self,
        manuscript_dir: str = "life/manuscript",
        persist_directory: str = "./chroma_db",
        embedding_model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize analyzer and vector store
        
        Args:
            manuscript_dir: Directory containing manuscript files
            persist_directory: Directory to persist ChromaDB
            embedding_model_name: HuggingFace embedding model name
        """
        if not INSTELLA_AVAILABLE:
            raise ImportError("Instella client not available")
            
        self.manuscript_dir = manuscript_dir
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model_name
        
        print(f"Loading embeddings: {embedding_model_name}...")
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        
        # Initialize Vector Store
        if os.path.exists(persist_directory) and os.listdir(persist_directory):
            print(f"Loading existing vector store from {persist_directory}...")
            self.vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
        else:
            print(f"Creating new vector store from {manuscript_dir}...")
            self.vector_store = self._create_vector_store()

    def _create_vector_store(self) -> Chroma:
        """Ingest documents and create vector store"""
        if not os.path.exists(self.manuscript_dir):
            print(f"⚠️  Manuscript directory not found: {self.manuscript_dir}")
            # Return empty store or raise error? Let's return empty but initialized
            return Chroma(embedding_function=self.embeddings, persist_directory=self.persist_directory)

        # Load documents (.tex and .md)
        loaders = [
            DirectoryLoader(self.manuscript_dir, glob="**/*.tex", loader_cls=TextLoader),
            DirectoryLoader(self.manuscript_dir, glob="**/*.md", loader_cls=TextLoader)
        ]
        
        documents = []
        for loader in loaders:
            try:
                docs = loader.load()
                documents.extend(docs)
            except Exception as e:
                print(f"Error loading docs: {e}")

        if not documents:
            print("No documents found to index.")
            return Chroma(embedding_function=self.embeddings, persist_directory=self.persist_directory)

        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        print(f"Indexing {len(texts)} chunks...")
        vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return vector_store

    def check_equation_consistency(self, equation_symbol: str) -> Dict:
        """Check consistency of equation usage"""
        print(f"🔍 Checking consistency for: {equation_symbol}")
        
        # Retrieve
        results = self.vector_store.similarity_search(f"usage of {equation_symbol}", k=10)
        
        # Build context
        context = "\n\n".join([
            f"**{r.metadata.get('source', 'Unknown')}**:\n{r.page_content}"
            for r in results
        ])
        
        # Analyze with Instella
        analysis = instella_chat(
            system="You are a technical editor checking equation consistency in a scientific manuscript.",
            messages=[{
                "role": "user",
                "content": f"""Analyze the consistency of '{equation_symbol}' usage across these excerpts:

{context}

Check for:
1. Consistent definition
2. Notation conflicts
3. Missing definitions
4. Inconsistent usage

Provide specific recommendations."""
            }],
            max_new_tokens=1024,
            temperature=0.2
        )
        
        return {
            "symbol": equation_symbol,
            "occurrences": len(results),
            "sources": list(set([r.metadata.get('source', 'Unknown') for r in results])),
            "analysis": analysis
        }

    def find_citation_gaps(self, section_name: str) -> List[str]:
        """Identify claims that need citations"""
        print(f"📚 Finding citation gaps in: {section_name}")
        
        # Retrieve section content (approximate by searching for section name)
        # Note: This is less precise than RAGFlow's metadata filter if we don't have strict metadata
        # But DirectoryLoader adds 'source' metadata, so we can filter if we knew the filename.
        # Assuming section_name maps to a file or content.
        
        # Try to find docs with source matching section_name
        # Chroma filter syntax: where={"source": "..."}
        # But we might not know the exact path. Let's do a similarity search for the section content first.
        
        results = self.vector_store.similarity_search(f"Content of section {section_name}", k=10)
        
        if not results:
            return []
            
        section_content = "\n\n".join([r.page_content for r in results])
        
        response = instella_chat(
            system="You are a scientific editor identifying claims that need supporting citations.",
            messages=[{
                "role": "user",
                "content": f"""Read this content (related to {section_name}) and identify specific claims that need citations:

{section_content}

List each claim that makes a factual assertion without a nearby citation.
Format: one claim per line, starting with '-'"""
            }],
            max_new_tokens=1024,
            temperature=0.3
        )
        
        claims = [
            line.strip('- ').strip()
            for line in response.split('\n')
            if line.strip().startswith('-')
        ]
        return claims

    def generate_literature_review(self, topic: str, max_length: int = 500) -> str:
        """Generate literature review"""
        print(f"📖 Generating literature review for: {topic}")
        
        results = self.vector_store.similarity_search(f"Papers and research on {topic}", k=10)
        
        context = "\n\n".join([
            f"**Source {i+1}**: {r.page_content}"
            for i, r in enumerate(results)
        ])
        
        review = instella_chat(
            system="You are writing a literature review for a scientific paper.",
            messages=[{
                "role": "user",
                "content": f"""Synthesize this literature into a {max_length}-word review on {topic}:

{context}

Write in academic style with proper flow. Cite sources as [Source N]."""
            }],
            max_new_tokens=int(max_length * 2),
            temperature=0.35
        )
        return review

    def rag_augmented_rewrite(self, section_name: str, section_content: str, style: str = "Nature Communications") -> str:
        """Rewrite section with RAG context"""
        print(f"✍️  RAG-augmented rewrite: {section_name}")
        
        results = self.vector_store.similarity_search(f"Context for {section_name}: equations, definitions", k=5)
        
        context = "\n\n".join([
            f"**{r.metadata.get('source', 'Context')}**:\n{r.page_content}"
            for r in results
        ])
        
        rewritten = instella_chat(
            system=f"""You are rewriting a section for {style}.
            
Use this context from other manuscript sections to ensure consistency:
{context}

Preserve all equations, maintain consistent notation, and ensure technical accuracy.""",
            messages=[{
                "role": "user",
                "content": f"""Rewrite this {section_name} section:

{section_content}

Improve clarity and flow while maintaining all technical content."""
            }],
            max_new_tokens=2048,
            temperature=0.35
        )
        return rewritten

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LangChain + Instella Manuscript Analyzer")
    parser.add_argument("--action", required=True, choices=[
        "check-equation",
        "citation-gaps",
        "literature-review",
        "rag-rewrite",
        "reindex"
    ])
    parser.add_argument("--input", help="Input (equation symbol, section name, topic, etc.)")
    parser.add_argument("--section-file", help="Section file for rewriting")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--manuscript-dir", default="life/manuscript", help="Directory of manuscript files")
    
    args = parser.parse_args()
    
    # If reindex, we might want to force fresh DB
    if args.action == "reindex":
        import shutil
        if os.path.exists("./chroma_db"):
            shutil.rmtree("./chroma_db")
        analyzer = ManuscriptAnalyzer(manuscript_dir=args.manuscript_dir)
        print("✅ Re-indexing complete.")
        sys.exit(0)

    analyzer = ManuscriptAnalyzer(manuscript_dir=args.manuscript_dir)
    
    if args.action == "check-equation":
        if not args.input:
            print("❌ --input required for check-equation")
            sys.exit(1)
        result = analyzer.check_equation_consistency(args.input)
        print(f"\n{'='*60}")
        print(f"Equation: {result['symbol']}")
        print(f"Occurrences: {result['occurrences']}")
        print(f"Sources: {', '.join(result['sources'])}")
        print(f"\nAnalysis:\n{result['analysis']}")
        
    elif args.action == "citation-gaps":
        if not args.input:
            print("❌ --input required for citation-gaps")
            sys.exit(1)
        claims = analyzer.find_citation_gaps(args.input)
        print(f"\n{'='*60}")
        print(f"Claims needing citations in {args.input}:")
        for claim in claims:
            print(f"  - {claim}")
            
    elif args.action == "literature-review":
        if not args.input:
            print("❌ --input required for literature-review")
            sys.exit(1)
        review = analyzer.generate_literature_review(args.input)
        print(f"\n{'='*60}")
        print(review)
        if args.output:
            Path(args.output).write_text(review)
            print(f"\n✅ Saved to {args.output}")

    elif args.action == "rag-rewrite":
        if not args.section_file:
            print("❌ --section-file required for rag-rewrite")
            sys.exit(1)
        content = Path(args.section_file).read_text()
        rewritten = analyzer.rag_augmented_rewrite(args.input or "Section", content)
        
        if args.output:
            Path(args.output).write_text(rewritten)
            print(f"✅ Saved to {args.output}")
        else:
            print(f"\n{'='*60}")
            print(rewritten)
