# Production-Grade Marketplace RAG Support Agent
**System Identifier:** `rag-ecommerce-support-chatbot`

# Participant Name
Nandani Bisht

## 1. Project Overview & Business Objective
Modern e-commerce marketplaces require highly available, accurate, and secure automated
support for their seller ecosystems. The goal of this project is to build an enterprise-grade,
production-ready Retrieval-Augmented Generation (RAG) chatbot for ShopSphere
Marketplace, a platform hosting thousands of independent business sellers.
The chatbot must accurately ingest complex corporate guidelines—specifically focusing on
advanced business operations, fulfillment strategies, seller ratings, and profitability matrices. It
must answer seller queries instantly while maintaining absolute deterministic safety standards,
ensuring no toxic, profane, or hallucinated outputs are surfaced to end-users.

## 2. Directory Structure
All project files follow the required directory standards:
```
rag-ecommerce-support-chatbot/
├── data/                       
├── chroma_db/                  
├── src/                        
│   ├── agent.py               
│   ├── guardrails_config.py    
│   └── database.py             
├── tests/                      
│   └── test_rag_metrics.py     
├── README.md                   
└── requirements.txt            
```

---

## 3. Technology Stack & Key Constraints
- **Orchestration Framework:** Pydantic AI (strongly typed agent states and dependencies).
- **Vector Database:** Chroma DB (local persistent storage under `./chroma_db` using cosine distance).
- **Embeddings:** Local Sentence-Transformers (`all-mpnet-base-v2`).
- **Security & Safety Layer:** Guardrails AI (wrapped input/output checking with Profanity and Toxicity validators).
- **Evaluation Framework:** DeepEval.
- **LLM Provider:** Groq (`llama-3.3-70b-versatile`).

---

## 4. Setup & Installation

### Prerequisites
- Python 3.11 
- `uv` package manager installed

### Environment Configuration
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your-groq-api-key
```

### Installation Steps
1. **Initialize and Activate Virtual Environment:**
   ```powershell
   uv venv
   .venv\Scripts\activate
   ```
2. **Install Hardened Dependencies:**
   ```powershell
   uv pip install -r requirements.txt
   ```
3. **Verify Raw PDF Placement:**
   Ensure the PDF is placed inside `data/` as `Advanced_Business_Seller_Guide_May09.pdf`. The application will automatically copy/rename it to `seller_guide.pdf`.

---

## 5. Execution Instructions

### A. Run Database Ingestion
```powershell
python src/database.py
```

### B. Run Chatbot Interface
```powershell
python src/agent.py
```

### C. Run Programmatic Evaluations
```powershell
pytest tests/test_rag_metrics.py -s
```

