# AI-Powered Customer Support Ticket Intelligence System

## Project Overview

This project is an AI-powered Customer Support Ticket Intelligence System built using **Python** and **Groq LLM APIs**.

The application acts as an internal support co-pilot that helps customer support teams process incoming support tickets faster and more consistently.

Instead of manually reviewing each ticket, support agents can use this system to:

* Summarize customer issues
* Classify ticket categories
* Detect customer sentiment
* Identify ticket priority
* Detect escalation risks
* Identify sensitive information
* Recommend internal routing
* Generate customer response drafts
* Review response quality
* Produce a final structured intelligence package

The system is designed to assist support agents and managers while keeping humans in control of final decisions.

---

# Features

## Ticket Summarization

Generates a concise summary of the customer issue including:

* Customer problem
* Business impact
* Requested action
* Important context
* Missing information

---

## Ticket Classification

Classifies tickets into categories such as:

* BILLING_ISSUE
* TECHNICAL_BUG
* ACCOUNT_ACCESS
* FEATURE_REQUEST
* SUBSCRIPTION_CHANGE
* COMPLIANCE_OR_PRIVACY
* PERFORMANCE_ISSUE
* HOW_TO_SUPPORT
* CANCELLATION_OR_REFUND
* ESCALATION_COMPLAINT
* OTHER

---

## Sentiment Analysis

Detects customer sentiment:

* POSITIVE
* NEUTRAL
* NEGATIVE
* FRUSTRATED
* ANGRY
* URGENT

Also identifies emotional signals and confidence scores.

---

## Priority & Escalation Risk Detection

Determines:

### Priority

* LOW
* MEDIUM
* HIGH
* URGENT

### Escalation Risk

* LOW
* MEDIUM
* HIGH
* CRITICAL

Factors considered:

* Customer impact
* SLA tier
* Public escalation threats
* Repeated support failures
* Payment issues

---

## Sensitive Information Detection

Detects:

* PAYMENT_INFORMATION
* PERSONAL_INFORMATION
* ACCOUNT_IDENTIFIER
* LEGAL_OR_COMPLIANCE_INFORMATION
* SECURITY_INFORMATION

Provides handling recommendations without exposing sensitive data.

---

## Internal Routing Recommendation

Suggests routing to:

* BILLING_SUPPORT
* TECHNICAL_SUPPORT
* ACCOUNT_MANAGEMENT
* SECURITY_TEAM
* COMPLIANCE_TEAM
* PRODUCT_TEAM
* CUSTOMER_SUCCESS
* GENERAL_SUPPORT

---

## Customer Response Generation

Creates professional responses that:

* Acknowledge customer concerns
* Show empathy
* Explain next steps
* Request missing information
* Avoid unsupported promises

---

## Response Quality Review

Evaluates generated responses on:

* Empathy
* Correctness
* Actionability
* Policy Safety
* Tone Alignment
* Completeness

---

# Prompt Engineering Techniques Used

## 1. Role Prompting

Each task assigns a specialized role:

| Task                            | Role                                 |
| ------------------------------- | ------------------------------------ |
| Summarization                   | Senior Support Analyst               |
| Classification                  | Support Operations Triage Specialist |
| Sentiment Analysis              | Customer Experience Analyst          |
| Risk Detection                  | Support Escalation Manager           |
| Sensitive Information Detection | Data Privacy Reviewer                |
| Routing Recommendation          | Support Operations Manager           |
| Response Generation             | Senior Customer Support Agent        |
| Quality Review                  | Support QA Reviewer                  |

---

## 2. Zero-Shot Prompting

Used for:

* Ticket Summarization
* Sentiment Analysis
* Sensitive Information Detection
* Quality Review

Each prompt includes:

* Role
* Task
* Input
* Rules
* Output Schema

---

# Project Structure

```text
support_ticket_ai_project/
│
├── app.py
├── groq_client.py
├── prompts.py
├── validators.py
├── output_parser.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
│
├── outputs/
│   └── sample_ticket_output.json
│
```

---

# Installation

## Initializing UV package
uv init

## Create Virtual Environment

### Windows

```powershell
uv venv
.venv\Scripts\activate
```

---

## Install Dependencies

```powershell
uv pip install -r requirements.txt
```
---

# Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

---

# Running the Application

```powershell
python app.py
```

The application will:

1. Accept ticket input
2. Validate data
3. Generate summary
4. Classify category
5. Analyze sentiment
6. Detect risk
7. Detect sensitive information
8. Recommend routing
9. Draft response
10. Review response
11. Generate final intelligence package
12. Save output

---

# Sample Output

The final output contains:

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
  "generation_metadata": {}
}
```

---

# Error Handling

The system handles:

* Missing API key
* Empty ticket subject
* Empty ticket body
* Short ticket body
* Invalid JSON responses
* API failures
* API timeout
* Rate limiting
* Long ticket inputs

---

# Security Considerations

* API keys are stored in environment variables
* Sensitive customer information is not unnecessarily displayed
* Real customer data should not be used
* Prototype should only be tested with sample or anonymized data

---

# Known Limitations

* Depends on LLM output quality
* Classification confidence may vary
* Does not use external knowledge sources
* No RAG or vector search support
* Response quality depends on ticket completeness

---
