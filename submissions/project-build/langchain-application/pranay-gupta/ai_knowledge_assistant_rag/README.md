# AI Knowledge Assistant RAG

A Retrieval-Augmented Generation (RAG) application built using LangChain, Groq LLM, ChromaDB, and HuggingFace Embeddings. The system allows users to ask questions about uploaded business documents and generates grounded answers using retrieved document context with source citations.

---

## Project Overview

This project implements an AI-powered Knowledge Assistant capable of:

* Loading and processing PDF documents
* Creating embeddings from document chunks
* Storing embeddings in a Chroma vector database
* Retrieving relevant document sections
* Generating grounded answers using Groq LLM
* Providing source citations for transparency
* Logging user queries for analysis
* Running benchmark evaluations

The application follows a modular architecture to ensure maintainability and scalability.

---

## Tech Stack

| Component              | Technology                        |
| ---------------------- | --------------------------------- |
| Programming Language   | Python                            |
| LLM                    | Groq (Llama 3.3 70B Versatile)    |
| Framework              | LangChain                         |
| Embeddings             | HuggingFace Sentence Transformers |
| Embedding Model        | all-MiniLM-L6-v2                  |
| Vector Database        | ChromaDB                          |
| PDF Processing         | PyPDF                             |
| Environment Management | Python Dotenv                     |
| Testing                | Python Assertions                 |

---

## Project Structure

```text
ai_knowledge_assistant_rag/

├── app.py
├── config.py
├── loaders.py
├── chunking.py
├── embeddings.py
├── vector_store.py
├── retriever.py
├── prompts.py
├── chains.py
├── output_parser.py
├── logger.py
├── benchmark_runner.py
├── requirements.txt
├── .env.example
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── vector_store/
│
├── logs/
│   └── query_logs.jsonl
│
├── outputs/
│   └── benchmark_results.json
│
└── tests/
    └── test_retrieval.py
```

---

## Application Workflow

```text
PDF Documents
      │
      ▼
Document Loader
      │
      ▼
Text Cleaning
      │
      ▼
Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Chroma Vector Store
      │
      ▼
Retriever
      │
      ▼
Query Classification
      │
      ▼
Grounded RAG Prompt
      │
      ▼
Groq LLM
      │
      ▼
Answer + Sources + Confidence
```

---

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

```bash
venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
GROQ_API_KEY=your_api_key

GROQ_MODEL=llama-3.3-70b-versatile

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHUNK_SIZE=1000

CHUNK_OVERLAP=150

TOP_K=5
```

---

### 4. Add Documents

Place PDF files inside:

```text
data/raw/
```

Example:

```text
data/raw/Amazon-2025-Annual-Report.pdf
```

---

## Running the Application

### Start the Knowledge Assistant

```bash
python app.py
```

During the first run:

* Documents are loaded
* Text is chunked
* Embeddings are generated
* Chroma vector database is created

Subsequent runs load the existing vector database.

---

### Example Query

```text
What are Amazon's business segments?
```

Example Output:

```text
Answer:
Amazon operates through North America, International, and AWS segments.

Confidence:
HIGH

Sources:
Amazon-2025-Annual-Report.pdf
Page 32
```

---

## Running Retrieval Test

Validate that the retriever is able to fetch relevant chunks.

```bash
python -m tests.test_retrieval
```

Expected Output:

```text
Retrieval test passed.
```

---

## Running Benchmark Evaluation

Execute benchmark questions and save results.

```bash
python benchmark_runner.py
```

Generated file:

```text
outputs/benchmark_results.json
```

---

## Features Implemented

* PDF document loading
* Metadata preservation
* Text chunking
* Embedding generation
* Chroma vector database
* Similarity-based retrieval
* Query classification
* Grounded answer generation
* Source citations
* Confidence scoring
* Query logging
* Benchmark evaluation
* Modular code structure

---

## Error Handling

The application handles:

* Missing document folder
* Empty document folder
* Missing API key
* PDF loading failures
* Empty retrieval results
* Invalid model responses
* Missing vector database
* Groq API failures

---

## Future Enhancements

* Streamlit UI
* Hybrid Search (Keyword + Vector)
* MMR Retrieval
* Conversation Memory
* Source Preview Panel
* Answer Review Chain
* Metadata Filtering
* Downloadable Reports

---

## Disclaimer

This project is intended for educational and prototype purposes. Generated answers should be reviewed before being used for business-critical decisions.
