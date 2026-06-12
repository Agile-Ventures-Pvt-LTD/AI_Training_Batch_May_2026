# Customer Support Ticket Intelligence System

This project reads a support ticket from `input.json`, sends it through a small LLM workflow, and saves both the intermediate decisions and the final support-agent output.

The code is intentionally split into step files under `steps/` so it is easy to see which LLM call produced which JSON artifact.

## Workflow

| Step code | Saved output | Purpose |
| --- | --- | --- |
| `steps/ticket_summarize.py` | `steps/02_ticket_summary.json` | Summarizes the customer issue and missing details |
| `steps/ticket_classify.py` | `steps/03_ticket_classification.json` | Classifies the ticket category |
| `steps/sentiment_analyze.py` | `steps/04_sentiment_analysis.json` | Reads customer sentiment and emotional signals |
| `steps/priority_escalation.py` | `steps/05_priority_and_escalation.json` | Assigns priority and escalation risk |
| `steps/sensitive_info_review.py` | `steps/06_sensitive_information_review.json` | Flags sensitive information and handling notes |
| `steps/routing_recommendation.py` | `steps/07_routing_recommendation.json` | Recommends the support queue |
| `steps/response_draft.py` | `steps/08_customer_response_draft.json` | Drafts the customer-facing reply |
| `steps/response_quality.py` | `steps/09_response_quality_review.json` | Reviews the response for quality and policy safety |

`app.py` is the orchestrator. It validates the input, calls each step, stores the step JSON files, and then writes:

```text
outputs/support_ticket_intelligence_output.json
```

## Setup

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=2500
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

or, if using the included virtual environment on Windows:

```bash
.\.venv\Scripts\python.exe app.py
```

## Input

The sample `input.json` includes:

- `customer_name`
- `customer_type`
- `ticket_subject`
- `ticket_body`
- `product_area`
- `previous_interaction_history`
- `sla_tier`
- `response_tone`
- `business_rules`

The validators keep the input simple: required fields cannot be blank, ticket text has length limits, and customer/SLA tiers must be known values.
