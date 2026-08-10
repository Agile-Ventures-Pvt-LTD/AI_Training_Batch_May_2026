
# Solution Summary

## Project Information

| Field | Details |
|---|---|
| Project ID | P2-003 |
| Project Name | NovaWorks Sales Lead Qualification Agent s |
| Platform | Microsoft Copilot Studio |
| Organization | NovaWorks Technologies Pvt. Ltd. |
| Agent Type | Autonomous Event-Driven AI Agent |
| Data Type | Synthetic Sales Data |

---

# 1. Business Problem

NovaWorks Technologies receives sales inquiries through a monitored Microsoft Outlook mailbox. The existing sales qualification process requires sales operations teams to manually review every incoming email, extract customer details, validate product requirements, determine business value, assign sales representatives, create qualification reports, and communicate with prospects.

This manual approach creates several operational challenges:

- High time consumption for repetitive lead processing.
- Inconsistent qualification decisions.
- Manual duplicate checking.
- Delayed response to qualified opportunities.
- Difficulty maintaining accurate lead records.
- Limited audit visibility of qualification decisions.

The Autonomous Sales Lead Qualification Agent addresses these challenges by automating the initial qualification workflow while maintaining controlled decision boundaries.

---

# 2. Solution Objective

The objective of the agent is to provide autonomous first-level sales qualification by:

- Monitoring incoming sales lead emails automatically.
- Identifying valid sales opportunities.
- Extracting structured lead information.
- Validating business data against reference tables.
- Calculating qualification scores.
- Assigning lead classifications.
- Routing leads to appropriate sales owners.
- Generating qualification reports.
- Updating operational records.
- Escalating uncertain cases for human review.

---

# 3. Solution Architecture

The solution is implemented completely within Microsoft Copilot Studio using autonomous triggers, generative orchestration, and Microsoft 365 connectors.

## High-Level Architecture


```
                Microsoft Outlook
                       |
                       |
          New Email Event Trigger
          (When a new email arrives V3)
                       |
                       v
          Microsoft Copilot Studio Agent
                       |
    -------------------------------------
    |                                   |

Generative Orchestration          Business Instructions
|                                   |
-------------------------------------
|
v
Lead Processing Workflow
|
-------------------------------------
|          |          |             |
v          v          v             v
Excel      Word       Outlook       Decision
Connector Connector Connector       Engine
|          |          |             |
v          v          v             v
Lead Register  Reports  Notifications  Classification

```

---

# 4. Autonomous Processing Flow

## Step 1: Email Validation

The agent receives an Outlook event when a new email arrives.

The trigger filter ensures that only emails containing:

```

[P2-003 LEAD]

```

in the subject are processed.

Non-project emails are ignored.

---

## Step 2: Information Extraction

The agent extracts:

### Source Information

- Message ID
- Sender name
- Sender email
- Lead source
- Received date

### Contact Information

- Contact name
- Job title
- Decision role

### Organization Information

- Company name
- Country
- Territory
- Industry
- Company size

### Opportunity Information

- Product interest
- Business requirement
- Budget
- Purchase timeline

### Assessment Information

- Missing information
- Confidence score
- Product fit
- Risk flags

Missing values are stored as:

```

Unknown

```

---

# 5. Duplicate Detection Logic

The agent prevents duplicate lead creation using a multi-level validation process.

## Detection Sequence

```

Check Message ID
|
v
Exact Match Found?
|
Yes -------> Duplicate
|
No
|
Compare:
Sender Email
Company Name
Product Interest
|
v
Potential Match?
|
Yes -------> Update Existing Record
|
No
|
Create New Lead

```

Duplicate records:

- Update existing Excel rows.
- Do not create new reports.
- Do not send duplicate acknowledgements.
- Record classification as Duplicate.

---

# 6. Qualification Engine

The qualification engine evaluates leads using predefined business rules.

Scoring dimensions:

| Factor | Maximum Score |
|---|---:|
| Product Fit | 20 |
| Budget Viability | 20 |
| Purchase Timeline | 15 |
| Decision Role | 15 |
| Company Size | 10 |
| Territory | 10 |
| Lead Source | 5 |
| Completeness | 5 |
| Total | 100 |

---

# 7. Classification Logic

The agent assigns one of the following outcomes:

| Classification | Behaviour |
|---|---|
| Hot | Create record, report, owner notification, acknowledgement |
| Qualified | Create record, report, owner notification, acknowledgement |
| Nurture | Store lead and communicate limited response |
| Low Priority | Store record without report generation |
| Additional Information Required | Request missing details |
| Human Review Required | Escalate to sales operations |
| Duplicate | Update existing record only |
| Not a Sales Lead | Stop sales processing |

---

# 8. Integrated Tools

## Outlook Connector

Used for:

- Receiving lead emails.
- Sending acknowledgements.
- Requesting missing information.
- Sending internal notifications.

---

## Excel Online (Business)

Used for:

- Reading qualification rules.
- Validating products.
- Mapping territories.
- Assigning owners.
- Creating and updating lead records.

Required tables:

- LeadsRegisterTable
- QualificationRulesTable
- TerritoryOwnersTable
- ProductCatalogTable
- SalesOwnersTable
- ActionMatrixTable

---

## Word Online (Business)

Used for:

- Generating qualification reports.

Reports are created only for:

- Hot leads.
- Qualified leads.

---

# 9. Human Review Boundary

The agent does not make autonomous decisions in uncertain situations.

Human review is required for:

- Unknown products.
- Unmapped territories.
- Competitor risks.
- Low confidence analysis.
- Conflicting information.
- Tool failures.

The agent records the exception and notifies Sales Operations.

---

# 10. Expected Outcomes

The implemented solution provides:

- Faster lead processing.
- Consistent qualification decisions.
- Reduced manual effort.
- Improved sales response time.
- Better lead tracking.
- Auditable autonomous decision-making.
- Controlled AI adoption with human oversight.

---

# 11. Implementation Benefits

| Area | Improvement |
|---|---|
| Lead Processing | Automated first-level qualification |
| Accuracy | Rule-based scoring and validation |
| Efficiency | Reduced manual review workload |
| Transparency | Recorded decisions and actions |
| Scalability | Handles multiple incoming leads |
| Safety | Human review for uncertain cases |

