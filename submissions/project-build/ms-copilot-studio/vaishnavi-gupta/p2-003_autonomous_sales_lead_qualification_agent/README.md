# NovaWorks Autonomous Sales Lead Qualification Agent

## Project Overview

The NovaWorks Autonomous Sales Lead Qualification Agent is an AI-powered business automation solution developed using Microsoft Copilot Studio. The agent automates the complete sales lead qualification process by analyzing incoming customer enquiries, validating business information, consulting organizational policies and operational data, generating qualification reports, updating operational records, assigning sales representatives, and sending professional email communications.

The solution is designed to minimize manual effort, ensure consistent decision-making, improve response times, and maintain compliance with NovaWorks' internal qualification policies.

---

# Business Problem

Organizations receive a large number of sales enquiries every day. Manually reviewing every lead requires considerable time and often results in:

- Slow response times
- Inconsistent qualification decisions
- Duplicate lead records
- Manual assignment of sales representatives
- Delayed follow-ups
- Human errors in documentation

NovaWorks required an intelligent solution capable of automating these repetitive activities while ensuring that every qualification decision follows company policies.

---

# Project Objectives

The primary objectives of this project are:

- Automatically process incoming sales enquiries.
- Extract structured business information from emails.
- Validate all required customer information.
- Identify duplicate leads.
- Determine lead qualification status.
- Assign the appropriate Territory Owner.
- Assign the appropriate Sales Owner.
- Update operational records.
- Generate standardized Lead Qualification Reports.
- Send professional customer acknowledgement emails.
- Maintain complete compliance with NovaWorks policies.

---

# Solution Architecture

The solution is built using Microsoft Copilot Studio with Microsoft 365 connectors.

---

# Technologies Used

## AI Platform

- Microsoft Copilot Studio

## Microsoft 365 Connectors

- Excel Online (Business)
- Microsoft Word Online (Business)
- Office 365 Outlook

## Storage

- OneDrive for Business

## Knowledge Sources

- Markdown (.md) files

---

# Knowledge Base

The project uses three mandatory knowledge documents.

## 1. NovaWorks Sales Lead Qualification and Autonomy Policy

Contains:

- Lead qualification policies
- Business rules
- Validation logic
- Escalation conditions
- Autonomy limits

---

## 2. Lead Qualification Report Structure

Defines the exact structure of the generated report.

Includes:

- Lead Summary
- Validation Results
- Qualification Decision
- Assigned Owner
- Business Justification
- Recommended Next Action

---

## 3. Autonomous Email Content Requirements

Defines:

- Customer acknowledgement format
- Internal notification format
- Professional writing standards
- Communication restrictions
- Business tone guidelines

---

# Operational Data

The operational data is maintained in an Excel workbook.

## Workbook

P2-003_Sales_Lead_Operational_Data.xlsx

The workbook contains the following tables.

## LeadsRegisterTable

Stores all processed leads.

Fields include:

- Lead ID
- Company
- Contact
- Product
- Territory
- Assigned Owner
- Qualification Status
- Notes
- Timestamp

---

## QualificationRulesTable

Contains:

- Qualification criteria
- Budget thresholds
- Timeline requirements
- Decision rules

---

## ProductCatalogTable

Contains:

- Supported products
- Product identifiers
- Product availability

---

## TerritoryOwnerTable

Maps:

- Country
- Region
- Territory
- Territory Owner

---

## SalesOwnersTable

Contains:

- Sales representatives
- Assigned territories
- Product responsibility

---

## ActionMatrixTable

Defines:

- Assign to Sales
- Reject
- Escalate
- Manual Review
- Request Additional Information

---

# Agent Workflow

The agent performs the following workflow.

Step 1

Receive customer email.

↓

Step 2

Extract lead information.

↓

Step 3

Validate mandatory fields.

↓

Step 4

Search Lead Register.

↓

Step 5

Retrieve Qualification Rules.

↓

Step 6

Validate Product.

↓

Step 7

Determine Territory.

↓

Step 8

Assign Sales Owner.

↓

Step 9

Determine Qualification Status.

↓

Step 10

Update Lead Register.

↓

Step 11

Generate Qualification Report.

↓

Step 12

Send Customer Email.

↓

Step 13

Complete Processing.

---

# Information Extracted

The agent extracts:

- Company Name
- Contact Name
- Email Address
- Phone Number
- Country
- Region
- Territory
- Industry
- Requested Product
- Requested Service
- Budget
- Timeline
- Business Need
- Use Case
- Decision Maker
- Employee Count
- Current Solution
- Additional Notes

---

# Qualification Decisions

The agent supports three outcomes.

## Qualified

Lead satisfies all qualification rules.

Next action:

Assign to Sales.

---

## Needs More Information

Required information is missing.

Next action:

Request clarification.

---

## Rejected

Lead does not satisfy qualification rules.

Next action:

Reject according to policy.

---

# Connectors Used

## Excel Online (Business)

Used for:

- List Rows
- Add Row
- Update Row
- Get Row

---

## Microsoft Word Online

Used for:

- Create Lead Qualification Report

---

## Office 365 Outlook

Used for:

- Send acknowledgement email
- Send clarification email
- Send rejection email
- Send internal notification

---

# Business Rules

The agent always:

- Validates customer information.
- Checks duplicate records.
- Uses qualification rules.
- Validates products.
- Assigns correct owners.
- Generates standardized reports.
- Sends professional emails.

The agent never:

- Fabricates information.
- Modifies qualification rules.
- Exposes confidential operational data.
- Makes business commitments.
- Skips validation.

---

# Error Handling

If an error occurs:

- Stop processing.
- Explain the error.
- Escalate for manual review.
- Do not continue with incomplete information.

---

# Testing Scenarios

## Scenario 1

Qualified Lead

Expected Result

- Qualified
- Excel updated
- Report generated
- Email sent

---

## Scenario 2

Missing Information

Expected Result

- Request clarification
- No qualification

---

## Scenario 3

Duplicate Lead

Expected Result

- Existing record updated
- No duplicate created

---

## Scenario 4

Unsupported Product

Expected Result

- Follow Action Matrix
- Reject or Escalate

---

# Assumptions

- Operational Excel workbook is accessible.
- Connectors are authenticated.
- Knowledge documents are available.
- Microsoft 365 services are operational.
- Email input follows standard business formats.

---

# Limitations

- Depends on Microsoft 365 connectors.
- Requires correctly formatted Excel tables.
- Does not make decisions beyond documented policies.
- Cannot qualify leads with insufficient information.
- Does not use external web data.
- Cannot modify business rules autonomously.

---

# Security Considerations

- Uses authenticated Microsoft 365 connectors.
- Does not expose confidential operational tables.
- Does not reveal internal decision logic.
- Stores operational data only in authorized locations.
- Follows least-privilege access principles.

---

# Future Enhancements

Potential improvements include:

- CRM integration (Dynamics 365, Salesforce)
- Microsoft Teams notifications
- Power BI dashboard integration
- Automatic meeting scheduling
- Lead scoring using predictive AI
- Multi-language email support
- Integration with ERP systems
- Analytics and reporting dashboards
- Human approval workflow for high-value leads

---

# Project Outcome

The NovaWorks Autonomous Sales Lead Qualification Agent successfully automates the end-to-end lead qualification lifecycle by combining Microsoft Copilot Studio, Microsoft 365 connectors, structured operational data, and organizational knowledge. The solution improves operational efficiency, reduces manual effort, ensures policy compliance, standardizes customer communication, and provides a scalable foundation for intelligent sales automation.


# Author
Vaishnavi Gupta