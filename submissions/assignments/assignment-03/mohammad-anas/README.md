# Assignment 03 - Advanced Hypothetical Question RAG Engine

## Participant Name
Mohammad Anas

## Project Description
This assignment implements a production-grade **Hypothetical Questions** RAG pipeline over complex SEC 10-K financial reports (Tesla). 

Standard keyword-based retrieval often fails when users ask abstract, business-oriented questions (e.g., "What should a board member ask..."). To bridge this vocabulary gap, this system uses the Groq API to translate legal compliance records into a searchable multi-tier index of predictive, executive-level questions. Crucially, it maps retrieved hypothetical questions back to their verified parent text blocks to ensure final answers are strictly grounded in factual data, completely eliminating hallucination risks.

## Key Enterprise Features Implemented
- **True Parent-Chunk Mapping:** The system retrieves based on hypothetical questions but synthesizes the final answer using ONLY the original parent document text.
- **Multi-Model Fault Isolation:** Built-in automatic API traffic redirection from `openai/gpt-oss-120b` to a fallback cluster (`llama-3.3-70b-versatile`) during backend connection failures or severe server overload.
- **Rate Limit Resilience:** Programmed with an Exponential Backoff retry engine to safely absorb heavy API pressure loops while parsing the complete PDF document.
- **Clean Architectural Segregation:** Prompt engineering logic is fully decoupled into a dedicated `prompts.py` file to ensure code maintainability.
- **Persistent Local Database:** Uses ChromaDB's persistent client and batch indexing to prevent memory overflow and avoid re-indexing the entire corpus on every run.

## Setup & Local Execution

1. **Build local container/environment:**
   ```bash
   python -m venv .venv
   On Windows: .venv\Scripts\activate
   ```

2. **Sync required project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure regional credentials:**
    Create a local ```.env``` file in the root execution directory:
    ```bash
    GROQ_API_KEY=your_secured_api_key_string_here
    ```

4. **Add Source Document:**
    Ensure the ```Tesla_10-K.pdf``` (or equivalent financial corpus) is placed directly in the execution root directory.

5. **Trigger Production Script:**
    ```bash
    python solution.py
    ```

## Output Structure & Validation

Output Structure & Validation
Upon successful execution, the system dynamically generates structured JSON logs matching the required evaluation schema. These results (including baseline vs. improved retrieval comparisons, parent chunk references, and similarity scores) are automatically exported to the ```outputs/``` directory.