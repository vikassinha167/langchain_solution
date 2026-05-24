"""
Embedding Module using LangChain
"""

from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from src.config import EMBEDDING_MODEL


class EmbeddingManager:
    """
    Manages document embeddings using LangChain
    """
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        Initialize the embedding manager
        
        Args:
            model_name: Name of the embedding model to use
        """
        try:
            self.embeddings = OpenAIEmbeddings(model=model_name)
            print(f"Initialized OpenAI Embeddings with model: {model_name}")
        except Exception as e:
            print(f"Error initializing embeddings: {str(e)}")
            self.embeddings = None
    
    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of embedding vectors
        """
        if not self.embeddings:
            print("Embeddings not initialized")
            return []
        
        try:
            texts = [doc.page_content for doc in documents]
            embeddings = self.embeddings.embed_documents(texts)
            print(f"Generated embeddings for {len(embeddings)} documents")
            print(f"Embedding dimension: {len(embeddings[0]) if embeddings else 0}")
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            return []
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a query string
        
        Args:
            query: Query text
            
        Returns:
            Embedding vector for the query
        """
        if not self.embeddings:
            print("Embeddings not initialized")
            return []
        
        try:
            embedding = self.embeddings.embed_query(query)
            print(f"Generated query embedding with dimension: {len(embedding)}")
            return embedding
        except Exception as e:
            print(f"Error embedding query: {str(e)}")
            return []
