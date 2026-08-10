# Qualification Logic

## Project Information

| Field | Details |
|-------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Nandani Bisht |

---

# Overview

The Autonomous Sales Lead Qualification Agent evaluates incoming sales inquiries using business rules and reference data stored in Microsoft Excel. The qualification process ensures that every lead is assessed consistently before being classified and assigned to the appropriate sales owner.

The qualification logic combines data extraction, validation, duplicate detection, rule evaluation, and business overrides to determine the final processing outcome.

---

# Qualification Workflow

```
Incoming Lead
      │
      ▼
Extract Lead Information
      │
      ▼
Validate Required Fields
      │
      ▼
Duplicate Detection
      │
      ▼
Read Qualification Rules
      │
      ▼
Calculate Qualification Score
      │
      ▼
Apply Business Overrides
      │
      ▼
Determine Classification
      │
      ▼
Assign Sales Owner
      │
      ▼
Update Operational Records
```

---

# Information Extraction

The agent extracts the following business information from each email:

## Contact Information

- Contact Name
- Email Address
- Job Title
- Decision Role

## Company Information

- Company Name
- Country
- Territory

## Opportunity Information

- Product Interest
- Business Need
- Budget
- Purchase Timeline

---

# Data Validation

Before qualification, the agent validates that sufficient information has been provided.

Validation includes:

- Contact details are available.
- Company name is identified.
- Product interest is specified.
- Budget information is available.
- Purchase timeline is mentioned.
- Decision maker information is present.

If required information is missing, the agent requests additional information instead of continuing with qualification.

---

# Duplicate Detection

The agent checks the existing Leads Register before creating a new record.

Duplicate evaluation considers:

- Message ID
- Contact Email
- Company Name
- Product Interest

If an existing opportunity is identified:

- A new lead record is not created.
- The existing record is updated when appropriate.
- The lead is classified as a duplicate.

This approach prevents duplicate records and supports idempotent processing.

---

# Qualification Rules

Business qualification rules are retrieved from the Qualification Rules table stored in Excel.

The agent evaluates factors such as:

- Product fit
- Available budget
- Purchase timeline
- Decision-making authority
- Company information
- Territory mapping
- Completeness of lead information

These rules are used to calculate the overall qualification result.

---

# Lead Classification

After evaluation, the lead is assigned one of the following classifications:

- Hot
- Qualified
- Nurture
- Low Priority
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

The classification determines the subsequent workflow, including notifications and report generation.

---

# Business Overrides

Certain scenarios override the standard qualification process regardless of the calculated result.

Examples include:

- Duplicate opportunities
- Missing mandatory information
- Competitor-related inquiries
- Unsupported or unknown products
- Ambiguous business requirements
- Low-confidence extraction results

When an override is applied, the corresponding business action takes precedence over the calculated classification.

---

# Sales Owner Assignment

Once a lead is successfully qualified, the agent assigns the appropriate sales owner based on the Territory Owners reference table.

The assigned owner receives an internal Outlook notification containing the lead summary.

---

# Qualification Report

For applicable qualified opportunities, the agent generates a Microsoft Word qualification report containing:

- Lead details
- Qualification outcome
- Assigned sales owner
- Classification summary

The report provides a standardized record for future reference.

---

# Human Review Conditions

The agent routes a lead for manual review when:

- Business information is incomplete.
- Product mapping is uncertain.
- Territory assignment cannot be determined.
- Competitor involvement is detected.
- Qualification confidence is low.
- Connector execution prevents reliable completion.

In these situations, automated actions are limited until human validation is completed.

---

# Error Handling

If an error occurs during qualification:

- The agent avoids creating inaccurate records.
- False success confirmations are not sent.
- Appropriate internal notifications are generated when required.
- Processing can be resumed after the issue is resolved.

---

# Summary

The qualification logic combines automated data extraction, validation, duplicate prevention, business rule evaluation, classification, and controlled exception handling to ensure that sales opportunities are processed consistently, accurately, and in accordance with NovaWorks Technologies' operational requirements.