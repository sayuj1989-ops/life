"""
RAGFlow + Instella Manuscript Analyzer

High-level analysis tasks combining RAGFlow retrieval with Instella generation
"""

from typing import List, Dict, Optional
from pathlib import Path
import sys

# Check if RAGFlow is available
try:
    from ragflow_client import RAGFlowClient
    RAGFLOW_AVAILABLE = True
except ImportError:
    RAGFLOW_AVAILABLE = False
    print("⚠️  RAGFlow client not available. Install dependencies or check ragflow_client.py")

# Check if Instella is available
try:
    from instella_client import instella_chat
    INSTELLA_AVAILABLE = True
except ImportError:
    INSTELLA_AVAILABLE = False
    print("⚠️  Instella client not available. Check instella_client.py and dependencies")


class ManuscriptAnalyzer:
    """Analyze manuscript using RAGFlow retrieval and Instella generation"""
    
    def __init__(
        self,
        ragflow_url: str = "http://localhost",
        ragflow_email: str = "researcher@ragflow.local",
        ragflow_password: str = "ragflow123",
        kb_id: Optional[str] = None
    ):
        """
        Initialize analyzer
        
        Args:
            ragflow_url: RAGFlow server URL
            ragflow_email: RAGFlow user email
            ragflow_password: RAGFlow user password
            kb_id: Knowledge base ID (if already created)
        """
        if not RAGFLOW_AVAILABLE:
            raise ImportError("RAGFlow client not available")
        
        if not INSTELLA_AVAILABLE:
            raise ImportError("Instella client not available")
        
        self.ragflow = RAGFlowClient(
            base_url=ragflow_url,
            email=ragflow_email,
            password=ragflow_password
        )
        self.kb_id = kb_id
    
    def check_equation_consistency(self, equation_symbol: str) -> Dict:
        """
        Check consistency of equation usage across manuscript
        
        Args:
            equation_symbol: Symbol to check (e.g., "I(s)", "\\kappa")
            
        Returns:
            Dictionary with findings and recommendations
        """
        print(f"🔍 Checking consistency for: {equation_symbol}")
        
        # Retrieve all mentions
        results = self.ragflow.query(
            kb_id=self.kb_id,
            question=f"Find all uses of {equation_symbol}",
            top_k=20
        )
        
        # Build context for Instella
        context = "\n\n".join([
            f"**{r.get('metadata', {}).get('source', 'Unknown')}**:\n{r['content']}"
            for r in results
        ])
        
        # Ask Instella to analyze consistency
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
            "sources": [r.get('metadata', {}).get('source', 'Unknown') for r in results],
            "analysis": analysis
        }
    
    def find_citation_gaps(self, section_name: str) -> List[str]:
        """
        Identify claims that need citations
        
        Args:
            section_name: Section to analyze (e.g., "results")
            
        Returns:
            List of claims needing citations
        """
        print(f"📚 Finding citation gaps in: {section_name}")
        
        # Retrieve section content
        results = self.ragflow.query(
            kb_id=self.kb_id,
            question=f"Content from {section_name} section",
            top_k=10,
            filters={"source": f"{section_name}.tex"}
        )
        
        if not results:
            return []
        
        section_content = "\n\n".join([r['content'] for r in results])
        
        # Ask Instella to identify claims needing citations
        response = instella_chat(
            system="You are a scientific editor identifying claims that need supporting citations.",
            messages=[{
                "role": "user",
                "content": f"""Read this section and identify specific claims that need citations:

{section_content}

List each claim that makes a factual assertion without a nearby citation.
Format: one claim per line, starting with '-'"""
            }],
            max_new_tokens=1024,
            temperature=0.3
        )
        
        # Parse response into list
        claims = [
            line.strip('- ').strip()
            for line in response.split('\n')
            if line.strip().startswith('-')
        ]
        
        return claims
    
    def generate_literature_review(
        self,
        topic: str,
        max_length: int = 500,
        literature_kb_id: Optional[str] = None
    ) -> str:
        """
        Generate literature review using RAG + Instella
        
        Args:
            topic: Topic to review
            max_length: Maximum length in words
            literature_kb_id: Knowledge base ID for literature (if separate)
            
        Returns:
            Generated literature review text
        """
        print(f"📖 Generating literature review for: {topic}")
        
        kb_to_use = literature_kb_id or self.kb_id
        
        # Retrieve relevant literature
        results = self.ragflow.query(
            kb_id=kb_to_use,
            question=f"Papers and research on {topic}",
            top_k=15
        )
        
        # Build context
        context = "\n\n".join([
            f"**Source {i+1}**: {r['content']}"
            for i, r in enumerate(results)
        ])
        
        # Generate review with Instella
        review = instella_chat(
            system="You are writing a literature review for a scientific paper.",
            messages=[{
                "role": "user",
                "content": f"""Synthesize this literature into a {max_length}-word review on {topic}:

{context}

Write in academic style with proper flow. Cite sources as [Source N]."""
            }],
            max_new_tokens=int(max_length * 2),  # Rough token estimate
            temperature=0.35
        )
        
        return review
    
    def rag_augmented_rewrite(
        self,
        section_name: str,
        section_content: str,
        style: str = "Nature Communications"
    ) -> str:
        """
        Rewrite section with RAG-retrieved context
        
        Args:
            section_name: Name of section
            section_content: Current section content
            style: Target journal style
            
        Returns:
            Rewritten section
        """
        print(f"✍️  RAG-augmented rewrite: {section_name}")
        
        # Retrieve related content from other sections
        context_results = self.ragflow.query(
            kb_id=self.kb_id,
            question=f"Context for {section_name}: equations, definitions, related content",
            top_k=10
        )
        
        # Build context
        context = "\n\n".join([
            f"**{r.get('metadata', {}).get('source', 'Context')}**:\n{r['content']}"
            for r in context_results
        ])
        
        # Rewrite with full context
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


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="RAGFlow + Instella Manuscript Analyzer")
    parser.add_argument("--kb-id", required=True, help="RAGFlow knowledge base ID")
    parser.add_argument("--action", required=True, choices=[
        "check-equation",
        "citation-gaps",
        "literature-review",
        "rag-rewrite"
    ])
    parser.add_argument("--input", help="Input (equation symbol, section name, topic, etc.)")
    parser.add_argument("--section-file", help="Section file for rewriting")
    parser.add_argument("--output", help="Output file")
    
    args = parser.parse_args()
    
    analyzer = ManuscriptAnalyzer(kb_id=args.kb_id)
    
    if args.action == "check-equation":
        result = analyzer.check_equation_consistency(args.input)
        print(f"\n{'='*60}")
        print(f"Equation: {result['symbol']}")
        print(f"Occurrences: {result['occurrences']}")
        print(f"Sources: {', '.join(set(result['sources']))}")
        print(f"\nAnalysis:\n{result['analysis']}")
        
    elif args.action == "citation-gaps":
        claims = analyzer.find_citation_gaps(args.input)
        print(f"\n{'='*60}")
        print(f"Claims needing citations in {args.input}:")
        for claim in claims:
            print(f"  - {claim}")
        
    elif args.action == "literature-review":
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
        rewritten = analyzer.rag_augmented_rewrite(args.input, content)
        
        if args.output:
            Path(args.output).write_text(rewritten)
            print(f"✅ Saved to {args.output}")
        else:
            print(f"\n{'='*60}")
            print(rewritten)
