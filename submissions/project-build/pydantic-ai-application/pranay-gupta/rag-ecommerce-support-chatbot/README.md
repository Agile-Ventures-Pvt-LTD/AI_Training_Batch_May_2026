# Production-Grade Marketplace RAG Support Agent

Modern e-commerce marketplaces require highly available, accurate, and secure automated 
support for their seller ecosystems. The goal of this project is to build an enterprise-grade, 
production-ready Retrieval-Augmented Generation (RAG) chatbot for ShopSphere 
Marketplace, a platform hosting thousands of independent business sellers. 
The chatbot must accurately ingest complex corporate guidelines—specifically focusing on 
advanced business operations, fulfillment strategies, seller ratings, and profitability matrices. It 
must answer seller queries instantly while maintaining absolute deterministic safety standards, 
ensuring no toxic, profane, or hallucinated outputs are surfaced to end-users.

---

## Project Overview

This project demonstrates how the **RAG Support Agent** can be used to connect a Large Language Model with external tools.

The solution consists of two main components:

- **Agent** – Agent call  Retriver tool.
- **Guardrails** – Guardrails check all input queries through Guardrails-AI


---

## Project Structure

```text
rag-ecommerce-support-chatbot/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── data/
│   └── Advanced_Business_Seller_Guide_May09
│
├── src/
│   ├── agent.py
│   ├── config.py
│   ├── database.py
│   └── guardrails_config.py
│
├── tests/
│   ├── test_rag_metrics.py
│
│
└── chroma_db/
```

---

## Tech Stack
- Python
- LangChain
- Groq LLM
- ChromaDB / Vector Store
- deepeval
- pydantic
- guardrails-ai

---

## Prerequisites

Before running the project, make sure you have:

- Python 3.11 or later
- A Groq API Key
- A Guardrails-ai API token
- Hugging Face Token

---

## Installation

Clone the repository.

```bash
git clone <repository-url>
```

Move into the project directory.

```bash
cd rag-ecommerce-support-chatbot
```

Create a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file using the provided `.env.example`.

```env
GUARDRAILS_API= "set configuration in terminal for Guardrails-hub
GROQ_API_KEY=
HF_TOKEN=
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
TOP_K=5
VECTOR_STORE_PATH=chroma_db
```

---

## Running the Pydantic Agent


```bash
python src/agent.py
```

---



## Application Workflow

```
User Query
      │
      ▼
    Agent
      │
      ▼
  Guardrails
      │
      ▼
     LLM
      │
      ▼
    tool call
      │
      ▼
    Tool Response
      │
      ▼
    Groq LLM
      │
      ▼
Final Response
```

---


## Running Tests

Execute all test cases using:

```bash
python test_rag_metrics.py
```

---


## Future Improvements

Possible enhancements include:

- Multi-step tool execution
- Automatic transition lookup by status name
- Conversation memory
- Tool result caching
- Rich terminal interface

---
## Author

**Pranay Gupta**