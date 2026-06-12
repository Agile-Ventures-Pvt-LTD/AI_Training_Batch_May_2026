# AI Knowledge Assistant using Advanced RAG

## Overview

AI Knowledge Assistant is a Retrieval-Augmented Generation (RAG) application that enables users to ask questions about enterprise documents and receive source-grounded answers.

The system uses Groq LLM, ChromaDB, LangChain, and HuggingFace Embeddings to retrieve relevant document chunks and generate accurate responses.

---

## Features

* Document Ingestion (PDF, TXT, MD)
* Intelligent Text Chunking
* Vector Embeddings using BGE Embeddings
* ChromaDB Vector Store
* Semantic Retrieval
* Source Attribution
* Query Classification
* Grounded Answer Generation
* Benchmark Evaluation
* Streamlit User Interface
* Query Logging

---

## Tech Stack

* LangChain v1.x
* Groq (Llama 3.3 70B)
* ChromaDB
* HuggingFace Embeddings
* Streamlit
* Python

---

## Project Structure

```text
ai_knowledge_assistant_rag/
│
├── app.py
├── ui.py
├── config.py
├── loaders.py
├── chunking.py
├── embeddings.py
├── vector_store.py
├── retriever.py
├── chains.py
├── prompts.py
├── logger.py
│
├── data/
│   ├── raw/
│   └── vector_store/
│
├── outputs/
│   └── benchmark_results.jsonl
│
└── test/
    ├── test_retrieval.py
    └── test_evaluator.py
```

---

## Installation

```bash
git clone <repository-url>

cd ai_knowledge_assistant_rag

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Build Vector Index

Place documents inside:

```text
data/raw/
```

Run:

```bash
python app.py
```

Select:

```text
1. Build Index
```

---

## Run Application

### CLI Mode

```bash
python app.py
```

Select:

```text
2. Ask Questions
```

---

## Evaluation

### Retrieval Test

```bash
python -m test.test_retrieval
```

### Benchmark Evaluation

```bash
python -m test.test_evaluator
```

Benchmark results are stored in:

```text
outputs/benchmark_results.json
```

---

## Benchmark Questions

1. Tesla business segments
2. Manufacturing and supply chain risks
3. Key risk factors summary
4. Automotive revenue and energy business
5. Automotive vs Energy comparison
6. Legal and regulatory risks
7. Tesla stock price prediction
8. Future AI profitability guarantees


