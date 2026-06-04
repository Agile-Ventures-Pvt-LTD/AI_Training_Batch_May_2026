# Assignment 03 - Hypothetical Question Generation for Retrieval-Augmented Generation (RAG)

## Participant Name

**Vaibhav Kesarwani**

## Project Title

**Hypothetical Question Generation and Retrieval using ChromaDB, LangChain, and NVIDIA LLM**

---

## Description

This project implements a **Hypothetical Questions retrieval pipeline** using Tesla 10-K annual report data stored in a ChromaDB vector database.

The workflow consists of:

1. Loading Tesla 10-K document chunks from a persistent ChromaDB collection.
2. Generating three hypothetical questions for each document chunk using the Groq LLM.
3. Storing the generated hypothetical questions in a separate vector database.
4. Retrieving the most relevant hypothetical questions for a user query.
5. Mapping the retrieved questions back to their original document chunks.
6. Using the retrieved context to generate a final answer to the user's query.

This approach improves retrieval quality by searching against generated questions rather than directly searching document embeddings.

---

## Technologies Used

* Python
* ChromaDB
* LangChain
* NVIDIA LLM API
* HuggingFace Sentence Transformers
* dotenv
* tqdm

---

## Libraries / Packages Required

All required dependencies are listed in `requirements.txt`.

Install them using **uv**:

```bash
uv add -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
NVIDIA_API_KEY="..."
```

---

## How to Run

### 1. Create a virtual environment

```bash
uv venv
```

### 2. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv add -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add your Groq API key:

```env
NVIDIA_API_KEY="..."
```

### 5. Open and run

```text
main.ipynb
```

Execute all notebook cells sequentially.

---

## Workflow

### Step 1: Load Existing Tesla 10-K Vector Database

The application connects to a persistent ChromaDB collection containing Tesla annual report chunks.

### Step 2: Generate Hypothetical Questions

For each document chunk, the NVIDIA LLM generates exactly three hypothetical questions that could be answered using that chunk.

### Step 3: Create Question Vector Store

Generated questions are embedded and stored in a separate ChromaDB collection.

### Step 4: Retrieve Relevant Questions

User queries are matched against the hypothetical-question collection.

### Step 5: Fetch Original Documents

The retrieved questions are mapped back to their source document chunks.

### Step 6: Generate Final Answer

Relevant document chunks are provided to the LLM to generate an answer grounded in the retrieved context.

---

## Example Query

```text
What is the fiscal year end date for the annual report of Tesla, Inc. as presented in the document?
```

---

## Example Output

```text
The fiscal year ends on **December 31, 2021**.
```

(The actual output depends on the retrieved document context.)

---

## Assumptions Made

1. A populated ChromaDB collection named:

```text
tesla-10k-2019-to-2023
```

already exists inside the `tesla_db` directory.

2. The NVIDIA API key is valid and has sufficient quota.

3. Internet connectivity is available for:

   * NVIDIA API calls
   * Downloading the embedding model (first run)

4. The embedding model used is:

```text
sentence-transformers/all-mpnet-base-v2
```

5. Each document chunk generates exactly three hypothetical questions.

---

## Model Configuration

### Embedding Model

```text
sentence-transformers/all-mpnet-base-v2
```

### LLM

```text
meta/llama-3.1-8b-instruct
```

### Retrieval Settings

```python
k = 5
```

for hypothetical-question retrieval.

---

## Output Explanation

The system retrieves the most relevant hypothetical questions, maps them back to their parent Tesla 10-K document chunks, and uses those chunks as context for generating a final answer.

This retrieval strategy can improve semantic search performance by capturing potential user intents through generated questions.

![Hypothetical Question](./assets/hypothetical-questions.png)

## Analytical Questions

### Q1. Which queries benefited most from hypothetical question retrieval?

HQ1, HQ2, and HQ4 benefited the most because they are abstract and indirectly phrased, requiring semantic interpretation beyond keyword matching.

- HQ4 benefited the most since cybersecurity/AI risks are often described implicitly in filings.
- HQ1 and HQ2 improved due to better mapping of risk and relationship-based reasoning.
- HQ3 benefited least because cash flow concepts are already explicitly stated in the 10-K.

### Q2. Which generated questions were too broad, too narrow, or misleading?

- **Too broad:** Questions combining multiple risk or financial dimensions in a single query, reducing retrieval precision.
- **Too narrow:** Questions focused on very specific metrics or single-year details, limiting relevant context retrieval.
- **Misleading:** A few questions implied relationships or causal links not explicitly supported in the source chunks.

### Q3. How did you prevent generated hypothetical questions from introducing unsupported facts?

- Used strict chunk-only input context (no external knowledge).
- Controlled generation via low temperature (0.2) for stability.
- Forced the model to generate questions only, not answers or explanations.
- Stored parent chunk IDs to ensure traceability back to source text.
- Final answers were generated only from retrieved original chunks, not hypothetical questions.

### Q4. Did the technique improve retrieval for abstract business questions?

Yes. The technique significantly improved retrieval for abstract and multi-hop business questions by bridging the gap between:

- natural user language, and
- formal financial disclosure language in 10-K filings.

It improved recall especially for:

- risk interpretation (HQ1, HQ4)
- relationship-based analysis (HQ2)
- implicit operational risk queries

### Q5. How would you update the hypothetical question index when new 10-K filings are added?

- Ingest new filings into the chunk database with metadata (year, section, source).
- Generate hypothetical questions only for new chunks (incremental update).
- Embed and append them to the existing hypothetical question vector store.
- Periodically clean duplicates and low-quality questions.
- Optionally version the index (e.g., v1, v2) to track filing updates over time.


## Required Comparative Analysis

| Question | Baseline Evidence Quality | Improved Evidence Quality | Improvement Observed | Failure Mode |
| -------- | -------- | -------- | -------- | -------- |
| HQ1 | Medium | High | Retrieval became more aligned with risk-related disclosures; better coverage of production, scaling, and operational constraints. | Slight noise from broadly framed risk questions introducing adjacent but non-critical sections. |
| HQ2 | Low–Medium | High | Strong improvement in connecting product defects → warranty obligations → customer trust; better multi-hop evidence chaining. | Some retrieved chunks were loosely related service/warranty text without direct defect linkage. |
| HQ3 | Medium | Medium–High | Moderate improvement in identifying cash flow drivers across sections (capex, operating income, working capital). | Retrieval still somewhat broad, mixing unrelated financial commentary sections. |
| HQ4 | Low | High | Largest improvement; successfully surfaced implicit cybersecurity/AI/data risk disclosures not keyword-matched in baseline. | Precision loss: some general “technology risk” chunks included without explicit cybersecurity relevance. |
