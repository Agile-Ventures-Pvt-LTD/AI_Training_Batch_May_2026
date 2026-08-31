# Support Ticket AI Project

A Python-based AI support ticket assistant that analyzes incoming customer tickets and generates structured summaries, classifications, risk assessments, routing recommendations, and draft agent responses.

## Project Overview

This project is built to help support teams quickly understand and act on customer issues. It uses prompt templates and response parsing to produce a consistent JSON output for each ticket, including:
- Ticket summary
- Ticket classification
- Sentiment analysis
- Priority and escalation risk
- Sensitive information detection
- Routing recommendation
- Draft customer response
- Response quality review
- Generation metadata

## Key Files

- `prompts.py` - Prompt templates and structured instructions for the AI model
- `output_parser.py` - JSON cleanup and parsing helper for model responses
- `validators.py` - Input validation logic for ticket details and response tone
- `main.py` - Project entrypoint placeholder for running the application
- `requirements.txt` - Python dependency list
- `Outputs/sample_ticket_output.json` - Example generated ticket output

## Requirements

- Python 3.11 or newer
- `groq` library
- `python-dotenv`

## Environment Setup

Create a `.env` file at the project root with your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Run the project

Open `main.py` and update it to call your prompt flow, or use the notebook/workflow you build around the prompt templates.

### Parse model output

Use `output_parser.py` to safely clean and parse JSON returned by the model, even when the response may include markdown fences or extra text.

Example:

```python
from output_parser import parse_json_response

response = "..."
data = parse_json_response(response)
```

### Validate inputs

Use `validators.py` to ensure required ticket fields are present before sending data to the AI model.

Example:

```python
from validators import validate_inputs

ticket_data = {
    "customer_name": "Amit",
    "customer_type": "Premium",
    "ticket_subject": "Charged twice and no response from support",
    "ticket_body": "...",
    "response_tone": "empathetic"
}
validate_inputs(ticket_data)
```




## Notes

- `prompts.py` defines the assistant role, zero-shot instructions, and few-shot guidance for structured ticket analysis.
- `output_parser.py` includes `clean_json_text` to remove code fences and extract valid JSON.
- `validators.py` provides checkpoints for required ticket fields and minimum content length.

## Improvements

To extend this project, consider adding:
- a proper notebook or CLI workflow for ticket ingestion
- full Groq client integration and API request handling
- automated tests for prompt validity and parser robustness
- support for multiple ticket sources or bulk processing
- richer sample outputs in `Outputs/sample_ticket_output.json`
