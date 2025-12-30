"""
RAGFlow API Client for Research Document Retrieval

This client provides a Python interface to RAGFlow's REST API for:
- Knowledge base management
- Document upload and parsing
- RAG-based query and retrieval
- Integration with Instella for hybrid generation
"""

import requests
from typing import List, Dict, Optional, Any
from pathlib import Path
import json


class RAGFlowClient:
    """Client for interacting with RAGFlow API"""
    
    def __init__(
        self,
        base_url: str = "http://localhost",
        api_key: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Initialize RAGFlow client
        
        Args:
            base_url: RAGFlow server URL (default: http://localhost)
            api_key: API key for authentication (if available)
            email: User email for login-based auth
            password: User password for login-based auth
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        elif email and password:
            self._login(email, password)
    
    def _login(self, email: str, password: str) -> Dict:
        """
        Login to RAGFlow and obtain session token
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Login response with token
        """
        url = f"{self.base_url}/api/login"
        response = self.session.post(url, json={
            "email": email,
            "password": password
        })
        response.raise_for_status()
        data = response.json()
        
        # Store token if provided
        if "token" in data:
            self.api_key = data["token"]
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        
        return data
    
    def health_check(self) -> bool:
        """
        Check if RAGFlow server is accessible
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    # Knowledge Base Operations
    
    def create_knowledge_base(
        self,
        name: str,
        description: str = "",
        language: str = "English",
        embedding_model: Optional[str] = None,
        chunk_method: str = "naive",
        parser_config: Optional[Dict] = None
    ) -> Dict:
        """
        Create a new knowledge base
        
        Args:
            name: Knowledge base name
            description: Description of the knowledge base
            language: Document language (default: English)
            embedding_model: Embedding model to use (default: RAGFlow default)
            chunk_method: Chunking method (naive, qa, etc.)
            parser_config: Parser configuration dict
            
        Returns:
            Created knowledge base info with ID
        """
        url = f"{self.base_url}/api/kb"
        payload = {
            "name": name,
            "description": description,
            "language": language,
            "chunk_method": chunk_method
        }
        
        if embedding_model:
            payload["embedding_model"] = embedding_model
        if parser_config:
            payload["parser_config"] = parser_config
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def list_knowledge_bases(self) -> List[Dict]:
        """
        List all knowledge bases
        
        Returns:
            List of knowledge base info dicts
        """
        url = f"{self.base_url}/api/kb"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("data", [])
    
    def get_knowledge_base(self, kb_id: str) -> Dict:
        """
        Get knowledge base details
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            Knowledge base info
        """
        url = f"{self.base_url}/api/kb/{kb_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def delete_knowledge_base(self, kb_id: str) -> Dict:
        """
        Delete a knowledge base
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            Deletion response
        """
        url = f"{self.base_url}/api/kb/{kb_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()
    
    # Document Operations
    
    def upload_document(
        self,
        kb_id: str,
        file_path: str,
        parser_type: str = "general",
        chunk_size: int = 512,
        chunk_overlap: int = 128
    ) -> Dict:
        """
        Upload document to knowledge base
        
        Args:
            kb_id: Knowledge base ID
            file_path: Path to file to upload
            parser_type: Parser type (general, academic, etc.)
            chunk_size: Chunk size in tokens
            chunk_overlap: Overlap between chunks in tokens
            
        Returns:
            Upload response with document ID
        """
        url = f"{self.base_url}/api/kb/{kb_id}/document"
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f)}
            data = {
                'parser_type': parser_type,
                'chunk_size': chunk_size,
                'chunk_overlap': chunk_overlap
            }
            response = self.session.post(url, files=files, data=data)
        
        response.raise_for_status()
        return response.json()
    
    def list_documents(self, kb_id: str) -> List[Dict]:
        """
        List documents in knowledge base
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            List of document info dicts
        """
        url = f"{self.base_url}/api/kb/{kb_id}/document"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("data", [])
    
    def get_document_status(self, kb_id: str, doc_id: str) -> Dict:
        """
        Get document parsing status
        
        Args:
            kb_id: Knowledge base ID
            doc_id: Document ID
            
        Returns:
            Document status info (parsing, ready, failed, etc.)
        """
        url = f"{self.base_url}/api/kb/{kb_id}/document/{doc_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def delete_document(self, kb_id: str, doc_id: str) -> Dict:
        """
        Delete document from knowledge base
        
        Args:
            kb_id: Knowledge base ID
            doc_id: Document ID
            
        Returns:
            Deletion response
        """
        url = f"{self.base_url}/api/kb/{kb_id}/document/{doc_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()
    
    # Query and Retrieval
    
    def query(
        self,
        kb_id: str,
        question: str,
        top_k: int = 5,
        similarity_threshold: float = 0.0,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Query knowledge base and retrieve relevant chunks
        
        Args:
            kb_id: Knowledge base ID
            question: Query text
            top_k: Number of chunks to retrieve
            similarity_threshold: Minimum similarity score (0.0-1.0)
            filters: Optional filters (e.g., {"source": "introduction.tex"})
            
        Returns:
            List of retrieved chunks with content, metadata, and scores
        """
        url = f"{self.base_url}/api/kb/{kb_id}/retrieval"
        payload = {
            "question": question,
            "top_k": top_k,
            "similarity_threshold": similarity_threshold
        }
        
        if filters:
            payload["filters"] = filters
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("data", [])
    
    def chat(
        self,
        kb_id: str,
        question: str,
        conversation_id: Optional[str] = None,
        stream: bool = False
    ) -> Dict:
        """
        Chat with knowledge base (RAG-based Q&A)
        
        Args:
            kb_id: Knowledge base ID
            question: User question
            conversation_id: Optional conversation ID for context
            stream: Whether to stream response
            
        Returns:
            Chat response with answer and sources
        """
        url = f"{self.base_url}/api/kb/{kb_id}/chat"
        payload = {
            "question": question,
            "stream": stream
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    # Utility Methods
    
    def batch_upload(
        self,
        kb_id: str,
        file_paths: List[str],
        parser_type: str = "general",
        verbose: bool = True
    ) -> List[Dict]:
        """
        Upload multiple documents to knowledge base
        
        Args:
            kb_id: Knowledge base ID
            file_paths: List of file paths to upload
            parser_type: Parser type for all files
            verbose: Print progress messages
            
        Returns:
            List of upload responses
        """
        results = []
        for i, file_path in enumerate(file_paths, 1):
            if verbose:
                print(f"Uploading {i}/{len(file_paths)}: {Path(file_path).name}")
            
            try:
                result = self.upload_document(kb_id, file_path, parser_type)
                results.append(result)
            except Exception as e:
                if verbose:
                    print(f"  ❌ Failed: {e}")
                results.append({"error": str(e), "file": file_path})
        
        return results
    
    def wait_for_parsing(
        self,
        kb_id: str,
        doc_id: str,
        timeout: int = 300,
        poll_interval: int = 5
    ) -> Dict:
        """
        Wait for document parsing to complete
        
        Args:
            kb_id: Knowledge base ID
            doc_id: Document ID
            timeout: Maximum wait time in seconds
            poll_interval: Polling interval in seconds
            
        Returns:
            Final document status
        """
        import time
        
        elapsed = 0
        while elapsed < timeout:
            status = self.get_document_status(kb_id, doc_id)
            
            if status.get("status") == "ready":
                return status
            elif status.get("status") == "failed":
                raise Exception(f"Document parsing failed: {status.get('error')}")
            
            time.sleep(poll_interval)
            elapsed += poll_interval
        
        raise TimeoutError(f"Document parsing timeout after {timeout}s")


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = RAGFlowClient(
        base_url="http://localhost",
        email="researcher@ragflow.local",
        password="ragflow123"
    )
    
    # Check health
    print("RAGFlow health:", "✅ OK" if client.health_check() else "❌ Failed")
    
    # Create knowledge base
    kb = client.create_knowledge_base(
        name="BCC Manuscript Test",
        description="Test knowledge base for Biological Counter-Curvature manuscript"
    )
    print(f"Created KB: {kb.get('id')}")
    
    # Upload a document
    # result = client.upload_document(
    #     kb_id=kb['id'],
    #     file_path="/Users/mac/LIFE/draft_intro_BCC.md"
    # )
    # print(f"Uploaded document: {result.get('id')}")
    
    # Query the knowledge base
    # results = client.query(
    #     kb_id=kb['id'],
    #     question="What is Information-Elasticity Coupling?",
    #     top_k=3
    # )
    # print(f"Retrieved {len(results)} chunks")
