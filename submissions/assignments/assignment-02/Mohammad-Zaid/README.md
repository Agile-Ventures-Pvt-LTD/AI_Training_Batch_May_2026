## Assignment 02 - Retrieval Improvement Using Query Expansion

## Participant Name

Mohammad Zaid

## Project Title

Retrieval Improvement in RAG Using Query Expansion

## Description

This project demonstrates how Query Expansion can improve retrieval performance in a Retrieval-Augmented Generation (RAG) pipeline.

The workflow uses an LLM to generate multiple semantic variations of a user's query. Each expanded query is used to retrieve relevant document chunks from a ChromaDB vector database containing Tesla 10-K annual reports. The retrieved contexts are aggregated, deduplicated, and provided to an LLM for answer generation.

This approach helps increase retrieval recall by capturing different phrasings and terminology that may exist within the source documents.

## How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a virtual environment (Optional)

```bash
uv venv
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install required dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Ensure Vector Database Exists

The notebook expects a persisted ChromaDB database at:

```text
./tesla_db
```

containing embeddings for Tesla 10-K reports (2019–2023).

### 6. Run the Notebook

Open and execute:

```bash
jupyter notebook
```

Run all cells in:

```text
query_expansion_rag.ipynb
```

## Libraries and Packages Required

```text
chromadb
langchain
langchain-chroma
langchain-community
sentence-transformers
groq
python-dotenv
jupyter
```

Install manually if required:

```bash
pip install chromadb langchain langchain-chroma langchain-community sentence-transformers groq python-dotenv jupyter
```

## Assumptions Made

* A valid Groq API key is available.
* The Tesla 10-K reports have already been processed and stored in ChromaDB.
* The vector database uses cosine similarity search.
* Query expansion generates meaningful alternative phrasings of the original question.
* Retrieved document chunks contain sufficient information to answer the user query.

## Workflow

1. Load embedding model.
2. Connect to persisted ChromaDB vector store.
3. Generate multiple query variations using an LLM.
4. Retrieve relevant document chunks for each expanded query.
5. Aggregate and deduplicate retrieved contexts.
6. Pass the retrieved context to the LLM.
7. Generate the final answer grounded in the retrieved documents.

## Sample Query

```text
What was the automotive revenue in 2021?
```

## Expected Output

The system returns a context-grounded answer extracted from the Tesla 10-K reports.

Example:

```text
Tesla's automotive revenue for 2021 was approximately $47.2 billion.
```

(The exact response may vary depending on retrieved context and model behavior.)

## Key Learning

This assignment demonstrates how Query Expansion improves retrieval coverage by generating multiple semantically equivalent versions of a user query, resulting in more comprehensive context retrieval and potentially higher answer quality in RAG systems.
