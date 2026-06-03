# Advanced RAG Retrieval Evaluation – Assignment 1: Query Expansion Retrieval

## Information

**Name:** Taniya Gupta

## Assignment Title

**Advanced RAG Retrieval Evaluation: Query Expansion on Tesla 10-K Documents**

---

## Project Overview

This project evaluates the impact of Query Expansion on Retrieval-Augmented Generation - RAG systems using Tesla Form 10-K filings as the knowledge corpus.

Multiple query variants were generated for each user question, and retrieval was performed independently for each variant. The retrieved results were merged and deduplicated before being used for answer generation.

The objective of this assignment was to determine whether query expansion improves retrieval quality.

---

## Technologies Used

* Python
* Groq API
* LangChain
* ChromaDB
* Sentence Transformers
* Jupyter Notebook
* Tesla Form 10-K Filings documents

---

## System Architecture

### Baseline Retrieval Pipeline

1. User submits a query.
2. Query is embedded using the embedding model.
3. ChromaDB retrieves the most similar document chunks.
4. Retrieved context is provided to the LLM.
5. The final answer is generated.

### Query Expansion Pipeline

1. User submits a query.
2. Groq generates multiple alternative query formulations.
3. Each expanded query performs retrieval independently.
4. Retrieved chunks from all searches are combined.
5. Duplicate chunks are removed.
6. The consolidated context is passed to the LLM.
7. The final answer is generated using the expanded evidence set.

---

## Dataset

The corpus consists of Tesla Form 10-K annual reports.

Documents were:

* Loaded using LangChain document loaders
* Split into overlapping chunks
* Embedded using Sentence Transformers
* Indexed in ChromaDB for similarity search


---

## Query Expansion Strategy

For each benchmark question, Groq generated multiple query variants from different perspectives:

1. Financial Analyst Perspective
2. Risk Factor Perspective
3. Operational Perspective
4. Strategic Perspective
5. Supply Chain Perspective
6. Alternative Terminology Perspective

The goal was to improve retrieval recall by introducing terminology that may not appear in the original user query.

---

## Benchmark Questions

### Q1

Does Tesla's growth story appear more constrained by external supply risk or internal execution and cost structure?

### Q2

Explain how Tesla's AI and product roadmap is reflected in spending, operational priorities, and risk disclosures.

### Q3

Assess Tesla's concentration risk across factories, suppliers, raw materials, and geographies.

### Q4

Compare the strategic importance of automotive operations and energy generation/storage.

---

## Experimental Results

| Question | Baseline Evidence Quality | Expanded Evidence Quality |
| -------- | ------------------------- | ------------------------- |
| Q1       | Medium                    | High                      |
| Q2       | Medium                    | High                      |
| Q3       | Low                       | Medium-High               |
| Q4       | Medium                    | High                      |

### Key Observations

* Query expansion improved retrieval coverage across all benchmark questions.
* Q3 showed the largest improvement because expanded queries introduced supplier, factory, geographic, and raw-material terminology that was not captured by the original query.
* Expanded retrieval surfaced additional evidence from risk-related and operational sections of Tesla filings.
* Retrieval recall improved significantly compared to baseline retrieval.

---


## Running the Project

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=yourapikey
```

### Launch Notebook

```bash
jupyter notebook
```

Open:

```text
Assignment_2_solution.ipynb
```

Run all cells sequentially.

---

## Required Libraries

```text
chromadb
langchain
langchain-community
langchain-chroma
sentence-transformers
groq
python-dotenv
numpy
pandas
jupyter
```

---

## Repository Structure

```text
assignment/
│
├── Assignment_2_solution.ipynb
├── README.md
├── requirements.txt
├── tesla_db/
├── query_expansion_evaluation.json
└── .env.example
```

---

## Conclusion

The experiment demonstrates that query expansion improves retrieval performance. By generating multiple perspectives of the original query, the system was able to retrieve a broader and more relevant evidence set than baseline similarity search alone. 
---

## Author

**Taniya Gupta**
