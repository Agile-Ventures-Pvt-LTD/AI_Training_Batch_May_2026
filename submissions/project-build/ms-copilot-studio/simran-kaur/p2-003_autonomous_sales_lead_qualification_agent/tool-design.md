
# Tool Design

## Agent Name
**NovaWorks Sales Lead Qualification Agent s**

---

# Tool Overview

The agent uses Microsoft 365 connector tools in Copilot Studio to read data, update records, generate reports, and communicate outcomes.

---

# Configured Tools

| Tool | Purpose | Usage |
|---|---|---|
| Get Lead Records | Duplicate detection | Checks existing lead records |
| Get Qualification Rules | Scoring logic | Retrieves qualification criteria |
| Get Territory Owners | Territory mapping | Assigns sales territory |
| Get Product Catalog | Product validation | Confirms supported products |
| Get Sales Owners | Owner assignment | Retrieves sales representative |
| Get Action Matrix | Action mapping | Determines required actions |
| Create Lead Record | Record creation | Adds new qualified leads |
| Update Lead Record | Record update | Updates duplicates/status |
| Generate Qualification Report | Documentation | Creates Word reports |
| Send Lead Acknowledgement | External communication | Sends lead response |
| Request Missing Information | Data collection | Requests incomplete details |
| Notify Assigned Sales Owner | Internal alert | Informs sales owner |
| Notify Sales Operations | Escalation | Handles exceptions |

---

# Tool Execution Sequence

```

Get Lead Records
|
Get Qualification Rules
|
Get Territory Owners
|
Get Product Catalog
|
Get Sales Owners
|
Get Action Matrix
|
Create/Update Record
|
Generate Report
|
Send Notifications

```

---

# Tool Boundaries

## Allowed

- Reading operational tables.
- Creating and updating lead records.
- Generating qualification reports.
- Sending approved communications.

## Restricted

The agent must not:

- Access unsupported data sources.
- Make unsupported business commitments.
- Send qualification decisions for human-review cases.
- Claim successful execution without tool confirmation.

---

# Input and Output Summary

| Tool Category | Input | Output |
|---|---|---|
| Excel Tools | Lead details/reference data | Records and rules |
| Word Tool | Qualification details | Report document |
| Outlook Tools | Lead information | Emails/notifications |

---

# Status

| Component | Status |
|---|---|
| Excel Tools | Configured |
| Word Tool | Configured |
| Outlook Tools | Configured |
| Tool Sequence | Implemented |


