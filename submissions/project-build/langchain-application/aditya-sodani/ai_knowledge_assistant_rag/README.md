# AI Knowledge Assistant (RAG)

A modular Retrieval-Augmented Generation (RAG) system built with Python, LangChain, and Groq. This assistant processes local PDF documents, classifies user queries, and provides grounded, verifiable answers based strictly on the provided context.

## File Structure

```text
ai_knowledge_assistant_rag/
├── app.py              # Main CLI orchestrator
├── config.py           # Configuration and environment management
├── loaders.py          # PDF document loading and metadata extraction
├── chunking.py         # Recursive text splitting and chunk ID generation
├── embeddings.py       # Local HuggingFace embedding model setup
├── vector_store.py     # ChromaDB creation and persistence
├── retriever.py        # Similarity search logic
├── prompts.py          # Structured JSON prompt templates
├── chains.py           # LangChain LCEL chains with JSON parsers
├── data/
│   └── raw/            # Place your source PDFs here
├── logs/
│   └── query_logs.jsonl # Append-only query history
└── outputs/
    └── benchmark_results.json # Structured RAG evaluation data
```

##  Quick Start

### 1. Prerequisites
* Python 3.11.15
* A [Groq API Key]

### 2. Setup
Initialize environment and install dependencies:
```bash
uv init
uv pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```text
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Data Preparation
Place your PDF files into the `data/raw/` folder.

### 5. Run the Application
```bash
python app.py
```

## How it Works
1. **Ingestion**: PDFs are loaded, enriched with metadata (source, page, year), and split into chunks with unique IDs.
2. **Classification**: Every query is analyzed to determine its type (e.g., `FACTUAL_LOOKUP`, `SUMMARY`) and whether it actually requires retrieval.
3. **Grounded RAG**: If retrieval is needed, the system fetches relevant chunks and generates a JSON-structured response using Groq's Llama-3 models.
4. **Citations**: Answers include snippets and source references (page numbers, chunk IDs) for verification.

## Example

**User Input:**
> "What are the main business segments described in the filings?"

**Assistant Output:**
```json
{
 "answer": "The company operates in three main segments: North America, International, and AWS.",
 "supporting_evidence": ["We have organized our operations into three segments: North America, International, and AWS."],
 "sources": ["Amazon-2025-Annual-Report.pdf, page 78"],
 "confidence": "HIGH",
 "answerability": "ANSWERED"
}
```
**Terminal View:**
*   **Source:** Amazon-2025-Annual-Report.pdf, page 78, Amazon-2025-Annual-Report.pdf_p78_c388
*   **Snippet:** "We have organized our operations into three segments: North America, International, and AWS..."

## Logging & Benchmarking
*   Detailed query history is kept in `logs/query_logs.jsonl`.
*   Structured output for benchmarking is saved in `outputs/benchmark_results.json`.