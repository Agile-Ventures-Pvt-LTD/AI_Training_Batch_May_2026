# AI Knowledge Assistant

An Enterprise Knowledge Assistant built with RAG, Groq, and LangChain.
## Participant Name

Mohammad Anas

## Setup and Execution

1. Create a virtual environment with uv venv and install dependencies:
   `uv add -r requirements.txt`

2. Copy `.env.example` to `.env` and add your Groq API Key. Remove the ``.example``

3. Place your document PDFs (Amazon Report) into `./data/raw/`.

4. Run the application:
   `python app.py`

## Usage
*It gives you two option 1 for asking question to the AI Assistant and option 2 for the running of benchmarks questions.*

- **Option 1:** Ask questions. The assistant will retrieve context, cite sources, and display debug chunks.

- **Option 2:** Run the benchmark evaluation script which will save a JSON report inside `outputs/`.

## Logs

Your asked questions are saved inside the ``/logs`` folder in the form of ``json``

## Thank You