# Agent Instructions Design

## Project Information

| Field | Details |
|-------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Nandani Bisht |

---

# Purpose

This document describes the instruction design used for the Autonomous Sales Lead Qualification Agent. It explains the agent's responsibilities, business rules, autonomous decision-making process, and operational boundaries without exposing implementation secrets or internal prompts.

---

# Agent Role

The agent acts as an autonomous Sales Lead Qualification Assistant for NovaWorks Technologies.

Its primary responsibility is to monitor qualifying Outlook emails, evaluate incoming business opportunities, classify leads according to company policy, update operational records, generate qualification reports where applicable, and send the appropriate communications.

---

# Autonomous Objective

The agent is designed to automate the first stage of the sales qualification process by:

- Monitoring Outlook for project emails.
- Extracting structured lead information.
- Validating required business fields.
- Detecting duplicate opportunities.
- Reading operational reference data.
- Calculating qualification scores.
- Determining lead classifications.
- Assigning the appropriate sales owner.
- Updating operational Excel records.
- Creating Microsoft Word qualification reports.
- Sending internal and external Outlook communications.

---

# Trigger Scope

The agent processes only Outlook emails whose subject contains:

```
[P2-003 LEAD]
```

Emails that do not match the required subject filter are ignored.

---

# Lead Information Extraction

The agent extracts:

## Contact Information

- Contact Name
- Job Title
- Decision Role
- Email Address

## Organisation Information

- Company Name
- Country
- Territory

## Opportunity Information

- Product Interest
- Business Need
- Budget
- Purchase Timeline

---

# Business Validation

The agent validates that sufficient information exists before qualification.

Validation includes:

- Contact identification
- Company information
- Product selection
- Budget availability
- Timeline availability
- Decision role

Missing or ambiguous information may result in an Additional Information Request or Human Review.

---

# Duplicate Detection

Before creating a new record, the agent checks for existing opportunities using operational Excel data.

Duplicate detection considers:

- Message ID
- Contact
- Company
- Product Interest

Duplicate opportunities update existing records instead of creating new ones.

---

# Qualification Logic

The agent evaluates opportunities using business reference data stored in Excel.

Scoring considers:

- Product fit
- Budget
- Purchase timeline
- Decision role
- Company size
- Territory
- Lead completeness

The calculated score is used together with business exception rules to determine the final classification.

---

# Lead Classifications

Possible outcomes include:

- Hot
- Qualified
- Nurture
- Low Priority
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

---

# Tool Usage Strategy

The agent uses connector tools only when required.

### Excel Online (Business)

- Read reference tables
- Create lead records
- Update duplicate records

### Word Online (Business)

- Create qualification reports for applicable leads

### Outlook

- Send acknowledgements
- Request missing information
- Notify assigned sales owners
- Notify Sales Operations

---

# Human Review Conditions

The agent routes a case for manual review when:

- Product information is unclear.
- Territory cannot be mapped.
- Confidence is low.
- Competitor-related requests are detected.
- Conflicting business information exists.
- Tool execution uncertainty occurs.

---

# Privacy and Security

The solution uses only synthetic training data.

The agent does not:

- expose internal business logic,
- reveal qualification scores externally,
- provide pricing commitments,
- disclose confidential operational information.

---

# Error Handling

If a connector action fails, the agent:

1. Records the failure when possible.
2. Avoids reporting false success.
3. Requests human review if required.
4. Prevents incomplete processing from being represented as completed.

---

# Design Principles

The instruction design follows these principles:

- Controlled autonomy
- Deterministic business rules
- Human-in-the-loop for exceptions
- Transparent processing
- Consistent lead qualification
- Secure handling of business information
- Auditable operational workflow

---

# Summary

The instruction design enables Microsoft Copilot Studio to autonomously process qualifying sales inquiries while maintaining business consistency, auditability, privacy, and operational control. The implementation combines Generative Orchestration with Microsoft 365 connector tools to automate routine sales qualification tasks while routing exceptional cases for human review.