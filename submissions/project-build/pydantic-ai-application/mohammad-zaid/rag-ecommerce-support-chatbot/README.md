# RAG E-commerce Support Chatbot

A simple chatbot that reads an eBay seller guide PDF and answers your questions about it.

## Setup (Step-by-Step)

**1. Download the PDF**
Download the eBay guide from this link: 
Save it inside the `data/` folder and rename it to exactly `seller_guide.pdf`.

**2. Add your API Key**
Create a file named `.env` in the main project folder and paste your Groq API key inside it:
```text
GROQ_API_KEY=your_actual_groq_api_key_here
```

**3. Install Dependencies**
Open your terminal in the project folder and run:
```bash
uv venv
uv pip install -r requirements.txt
```



## How to Run Tests

To check if the chatbot is answering questions accurately, run:
```bash
uv run python tests/test_rag_metrics.py
```