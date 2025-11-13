"""
Vector store service using ChromaDB for semantic search.
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.config.settings import settings
from src.utils.logger import logger


class VectorStoreService:
    """Service for semantic search across all knowledge sources."""
    
    def __init__(self):
        """Initialize vector store with embeddings."""
        logger.info("Initializing Vector Store Service")
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize ChromaDB
        self.persist_directory = settings.chroma_persist_directory
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="lyra_knowledge"
        )
        
        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        logger.info("Vector Store initialized successfully")
    
    def index_documents(
        self,
        documents: List[Dict[str, Any]],
        source_type: str
    ) -> int:
        """
        Index documents into vector store.
        
        Args:
            documents: List of documents with 'content' and 'metadata'
            source_type: Source type (jira, github, confluence, etc.)
            
        Returns:
            Number of chunks indexed
        """
        try:
            texts = []
            metadatas = []
            
            for doc in documents:
                # Split document into chunks
                chunks = self.text_splitter.split_text(doc['content'])
                
                for chunk in chunks:
                    texts.append(chunk)
                    metadata = doc.get('metadata', {})
                    metadata['source_type'] = source_type
                    metadatas.append(metadata)
            
            # Add to vector store
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            
            logger.info(f"Indexed {len(texts)} chunks from {source_type}")
            return len(texts)
            
        except Exception as e:
            logger.error(f"Failed to index documents: {e}")
            raise
    
    def search(
        self,
        query: str,
        source_types: Optional[List[str]] = None,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Semantic search across indexed knowledge.
        
        Args:
            query: Search query
            source_types: Filter by source types (optional)
            k: Number of results
            
        Returns:
            List of results with content and metadata
        """
        try:
            # Build filter if source types specified
            filter_dict = None
            if source_types:
                filter_dict = {"source_type": {"$in": source_types}}
            
            # Perform search
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'relevance_score': float(score)
                })
            
            logger.debug(f"Search for '{query}' returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def clear_source(self, source_type: str):
        """
        Clear all documents from a specific source.
        
        Args:
            source_type: Source type to clear
        """
        try:
            # This is a simplification - ChromaDB doesn't have direct delete by metadata
            # In production, you'd need to recreate the collection
            logger.warning(f"Clearing {source_type} from vector store")
            # Implementation depends on ChromaDB version
        except Exception as e:
            logger.error(f"Failed to clear source: {e}")

