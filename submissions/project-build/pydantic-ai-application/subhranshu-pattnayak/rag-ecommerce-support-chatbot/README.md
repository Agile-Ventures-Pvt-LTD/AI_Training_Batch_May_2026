# `P005 - Rag Ecommerce Support Chatbot`

This is a Rag Ecommerce Support Chatbot built with **Pydantic, GroqLLM, ChromaDB**, and **COHERE**.

Here, Chatbot can use a language model to interact with seller_guide_db vector database to answer user queries.

---

# Project Structure

```
rag-ecommerce-support-chatbot
├── .env.example
├── README.md
├── data
│   └── Advanced_Business_Seller_Guide_May09.pdf
├── requirements.txt
├── seller_guide_db
│   ├── chroma.sqlite3
│   └── fe7046c0-13f5-4569-930e-deb28aa2334a
│       ├── data_level0.bin
│       ├── header.bin
│       ├── length.bin
│       └── link_lists.bin
└── src
    ├── agent.py
    ├── config.py
    ├── database.py
    ├── prompts.py
    └── rag
        ├── __init__.py
        ├── chunker.py
        ├── embedding.py
        └── loader.py
```

---

# Environment Variables (Jira and Groq Configuration)

Create a `.env` file in the project root and add the corresponding values.

```env
GROQ_API_KEY=...
GROQ_MODEL=openai/gpt-oss-120b

COHERE_API_KEY=...

OUTPUT_PATH=outputs
DATA_PATH=data

COLLECTION_NAME=09th-May-advanced-business-seller-guide
```

---


# Available MCP Tools

The Chatbot exposes the following tools.

| Tool | Description |
|------|-------------|
| retrieve | Retrieves data from vector database after reranking and compressing it. |


---

# Running the Server (stdio)

Start the Agent Loop:

```bash
python src/agent.py
```
The agent returns output in natural language.


---

# Notes

1. The project is missing the following requirements:
- Guardrails config
- DeepEval Tests

2. What the project displays:
- Clean and safe database creation pipeline
- Refined reranking based retriever tool to increase context relevancy and answer relevancy
- Agent loop in asnychronous mode.

3. Warning: For evaluation purpose the data and database are uploaded, although this is not appropriate practice.

---

# `THANK YOU`