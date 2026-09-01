# Advanced RAG Retrieval Evaluation – Assignment 3: Hypothetical question Retrieval

## 1. Name

Taniya Gupta

---

## 2. Assignment Title

**Advanced RAG Retrieval – Hypothetical Question Retrieval**

---

## 3. Project Description

This project implements a Retrieval-Augmented Generation - RAG system and evaluates the effectiveness of **Hypothetical Question (HQ) Retrieval** as a retrieval enhancement technique.

A baseline vector index was created using document chunks extracted. For each chunk, three hypothetical questions were generated using an LLM and stored in a separate vector index. During retrieval, user queries are matched against the hypothetical question index, and the corresponding parent chunks are used to generate answers.

The project compares baseline retrieval with HQ Retrieval across multiple benchmark questions.

---

## 4. Steps to Run the Code

1. Clone or download the project files.
2. Create and activate a Python virtual environment.
3. Install all required dependencies.
4. Set the required API credentials and model configuration.
5. Place files inside the `tesla-annual-reports` folder.
6. Open the Jupyter Notebook.
7. Run the notebook cells in order:

   * Load Tesla 10-K documents
   * Chunk documents and add metadata
   * Create baseline vector store
   * Generate hypothetical questions
   * Create HQ vector store
   * Run benchmark queries
   * Compare baseline and HQ retrieval results
8. Review the generated outputs and comparative analysis.

---

## 5. Libraries and Packages Required

* Python 3.11+
* langchain
* langchain-community
* langchain-chroma
* chromadb
* sentence-transformers
* tqdm
* pypdf
* tiktoken
* openai (for NVIDIA NIM API)
* json
* os
* re
* time


---

## 6. Assumptions Made

* NVIDIA NIM was used as the LLM endpoint for hypothetical question generation and answer synthesis.
* Three hypothetical questions were generated for each chunk.
* Final answers are generated using the original parent document chunks.
* A cache file (`hq_cache.json`) is used to avoid regenerating hypothetical questions after interruptions.

---

## Repository structure

```text
assignment/assignment-03/taniya-gupta
│
├── Assignment_3_solution.ipynb
├── README.md
├── requirements.txt
├── tesla_db/
├── hq_cache.json
├── assignment3_result.json
└── .env.example
```

---

## Analytical Questions

**Which queries benefited most from hypothetical question retrieval?**  
HQ1 and HQ4 showed the biggest improvement.

**Which generated questions were too broad, too narrow, or misleading?**  
Some questions were too broad, while a few were too narrow. No major misleading questions were observed.

**How did you prevent generated hypothetical questions from introducing unsupported facts?**  
Questions were generated only from the chunk content, and final answers were produced using the original document chunks.

**Did the technique improve retrieval for abstract business questions?**  
Yes. Hypothetical question retrieval improved retrieval quality.

**How would you update the hypothetical question index when new 10-K filings are added?**  
New filings would be chunked, hypothetical questions would be generated for the new chunks, and the resulting embeddings would be added to the existing HQ vector index.

---

## 7. Output Explanation

The notebook produces:

1. **Baseline Retrieval Results**

   * Standard semantic similarity retrieval over Tesla 10-K chunks.

2. **Hypothetical Question Retrieval Results**

   * Retrieval using generated hypothetical questions linked to parent chunks.

3. **Answer Generation**

   * Grounded answers generated from retrieved parent chunks.

4. **Comparative Analysis**

   * Quality comparison between baseline and HQ retrieval.

Expected outcome: HQ Retrieval should improve retrieval quality.
