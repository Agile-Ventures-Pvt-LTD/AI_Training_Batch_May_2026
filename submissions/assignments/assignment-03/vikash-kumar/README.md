# Hypothetical Question Retrieval for RAG Improvement

## Overview

This project improves Retrieval-Augmented Generation (RAG) performance on Tesla Form 10-K filings using **Hypothetical Question Retrieval**.

Traditional vector search embeds and retrieves document chunks directly. However, many analyst questions are phrased differently from the language used in financial filings, causing relevant evidence to be missed.

To address this, this implementation generates hypothetical questions that each chunk can answer, embeds those questions, and uses them as an additional retrieval layer.

---

## Motivation

Financial analysts often ask abstract business questions such as:

* What risks could prevent Tesla from scaling production?
* How do warranty obligations affect future profitability?
* Which factors influence future cash flow generation?

The wording of these questions may not closely match the text found in annual reports.

Hypothetical Question Retrieval bridges this gap by indexing likely user questions alongside the original document chunks.

---

## Architecture

### Step 1: Document Ingestion

Tesla 10-K filings are loaded and split into semantically meaningful chunks.

Metadata is preserved for every chunk:

```json
{
  "chunk_id": "tsla_2025_item1a_0042",
  "source_doc": "tsla-20251231_10k.html",
  "company": "Tesla, Inc.",
  "fiscal_year": 2025,
  "form_type": "10-K",
  "section": "Item 1A - Risk Factors"
}
```

---

### Step 2: Generate Hypothetical Questions

For every chunk, an LLM generates three retrieval-oriented questions that can be answered using the chunk.

Example:

**Chunk Content**

```text
Supply chain disruptions may affect production rates and vehicle deliveries.
```

**Generated Questions**

```text
What risks could impact Tesla's production capacity?
How could supply chain issues affect vehicle deliveries?
Which operational challenges may slow Tesla's growth plans?
```

Each generated question maintains a reference to its parent chunk.

---

### Step 3: Build Hypothetical Question Index

Generated questions are embedded and stored in a dedicated vector index.

Schema:

```json
{
  "hypothetical_question": "...",
  "parent_chunk_id": "...",
  "section": "...",
  "year": 2025
}
```

This creates an alternative retrieval pathway optimized for user intent rather than document wording.

---

### Step 4: Query-Time Retrieval

When a user submits a query:

1. Embed the user query.
2. Search the hypothetical question index.
3. Retrieve the most relevant hypothetical questions.
4. Map results back to parent chunks.
5. Retrieve the original chunk content.
6. Generate the final answer using only parent chunks.

Important:

* Final answers are generated from original document chunks.
* Generated hypothetical questions are used only for retrieval.
* Citations always reference original Tesla 10-K evidence.

---

## Retrieval Pipeline

```text
User Query
      │
      ▼
Embed Query
      │
      ▼
Hypothetical Question Index
      │
      ▼
Top Matching Questions
      │
      ▼
Parent Chunk Mapping
      │
      ▼
Original Tesla 10-K Chunks
      │
      ▼
Answer Generation
```

---

## Prompt Design

### Hypothetical Question Generation Prompt

Objectives:

* Generate exactly three questions.
* Ensure questions are answerable from the chunk.
* Improve retrieval coverage.
* Avoid hallucinated facts.
* Encourage analyst-style questioning.

Question categories may include:

* Financial performance
* Business operations
* Risk analysis
* Corporate strategy
* Capital allocation
* Product and technology initiatives

---

## Benefits

### Improved Recall

Retrieves evidence even when user wording differs significantly from filing language.

### Better Support for Abstract Queries

Works well for analyst and board-level questions that use business terminology rather than exact filing terminology.

### Stronger Semantic Matching

Captures intent-based relationships that direct chunk embeddings may miss.

### Enhanced Evidence Coverage

Often retrieves relevant sections across multiple years and filing categories.

---

## Evaluation Methodology

The system is evaluated against a baseline chunk-retrieval RAG pipeline.

For each benchmark query:

1. Run baseline retrieval.
2. Run hypothetical-question retrieval.
3. Compare retrieved evidence.
4. Compare answer completeness.
5. Compare citation quality.
6. Analyze precision and recall trade-offs.

Metrics considered:

* Evidence relevance
* Citation quality
* Retrieval recall
* Retrieval precision
* Answer completeness

---

## Example Output Schema

```json
{
  "question_id": "HQ1",
  "user_query": "...",
  "retrieved_hypothetical_questions": [
    {
      "hypothetical_question": "...",
      "parent_chunk_id": "...",
      "section": "...",
      "year": 2025,
      "score": 0.84
    }
  ],
  "parent_chunks_used": [
    {
      "chunk_id": "...",
      "source_doc": "...",
      "section": "...",
      "year": 2025
    }
  ],
  "final_answer": "...",
  "citations": [],
  "comparison_with_baseline": "..."
}
```

---

## Key Findings

Hypothetical Question Retrieval is particularly effective for:

* Risk-oriented questions
* Strategic analysis questions
* Indirect business questions
* Board-level decision-making queries
* Analyst research workflows

The technique improves retrieval recall and answer completeness while maintaining answer grounding through original Tesla 10-K evidence.

---

## Limitations

* Additional LLM cost for question generation.
* Larger index size due to generated questions.
* Poorly generated questions can introduce retrieval noise.
* Requires periodic regeneration when new filings are added.

---

## Future Improvements

* Hybrid retrieval combining baseline and hypothetical-question results.
* Cross-encoder reranking.
* Multi-query expansion before hypothetical retrieval.
* Automatic quality filtering for generated questions.
* Incremental index updates for newly released filings.
