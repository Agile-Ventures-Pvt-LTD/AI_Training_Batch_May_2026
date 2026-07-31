
# NovaSphere BC/DR Supervisor Agent Design

## Agent Overview

The **NovaSphere BC/DR Supervisor** is the central orchestration agent responsible for managing the complete BC/DR assessment lifecycle.

It receives assessment requests through an autonomous trigger, coordinates specialist agents, validates responses, consolidates findings, and controls final report generation and communication.

---

# Responsibilities

The Supervisor Agent performs the following activities:

- Receives assessment request trigger payload.
- Identifies the application requiring assessment.
- Retrieves required application and assessment data.
- Delegates analysis tasks to specialist agents.
- Passes relevant context to each specialist.
- Collects specialist outputs.
- Detects missing or incomplete responses.
- Handles conflicting specialist findings.
- Consolidates assessment results.
- Determines final readiness classification.
- Updates assessment register.
- Authorizes report generation.
- Authorizes stakeholder notification.

---

# Knowledge Source

The Supervisor Agent uses:

- **NovaSphere_BCDR_Policy.docx**

The knowledge source provides BC/DR definitions, readiness criteria, recovery expectations, escalation rules, and assessment guidelines.

---

# Tools Used

## Get Assessment Requests

Purpose:
- Retrieves incoming BC/DR assessment requests triggered by new file creation.

---

## Get Application Details

Purpose:
- Retrieves application information required for assessment.

Information includes:
- Application details
- Business ownership
- Technical ownership
- Hosting information
- Recovery configuration

---

## Get Risk Scoring Rules

Purpose:
- Retrieves predefined BC/DR risk classification rules.

Used for:
- Gap severity evaluation
- Readiness classification support

---

## Update Assessment Register

Purpose:
- Updates assessment progress and final assessment status.

Updates include:
- Assessment status
- Readiness classification
- Risk summary
- Report generation status
- Notification status

---

# Agent Orchestration Flow

```

Autonomous Trigger
|
↓
NovaSphere BC/DR Supervisor
|
↓
Retrieve Assessment Information
|
↓
Invoke Specialist Agents
|
↓
Collect Specialist Outputs
|
↓
Validate Findings
|
↓
Consolidate Assessment
|
↓
Final Readiness Classification
|
↓
Reporting & Communication

```

---

# Specialist Delegation

The Supervisor delegates tasks to:

| Specialist Agent | Responsibility |
|---|---|
| Application Criticality Specialist | Business impact and criticality analysis |
| Recovery Requirements Specialist | RTO/RPO and recovery objective analysis |
| Technical Recovery Specialist | Technical resilience evaluation using MCP |
| Risk & Recovery Gap Specialist | Risk identification and readiness recommendation |
| Remediation Planning Specialist | Remediation action creation |
| Reporting & Communication Specialist | Report generation and notification |

---

# Decision Handling

## Missing Specialist Output

If a specialist fails to return a response:

- Supervisor identifies missing information.
- Assessment is marked as incomplete.
- Additional review or reassessment is requested.

---

## Conflicting Specialist Findings

If specialists provide conflicting results:

- Supervisor compares evidence.
- Validates against available knowledge sources.
- Requests reassessment if conflict cannot be resolved.

---

## MCP Failure Handling

If Microsoft Learn MCP is unavailable:

- Supervisor continues using available evidence.
- Technical evidence status is marked unavailable.
- Unsupported technical claims are not generated.

---

# Final Decision Control

The Supervisor Agent is the only component responsible for:

- Final readiness classification.
- Report approval.
- Notification approval.

Specialist agents only provide recommendations and findings.

