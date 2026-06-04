# 🚀 Assignment 3 - Advanced RAG: Hypothetical Question Generation for Enhanced Retrieval (TESLA Reports)

## 👨‍💻 Participant Name

**Pranay Gupta**

---

## 📌 Assignment / Project Title

**Advanced Retrieval-Augmented Generation (RAG) Using Hypothetical Question Expansion for Tesla Annual Reports (2019–2023)**

---

## 🧠 Description

This project implements an **Advanced RAG technique called Hypothetical Question Generation (HyDE-style retrieval enhancement)** to improve document retrieval accuracy over Tesla 10-K annual reports.

Instead of directly matching user queries with document chunks, the system:

* Generates **3 hypothetical questions per document chunk**
* Indexes these questions into a **separate vector database**
* Links each question to its **original parent document chunk**
* Uses these hypothetical questions as an **intermediate retrieval layer**

At query time:

1. The user query is compared against hypothetical questions
2. Relevant questions are retrieved
3. Associated document chunks are fetched
4. Final context is passed to the LLM (LLaMA 3 via NVIDIA API) for answer generation

This significantly improves **semantic coverage, recall, and retrieval robustness**.

---

## 🎯 Key Features

* Advanced RAG pipeline using **Hypothetical Question Expansion**
* Tesla 10-K (2019–2023) financial document analysis
* Two-stage retrieval system (Question → Document chunk)
* Embedding-based semantic search using **ChromaDB**
* LLM-powered generation using **LLaMA 3 (NVIDIA API)**
* Improved handling of ambiguous financial queries

---

## ⚙️ Prerequisites

Before running the project, ensure:

* Python 3.10+
* NVIDIA API Key
* ChromaDB installed and configured
* Tesla 10-K dataset indexed
* Internet connection for model inference

---

## 📁 Project Structure

```text
Advanced_RAG_Hypothetical/
│
├── RAG_TESLAReports_Hypothetical.ipynb
├── tesla_db/
│   └── Persisted Chroma Vector Store
│
├── .env
├── requirements.txt
└── README.md
```

---

## 📦 Required Libraries

```bash
chromadb
langchain
langchain-chroma
langchain-community
langchain-core
sentence-transformers
huggingface-hub
openai
python-dotenv
tqdm
numpy
```

---

## 🔧 Installation

Install dependencies using:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install chromadb
pip install langchain
pip install langchain-chroma
pip install langchain-community
pip install sentence-transformers
pip install openai
pip install python-dotenv
pip install tqdm
pip install numpy
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
NVIDIA_API_KEY=your_api_key_here
```

Load environment variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## ▶️ How to Run

### Step 1: Launch Jupyter Notebook

```bash
jupyter notebook
```

### Step 2: Open File

```text
RAG_TESLAReports_Hypothetical(4).ipynb
```

### Step 3: Execute Cells Sequentially

The notebook performs the following steps:

1. Load embeddings (Sentence Transformers)
2. Load Tesla 10-K documents
3. Split documents into chunks
4. Generate **3 hypothetical questions per chunk**
5. Store questions in a separate ChromaDB collection
6. Link questions with parent document chunks
7. Perform query-time retrieval using hypothetical questions
8. Retrieve original supporting chunks
9. Generate final answer using LLaMA 3 (NVIDIA API)

---

## 🔄 System Architecture

```text
User Query
     │
     ▼
Compare with Hypothetical Questions
     │
     ▼
Retrieve Matching Questions (Vector DB)
     │
     ▼
Fetch Parent Document Chunks
     │
     ▼
Build Context Window
     │
     ▼
LLM (LLaMA 3 via NVIDIA API)
     │
     ▼
Final Answer
```

---

## 📌 Example

### User Query

```text
What was Tesla's automotive revenue in 2021?
```

### System Behavior

* Query is matched against generated hypothetical questions
* Relevant questions like:

  * “What is Tesla’s revenue breakdown for 2021?”
  * “How did Tesla perform financially in automotive segment in 2021?”
* Corresponding document chunks are retrieved
* Final answer is generated using grounded context

---

## 💡 Advantages of Hypothetical Question RAG

✅ Improves semantic retrieval accuracy
✅ Bridges vocabulary gap between query and documents
✅ Better recall than naive similarity search
✅ Strong performance on financial documents
✅ Reduces missed-context retrieval failures
✅ More robust than standard embedding-only RAG

---

## ⚠️ Assumptions

* Tesla 10-K documents are preloaded into ChromaDB
* Hypothetical questions are generated using an LLM
* NVIDIA API key is valid and active
* Embedding model (`all-mpnet-base-v2`) is available
* Each document chunk can generate meaningful synthetic questions
* Vector database is properly persisted before querying

---

## 📊 Output

The system generates:

* Hypothetical questions per document chunk
* Indexed question-chunk mappings
* Retrieved question matches for user query
* Retrieved document context
* Final LLM-generated answer

---

## 🎓 Learning Outcomes

After completing this assignment, you will understand:

* Advanced RAG architectures beyond basic retrieval
* Hypothetical Question Generation (HyDE-style technique)
* Two-stage retrieval pipelines
* Vector database design for improved recall
* How to reduce semantic mismatch in RAG systems
* Real-world financial document QA systems
* Integration of NVIDIA LLM APIs with LangChain

---

## 🔍 Key Concepts

* Advanced RAG
* Hypothetical Question Generation
* Semantic Search
* Vector Databases (ChromaDB)
* Document Chunking
* Retrieval-Augmented Generation
* LLaMA 3 via NVIDIA API
* Financial NLP Systems

---

## 📈 Observations

This approach significantly improves retrieval quality by introducing an intermediate semantic layer (hypothetical questions).

Instead of directly matching queries to raw document chunks, the system:

* Expands semantic space
* Improves retrieval recall
* Handles ambiguity better
* Enhances downstream answer quality

This demonstrates how **Advanced RAG techniques outperform traditional embedding-based retrieval systems**.

---

## 👨‍💻 Author

**Pranay Gupta**

Assignment 3: **Advanced RAG – Hypothetical Question Generation**

Built using **ChromaDB, LangChain, Sentence Transformers, and NVIDIA LLaMA 3 API** 🚀
