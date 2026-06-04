# Assignment 02 - Query Expansion for Enhanced RAG Retrieval

## Participant Name

**Mohd Zaid Ansari**

## Description

This project enhances Retrieval-Augmented Generation (RAG) performance using **Query Expansion** and **Retrieval Fusion** techniques.

Instead of retrieving documents using only the user's original query, the system generates multiple semantically diverse query variants using Groq LLM. The expanded queries are designed from different perspectives such as:

* Financial analyst phrasing
* Risk-factor phrasing
* Operational/business phrasing
* Strategic phrasing
* Financial performance phrasing
* Synonym/subtopic phrasing

Each expanded query performs independent retrieval against a vector database.

Retrieved chunks are then merged and ranked using **Reciprocal Rank Fusion (RRF)** to improve retrieval recall while maintaining relevance.

The system compares:

1. Baseline retrieval using the original query.
2. Query-expanded retrieval using multiple generated queries.

The final answer is generated using the fused retrieval context and includes traceable citations.

---

## Features

### Baseline Retrieval

* Retrieves relevant document chunks using only the original user query.
* Used as a benchmark for comparison.

### Query Expansion

* Generates 4–6 semantically diverse query variants.
* Preserves the original intent of the user's question.
* Improves retrieval coverage across different document sections.

### Retrieval Fusion

* Retrieves documents for each expanded query.
* Combines retrieval results using Reciprocal Rank Fusion (RRF).
* Removes duplicate chunks.
* Tracks which expanded query retrieved each chunk.

### Answer Generation

* Uses the fused retrieval context.
* Produces evidence-based answers.
* Includes citations linked to retrieved chunks.

### Benchmark Evaluation

The system evaluates retrieval performance using the following benchmark questions:

* Q1: Growth constraints (supply risk vs execution risk)
* Q2: AI roadmap and operational priorities
* Q3: Supplier and concentration risk
* Q4: Automotive vs Energy business strategy

---

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

#### Windows

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 5. Configure API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```
---

## Libraries / Packages Required

* Python
* Groq
* python-dotenv
* LangChain
* ChromaDB
* Sentence Transformers / Embedding Model
* UV

---

## Assumptions Made

* A valid Groq API key is available.
* Vector embeddings accurately represent document semantics.
* The retriever returns relevant chunks for both baseline and expanded queries.
* Query expansion preserves the original user intent.
* Reciprocal Rank Fusion improves retrieval diversity and recall.
* Duplicate chunks are removed before answer generation.

---

## Retrieval Workflow

```text
User Query
    ↓
Baseline Retrieval
    ↓
Generate 4–6 Expanded Queries
    ↓
Retrieve Documents for Each Query
    ↓
Reciprocal Rank Fusion (RRF)
    ↓
Deduplicate Chunks
    ↓
Create Final Context
    ↓
Answer Generation
    ↓
Structured JSON Output
```

---

## Output Schema

```json
{
  "question_id": "Q1",
  "original_query": "...",
  "expanded_queries": [
    "...",
    "..."
  ],
  "baseline_top_chunks": [
    {
      "chunk_id": "...",
      "section": "...",
      "score": 0.81
    }
  ],
  "expanded_top_chunks": [
    {
      "chunk_id": "...",
      "section": "...",
      "score": 0.88,
      "retrieved_by": [
        "expanded query"
      ]
    }
  ],
  "final_answer": "...",
  "citations": [
    {
      "chunk_id": "...",
      "source_doc": "...",
      "section": "..."
    }
  ],
  "retrieval_improvement_analysis": "..."
}
```

---

## Evaluation Questions

The following benchmark questions were used:

### Q1

Does Tesla's growth story appear more constrained by external supply risk or internal execution and cost structure?

### Q2

Explain how Tesla's AI and product roadmap is reflected in spending, operational priorities, and risk disclosures.

### Q3

Assess Tesla's exposure to concentration risk across factories, suppliers, raw materials, and geographies.

### Q4

Compare the strategic importance of automotive operations and energy generation/storage using evidence from the 10-K.

---

## Retrieval Improvement Analysis

The project compares baseline retrieval against query-expanded retrieval and evaluates:

* Which benchmark questions improved most after expansion.
* Which query variants introduced irrelevant retrieval.
* Recall versus precision trade-offs.
* Strategies for controlling noisy query expansions.
* Potential metadata filters for year-specific or section-specific analysis.

---

## Output Files

Results are stored as:

```text
assignment2_results.json
```

containing benchmark outputs, retrieved chunks, citations, and retrieval analysis for all evaluation questions.
