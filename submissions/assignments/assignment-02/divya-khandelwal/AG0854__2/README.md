# Query Expansion in Retrieval-Augmented Generation (RAG)

## Overview

This project demonstrates the implementation of **Query Expansion** in a Retrieval-Augmented Generation (RAG) pipeline. Query Expansion improves retrieval quality by generating multiple semantically related variations of a user's query before searching the vector database.

The goal is to increase the likelihood of retrieving relevant documents and improve the quality of generated responses.

---

## Objective

Traditional RAG systems rely on a single user query for retrieval. However, a user's query may not contain all the keywords or context needed to retrieve the most relevant information.

Query Expansion addresses this problem by:

* Generating alternative versions of the original query.
* Expanding the semantic search space.
* Improving document recall.
* Enhancing the final response quality.

---

## Project Workflow

### 1. User Query

The user submits a question.

**Example:**

```text
What are the benefits of renewable energy?
```

### 2. Query Expansion

An LLM generates multiple variations of the query.

**Generated Queries:**

```text
Advantages of renewable energy
Benefits of sustainable energy sources
Why is renewable energy important?
Positive impacts of clean energy
```

### 3. Embedding Generation

The original query and expanded queries are converted into vector embeddings.

### 4. Vector Search

The embeddings are used to retrieve relevant documents from the vector database.

### 5. Context Aggregation

Retrieved documents from all expanded queries are combined and ranked.

### 6. Response Generation

The retrieved context is passed to the LLM to generate the final answer.

---

## Technologies Used

* Python
* LangChain
* ChromaDB
* OpenAI / Groq API
* Embedding Models
* Jupyter Notebook

---

## Project Structure

```text
AG0854_2/
│
├── .venv/                     # Virtual environment
├── tesla_db/                  # Chroma vector database
├── tesla-annual-reports/      # Source documents
│
├── .env                       # API keys and environment variables
├── .gitignore                 # Git ignore rules
├── .python-version            # Python version configuration
├── main.py                    # Main application script
├── query_expansion.ipynb      # Query Expansion implementation notebook
├── pyproject.toml             # Project dependencies and configuration
├── requirements.txt           # Python dependencies
├── uv.lock                    # Dependency lock file
└── README.md                  # Project documentation
```

---

## Key Benefits of Query Expansion

* Improves document retrieval accuracy.
* Reduces missed relevant documents.
* Enhances answer quality.
* Handles ambiguous user queries effectively.
* Increases semantic coverage during retrieval.

---

## Example

### Original Query

```text
How can AI improve healthcare?
```

### Expanded Queries

```text
Applications of AI in healthcare
Benefits of artificial intelligence in medicine
How AI helps doctors and hospitals
AI-powered healthcare solutions
```

### Retrieved Context

Relevant healthcare and AI-related documents are retrieved from the vector database.

### Final Response

The LLM generates a comprehensive answer using the retrieved context.

---

## Challenges

* Increased retrieval cost.
* Additional LLM calls for query generation.
* Potential retrieval of redundant documents.
* Need for result deduplication and ranking.

---

## Conclusion

Query Expansion significantly improves the effectiveness of Retrieval-Augmented Generation systems by increasing retrieval recall and providing richer context to the language model. This leads to more accurate, relevant, and comprehensive responses compared to traditional single-query retrieval approaches.

---

## Author

**Divya Khandelwal**

Assignment: Query Expansion in RAG
AI Training Batch May 2026
