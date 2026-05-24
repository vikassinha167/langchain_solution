# API Reference - LangChain GenAI Solution

## Table of Contents
1. [DocumentChunker](#documentchunker)
2. [EmbeddingManager](#embeddingmanager)
3. [IndexManager](#indexmanager)
4. [LLMInvoker](#llminvoker)
5. [SummaryEvaluator](#summaryeluator)
6. [LLMBasedEvaluator](#llmbasedevaluator)
7. [DocumentProcessingPipeline](#documentprocessingpipeline)

---

## DocumentChunker

**Module**: `src.chunking`

### Purpose
Loads PDF documents and splits them into manageable chunks.

### Methods

#### `__init__(chunk_size: int = 1000, chunk_overlap: int = 200)`
Initialize the chunker with chunk parameters.

```python
from src.chunking import DocumentChunker

chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
```

#### `load_pdf(file_path: str) -> List[Document]`
Load a PDF file and return Document objects.

```python
documents = chunker.load_pdf("data/document.pdf")
# Returns: List of Document objects, one per page
```

**Returns**: `List[Document]` - Each element contains page content and metadata

#### `chunk_documents(documents: List[Document]) -> List[Document]`
Split documents into overlapping chunks.

```python
chunks = chunker.chunk_documents(documents)
# Returns: Smaller Document objects with chunk text
```

**Returns**: `List[Document]` - Chunked documents

#### `process_pdf(file_path: str) -> List[Document]`
Complete pipeline: load PDF and chunk it.

```python
chunks = chunker.process_pdf("data/document.pdf")
# Combines load_pdf() and chunk_documents()
```

**Returns**: `List[Document]` - Chunked documents from PDF

---

## EmbeddingManager

**Module**: `src.embeddings`

### Purpose
Generate vector embeddings for documents and queries using OpenAI.

### Methods

#### `__init__(model_name: str = "text-embedding-3-small")`
Initialize the embedding manager.

```python
from src.embeddings import EmbeddingManager

embedder = EmbeddingManager(model_name="text-embedding-3-small")
```

#### `embed_documents(documents: List[Document]) -> List[List[float]]`
Generate embeddings for multiple documents.

```python
embeddings = embedder.embed_documents(chunks)
# Returns: List of embedding vectors (1536-dimensional)
```

**Returns**: `List[List[float]]` - 2D array of embeddings

#### `embed_query(query: str) -> List[float]`
Generate embedding for a single query string.

```python
query_embedding = embedder.embed_query("What is AI?")
# Returns: 1536-dimensional vector
```

**Returns**: `List[float]` - Query embedding vector

---

## IndexManager

**Module**: `src.indexing`

### Purpose
Build and manage FAISS vector indices for similarity search.

### Methods

#### `__init__(index_name: str = "document_index")`
Initialize the index manager.

```python
from src.indexing import IndexManager

indexer = IndexManager(index_name="my_index")
```

#### `create_index(documents: List[Document]) -> bool`
Create a FAISS vector index from documents.

```python
success = indexer.create_index(chunks)
# Returns: True if successful
```

**Returns**: `bool` - Success status

#### `save_index(output_path: str = "./indexes") -> bool`
Save the index to disk.

```python
success = indexer.save_index(output_path="./my_indexes")
```

**Returns**: `bool` - Success status

#### `load_index(index_path: str) -> bool`
Load a previously saved index from disk.

```python
success = indexer.load_index(index_path="./my_indexes")
```

**Returns**: `bool` - Success status

#### `similarity_search(query: str, k: int = 4) -> List[Document]`
Find k most similar documents to the query.

```python
results = indexer.similarity_search("Tell me about AI", k=3)
# Returns: 3 most relevant documents
```

**Returns**: `List[Document]` - Most similar documents

**Parameters**:
- `query` (str): Search query
- `k` (int): Number of results to return (default: 4)

#### `similarity_search_with_scores(query: str, k: int = 4) -> List[tuple]`
Find similar documents with similarity scores.

```python
results = indexer.similarity_search_with_scores("Tell me about AI", k=3)
# Returns: [(Document, score), ...]
```

**Returns**: `List[tuple]` - List of (Document, similarity_score) tuples

---

## LLMInvoker

**Module**: `src.llm_invoker`

### Purpose
Invoke LLM to generate summaries and answers.

### Methods

#### `__init__(model_name: str = "gpt-3.5-turbo", temperature: float = 0.7)`
Initialize the LLM invoker.

```python
from src.llm_invoker import LLMInvoker

llm = LLMInvoker(model_name="gpt-3.5-turbo", temperature=0.7)
```

**Parameters**:
- `model_name` (str): Model to use (default: "gpt-3.5-turbo")
- `temperature` (float): Sampling temperature 0-1 (default: 0.7)

#### `generate_summary(content: str, max_length: int = 150) -> str`
Generate a summary of provided text.

```python
summary = llm.generate_summary(
    content="Long text to summarize...",
    max_length=150
)
# Returns: Concise summary
```

**Returns**: `str` - Generated summary

**Parameters**:
- `content` (str): Text to summarize
- `max_length` (int): Target summary length in words

#### `generate_summary_from_documents(documents: List[Document], max_length: int = 150) -> str`
Generate summary from multiple documents.

```python
summary = llm.generate_summary_from_documents(chunks, max_length=150)
```

**Returns**: `str` - Generated summary

#### `answer_question(question: str, context: str) -> str`
Answer a question based on provided context.

```python
answer = llm.answer_question(
    question="What is artificial intelligence?",
    context="AI is a field of computer science..."
)
```

**Returns**: `str` - Generated answer

#### `generate_qa_pairs(content: str, num_pairs: int = 3) -> List[dict]`
Generate question-answer pairs from content.

```python
qa_pairs = llm.generate_qa_pairs(content, num_pairs=5)
# Returns: [{"question": "...", "answer": "..."}, ...]
```

**Returns**: `List[dict]` - List of QA pair dictionaries

---

## EvaluationMetrics

**Module**: `src.evaluation`

### Purpose
Static methods for calculating evaluation metrics.

### Methods

#### `calculate_coherence(text: str) -> float`
Calculate coherence score (0-1) based on text structure.

```python
from src.evaluation import EvaluationMetrics

score = EvaluationMetrics.calculate_coherence("Sample text...")
# Returns: 0.0-1.0
```

**Returns**: `float` - Coherence score 0-1

#### `calculate_relevance(summary: str, original: str) -> float`
Calculate relevance score comparing summary to original.

```python
score = EvaluationMetrics.calculate_relevance(
    summary="AI is transformative",
    original="Artificial Intelligence is..."
)
# Returns: 0.0-1.0
```

**Returns**: `float` - Relevance score 0-1

#### `calculate_summary_compression_ratio(summary: str, original: str) -> float`
Calculate compression ratio of summary vs original.

```python
ratio = EvaluationMetrics.calculate_summary_compression_ratio(summary, original)
# Returns: 0.04 (4% of original length)
```

**Returns**: `float` - Compression ratio 0-1

---

## SummaryEvaluator

**Module**: `src.evaluation`

### Purpose
Evaluate summary quality with multiple metrics.

### Methods

#### `__init__()`
Initialize the evaluator.

```python
from src.evaluation import SummaryEvaluator

evaluator = SummaryEvaluator()
```

#### `evaluate_summary(summary: str, original_text: str) -> Dict[str, Any]`
Comprehensive evaluation of a summary.

```python
evaluation = evaluator.evaluate_summary(
    summary="AI is transformative technology",
    original_text="Artificial Intelligence is..."
)
```

**Returns**: `Dict[str, Any]` - Evaluation results with metrics

**Example Output**:
```python
{
    "summary": "AI is transformative...",
    "original_length": 500,
    "summary_length": 20,
    "coherence_score": 0.85,
    "relevance_score": 0.92,
    "compression_ratio": 0.04
}
```

#### `batch_evaluate(summaries: List[str], original_texts: List[str]) -> List[Dict]`
Evaluate multiple summaries.

```python
evaluations = evaluator.batch_evaluate(
    summaries=["Summary 1", "Summary 2"],
    original_texts=["Original 1", "Original 2"]
)
```

**Returns**: `List[Dict]` - List of evaluation results

#### `generate_evaluation_report(evaluation: Dict) -> str`
Generate a formatted evaluation report.

```python
report = evaluator.generate_evaluation_report(evaluation)
print(report)
```

**Returns**: `str` - Formatted report

---

## LLMBasedEvaluator

**Module**: `src.evaluation`

### Purpose
Use LLM for semantic evaluation of summaries.

### Methods

#### `__init__()`
Initialize the LLM-based evaluator.

```python
from src.evaluation import LLMBasedEvaluator

llm_evaluator = LLMBasedEvaluator()
```

#### `evaluate_semantic_quality(summary: str, original_text: str) -> Dict[str, Any]`
Evaluate semantic quality using LLM.

```python
evaluation = llm_evaluator.evaluate_semantic_quality(
    summary="AI summary...",
    original_text="Original text..."
)
```

**Returns**: `Dict[str, Any]` - Semantic evaluation results

**Example Output**:
```python
{
    "raw_evaluation": "Accuracy: 9/10...",
    "accuracy": 0.9,
    "completeness": 0.85,
    "clarity": 0.92,
    "overall_quality": 0.88
}
```

---

## DocumentProcessingPipeline

**Module**: `src.pipeline`

### Purpose
End-to-end document processing orchestration.

### Methods

#### `__init__()`
Initialize the complete pipeline.

```python
from src.pipeline import DocumentProcessingPipeline

pipeline = DocumentProcessingPipeline()
```

#### `process_single_document(pdf_path: str, query: str = "Summarize") -> dict`
Process a single document through all stages.

```python
result = pipeline.process_single_document(
    pdf_path="data/document.pdf",
    query="Summarize"
)
```

**Returns**: `dict` - Complete pipeline results with all stages

**Result Structure**:
```python
{
    "stages": {
        "chunking": {"num_chunks": 15, ...},
        "embedding": {"num_embeddings": 15, ...},
        "indexing": {"index_created": True, ...},
        "llm_invocation": {"summary": "...", ...},
        "evaluation": {"coherence_score": 0.85, ...}
    },
    "evaluation_report": "..."
}
```

#### `process_multiple_documents(pdf_paths: List[str]) -> List[dict]`
Process multiple documents.

```python
results = pipeline.process_multiple_documents([
    "data/doc1.pdf",
    "data/doc2.pdf"
])
```

**Returns**: `List[dict]` - Results for each document

#### `interactive_qa(pdf_path: str)`
Start interactive Q&A mode with a document.

```python
pipeline.interactive_qa("data/document.pdf")
# User can ask questions interactively
```

#### `generate_qa_dataset(pdf_path: str, num_pairs: int = 5) -> List[dict]`
Generate Q&A pairs from a document.

```python
qa_pairs = pipeline.generate_qa_dataset(
    pdf_path="data/document.pdf",
    num_pairs=5
)
```

**Returns**: `List[dict]` - QA pair dictionaries

---

## Configuration

**Module**: `src.config`

### Available Settings

```python
from src.config import (
    LLM_MODEL,           # OpenAI model name
    OPENAI_API_KEY,      # API key from environment
    EMBEDDING_MODEL,     # Embedding model name
    CHUNK_SIZE,          # Size of text chunks
    CHUNK_OVERLAP,       # Overlap between chunks
    VECTOR_STORE_TYPE    # Type of vector store (faiss)
)
```

### Environment Variables

```bash
OPENAI_API_KEY=your_key_here
LLM_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
VECTOR_STORE_TYPE=faiss
```

---

## Common Usage Patterns

### Pattern 1: Basic Summarization
```python
from src.pipeline import DocumentProcessingPipeline

pipeline = DocumentProcessingPipeline()
result = pipeline.process_single_document("document.pdf")
print(result["stages"]["llm_invocation"]["summary"])
```

### Pattern 2: Custom Chunk Configuration
```python
from src.chunking import DocumentChunker

chunker = DocumentChunker(chunk_size=500, chunk_overlap=100)
chunks = chunker.process_pdf("document.pdf")
```

### Pattern 3: Search and Answer
```python
from src.indexing import IndexManager
from src.llm_invoker import LLMInvoker

indexer = IndexManager()
indexer.create_index(chunks)

llm = LLMInvoker()
docs = indexer.similarity_search("your question", k=3)
answer = llm.answer_question("your question", context=str(docs))
```

### Pattern 4: Batch Evaluation
```python
from src.evaluation import SummaryEvaluator

evaluator = SummaryEvaluator()
results = evaluator.batch_evaluate(summaries, originals)
for result in results:
    print(f"Coherence: {result['coherence_score']}")
```

---

## Error Handling

All modules handle errors gracefully:

```python
try:
    result = pipeline.process_single_document("nonexistent.pdf")
except Exception as e:
    print(f"Error: {str(e)}")
```

Common errors and handling:
- Missing API key: Check `.env` file
- PDF not found: Verify file path
- Embedding error: Check OpenAI API quota
- Index error: Ensure documents are chunked first

---

## Performance Tips

1. **Batch Processing**: Process multiple documents together
2. **Cache Embeddings**: Save indices for reuse
3. **Adjust Chunk Size**: Larger = more context, more tokens
4. **Select Model**: Cheaper models for simple tasks
5. **Reduce Search Results**: Lower `k` for faster search

---

## Version Information

- LangChain: 0.1.0+
- Python: 3.8+
- OpenAI API: Latest

---

Last Updated: May 2026
