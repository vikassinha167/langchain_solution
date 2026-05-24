"""
LLM Invocation Module using LangChain
"""

from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import Document, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from src.config import LLM_MODEL


class LLMInvoker:
    """
    Manages LLM interactions using LangChain
    """
    
    def __init__(self, model_name: str = LLM_MODEL, temperature: float = 0.7):
        """
        Initialize the LLM invoker
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Sampling temperature (0-1)
        """
        try:
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                max_tokens=1024
            )
            print(f"Initialized LLM with model: {model_name}")
        except Exception as e:
            print(f"Error initializing LLM: {str(e)}")
            self.llm = None
    
    def generate_summary(self, content: str, max_length: int = 150) -> str:
        """
        Generate a summary of the provided content
        
        Args:
            content: Text content to summarize
            max_length: Maximum length of summary in words
            
        Returns:
            Generated summary
        """
        if not self.llm:
            return "LLM not initialized"
        
        try:
            prompt = PromptTemplate(
                input_variables=["content", "max_length"],
                template="""Please provide a concise summary of the following text in approximately {max_length} words.
Focus on the key points and main ideas.

Text:
{content}

Summary:"""
            )
            
            formatted_prompt = prompt.format(content=content, max_length=max_length)
            messages = [HumanMessage(content=formatted_prompt)]
            
            response = self.llm.invoke(messages)
            summary = response.content
            print(f"Generated summary with {len(summary.split())} words")
            return summary
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return ""
    
    def generate_summary_from_documents(self, documents: List[Document], max_length: int = 150) -> str:
        """
        Generate a summary from multiple documents
        
        Args:
            documents: List of Document objects
            max_length: Maximum length of summary in words
            
        Returns:
            Generated summary
        """
        if not documents:
            return "No documents provided"
        
        combined_content = "\n\n".join([doc.page_content for doc in documents])
        return self.generate_summary(combined_content, max_length)
    
    def answer_question(self, question: str, context: str) -> str:
        """
        Answer a question based on provided context
        
        Args:
            question: The question to answer
            context: Context/background information
            
        Returns:
            Generated answer
        """
        if not self.llm:
            return "LLM not initialized"
        
        try:
            prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
            )
            
            formatted_prompt = prompt.format(context=context, question=question)
            messages = [HumanMessage(content=formatted_prompt)]
            
            response = self.llm.invoke(messages)
            answer = response.content
            print(f"Generated answer with {len(answer.split())} words")
            return answer
        except Exception as e:
            print(f"Error answering question: {str(e)}")
            return ""
    
    def generate_qa_pairs(self, content: str, num_pairs: int = 3) -> List[dict]:
        """
        Generate question-answer pairs from content
        
        Args:
            content: Text content
            num_pairs: Number of QA pairs to generate
            
        Returns:
            List of QA pair dictionaries
        """
        if not self.llm:
            return []
        
        try:
            prompt = PromptTemplate(
                input_variables=["content", "num_pairs"],
                template="""Based on the following text, generate {num_pairs} important question-answer pairs.
Format each pair as:
Q: [question]
A: [answer]

Text:
{content}

Questions and Answers:"""
            )
            
            formatted_prompt = prompt.format(content=content, num_pairs=num_pairs)
            messages = [HumanMessage(content=formatted_prompt)]
            
            response = self.llm.invoke(messages)
            response_text = response.content
            
            qa_pairs = []
            pairs = response_text.split("Q:")
            for pair in pairs[1:]:
                if "A:" in pair:
                    q, a = pair.split("A:", 1)
                    qa_pairs.append({
                        "question": q.strip(),
                        "answer": a.strip()
                    })
            
            print(f"Generated {len(qa_pairs)} QA pairs")
            return qa_pairs
        except Exception as e:
            print(f"Error generating QA pairs: {str(e)}")
            return []
