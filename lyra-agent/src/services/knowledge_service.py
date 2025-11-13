"""
Knowledge service - Sprint 1 version.
Simplified to just handle existing docs for style examples.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.services.vector_store import VectorStoreService
from src.utils.logger import logger
from pathlib import Path


class KnowledgeService:
    """Simplified knowledge service for Sprint 1."""
    
    def __init__(self):
        self.vector_store = VectorStoreService()
        logger.info("Knowledge Service initialized (Sprint 1)")
    
    def index_existing_docs(self, docs_directory: str = "./data/existing_docs"):
        """Index existing documentation for style examples."""
        docs_path = Path(docs_directory)
        if not docs_path.exists():
            logger.warning(f"Docs directory not found: {docs_directory}")
            return
        
        documents = []
        for doc_file in docs_path.rglob("*.md"):
            content = doc_file.read_text()
            documents.append({
                'content': content,
                'metadata': {
                    'filename': doc_file.name,
                    'path': str(doc_file),
                    'indexed_at': datetime.now().isoformat()
                }
            })
        
        if documents:
            self.vector_store.index_documents(documents, "existing_docs")
            logger.info(f"Indexed {len(documents)} existing documents")
    
    def get_style_examples(self, doc_type: str, n_examples: int = 3) -> List[str]:
        """Get style examples for a document type."""
        query = f"{doc_type} documentation example"
        results = self.vector_store.search(
            query=query,
            source_types=["existing_docs"],
            k=n_examples
        )
        
        return [r['content'] for r in results]

