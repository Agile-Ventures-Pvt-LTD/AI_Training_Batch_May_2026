# Assignment 1: Improving RAG Retrieval Using Query Expansion

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline for answering analytical questions from Tesla's annual 10-K filings (2019–2023).

The objective is to improve document retrieval quality by applying Query Expansion before vector search and comparing the results against a baseline retrieval system.

The solution uses:

* Groq LLM (`openai/gpt-oss-120b`) for query expansion and answer generation
* ChromaDB for vector storage
* LangChain for document ingestion and retrieval
* HuggingFace Embeddings (`all-mpnet-base-v2`) for semantic search

---

# Problem Statement

Financial analysts often ask broad strategic questions that do not exactly match the wording used in SEC filings.

Example:

> Does Tesla's growth story appear more constrained by external supply risk or internal execution and cost structure?

A standard vector search may miss relevant evidence because the filing uses different terminology.

To address this issue, query expansion is used to generate multiple semantically related retrieval queries before performing vector search.

---

# Solution Architecture

```text
Tesla 10-K PDFs
       │
       ▼
Document Loader
       │
       ▼
Chunking
       │
       ▼
Embedding Generation
       │
       ▼
Chroma Vector Database
       │
       ├───────────────► Baseline Retrieval
       │
       ▼
Query Expansion (Groq)
       │
       ▼
Multiple Expanded Queries
       │
       ▼
Vector Search
       │
       ▼
Retrieval Fusion
       │
       ▼
Deduplication
       │
       ▼
Context Construction
       │
       ▼
Answer Generation (Groq)
       │
       ▼
JSON Output
```

---

# Technologies Used

| Component       | Technology                              |
| --------------- | --------------------------------------- |
| LLM             | Groq GPT OSS 120B                       |
| Embeddings      | sentence-transformers/all-mpnet-base-v2 |
| Vector Database | ChromaDB                                |
| Framework       | LangChain                               |
| Language        | Python                                  |
| Data Source     | Tesla 10-K Filings (2019–2023)          |

---

# Project Configuration

```python
MODEL_NAME = "openai/gpt-oss-120b"

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

CHROMA_DB_PATH = "./tesla_db"

COLLECTION_NAME = "tesla-10k-2019-to-2023"

CHUNK_SIZE = 512

CHUNK_OVERLAP = 16

TOP_K = 5
```

---

# Data Ingestion

The project loads Tesla annual reports from PDF files.

Steps:

1. Load PDFs using PyPDFDirectoryLoader
2. Split documents into chunks
3. Generate embeddings
4. Store embeddings in ChromaDB

Chunk metadata is retained to support:

* Source tracking
* Citation generation
* Retrieval analysis

---

# Baseline Retrieval

The baseline system performs retrieval using only the original user question.

Example:

```text
Original Query:
What was Tesla's automotive revenue in 2021?
```

Process:

1. Embed query
2. Perform similarity search
3. Retrieve top-k chunks
4. Generate answer

Limitations:

* Vocabulary mismatch
* Missing related sections
* Lower recall

---

# Query Expansion Strategy

The improved retriever generates multiple query variants using Groq.

Expansion is performed from four perspectives:

### 1. Financial Analyst Perspective

Example:

```text
How did Tesla's supply chain constraints affect growth?
```

### 2. Risk Factor Perspective

Example:

```text
What risks limited Tesla's production expansion?
```

### 3. Operational Perspective

Example:

```text
How did manufacturing and logistics challenges impact Tesla?
```

### 4. Synonym/Subtopic Perspective

Example:

```text
Did sourcing and procurement challenges constrain Tesla growth?
```

Generated queries preserve the original intent while increasing recall.

---

# Retrieval Fusion

Each expanded query retrieves documents independently.

Retrieved chunks are combined using:

## Reciprocal Rank Fusion (RRF)

Formula:

```text
Score = Σ 1 / (k + rank)
```

Benefits:

* Robust ranking
* Combines evidence from multiple retrieval paths
* Reduces dependence on a single query formulation

---

# Deduplication

Duplicate chunks retrieved by multiple expanded queries are removed.

The system also records:

```json
{
  "retrieved_by": "expanded query text"
}
```

This provides retrieval traceability.

---

# Answer Generation

The final context is built from the highest-ranked fused chunks.

Groq GPT OSS 120B generates the final answer using:

* Retrieved evidence only
* No external knowledge
* Explicit citation support

---

# Benchmark Questions

The following benchmark questions were evaluated.

## Q1

Does Tesla's growth story appear more constrained by external supply risk or internal execution and cost structure?

## Q2

Explain how Tesla's AI and product roadmap is reflected in spending, operational priorities, and risk disclosures.

## Q3

A supplier asks whether Tesla is exposed to concentration risk across factories, suppliers, raw materials, or geographies.

## Q4

Compare the strategic importance of automotive operations and energy generation/storage.

---

# Output Schema

Each question produces a structured JSON output.

```json
{
  "question_id": "Q1",
  "original_query": "...",
  "expanded_queries": [],
  "baseline_top_chunks": [],
  "expanded_top_chunks": [],
  "final_answer": "...",
  "citations": [],
  "retrieval_improvement_analysis": "..."
}
```

---

# How to Run

## Step 1: Clone Project

```bash
git clone <repository-url>
cd assignment1-rag-query-expansion
```

## Step 2: Create Environment

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create:

```text
.env
```

Add:

```text
GROQ_API_KEY=<your-api-key>
```

---

## Step 5: Add Tesla Annual Reports

Place PDFs inside:

```text
tesla-annual-reports/
```

Example:

```text
tesla-annual-reports/
├── Tesla_2019_10K.pdf
├── Tesla_2020_10K.pdf
├── Tesla_2021_10K.pdf
├── Tesla_2022_10K.pdf
└── Tesla_2023_10K.pdf
```

---

## Step 6: Build Vector Database

Run notebook cells for:

* Loading documents
* Chunking
* Embedding generation
* Chroma persistence

---

## Step 7: Execute Benchmark Questions

Run:

```python
all_results = run_benchmark()
```

---

## Step 8: Export Results

```python
with open("results.json", "w") as f:
    json.dump(all_results, f, indent=4)
```

---

# Comparative Analysis

| Question | Baseline Quality | Expanded Quality |
| -------- | ---------------- | ---------------- |
| Q1       | Medium           | High             |
| Q2       | Medium           | High             |
| Q3       | Medium           | High             |
| Q4       | Medium           | High             |

Query expansion consistently improved retrieval coverage across multiple 10-K sections.

---

# Trade-Off Analysis

## Advantages

### Higher Recall

Expanded queries retrieve evidence that would otherwise be missed.

### Better Coverage

Questions spanning multiple sections benefit significantly.

### Improved Answer Completeness

More relevant chunks are available for answer generation.

### Better Traceability

Retrieved chunks can be linked back to individual expanded queries.

---

## Disadvantages

### Increased Retrieval Cost

Multiple vector searches are performed.

### Larger Context Windows

Expanded retrieval may generate large prompts.

This required:

* Context truncation
* Top-k filtering

to remain within Groq token limits.

### Precision Reduction

Some expanded queries retrieved partially relevant chunks.

Example:

Questions about AI occasionally retrieved general automation discussions.

---

# Failure Modes

## 1. Noisy Query Expansion

Some generated variants introduce broader terminology.

Example:

```text
AI strategy
```

retrieving generic technology discussions.

Impact:

* Lower precision
* Increased context size

Mitigation:

* Similarity threshold filtering
* Expansion quality validation

---

## 2. Token Limit Exceeded

Large retrieval sets can exceed Groq limits.

Observed:

```text
413 Request Too Large
```

Mitigation:

* Restrict context to top-ranked chunks
* Limit context size before generation

---

## 3. Duplicate Retrieval

Multiple expanded queries may retrieve identical chunks.

Mitigation:

* Deduplication
* Reciprocal Rank Fusion

---


# Conclusion

The query expansion approach significantly improved retrieval recall and evidence coverage across Tesla 10-K filings.

Compared with baseline retrieval, expanded retrieval consistently surfaced additional relevant sections from Risk Factors, MD&A, Business Overview, and Segment Reporting, resulting in more complete and better-supported answers.

While query expansion introduces additional retrieval cost and potential precision loss, these issues can be controlled through retrieval fusion, deduplication, metadata filtering, and context-size management.

The final system demonstrates a practical and scalable approach for improving RAG performance in financial document analysis.
