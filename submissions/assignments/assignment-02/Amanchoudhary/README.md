# Query Expansion for RAG using Tesla Annual Reports

## Overview

This project demonstrates how Query Expansion techniques can improve Retrieval-Augmented Generation (RAG) performance when answering questions from Tesla Annual Reports.

The system uses:

* Groq LLM (Llama 3.1 8B Instant)
* ChromaDB Vector Store
* HuggingFace Embeddings
* Tesla Annual Reports Dataset
* Query Expansion Techniques
* Hypothetical Question Generation

The goal is to improve retrieval quality by generating alternative search queries before performing vector search.

---

## Project Structure

```text
Amanchoudary/
│
├── Query Expansion.ipynb
├── main.py
├── requirements.txt
├── README.md
│
├── tesla-annual-reports.zip
├── tesla-annual-reports/
├── tesla_db/
│
├── .env
└── .venv/
```

---

## Features

### Document Loading

* Loads Tesla Annual Report PDFs.
* Extracts text from multiple documents.

### Text Chunking

Documents are split into smaller chunks using:

* RecursiveCharacterTextSplitter
* Chunk Size: 512
* Chunk Overlap: 16

### Embedding Generation

Embeddings are created using:

```python
sentence-transformers/all-mpnet-base-v2
```

### Vector Database

Uses ChromaDB for:

* Storing document embeddings
* Similarity search
* Efficient retrieval

### Query Expansion

The system generates multiple variations of a user query before retrieval.

Benefits:

* Better semantic coverage
* Improved recall
* More relevant document retrieval

### Hypothetical Questions

Generates possible questions related to document content.

Benefits:

* Improves retrieval quality
* Retrieves hidden relevant information
* Enhances answer generation

### Response Generation

Retrieved context is passed to the Groq LLM:

```text
llama-3.1-8b-instant
```

for final answer generation.

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd Amanchoudary
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Git Bash:

```bash
source .venv/Scripts/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run the Notebook

Open:

```text
Query Expansion.ipynb
```

Run all cells sequentially.

---

## Workflow

1. Load Tesla Annual Report PDFs
2. Split documents into chunks
3. Generate embeddings
4. Store embeddings in ChromaDB
5. Receive user query
6. Generate expanded queries
7. Retrieve relevant chunks
8. Generate final answer using Groq LLM

---

## Technologies Used

* Python
* LangChain
* ChromaDB
* Groq
* HuggingFace Embeddings
* Jupyter Notebook
* RAG Architecture

---

## Dataset

Tesla Annual Reports (10-K filings)

Used for:

* Information Retrieval
* Semantic Search
* Query Expansion Experiments
* RAG Evaluation

---

## Future Improvements

* Hybrid Search (BM25 + Vector Search)
* Reranking Models
* Multi-Query Retrieval
* HyDE Retrieval
* Evaluation Metrics
* Streamlit Interface
* FastAPI Deployment

---

## Author

Aman Choudhary
AI Training Batch May 2026
