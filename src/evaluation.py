"""
Evaluation Module using LangChain
"""

from typing import List, Dict, Any
import re
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


class EvaluationMetrics:
    """
    Evaluation metrics for generated summaries and content
    """
    
    @staticmethod
    def calculate_coherence(text: str) -> float:
        """
        Calculate coherence score (0-1) based on text structure
        
        Args:
            text: Text to evaluate
            
        Returns:
            Coherence score
        """
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return 0.5
        
        # Simple coherence check: presence of transition words
        transition_words = ['however', 'therefore', 'thus', 'moreover', 'furthermore', 
                          'additionally', 'consequently', 'meanwhile', 'indeed', 'rather']
        transition_count = sum(1 for word in transition_words if word.lower() in text.lower())
        
        coherence = min(0.5 + (transition_count * 0.05), 1.0)
        return round(coherence, 2)
    
    @staticmethod
    def calculate_relevance(summary: str, original: str) -> float:
        """
        Calculate relevance score by comparing key terms
        
        Args:
            summary: Generated summary
            original: Original text
            
        Returns:
            Relevance score (0-1)
        """
        summary_words = set(summary.lower().split())
        original_words = set(original.lower().split())
        
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        summary_words = summary_words - common_words
        original_words = original_words - common_words
        
        if len(original_words) == 0:
            return 0.0
        
        common = summary_words.intersection(original_words)
        relevance = len(common) / len(original_words)
        return round(min(relevance, 1.0), 2)
    
    @staticmethod
    def calculate_summary_compression_ratio(summary: str, original: str) -> float:
        """
        Calculate compression ratio
        
        Args:
            summary: Generated summary
            original: Original text
            
        Returns:
            Compression ratio (0-1), where 1 = no compression, 0 = fully compressed
        """
        summary_length = len(summary.split())
        original_length = len(original.split())
        
        if original_length == 0:
            return 0.0
        
        ratio = summary_length / original_length
        return round(ratio, 2)


class SummaryEvaluator:
    """
    Evaluates summaries using LangChain and custom metrics
    """
    
    def __init__(self):
        """Initialize the evaluator"""
        try:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
        except Exception as e:
            print(f"Error initializing evaluator LLM: {str(e)}")
            self.llm = None
    
    def evaluate_summary(self, summary: str, original_text: str) -> Dict[str, Any]:
        """
        Comprehensive evaluation of a summary
        
        Args:
            summary: Generated summary to evaluate
            original_text: Original text
            
        Returns:
            Dictionary containing evaluation metrics
        """
        evaluation = {
            "summary": summary,
            "original_length": len(original_text.split()),
            "summary_length": len(summary.split()),
            "coherence_score": EvaluationMetrics.calculate_coherence(summary),
            "relevance_score": EvaluationMetrics.calculate_relevance(summary, original_text),
            "compression_ratio": EvaluationMetrics.calculate_summary_compression_ratio(summary, original_text),
        }
        
        return evaluation
    
    def batch_evaluate(self, summaries: List[str], original_texts: List[str]) -> List[Dict[str, Any]]:
        """
        Evaluate multiple summaries
        
        Args:
            summaries: List of summaries to evaluate
            original_texts: List of original texts
            
        Returns:
            List of evaluation dictionaries
        """
        evaluations = []
        for summary, original in zip(summaries, original_texts):
            eval_result = self.evaluate_summary(summary, original)
            evaluations.append(eval_result)
        
        print(f"Evaluated {len(evaluations)} summaries")
        return evaluations
    
    def generate_evaluation_report(self, evaluation: Dict[str, Any]) -> str:
        """
        Generate a detailed evaluation report
        
        Args:
            evaluation: Evaluation dictionary
            
        Returns:
            Formatted report string
        """
        report = f"""
SUMMARY EVALUATION REPORT
{'='*50}

Original Text Length: {evaluation['original_length']} words
Summary Length: {evaluation['summary_length']} words
Compression Ratio: {evaluation['compression_ratio']} ({evaluation['compression_ratio']*100:.1f}%)

QUALITY METRICS:
- Coherence Score: {evaluation['coherence_score']}/1.0
- Relevance Score: {evaluation['relevance_score']}/1.0

GENERATED SUMMARY:
{'-'*50}
{evaluation['summary']}
{'-'*50}
"""
        return report


class LLMBasedEvaluator:
    """
    Uses LLM for semantic evaluation of summaries
    """
    
    def __init__(self):
        """Initialize the LLM-based evaluator"""
        try:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
        except Exception as e:
            print(f"Error initializing LLM evaluator: {str(e)}")
            self.llm = None
    
    def evaluate_semantic_quality(self, summary: str, original_text: str) -> Dict[str, Any]:
        """
        Evaluate semantic quality using LLM
        
        Args:
            summary: Generated summary
            original_text: Original text
            
        Returns:
            Evaluation results
        """
        if not self.llm:
            return {}
        
        try:
            prompt = PromptTemplate(
                input_variables=["summary", "original"],
                template="""Evaluate the quality of this summary based on the original text.
                
Original Text:
{original}

Summary:
{summary}

Provide your evaluation in the following format:
Accuracy: [score 0-10]
Completeness: [score 0-10]
Clarity: [score 0-10]
Overall Quality: [score 0-10]
Feedback: [brief feedback]"""
            )
            
            formatted_prompt = prompt.format(summary=summary, original=original_text)
            response = self.llm.invoke([{"role": "user", "content": formatted_prompt}])
            evaluation_text = response.content
            
            # Parse the response
            evaluation = {
                "raw_evaluation": evaluation_text,
                "accuracy": self._extract_score(evaluation_text, "Accuracy"),
                "completeness": self._extract_score(evaluation_text, "Completeness"),
                "clarity": self._extract_score(evaluation_text, "Clarity"),
                "overall_quality": self._extract_score(evaluation_text, "Overall Quality"),
            }
            
            return evaluation
        except Exception as e:
            print(f"Error in semantic evaluation: {str(e)}")
            return {}
    
    @staticmethod
    def _extract_score(text: str, metric_name: str) -> float:
        """Extract numeric score from evaluation text"""
        try:
            lines = text.split('\n')
            for line in lines:
                if metric_name.lower() in line.lower():
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        return float(numbers[0]) / 10.0
        except:
            pass
        return 0.0
