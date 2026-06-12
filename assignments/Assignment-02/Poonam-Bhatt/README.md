# Query Expansion for Retrieval Improvement in RAG Systems

## 1. Name

Poonam Bhatt

## 2. Assignment / Project Title

Query Expansion for Improving Retrieval in RAG Systems

## 3. Short Description of What I Built

This project implements the **Query Expansion retrieval enhancement technique** in a Retrieval-Augmented Generation (RAG) pipeline built using Tesla Annual Report data.

The system improves document retrieval by generating multiple semantically similar versions of the user's original query using the **Groq API (Llama-3.1-8B-Instant model)**.

Workflow:

* User enters a query.
* The system generates **3 expanded queries** preserving original meaning and company context.
* Each expanded query retrieves relevant document chunks from the vector database.
* Retrieved chunks are combined into context.
* The LLM generates the final answer using retrieved context.
* All expanded queries are automatically saved into a JSON log file for tracking and evaluation.

## 4. Steps to Run the Code

1. Create virtual environment:

```bash
python -m venv .venv
```

2. Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

3. Install required libraries:

```bash
pip install -r requirements.txt
```

4. Set API key:

```bash
GROQ_API_KEY=your_api_key
```

5. Run notebook or Python file.

6. Execute:

```python
respond_query_expansion(
    "What was the automotive revenue in 2021?"
)
```

## 5. Libraries or Packages Required

* groq
* chromadb
* langchain
* langchain-community
* langchain-chroma
* pypdf
* tiktoken
* json
* os
* datetime

## 6. Assumptions Made

* Tesla Annual Report embeddings already exist inside ChromaDB.
* Groq API key is valid and configured.
* Retrieval database is properly persisted and accessible.
* Expanded queries preserve the original semantic intent.

## 7. Output Explanation

Example Input:

```text
What was the automotive revenue in 2021?
```

Generated Expanded Queries:

```text
What was Tesla's automotive revenue in 2021?
How much automotive revenue did Tesla generate in 2021?
What is Tesla's 2021 automotive revenue figure?
```

Final Output:

```text
The automotive revenue in 2021 was $47,232 million.
```

JSON Log Example:

```json
{
  "original_query":"What was the automotive revenue in 2021?",
  "expanded_queries":[
    "...",
    "...",
    "..."
  ]
}
```
