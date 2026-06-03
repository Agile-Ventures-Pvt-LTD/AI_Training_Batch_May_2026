# Assignment 02 - Query Expansion for Enhanced RAG Retrieval

## Participant Name

**Mohd Zaid Ansari**

## Description

This project improves document retrieval in a RAG system using **Query Expansion**. Instead of retrieving documents using only the user's original query, an LLM generates 3–4 semantically similar query variations. Each query is used for retrieval, and the final context is created from the **unique set of retrieved documents**. This helps improve retrieval recall and provides richer context for answer generation.

## How to Run

### 1. Initialize Project

```bash
uv init
```

### 2. Create Virtual Environment

```bash
uv venv
```

### 3. Activate Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 5. Configure API Key

Create a `.env` file and add:

```env
GROQ_API_KEY=your_api_key_here
```

### 6. Run the Application

```bash
python main.py
```

## Libraries / Packages Required

* Python
* Groq
* python-dotenv
* UV

## Assumptions Made

* A valid Groq API key is available.
* The retriever returns relevant document chunks for each expanded query.
* Duplicate documents are removed before generating the final context.
* The LLM generates 3–4 meaningful query variations while preserving the user's intent.

## Output Explanation

1. User enters a query.
2. The Groq model generates multiple query expansions.
3. Documents are retrieved for each expanded query.
4. Retrieved documents are merged and deduplicated.
5. A final context is generated from the unique documents.
6. The LLM produces the final answer using the aggregated context.

### Example Flow

```text
User Query
    ↓
Query Expansion (3–4 Queries)
    ↓
Document Retrieval
    ↓
Deduplication
    ↓
Final Context
    ↓
Answer Generation
```
