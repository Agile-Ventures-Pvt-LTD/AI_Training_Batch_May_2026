## Grade Marketplace RAG Support Agent

An enterprise -grade, production-ready RAG chatbot for ShopeSphere Marketplace- a platform hosting thousands of independent bussiness sellers.

## SetUP
 
1. Create a virtual environment:
activate 
```
.venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:
```
 .env.example  or .env
```

5.  `.env` with your API keys:
```
GROQ_API_KEY= your_groq_API_key
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB=chroma
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
TOP_K=5

```
6. download the dataset from the given link and add to the folder :
```
[https://ir.ebaystatic.com/pictures/aw/pics/business/pdf/Advanced_Business_Se ler_Guide_May
09.pdf](https://ir.ebaystatic.com/pictures/aw/pics/business/pdf/Advanced_Business_Se ler_Guid
e_May09.pdf) 

```
dataset folder
```
 rag-ecommerce-support-chatbot/ 
                ├── data/ Advanced_Business_Se ler_Guid
e_May09.pdf  
```

## Architecture

 ```
user query
   |
Input_validator for profanity/toxic language(guardrails)
   |
   |
RAg Agent(LLM) ____ (pydantic AI )
    |   
    |____ Vector_DB ( chromaDB)
    |
raw_ouput
    |
    |
Output validator for profanity/toxic language ( guardrails AI )
    |
    |
final_filttered_output
``` 
 pip install -r requirements

## How to run 

Run the agent
```bash
 python src.agent.py
```
Run the tests
```bash
python tests/
```
## Folder Structure 

```
rag-ecommerce-support-chatbot/ 
                ├── data/                  #  contain the downloaded seller_guide.pdf 
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

## Future scope:
1. interated with web UI interface
2. conversation memory
3. Multi language support 
