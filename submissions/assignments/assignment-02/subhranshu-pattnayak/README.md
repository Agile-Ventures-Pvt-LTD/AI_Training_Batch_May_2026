# Tesla 10-K Query Expansion Notebook
This notebook demonstrates a retrieval-augmented question answering workflow over Tesla 10-K documents using a Chroma vector store, embedding model, and the Groq chat API.

## What this notebook does
- loads environment variables and configures the Groq API client
- initializes a Chroma persistent vector store stored in `./tesla_db`
- creates an embedding model for semantic retrieval
- defines a query expansion prompt to generate multiple paraphrases of the user question
- retrieves relevant document passages for each expanded query
- constructs a context-aware question prompt and asks the Groq chat model to answer

## Setup
1. Create a `.env` file with your Groq API key:
   ```text
   GROQ_API_KEY=your_api_key_here
   ```
   ```bash
   uv venv
   ```
2. Install the required Python packages:
   ```bash
   uv sync
   ```
3. Ensure the `./tesla_db` directory exists.
4. Run the notebook cells sequentially from top to bottom.

## Notes
- The notebook expects a persistent Chroma collection named `tesla-10k-2019-to-2023`.
- Query expansion is performed before retrieval to broaden the search and capture paraphrased match text.
- The final response is produced by a second Groq chat prompt that is constrained to the retrieved context.
- If the answer is not found in the retrieved context, the model is instructed to return `I don't know`.

## Usage
- Change `user_input` to your question.
- Run `retrieve_context(...)` to fetch relevant context.
- Run `respond(...)` to get the final answer.

## Important
- This notebook is intended for experimentation and evaluation of query expansion and retrieval.
- Review the prompts and behavior before using it for production or sensitive financial decision-making.
