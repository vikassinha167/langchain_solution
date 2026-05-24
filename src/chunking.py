"""
Document Chunking Module using LangChain
"""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


class DocumentChunker:
    """
    Handles document loading and chunking using LangChain
    """
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Initialize the chunker with specified chunk size and overlap
        
        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """
        Load PDF document using LangChain PyPDFLoader
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of Document objects
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            print(f"Loaded PDF: {file_path} with {len(documents)} pages")
            return documents
        except Exception as e:
            print(f"Error loading PDF {file_path}: {str(e)}")
            return []
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks using LangChain text splitter
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects
        """
        if not documents:
            print("No documents to chunk")
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks from {len(documents)} documents")
        print(f"Average chunk size: {sum(len(chunk.page_content) for chunk in chunks) / len(chunks):.0f} characters")
        return chunks
    
    def process_pdf(self, file_path: str) -> List[Document]:
        """
        Complete pipeline: load and chunk a PDF
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of chunked Document objects
        """
        documents = self.load_pdf(file_path)
        chunks = self.chunk_documents(documents)
        return chunks
