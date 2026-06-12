# AI Powered Customer Support Ticket Intelligence System

## Overview

This project uses Groq LLM APIs and Python to analyze customer support tickets and generate structured support intelligence.

The application performs:

- Ticket Summarization
- Ticket Classification
- Sentiment Analysis
- Priority Detection
- Escalation Risk Detection
- Sensitive Information Detection
- Internal Routing Recommendation
- Draft Customer Response Generation
- Response Quality Review
- JSON Export

---

## Project Structure

```text
support_ticket_ai_project/

├── app.py
├── groq_client.py
├── prompts.py
├── validators.py
├── output_parser.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md

├── outputs/
│   └── sample_ticket_output.json

└── tests/
    └── test_validators.py
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create a .env file

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Run Application

```bash
python app.py
```

---

## Run Tests

```bash
pytest
```

---

## Prompt Engineering Techniques Used

### Role Prompting

Each task uses a specialized role:

- Senior Support Analyst
- Support Operations Specialist
- Customer Experience Analyst
- Escalation Manager
- Data Privacy Reviewer
- Support QA Reviewer

### Zero Shot Prompting

Used for:

- Summarization
- Sentiment Analysis
- Sensitive Information Detection
- Response Review

### Structured Output Prompting

All model outputs return JSON.

### Hallucination Control

The prompts explicitly instruct:

- Do not invent account status
- Do not invent refund status
- Do not invent cancellation status
- Ask for missing information

---

## Error Handling

The project handles:

- Missing API key
- Empty subject
- Empty body
- Short ticket body
- Invalid JSON response
- API retry failures

---

## Restrictions Followed

- No RAG
- No Embeddings
- No Vector Databases
- No External Knowledge Base
- No Web Search

---

## Output

Generated file:

```text
outputs/sample_ticket_output.json
```