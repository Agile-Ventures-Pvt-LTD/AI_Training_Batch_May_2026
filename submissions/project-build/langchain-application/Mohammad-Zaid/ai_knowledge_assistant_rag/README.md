# AI Knowledge Assistant - RAG System 

RAG system for AI Knowledge Assistant  Loads PDFs, chunks them, and queries using Groq LLM.


### 1. Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Groq API key
```

### 2. Index Documents
```bash
python app.py index "./data/raw/Amazon-2025-Annual-Report.pdf"
```

### 3. Ask Questions
```bash
python app.py query "What are the key financial highlights?"
```

Queries are automatically logged to `logs/query_logs.jsonl`

## Folder Structure
```
ai_knowledge_assistant_rag/
├── app.py                      # Main application
├── config.py                   # Environment config
├── loaders.py                  # PDF loading
├── chunking.py                 # Document chunking
├── embeddings.py               # Embeddings model
├── vector_store.py             # Chroma setup
├── retriever.py                # Document retrieval
├── prompts.py                  # Prompt template
├── output_parser.py            # Response parsing
├── logger.py                   # Query logging
├── requirements.txt            # Dependencies
├── .env.example                # Env template
├── README.md                   # This file
├── data/raw/                   # Input PDFs
├── data/vector_store/          # Chroma database
├── logs/query_logs.jsonl       # Query history
└── tests/test_retrieval.py     # Tests
```

## Configuration

Edit `.env`:
```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
TOP_K=5
```

## How It Works

1. **Load**: Read PDF from `data/raw/`
2. **Process**: Clean text and extract metadata
3. **Chunk**: Split into 1000-char chunks with 150-char overlap
4. **Embed**: Generate embeddings using HuggingFace model
5. **Index**: Store in Chroma vector database
6. **Query**: Retrieve top-5 chunks similar to question
7. **Answer**: Send context + question to Groq LLM
8. **Log**: Save query and answer to JSONL

## Query Logs

Results saved to `logs/query_logs.jsonl`:
```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "question": "What are the financial highlights?",
  "answer": "...",
  "sources": ["Amazon-2025-Annual-Report.pdf (Page 12)"],
  "confidence": "MEDIUM",
  "answerability": "ANSWERED"
}
```

## Files Overview

- `app.py` - Simple CLI: `index` command and `query` command
- `config.py` - Load and validate environment variables
- `loaders.py` - `load_pdf()` function
- `chunking.py` - Text cleaning and document chunking
- `embeddings.py` - Initialize HuggingFace embeddings
- `vector_store.py` - Create Chroma vector database
- `retriever.py` - Retrieve similar documents
- `prompts.py` - RAG prompt template
- `output_parser.py` - Parse LLM response
- `logger.py` - Save query logs to JSONL

## Troubleshooting

**"GROQ_API_KEY Error"**
- Add `GROQ_API_KEY` to `.env`

**No documents retrieved**
- Run `python app.py index "./data/raw/yourfile.pdf"`
- Check `data/vector_store/` was created

**Slow queries**
- Reduce `TOP_K` in `.env`
- Increase `CHUNK_SIZE`

---


