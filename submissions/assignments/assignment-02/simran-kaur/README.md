
# Assignment 02 - Advanced RAG Retrieval using Query Expansion

## Participant Name
Simran Kaur



## Assignment Title
Advanced Retrieval-Augmented Generation (RAG) System using Query Expansion on Tesla 10-K Financial Documents



## Description
This project implements a Retrieval-Augmented Generation (RAG) system designed to answer financial analysis questions using Tesla 10-K annual reports stored in a vector database (ChromaDB).

The system improves retrieval quality using **Query Expansion**, where a single user query is transformed into multiple semantically diverse queries using a Large Language Model (Groq API). These expanded queries are used to retrieve relevant document chunks from a prebuilt vector database.

The retrieved context is then passed to a Groq-based LLM which generates a final grounded answer strictly based on retrieved information.

Key capabilities of the system include:
- Query expansion using LLM for improved retrieval coverage
- Vector similarity search using ChromaDB
- Dense embeddings using sentence-transformers
- Retrieval fusion using multiple expanded queries
- Context-grounded answer generation using Groq API
- Structured JSON output for evaluation

---

## How to Run

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Set environment variables
export GROQ_API_KEY="your_api_key"

# Step 3: Run the  notebook
jupyter notebook assignment_02_solution.ipynb
````

---

## Libraries or Packages Required

* groq>=1.2.0
* chromadb>=0.6.3
* langchain==0.3.20
* langchain-community==0.3.19
* langchain-chroma==0.2.2
* sentence-transformers==5.1.2
* python-dotenv>=1.2.2
* datasets>=3.3.2
* tiktoken==0.9.0
* pypdf==5.4.0
* ipykernel>=7.2.0

---

## Assumptions Made

* The Tesla 10-K corpus is already preprocessed and stored in a ChromaDB vector database (`tesla_db`).
* The vector database is pre-built; raw PDF ingestion is not part of this submission.
* Retrieval is performed only using semantic similarity search.
* No external internet or web search is used for answering queries.
* Metadata (such as chunk_id, section, or fiscal year) is not required in the final submission format.
* Query expansion improves retrieval by generating multiple semantically different variations of the same question.
* Final answers are strictly generated using retrieved context only.

---

## Output Format

The system generates a single JSON file:

```
outputs/rag_results.json
```

---

## Output Structure

Each result in the JSON file contains:

* question_id → Identifier for each benchmark question (Q1–Q4)
* original_query → The input question from benchmark set
* expanded_queries → LLM-generated query variations
* final_answer → Answer generated using retrieved context

---

## Example Output

```json
{
  "results": [
    {
      "question_id": "Q1",
      "original_query": "Does Tesla's growth story appear more constrained by external supply risk or internal execution?",
      "expanded_queries": [
        "Tesla growth supply chain constraints",
        "internal execution challenges Tesla scaling",
        "Tesla risk factors growth limitations"
      ],
      "final_answer": "Tesla's growth is more constrained by internal execution challenges such as manufacturing scale and operational efficiency..."
    }
  ]
}
```

---

## Notes

* This project focuses on improving retrieval quality rather than memorizing answers.
* Query Expansion significantly increases recall by retrieving semantically diverse relevant chunks.
* The system ensures all answers are grounded strictly in retrieved Tesla 10-K content.
* The architecture is modular and can be extended to Hypothetical Question Retrieval or hybrid RAG pipelines.


