"""
Unit Tests for LangChain Document Processing Pipeline
"""

import unittest
import os
from pathlib import Path
from src.chunking import DocumentChunker
from src.embeddings import EmbeddingManager
from src.indexing import IndexManager
from src.llm_invoker import LLMInvoker
from src.evaluation import EvaluationMetrics, SummaryEvaluator


class TestDocumentChunker(unittest.TestCase):
    """Test cases for DocumentChunker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chunker = DocumentChunker(chunk_size=500, chunk_overlap=100)
    
    def test_chunker_initialization(self):
        """Test chunker initialization"""
        self.assertIsNotNone(self.chunker)
        self.assertEqual(self.chunker.chunk_size, 500)
        self.assertEqual(self.chunker.chunk_overlap, 100)
    
    def test_load_pdf(self):
        """Test PDF loading"""
        pdf_path = "data/ai_guide.pdf"
        if os.path.exists(pdf_path):
            documents = self.chunker.load_pdf(pdf_path)
            self.assertGreater(len(documents), 0)
        else:
            self.skipTest("PDF file not found")
    
    def test_chunk_documents(self):
        """Test document chunking"""
        pdf_path = "data/ai_guide.pdf"
        if os.path.exists(pdf_path):
            documents = self.chunker.load_pdf(pdf_path)
            chunks = self.chunker.chunk_documents(documents)
            self.assertGreater(len(chunks), 0)
            # Check that chunks are not too large
            for chunk in chunks:
                self.assertLessEqual(len(chunk.page_content), self.chunker.chunk_size + self.chunker.chunk_overlap)
        else:
            self.skipTest("PDF file not found")


class TestEmbeddingManager(unittest.TestCase):
    """Test cases for EmbeddingManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.embedding_manager = EmbeddingManager()
    
    def test_embedding_manager_initialization(self):
        """Test embedding manager initialization"""
        self.assertIsNotNone(self.embedding_manager)


class TestEvaluationMetrics(unittest.TestCase):
    """Test cases for Evaluation Metrics"""
    
    def test_coherence_calculation(self):
        """Test coherence score calculation"""
        text = "This is a sentence. However, this is another. Therefore, we can conclude."
        score = EvaluationMetrics.calculate_coherence(text)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_relevance_calculation(self):
        """Test relevance score calculation"""
        summary = "The cat sat on the mat."
        original = "The cat and the dog sat on the mat and played together."
        score = EvaluationMetrics.calculate_relevance(summary, original)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_compression_ratio(self):
        """Test compression ratio calculation"""
        summary = "Short text."
        original = "This is a much longer text that contains many more words than the summary."
        ratio = EvaluationMetrics.calculate_summary_compression_ratio(summary, original)
        self.assertGreaterEqual(ratio, 0.0)
        self.assertLessEqual(ratio, 1.0)
        self.assertLess(ratio, 1.0)  # Summary should be shorter


class TestSummaryEvaluator(unittest.TestCase):
    """Test cases for SummaryEvaluator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.evaluator = SummaryEvaluator()
    
    def test_evaluate_summary(self):
        """Test summary evaluation"""
        summary = "AI is transformative technology."
        original = "Artificial Intelligence is a transformative technology that is changing many industries."
        
        evaluation = self.evaluator.evaluate_summary(summary, original)
        
        self.assertIn("coherence_score", evaluation)
        self.assertIn("relevance_score", evaluation)
        self.assertIn("compression_ratio", evaluation)
        self.assertIn("summary_length", evaluation)
        self.assertIn("original_length", evaluation)
    
    def test_batch_evaluate(self):
        """Test batch evaluation"""
        summaries = ["AI is important.", "Cloud is scalable."]
        originals = [
            "Artificial Intelligence is an important technology.",
            "Cloud computing provides scalable solutions."
        ]
        
        evaluations = self.evaluator.batch_evaluate(summaries, originals)
        self.assertEqual(len(evaluations), 2)
    
    def test_generate_evaluation_report(self):
        """Test evaluation report generation"""
        evaluation = {
            "summary": "Test summary.",
            "original_length": 100,
            "summary_length": 25,
            "coherence_score": 0.8,
            "relevance_score": 0.75,
            "compression_ratio": 0.25
        }
        
        report = self.evaluator.generate_evaluation_report(evaluation)
        self.assertIn("SUMMARY EVALUATION REPORT", report)
        self.assertIn("Coherence Score", report)
        self.assertIn("Relevance Score", report)


class TestIndexManager(unittest.TestCase):
    """Test cases for IndexManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.index_manager = IndexManager()
    
    def test_index_manager_initialization(self):
        """Test index manager initialization"""
        self.assertIsNotNone(self.index_manager)
        self.assertIsNotNone(self.index_manager.embeddings)


class TestLLMInvoker(unittest.TestCase):
    """Test cases for LLMInvoker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.llm_invoker = LLMInvoker(temperature=0.5)
    
    def test_llm_invoker_initialization(self):
        """Test LLM invoker initialization"""
        self.assertIsNotNone(self.llm_invoker)


def run_unit_tests():
    """Run all unit tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentChunker))
    suite.addTests(loader.loadTestsFromTestCase(TestEmbeddingManager))
    suite.addTests(loader.loadTestsFromTestCase(TestEvaluationMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestSummaryEvaluator))
    suite.addTests(loader.loadTestsFromTestCase(TestIndexManager))
    suite.addTests(loader.loadTestsFromTestCase(TestLLMInvoker))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_unit_tests()
    exit(0 if result.wasSuccessful() else 1)
