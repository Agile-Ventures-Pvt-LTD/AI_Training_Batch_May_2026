# RAG Query Expansion Assignment

## 1. Name

**Aditya Sodani**

---

## 2. Assignment Title

**Retrieval-Augmented Generation (RAG) with Query Expansion**

---

## 3. Short Description

This project implements a Retrieval-Augmented Generation (RAG) pipeline for question answering over Tesla annual report documents.

The system:

* Loads and processes PDF documents.
* Splits documents into smaller chunks.
* Creates embeddings using Sentence Transformers.
* Stores embeddings in ChromaDB vector database.
* Retrieves relevant document chunks based on user queries.
* Uses Query Expansion to improve retrieval quality.
* Generates context-aware answers using a Large Language Model (LLM) through the Groq API.

The objective is to improve the relevance of retrieved information and generate accurate answers grounded in the provided documents.

---

## 4. Steps to Run the Code

### Step 1: Clone or Download the Project

Ensure the following files are available:

* `RAG_query_expansion.ipynb`
* `requirements.txt`
* Tesla Annual Report PDF files

### Step 2: Create a Virtual Environment

```bash
uv venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

### Step 3: Install Required Packages

```bash
uv pip install -r requirements.txt
```

### Step 4: Configure API Key

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

### Step 5: Launch Jupyter Notebook

```bash
jupyter notebook
```

Open:

```text
RAG_query_expansion.ipynb
```

### Step 6: Run the Notebook

Execute all notebook cells sequentially:

1. Environment Setup
2. PDF Loading
3. Text Chunking
4. Embedding Generation
5. ChromaDB Vector Store Creation
6. Retriever Setup
7. Query Expansion
8. Response Generation

---

## 5. Libraries / Packages Required

The following libraries are required:

```text
groq
python-dotenv
langchain
langchain-community
langchain-chroma
chromadb
sentence-transformers
datasets
tiktoken
pypdf
ipykernel
openai
```

---

## 6. Assumptions Made

* Tesla annual report PDFs are available locally.
* A valid Groq API key is available.
* Internet connectivity is available for model access.
* PDF files contain readable text.
* ChromaDB is used as the vector database for storing embeddings.
* Query Expansion improves retrieval quality by generating related search queries.

---

## 7. Output Explanation

### Example User Query

```text
What were Tesla's main revenue sources in 2023?
```

### System Workflow

1. User submits a question.
2. Query Expansion generates related search queries.
3. Relevant document chunks are retrieved from ChromaDB.
4. Retrieved context is provided to the LLM.
5. The LLM generates a grounded answer based on the retrieved information.

### Example Output

```text
Tesla's primary revenue sources in 2023 included automotive sales,
regulatory credits, energy generation and storage products,
and services related to vehicle maintenance and support.
```

---

## Project Outcome

This assignment demonstrates:

* Retrieval-Augmented Generation (RAG)
* Document Processing and Chunking
* Semantic Search
* Query Expansion
* Vector Databases (ChromaDB)
* Embedding Models
* Context-Aware Question Answering
* LangChain-Based RAG Pipelines
* LLM Integration using Groq API

##
