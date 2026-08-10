# Agent Instructions Design

## Project Information

| Item | Details |
|------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Mohammad Anas |

---

# Purpose

This document describes the design principles, reasoning strategy, execution workflow, and business rules used to create the Microsoft Copilot Studio autonomous sales lead qualification agent.

The document explains how the agent was instructed to perform business tasks while remaining compliant with NovaWorks policies.

No confidential configuration values, authentication information, or connector secrets are included.

---

# Agent Role

The agent acts as an autonomous Sales Lead Qualification Assistant responsible for:

- Monitoring new Outlook sales enquiries
- Identifying valid commercial opportunities
- Extracting structured business information
- Reading operational reference data
- Detecting duplicate opportunities
- Calculating qualification scores
- Assigning lead classifications
- Assigning sales owners
- Updating the operational lead register
- Creating qualification reports
- Sending appropriate Outlook communications
- Escalating uncertain cases for human review

---

# Design Objectives

The instruction design was created to achieve the following objectives:

- Execute the complete workflow autonomously.
- Maintain deterministic business behaviour.
- Minimize hallucinations during decision making.
- Ensure connector tools are executed in the correct order.
- Prevent unsupported business commitments.
- Route uncertain situations to human review.
- Maintain auditability of every completed action.

---

# Instruction Structure

The overall instruction set is divided into the following logical sections.

## 1. Role Definition

Defines the business responsibility of the agent and establishes its operational scope.

The role instruction limits the agent to autonomous sales qualification activities only.

---

## 2. Trigger Scope

The agent processes only Outlook emails whose subject contains:

```
[P2-003 LEAD]
```

Emails outside this scope are ignored.

Messages classified as support, recruitment, academic research, spam, or competitor enquiries are identified as **Not a Sales Lead**.

---

## 3. Workflow Guidance

The instructions enforce a sequential execution model.

The agent is instructed to complete every required step before finishing execution.

The workflow includes:

1. Duplicate detection
2. Lead extraction
3. Data normalization
4. Reference table lookup
5. Qualification scoring
6. Lead classification
7. Excel update
8. Word report generation
9. Outlook communication

---

## 4. Information Extraction

The instructions direct the agent to extract structured business information from incoming emails.

Required information includes:

- Contact Name
- Email Address
- Job Title
- Company
- Country
- Territory
- Industry
- Company Size
- Product Interest
- Business Need
- Budget
- Purchase Timeline
- Decision Role
- Lead Source

Unknown information is preserved as **Unknown** instead of being inferred.

---

## 5. Reference Data Usage

The agent reads operational reference tables before making business decisions.

Reference tables include:

- QualificationRulesTable
- ProductCatalogTable
- TerritoryOwnersTable
- SalesOwnersTable
- ActionMatrixTable

These tables are treated as the authoritative business source.

---

## 6. Duplicate Detection Strategy

Before creating a new lead record, the agent searches the existing Lead Register.

Duplicate evaluation is performed using:

- Source Message ID
- Company Name
- Sender Email
- Product Interest

If a duplicate exists:

- Existing record is updated.
- A second acknowledgement is not sent.
- A second Word report is not created.
- Processing status becomes **Duplicate**.

---

## 7. Qualification Logic

The instructions require the agent to evaluate every lead using multiple business dimensions.

Evaluation includes:

- Product Fit
- Budget Viability
- Purchase Timeline
- Decision Role
- Company Size
- Territory
- Lead Source
- Data Completeness

Business override rules are evaluated before assigning the final classification.

---

## 8. Classification Logic

The agent is restricted to the following classifications:

- Hot
- Qualified
- Nurture
- Low Priority
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

No additional classifications may be generated.

---

## 9. Connector Execution

Connector tools are executed only when their business conditions are satisfied.

### Outlook

Used for:

- Customer acknowledgements
- Missing information requests
- Internal notifications

### Excel

Used for:

- Reading operational data
- Duplicate detection
- Creating lead records
- Updating existing records

### Word

Used only for eligible qualification outcomes.

---

## 10. Human Review

The instructions prevent autonomous qualification decisions when any of the following occur:

- Low confidence
- Unknown product
- Unmapped territory
- Conflicting information
- Competitor risk
- Connector failure
- Processing uncertainty

In these situations, the agent records completed actions and routes the case for manual review.

---

# Business Constraints

The instruction set explicitly prevents the agent from:

- Offering prices
- Negotiating discounts
- Making contractual commitments
- Guaranteeing delivery dates
- Sharing internal scoring logic
- Exposing confidential operational information
- Sending internal links to external users

---

# Error Handling Strategy

Each connector action follows the same handling pattern.

1. Execute connector.
2. Retry once if a transient failure occurs.
3. Record failure.
4. Notify Sales Operations.
5. Do not report unsuccessful actions as completed.

---

# Design Principles

The instruction design follows these principles:

- Deterministic workflow execution
- Controlled autonomous reasoning
- Policy-first decision making
- Human oversight for uncertain cases
- Minimal assumptions
- Structured output generation
- Connector-driven automation
- Auditability

---

# Security Considerations

The instruction design does not contain:

- Authentication credentials
- API keys
- Connector secrets
- Tenant identifiers
- Internal URLs
- Microsoft 365 tokens

Operational decisions rely only on:

- Incoming email content
- Operational Excel reference tables
- NovaWorks business policy
- Configured Microsoft 365 connector tools

---

# Summary

The instruction design enables the Microsoft Copilot Studio agent to autonomously process sales enquiries while maintaining compliance with NovaWorks operational policies.

The structured workflow, deterministic execution order, business-rule enforcement, and controlled human-review boundaries ensure that the agent performs consistent, auditable, and policy-compliant lead qualification.