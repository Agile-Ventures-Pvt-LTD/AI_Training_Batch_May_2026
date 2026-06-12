# Enterprise AI Assistant

An AI-powered assistant built using LangChain, Vector Databases, and Large Language Models (LLMs) to enable intelligent question-answering, document retrieval, and enterprise knowledge management.

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline that allows users to interact with organizational knowledge through natural language.

The system ingests documents, converts them into vector embeddings, stores them in a vector database, retrieves relevant information based on user queries, and generates accurate responses using an LLM.

The application can be extended to support conversational memory, multiple document sources, enterprise search, and AI agents with tool-calling capabilities.

---

## Features

* Document ingestion and processing
* Automatic text chunking
* Semantic search using embeddings
* Vector database storage
* Retrieval-Augmented Generation (RAG)
* Multi-document support
* Conversational chat interface
* Source citation support
* Streamlit-based user interface
* Enterprise-ready architecture
* Extensible agent and tool integration

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python
* LangChain

### Vector Database

* ChromaDB

### Embedding Model

* sentence-transformers/all-MiniLM-L6-v2

### Large Language Model

* Groq Llama Models

### Document Processing

* PyPDFLoader
* RecursiveCharacterTextSplitter

---

## Architecture

User Query
↓
Retriever
↓
Vector Database (Chroma)
↓
Relevant Chunks
↓
Large Language Model
↓
Final Response

### RAG Pipeline

Document Loading
↓
Chunking
↓
Embedding Generation
↓
Vector Storage
↓
Semantic Retrieval
↓
Answer Generation

---

## Project Structure

```text
ai_knowledge_assistant_rag/
│
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
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ ├── raw/
│ ├── processed/
│ └── vector_store/
│
├── logs/
│ └── query_logs.jsonl
│
├── outputs/
│ └── benchmark_results.json
│
└── tests/
 └── test_retrieval.py
```

---



### Create Virtual Environment

```bash
uv venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
HF_TOKEN=hf_token
```

---

### Streamlit Version

```bash
streamlit run app.py
```

---

## Example Queries

* When is Amazon LEO scheduled?
* What is AWS and why it is required?
* Explain reimbursement policy.


---

## Future Enhancements

* Hybrid Search
* Re-ranking
* Multi-modal RAG
* Agentic Workflows
* Tool Calling
* Knowledge Graph Integration
* Authentication and Role-Based Access
* Cloud Deployment

---

## Challenges Faced

* Document chunking optimization
* Retrieval quality improvement
* Prompt engineering
* Managing hallucinations
* Conversational context handling
* Vector database persistence

---

## Key Learnings

* Retrieval-Augmented Generation (RAG)
* Embedding Models
* Vector Databases
* Semantic Search
* LangChain Framework
* Prompt Engineering
* Enterprise AI Architecture
* Conversational AI Systems

---

## Conclusion

This project demonstrates how modern AI systems can combine retrieval mechanisms with Large Language Models to create accurate, scalable, and enterprise-ready knowledge assistants. The architecture can be extended to support advanced use cases such as conversational agents, enterprise search systems, and intelligent workflow automation.
