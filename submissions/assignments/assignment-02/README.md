# Assignment 02 - Query Expansion

## Participant Name
Mohammad Anas

## Description
This assignment demonstrates the Query Expansion technique to improve retrieval in a Retrieval-Augmented Generation (RAG) system. It uses an LLM via the Groq API to generate synonymous variations of a user query, expanding the semantic search space across a local vector database (ChromaDB) to retrieve more comprehensive context from PDF documents (Tesla Annual Reports).

## How to Run

1. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   On Windows use: 
   .venv\Scripts\activate
   ```
2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Environment Variables:**
    Create a .env file in the root directory and add your Groq API key:

    ```bash
    GROQ_API_KEY=your_actual_api_key_here
    ```

4. **Execute the Code:**
    ```bash
    python solution.py
    ```


##  Libraries / Packages Required


    groq>=1.2.0
    ipykernel>=7.2.0
    python-dotenv>=1.2.2
    datasets>=3.3.2
    tiktoken==0.9.0
    pypdf==5.4.0

    langchain==0.3.20
    langchain-community==0.3.19
    langchain-core==0.3.41
    langchain-text-splitters==0.3.6

    chromadb==0.5.15
    sentence-transformers==5.1.2
    langchain-cohere==0.4.5

## Files Included

1. **solution.py :** Main execution script containing the PDF loading, vector database creation, and Query Expansion logic.

2. **requirements.txt :** Project dependencies.

3. **README.md :** Project documentation.

## Output Explanation

The system parses local PDF files, splits them into manageable chunks, and stores their embeddings in a Chroma vector database. During execution, the console outputs the real-time progress. When a test query is passed, the system prints the original query, displays the 3 LLM-generated expanded queries, and finally outputs the context-grounded accurate answer retrieved entirely from the vector database.