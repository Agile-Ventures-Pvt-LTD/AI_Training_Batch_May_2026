# Support Ticket AI Project

## Participant Name

**Mohd Zaid Ansari**

## Description

This project implements an end-to-end Support Ticket Intelligence System that automates the analysis of customer support tickets using Large Language Models (LLMs) through the Groq API.

The system processes customer support tickets and generates a structured Ticket Intelligence Package containing:

* Ticket Summarization
* Ticket Classification
* Sentiment Analysis
* Priority and Escalation Risk Detection
* Sensitive Information Detection
* Internal Routing Recommendation
* Draft Customer Response Generation
* Response Quality Review

The application follows prompt engineering best practices including:

* Zero-Shot Prompting
* Few-Shot Prompting
* Role-Based Prompting
* Reasoning Summary Generation
* Hallucination Control

The final output is generated as structured JSON and can be displayed in the notebook or saved to a file.

---

## Features Implemented

### FR-2: Input Validation

Validates:

* Ticket subject cannot be empty
* Ticket body cannot be empty
* Ticket body must contain at least 30 characters
* Response tone must be provided
* Previous interaction history handling
* Long ticket body detection

### FR-3: Ticket Summarization

Generates:

* Short summary
* Customer problem
* Business impact
* Customer requested action
* Important context
* Missing information

### FR-4: Ticket Classification

Classifies tickets into categories such as:

* BILLING_ISSUE
* TECHNICAL_BUG
* FEATURE_REQUEST
* ACCOUNT_ACCESS
* COMPLIANCE_OR_PRIVACY
* ESCALATION_COMPLAINT

### FR-5: Sentiment Analysis

Detects:

* Sentiment
* Emotion signals
* Sentiment reasoning
* Confidence score

### FR-6: Priority and Escalation Risk Detection

Determines:

* Priority Level
* Escalation Risk
* Risk Triggers
* Recommended SLA Action

### FR-7: Sensitive Information Detection

Identifies:

* Payment Information
* Personal Information
* Account Data
* Other sensitive content

### FR-8: Internal Routing Recommendation

Routes tickets to:

* BILLING_SUPPORT
* TECHNICAL_SUPPORT
* ACCOUNT_MANAGEMENT
* SECURITY_TEAM
* COMPLIANCE_TEAM
* PRODUCT_TEAM
* CUSTOMER_SUCCESS
* GENERAL_SUPPORT

### FR-9: Draft Customer Response Generation

Creates a professional customer-facing response while:

* Maintaining empathy
* Avoiding unsupported promises
* Following business rules
* Requesting missing information

### FR-10: Response Quality Review

Evaluates responses based on:

* Empathy
* Correctness
* Actionability
* Policy Safety
* Tone Alignment
* Completeness

### FR-11: Final Ticket Intelligence Package

Generates a consolidated JSON output containing all analysis stages.

---

## Project Structure

```text
support-ticket-intelligence/
│
├── app.py
├── prompts.py
├── validators.py
├── groq_client.py
├── output_parser.py
├── requirements.txt
│
├── tests/
│   └── test_validators.py
│
├── outputs/
│   └── sample_ticket_output.json
│
└── main.ipynb
```

---

## Prompt Engineering Techniques Used

| Requirement                     | Technique Used                                   |
| ------------------------------- | ------------------------------------------------ |
| Ticket Summarization            | Role Prompting                                   |
| Classification                  | Role + Few-Shot Prompting                        |
| Sentiment Analysis              | Role + Few-Shot Prompting                        |
| Priority Detection              | Role + Few-Shot Prompting                        |
| Sensitive Information Detection | Role Prompting                                   |
| Routing Recommendation          | Role + Few-Shot Prompting                        |
| Draft Response Generation       | Role Prompting + Internal Reasoning Instructions |
| Quality Review                  | Role Prompting + Zero-Shot Prompting             |

---

## How to Run

### 1. Clone Repository

```bash
git clone <repository-url>
cd support-ticket-intelligence
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### 4. Run Notebook

Open:

```text
main.ipynb
```

Run all cells sequentially.

or run the application:

```bash
python app.py
```

---

## Required Libraries

```text
groq
python-dotenv
json
pytest
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Assumptions

* Groq API key is available and valid.
* LLM returns valid JSON responses.
* Customer input follows the provided schema.
* Refunds, cancellations, or billing corrections are never confirmed unless explicitly verified.
* Public escalation threats increase escalation risk.
* Premium customers may require higher-priority handling.
* Feature requests are treated separately from technical bugs.

---

## Sample Input

The project uses the sample customer ticket provided in the assignment document involving:

* Duplicate billing charge
* Subscription cancellation dispute
* Prior unresolved support interactions
* Public escalation threat
* Premium customer SLA

---

## Sample Output

The system generates a Final Ticket Intelligence Package containing:

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

## Output Location

Generated outputs are saved in:

```text
outputs/sample_ticket_output.json
```

---

