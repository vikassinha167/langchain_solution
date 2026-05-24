"""
LangChain Configuration and Setup
"""

import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Vector Store Configuration
VECTOR_STORE_TYPE = "faiss"  # faiss, chroma, pinecone

# Evaluation Configuration
EVALUATION_METRICS = ["coherence", "relevance", "summary_length"]
