# Project Build 1: AI Knowledge Assistant (RAG)

**Participant:** Mohammad Anas

This is my submission for the Enterprise AI Knowledge Assistant. It uses LangChain, Groq (Llama-3), ChromaDB, and a local Retrieval-Augmented Generation (RAG) pipeline to answer questions based on the provided Amazon 2025 Annual Report.

## How to run the project
1. Create a virtual environment using uv: `uv venv`
2. Install the required packages: `uv pip install -r requirements.txt`
3. Rename `.env.example` to `.env` and paste your `GROQ_API_KEY`.
4. Make sure your document PDFs (like the Amazon Report) are inside the `data/raw/` folder.
5. Run the main file: `python app.py`

## Usage
When you start the application, you will be given two options:
* **Option 1:** Ask a question. The assistant will classify the query, search the Chroma vector database, generate a grounded answer, and display the source citations (along with a debug view of the chunks).
* **Option 2:** Run benchmarks. This automatically runs the 8 mandatory benchmark questions and saves the results as a JSON file inside the `outputs/` folder.

All questions asked during the session are automatically saved inside the `logs/query_logs.jsonl` file for auditing.

## Development Notes & Approach
Instead of putting all the code in one massive file, I built a modular architecture (`loaders.py`, `chunking.py`, `vector_store.py`, `chains.py`) so it's easier to maintain. For chunking the PDFs, I used `RecursiveCharacterTextSplitter` with a chunk size of 1000 and an overlap of 150 to ensure context wasn't lost between pages.

**A challenge I faced:** While testing the generation step, the application would occasionally crash with a `JSONDecodeError`. I realized this was happening because the Groq LLM would sometimes wrap its structured output in markdown formatting (e.g., writing ` ```json ` at the start of the string), which broke python's `json.loads()`. 

To fix this, I wrote a custom `_clean_json()` helper function inside `chains.py` that automatically detects and strips out markdown code fences before attempting to parse the JSON. This made the RAG pipeline significantly more stable during the benchmark runs.