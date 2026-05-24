"""
Main Pipeline Orchestrator using LangChain
Coordinates all components: Chunking, Embedding, Indexing, LLM Invocation, and Evaluation
"""

import os
from typing import List
from src.chunking import DocumentChunker
from src.embeddings import EmbeddingManager
from src.indexing import IndexManager
from src.llm_invoker import LLMInvoker
from src.evaluation import SummaryEvaluator, LLMBasedEvaluator


class DocumentProcessingPipeline:
    """
    End-to-end document processing pipeline using LangChain
    """
    
    def __init__(self):
        """Initialize all components"""
        self.chunker = DocumentChunker()
        self.embedding_manager = EmbeddingManager()
        self.index_manager = IndexManager()
        self.llm_invoker = LLMInvoker()
        self.evaluator = SummaryEvaluator()
        self.llm_evaluator = LLMBasedEvaluator()
        
        print("Pipeline initialized successfully")
    
    def process_single_document(self, pdf_path: str, query: str = "Summarize") -> dict:
        """
        Process a single PDF document through the entire pipeline
        
        Args:
            pdf_path: Path to the PDF file
            query: Task query (e.g., "Summarize" or specific question)
            
        Returns:
            Dictionary containing results from all pipeline stages
        """
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_path}")
        print(f"{'='*60}\n")
        
        results = {"stages": {}}
        
        # Stage 1: Chunking
        print("STAGE 1: CHUNKING")
        print("-" * 40)
        chunks = self.chunker.process_pdf(pdf_path)
        results["stages"]["chunking"] = {
            "num_chunks": len(chunks),
            "chunks": chunks
        }
        print()
        
        # Stage 2: Embedding
        print("STAGE 2: EMBEDDING")
        print("-" * 40)
        embeddings = self.embedding_manager.embed_documents(chunks)
        results["stages"]["embedding"] = {
            "num_embeddings": len(embeddings),
            "embedding_dimension": len(embeddings[0]) if embeddings else 0
        }
        print()
        
        # Stage 3: Indexing
        print("STAGE 3: INDEXING")
        print("-" * 40)
        success = self.index_manager.create_index(chunks)
        results["stages"]["indexing"] = {
            "index_created": success,
            "num_documents": len(chunks)
        }
        print()
        
        # Stage 4: LLM Invocation
        print("STAGE 4: LLM INVOCATION")
        print("-" * 40)
        
        # Retrieve relevant documents for the query
        relevant_docs = self.index_manager.similarity_search(query, k=3)
        print(f"Retrieved {len(relevant_docs)} relevant documents for the query")
        
        # Generate summary from relevant documents
        summary = self.llm_invoker.generate_summary_from_documents(relevant_docs, max_length=150)
        results["stages"]["llm_invocation"] = {
            "query": query,
            "retrieved_docs": len(relevant_docs),
            "summary": summary
        }
        print(f"Summary generated:\n{summary}\n")
        
        # Stage 5: Evaluation
        print("STAGE 5: EVALUATION")
        print("-" * 40)
        
        # Combine all original content for evaluation
        original_content = "\n\n".join([chunk.page_content for chunk in chunks])
        
        # Standard evaluation
        evaluation = self.evaluator.evaluate_summary(summary, original_content)
        results["stages"]["evaluation"] = {
            "coherence_score": evaluation["coherence_score"],
            "relevance_score": evaluation["relevance_score"],
            "compression_ratio": evaluation["compression_ratio"],
            "original_words": evaluation["original_length"],
            "summary_words": evaluation["summary_length"]
        }
        
        # Print evaluation report
        report = self.evaluator.generate_evaluation_report(evaluation)
        print(report)
        
        results["evaluation_report"] = report
        
        return results
    
    def process_multiple_documents(self, pdf_paths: List[str]) -> List[dict]:
        """
        Process multiple PDF documents
        
        Args:
            pdf_paths: List of paths to PDF files
            
        Returns:
            List of results from processing each document
        """
        results = []
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                result = self.process_single_document(pdf_path)
                results.append(result)
            else:
                print(f"Warning: File not found: {pdf_path}")
        
        return results
    
    def interactive_qa(self, pdf_path: str) -> None:
        """
        Interactive Q&A mode with a document
        
        Args:
            pdf_path: Path to the PDF file
        """
        print(f"\nInitializing Q&A session for: {pdf_path}\n")
        
        # Load and chunk the document
        chunks = self.chunker.process_pdf(pdf_path)
        
        # Create index
        self.index_manager.create_index(chunks)
        
        # Interactive loop
        while True:
            question = input("\nAsk a question (or 'exit' to quit): ").strip()
            if question.lower() == 'exit':
                break
            
            # Search for relevant documents
            relevant_docs = self.index_manager.similarity_search(question, k=3)
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Generate answer
            answer = self.llm_invoker.answer_question(question, context)
            print(f"\nAnswer: {answer}")
    
    def generate_qa_dataset(self, pdf_path: str, num_pairs: int = 5) -> List[dict]:
        """
        Generate question-answer pairs from a document for evaluation
        
        Args:
            pdf_path: Path to the PDF file
            num_pairs: Number of QA pairs to generate
            
        Returns:
            List of QA pair dictionaries
        """
        print(f"\nGenerating QA dataset from: {pdf_path}\n")
        
        # Load document
        chunks = self.chunker.process_pdf(pdf_path)
        combined_content = "\n\n".join([chunk.page_content for chunk in chunks])
        
        # Generate QA pairs
        qa_pairs = self.llm_invoker.generate_qa_pairs(combined_content, num_pairs)
        
        print(f"\nGenerated {len(qa_pairs)} QA pairs")
        return qa_pairs


def main():
    """Main execution function"""
    
    print("\n" + "="*60)
    print("LangChain Document Processing Pipeline")
    print("="*60 + "\n")
    
    # Initialize pipeline
    pipeline = DocumentProcessingPipeline()
    
    # Define PDF paths
    data_dir = "data"
    pdf_files = [
        os.path.join(data_dir, "ai_guide.pdf"),
        os.path.join(data_dir, "cloud_computing.pdf")
    ]
    
    # Check if PDFs exist, if not create them
    if not all(os.path.exists(f) for f in pdf_files):
        print("PDFs not found. Please run 'python create_pdfs.py' first\n")
        return
    
    # Process documents
    results = pipeline.process_multiple_documents(pdf_files)
    
    print("\n" + "="*60)
    print("Pipeline Execution Complete")
    print("="*60 + "\n")
    
    # Print summary
    print("EXECUTION SUMMARY:")
    for i, result in enumerate(results, 1):
        print(f"\nDocument {i}:")
        for stage, stage_result in result["stages"].items():
            print(f"  - {stage}: OK")


if __name__ == "__main__":
    main()
