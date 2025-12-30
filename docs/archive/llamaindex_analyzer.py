"""
LlamaIndex + Instella Manuscript Analyzer

Advanced manuscript analysis using LlamaIndex for better structure understanding
and Instella for intelligent critique.
"""

import os
import sys
import argparse
from typing import List, Any, Optional, Dict
from pathlib import Path

# LlamaIndex imports
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    Document
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.llms import CustomLLM, LLMMetadata, CompletionResponse, CompletionResponseGen
from llama_index.core.llms.callbacks import llm_completion_callback
import chromadb

# Import Instella client
try:
    from instella_client import instella_chat
    INSTELLA_AVAILABLE = True
except ImportError:
    INSTELLA_AVAILABLE = False
    print("⚠️  Instella client not available.")

# Custom LLM Wrapper for Instella
class InstellaLlamaLLM(CustomLLM):
    context_window: int = 120000
    num_output: int = 2048
    model_name: str = "instella-3b-long"
    
    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = instella_chat(
            system="You are a helpful AI research assistant.",
            messages=[{"role": "user", "content": prompt}],
            max_new_tokens=self.num_output,
            temperature=kwargs.get("temperature", 0.1)
        )
        return CompletionResponse(text=response)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        # Basic implementation, not truly streaming for now to keep it simple
        response = self.complete(prompt, **kwargs)
        yield response

class LlamaIndexAnalyzer:
    def __init__(
        self,
        manuscript_dir: str = "life/manuscript",
        persist_dir: str = "./chroma_db_llama",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        if not INSTELLA_AVAILABLE:
            raise ImportError("Instella client required")
            
        self.manuscript_dir = manuscript_dir
        self.persist_dir = persist_dir
        
        # Configure Settings
        Settings.llm = InstellaLlamaLLM()
        Settings.embed_model = HuggingFaceEmbedding(model_name=embedding_model)
        
        # Initialize/Load Index
        self.index = self._initialize_index()
        self.query_engine = self.index.as_query_engine(similarity_top_k=5)

    def _initialize_index(self) -> VectorStoreIndex:
        # ChromaDB setup
        db = chromadb.PersistentClient(path=self.persist_dir)
        chroma_collection = db.get_or_create_collection("manuscript_collection")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Check if already indexed (naive check: if collection has items)
        if chroma_collection.count() > 0:
            print(f"Loading existing index from {self.persist_dir}...")
            return VectorStoreIndex.from_vector_store(
                vector_store,
                storage_context=storage_context
            )
        
        print(f"Indexing documents from {self.manuscript_dir}...")
        documents = SimpleDirectoryReader(
            self.manuscript_dir,
            recursive=True,
            required_exts=[".tex", ".md"]
        ).load_data()
        
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context
        )
        print(f"Indexed {len(documents)} documents.")
        return index

    def analyze_structure(self) -> str:
        """Analyze the logical flow of the manuscript"""
        print("🔍 Analyzing manuscript structure...")
        response = self.query_engine.query(
            "Analyze the overall structure of the manuscript based on the provided sections. "
            "Does the flow from Introduction to Theory to Methods to Results to Discussion make logical sense? "
            "Identify any disjointed transitions."
        )
        return str(response)

    def cross_reference_check(self) -> str:
        """Check for broken or missing internal references"""
        print("🔗 Checking cross-references...")
        response = self.query_engine.query(
            "Identify any missing internal references or vague pointers like 'as mentioned above' "
            "where the antecedent is unclear. List specific instances."
        )
        return str(response)

    def deep_consistency_check(self, topic: str) -> str:
        """Deep consistency check on a specific topic"""
        print(f"🔬 Deep consistency check for: {topic}")
        response = self.query_engine.query(
            f"Perform a deep consistency check on '{topic}'. "
            "Compare how it is defined in the Theory section versus how it is applied in Results. "
            "Are there contradictions or notation changes?"
        )
        return str(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LlamaIndex Manuscript Analyzer")
    parser.add_argument("--action", required=True, choices=[
        "structure", "cross-ref", "consistency", "reindex"
    ])
    parser.add_argument("--topic", help="Topic for consistency check")
    parser.add_argument("--dir", default="life/manuscript", help="Manuscript directory")
    
    args = parser.parse_args()
    
    if args.action == "reindex":
        import shutil
        if os.path.exists("./chroma_db_llama"):
            shutil.rmtree("./chroma_db_llama")
        analyzer = LlamaIndexAnalyzer(manuscript_dir=args.dir)
        print("✅ Re-indexing complete.")
        sys.exit(0)

    analyzer = LlamaIndexAnalyzer(manuscript_dir=args.dir)
    
    if args.action == "structure":
        print(f"\n{'='*60}\nStructure Analysis\n{'='*60}")
        print(analyzer.analyze_structure())
        
    elif args.action == "cross-ref":
        print(f"\n{'='*60}\nCross-Reference Check\n{'='*60}")
        print(analyzer.cross_reference_check())
        
    elif args.action == "consistency":
        if not args.topic:
            print("❌ --topic required for consistency check")
            sys.exit(1)
        print(f"\n{'='*60}\nConsistency Check: {args.topic}\n{'='*60}")
        print(analyzer.deep_consistency_check(args.topic))
