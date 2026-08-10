# RAG with Hypothetical Questions Assignment

## 1. Name

**Aditya Sodani**

---

## 2. Assignment Title

**Retrieval-Augmented Generation (RAG) using Hypothetical Questions**

---

## 3. Short Description

This project implements a Retrieval-Augmented Generation (RAG) pipeline on Tesla Annual Reports using a Hypothetical Questions retrieval strategy.

The system:

* Loads Tesla annual report PDFs.
* Splits documents into manageable chunks.
* Creates embeddings using Sentence Transformers.
* Stores embeddings in ChromaDB.
* Uses an LLM to generate hypothetical questions from document content.
* Stores generated questions along with document context.
* Retrieves relevant content using similarity search.
* Generates context-aware answers using an LLM.

The objective is to improve retrieval performance by indexing document chunks with generated hypothetical questions, making it easier to match user queries with relevant information.

---

## 4. Steps to Run the Code

### Step 1: Create Virtual Environment

```bash
uv venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

---

### Step 2: Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

### Step 3: Configure Environment Variables

Create a `.env` file:

```env
NVIDIA_API_KEY=your_nvidia_api_key
```

---

### Step 4: Prepare Dataset

Place the Tesla Annual Report PDF files inside the project directory.

Example:

```text
tesla-annual-reports/
├── 2021.pdf
├── 2022.pdf
├── 2023.pdf
```

---

### Step 5: Launch Jupyter Notebook

```bash
jupyter notebook
```

Open:

```text
RAG_hypothetical_questions.ipynb
```

---

### Step 6: Execute Notebook Cells Sequentially

Run all cells in order:

1. Environment Setup
2. LLM Initialization
3. Embedding Model Setup
4. PDF Loading
5. Document Chunking
6. Vector Database Creation
7. Hypothetical Question Generation
8. ChromaDB Storage
9. Retrieval
10. Answer Generation
11. JSON Export

---

## 5. Libraries / Packages Required

```text
groq
openai
python-dotenv
langchain
langchain-community
langchain-chroma
chromadb
sentence-transformers
datasets
tiktoken
pypdf
ipykernel
```

Install all dependencies using:

```bash
uv pip install -r requirements.txt
```

---

## 6. Assumptions Made

* Tesla annual report PDFs are available locally.
* A valid NVIDIA API key is available.
* Documents contain machine-readable text.
* Internet connectivity is available for API access.
* ChromaDB is used as the vector database.
* Generated hypothetical questions improve retrieval quality by creating additional semantic search signals.

---

## 7. Output Explanation

### Example User Query

```text
What risks did Tesla identify in its annual report?
```

### System Workflow

1. Tesla reports are loaded and chunked.
2. The LLM generates hypothetical questions for each chunk.
3. Questions and chunk content are stored in ChromaDB.
4. User query is matched against the indexed questions and content.
5. Relevant chunks are retrieved.
6. Retrieved context is passed to the LLM.
7. A grounded answer is generated.

### Example Output

```text
Tesla identified several risks including supply chain disruptions,
battery material shortages, increasing competition in the electric
vehicle market, regulatory changes, and manufacturing scalability
challenges.
```

---

## Project Outcome

This assignment demonstrates:

* Retrieval-Augmented Generation (RAG)
* PDF Document Processing
* Text Chunking
* Vector Databases (ChromaDB)
* Embedding Models
* Semantic Search
* Hypothetical Question Generation
* Context Retrieval
* LLM-Based Question Answering
* JSON Data Export

---

##
