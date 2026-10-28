# LLM Application -  AI-Powered Customer Support Ticket Intelligence System Using Groq + Python

## Participant Name

**Vaibhav Kesarwani**

## Project Title

## AI-Powered Customer Support Ticket Triage and Response Assistant

This project is an automated tool for processing incoming customer support tickets and generate a structured support intelligence report with all the madatory things which needs to have the attention like:

1. Ticket summary
2. Ticket category classification
3. Sentiment analysis
4. Priority classification
5. Escalation risk detection
6. Sensitive information detection
7. Suggested internal routing
8. Draft customer response
9. Response quality review

It is designed for SaaS company who receives hundreds of customer support tickets every day through email, chat, and helpdesk tools. Support agents manually read each ticket,  understand the issue, classify it, decide priority, identify risks, and draft customer responses using AI while maintaining control, consistency, and quality checks.

---

## The manual process creates several problems:

1. Tickets are not classified consistently.
2. Urgent tickets are sometimes missed.
3. Support managers do not get quick visibility into common issues.
4. Customer responses vary in quality and tone.
5. Escalation risks are identified late.
6. Agents spend too much time reading long customer messages
7. Tickets containing sensitive information are not always flagged correctly

## The soultion for the above process

The AI tool analyze the ticket and produce:

- Summary of the issue
- Category: Billing issue | TECHNICAL_BUG | ACCOUNT_ACCESS
- Sentiment: Positive | Negative | frustrated
- Priority: Urgent | LOW | HIGH
- Escalation risk: High | Low | Medium
- Sensitive information: Payment-related information present
- Suggested team: Billing support | finance operations
- Draft response: Empathetic, professional, does not promise refund without verification
- Internal note: Requires verification of cancellation date and duplicate charge

---

## Key Features

- Modular LLM-based pipeline (step-by-step generation)
- Structured JSON outputs at each stage
- Priority and Escalation Risk Detection
- Internal Routing Suggestion
- Response Quality Review 
- Final consolidated export (`output/final_ticket.json`)

---

## How It Works

### 1. Input Data
You define structured input like:

- Ticket Subject
- Ticket Body
- Product Area
- Previous Interaction 
- History
- SLA Tier
- Response Tone
- Business Rules 

---

### 2. Pipeline Steps

The system runs through multiple LLM stages:

- Ticket Summarization  
- Ticket Classification
- Sentiment and Customer Emotion Detection
- Priority and Escalation Risk Detection
- Sensitive Information Detection
- Suggested Internal Routing
- Draft Customer Response Generation
- Response Quality Review

Each step uses a dedicated prompt inside the `prompts.py` file.

---

### 3. Output Generation

Final outputs are stored in:

- `output/final_ticket.json` -> Structured JSON containing all artifacts  

---

## Example Output Structure

```json
{
    "ticket_summary": {},
    "classification": {},
    "sentiment_analysis": {},
    "priority_and_risk": {},
    "sensitive_information_check": {},
    "routing_recommendation": {},
    "draft_customer_response": {},
    "response_quality_review": {},
    "generation_metadata": {
        "model_used": "llama-3.3-70b-versatile",
        "temperature": 0.2,
        "total_steps_completed": 8
    }
}
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 2. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 3. Run the Pipeline

```bash
app.ipynb
```
Run all the cells
