# Assignment 03 - Hypothetical Question Based RAG

## Participant Name

**Mohd Zaid Ansari**

## Description

This assignment implements a Retrieval-Augmented Generation (RAG) pipeline using Tesla Annual Reports (10-K filings).

The workflow consists of:

1. Loading multiple Tesla annual report PDFs.
2. Splitting documents into chunks using RecursiveCharacterTextSplitter.
3. Generating three hypothetical questions for each document chunk using NVIDIA's Llama model.
4. Creating a separate vector database containing the generated hypothetical questions.
5. Storing metadata that maps each question back to its original document chunk.
6. Retrieving relevant hypothetical questions for a user query.
7. Using the parent chunk IDs to fetch the original document chunks.
8. Providing contextual information to an LLM for answering user queries.

This approach improves retrieval quality by matching user queries against generated questions instead of directly searching document chunks.

---

## Dataset

Tesla Annual Reports (10-K Filings)

Files used:

* tsla-10ka_20211231-gen.pdf
* Additional Tesla annual report PDFs provided in the assignment folder

---

## Technologies Used

* Python
* LangChain
* ChromaDB
* NVIDIA NIM API
* HuggingFace Embeddings
* RecursiveCharacterTextSplitter

---

## Libraries Required

```bash
pip install langchain
pip install langchain-community
pip install langchain-chroma
pip install chromadb
pip install sentence-transformers
pip install pypdf
pip install openai
pip install tqdm
```

---

## Model Used

### Embedding Model

```python
sentence-transformers/all-mpnet-base-v2
```

### LLM

```python
meta/llama-3.3-70b-instruct
```

via NVIDIA NIM API.

---

## How to Run

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set NVIDIA API Key

```bash
export NVIDIA_API=your_api_key
```

or on Windows:

```cmd
set NVIDIA_API=your_api_key
```

### Step 3: Run Notebook

Execute all notebook cells in order:

1. Load PDFs
2. Chunk Documents
3. Generate Hypothetical Questions
4. Create Question Vector Store
5. Create Document Vector Store
6. Run Retrieval Pipeline
7. Generate Final Answer

---

## Assumptions

* Each document chunk generates exactly three hypothetical questions.
* Questions are stored separately from document chunks.
* Metadata contains parent chunk information for mapping questions back to original chunks.
* NVIDIA NIM API is available and properly configured.
* Tesla annual reports are available in the specified directory.

---

## Output

### Document Processing

```text
Total Chunks: 3337
```

### Hypothetical Question Generation

```text
Total Questions Generated: 10011
```

### Retrieval Flow

```text
User Query
    ↓
Question Vector Store
    ↓
Top Matching Questions
    ↓
Parent Chunk IDs
    ↓
Original Document Chunks
    ↓
Context Generation
    ↓
LLM Answer
```

### Sample Generated Questions

```text
What is the purpose of the Form 10-K/A filing?

How does Tesla determine its filing status as a well-known seasoned issuer?

What are the implications of Tesla's registration of its common stock under Section 12(b) of the Securities Exchange Act of 1934?
```

---

## Project Structure

```text
project/
│
├── tesla-annual-reports/
│   ├── *.pdf
│
├── notebooks/
│   └── Assignment.ipynb
│
├── chroma_db/
│
├── requirements.txt
│
└── README.md
```
