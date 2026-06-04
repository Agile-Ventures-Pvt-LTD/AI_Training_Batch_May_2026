# Assignment 2: Improving RAG Retrieval using Query Expansion

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system on Tesla 10-K filings (2019–2023).

The objective is to improve retrieval quality by generating multiple query variations using Groq before performing vector search and comparing the results against a baseline retriever.

---

## Technologies Used

- Groq LLM (`openai/gpt-oss-120b`)
- ChromaDB
- LangChain
- HuggingFace Embeddings (`all-mpnet-base-v2`)
- Python

---

## Project Workflow

1. Load Tesla 10-K PDF reports.
2. Split documents into chunks.
3. Generate embeddings using HuggingFace.
4. Store embeddings in ChromaDB.
5. Perform baseline retrieval using the original query.
6. Generate 4–6 expanded queries using Groq.
7. Retrieve documents for all expanded queries.
8. Merge and deduplicate results using Reciprocal Rank Fusion (RRF).
9. Generate final answers with citations.
10. Compare baseline and expanded retrieval performance.

---

## Query Expansion Strategy

Query variations are generated from multiple perspectives:

- Financial Analyst View
- Risk Factor View
- Operational View
- Synonym/Subtopic View

This improves retrieval recall while preserving the original intent.

---

## Retrieval Fusion

Retrieved chunks from all expanded queries are combined using:

**Reciprocal Rank Fusion (RRF)**

Benefits:

- Better coverage
- Reduced dependence on a single query
- Improved retrieval robustness

---

## Benchmark Questions

- Q1: Supply risk vs execution/cost structure
- Q2: AI and product roadmap
- Q3: Concentration risk analysis
- Q4: Automotive vs Energy business comparison

---

## Output Format

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

## How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create .env

```text
GROQ_API_KEY=your_api_key
```

### Add Tesla Reports

Place PDF files inside:

```text
tesla-annual-reports/
```

### Run Notebook

Execute all notebook cells in order:

1. Load PDFs
2. Create embeddings
3. Build ChromaDB
4. Run benchmark questions
5. Export JSON results

---

## Results

Query expansion improved retrieval quality by:

- Increasing recall
- Retrieving evidence from multiple sections
- Producing more complete answers
- Improving citation coverage

Compared to baseline retrieval, expanded retrieval consistently returned more relevant chunks for Q1–Q4.

---

## Trade-Offs

### Advantages

- Higher recall
- Better evidence coverage
- Improved answer completeness
- Better traceability

### Disadvantages

- Higher retrieval cost
- Larger prompts
- Potential precision loss from noisy expansions

---

## Failure Modes

1. Noisy query expansions may retrieve irrelevant chunks.
2. Large contexts can exceed Groq token limits.
3. Duplicate chunks can appear across expanded queries.
4. Broad queries may retrieve unrelated sections.

### Mitigation

- Reciprocal Rank Fusion
- Deduplication
- Top-k filtering
- Metadata filtering
- Context size limits

---

## Conclusion

Query Expansion significantly improved retrieval performance over the baseline system by retrieving more relevant evidence across Tesla's 10-K filings. While it introduces additional retrieval cost and occasional noise, techniques such as RRF, deduplication, and filtering help maintain answer quality and reliability.