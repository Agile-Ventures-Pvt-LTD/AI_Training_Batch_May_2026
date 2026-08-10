# Tool Implementation

## Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower integrates Microsoft 365 tools to automate data retrieval, investigation management, report generation, and stakeholder communication. Each tool is assigned to a specific agent to maintain clear ownership and prevent overlapping responsibilities.

---

# Tool Architecture

| Tool Type | Platform |
|------------|----------|
| Data Management | Excel Online (Business) |
| Report Generation | Microsoft Word |
| Email Notifications | Outlook |
| Microsoft Guidance | Microsoft Learn MCP |

---

# Supervisor Tools

## 1. Supervisor Customer Complaints

**Platform:** Excel Online (Business)

**Action:** List rows present in a table

**Purpose**

- Retrieve customer complaint records.
- Start investigation workflow.
- Validate Complaint IDs.

---

## 2. Supervisor Quality Rules

**Platform:** Excel Online (Business)

**Action:** List rows present in a table

**Purpose**

- Retrieve quality rules.
- Apply deterministic investigation policies.

---

## 3. Supervisor Quality Incidents Add

**Platform:** Excel Online (Business)

**Action:** Add a row into a table

**Purpose**

- Create a new Quality Incident record.
- Store investigation metadata.

---

## 4. Supervisor Quality Incident Update

**Platform:** Excel Online (Business)

**Action:** Update a row

**Purpose**

- Update investigation status.
- Store classification.
- Record investigation rationale.

---

## 5. Supervisor CAPA Register

**Platform:** Excel Online (Business)

**Action:** List rows present in a table

**Purpose**

- Read CAPA history.
- Check overdue CAPA records.

---

## 6. Supervisor Update a Row

**Platform:** Excel Online (Business)

**Action:** Update a row

**Purpose**

- Update operational Excel tables after investigation completion.

---

## 7. Create a Microsoft Word Document

**Platform:** Microsoft Word Online

**Purpose**

Generate the final Quality Investigation Report containing:

- Complaint Information
- Investigation Findings
- Specialist Analysis
- Final Classification
- CAPA Details (if applicable)
- Investigation Summary

---

## 8. Send an Email (V2)

**Platform:** Outlook

**Purpose**

Notify stakeholders after investigation completion.

Typical recipients include:

- Quality Manager
- Product Team
- Customer Support
- Investigation Owner

---

# Specialist Agent Tools

| Agent | Tool | Purpose |
|---------|------|---------|
| Complaint Pattern Specialist | Customer Complaints | Complaint trend and pattern analysis |
| Returns Specialist | Returns Register | Return-rate analysis |
| Product/Batch Specialist | Product Master, Batch Register | SKU and batch validation |
| Customer Impact Specialist | Customer Complaints | Customer impact assessment |
| Safety Specialist | Customer Complaints | Safety evaluation |
| CAPA Specialist | CAPA Register | CAPA creation and tracking |
| M365 Guidance Specialist | Microsoft Learn MCP | Microsoft platform guidance |

---

# Tool Execution Flow

```text
Quality Supervisor
       │
       ▼
Customer Complaints
       │
       ▼
Custom Topics
       │
       ▼
Specialist Agents
       │
       ▼
Quality Decision
       │
       ▼
Quality Incidents Update
       │
       ▼
Word Report
       │
       ▼
Outlook Email
```

---

# Tool Ownership Principles

- Each tool is owned by a single agent.
- Specialist agents use only their assigned tools.
- The Quality Supervisor controls workflow execution.
- Operational updates are performed only by the Supervisor.
- Microsoft Learn MCP is accessed only through the M365 Guidance Specialist.

---

# Testing Summary

| Tool | Test Objective | Result |
|------|----------------|--------|
| Customer Complaints | Read complaint records | Passed |
| Quality Rules | Retrieve investigation rules | Passed |
| Quality Incidents Add | Create incident | Passed |
| Quality Incident Update | Update investigation | Passed |
| CAPA Register | Retrieve CAPA records | Passed |
| Word Document | Generate report | Passed |
| Outlook Email | Send notification | Passed |
| Microsoft Learn MCP | Retrieve official guidance | Passed |

---

# Error Handling

| Scenario | Action |
|----------|--------|
| Excel table unavailable | Return error and stop affected workflow |
| Word generation fails | Log failure and retain investigation record |
| Email fails | Preserve report and notify for manual follow-up |
| MCP unavailable | Return graceful failure message without affecting investigation |

---

# Benefits

- Automated investigation workflow
- Centralized operational updates
- Standardized report generation
- Automated stakeholder notifications
- Clear tool ownership
- Improved traceability and governance

---

# Conclusion

The Microsoft 365 tool implementation provides reliable integration with Excel, Word, Outlook, and Microsoft Learn MCP. By assigning dedicated tool ownership to the Quality Supervisor and specialist agents, the solution maintains a governed, scalable, and auditable quality investigation process.