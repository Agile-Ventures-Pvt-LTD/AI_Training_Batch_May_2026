# Qualification Logic

## Purpose

This document describes the business logic implemented by the Autonomous Sales Lead Qualification Agent for qualifying inbound sales leads. The qualification process combines AI-based information extraction with configurable business rules to ensure consistent, repeatable, and policy-compliant decision making.

---

# Qualification Workflow

Every inbound sales inquiry follows the same processing sequence.

1. Lead Information Extraction
2. Data Normalization
3. Duplicate Detection
4. Reference Data Lookup
5. Qualification Scoring
6. Lead Classification
7. Sales Owner Assignment
8. Processing Decision

This deterministic workflow ensures that all leads are evaluated using identical business rules.

---

# Lead Information Extraction

The AI extracts structured information from the incoming email, including:

- Contact Name
- Company Name
- Job Title
- Country
- Industry
- Company Size
- Product Interest
- Estimated Budget
- Purchase Timeline
- Decision Role
- Lead Source
- Business Need

Extracted values are validated before further processing.

---

# Data Normalization

The extracted information is standardized to improve consistency.

Normalization includes:

- Country normalization
- Product normalization
- Company name formatting
- Budget conversion
- Timeline normalization

Reference data is used wherever applicable to minimize inconsistent values.

---

# Duplicate Detection

Before qualification, the agent checks whether the inquiry has already been processed.

Duplicate detection uses available identifiers and business information stored in the Lead Register.

If a duplicate is detected:

- Qualification is stopped.
- No new Lead Register entry is created.
- No Word report is generated.
- No customer communication is sent.

> **Screenshot – Duplicate Detection**

![Duplicate Detection](<Screenshot 2026-07-31 163729.png>)

---

# Reference Data Lookup

The agent retrieves operational data from Excel Online.

Reference tables include:

- Qualification Rules
- Product Catalog
- Territory Mapping
- Sales Owner Mapping
- Action Matrix

These tables provide the business rules used during autonomous decision making.

---

# Qualification Scoring

The agent evaluates each lead against the configured qualification criteria.

Typical evaluation factors include:

- Product alignment
- Budget availability
- Purchase timeline
- Decision authority
- Company profile
- Business requirement

A qualification score is calculated using the configured rules.

---

# Lead Classification

Based on the qualification score and configured thresholds, the agent classifies the inquiry into one of the supported categories.

Possible classifications include:

- Hot
- Qualified
- Nurture
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

Decision confidence is also evaluated before the classification is finalized.

---

# Sales Owner Assignment

Following classification, the agent determines the appropriate sales owner using the configured territory and ownership mappings.

Assignment considers:

- Customer territory
- Supported regions
- Product ownership
- Configured routing rules

The assigned owner is recorded in the Lead Register.

---

# Autonomous Decision Making

After qualification, the agent determines the required autonomous actions.

Possible actions include:

- Update Lead Register
- Generate Qualification Report
- Send Customer Acknowledgement
- Request Additional Information
- Notify Assigned Owner
- Notify Sales Operations
- Escalate for Human Review

Actions are determined using the configured business rules and decision confidence.

---

# Exception Handling

The qualification process handles several exceptional conditions.

Examples include:

- Missing mandatory information
- Duplicate inquiries
- Unsupported products
- Unsupported territories
- Low confidence classifications
- Connector failures

Cases that cannot be resolved autonomously are escalated for human review.

---

# Design Principles

The qualification logic was designed to ensure:

- Consistent decision making
- Configuration-driven business rules
- Minimal manual intervention
- Policy compliance
- Reliable autonomous execution