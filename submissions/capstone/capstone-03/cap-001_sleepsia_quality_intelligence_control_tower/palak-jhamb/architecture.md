# Architecture

## Sleepsia Quality Intelligence Control Tower

### Overview

The Sleepsia Quality Intelligence Control Tower is implemented using **Microsoft Copilot Studio** with a **Supervisor–Specialist multi-agent architecture**. The solution follows a hierarchical orchestration model where a single **Quality Supervisor** coordinates the complete investigation lifecycle while delegating specialized tasks to domain-specific child agents.

The supervisor also orchestrates four deterministic custom topics that standardize investigation decisions and ensure every incident follows the same enterprise workflow.

---

# Supervisor Agent

The **Quality Supervisor** is the parent orchestration agent responsible for coordinating the complete investigation lifecycle.

It performs:

- Investigation intake and validation
- Child agent orchestration
- Topic orchestration
- Quality classification
- CAPA approval
- Record creation and updates
- Investigation report generation
- Stakeholder notification
- Investigation closure

The supervisor is the **only agent authorized** to:

- Assign the final investigation classification
- Approve CAPA
- Close investigations
- Trigger reassessment
- Update enterprise records

---

# Custom Topics

The supervisor invokes four deterministic custom topics during the investigation lifecycle.

| Topic | Purpose |
|---------|---------|
| **Topic 1 – Incident Intake & Validation** | Validates complaint completeness and determines whether investigation can proceed. |
| **Topic 2 – Quality Investigation Decision** | Applies deterministic quality rules and assigns the official investigation classification. |
| **Topic 3 – CAPA Planning & Ownership** | Generates CAPA ID, containment, corrective actions, preventive actions, owner, target date and validation plan. |
| **Topic 4 – Evidence Update & Selective Reassessment** | Processes new evidence, selectively reruns affected specialists and enforces reassessment limits. |

---

# Specialist Agent Architecture

The supervisor delegates only the required analysis to specialist agents.

## Complaint Pattern Specialist

Responsibilities

- Complaint clustering
- Complaint trends
- Complaint frequency
- Complaint categorization

Uses

- Customer Complaint Records

---

## Returns Specialist

Responsibilities

- Return rate analysis
- Return trend analysis
- Return impact assessment

Uses

- Product Returns
- Sales Summary

---

## Product & Batch Specialist

Responsibilities

- SKU validation
- Batch investigation
- Manufacturing history
- Historical incident analysis

Uses

- Product Information
- Batch Information
- Historical Product Incidents

---

## Customer Impact Specialist

Responsibilities

- Customer impact assessment
- Business impact analysis
- Return impact correlation

Uses

- Complaint Impact Data
- Customer Return Impact Data

---

## Safety Specialist

Responsibilities

- Safety evaluation
- Risk assessment
- Critical safety identification

Uses

- Customer Safety Complaints

---

## CAPA Specialist

Responsibilities

- CAPA recommendations
- Corrective actions
- Preventive actions
- Validation methods
- Responsible owner recommendation

Uses

- Existing CAPA Records
- Quality Decision Rules

---

## M365 Guidance Specialist

Responsibilities

- Microsoft Copilot Studio guidance
- Microsoft 365 documentation
- Power Platform implementation guidance
- Microsoft Learn MCP support

Uses

- Microsoft Learn MCP

---

# Enterprise Tool Boundaries

The solution integrates Microsoft 365 tools while maintaining clear responsibility boundaries.

## Excel Online (Business)

Used as the operational data layer.

### Retrieval Tools

- Get Customer Complaint Records
- Get Product Information
- Get Batch Information
- Get Historical Product Incidents
- Get Product Returns
- Get Sales Summary
- Get Customer Complaint Impact Data
- Get Customer Return Impact Data
- Get Customer Safety Complaints
- Get Existing CAPA Records
- Get Responsible Owners
- Get Quality Investigation Records
- Get Quality Decision Rules

### Update Tools

- Update Customer Complaint
- Update Quality Investigation
- Update CAPA Record

### Create Tools

- Create CAPA Record
- Add a Row into Excel Table

The supervisor owns all enterprise record creation and updates, while specialist agents use retrieval tools only for analysis.

---

## Microsoft Word

Used for automated investigation report generation.

Output includes:

- Investigation Summary
- Incident Details
- Specialist Findings
- Quality Classification
- CAPA Details
- Investigation Outcome

---

## Outlook

Used to notify stakeholders after investigation completion.

Recipients may include:

- Quality Manager
- Product Owner
- CAPA Owner
- Customer Experience Team

---

## Microsoft Learn MCP

Used exclusively by the M365 Guidance Specialist to retrieve Microsoft documentation and implementation guidance.

---

# Orchestration Flow

```
Customer Complaint
        │
        ▼
Quality Supervisor
        │
        ▼
Topic 1 – Incident Intake & Validation
        │
        ▼
Required Specialist Agents
        │
        ▼
Topic 2 – Quality Investigation Decision
        │
        ├─────────────── Informational
        │                     │
        │                     ▼
        │              Update Records
        │
        └────────────── Investigation Required /
                        High Priority /
                        Critical
                                │
                                ▼
                  Topic 3 – CAPA Planning
                                │
                                ▼
                 Update Excel Records
                                │
                                ▼
      Topic 4 – Evidence Update (if applicable)
                                │
                                ▼
                  Selective Specialist Rerun
                                │
                                ▼
            Generate Word Investigation Report
                                │
                                ▼
              Send Outlook Notifications
                                │
                                ▼
                  Investigation Completed
```

---

# Design Principles

The architecture follows these principles:

- Hierarchical supervisor-specialist orchestration
- Deterministic topic-based decision making
- Clear separation between orchestration and analysis
- Tool ownership based on responsibility
- Evidence-driven investigation workflow
- Selective reassessment to avoid unnecessary recomputation
- Complete auditability and traceability
- Microsoft 365 native integration using Excel, Word, Outlook and MCP