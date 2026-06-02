# RAG Pipeline with Persistent ChromaDB and Query Expansion

## Author

**Vikash Kumar**

---

## Overview

This project demonstrates the complete implementation of a **Retrieval-Augmented Generation (RAG)** pipeline using:

* Persistent ChromaDB Vector Database
* CRUD Operations on Vector Database
* Hugging Face Embedding Models
* OpenAI GPT-OSS-120B LLM
* Document Retrieval and Semantic Search
* Prompt Engineering
* System & User Message Design
* Query Expansion for Improved Retrieval
* End-to-End Question Answering (Q&A)

The notebook walks through the entire lifecycle of a RAG application, from document ingestion and vector storage to intelligent retrieval and answer generation.

---

## Features

### Vector Database Operations

* Create ChromaDB persistent storage
* Insert documents into vector database
* Read stored embeddings and metadata
* Update existing records
* Delete vectors/documents
* Load existing vector database

### Embedding Generation

* Hugging Face Embedding Models
* Semantic vector representations
* Efficient similarity search

### Retrieval-Augmented Generation (RAG)

* Context retrieval from vector database
* Relevant chunk extraction
* LLM-powered answer generation
* Grounded responses using retrieved context

### Prompt Engineering

* Structured system messages
* Dynamic user prompts
* Context injection
* Hallucination reduction techniques

### Query Expansion

* Automatic query enhancement
* Multiple search variations
* Improved retrieval accuracy
* Better context coverage

---

## Project Workflow

```text
Documents
    │
    ▼
Text Chunking
    │
    ▼
Hugging Face Embeddings
    │
    ▼
Persistent ChromaDB
    │
    ▼
Similarity Search
    │
    ▼
Relevant Chunks Retrieval
    │
    ▼
Query Expansion
    │
    ▼
Prompt Construction
    │
    ▼
GPT-OSS-120B
    │
    ▼
Final Answer
```

---

## Technologies Used

| Technology       | Purpose                 |
| ---------------- | ----------------------- |
| Python           | Programming Language    |
| ChromaDB         | Vector Database         |
| Hugging Face     | Embedding Models        |
| GPT-OSS-120B     | Large Language Model    |
| LangChain        | RAG Framework           |
| Jupyter Notebook | Development Environment |

---

## Project Structure

```text
project/
│
├── RAG_Project.ipynb
├── chroma_db/
│   ├── chroma.sqlite3
│   └── ...
│
├── data/
│   └── documents/
│
├── README.md
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Required Libraries

```python
groq>=1.2.0
ipykernel>=7.2.0
python-dotenv>=1.2.2
datasets>=3.3.2
tiktoken==0.9.0
pypdf==5.4.0
langchain==0.3.20
langchain-community==0.3.19
langchain-chroma==0.2.2
sentence-transformers==5.1.2
chromadb>=0.6.3
langchain-cohere==0.4.5
```

Install using:

```bash
pip install chromadb langchain langchain-community langchain-huggingface sentence-transformers groq
```

---

## Embedding Model

Example Hugging Face Embedding Model:

```python
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

---

## LLM Configuration

```python
model_name = "openai/gpt-oss-120b"
```

Used for:

* Question Answering
* Query Expansion
* Context-Aware Responses
* Prompt Optimization

---

## CRUD Operations

### Create

Store document chunks in ChromaDB.

```python
vector_store.add_documents(documents)
```

### Read

Retrieve similar documents.

```python
vector_store.similarity_search(query)
```

### Update

Modify existing records.

```python
collection.update(...)
```

### Delete

Remove vectors/documents.

```python
collection.delete(...)
```

---

## Persistent ChromaDB

Create persistent storage:

```python
from langchain_chroma import Chroma

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)
```

Load existing database:

```python
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)
```

---

## RAG Pipeline

### Step 1: User Query

```python
query = "What is Retrieval Augmented Generation?"
```

### Step 2: Retrieve Relevant Chunks

```python
docs = retriever.invoke(query)
```

### Step 3: Build Prompt

Combine:

* System Message
* User Query
* Retrieved Context

### Step 4: Generate Response

```python
response = llm.invoke(messages)
```

---

## Prompt Design

### System Message

```text
You are an AI assistant that answers questions strictly based on the provided context.
If the answer is not available in the context, say that the information is unavailable.
```

### User Message

```text
Question:
{question}

Context:
{retrieved_chunks}
```

---

## Retrieving Relevant Chunks

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

retrieved_docs = retriever.invoke(query)
```

Benefits:

* Faster retrieval
* Better context relevance
* Reduced hallucinations

---

## Query Expansion

Query expansion improves retrieval by generating alternative search queries.

### Example

Original Query:

```text
What is RAG?
```

Expanded Queries:

```text
What is Retrieval Augmented Generation?

Explain RAG architecture.

How does RAG work in LLM applications?

Benefits of Retrieval Augmented Generation.
```

### Advantages

* Better semantic coverage
* Improved recall
* More relevant document retrieval
* Enhanced answer quality

---

## Sample RAG Flow

```python
user_query
      │
      ▼
query_expansion()
      │
      ▼
retrieve_chunks()
      │
      ▼
construct_prompt()
      │
      ▼
gpt_oss_120b()
      │
      ▼
final_answer
```

---

## Learning Outcomes

By completing this project, you will understand:

* Vector Databases
* Embedding Models
* ChromaDB Persistence
* CRUD Operations
* Semantic Search
* Retrieval-Augmented Generation
* Prompt Engineering
* Query Expansion Techniques
* Context-Aware LLM Applications

---

## Future Improvements

* Hybrid Search (BM25 + Vector Search)
* Re-ranking Models
* Multi-Query Retrieval
* Metadata Filtering
* Parent-Child Retrieval
* Conversational Memory
* Agentic RAG
* Evaluation Frameworks

---

## Conclusion

This project provides a complete hands-on implementation of a modern RAG pipeline using Persistent ChromaDB, Hugging Face Embeddings, GPT-OSS-120B, and Query Expansion techniques. It demonstrates how retrieval and generation can be combined to build accurate, context-aware AI applications.

---

## License

Copyright © 2026 Vikash Kumar

All Rights Reserved.
