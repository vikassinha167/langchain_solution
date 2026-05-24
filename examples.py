"""
Example usage of the LangChain Document Processing Pipeline
"""

import os
from src.pipeline import DocumentProcessingPipeline


def example_basic_usage():
    """Basic usage example"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Pipeline Usage")
    print("="*60)
    
    pipeline = DocumentProcessingPipeline()
    
    pdf_path = "data/ai_guide.pdf"
    if os.path.exists(pdf_path):
        result = pipeline.process_single_document(pdf_path)
        print("\nPipeline execution completed successfully!")
    else:
        print(f"PDF not found: {pdf_path}")


def example_with_custom_query():
    """Example with custom query"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Query Processing")
    print("="*60)
    
    pipeline = DocumentProcessingPipeline()
    
    pdf_path = "data/cloud_computing.pdf"
    if os.path.exists(pdf_path):
        result = pipeline.process_single_document(
            pdf_path, 
            query="What are the main cloud service models?"
        )
        print("\nCustom query processing completed!")
    else:
        print(f"PDF not found: {pdf_path}")


def example_qa_generation():
    """Example of QA pair generation"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Question-Answer Pair Generation")
    print("="*60)
    
    pipeline = DocumentProcessingPipeline()
    
    pdf_path = "data/ai_guide.pdf"
    if os.path.exists(pdf_path):
        qa_pairs = pipeline.generate_qa_dataset(pdf_path, num_pairs=3)
        
        print(f"\nGenerated {len(qa_pairs)} Q&A pairs:\n")
        for i, pair in enumerate(qa_pairs, 1):
            print(f"Pair {i}:")
            print(f"Q: {pair['question']}")
            print(f"A: {pair['answer']}\n")
    else:
        print(f"PDF not found: {pdf_path}")


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    # example_with_custom_query()
    # example_qa_generation()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
