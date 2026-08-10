# AI-Powered Customer Support Ticket Triage and Response Assistant

This prototype processes customer support tickets and produces a structured support intelligence package using Python and the Groq API.

## Participant Name
Nandani Bisht

## Features

- Input validation for ticket subject, body, and response tone
- Ticket summarization
- Business issue classification
- Sentiment analysis
- Priority and escalation risk detection
- Sensitive information detection
- Internal routing recommendation
- Draft customer response generation
- Response quality review
- Final structured JSON output

## Setup the environment:

1. Copy `.env.example` to `.env`
2. Set `GROQ_API_KEY` in `.env`
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the code:

Use the sample ticket input by running:

```bash
python app.py
```

To load a custom ticket JSON file and save output to a specific path:

```bash
python app.py --input-file sample_ticket.json --output-file outputs/my_ticket_output.json
```

To save Markdown as well:

```bash
python app.py --markdown
```

## Prompt Engineering Techniques Used

- Role prompting for each task to set a clear analyst persona.
- Zero-shot prompts for summarization, sentiment detection, sensitive information detection, and quality review.
- Few-shot prompts for classification and priority/escalation risk analysis.
- Structured output schemas in every prompt to ensure valid JSON responses.
- Hallucination and policy control instructions to prevent unsupported promises, especially around refunds, cancellation status, and legal conclusions.

## Risk and Safety Handling

- The system flags **payment-related sensitive information** and avoids exposing actual sensitive data.
- Draft responses are constrained to **verification-based language** and explicitly avoid promises of refunds or cancellations unless supported.
- Escalation signals are used to determine **priority** and **routing recommendations**.

## Known Limitations
- The Groq API endpoint is assumed to use a generic `/v1/generate` interface.
- The model response parser attempts JSON extraction but may fail if the model returns badly formatted text.
- The prototype is built for a single-ticket workflow and does not yet support batch processing.


## Testing

Run the validation tests with:

```bash
pytest
```
