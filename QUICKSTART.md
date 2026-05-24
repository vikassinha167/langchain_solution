# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure OpenAI API
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
export OPENAI_API_KEY="your_api_key_here"
```

### Step 3: Generate Sample PDFs
```bash
python create_pdfs.py
```

Expected output:
```
PDF created: data/ai_guide.pdf
PDF created: data/cloud_computing.pdf
Sample PDFs created successfully!
```

### Step 4: Run the Pipeline
```bash
python -m src.pipeline
```

This will process the PDFs through all 5 stages:
1. **Chunking** - Split PDFs into text chunks
2. **Embedding** - Generate vector embeddings
3. **Indexing** - Create searchable index
4. **LLM Invocation** - Generate summaries
5. **Evaluation** - Score the summaries

---

## Common Tasks

### Generate Multiple Summaries
```python
from src.pipeline import DocumentProcessingPipeline

pipeline = DocumentProcessingPipeline()
results = pipeline.process_multiple_documents([
    "data/ai_guide.pdf",
    "data/cloud_computing.pdf"
])
```

### Answer Questions from Documents
```python
pipeline.interactive_qa("data/ai_guide.pdf")

# Then ask questions like:
# "What is artificial intelligence?"
# "What are the applications of AI?"
# "exit"  (to quit)
```

### Generate Training Data
```python
qa_pairs = pipeline.generate_qa_dataset("data/ai_guide.pdf", num_pairs=5)
for pair in qa_pairs:
    print(f"Q: {pair['question']}")
    print(f"A: {pair['answer']}\n")
```

### Run Tests
```bash
# Unit tests
python -m unittest tests.test_pipeline -v

# Integration tests
python -m unittest tests.test_integration -v

# All tests
python -m pytest tests/ -v
```

---

## Output Examples

### Chunking Stage Output
```
Loaded PDF: data/ai_guide.pdf with 2 pages
Created 15 chunks from 2 documents
Average chunk size: 856 characters
```

### Embedding Stage Output
```
Initialized OpenAI Embeddings with model: text-embedding-3-small
Generated embeddings for 15 documents
Embedding dimension: 1536
```

### Summary Output
```
AI (Artificial Intelligence) is transforming multiple sectors including 
healthcare, finance, and transportation. Machine learning and deep learning 
are key technologies enabling computers to learn from data and make intelligent 
decisions autonomously.
```

### Evaluation Output
```
SUMMARY EVALUATION REPORT
============================================================

Original Text Length: 1234 words
Summary Length: 45 words
Compression Ratio: 0.04 (96% reduction)

QUALITY METRICS:
- Coherence Score: 0.85/1.0
- Relevance Score: 0.92/1.0
```

---

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution:** 
```bash
export OPENAI_API_KEY="sk-..."
# or edit .env file
```

### Issue: "ModuleNotFoundError: No module named 'langchain'"
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "PDF not found in data/"
**Solution:**
```bash
python create_pdfs.py
```

### Issue: "FAISS Index Error"
**Solution:**
- Delete the `indexes/` folder
- Restart the pipeline
- Check embeddings are being generated

---

## Pipeline Customization

### Adjust Chunk Size
Edit `src/config.py`:
```python
CHUNK_SIZE = 500  # Smaller chunks
CHUNK_OVERLAP = 100
```

### Use Different LLM Model
```python
from src.llm_invoker import LLMInvoker

invoker = LLMInvoker(model_name="gpt-4")
```

### Adjust Summary Length
```python
summary = llm_invoker.generate_summary(text, max_length=200)  # More words
```

---

## Next Steps

1. ✅ Run the basic pipeline
2. ✅ Generate your own PDFs
3. ✅ Customize chunk sizes and models
4. ✅ Generate QA datasets
5. ✅ Evaluate summaries
6. ✅ Integrate into your application

---

## Documentation

- [Full README](README.md) - Complete documentation
- [Source Code](src/) - Detailed implementation
- [Tests](tests/) - Usage examples and tests
- [LangChain Docs](https://python.langchain.com/) - Framework documentation

---

## Support

For issues:
1. Check `.env` file configuration
2. Verify OpenAI API key is valid
3. Run `python create_pdfs.py` to regenerate samples
4. Check test files for more examples

Happy coding! 🚀
