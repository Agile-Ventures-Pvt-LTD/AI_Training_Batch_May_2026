# Tool Design

## P2-003 Autonomous Sales Lead Qualification Agent

## Purpose

This document defines the Microsoft Copilot Studio connector tool architecture for the **NovaWorks Autonomous Sales Lead Qualification Agent**. The agent uses Microsoft 365 connectors to perform autonomous lead qualification, duplicate detection, operational data retrieval, Excel record management, Word report generation, and Outlook communications.

The design focuses on deterministic tool execution, parameter binding, connector reliability, and auditable autonomous processing.

---

# Tool architecture overview

The agent uses three connector groups.

| Connector                           | Purpose                                              |
| ----------------------------------- | ---------------------------------------------------- |
| Office 365 Outlook                  | Trigger and email communications                     |
| Excel Online (Business)             | Reference data retrieval and lead record management  |
| Word Online / OneDrive for Business | Qualification report generation and document storage |

All tools execute within the Microsoft 365 ecosystem.

---

# Tool orchestration sequence

The agent executes tools in a strict deterministic order.

```text
Outlook Trigger
       |
       v
Read Lead Register
       |
       v
Duplicate Detection
       |
       v
Read Qualification Rules
       |
       v
Read Territory Owners
       |
       v
Read Product Catalog
       |
       v
Calculate Score
       |
       v
Add or Update Lead Record
       |
       +------> Create Word Report
       |
       +------> Reply to Prospect
       |
       +------> Send Internal Alert
```

No write operation occurs before duplicate validation completes.

---

# Tool 1: Excel Online (Business) — List rows present in a table

## Purpose

Retrieve historical lead records for duplicate detection and read operational reference tables used for scoring, normalization, territory routing, and owner assignment.

## Connector

Excel Online (Business)

## Execution stage

Read

## Configuration

| Parameter        | Value / Binding                         |
| ---------------- | --------------------------------------- |
| Location         | OneDrive for Business                   |
| Document Library | OneDrive                                |
| File             | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table            | Dynamic                                 |
| Filter Query     | Dynamic OData query                     |

## Supported tables

* LeadsRegisterTable
* QualificationRulesTable
* TerritoryOwnersTable
* ProductCatalogTable
* SalesOwnersTable
* ActionMatrixTable

## Input bindings

| Input            | Source          |
| ---------------- | --------------- |
| Message ID       | Outlook trigger |
| Sender email     | Outlook trigger |
| Company name     | AI extraction   |
| Product interest | AI extraction   |

## Example filter query

```text
Source_Message_ID eq '{Message_ID}'
```

## Output

Returns matching Excel rows used for:

* exact duplicate detection
* probable duplicate detection
* scoring rules
* territory mapping
* product normalization
* owner assignment

## Action boundary

This tool performs **read-only operations**.

It must execute before any record creation or update.

---

# Tool 2: Excel Online (Business) — Add a row into a table

## Purpose

Create a new lead record in the operational lead register after duplicate detection and qualification scoring are completed.

## Connector

Excel Online (Business)

## Execution stage

Write

## Configuration

| Parameter        | Value                                   |
| ---------------- | --------------------------------------- |
| Location         | OneDrive for Business                   |
| Document Library | OneDrive                                |
| File             | P2-003_Sales_Lead_Operational_Data.xlsx |
| Table            | LeadsRegisterTable                      |
| Row              | Dynamic JSON payload                    |

## Input payload

The agent constructs a structured lead record.

### Core fields

* Lead_ID
* Source_Message_ID
* Received_Date
* Sender_Email
* Contact_Name
* Contact_Email
* Company_Name
* Country_Region
* Territory
* Company_Size
* Industry

### Opportunity fields

* Product_Interest
* Business_Need
* Stated_Budget
* Purchase_Timeline
* Decision_Role

### Qualification fields

* Qualification_Score
* Classification
* Confidence
* Assigned_Sales_Owner
* Sales_Owner_Email
* Processing_Status

## Lead ID format

```text
LEAD-{YYYYMMDD}-{INDEX}
```

## Output

Creates a new lead record and returns the inserted row.

## Action boundary

This tool must **never execute** when:

* an exact duplicate exists
* a probable duplicate has been confirmed
* duplicate validation has not completed

---

# Tool 3: Excel Online (Business) — Update a row

## Purpose

Update existing lead records with report locations, processing status, duplicate flags, owner changes, and audit information.

## Connector

Excel Online (Business)

## Execution stage

Write

## Configuration

| Parameter  | Value                        |
| ---------- | ---------------------------- |
| Table      | LeadsRegisterTable           |
| Key Column | Source_Message_ID or Lead_ID |
| Key Value  | Dynamic                      |
| Row        | Updated field object         |

## Update scenarios

* duplicate detected
* Word report generated
* processing completed
* owner reassigned
* additional information received
* human review initiated

## Typical updated fields

* Report_File_Path
* Processing_Status
* Last_Action
* Duplicate_Flag
* Assigned_Sales_Owner
* Classification

## Output

Returns the updated lead record.

## Action boundary

This tool must only update existing records.

It must not create new records.

---

# Tool 4: Word Online / OneDrive — Create file

## Purpose

Generate a structured Microsoft Word qualification report for qualified sales opportunities.

## Connector

Word Online / OneDrive for Business

## Execution stage

Document generation

## Configuration

| Parameter    | Value                                    |
| ------------ | ---------------------------------------- |
| Folder Path  | /Lead_Reports/                           |
| File Name    | Lead_Qualification_Report_{Lead_ID}.docx |
| File Content | Dynamic formatted document               |

## Report content

The generated report includes:

* report metadata
* contact information
* organization profile
* opportunity summary
* qualification score
* score breakdown
* classification
* confidence assessment
* duplicate result
* owner assignment
* risk flags
* recommended action
* autonomous action log

## Output

Creates a Word document and returns the file path.

## Execution condition

Execute **only when**:

* Classification = Hot
* Classification = Qualified

## Must not execute

* Duplicate
* Nurture
* Low Priority
* Additional Information Required
* Human Review Required
* Not a Sales Lead

---

# Tool 5: Office 365 Outlook — Reply to email (V3)

## Purpose

Send contextual responses directly to the original prospect.

## Connector

Office 365 Outlook

## Execution stage

External communication

## Configuration

| Parameter  | Value   |
| ---------- | ------- |
| Message ID | Dynamic |
| Body       | Dynamic |
| Reply All  | false   |

## Mandatory parameter binding

Both parameters are required.

### Message ID

Must be populated from the Outlook trigger.

### Body

Must contain a fully formatted response.

## Response types

* acknowledgement
* missing-information request
* nurture response
* follow-up guidance

## Output

Returns Outlook delivery confirmation.

## Action boundary

This tool must not send:

* qualification confirmations for Human Review Required
* duplicate acknowledgements
* unsupported commercial commitments

---

## Human review routing

Human Review Required notifications must be sent exclusively to:

```text
salesops@novaworks.example
```

External qualification communication must be withheld.

---

# Parameter binding rules

## Reply tool

Required:

* Message ID
* Body

Missing either parameter must prevent execution.

## Excel lookup

Use exact column names:

* Source_Message_ID
* Sender_Email
* Company_Name

Case-sensitive matching is required.

## Word report

Execute only for:

* Hot
* Qualified

## Internal alerts

Route Human Review Required cases only to Sales Operations.

---

# Tool execution matrix

| Classification                  | Add Row | Update Row | Word | Reply       | Internal Email |
| ------------------------------- | ------- | ---------- | ---- | ----------- | -------------- |
| Hot                             | Yes     | Optional   | Yes  | Yes         | Yes            |
| Qualified                       | Yes     | Optional   | Yes  | Yes         | Yes            |
| Nurture                         | Yes     | Optional   | No   | Yes         | No             |
| Low Priority                    | Yes     | Optional   | No   | Conditional | No             |
| Additional Information Required | Yes     | Yes        | No   | Yes         | No             |
| Human Review Required           | Yes     | Yes        | No   | No          | Yes            |
| Duplicate                       | No      | Yes        | No   | No          | No             |
| Not a Sales Lead                | No      | No         | No   | No          | No             |

---

# Error handling

## Retry policy

One controlled retry is permitted.

## Failure handling

If retry fails:

* stop downstream dependent tools
* record the failure
* notify Sales Operations
* do not report success

## Protected operations

Do not execute:

* Word generation after Excel failure
* external email after classification uncertainty
* owner notification before owner assignment

---

# Security controls

All connector actions operate within Microsoft 365 permissions.

The agent may access only:

* configured Outlook mailbox
* approved Excel workbook
* approved Word report folder
* authorized OneDrive storage

No external APIs or third-party systems are accessed.

---

# Monitoring

Tool execution is monitored through Copilot Studio run history.

Tracked events:

* tool execution time
* success or failure
* retry count
* parameter validation
* connector response
* dependency failures

---

# Design rationale

The tool architecture separates **read operations**, **decision support**, **record management**, **document generation**, and **communication**.

Strict parameter binding prevents runtime connector errors, duplicate validation ensures idempotency, and conditional execution boundaries prevent unauthorized or inappropriate autonomous actions.

This design provides deterministic, auditable, and production-ready Microsoft Copilot Studio orchestration.

---

# PRD compliance

| Requirement                 | Status   |
| --------------------------- | -------- |
| Outlook connector tools     | Complete |
| Excel connector tools       | Complete |
| Word connector tool         | Complete |
| Connector parameter schemas | Complete |
| Tool input mapping          | Complete |
| Tool output mapping         | Complete |
| Execution sequence          | Complete |
| Action boundaries           | Complete |
| Parameter binding rules     | Complete |
| Error handling              | Complete |
| Human review routing        | Complete |

---

# Final status

The Microsoft Copilot Studio tool architecture has been fully defined with connector specifications, parameter schemas, execution sequencing, payload design, validation rules, and autonomous action boundaries.

The implementation satisfies the P2-003 PRD requirements for connector configuration, tool orchestration, duplicate-safe processing, document generation, internal and external communication, and enterprise governance.
