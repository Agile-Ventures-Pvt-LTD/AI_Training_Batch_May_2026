
# Grade Marketplace RAG Support Agent 

In this project, we need to ingest the pdf and create the chunks. Then we need to store in persistent chroma db while embedding. The user will ask question and the query should pass through the guardrails as input and then later the pydantic ai agent will revert to the user's query and the output is also passed through the output guardrails.

# Business Objective & Background 
Modern e-commerce marketplaces require highly available, accurate, and secure automated 
support for their se ler ecosystems. The goal of this project is to build an enterprise-grade, 
production-ready Retrieval-Augmented Generation (RAG) chatbot for ShopSphere 
Marketplace, a platform hosting thousands of independent business selers. 
The chatbot must accurately ingest complex corporate guidelines—specificaly focusing on 
advanced business operations, fulfi lment strategies, se ler ratings, and profitability matrices. It 
must answer seler queries instantly while maintaining absolute deterministic safety standards, 
ensuring no toxic, profane, or ha lucinated outputs are surfaced to end-users. 

# Tech Stack
- Orchestration Framework: Pydantic AI
- Vector Database: Chroma DB
- Security & Safety Layer: Guardrails AI
- Evaluation Framework: DeepEval

# Environment Variables

```bash
GROQ_API_KEY=

GROQ_MODEL=llama-3.3-70b-versatile

HF_TOKEN=
```

# Directory Standard
```bash
submissions/ 
└── project-build/ 
    └── pydantic-ai-application/ 
        └── firstname-lastname/ 
            └── rag-ecommerce-support-chatbot/ 
                ├── data/                  # Must contain the downloaded seller_guide.pdf 
                ├── chroma_db/             # Local persistent Chroma database store 
                ├── src/                   # Core application source code 
                │   ├── agent.py 
                │   ├── guardrails_config.py 
                │   └── database.py 
                ├── tests/                 # DeepEval testing suites 
                │   └── test_rag_metrics.py 
                ├── README.md              # Setup, architecture, and run instructions 
                └── requirements.txt       # Hardened dependency definitions 

```

# Setup

```python
uv venv

.venv\Scripts\activate

uv pip install -r requirements.txt
```

# Running the files

```python
python src/agent.py
```

# Testing

You can use below code for testing

```python
pytest tests/test_rag_metrics.py
```

# Future Improvement

We need to add much more guardrails to prevent from prompt injection and can use better chunking if the recall is not given as per the standards.

# Author

Vikash Kumar

