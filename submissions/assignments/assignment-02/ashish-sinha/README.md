# Tesla Annual Reports RAG System

A Retrieval-Augmented Generation (RAG) system that answers questions from Tesla Annual Reports (10-K filings) using LangChain, ChromaDB, Sentence Transformers, and Groq LLMs.

---

## 📌 Overview

This project enables semantic search and question answering over Tesla annual reports from **2019–2023**.

The system:

* Loads Tesla annual report PDFs
* Splits documents into chunks
* Generates embeddings using Sentence Transformers
* Stores embeddings in ChromaDB
* Retrieves relevant context using vector search
* Expands user queries for improved retrieval
* Generates grounded answers using GPT-OSS via Groq

---

## 🏗️ Architecture

```text
Tesla Annual Reports (PDFs)
            │
            ▼
   PDF Document Loader
            │
            ▼
     Text Chunking
            │
            ▼
 Embedding Generation
            │
            ▼
      ChromaDB
            │
            ▼
      Retriever
            │
            ▼
   Query Expansion
            │
            ▼
 Context Retrieval
            │
            ▼
   GPT-OSS (Groq)
            │
            ▼
      Final Answer
```

---

## 🛠️ Tech Stack

| Component       | Technology                     |
| --------------- | ------------------------------ |
| LLM             | GPT-OSS-120B (Groq)            |
| Framework       | LangChain                      |
| Vector Database | ChromaDB                       |
| Embeddings      | all-mpnet-base-v2              |
| Document Loader | PyPDFDirectoryLoader           |
| Text Splitter   | RecursiveCharacterTextSplitter |
| Language        | Python                         |

---

## 📂 Project Structure

```text
Tesla-RAG/
│
├── tesla-annual-reports/
│   ├── Tesla_2019.pdf
│   ├── Tesla_2020.pdf
│   ├── Tesla_2021.pdf
│   ├── Tesla_2022.pdf
│   └── Tesla_2023.pdf
│
├── tesla_db/
│   └── ChromaDB Files
│
├── Tesla_RAG.ipynb
├── README.md
└── .env
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd Tesla-RAG
```

### Create Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install langchain
pip install langchain-community
pip install langchain-chroma
pip install chromadb
pip install sentence-transformers
pip install groq
pip install python-dotenv
pip install tiktoken
pip install pandas
pip install matplotlib
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY2=your_groq_api_key
```

---

## 🧠 Embedding Model

```python
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
```

Why this model?

* Strong semantic understanding
* Excellent retrieval performance
* Popular choice for RAG systems

---

## 🗄️ Vector Database

```python
CHROMA_DB_PATH = "./tesla_db"

COLLECTION_NAME = "tesla-10k-2019-to-2023"
```

Features:

* Persistent storage
* Fast similarity search
* Efficient retrieval

---

## ✂️ Document Chunking

```python
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
```

The reports are split into overlapping chunks to preserve context and improve retrieval quality.

---

## 🔍 Query Expansion

To improve retrieval accuracy, the system generates multiple variations of the user's question.

### Example

**Input**

```text
What was the automotive revenue in 2021?
```

**Expanded Queries**

```text
What was Tesla's automotive revenue in 2021?
How much revenue did Tesla generate from automotive sales in 2021?
What automotive segment revenue was reported during fiscal year 2021?
```

This increases retrieval coverage and improves answer quality.

---

## 🤖 Retrieval-Augmented Generation (RAG)

Workflow:

1. User asks a question
2. Query expansion generates alternative phrasings
3. Retriever fetches relevant chunks
4. Duplicate chunks are removed
5. Context is assembled
6. GPT-OSS generates a grounded answer
7. Final answer is returned

---

## 🚀 Usage

### Run a Query

```python
question = "What was the automotive revenue in 2021?"

answer = advanced_rag_query(question)

print(answer)
```

### Example Output

```text
Tesla's automotive revenue in 2021 was $47.2 billion.
```

---

## 📊 Features

* ✅ Semantic Search
* ✅ ChromaDB Persistence
* ✅ Query Expansion
* ✅ Financial Report Analysis
* ✅ Context-Aware Responses
* ✅ Reduced Hallucinations
* ✅ Modular RAG Pipeline

---

## 🛠️ Core Functions

```python
generate_response()

build_query_expansion_prompt()

expand_query()

build_qa_prompt()

answer_question()

advanced_rag_query()
```

---

## 📈 Future Improvements

* Hybrid Search (BM25 + Vector Search)
* Reranking Models
* Source Citations
* Streamlit Web Interface
* Multi-Company Analysis
* Evaluation Dashboard
* Retrieval Metrics

---

## 🎯 Results

The system successfully retrieves relevant information from Tesla annual reports and generates accurate, context-grounded financial answers using Retrieval-Augmented Generation.

---

## 👨‍💻 Author

Financial RAG System built using LangChain, ChromaDB, Sentence Transformers, and Groq LLMs.
