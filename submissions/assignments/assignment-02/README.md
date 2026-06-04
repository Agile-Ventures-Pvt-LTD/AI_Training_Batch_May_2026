# Advanced RAG Retrieval Evaluation using Query Expansion

**Author:** Vikash Kumar

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system for answering financial analysis questions using Tesla Form 10-K annual reports. The primary objective is to improve retrieval quality through **Query Expansion**, enabling the system to discover relevant evidence even when user queries use terminology different from that found in the filings.

The solution compares a baseline semantic retrieval approach against an enhanced retrieval pipeline that generates multiple query variants using a Large Language Model (LLM), retrieves evidence for each variant, and combines the results to improve coverage and answer quality.

---

## Objectives

### Baseline Retrieval

* Load Tesla 10-K documents.
* Create document chunks with metadata.
* Generate embeddings and store them in a vector database.
* Retrieve relevant chunks using the original user query.
* Generate grounded answers using retrieved evidence.

### Query Expansion Retrieval

* Generate multiple semantically related query variants.
* Retrieve documents for each expanded query.
* Combine and deduplicate retrieval results.
* Improve recall while preserving relevance.
* Generate evidence-based answers with citations.

### Evaluation

* Compare baseline retrieval against expanded retrieval.
* Analyze retrieval quality, citation quality, recall, and precision.
* Identify retrieval improvements and failure modes.

---

## Project Workflow

### 1. Document Ingestion

Tesla 10-K filings are loaded and processed.

### 2. Text Chunking

Documents are split into overlapping chunks while preserving context.

### 3. Metadata Preservation

Each chunk retains metadata such as:

```json
{
  "chunk_id": "tsla_2025_item1a_0042",
  "source_doc": "Tesla_2025_10K.pdf",
  "company": "Tesla, Inc.",
  "fiscal_year": 2025,
  "section": "Item 1A - Risk Factors"
}
```

### 4. Embedding Generation

Embeddings are created using a Hugging Face embedding model.

### 5. Vector Database Creation

Embeddings are stored in a persistent ChromaDB vector database.

### 6. Baseline Retrieval

Relevant chunks are retrieved using the original user query.

### 7. Query Expansion

The Groq LLM generates multiple query variants from different perspectives:

* Financial analyst phrasing
* Risk-factor phrasing
* Operational phrasing
* Strategic phrasing
* Synonym-based phrasing

### 8. Retrieval Fusion

Results from expanded queries are combined and deduplicated.

### 9. Answer Generation

Retrieved evidence is provided to the LLM to generate grounded answers.

### 10. Comparative Analysis

Baseline and expanded retrieval pipelines are evaluated and compared.

---

## Technologies Used

### Large Language Model

* Groq API

### Embeddings

* HuggingFace Embeddings

### Vector Database

* ChromaDB

### Frameworks

* LangChain
* Python

### Document Processing

* PDF Loaders
* Recursive Character Text Splitter

---

## Repository Structure

```text
.
├── assignment_2_new.ipynb
├── data/
│   ├── tesla_2023_10k.pdf
│   ├── tesla_2024_10k.pdf
│   └── tesla_2025_10k.pdf
├── chroma_db/
├── outputs/
│   ├── baseline_results.json
│   ├── expanded_results.json
│   └── comparison_results.json
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Running the Notebook

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```text
assignment_2_new.ipynb
```

Execute all cells sequentially.

---

## Query Expansion Example

### Original Query

```text
Does Tesla's growth story appear more constrained by external supply risk or internal execution and cost structure?
```

### Expanded Queries

```text
Tesla supply chain and raw material dependency risks

Tesla manufacturing execution and operational efficiency challenges

Factors affecting Tesla growth and production scalability

Tesla cost structure and profitability constraints

Tesla risk disclosures related to suppliers and operations
```

---

## Answer Generation Strategy

The system:

1. Retrieves relevant chunks.
2. Passes retrieved evidence to the LLM.
3. Generates grounded answers.
4. Includes supporting citations.

Example:

```text
Tesla's growth appears constrained by both external supply risks and internal execution challenges.
The company identifies risks related to supplier dependency, raw material availability,
production ramp-up, and manufacturing efficiency. [expanded_2, expanded_5]
```

---

## Evaluation Metrics

### Retrieval Quality

* Relevance of retrieved chunks
* Coverage across sections
* Evidence completeness

### Answer Quality

* Accuracy
* Groundedness
* Citation quality

### Comparative Analysis

* Recall improvement
* Precision trade-offs
* Failure mode identification

---

## Expected Outputs

For each benchmark question:

```json
{
  "question_id": "Q1",
  "original_query": "...",
  "expanded_queries": [
    "...",
    "..."
  ],
  "baseline_top_chunks": [],
  "expanded_top_chunks": [],
  "final_answer": "...",
  "citations": [],
  "retrieval_improvement_analysis": "..."
}
```

---

## Key Learnings

* Query expansion improves retrieval recall.
* Diverse query perspectives uncover additional evidence.
* Retrieval fusion increases document coverage.
* Excessive expansion can introduce retrieval noise.
* Proper citation tracking improves answer transparency.

---

## Future Improvements

* Reciprocal Rank Fusion (RRF)
* Hybrid Retrieval (BM25 + Vector Search)
* Metadata-aware filtering
* Reranking models
* Automated retrieval evaluation using RAGAS

---

## Security

* API keys are stored in environment variables.
* No secrets are committed to source control.
* `.gitignore` excludes sensitive files and generated databases.


---

## Author

**Vikash Kumar**
