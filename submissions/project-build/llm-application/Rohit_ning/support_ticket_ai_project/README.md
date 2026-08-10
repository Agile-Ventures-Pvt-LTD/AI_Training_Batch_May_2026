# AI-Powered Customer Support Ticket Intelligence

A simple Python prototype that analyzes customer support tickets using the Groq API and structured prompt engineering.

## Project Structure

- `app.py` - orchestration of ticket validation, prompt calls, and output saving
- `groq_client.py` -reusable client code
- `prompt.py` - all prompt templates 
- `validators.py` - ticket input validation rules
- `output_parser.py` - JSON parsing and simple repair for model output
- `outputs/sample_ticket_output.json` - sample output JSON
- `

## Setup

1. create .venv 
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The app will validate the sample ticket, call Groq for each analysis step, and save final output to `outputs/sample_ticket_output.json`.

## Prompt Engineering Techniques Used

- Role prompting: Each prompt assigns a task-specific role
- **Zero-shot prompting: Summary, sentiment, sensitive information detection, and response review use zero-shot templates with clear rules and output schemas.
- Few-shot prompting: Classification uses multiple examples to teach category mapping and avoid tone-only classification.
- Structured output: Every prompt includes a JSON schema to guide the model and simplify parsing.
- Hallucination control: Draft response instructions explicitly forbid inventing refund or cancellation status.

