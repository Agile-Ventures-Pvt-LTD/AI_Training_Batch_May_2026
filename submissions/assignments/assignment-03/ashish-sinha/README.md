# Assignment A003 – Improving RAG Retrieval using Hypothetical Questions

## Overview

This project improves Retrieval-Augmented Generation (RAG) performance on Tesla 10-K filings by using **Hypothetical Question Retrieval (HQR)**.

Traditional RAG retrieves document chunks based on semantic similarity between the user query and chunk text. However, business-oriented queries often use language that differs significantly from the wording used in financial filings.

To address this issue, hypothetical questions are generated for each chunk and indexed separately. User queries are matched against these hypothetical questions, and the retrieved questions are mapped back to their original parent chunks for grounded answer generation.

---

## Project Structure

```text
.
│
├── tesla-annual-reports/
│   ├── tsla-2019.pdf
│   ├── tsla-2020.pdf
│   ├── tsla-2021.pdf
│   ├── tsla-2022.pdf
│   └── tsla-2023.pdf
│
├── tesla_db/
│   ├── baseline chunk index
│   └── hypothetical question index
│
├── tesla_hypothetical_questions.json
│
├── HQ1.json
├── HQ2.json
├── HQ3.json
├── HQ4.json
│
├── comparison_table.csv
├── analysis_answers.json
│
├── Assignment_A003.ipynb
│
├── requirements.txt
│
└── README.md
```

---

## Environment Setup

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

Required libraries include:

```text
chromadb
langchain
langchain-community
langchain-chroma
sentence-transformers
python-dotenv
openai
tqdm
pandas
```

---

## API Configuration

Create a `.env` file in the project root.

```env
NVIDIA_API_KEY=YOUR_NVIDIA_API_KEY
```

The project uses NVIDIA NIMs through the OpenAI-compatible API endpoint.

```python
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)
```

Model used:

```python
meta/llama-3.1-70b-instruct
```

Embedding model:

```python
sentence-transformers/all-mpnet-base-v2
```

---

## Execution Steps

### Step 1 – Load Tesla Filings

Load all Tesla annual reports.

```python
pdf_loader = PyPDFDirectoryLoader(
    "tesla-annual-reports"
)
```

---

### Step 2 – Chunk Documents

Documents are split using:

```python
RecursiveCharacterTextSplitter
```

Configuration:

```python
chunk_size = 512
chunk_overlap = 16
```

Metadata retained:

* chunk_id
* source_doc
* year
* section
* page number

---

### Step 3 – Build Baseline Vector Index

Create a ChromaDB collection containing original Tesla chunks.

```python
vectorstore_persisted
```

This index is used for baseline retrieval.

---

### Step 4 – Generate Hypothetical Questions

For each chunk:

* Generate exactly 3 hypothetical questions.
* Questions must be answerable from the chunk.
* No unsupported facts are allowed.
* Parent chunk metadata is preserved.

Example:

```text
What risks could affect Tesla's production scaling plans?

How might supply chain disruptions impact vehicle deliveries?

What operational factors could prevent Tesla from meeting growth expectations?
```

Generated questions are saved in:

```text
tesla_hypothetical_questions.json
```

---

### Step 5 – Build Hypothetical Question Index

Create a second Chroma collection.

```python
hq_vectorstore
```

Each question stores:

```json
{
  "parent_chunk_id": "...",
  "source_doc": "...",
  "year": 2022,
  "section": "Risk Factors"
}
```

---

### Step 6 – Run Benchmark Questions

Assignment benchmark questions:

* HQ1
* HQ2
* HQ3
* HQ4

Process:

```text
User Query
    ↓
HQ Index Retrieval
    ↓
Retrieve Matching Questions
    ↓
Map to Parent Chunks
    ↓
Generate Final Answer
```

Answers are generated using parent chunks only.

---

### Step 7 – Generate Required Outputs

Outputs produced:

```text
HQ1.json
HQ2.json
HQ3.json
HQ4.json
```

Each file follows:

```json
{
  "question_id": "",
  "user_query": "",
  "retrieved_hypothetical_questions": [],
  "parent_chunks_used": [],
  "final_answer": "",
  "citations": [],
  "comparison_with_baseline": ""
}
```

---

### Step 8 – Baseline vs Improved Retrieval Comparison

Compare:

1. Baseline chunk retrieval
2. Hypothetical question retrieval

Metrics evaluated:

* Evidence quality
* Retrieval relevance
* Coverage
* Precision
* Failure modes

Outputs:

```text
comparison_table.csv
comparison_table.xlsx
```

---

## Analytical Evaluation

The project answers:

1. Which queries benefited most from hypothetical question retrieval?
2. Which generated questions were too broad or misleading?
3. How unsupported facts were prevented?
4. Whether retrieval improved for abstract business questions?
5. How to update the HQ index when new filings are added?

Results are saved in:

```text
analysis_answers.json
```

---

## Rebuilding the Index

Delete existing database:

```text
tesla_db/
```

Then rerun:

1. Corpus ingestion
2. Chunk generation
3. Baseline indexing
4. HQ generation
5. HQ indexing

---

## Production Considerations

Potential improvements:

* Hybrid BM25 + Vector Retrieval
* Parent-Child Retrieval
* Cross-Encoder Re-ranking
* Incremental HQ Index Updates
* Metadata-Based Filtering
* Section Classification

---

## Submission Deliverables

This repository includes:

* Complete notebook implementation
* Prompt templates
* Baseline RAG pipeline
* Hypothetical Question Retrieval pipeline
* Benchmark outputs
* Comparison analysis
* Final written evaluation

No API keys are committed to the repository.
