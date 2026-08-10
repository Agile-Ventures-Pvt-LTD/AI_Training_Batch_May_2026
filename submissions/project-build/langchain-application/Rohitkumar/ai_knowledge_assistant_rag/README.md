# AI Knowledge Assistant for Enterprise Document Question Answering

AI Knowledge Assistant Using RAG, Groq, Python, and LangChain. user can ask query related to document and  it gives answer from the context

## How it works


PDF Documents > Chunks > Embeddings > Vector Store
                                          |
User Question > Retrieve chunks > LLM > Answer > Sources


## Setup


python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


Create `.env` file:

GROQ_API_KEY =  gsk_your_key_here


Place PDF files in `data/raw/`.

## Run

Notebook: Open and run `rag_pipeline.ipynb`



## Output

output is saved in output folder in json format and benchmark  also

## Run tests


python -m pytest tests/test_retrieval.py -v


## Project folder structure 
Suggested Folder Structure
ai_knowledge_assistant_rag/
│
├── app.py
├── config.py
├── loaders.py
├── chunking.py
├── embeddings.py
├── vector_store.py
├── retriever.py
├── prompts.py
├── chains.py
├── output_parser.py
├── logger.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ ├── raw/
│ ├── processed/
│ └── vector_store/
│
├── logs/
│ └── query_logs.jsonl
│
├── outputs/
│ └── benchmark_results.json
│
└── tests/
 └── test_retrieval.py


 `rag_pipeline.ipynb` | Jupyter notebook walkthrough