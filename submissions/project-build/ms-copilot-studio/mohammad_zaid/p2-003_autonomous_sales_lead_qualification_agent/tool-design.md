
# Tool Design

# Project Information

| Property               | Value                                                               |
| ---------------------- | ------------------------------------------------------------------- |
| Project                | P2-003 – NovaWorks Sales Lead Qualification Agent                  |
| Platform               | Microsoft Copilot Studio                                            |
| Orchestration          | Generative Orchestration                                            |
| Connector Technologies | Excel Online (Business), Word Online (Business), Office 365 Outlook |

---

# Purpose

The NovaWorks Sales Lead Qualification Agent uses Microsoft Copilot Studio tools to perform business actions that cannot be completed through AI reasoning alone.

Each tool is responsible for a single operational task and is invoked by Generative Orchestration based on the current stage of the workflow.

The tools are intentionally designed with clear responsibilities to improve maintainability, reduce ambiguity, and support deterministic execution.

---

# Tool Architecture

The agent contains the following operational tools.

| Tool                               | Connector               | Action                                                  |
| ---------------------------------- | ----------------------- | ------------------------------------------------------- |
| Read Lead Reference Data           | Excel Online (Business) | List rows present in a table                            |
| Create Lead Record                 | Excel Online (Business) | Add a row into a table                                  |
| Update Lead Record                 | Excel Online (Business) | Update a row using a key column                         |
| Generate Lead Qualification Report | Word Online (Business)  | Create a Microsoft Word document with the given content |
| Send Email                         | Office 365 Outlook      | Send an email (V2)                                      |

---

# Tool 1 – Read Lead Reference Data

## Purpose

Reads operational and reference data from the Sales Lead Operational workbook before any business decision is made.

The tool provides access to business reference information required for duplicate detection, qualification, owner assignment, territory validation, and operational processing.

---

## Connector

Excel Online (Business)

---

## Action

List rows present in a table

---

## Workbook

P2-003_Sales_Lead_Operational_Data.xlsx

---

## Tables Accessed

The tool may read the following operational tables:

- LeadsRegisterTable
- QualificationRulesTable
- TerritoryOwnersTable
- ProductCatalogTable
- SalesOwnersTable
- ActionMatrixTable

The table selection is determined dynamically based on the processing requirement.

---

## Inputs

| Input      | Source                                 |
| ---------- | -------------------------------------- |
| Workbook   | Configured OneDrive workbook           |
| Table Name | Determined by Generative Orchestration |

---

## Outputs

Returns the requested operational rows from the selected table.

---

## Action Boundary

### Use When

- Reading existing lead records
- Performing duplicate detection
- Retrieving qualification rules
- Looking up territories
- Determining sales owner
- Reading operational reference information

### Do Not Use

- Creating records
- Updating records
- Generating reports
- Sending emails

---

# Tool 2 – Create Lead Record

## Purpose

Creates a new operational lead record after the lead has successfully completed validation and has been confirmed as a new lead.

---

## Connector

Excel Online (Business)

---

## Action

Add a row into a table

---

## Workbook

P2-003_Sales_Lead_Operational_Data.xlsx

---

## Target Table

LeadsRegisterTable

---

## Inputs

The tool receives structured lead information produced during processing, including:

- Contact details
- Company information
- Product interest
- Qualification results
- Classification
- Assigned owner
- Processing status
- Report location

---

## Outputs

Creates a new operational lead record.

---

## Action Boundary

### Use When

- Lead is confirmed as new.
- Duplicate detection has completed.
- Qualification has completed.

### Do Not Use

- Updating existing records.
- Duplicate leads.

---

# Tool 3 – Update Lead Record

## Purpose

Updates an existing operational lead after it has been identified through duplicate detection or when additional processing information becomes available.

---

## Connector

Excel Online (Business)

---

## Action

Update a row using a key column

---

## Workbook

P2-003_Sales_Lead_Operational_Data.xlsx

---

## Target Table

LeadsRegisterTable

---

## Key Column

Lead_ID

---

## Key Value

Provided dynamically from the output of the **Read Lead Reference Data** tool after locating the existing lead.

---

## Inputs

- Lead_ID
- Updated qualification information
- Processing status
- Assigned owner
- Report path
- Additional operational updates

---

## Outputs

Updates the selected lead record.

---

## Action Boundary

### Use When

- Existing lead located.
- Duplicate detected.
- Operational information changes.
- Report path must be stored.

### Do Not Use

- Creating new records.

---

# Tool 4 – Generate Lead Qualification Report

## Purpose

Creates a professional Lead Qualification Report summarizing the outcome of lead processing.

The report follows the required report structure supplied with the project dataset.

---

## Connector

Word Online (Business)

---

## Action

Create a Microsoft Word document with the given content

---

## Inputs

The report content is generated dynamically using:

- Lead details
- Company information
- Qualification score
- Classification
- Assigned owner
- Decision confidence
- Risk flags
- Recommendations

---

## Outputs

A Microsoft Word document containing the Lead Qualification Report.

---

## Action Boundary

### Use When

- Qualification has completed.
- Report is required for operational processing.

### Do Not Use

- Before qualification.
- Before owner assignment.
- Before duplicate detection.

---

# Tool 5 – Send Email

## Purpose

Sends business communications as part of the autonomous workflow.

The communication type depends on the processing outcome.

---

## Connector

Office 365 Outlook

---

## Action

Send an email (V2)

---

## Communication Types

- Customer acknowledgement
- Request for additional information
- Internal sales notification

---

## Inputs

| Input      | Description                      |
| ---------- | -------------------------------- |
| Recipient  | Customer or internal sales owner |
| Subject    | Generated dynamically            |
| Email Body | Generated dynamically            |
| Importance | Normal                           |

---

## Outputs

Successfully delivered Outlook email.

---

## Action Boundary

### Use When

- Customer acknowledgement required.
- Additional information required.
- Internal notification required.

### Do Not Use

- Sending unrelated communications.
- Sending emails outside the lead qualification workflow.

---

# Tool Interaction Flow

The tools are executed according to the business workflow.

```
Outlook Trigger
       │
       ▼
Read Lead Reference Data
       │
       ▼
Duplicate Detection
       │
       ├──────────── Existing Lead
       │                     │
       │                     ▼
       │             Update Lead Record
       │
       ▼
New Lead
       │
       ▼
Qualification
       │
       ▼
Owner Assignment
       │
       ▼
Generate Lead Qualification Report
       │
       ▼
Create Lead Record
       │
       ▼
Send Email
```

---

# Tool Design Principles

The tools were designed according to the following principles:

- Single responsibility for each tool.
- Clear action boundaries.
- No overlapping responsibilities.
- Separation of AI reasoning and operational actions.
- Connector-specific implementation.
- Reusable operational components.
- Compatibility with Generative Orchestration.

---

# Security Considerations

The tools do not store or expose:

- Passwords
- Secrets
- Access tokens
- API keys
- Personal credentials

Authentication is handled through Microsoft 365 connector connections configured within Copilot Studio.

---

# Conclusion

The tool design provides a modular and maintainable implementation for the NovaWorks Sales Lead Qualification Agent. Each tool has a clearly defined responsibility, explicit action boundaries, and integrates with Microsoft 365 services through secure connector authentication.

This design enables Generative Orchestration to invoke the appropriate operational capability while maintaining consistent business processing and minimizing unnecessary complexity.
