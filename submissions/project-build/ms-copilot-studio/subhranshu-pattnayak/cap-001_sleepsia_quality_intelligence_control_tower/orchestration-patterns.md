# Orchestration Patterns

## Overview

The Sleepsia Quality Intelligence Control Tower follows a supervisor-specialist orchestration model.

The Quality Supervisor coordinates workflow execution, invokes specialists, executes decision topics, and manages investigation outcomes.

---

## Supervisor-Orchestrator Pattern

The Quality Supervisor acts as the central orchestrator.

Responsibilities include:

- Complaint intake
- Specialist invocation
- Investigation coordination
- Classification processing
- Incident management
- CAPA initiation
- Reassessment processing
- Report generation
- Notification processing

Specialists provide evidence and analysis only.

Final investigation decisions are controlled by the Quality Supervisor.

---

## Specialist Delegation Pattern

Investigation activities are delegated to specialized agents.

| Specialist | Responsibility |
|------------|---------------|
| Complaint Pattern Specialist | Complaint pattern analysis |
| Returns Specialist | Returns analysis |
| Product/Batch Specialist | Product and batch validation |
| Customer Impact Specialist | Customer impact analysis |
| CAPA Specialist | CAPA generation |
| M365 Guidance Specialist | MCP-based information retrieval |

Each specialist operates within a defined scope and returns findings to the Quality Supervisor.

---

## Evidence Aggregation Pattern

Specialist findings are collected by the Quality Supervisor.

The supervisor combines specialist outputs and workbook data to build investigation inputs used by the Quality Investigation Decision topic.

---

## Policy-Driven Decision Pattern

Investigation classifications are determined through the Quality Investigation Decision topic.

Policy precedence:

1. Safety Override
2. Complaint Pattern Rules
3. Return Rate Rules
4. Previous Incident Rules
5. Missing Evidence Rules
6. CAPA Escalation Rules
7. Reassessment Rules

Safety Override always takes precedence.

---

## Incident Management Pattern

The Quality Supervisor determines whether a matching incident already exists.

If a matching incident exists:

- Existing incident information is used.
- Reassessment history is preserved.

If no matching incident exists:

- A new incident record is created.

---

## Reassessment Pattern

When reassessment conditions are met:

- Existing incident information is retrieved.
- Reassessment processing is executed.
- Relevant specialists may be reinvoked.
- Decision logic may be rerun using updated evidence.

---

## Interactive Utilization Pattern

User-driven interactions operate in read-only mode.

Interactive mode may:

- Retrieve information
- Answer questions
- Provide guidance

Interactive mode does not:

- Create incidents
- Create CAPAs
- Modify records
- Send notifications
- Trigger investigations

---

## Result

The orchestration model centralizes investigation control within the Quality Supervisor while using specialist agents for focused analysis and evidence collection.