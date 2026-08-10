# Customer Support Ticket Intelligence System

## Overview

This project is a Customer Support Ticket Intelligence System built using Python and the Groq API.

The application analyzes a support ticket and generates:

* Ticket Summary
* Ticket Classification
* Customer Sentiment Analysis
* Priority and Escalation Risk
* Sensitive Information Detection
* Routing Recommendation
* Draft Customer Response
* Response Quality Review
* Final Ticket Intelligence Package

---

## Project Structure

```text
project/
│
├── app.py
├── config.py
├── groq_client.py
├── prompts.py
├── validators.py
├── output_parser.py
│
├── outputs/
│   └── sample_ticket_output.json
│
├── tests/
│   └── test_validators.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a .env file

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Run the project

```bash
python app.py
```

---

## Prompting Techniques Used

* Role Prompting
* Few-Shot Prompting
* Structured JSON Output
* Hallucination Control Rules

---

## Output

The final output is saved as:

```text
outputs/sample_ticket_intelligence_output.json
```

---

## Notes

* The system only uses information provided in the ticket.
* It avoids making assumptions or unsupported claims.
* Generated responses should be reviewed before sending to customers.
* This project was built as part of the LLM Application Assignment.

```
```
