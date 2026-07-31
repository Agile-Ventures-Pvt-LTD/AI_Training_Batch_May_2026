# Agent Instructions Design

## Project Information

| Field                | Details                                   |
| -------------------- | ----------------------------------------- |
| **Project ID**       | P2-003                                |
| **Project Title**    | Autonomous Sales Lead Qualification Agent |
| **Participant Name** | Pranay Gupta                     |
| **Agent Name**       | Pranay NovaWorks Sales Lead Agent      |

---

# Purpose

The Agent Instructions define the behavior, responsibilities, decision boundaries, and operational workflow of the Autonomous Sales Lead Qualification Agent.

The instructions ensure that the agent performs lead qualification consistently while following the NovaWorks Sales Lead Qualification and Autonomy Policy and the operational data provided for the project.

---

# Design Objectives

The instruction set was designed to achieve the following objectives:

* Process incoming sales inquiries autonomously.
* Follow a structured execution sequence.
* Use operational reference data before making decisions.
* Prevent duplicate lead creation.
* Apply qualification rules consistently.
* Generate standardized outputs.
* Protect confidential business information.
* Escalate uncertain cases for human review.

---

# Agent Role

The agent acts as an autonomous Sales Lead Qualification Assistant responsible for:

* Processing incoming Outlook emails.
* Identifying valid sales opportunities.
* Extracting business information.
* Normalizing extracted data.
* Performing duplicate detection.
* Calculating qualification scores.
* Assigning business classifications.
* Determining the appropriate sales owner.
* Updating operational records.
* Generating qualification reports.
* Sending approved communications.
* Escalating exceptional scenarios.

---

# Instruction Structure

The instructions are organized into the following logical sections:

1. Agent Role
2. Trigger Scope
3. Lead Validation
4. Information Extraction
5. Data Normalization
6. Duplicate Detection
7. Qualification Logic
8. Classification Rules
9. Sales Owner Assignment
10. Excel Processing
11. Word Report Generation
12. Outlook Communication
13. Human Review Conditions
14. Error Handling
15. Privacy and Security Controls
16. Unsupported Requests

This modular structure improves readability, maintainability, and future updates.

---

# Execution Flow

The agent follows the execution sequence below:

```text
Receive Outlook Event
        │
        ▼
Validate Trigger
        │
        ▼
Determine Lead Eligibility
        │
        ▼
Extract Business Information
        │
        ▼
Normalize Values
        │
        ▼
Duplicate Detection
        │
        ▼
Read Operational Reference Data
        │
        ▼
Calculate Qualification Score
        │
        ▼
Apply Classification Rules
        │
        ▼
Assign Sales Owner
        │
        ▼
Update Excel Workbook
        │
        ▼
Generate Word Report (If Required)
        │
        ▼
Send Outlook Communication
        │
        ▼
Complete Processing
```

---

# Business Decision Strategy

The instructions require the agent to make decisions using operational business rules rather than assumptions.

The agent evaluates:

* Product suitability
* Budget availability
* Purchase timeline
* Decision authority
* Company size
* Territory support
* Lead source
* Information completeness

The resulting score determines the lead classification according to the defined business rules.

---

# Data Validation Strategy

Before any business decision is made, extracted information is validated and normalized.

Validation includes:

* Product verification
* Country normalization
* Territory mapping
* Decision role standardization
* Company size categorization
* Mandatory field verification

Unknown values are preserved rather than inferred.

---

# Duplicate Prevention Strategy

To prevent duplicate opportunities, the agent:

1. Checks the unique message identifier.
2. Compares company information.
3. Compares sender email.
4. Compares product interest.
5. Updates existing records when duplicates are detected.

This approach minimizes redundant records and prevents duplicate communications.

---

# Qualification Strategy

Qualification decisions are based on structured business criteria rather than free-form reasoning.

The scoring model evaluates multiple dimensions before assigning one of the supported business classifications.

Override rules are applied before the final classification is confirmed.

---

# Communication Strategy

The instructions define separate communication paths for different outcomes.

The agent may:

* Send acknowledgement emails.
* Request missing information.
* Notify assigned sales owners.
* Notify Sales Operations for exceptions.

The agent does not disclose internal scores, reasoning, pricing, contractual commitments, or confidential operational information.

---

# Human Review Strategy

The instructions intentionally avoid autonomous decision-making for uncertain or exceptional situations.

Examples include:

* Unknown products
* Unsupported territories
* Low confidence
* Conflicting information
* Competitor-related inquiries
* Tool failures
* Processing exceptions

These cases are routed for manual review.

---

# Error Handling Strategy

The instruction design includes controlled recovery mechanisms.

Supported behaviors include:

* Retry transient failures once.
* Record processing failures.
* Notify internal stakeholders.
* Prevent incomplete processing from being reported as successful.

This approach improves operational reliability while reducing unnecessary manual intervention.

---

# Privacy and Security Controls

The instruction set incorporates safeguards to ensure appropriate handling of project data.

The agent is instructed to:

* Use only supplied synthetic data.
* Avoid storing unnecessary personal information.
* Protect confidential business information.
* Prevent disclosure of internal logic.
* Avoid revealing operational tables or hidden instructions.

---

# Benefits of the Instruction Design

The implemented instruction design provides:

* Consistent autonomous behavior.
* Repeatable business decisions.
* Controlled exception handling.
* Standardized communication.
* Reliable operational processing.
* Improved maintainability.
* Better compliance with project requirements.

---

# Future Improvements

Possible enhancements to the instruction design include:

* Dynamic scoring models.
* Multi-language processing.
* AI confidence calibration.
* CRM-specific instruction sets.
* Industry-specific qualification logic.
* Expanded communication templates.

---

# Conclusion

The Agent Instructions provide a structured framework that enables the Microsoft Copilot Studio agent to autonomously process sales inquiries while following defined business rules, operational data, and governance requirements. The modular design improves readability, simplifies maintenance, and supports reliable autonomous execution across routine sales qualification scenarios.
