"""
Indexing Module using LangChain with FAISS Vector Store
"""

from typing import List, Optional
import os
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.config import EMBEDDING_MODEL, VECTOR_STORE_TYPE


class IndexManager:
    """
    Manages document indexing and retrieval using LangChain and FAISS
    """
    
    def __init__(self, index_name: str = "document_index"):
        """
        Initialize the index manager
        
        Args:
            index_name: Name of the vector store index
        """
        self.index_name = index_name
        self.vector_store = None
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        print(f"Initialized Index Manager with type: {VECTOR_STORE_TYPE}")
    
    def create_index(self, documents: List[Document]) -> bool:
        """
        Create a vector store index from documents using LangChain
        
        Args:
            documents: List of Document objects to index
            
        Returns:
            Boolean indicating success
        """
        if not documents:
            print("No documents to index")
            return False
        
        try:
            # Create FAISS vector store from documents
            self.vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            print(f"Created index with {len(documents)} documents")
            return True
        except Exception as e:
            print(f"Error creating index: {str(e)}")
            return False
    
    def save_index(self, output_path: str = "./indexes") -> bool:
        """
        Save the vector store index to disk
        
        Args:
            output_path: Path where to save the index
            
        Returns:
            Boolean indicating success
        """
        if not self.vector_store:
            print("No index to save")
            return False
        
        try:
            os.makedirs(output_path, exist_ok=True)
            self.vector_store.save_local(output_path)
            print(f"Index saved to: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving index: {str(e)}")
            return False
    
    def load_index(self, index_path: str) -> bool:
        """
        Load a vector store index from disk
        
        Args:
            index_path: Path to the saved index
            
        Returns:
            Boolean indicating success
        """
        try:
            self.vector_store = FAISS.load_local(index_path, self.embeddings)
            print(f"Index loaded from: {index_path}")
            return True
        except Exception as e:
            print(f"Error loading index: {str(e)}")
            return False
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Search for similar documents using LangChain's similarity search
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar Document objects
        """
        if not self.vector_store:
            print("No index loaded")
            return []
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            print(f"Found {len(results)} similar documents")
            return results
        except Exception as e:
            print(f"Error during similarity search: {str(e)}")
            return []
    
    def similarity_search_with_scores(self, query: str, k: int = 4) -> List[tuple]:
        """
        Search with similarity scores
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (Document, score) tuples
        """
        if not self.vector_store:
            print("No index loaded")
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            print(f"Found {len(results)} results with scores")
            return results
        except Exception as e:
            print(f"Error during scored search: {str(e)}")
            return []
