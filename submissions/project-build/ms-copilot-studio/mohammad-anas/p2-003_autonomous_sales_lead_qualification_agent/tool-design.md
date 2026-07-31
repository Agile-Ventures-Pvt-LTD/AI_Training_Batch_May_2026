# Tool Design

## Project Information

| Item | Details |
|------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Mohammad Anas |

---

# Purpose

This document describes the Microsoft 365 connector tools used by the Autonomous Sales Lead Qualification Agent, their responsibilities, execution sequence, inputs, outputs, and error-handling strategy.

The solution uses native Microsoft Copilot Studio connector tools to automate the complete lead qualification workflow.

---

# Tool Architecture

The agent follows a tool-driven execution model.

```
Outlook Trigger
        │
        ▼
Lead Information Extraction
        │
        ▼
Excel Data Retrieval
        │
        ▼
Duplicate Detection
        │
        ▼
Qualification Evaluation
        │
        ▼
Excel Record Update
        │
        ▼
Word Report Generation
        │
        ▼
Outlook Communication
```

Each tool performs a specific business function before control passes to the next stage.

---

# Tool Inventory

| Tool | Purpose |
|------|---------|
| Outlook – When a New Email Arrives (V3) | Starts the workflow |
| Excel – List Rows Present in a Table | Retrieves operational reference data |
| Excel – Add a Row into a Table | Creates new lead records |
| Excel – Update a Row | Updates existing lead records |
| Word – Populate a Microsoft Word Template | Generates qualification reports |
| Outlook – Send an Email (V2) | Sends customer and internal communications |

---

# Tool 1 – Outlook Trigger

## Purpose

Automatically starts the qualification workflow when a new Outlook email is received.

## Input

- Incoming Outlook email

## Output

- Message ID
- Subject
- Sender
- Email body
- Conversation ID
- Attachments
- Received time

## Downstream Usage

Provides the source data required for extraction, duplicate detection, and qualification.

---

# Tool 2 – Excel: List Rows Present in a Table

## Purpose

Reads operational reference data required during qualification.

## Tables Accessed

- LeadsRegisterTable
- QualificationRulesTable
- TerritoryOwnersTable
- ProductCatalogTable
- SalesOwnersTable
- ActionMatrixTable

## Input

- Workbook location
- Table name

## Output

Structured table records used by the qualification engine.

## Business Role

This tool provides the reference information needed to:

- Detect duplicate leads
- Retrieve qualification rules
- Validate products
- Assign territories
- Determine sales ownership
- Identify recommended actions

---

# Tool 3 – Excel: Add a Row into a Table

## Purpose

Creates a new lead record when no existing record is found.

## Input

Structured lead information including:

- Lead ID
- Company
- Contact Name
- Email Address
- Product Interest
- Qualification Score
- Classification
- Assigned Owner
- Processing Status

## Output

A new record in the Lead Register.

## Execution Condition

Executed only when duplicate detection confirms that no matching lead exists.

---

# Tool 4 – Excel: Update a Row

## Purpose

Updates an existing lead record when the incoming enquiry matches an existing opportunity.

## Updated Information

- Qualification score
- Classification
- Assigned owner
- Last processed date
- Processing status
- Follow-up action

## Execution Condition

Executed only after successful duplicate detection.

---

# Tool 5 – Word: Populate a Microsoft Word Template

## Purpose

Generates a standardized Lead Qualification Report for eligible opportunities.

## Report Contents

- Lead details
- Customer information
- Opportunity summary
- Qualification score
- Classification
- Assigned sales owner
- Recommended next action
- Processing timestamp

## Output

Completed Microsoft Word qualification report.

## Execution Condition

Executed only after successful qualification and classification.

---

# Outlook – Send an Email (V2)

## Purpose

Sends the appropriate email based on the qualification outcome.

## Communication Types

### Customer Acknowledgement

Sent when a valid lead has been successfully processed.

---

### Missing Information Request

Sent when mandatory information required for qualification is incomplete.

---

### Internal Notification

Sent to the assigned sales representative after successful qualification.

---

### Human Review Notification

Sent internally when the agent cannot make a confident autonomous decision.

---

# Tool Execution Sequence

The tools execute in the following order:

| Step | Tool |
|------|------|
| 1 | Outlook Trigger |
| 2 | Excel – Read Reference Tables |
| 3 | Duplicate Detection |
| 4 | Qualification Evaluation |
| 5 | Excel – Add or Update Lead |
| 6 | Word Report Generation |
| 7 | Outlook Communication |

Each tool depends on the successful completion of the previous step.

---

# Tool Dependencies

| Tool | Depends On |
|------|------------|
| Outlook Trigger | None |
| Excel Read | Outlook Trigger |
| Duplicate Detection | Excel Read |
| Qualification Evaluation | Duplicate Detection |
| Excel Update | Qualification Evaluation |
| Word Generation | Excel Update |
| Outlook Communication | Word Generation (where applicable) |

---

# Error Handling Strategy

Each tool follows a consistent error-handling approach.

1. Execute the tool.
2. Validate the returned result.
3. Retry once for transient failures.
4. Record the failure.
5. Stop dependent operations if required.
6. Route unresolved cases for human review.

This approach prevents incomplete or inconsistent processing.

---

# Security Controls

The tools do not expose:

- Authentication credentials
- Access tokens
- Tenant identifiers
- Internal URLs
- Business secrets

All authentication is managed securely through Microsoft 365 connector permissions.

---

# Design Principles

The tool design follows these principles:

- Single responsibility for each tool
- Sequential execution
- Controlled data flow
- Reusable connector actions
- Minimal manual intervention
- Consistent error handling
- Policy-compliant automation
- Full auditability

---

# Benefits

The selected tool architecture provides:

- Native Microsoft 365 integration
- Reduced manual processing
- Reliable operational workflows
- Standardized business execution
- Improved data consistency
- Automatic documentation
- Faster customer response
- Easier maintenance and future enhancement

---

# Summary

The Autonomous Sales Lead Qualification Agent uses Microsoft Copilot Studio together with Microsoft 365 connector tools to automate lead qualification from email receipt through final communication.

Each tool performs a clearly defined responsibility within the workflow, enabling a modular, reliable, and maintainable solution while ensuring compliance with business rules and organizational governance.