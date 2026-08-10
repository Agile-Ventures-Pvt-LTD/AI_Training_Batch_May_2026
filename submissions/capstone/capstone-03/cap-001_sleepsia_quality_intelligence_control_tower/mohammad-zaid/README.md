# README.md

# CAP-001 — Sleepsia Product Quality & Customer Experience Intelligence Control Tower

## Project Information

| Field | Details |
|---|---|
| Project ID | CAP-001 |
| Project Name | Sleepsia Product Quality & Customer Experience Intelligence Control Tower |
| Platform | Microsoft Copilot Studio |
| Participant | [Participant Name] |
| Agent | Quality Supervisor |
| Agent URL | [Copilot Studio Agent URL] |
| Primary Channel | Microsoft Teams |
| Microsoft 365 Copilot | [Available / Tenant Restricted] |
| Project Status | Completed |

## Solution Summary

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower is an autonomous multi-agent quality-governance solution built in Microsoft Copilot Studio.

The system detects unprocessed customer complaints through a recurrence trigger, validates required complaint information, coordinates independent specialist analysis, consolidates specialist findings, applies deterministic quality rules, manages CAPA and evidence requirements, performs selective reassessment when new evidence is supplied, and preserves final decisions through the Quality Supervisor.

The Quality Supervisor is the sole final decision owner. Specialist agents provide domain-specific findings but do not independently determine final incident severity or external or internal actions.

## Core Capabilities

- Autonomous detection of unprocessed complaint records.
- Complaint identifier and evidence validation.
- Prevention of duplicate complaint processing.
- Parallel specialist analysis with Supervisor fan-in.
- Hierarchical Supervisor-to-specialist orchestration.
- Deterministic quality decision precedence.
- Safety-driven Critical escalation.
- Investigation and High-Priority routing.
- Missing-evidence handling.
- CAPA ownership and escalation.
- Selective reassessment when evidence changes.
- Bounded reassessment cycles.
- Specialist retry and fallback handling.
- Quality incident and CAPA state updates.
- Word quality-report generation.
- Conditional Outlook notification.
- Microsoft Learn MCP integration for M365 guidance.
- Interactive employee queries through the published agent.

## Agent Architecture

### Quality Supervisor

The Quality Supervisor is the parent orchestrator and sole final decision owner.

Responsibilities include:

- Trigger orchestration.
- Intake validation.
- Specialist selection and delegation.
- Fan-out/fan-in coordination.
- Rule precedence.
- Final incident classification.
- Reassessment control.
- CAPA and evidence workflow control.
- Authorization of Word report generation.
- Authorization of Outlook notification.

### Specialist Agents

The solution contains domain-specific specialists with non-overlapping responsibilities:

- Complaint Pattern Specialist
- Returns Specialist
- Product-Batch Specialist
- Customer Impact Specialist
- Safety Specialist
- CAPA Specialist
- M365 Guidance Specialist

Specialist agents provide evidence-based findings to the Quality Supervisor and do not independently issue the final quality decision.

## Autonomous Workflow

```text
Recurrence Trigger
       |
       v
Read unprocessed complaints
       |
       v
Incident Intake & Validation
       |
       v
Validate required evidence
       |
       v
Parallel Specialist Analysis
       |
       +--> Complaint Pattern Specialist
       +--> Returns Specialist
       +--> Product-Batch Specialist
       +--> Customer Impact Specialist
       |
       v
Supervisor Fan-In
       |
       v
Quality Investigation Decision
       |
       +--> Critical Escalation
       +--> Investigation Required
       +--> High-Priority
       +--> Insufficient Evidence
       +--> Monitoring
       |
       v
CAPA / Evidence / Reassessment Path
       |
       v
Supervisor Validation
       |
       +--> Word Quality Report
       +--> Excel State Update
       +--> Outlook Notification

```bash
submissions/
└── project-build/
    └── ms-copilot-studio/
        └── firstname-lastname/
            └── cap-001_sleepsia_quality_intelligence_control_tower/
                ├── README.md
                ├── architecture.md
                ├── orchestration-patterns.md
                ├── custom-topics.md
                ├── knowledge-sources.md
                ├── mcp-implementation.md
                ├── tool-implementation.md
                ├── publishing.md
                ├── test-report.md
                ├── ai-usage-declaration.md
                └── known-limitations.md
```