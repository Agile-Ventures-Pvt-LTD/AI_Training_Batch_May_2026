# CAP-001 — Sleepsia Quality Intelligence Control Tower

## 1. Project Information

| Field | Details |
|---|---|
| Participant | **Aditya Sodani** |
| Repository Path | `submissions/project-build/ms-copilot-studio/firstname-lastname/cap-001_sleepsia_quality_intelligence_control_tower` |
| Agent Name | Sleepsia Quality Supervisor |
| Agent URL | **https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/b44a0c5f-7f94-f111-b8dc-000d3af21e08/overview** |
| Project Build | CAP-001 |
| Completion Status | **[Completed]** |

---

## 2. Project Summary

The **Sleepsia Quality Intelligence Control Tower** is a Microsoft Copilot Studio solution designed to support quality investigation and CAPA decision-making.

The solution uses a **Quality Supervisor** agent to coordinate specialist analyses, apply explicit quality-decision precedence, perform CAPA planning and ownership, and support evidence-driven reassessment.

The implemented architecture separates:

- Intake and validation
- Quality investigation decision-making
- CAPA planning and ownership
- Evidence update and selective reassessment
- Specialist-agent analysis
- Enterprise data and tool access
- Reporting and notification

The Supervisor consolidates specialist findings rather than independently replacing specialist analyses.

---

## 3. Mandatory Topics

### Topic 1 — Intake & Validation

**Purpose:** Validate an incoming complaint before allowing quality investigation to proceed.

Key validation checks:

- ComplaintID exists
- OrderID exists
- SKU exists in Product Master
- BatchID exists where supplied
- BatchID maps to the supplied SKU
- ComplaintDate is valid
- Category exists
- Severity is valid
- Duplicate complaint has not already been processed

**Outputs:**

- ValidationStatus
- ValidationReason

Only valid intake records proceed to the quality investigation stage.

---

### Topic 2 — Quality Investigation Decision

**Purpose:** Consolidate specialist findings using explicit policy precedence and assign exactly one final classification.

The decision logic evaluates:

1. Safety override
2. Potential safety cluster
3. Complaint cluster threshold
4. Return-rate threshold
5. Previous incident history
6. Missing evidence
7. Overdue CAPA
8. Informational fallback

**Outputs:**

- FinalClassification
- DecisionRationale
- SourceFindings

The topic is designed so that the first applicable policy rule determines the final classification.

---

### Topic 3 — CAPA Planning & Ownership

**Purpose:** Convert an applicable quality classification into an actionable CAPA plan.

The topic receives:

- Incident ID
- Final classification

It supports:

- Containment action
- Corrective recommendation
- Preventive recommendation
- OwnerRole
- OwnerName
- Target date
- Validation method
- CAPA_Register update
- CAPA summary returned to the Supervisor

The Owner lookup retrieves ownership information from the Owners table.

---

### Topic 4 — Evidence Update & Selective Reassessment

**Purpose:** Reassess a quality case when evidence changes without unnecessarily rerunning unaffected specialist analyses.

The topic:

1. Identifies changed evidence
2. Determines stale specialist findings
3. Reruns only stale specialists
4. Preserves unaffected findings
5. Increments ReassessmentCount
6. Re-enters the Quality Investigation Decision
7. Routes the case to Manual Review when `ReassessmentCount > 2`

The intended behavior is selective rather than full reprocessing.

---

## 4. Specialist Agents

The Supervisor architecture includes specialist analysis for:

- Complaint Pattern
- Returns
- Product/Batch
- Safety
- CAPA

Specialist agents provide findings to the Quality Supervisor.

The Supervisor consolidates these findings and applies the configured decision precedence.

---

## 5. Data Sources

The solution uses operational and policy information including:

- Customer Complaints
- Product Master
- Batch Register
- Returns
- Quality Incidents
- CAPA Register
- Owners
- Sleepsia quality policy and knowledge sources

Exact source configuration and retrieval evidence are documented in `knowledge-sources.md`.

---

## 6. Tools and Integrations

### Excel

Excel is used for structured operational data and lookup/update operations.

Examples:

- Complaint validation
- Product validation
- Batch validation
- Owner lookup
- CAPA Register operations

**Implementation Status:** [ADD STATUS]

### Word

Word integration is intended to generate a quality investigation/CAPA report.

**Implementation Status:** [ADD STATUS]

### Outlook

Outlook integration is intended to send quality/CAPA notifications to the assigned owner or relevant quality role.

**Implementation Status:** [ADD STATUS]

### MCP

MCP implementation/configuration and discovered tools are documented separately in `mcp-implementation.md`.

**MCP Status:** [ADD STATUS]

---

## 7. End-to-End Orchestration

```text
User Request
     |
     v
Quality Supervisor
     |
     v
Topic 1 — Intake & Validation
     |
     +---- Invalid ----> Stop / Return validation reason
     |
     v
Topic 2 — Quality Investigation Decision
     |
     +---- Final Classification
     |
     v
Topic 3 — CAPA Planning & Ownership
     |
     +---- Owner Lookup
     +---- CAPA Register
     +---- Word Report [if enabled]
     +---- Outlook Notification [if enabled]
     |
     v
Final Supervisor Response