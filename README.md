# GenAI Solution using LangChain Framework

## Project Overview

This project implements a comprehensive GenAI solution using the **LangChain framework** for document processing and summarization. The solution demonstrates all key components of a production-ready document AI pipeline:

1. **Chunking**: Split documents into manageable pieces
2. **Embedding**: Generate vector representations of text
3. **Indexing**: Store and retrieve documents efficiently
4. **LLM Invocation**: Generate summaries and answer questions
5. **Evaluation**: Assess quality of generated content

## Project Structure

```
langchain_solution/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── chunking.py            # Document chunking module
│   ├── embeddings.py          # Embedding generation
│   ├── indexing.py            # Vector store indexing
│   ├── llm_invoker.py         # LLM interactions
│   ├── evaluation.py          # Quality evaluation metrics
│   └── pipeline.py            # Main orchestrator
├── tests/
│   ├── __init__.py
│   ├── test_pipeline.py       # Unit tests
│   └── test_integration.py    # Integration tests
├── data/
│   ├── ai_guide.pdf           # Sample PDF 1
│   └── cloud_computing.pdf    # Sample PDF 2
├── create_pdfs.py             # PDF generation utility
├── examples.py                # Usage examples
├── requirements.txt           # Dependencies
├── .env.example              # Environment configuration
└── README.md                 # This file
```

## Features

### 1. **Document Chunking** (`src/chunking.py`)
- Load PDFs using LangChain's PyPDFLoader
- Split documents into overlapping chunks for context preservation
- Recursive text splitting with configurable chunk size and overlap

### 2. **Embeddings** (`src/embeddings.py`)
- Generate vector embeddings using OpenAI's embedding models
- Support for batch embedding of documents
- Query embedding for similarity search

### 3. **Vector Indexing** (`src/indexing.py`)
- Build FAISS vector indices for efficient search
- Similarity search with configurable number of results
- Save/load indices for reuse
- Support for scored similarity search

### 4. **LLM Invocation** (`src/llm_invoker.py`)
- Generate concise summaries from document chunks
- Answer questions based on document context
- Generate Q&A pairs for evaluation datasets
- Configurable LLM models and parameters

### 5. **Evaluation** (`src/evaluation.py`)
- Calculate coherence scores for summaries
- Measure relevance against original text
- Compute compression ratios
- Generate detailed evaluation reports
- LLM-based semantic quality evaluation

### 6. **Pipeline Orchestration** (`src/pipeline.py`)
- End-to-end document processing workflow
- Batch processing of multiple documents
- Interactive Q&A mode
- Comprehensive result reporting

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   cd /workspaces/langchain_solution
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   nano .env  # or use your preferred editor
   ```

## Usage

### 1. Generate Sample PDFs

```bash
python create_pdfs.py
```

This creates two sample PDFs in the `data/` folder:
- `ai_guide.pdf` - Document about Artificial Intelligence
- `cloud_computing.pdf` - Document about Cloud Computing

### 2. Run the Main Pipeline

```bash
python -m src.pipeline
```

This will:
- Load PDF documents
- Chunk them into manageable pieces
- Generate embeddings
- Create vector indices
- Summarize content using LLM
- Evaluate the summaries

### 3. Run Examples

```bash
python examples.py
```

### 4. Run Tests

**Unit Tests:**
```bash
python -m unittest tests.test_pipeline -v
```

**Integration Tests:**
```bash
python -m unittest tests.test_integration -v
```

**All Tests:**
```bash
python -m pytest tests/ -v
```

## Pipeline Components

### Chunking Pipeline
```
PDF File → Load Documents → Split into Chunks → Output: Document Chunks
```

### Embedding Pipeline
```
Document Chunks → Generate Embeddings → Output: Vector Representations
```

### Indexing Pipeline
```
Vector Representations → Build FAISS Index → Output: Searchable Index
```

### LLM Pipeline
```
Query + Index → Similarity Search → Retrieve Context → Generate Summary
```

### Evaluation Pipeline
```
Summary + Original → Calculate Metrics → Generate Report
```

## Configuration

Edit `src/config.py` to adjust:

- **Chunking**: `CHUNK_SIZE`, `CHUNK_OVERLAP`
- **Embedding**: `EMBEDDING_MODEL`
- **LLM**: `LLM_MODEL`
- **Vector Store**: `VECTOR_STORE_TYPE`

Or set environment variables in `.env`:
```
OPENAI_API_KEY=your_key_here
LLM_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Evaluation Metrics

The solution provides comprehensive evaluation:

1. **Coherence Score** (0-1)
   - Measures logical flow and structure
   - Based on transition words and sentence structure

2. **Relevance Score** (0-1)
   - Measures how well summary captures original content
   - Based on keyword overlap

3. **Compression Ratio** (0-1)
   - Ratio of summary length to original length
   - Lower values indicate more compression

4. **LLM-Based Evaluation**
   - Accuracy assessment
   - Completeness evaluation
   - Clarity scoring
   - Overall quality rating

## Example Output

```
STAGE 1: CHUNKING
- Loaded PDF with 5 pages
- Created 12 chunks

STAGE 2: EMBEDDING
- Generated embeddings for 12 documents
- Embedding dimension: 1536

STAGE 3: INDEXING
- Created FAISS index
- Index size: 12 documents

STAGE 4: LLM INVOCATION
- Retrieved 3 relevant documents
- Summary: "Artificial Intelligence represents..."

STAGE 5: EVALUATION
- Coherence Score: 0.85/1.0
- Relevance Score: 0.78/1.0
- Compression Ratio: 0.12 (88% reduction)
```

## Key LangChain Components Used

1. **Document Loaders**: `PyPDFLoader`
2. **Text Splitters**: `RecursiveCharacterTextSplitter`
3. **Embeddings**: `OpenAIEmbeddings`
4. **Vector Stores**: `FAISS`
5. **LLMs**: `ChatOpenAI`
6. **Prompts**: `PromptTemplate`
7. **Schemas**: `Document`, `HumanMessage`

## Advanced Features

### Interactive Q&A Mode
```python
from src.pipeline import DocumentProcessingPipeline

pipeline = DocumentProcessingPipeline()
pipeline.interactive_qa("data/ai_guide.pdf")
```

### Generate QA Datasets
```python
qa_pairs = pipeline.generate_qa_dataset("data/ai_guide.pdf", num_pairs=5)
```

### Batch Processing
```python
results = pipeline.process_multiple_documents([
    "data/ai_guide.pdf",
    "data/cloud_computing.pdf"
])
```

## Error Handling

The solution includes comprehensive error handling:
- API connection failures
- Missing files
- Invalid PDFs
- LLM timeouts
- Embedding generation errors

All errors are logged with informative messages.

## Performance Considerations

- **Chunking**: Larger chunks provide more context but require more tokens
- **Embeddings**: Batch processing is more efficient than single embeddings
- **Index Size**: FAISS is efficient for indices up to millions of vectors
- **LLM Calls**: Use caching and batch requests where possible

## Troubleshooting

### "OpenAI API key not found"
- Ensure `.env` file has `OPENAI_API_KEY=your_key`
- Verify the API key is valid

### "PDF not found"
- Run `python create_pdfs.py` first
- Check the `data/` folder exists

### "FAISS index creation failed"
- Verify embeddings were generated successfully
- Check vector dimension consistency

## Dependencies

- `langchain` - Core framework
- `langchain-community` - Community integrations
- `langchain-openai` - OpenAI integration
- `pypdf` - PDF processing
- `faiss-cpu` - Vector indexing
- `openai` - OpenAI API client
- `python-dotenv` - Environment configuration
- `reportlab` - PDF generation

## Future Enhancements

- [ ] Support for multiple document formats (DOCX, TXT, etc.)
- [ ] Advanced chunking strategies (semantic chunking)
- [ ] Multiple vector store backends (Pinecone, Weaviate, etc.)
- [ ] Streaming responses for large documents
- [ ] Document comparison and clustering
- [ ] Web UI for document upload and querying
- [ ] Fine-tuned embedding models
- [ ] Multi-language support

## License

MIT License

## Author

GenAI Solutions Team

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review test cases for usage examples
3. Consult LangChain documentation: https://python.langchain.com/