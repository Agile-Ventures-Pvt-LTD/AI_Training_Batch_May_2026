# Project 1: RAG E-commerce Support Chatbot

This project demonstrates a complete Retrieval-Augmented Generation (RAG) system built using **Pydantic AI**, **Groq**, and **guardrails** for pdf search. It implements input guardrails (safety and scope analysis) and output guardrails (groundedness / hallucination audit with self-correction retry loop).

---

## 🏗️ Project Flow Architecture

```
[User Query]
     │
     ▼
[Input Guardrails] (Checks for Injection, Toxicity, Scope) ──(Fail)──> [Blocked Response]
     │
     ├─(Pass)
     ▼
[Retrieve Context] (chroma db & BM25-like search on Advanced_Business_Seller_Guide_May09.pdf.txt)
     │
     ▼
[Pydantic AI Agent] (Generates Answer using injected retrieved context dependency)
     │
     ▼
[Output Guardrails] (Audits generated response against source context)
     │
     ├─── (Fails groundedness check: feedback sent to self-correction loop) ──> (Max Retries: 2)
     │
     └─── (Passes check) ──> [Final Grounded Answer]
```

---




## 🏗️ Folder Structure

rag-ecommerce-support-chatbot/
├── data/                                     # Must contain the downloaded seller_guide.pdf
├── chroma_db/                                # Local persistent Chroma database store
├── src/                                      # Core application source code
│ ├── agent.py
│ ├── guardrails_config.py
│ └── database.py
├── tests/                                    # DeepEval testing suites
│ └── test_rag_metrics.py
├── README.md                                 # Setup, architecture, and run instructions
└── requirements.txt                          # Hardened dependency definitions





## 🛠️ Key Implementation Files

1. **`database.py`**: Chroma Db (Full pdf Search) store. Handles pdf file loading, paragraph-based chunking, indexing, and relevance-ranked search.
2. **`input_guardrails.py`**: Defines a structured Pydantic model (`InputGuardrailResult`) and queries a specialized Pydantic AI agent to classify the user query's safety and scope.
3. **`output_guardrails.py`**: Defines a structured Pydantic model (`OutputGuardrailResult`) that checks the generated answer against the source context to ensure absolute factual groundedness (zero hallucination) and flags sensitive leakage.
4. **`agent.py`**: Injects context into the agent using Pydantic AI's dependency injection (`RunContext` and `deps_type`), orchestrates the execution, and performs a self-correction retry loop if output validation fails.

---

## 🚀 Running the Project

### Prerequisites
- Python 3.10+
- Groq API Key

### Setup
1. Navigate to the project directory:
   ```bash
   cd "C:\Users\Poonam Bhatt\Desktop\pydantic ai\project_1_rag_system"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API key in the `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

### Execution

- For running the test case which include deepeval test and database chunk testing 
         DeepEval
         |---AnswerRelevancyMetric
         |---ContextualPrecisionMetric

```bash
pytest tests/     # Run All the test cases at once

- Run the RAG pipeline demonstrating standard, out-of-scope, injection-attempt, and ignorance-fallback test cases:
```bash
python -m src.agent     # this will run agent.py diectly from root.


# Note- Created __init__.py file in src and test folder to make sure the path will be cleared while running particular file .

Name - Poonam Bhatt
Project - P006 (RAG ECOMMERCE SUPPORT CHATBOT)


```
