# tool-design.md

# Tool Design

## Overview

The Autonomous Sales Lead Agent uses a modular tool-based architecture in Microsoft Copilot Studio. Each tool performs a single business function, allowing the agent to execute the lead qualification workflow in a structured, maintainable, and reusable manner.

The tools interact with Microsoft Excel, Microsoft Word, and Microsoft Outlook to retrieve data, update records, generate reports, and communicate with customers and internal stakeholders.

---

# Tool Execution Sequence

The agent invokes tools in the following order when processing a valid sales enquiry:

1. Read Lead Register
2. Read Qualification Rules
3. Read Territory Owners
4. Read Product Catalog
5. Read Sales Owners
6. Read Action Matrix
7. Create Lead Record (if new)
8. Update Existing Lead (if duplicate)
9. Generate Qualification Report
10. Send External Acknowledgement
11. Request Missing Information (if required)
12. Notify Sales Operations

---

# Tool Specifications

## 1. Read Lead Register

### Purpose

Retrieves all existing lead records to identify duplicate enquiries.

### Data Source

Microsoft Excel – Lead Register Table

### Inputs

- Customer Name
- Company Name
- Email Address (if available)

### Outputs

- Existing Lead Found
- Lead ID
- Previous Status
- Previous Qualification
- Duplicate Indicator

### Action Boundary

Read-only operation.

---

## 2. Read Qualification Rules

### Purpose

Retrieves business rules used to calculate lead qualification.

### Data Source

Qualification Rules Table

### Inputs

None

### Outputs

- Budget thresholds
- Timeline rules
- Decision-maker weights
- Override rules
- Qualification score ranges

### Action Boundary

Read-only operation.

---

## 3. Read Territory Owners

### Purpose

Determines the responsible territory owner based on the customer location.

### Data Source

Territory Owners Table

### Inputs

- Country

### Outputs

- Territory
- Territory Owner

### Action Boundary

Read-only operation.

---

## 4. Read Product Catalog

### Purpose

Validates the requested product and retrieves supported product information.

### Data Source

Product Catalog Table

### Inputs

- Product Interest

### Outputs

- Product Name
- Product Category
- Product Availability

### Action Boundary

Read-only operation.

---

## 5. Read Sales Owners

### Purpose

Determines the appropriate sales representative responsible for the lead.

### Data Source

Sales Owners Table

### Inputs

- Territory
- Product

### Outputs

- Sales Owner
- Sales Team
- Contact Details

### Action Boundary

Read-only operation.

---

## 6. Read Action Matrix

### Purpose

Determines the business actions required for the calculated lead classification.

### Data Source

Action Matrix Table

### Inputs

- Lead Classification

### Outputs

- Required Actions
- Notification Requirements
- Report Generation Requirement

### Action Boundary

Read-only operation.

---

## 7. Create Lead Record

### Purpose

Creates a new lead in the Lead Register when no duplicate exists.

### Data Source

Lead Register Table

### Inputs

- Customer Information
- Company
- Product
- Budget
- Timeline
- Classification
- Assigned Owner

### Outputs

- Lead Record Created
- Lead Identifier

### Action Boundary

Creates new records only.

---

## 8. Update Existing Lead

### Purpose

Updates an existing lead when a duplicate enquiry is identified.

### Data Source

Lead Register Table

### Inputs

- Existing Lead ID
- Updated Lead Information
- Current Status
- Latest Enquiry Details

### Outputs

- Updated Lead Record
- Updated Status

### Action Boundary

Updates existing records only.

---

## 9. Generate Qualification Report

### Purpose

Creates a structured Microsoft Word report summarizing the lead qualification outcome.

### Data Source

Microsoft Word Online

### Inputs

- Lead Details
- Qualification Score
- Classification
- Assigned Owner
- Business Recommendation

### Outputs

- Word Document
- Qualification Report

### Action Boundary

Generates documentation only.

---

## 10. Send External Acknowledgement

### Purpose

Acknowledges receipt of the customer's enquiry.

### Connector

Office 365 Outlook

### Inputs

- Customer Email
- Customer Name
- Product Interest

### Outputs

- Acknowledgement Email Sent

### Action Boundary

Sends external communications only.

---

## 11. Request Missing Information

### Purpose

Requests mandatory information when the enquiry is incomplete.

### Connector

Office 365 Outlook

### Inputs

- Customer Email
- Missing Fields

### Outputs

- Information Request Email Sent

### Action Boundary

Executed only for incomplete enquiries.

---

## 12. Notify Sales Operations

### Purpose

Notifies the internal Sales Operations team about qualified leads requiring follow-up.

### Connector

Office 365 Outlook

### Inputs

- Lead Summary
- Qualification Outcome
- Assigned Sales Owner
- Recommended Action

### Outputs

- Internal Notification Email Sent

### Action Boundary

Internal communication only.

---

# Tool Dependencies

| Tool | Depends On |
|--------|------------|
| Read Lead Register | Trigger |
| Read Qualification Rules | Trigger |
| Read Territory Owners | Country |
| Read Product Catalog | Product Interest |
| Read Sales Owners | Territory + Product |
| Read Action Matrix | Classification |
| Create Lead Record | Validation Complete |
| Update Existing Lead | Duplicate Found |
| Generate Qualification Report | Qualification Complete |
| Send External Acknowledgement | Successful Processing |
| Request Missing Information | Validation Failure |
| Notify Sales Operations | Qualified Lead |

---

# Error Handling

If a tool encounters an error:

- Processing stops for dependent steps.
- No fabricated information is generated.
- Existing records remain unchanged.
- Errors are logged in the workflow history.
- The agent continues only when safe to do so.

---

# Security and Permissions

The tools operate using Microsoft 365 authenticated connections.

Each tool follows the principle of least privilege:

- Read tools cannot modify data.
- Create tools cannot overwrite existing records.
- Update tools modify only identified records.
- Communication tools only send approved email templates.

No credentials or confidential connection details are stored within the tool definitions.

---

# Design Principles

The tool architecture was designed to achieve:

- Modular implementation
- High maintainability
- Reusability
- Separation of responsibilities
- Secure data handling
- Predictable execution
- Enterprise scalability

---

# Summary

The Autonomous Sales Lead Qualification Agent uses twelve specialized tools that work together to automate lead qualification. Each tool has a clearly defined responsibility, controlled inputs and outputs, and well-defined execution boundaries, enabling reliable, secure, and maintainable business process automation.