# Advanced RAG Retrieval Evaluation

## Participant Name
Nandani Bisht

## Assignment Title
Advanced RAG Retrieval Evaluation — Query Expansion and Hypothetical Question Retrieval on Tesla 10-K Documents

## Description
Two retrieval improvement pipelines built over Tesla Form 10-K filings (2019–2023):

**Assignment 1 — Query Expansion** (`A001_QueryExpansion.ipynb`): Generates 4–6 alternative phrasings of a user query using an LLM, retrieves evidence for each in parallel, deduplicates results, and synthesises a cited answer. Compares against single-query baseline retrieval.

**Assignment 2 — Hypothetical Question Retrieval** (`A003_HypotheticalRetrieval.ipynb`): For each document chunk, generates 3 hypothetical questions the chunk can answer and indexes them in a separate vector store. At query time, retrieves matching hypothetical questions and maps them back to the parent chunks. Compares against direct chunk retrieval.

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API keys in .env
echo "GROQ_API_KEY=your_key_here" > .env
# Optional (faster): echo "NVIDIA_API_KEY=your_key_here" >> .env

# 3. Launch Jupyter
jupyter notebook

# 4. Run A003 first (builds the corpus DB), then A001
#    Kernel → Restart & Run All in each notebook
```

Run `A003_HypotheticalRetrieval.ipynb` before `A001_QueryExpansion.ipynb` — both share the same ChromaDB instance.

## Libraries Required

See `requirements.txt`. Key packages:

- `openai` — LLM API client (NVIDIA NIMs or Groq)
- `groq` — Groq API fallback
- `chromadb` — vector database
- `langchain`, `langchain-chroma`, `langchain-huggingface` — RAG pipeline
- `sentence-transformers` — embedding model (`all-mpnet-base-v2`)
- `pypdf` — PDF ingestion

## Assumptions

- Tesla 10-K PDFs (2019–2023) are placed in `./tesla-annual-reports/`
- API key is set in `.env` as `GROQ_API_KEY` or `NVIDIA_API_KEY`
- NVIDIA NIMs is used as primary provider if `NVIDIA_API_KEY` is present (200K TPM vs Groq's 6K TPM), otherwise falls back to Groq
- Chunk size: 500 tokens with 50 token overlap for ingestion; rechunked to 1000 tokens with 150 overlap for hypothetical question generation
- Embeddings run on CPU; `batch_size=128` used for throughput

## Output Files

| File | Description |
|------|-------------|
| `benchmark_outputs_query_expansion.json` | Q1–Q4 results for Assignment 1 in required schema |
| `hyp_questions_progress_v2.json` | Generated hypothetical questions for all chunks |
| `tesla_db/` | Persisted ChromaDB collections |

## Files Included

```
A001_QueryExpansion.ipynb          Assignment 1 notebook
A003_HypotheticalRetrieval.ipynb   Assignment 2 notebook
requirements.txt                   All dependencies
README.md                          This file
tesla-annual-reports/              Tesla 10-K PDFs (2019–2023)
tesla_db/                          ChromaDB vector store
benchmark_outputs_query_expansion.json   Saved benchmark outputs
hyp_questions_progress_v2.json     Saved hypothetical questions
```
