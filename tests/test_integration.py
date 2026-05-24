"""
Integration Tests for LangChain Document Processing Pipeline
"""

import unittest
import os
from src.pipeline import DocumentProcessingPipeline


class TestDocumentProcessingPipeline(unittest.TestCase):
    """Integration tests for the complete pipeline"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for the class"""
        cls.pipeline = DocumentProcessingPipeline()
        cls.test_pdf = "data/ai_guide.pdf"
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization"""
        self.assertIsNotNone(self.pipeline)
        self.assertIsNotNone(self.pipeline.chunker)
        self.assertIsNotNone(self.pipeline.embedding_manager)
        self.assertIsNotNone(self.pipeline.index_manager)
        self.assertIsNotNone(self.pipeline.llm_invoker)
        self.assertIsNotNone(self.pipeline.evaluator)
    
    def test_process_single_document(self):
        """Test processing a single document through the pipeline"""
        if not os.path.exists(self.test_pdf):
            self.skipTest("Test PDF not found")
        
        result = self.pipeline.process_single_document(self.test_pdf, query="Summarize")
        
        # Verify all stages are present
        self.assertIn("stages", result)
        self.assertIn("chunking", result["stages"])
        self.assertIn("embedding", result["stages"])
        self.assertIn("indexing", result["stages"])
        self.assertIn("llm_invocation", result["stages"])
        self.assertIn("evaluation", result["stages"])
        
        # Verify chunking stage
        self.assertGreater(result["stages"]["chunking"]["num_chunks"], 0)
        
        # Verify embedding stage
        self.assertGreater(result["stages"]["embedding"]["num_embeddings"], 0)
        self.assertGreater(result["stages"]["embedding"]["embedding_dimension"], 0)
        
        # Verify indexing stage
        self.assertTrue(result["stages"]["indexing"]["index_created"])
        
        # Verify LLM invocation stage
        self.assertIn("summary", result["stages"]["llm_invocation"])
        self.assertGreater(len(result["stages"]["llm_invocation"]["summary"]), 0)
        
        # Verify evaluation stage
        self.assertIn("coherence_score", result["stages"]["evaluation"])
        self.assertIn("relevance_score", result["stages"]["evaluation"])
        self.assertIn("compression_ratio", result["stages"]["evaluation"])
    
    def test_pipeline_output_consistency(self):
        """Test that pipeline produces consistent outputs"""
        if not os.path.exists(self.test_pdf):
            self.skipTest("Test PDF not found")
        
        result1 = self.pipeline.process_single_document(self.test_pdf, query="Summarize")
        result2 = self.pipeline.process_single_document(self.test_pdf, query="Summarize")
        
        # Both runs should have same stages
        self.assertEqual(
            set(result1["stages"].keys()),
            set(result2["stages"].keys())
        )
        
        # Evaluation metrics should be similar (allowing for small variations)
        eval1 = result1["stages"]["evaluation"]
        eval2 = result2["stages"]["evaluation"]
        
        self.assertEqual(eval1["original_words"], eval2["original_words"])
        self.assertEqual(eval1["compression_ratio"], eval2["compression_ratio"])


class TestProcessingPipelineWithMultipleDocuments(unittest.TestCase):
    """Test pipeline with multiple documents"""
    
    def test_process_multiple_documents(self):
        """Test processing multiple documents"""
        pipeline = DocumentProcessingPipeline()
        pdf_paths = ["data/ai_guide.pdf", "data/cloud_computing.pdf"]
        
        # Check if test files exist
        if not all(os.path.exists(p) for p in pdf_paths):
            self.skipTest("Test PDF files not found")
        
        results = pipeline.process_multiple_documents(pdf_paths)
        
        # Verify results
        self.assertEqual(len(results), 2)
        
        for result in results:
            self.assertIn("stages", result)
            self.assertIn("evaluation_report", result)


def run_integration_tests():
    """Run all integration tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentProcessingPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestProcessingPipelineWithMultipleDocuments))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_integration_tests()
    exit(0 if result.wasSuccessful() else 1)
