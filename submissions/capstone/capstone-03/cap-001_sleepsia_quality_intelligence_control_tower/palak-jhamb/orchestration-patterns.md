# Orchestration Patterns

## Project
**Sleepsia Quality & Customer Experience Intelligence Control Tower**

## Overview

The solution follows a **multi-agent orchestration architecture** built in Microsoft Copilot Studio. The **Quality Supervisor** acts as the parent orchestrator, coordinating specialist agents, custom topics, and enterprise tools to execute end-to-end product quality investigations.

The implementation combines **hierarchical, sequential, parallel, conditional, loop, and fallback orchestration** to ensure investigations are accurate, scalable, and audit-ready.

---

# 1. Hierarchical Orchestration

## Purpose

A parent-child architecture is used where the **Quality Supervisor** controls the entire workflow and delegates specialized tasks to child agents.

The supervisor is the only agent responsible for:

- Starting investigations
- Delegating work
- Applying quality rules
- Making the final classification
- Approving CAPA
- Updating enterprise records
- Closing investigations

### Child Agents

| Agent | Responsibility |
|--------|---------------|
| Complaint Pattern Specialist | Complaint clustering and trend analysis |
| Returns Specialist | Return rate and return trend analysis |
| Product & Batch Specialist | Product, SKU, batch and manufacturing investigation |
| Customer Impact Specialist | Customer/business impact assessment |
| Safety Specialist | Safety and risk evaluation |
| CAPA Specialist | Generate CAPA recommendations |
| M365 Guidance Specialist | Microsoft Copilot Studio and Microsoft 365 guidance |

---

# 2. Sequential Orchestration

The supervisor executes investigation steps in a predefined sequence.

### Workflow

1. Receive investigation request
2. Retrieve Excel investigation records
3. Invoke **Topic 1 – Incident Intake & Validation**
4. If valid, invoke required specialist agents
5. Collect specialist findings
6. Invoke **Topic 2 – Quality Investigation Decision**
7. Determine final quality classification
8. If required, invoke **Topic 3 – CAPA Planning & Ownership**
9. Review CAPA recommendations
10. Update Excel records
11. Generate investigation report (Word)
12. Send stakeholder notifications (Outlook)
13. Close investigation

---

# 3. Parallel Orchestration

Independent specialist agents execute simultaneously whenever possible to reduce investigation time.

Typical parallel execution includes:

- Complaint Pattern Specialist
- Returns Specialist
- Product & Batch Specialist
- Customer Impact Specialist
- Safety Specialist

The supervisor waits until all required specialist responses are received before proceeding to the decision stage.

---

# 4. Conditional Orchestration

Decision points determine the next action based on investigation data and topic outputs.

## Topic 1 – Incident Intake & Validation

| Result | Action |
|----------|--------|
| Valid | Continue investigation |
| Invalid | Stop workflow |
| Insufficient Evidence | Request additional information |

---

## Topic 2 – Quality Investigation Decision

Possible outcomes:

- Informational
- Investigation Required
- High-Priority Quality Incident
- Critical Escalation

If the result is:

- **Informational** → Close investigation.
- **Investigation Required / High-Priority / Critical** → Invoke Topic 3.

---

## Topic 3 – CAPA Planning & Ownership

Executed only for qualifying investigations.

Outputs include:

- CAPA ID
- Containment Action
- Corrective Action
- Preventive Action
- Owner
- Target Date
- Validation Method

The supervisor reviews and approves the generated CAPA before updating records.

---

## Topic 4 – Evidence Update & Selective Reassessment

Triggered when new investigation evidence is received.

Possible outcomes:

- No reassessment required
- Selective specialist rerun
- Manual review after reassessment limit

Only affected specialists are re-executed, preserving valid previous findings.

---

# 5. Loop Orchestration

The solution supports controlled reassessment loops through **Topic 4**.

### Process

1. Receive new evidence.
2. Increment reassessment count.
3. Identify stale specialist results.
4. Rerun only affected specialists.
5. Merge new and existing findings.
6. Reapply quality decision rules.
7. Repeat if additional evidence is received.

### Loop Boundary

- Maximum automated reassessments: **2**
- Third reassessment automatically routes the investigation for **Manual Review**.

This prevents infinite investigation cycles.

---

# 6. Fallback Implementation

The supervisor handles failures gracefully without generating unsupported decisions.

## Incomplete Investigation Data

- Stop investigation.
- Request missing information.
- Resume only after required details are available.

---

## Specialist Agent Failure

If a child agent is unavailable:

- Continue with available evidence where appropriate.
- Clearly identify unavailable analysis.
- Do not fabricate findings.

---

## Tool Failure

If an Excel, Word, Outlook, or MCP tool fails:

- Record the failure.
- Preserve completed investigation decisions.
- Continue remaining workflow where possible.
- Notify the user if manual intervention is required.

---

## Reassessment Limit Exceeded

When automated reassessment exceeds the configured limit:

- Stop reassessment.
- Set investigation status to **Manual Review**.
- Escalate to the Quality Manager.

---

# Overall Orchestration Flow

```text
Investigation Request
          │
          ▼
Topic 1 – Incident Intake & Validation
          │
          ▼
Retrieve Excel Records
          │
          ▼
Parallel Specialist Agents
 ├── Complaint Pattern
 ├── Returns
 ├── Product & Batch
 ├── Customer Impact
 └── Safety
          │
          ▼
Topic 2 – Quality Investigation Decision
          │
          ├── Informational
          │      ▼
          │   Close Investigation
          │
          └── Investigation Required / High Priority / Critical
                   │
                   ▼
Topic 3 – CAPA Planning & Ownership
                   │
                   ▼
Approve CAPA
                   │
                   ▼
Update Excel Records
                   │
                   ▼
Generate Word Report
                   │
                   ▼
Send Outlook Notifications
                   │
                   ▼
Close Investigation
                   │
          New Evidence?
                   │
              Yes ▼
Topic 4 – Evidence Update & Selective Reassessment
                   │
        ├── Selective Specialist Rerun
        ├── Preserve Existing Findings
        └── Manual Review (after 2 reassessments)
```

---

# Summary

This project implements:

- **Hierarchical orchestration** through a parent Quality Supervisor and specialist child agents.
- **Sequential orchestration** for the end-to-end investigation lifecycle.
- **Parallel orchestration** for concurrent specialist analyses.
- **Conditional orchestration** using four custom topics to guide workflow decisions.
- **Loop orchestration** with bounded selective reassessment for new evidence.
- **Fallback mechanisms** to handle incomplete data, tool failures, specialist failures, and reassessment limits while maintaining an auditable and reliable investigation process.