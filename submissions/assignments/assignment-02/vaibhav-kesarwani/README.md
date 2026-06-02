# Assignment 02 - Advanced RAG Retrieval System (Query Expansion)

## Participant Name
Vaibhav Kesarwani

## Project Title
Advanced RAG Retrieval with Query Expansion

## Description
This project demonstrates a **advance Retrieval-Augmented Generation (RAG) system** that uses **query expansion techniques** to improve retrieval quality.  
The system expands user queries using semantic embeddings before retrieving documents, ensuring more relevant context is passed to the language model.  
It integrates the **Groq API** for generation, the **all-mpnet-base-v2** embedding model for query expansion, and **ChromaDB** as the vector database to store and retrieve documents efficiently.

## How to Run

### Step 1: Initalise the UV

```bash
uv init
```

### Step 2: Initalise the virtual environment

```bash
uv venv
```

### Step 2: Install dependencies using uv

```bash
uv add -r requirements.txt
```

### Step 3: Make the env file

`.env` file
```bash
GROQ_API_KEY="..."
```

### Step 4: Run the main notebook

```bash
main.ipynb
```

## Libraries/Packages Required

- Python 3.11
- uv 
- sentence-transformers
- chromadb
- langchain
- groq

## Assumptions Made

- ChromaDB is used as the vector database for retrieval.
- The Embedding model which is used to create the embedding is all-mpnet-base-v2.
- Groq API is used for final answer generation.
- API keys are stored securely in a .env file.
- This is used for the fast reterival of the system, focusing on core functionality.

## Output

![output](./assets/query-expansion.png)